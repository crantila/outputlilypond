#! /usr/bin/python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Name:         OutputLilyPond.py
# Purpose:      Outputs music21 Objects into LilyPond Format
#
# Copyright (C) 2012 Christopher Antila
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------
"""
The OutputLilyPond module converts music21 objects into a LilyPond notation
file, then tries to run LilyPond to convert that into a PDF score.

OutputLilyPond is a python library that uses music21; it's intended for use
with music research software.
"""

## Imports
# python standard library
#import os # needed for writing the output file
#from subprocess import Popen, PIPE # for running bash things
#from string import letters as string_letters
#from random import choice as random_choice
from itertools import repeat
# music21
from music21 import clef
from music21 import meter
from music21 import key
#from music21 import stream
#from music21 import metadata
from music21 import layout
from music21 import bar
from music21 import humdrum
#from music21 import tempo
from music21 import note
from music21.duration import Duration
#from music21.note import Note, Rest
#from music21.instrument import Instrument
# output_LilyPond
#from FileOutput import file_outputter
from LilyPondProblems import UnidentifiedObjectError, ImpossibleToProcessError
#from LilyPondSettings import LilyPondSettings


class LilyPondObjectMaker(object):
    """
    Template for class that converts music21 objects to the relevant object in LilyPond notation.
    Some implementations will automatically generate
    """

    # Instance Data:
    # - _as_m21 : the associated music21 object
    # - _as_ly : the associated LilyPond source file representation (a string)
    # - _children : the ___Maker children of this ___Maker object (a NoteMaker, for example, would
    #               have Pitch and Duration children, among others)

    def __init__(self, m21_obj):
        """
        Create a new LilyPondObjectMaker instance. For some objects, this will also generate the
        LilyPond string corresponding to the objects stored in this LilyPondObjectMaker.

        Parameters
        ----------

        m21_obj : music21.*
            A music21 object
        """
        # NOTE: you need not re-implmement this in subclasses
        # NOTE2: this method does not pre-calculate the LilyPond object
        self._as_m21 = m21_obj
        self._as_ly = None
        self._children = None

    def _calculate_lily(self):
        """
        Generate the LilyPond string corresponding to the objects stored in this
        LilyPondObjectMaker.
        """
        # NOTE: you must re-implement this in subclasses
        self._as_ly = ''

    def get_lilypond(self):
        """
        Return the LilyPond source code for this object, as a string. If the string was not yet
        calculated, it is calculated before returning.
        """
        # NOTE: you need not re-implmement this in subclasses
        if self._as_ly is None:
            self._calculate_lily()
        return self._as_ly

    def get_music21(self):
        """
        Return the music21 object stored in this object.
        """
        # NOTE: you need not re-implmement this in subclasses
        return self._as_m21


class NoteMaker(LilyPondObjectMaker):
    """
    Class corresponding to a music21.note.Note object. Holds information about the pitch class,
    register, duration, articulation, etc., about a Note.
    """

    def __init__(self, m21_obj, known_tuplet=False):
        """
        Create a new NoteMaker instance. The constructor pre-calculates the LilyPond format.

        Parameters
        ----------

        known_tuplet : boolean
            Whether we know this Note is part of a tuplet. Default is False.
        """
        super(NoteMaker, self).__init__(m21_obj)
        self._known_tuplet = known_tuplet
        self._calculate_lily()

    def _calculate_lily(self):
        """
        Prepare and return the LilyPond source code for this Note.
        """
        # NOTE: I removed a "known_tuplet" argument that I said was directly passed
        # to duration_to_lily

        post = ''

        if len(self._as_m21.duration.components) > 1:
            # We obviously can't ask for the pitch of a Rest
            the_pitch = None
            if self._as_m21.isRest:
                the_pitch = 'r'
            else:
                the_pitch = NoteMaker._pitch_to_lily(self._as_m21.pitch)
            # But this should be the same for everybody
            for durational_component in self._as_m21.duration.components:
                post = the_pitch
                post += NoteMaker._duration_to_lily(durational_component, self._known_tuplet)
                post += '~ '
            post = post[:-2]
        elif self._as_m21.isRest:
            post += "r" + NoteMaker._duration_to_lily(self._as_m21.duration, self._known_tuplet)
        elif hasattr(self._as_m21, 'lily_invisible') and \
        True == self._as_m21.lily_invisible:
            post += "s" + NoteMaker._duration_to_lily(self._as_m21.duration, self._known_tuplet)
        else:
            post += NoteMaker._pitch_to_lily(self._as_m21.pitch) + \
                NoteMaker._duration_to_lily(self._as_m21.duration, self._known_tuplet)

        if self._as_m21.tie is not None:
            if self._as_m21.tie.type is 'start':
                post += '~'

        if hasattr(self._as_m21, 'lily_markup'):
            post += str(self._as_m21.lily_markup)

        self._as_ly = post

    @staticmethod
    def _octave_num_to_lily(num):
        """
        Calculate the LilyPond symbol corresponding to the octave number.

        Parameter:
        ----------

        num : integer
            The octave number to convert to a LilyPond register symbol, as in '4' for the octave
            in which "middle C" occurs.

        Returns:
        --------

        a string
            A string that represents the string to append to a note to put it in the right octave.

        >>> NoteMaker._octave_num_to_lily(1)
        ",,"
        >>> NoteMaker._octave_num_to_lily(6)
        "'''"
        """
        dictionary_of_octaves = {0: ",,,", 1: ",,", 2: ",", 3: "", 4: "'", 5: "''", 6: "'''",
            7: "''''", 8: "'''''", 9: "''''''", 10: "''''''", 11: "''''''", 12: "'''''''''"}

        if num in dictionary_of_octaves:
            return dictionary_of_octaves[num]
        else:
            raise UnidentifiedObjectError('Octave out of range: ' + str(num))

    @staticmethod
    def _pitch_to_lily(start_p, include_octave=True):
        """
        Calculate the LilyPond pitch name for the pitch.Pitch.

        Parameters
        ----------

        start_p : music21.pitch.Pitch
            The pitch to convert to its LilyPond string version.

        include_octave : boolean
            Whether to include the commas or apostrophes that indicate the absolute octave of a
            pitch. Default is True.

        Returns
        -------

        a string
            The string-wise representation of this Pitch in LilyPond format.
        """
        start_pc = start_p.name.lower()
        post = start_pc[0]

        for accidental in start_pc[1:]:
            if '-' == accidental:
                post += 'es'
            elif '#' == accidental:
                post += 'is'

        if include_octave:
            if start_p.octave is None:
                post += NoteMaker._octave_num_to_lily(start_p.implicitOctave)
            else:
                post += NoteMaker._octave_num_to_lily(start_p.octave)

        return post

    @staticmethod
    def _duration_to_lily(dur, known_tuplet=False):
        """
        Convert a Duration to its LilyPond-format version.

        Parameters
        ----------

        dur : music21.duration.Duration
            The duration to convert to its LilyPond-format length string.

        known_tuplet : boolean
            If we know this Duration is part of a tuplet.

        Returns
        -------

        a string
            The LilyPond string corresonding to the duration of this Duration.
        """

        # First of all, we can't deal with tuplets or multiple-component durations
        # in this method. We need process_measure() to help.
        if dur.tuplets is not ():
            # We know either there are multiple components or we have part of a
            # tuplet, we we need to find out which.
            if len(dur.components) > 1:
                # We have multiple components
                raise ImpossibleToProcessError('Cannot process durations with ' +
                    'multiple components (received ' + str(dur.components) +
                    ' for quarterLength of ' + str(dur.quarterLength) + ')')
            elif known_tuplet:
                # We have part of a tuple. This isn't necessarily a problem; we'll
                # assume we are given this by process_measure() and that it knows
                # what's going on. But, in tuplets, the quarterLength doesn't match
                # the type of written note, so we'll make a new Duration with an
                # adjusted quarterLength
                dur = Duration(dur.type)
            else:
                msg = 'duration_to_lily(): Cannot process tuplet components'
                raise ImpossibleToProcessError(msg)

        # We need both a list of our potential durations and a dictionary of what
        # they mean in LilyPond terms.
        list_of_durations = [16.0, 8.0, 4.0, 2.0, 1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125]
        dictionary_of_durations = {16.0: '\longa', 8.0: '\\breve', 4.0: '1', 2.0: '2', 1.0: '4',
            0.5: '8', 0.25: '16', 0.125: '32', 0.0625: '64', 0.3125: '128'}

        # So we only access the quarterLength once
        dur_ql = dur.quarterLength

        # If there are no dots, the value should be in the dictionary, and we can
        # simply return it.
        if dur_ql in dictionary_of_durations:
            return dictionary_of_durations[dur_ql]
        else:
            # We have to figure out the largest value that will fit, then append the
            # correct number of dots.
            post = ''
            for durat in list_of_durations:
                if (dur_ql - durat) > 0.0:
                    post += dictionary_of_durations[durat]
                    break

            # For every dot in this Duration, append a '.' to "post"
            for _ in repeat(None, dur.dots):
                post += '.'

            return post


class MeasureMaker(object):
    """
    Class corresponding to a music21.stream.Measure object. Holds information about all the notes
    and chords and other things in the measure.
    """

    def _barline_to_lily(barline):
        """
        Generate the LilyPond-format notation for a music21.bar.Barline object.

        Parameters
        ----------

        barline : music21.bar.Barline
            The barline to convert to LilyPond format.

        Returns
        -------

        a string
            The LilyPond notation for this barline.
        """

        # From the music21 source code... a list of barline styles...
        #
        # barStyleList = ['regular', 'dotted', 'dashed', 'heavy', 'double', 'final',
        #               'heavy-light', 'heavy-heavy', 'tick', 'short', 'none']

        dictionary_of_barlines = {'regular': "|", 'dotted': ":", 'dashed': "dashed",
            'heavy': "|.|", 'double': "||", 'final': "|.", 'heavy-light': ".|",
            'heavy-heavy': ".|.", 'tick': "'", 'short': "'", 'none': ""}

        post = '\\bar "'

        if barline.style in dictionary_of_barlines:
            post += dictionary_of_barlines[barline.style] + '"'
            return post
        else:
            start_msg = 'Barline type not recognized ('
            UnidentifiedObjectError(start_msg + barline.style + ')')

    def _calculate_lily(self):
        """
        Returns a str that is one line of a LilyPond score, containing one Measure.

        Input should be a Measure.
        """

        post = "\t"

        # Hold whether this Measure is supposed to be "invisible"
        invisible = False
        if hasattr(self._as_m21, 'lily_invisible'):
            invisible = self._as_m21.lily_invisible

        # Add the first requirement of invisibility
        if invisible:
            post += '\stopStaff\n\t'

        # first check if it's a partial (pick-up) measure
        if 0.0 < self._as_m21.duration.quarterLength < self._as_m21.barDuration.quarterLength:
            # NOTE: This next check could have been done in the first place, but it's
            # a work-around for what I think is a bug, so I didn't.
            if round(self._as_m21.duration.quarterLength, 2) < \
            self._as_m21.barDuration.quarterLength:
                # But still, we may get something stupid...
                try:
                    post += "\\partial " + \
                        NoteMaker._duration_to_lily(self._as_m21.duration) + \
                        "\n\t"
                except UnidentifiedObjectError:
                    # ... so if it doesn't work the first time, it may in fact be a
                    # partial measure; we'll try rounding and see what we can get.
                    rounded_duration = Duration(round(self._as_m21.duration.quarterLength, 2))
                    post += "\\partial " + NoteMaker._duration_to_lily(rounded_duration) + "\n\t"

        # Make self._as_m21 an iterable, so we can pull in multiple elements when we
        # need to deal with tuplets.
        self._as_m21 = iter(self._as_m21)

        # now fill in all the stuff
        for obj in self._as_m21:
            # Note or Rest
            if isinstance(obj, note.Note) or isinstance(obj, note.Rest):
                # TODO: is there a situation where I'll ever need to deal with
                # multiple-component durations for a single Note/Rest?
                # ANSWER: yes, sometimes

                # Is it a full-measure rest?
                if isinstance(obj, note.Rest) and \
                self._as_m21.srcStream.barDuration.quarterLength == obj.quarterLength:
                    if invisible:
                        post += 's' + NoteMaker._duration_to_lily(obj.duration) + ' '
                    else:
                        post += 'R' + NoteMaker._duration_to_lily(obj.duration) + ' '
                # Is it the start of a tuplet?
                elif obj.duration.tuplets is not None and len(obj.duration.tuplets) > 0:
                    number_of_tuplet_components = obj.duration.tuplets[0].numberNotesActual
                    in_the_space_of = obj.duration.tuplets[0].numberNotesNormal
                    post += '\\times ' + str(in_the_space_of) + '/' + \
                        str(number_of_tuplet_components) + ' { ' + \
                        NoteMaker(obj, True).get_lilypond() + " "
                    # For every tuplet component...
                    for _ in repeat(None, number_of_tuplet_components - 1):
                        post += NoteMaker(next(self._as_m21), True).get_lilypond() + ' '
                    post += '} '
                # It's just a regular note or rest
                else:
                    post += NoteMaker(obj).get_lilypond() + ' '

            #if isinstance(obj, Note):
                #post += note_to_lily(obj) + " "
            #elif isinstance(obj, Rest):
                ## If it's a full-measure rest, we'll use the upper-case symbol so
                ## the rest is placed in the middle of the bar. This is something
                ## note_to_lily() couldn't pick up without access to self._as_m21
                #if self._as_m21.barDuration.quarterLength == obj.quarterLength:
                #post += 'R' + duration_to_lily(obj.duration) + ' '
                #else:
                #post += note_to_lily(obj) + " "
            # Clef
            elif isinstance(obj, clef.Clef):
                if invisible:
                    post += "\\once \\override Staff.Clef #'transparent = ##t\n\t"

                if isinstance(obj, clef.TrebleClef):
                    post += "\\clef treble\n\t"
                elif isinstance(obj, clef.BassClef):
                    post += "\\clef bass\n\t"
                elif isinstance(obj, clef.TenorClef):
                    post += "\\clef tenor\n\t"
                elif isinstance(obj, clef.AltoClef):
                    post += "\\clef alto\n\t"
                else:
                    raise UnidentifiedObjectError('Clef type not recognized: ' + obj)
            # Time Signature
            elif isinstance(obj, meter.TimeSignature):
                if invisible:
                    post += "\\once \\override Staff.TimeSignature #'transparent = ##t\n\t"

                post += "\\time " + str(obj.beatCount) + "/" + \
                        str(obj.denominator) + "\n\t"
            # Key Signature
            elif isinstance(obj, key.KeySignature):
                pitch_and_mode = obj.pitchAndMode
                if invisible:
                    post += "\\once \\override Staff.KeySignature #'transparent = ##t\n\t"

                if 2 == len(pitch_and_mode) and pitch_and_mode[1] is not None:
                    post += "\\key " + \
                        NoteMaker._pitch_to_lily(pitch_and_mode[0], include_octave=False) + \
                        " \\" + pitch_and_mode[1] + "\n\t"
                else:
                    # We'll have to assume it's \major, because music21 does that.
                    post += "\\key " + \
                        NoteMaker._pitch_to_lily(pitch_and_mode[0], include_octave=False) + \
                        " \\major\n\t"
            # Barline
            elif isinstance(obj, bar.Barline):
                # There's no need to write down a regular barline, because they tend
                # to happen by themselves. Of course, this will have to change once
                # we have the ability to override the standard barline.
                if 'regular' != obj.style:
                    post += '\n\t' + MeasureMaker._barline_to_lily(obj) + " "
            # PageLayout and SystemLayout
            elif isinstance(obj, layout.SystemLayout) or isinstance(obj, layout.PageLayout):
                # I don't know what to do with these undocumented features.
                # NB: They now have documentation, so I could check up on this...
                pass
            # **kern importer garbage... well, it's only garbage to us
            elif isinstance(obj, humdrum.spineParser.MiscTandem):
                # http://mit.edu/music21/doc/html/moduleHumdrumSpineParser.html
                # Is there really nothing we can use this for? Seems like these
                # exist only to help music21 developers.
                pass
            # We don't know what it is, and should probably figure out!
            else:
                raise UnidentifiedObjectError('Unknown object in Bar: ' + str(obj))

        # Append a bar-check symbol, if there was anything outputted.
        if len(post) > 1:
            post += "|\n"

        # The final requirement of invisibility
        if invisible:
            post += '\t\\startStaff\n'

        self._as_ly = post


class AnalysisVoiceMaker(object):
    """
    Processes a music21 Part that has the "lily_analysis_voice attribute," and it is True.

    This is turned into a Part that has no staff lines, is printed in its score order, and has all
    "lily_markup" attributes attached to 'spacer' notes (i.e., with the letter name "s").
    """

    def _calculate_lily(self):
        """
        Generate the LilyPond string corresponding to the objects stored in this
        LilyPondObjectMaker.
        """
        # NOTE: at one point, this was very similar to the NoteMaker _calculate_lily() method.

        def space_for_lily(lily_this):
            """
            Something something inner function.
            """
            post = 's'

            if len(lily_this.duration.components) > 1:
                for durational_component in lily_this.duration.components:
                    post += NoteMaker._duration_to_lily(durational_component) + '~ '
                    post = post[:-2]
            else:
                post += NoteMaker._duration_to_lily(lily_this.duration)

            if lily_this.tie is not None:
                if lily_this.tie.type is 'start':
                    post += '~'

            if hasattr(lily_this, 'lily_markup'):
                post += str(lily_this.lily_markup)

            return post

        # Just try to fill in all the stuff
        post = ''
        for obj in self._as_m21:
            post += '\t' + space_for_lily(obj) + '\n'
        self._as_ly = post
