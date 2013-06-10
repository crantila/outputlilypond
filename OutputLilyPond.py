#! /usr/bin/python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Filename: OutputLilyPond.py
# Purpose: Outputs music21 Objects into LilyPond Format
#
# Copyright (C) 2012, 2013 Christopher Antila
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
from subprocess import Popen, PIPE  # for running bash things
import random
from itertools import repeat
# music21
from music21 import clef, meter, key, stream, metadata, layout, bar, humdrum, tempo, note, \
    instrument, expressions, chord, duration, text
#from music21.duration import Duration
# output_LilyPond
#from FileOutput import file_outputter
from LilyPondProblems import UnidentifiedObjectError, ImpossibleToProcessError
from LilyPondSettings import LilyPondSettings


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


def _clef_to_lily(the_clef, append=u'\n', invisible=False):
    """
    Generate the LilyPond-format notation for a music21.clef.* object.

    Parameters
    ----------

    the_clef : music21.clef.*
        One of:
        - Treble8vbClef
        - Treble8vaClef
        - Bass8vbClef
        - Bass8vaClef
        - TrebleClef
        - BassClef
        - TenorClef
        - AltoClef

    append : string
        Append this to the end of every line of code generated. This is intended to be used for
        newline and tab characters, for setting up the line after the ones returned by this
        function. The default value is u'\n' meaning a single newline character.

    invisible : boolean
        Whether to override the #'transparent property of the clef to ##t in LilyPond

    Returns
    -------

    string
        The LilyPond-format notation for this clef.

    Raises
    ------

    UnidentifiedObjectError
        If the Clef is not of a known type.
    """
    post = u"\\once \\override Staff.Clef #'transparent = ##t" + append if invisible else u''

    clef_dict = {clef.Treble8vbClef: u"\\clef \"treble_8\"",
                 clef.Treble8vaClef: u"\\clef \"treble^8\"",
                 clef.Bass8vbClef: u"\\clef \"bass_8\"",
                 clef.Bass8vaClef: u"\\clef \"bass^8\"",
                 clef.TrebleClef: u"\\clef treble",
                 clef.BassClef: u"\\clef bass",
                 clef.TenorClef: u"\\clef tenor",
                 clef.AltoClef: u"\\clef alto",
                 clef.FBaritoneClef: u"\\clef varbaritone",
                 clef.CBaritoneClef: u"\\clef baritone",
                 clef.FrenchViolinClef: u"\\clef french",
                 clef.MezzoSopranoClef: u"\\clef mezzosoprano",
                 clef.PercussionClef: u"\\clef percussion",
                 clef.SopranoClef: u"\\clef soprano",
                 clef.SubBassClef: u"\\clef subbass"}

    clef_type = type(the_clef)
    if clef_type in clef_dict:
        return post + clef_dict[clef_type] + append
    else:
        raise UnidentifiedObjectError('Clef type not recognized: ' + unicode(the_clef))


def _string_of_n_letters(n):
    """
    Generate a string of n pseudo-random letters.

    This function is currently used to help create unique part names in scores.
    """
    post = u''
    for _ in repeat(None, n):
        post += random.choice(u'qwertyuiopasdfghjklzxcvbnm')
    return post


def _barline_to_lily(barline):
    """
    Generate the LilyPond-format notation for a music21.bar.Barline object.

    Parameters
    ----------

    barline : music21.bar.Barline
        The barline to convert to LilyPond format. The 'style' property must be one of these:
        'regular', 'dotted', 'dashed', 'heavy', 'double', 'final', 'heavy-light', 'heavy-heavy',
        'tick', 'short', or 'none'.

    Returns
    -------

    a string
        The LilyPond notation for this barline.

    Raises
    ------

    UnidentifiedObjectError
        If the barline's "style" property is not recognized
    """

    # From the music21 source code... a list of barline styles...
    #
    # barStyleList = ['regular', 'dotted', 'dashed', 'heavy', 'double', 'final',
    #               'heavy-light', 'heavy-heavy', 'tick', 'short', 'none']

    dictionary_of_barlines = {'regular': u"|", 'dotted': u":", 'dashed': u"dashed",
        'heavy': u"|.|", 'double': u"||", 'final': u"|.", 'heavy-light': u".|",
        'heavy-heavy': u".|.", 'tick': u"'", 'short': u"'", 'none': u""}

    if barline.style in dictionary_of_barlines:
        return u'\\bar "' + dictionary_of_barlines[barline.style] + u'"'
    else:
        start_msg = 'Barline type not recognized ('
        raise UnidentifiedObjectError(start_msg + barline.style + ')')


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

    # Every Duration should actually have some duration.
    if 0.0 == dur.quarterLength:
        msg = u'_duration_to_lily(): Cannot process quarterLength of 0.0'
        raise ImpossibleToProcessError(msg)

    # First of all, we can't deal with tuplets or multiple-component durations
    # in this method. We need process_measure() to help.
    if dur.tuplets is not ():
        # We know either there are multiple components or we have part of a
        # tuplet, we we need to find out which.
        if len(dur.components) > 1:
            # We have multiple components
            raise ImpossibleToProcessError('Cannot process durations with ' +
                'multiple components (received ' + unicode(dur.components) +
                ' for quarterLength of ' + unicode(dur.quarterLength) + ')')
        elif known_tuplet:
            # We have part of a tuple. This isn't necessarily a problem; we'll
            # assume we are given this by process_measure() and that it knows
            # what's going on. But, in tuplets, the quarterLength doesn't match
            # the type of written note, so we'll make a new Duration with an
            # adjusted quarterLength
            dur = duration.Duration(dur.type)
        else:
            msg = 'duration_to_lily(): Cannot process tuplet components'
            raise ImpossibleToProcessError(msg)

    # We need both a list of our potential durations and a dictionary of what
    # they mean in LilyPond terms.
    list_of_durations = [16.0, 8.0, 4.0, 2.0, 1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125]
    dictionary_of_durations = {16.0: u'\longa', 8.0: u'\\breve', 4.0: u'1', 2.0: u'2', 1.0: u'4',
        0.5: u'8', 0.25: u'16', 0.125: u'32', 0.0625: u'64', 0.3125: u'128'}

    # So we only access the quarterLength once
    dur_ql = dur.quarterLength

    # If there are no dots, the value should be in the dictionary, and we can
    # simply return it.
    if dur_ql in dictionary_of_durations:
        return dictionary_of_durations[dur_ql]
    else:
        # We have to figure out the largest value that will fit, then append the
        # correct number of dots.
        post = None
        for durat in list_of_durations:
            if (dur_ql - durat) > 0.0:
                post = dictionary_of_durations[durat]
                break

        # For every dot in this Duration, append a '.' to "post"
        for _ in repeat(None, dur.dots):
            post += u'.'

        return post


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

    >>> _octave_num_to_lily(1)
    ",,"
    >>> _octave_num_to_lily(6)
    "'''"
    """
    dictionary_of_octaves = {0: u",,,", 1: u",,", 2: u",", 3: u"", 4: u"'", 5: u"''", 6: u"'''",
        7: u"''''", 8: u"'''''", 9: u"''''''", 10: u"'''''''", 11: u"''''''''", 12: u"'''''''''"}

    if num in dictionary_of_octaves:
        return dictionary_of_octaves[num]
    else:
        raise UnidentifiedObjectError('Octave out of range: ' + unicode(num))


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
            post += u'es'
        elif '#' == accidental:
            post += u'is'

    if include_octave:
        if start_p.octave is None:
            post += _octave_num_to_lily(start_p.implicitOctave)
        else:
            post += _octave_num_to_lily(start_p.octave)

    return post


def _process_stream(the_stream, the_settings):
    """
    Create a string that contains all the LilyPond syntax for the object.

    Parameters
    ----------

    the_stream : music21.stream.Part
    the_stream : music21.stream.Score
    the_stream : music21.metadata.Metadata
    the_stream : music21.layout.StaffGroup
    the_stream : music21.humdrum.spineParser.MiscTandem
    the_stream : music21.humdrum.spineParser.SpineComment
    the_stream : music21.humdrum.spineParser.GlobalComment
        The object to convert to its LilyPond syntax. If a Part has the "lily_analysis_voice"
        attribute, and it is True, then all Note objects will be turned into spacer objects that
        may contain an annotation, and all Rest objects will be turned into spacer objects without
        an annotation.

    the_settings : LilyPondSettings
        ????

    Returns
    -------

    a string
        The LilyPond syntax for the given music21 object.

    Raises
    ------

    UnidentifiedObjectError
        When the object is of a type not supported by this function.
    """
    obj_type = type(the_stream)

    if obj_type == stream.Score:
        return ScoreMaker(the_stream, the_settings).get_lilypond()
    elif obj_type == stream.Part:
        return PartMaker(the_stream, the_settings).get_lilypond()
    elif obj_type == metadata.Metadata:
        return MetadataMaker(the_stream, the_settings).get_lilypond()
    elif obj_type == layout.StaffGroup:
        # TODO: Figure out how to use this by reading documentation
        return u''
    elif obj_type == humdrum.spineParser.MiscTandem:
        # http://mit.edu/music21/doc/html/moduleHumdrumSpineParser.html
        # Is there really nothing we can use this for? Seems like these exist only to help
        # the music21 developers.
        return u''
    elif obj_type == humdrum.spineParser.GlobalReference:
        # http://mit.edu/music21/doc/html/moduleHumdrumSpineParser.html
        # These objects have lots of metadata, so they'd be pretty useful!
        return u''
    elif obj_type == humdrum.spineParser.GlobalComment:
        # http://mit.edu/music21/doc/html/moduleHumdrumSpineParser.html
        # These objects have lots of metadata, so they'd be pretty useful!
        return u''
    elif obj_type == layout.ScoreLayout:  # TODO: this (as in Lassus duos)
        return u''
    elif obj_type == text.TextBox:  # TODO: this (as in Lassus duos)
        return u''
    else:
        # Anything else, we don't know what it is!
        msg = u'Unknown object in Stream: ' + unicode(the_stream)
        print(msg)  # DEBUG
        #raise UnidentifiedObjectError(msg)


def run_lilypond(filename):
    """
    Given a filename, run lilypond on that file.
    """
    return _run_lilypond(filename, LilyPondSettings())


def _run_lilypond(filename, the_settings):
    """
    Arguments should be a str that is the file name followed by a
    LilyPondSettings object.
    """
    # Make the PDF filename: if "filename" ends with ".ly" then remove it so
    # we don't output to ".ly.pdf"
    pdf_filename = ''
    if 3 < len(filename) and '.ly' == filename[-3:]:
        pdf_filename = filename[:-3]
    else:
        pdf_filename = filename

    # NB: this method returns something that might be interesting
    Popen([the_settings.get_property('lilypond_path'), '--pdf', '-o', pdf_filename, filename],
        stdout=PIPE,
        stderr=PIPE)


def process_score(the_score, the_settings=None):
    """
    Process an entire music21 Score object, turning it into a string that can be output as a
    complete LilyPond source file.

    Parameters
    ----------

    the_score : music21.stream.Score

    the_settings : LilyPondSettings
        Optional settings object. If none is provided, or if "None" is provided, a new instance
        will be created with the default settings.

    Returns
    -------

    string
        This is the LilyPond source file.
    """
    the_settings = LilyPondSettings() if the_settings is None else the_settings
    return _process_stream(the_score, the_settings)


class NoteMaker(LilyPondObjectMaker):
    """
    Class corresponding to a music21.note.Note or Rest object. Holds information about the pitch
    class, register, duration, articulation, etc., about a Note.
    """

    def __init__(self, m21_obj, known_tuplet=False):
        """
        Create a new NoteMaker instance. The constructor pre-calculates the LilyPond format.

        Parameters
        ----------

        m21_obj : music21.note.Note or music21.note.Rest
            The Note or Rest object to turn into LilyPond source code. There are two special
            attributes:
            - lily_invisible (boolean)
                If this attribute is True, the Note or Rest will use the letter 's' rather than
                'r' if it is a Rest or the letter name if it is a Note.
            - lily_markup (string)
                If this attribute exists, its contents will be passed through unicode() then
                appended after (to the right of) the rest of the Note/Rest/object's code. The
                intended purpose is use with the \markup{} command.

        known_tuplet : boolean
            Whether we know this Note is part of a tuplet. Default is False.
        """
        super(NoteMaker, self).__init__(m21_obj)
        self._known_tuplet = known_tuplet

    def _calculate_lily(self):
        """
        Prepare and return the LilyPond source code for this Note.

        Raises
        ------

        Any exceptions raised by the following functions will also be raised by this:
        - _pitch_to_lily()
        - _duration_to_lily()
        """
        post = ''

        # Find the letter: either a pitch, 'r', or 's'
        the_pitch = None
        if hasattr(self._as_m21, 'lily_invisible') and True == self._as_m21.lily_invisible:
            the_pitch = u's'
        elif self._as_m21.isRest:
            the_pitch = u'r'
        else:
            the_pitch = _pitch_to_lily(self._as_m21.pitch)

        # NB: From here to the end of the method, it's the same as ChordMaker._calculate_lily()
        # Find the duration
        if len(self._as_m21.duration.components) > 1:
            # We have a multiple-part duration
            for durational_component in self._as_m21.duration.components:
                post = u''.join([post,
                    the_pitch,
                    _duration_to_lily(durational_component, self._known_tuplet),
                    u'~ '])
            post = post[:-2]
        else:
            # Just a straightforward duration
            post = u''.join([the_pitch,
                _duration_to_lily(self._as_m21.duration, self._known_tuplet)])

        # Add a tie if necessary
        if self._as_m21.tie is not None:
            if u'start' == self._as_m21.tie.type:
                post = u''.join([post, u'~'])

        # Add the \markup{} block, if there is one
        if hasattr(self._as_m21, 'lily_markup'):
            post = u''.join([post, unicode(self._as_m21.lily_markup)])

        # Done
        self._as_ly = post


class ChordMaker(LilyPondObjectMaker):
    """
    Class corresponding to a music21.chord.Chord object. Holds information about the pitch classes,
    registers, duration, articulation, etc., about a Chord.
    """

    def __init__(self, m21_obj, known_tuplet=False):
        """
        Create a new NoteMaker instance. The constructor pre-calculates the LilyPond format.

        Parameters
        ----------

        m21_obj : music21.chord.Chord
            The Chord object to turn into LilyPond source code. There is one special attribute:
            - lily_markup (string)
                If this attribute exists, its contents will be passed through unicode() then
                appended after (to the right of) the rest of the Note/Rest/object's code. The
                intended purpose is use with the \markup{} command.

        known_tuplet : boolean
            Whether we know this Note is part of a tuplet. Default is False.
        """
        super(ChordMaker, self).__init__(m21_obj)
        self._known_tuplet = known_tuplet

    def _calculate_lily(self):
        """
        Prepare and return the LilyPond source code for this Chord.

        Raises
        ------

        Any exceptions raised by the following functions will also be raised by this:
        - _pitch_to_lily()
        - _duration_to_lily()
        """

        # Add the pitch letters and register numbers
        post = u''
        the_pitches = u'<'
        for each_pitch in self._as_m21.pitches:
            the_pitches = u''.join([the_pitches, _pitch_to_lily(each_pitch), u' '])
        the_pitches = u''.join([the_pitches[:-1], u'>'])  # also remove the last space

        # NB: From here to the end of the method, it's the same as NoteMaker._calculate_lily()
        # Find the duration
        if len(self._as_m21.duration.components) > 1:
            # We have a multiple-part duration
            for durational_component in self._as_m21.duration.components:
                post = u''.join([post,
                    the_pitches,
                    _duration_to_lily(durational_component, self._known_tuplet),
                    u'~ '])
            post = post[:-2]
        else:
            # Just a straightforward duration
            post = u''.join([the_pitches,
                _duration_to_lily(self._as_m21.duration, self._known_tuplet)])

        # Add a tie if necessary
        if self._as_m21.tie is not None:
            if u'start' == self._as_m21.tie.type:
                post = u''.join([post, u'~'])

        # Add the \markup{} block, if there is one
        if hasattr(self._as_m21, 'lily_markup'):
            post = u''.join([post, unicode(self._as_m21.lily_markup)])

        # Done
        self._as_ly = post


class MeasureMaker(LilyPondObjectMaker):
    """
    Class corresponding to a music21.stream.Measure object. Holds information about all the notes
    and chords and other things in the measure.
    """

    def __init__(self, m21_obj, first_or_last=False):
        """
        Create a new MeasureMaker instance. For some objects, this will also generate the
        LilyPond string corresponding to the objects stored in this LilyPondObjectMaker.

        Parameters
        ----------

        m21_obj : music21.*
            A music21 object

        first_or_last : boolean
            Whether this measure is either the first or the last; this triggers the call to see
            whether the measure is incomplete. Better to check this only on the first and last
            measures, since it takes a very long time. Default is False.
        """
        super(MeasureMaker, self).__init__(m21_obj)
        self._check_for_incomplete = first_or_last

    def _calculate_lily(self):
        """
        Returns a str that is one line of a LilyPond score, containing one Measure.

        Input should be a Measure.
        """

        post = [u"\t"]
        barcheck_included = False

        # Hold whether this Measure is supposed to be "invisible"
        invisible = False
        if hasattr(self._as_m21, 'lily_invisible'):
            invisible = self._as_m21.lily_invisible

        # Add the first requirement of invisibility
        if invisible:
            post.append(u'\stopStaff\n\t')

        # first check if it's a partial (pick-up) measure
        if self._check_for_incomplete:
            bar_dur = self._as_m21.barDuration.quarterLength
            my_dur = self._as_m21.duration.quarterLength
            if round(my_dur, 2) < bar_dur:
                if self._as_m21.duration.components is not None:
                    rounded = duration.Duration(round(my_dur, 2))
                    post.extend([u"\\partial ", _duration_to_lily(rounded), u"\n\t"])
                else:
                    post.extend([u"\\partial ", _duration_to_lily(self._as_m21.duration), u"\n\t"])

        # Make self._as_m21 an iterable, so we can pull in multiple elements when we need to deal
        # with tuplets.
        bar_iter = iter(self._as_m21)
        # This holds \markup{} blocks that happened before a Note/Rest, and should be appended
        # to the next Note/Rest that happens.
        attach_this_markup = u''
        # And fill in all the stuff
        for obj in bar_iter:
            # Note or Rest
            if isinstance(obj, note.Note) or isinstance(obj, note.Rest):
                # TODO: is there a situation where I'll ever need to deal with
                # multiple-component durations for a single Note/Rest?
                # ANSWER: yes, sometimes

                # Is it a full-measure rest?
                if isinstance(obj, note.Rest) and \
                bar_iter.srcStream.barDuration.quarterLength == obj.quarterLength:
                    if invisible:
                        post.extend(['s', _duration_to_lily(obj.duration), u' '])
                    else:
                        post.extend([u'R', _duration_to_lily(obj.duration), u' '])
                # Is it the start of a tuplet?
                elif obj.duration.tuplets is not None and len(obj.duration.tuplets) > 0:
                    number_of_tuplet_components = obj.duration.tuplets[0].numberNotesActual
                    in_the_space_of = obj.duration.tuplets[0].numberNotesNormal
                    post.extend([u'\\times ', unicode(in_the_space_of), u'/',
                        unicode(number_of_tuplet_components), u' { ',
                        NoteMaker(obj, True).get_lilypond(), u" "])
                    # For every tuplet component...
                    for _ in repeat(None, number_of_tuplet_components - 1):
                        post.extend([NoteMaker(next(bar_iter), True).get_lilypond(), u' '])
                    post.append(u'} ')
                # It's just a regular note or rest
                else:
                    post.extend([NoteMaker(obj).get_lilypond(), u' '])

                # Is there a \markup{} block to append?
                if attach_this_markup != '':
                    post.append(attach_this_markup)
                    attach_this_markup = ''
            # Chord
            elif isinstance(obj, chord.Chord):
                post.extend([ChordMaker(obj).get_lilypond(), u' '])
            # Clef
            elif isinstance(obj, clef.Clef):
                post.extend([_clef_to_lily(obj, append=u'\n\t', invisible=invisible)])
            # Time Signature
            elif isinstance(obj, meter.TimeSignature):
                if invisible:
                    post.append(u"\\once \\override Staff.TimeSignature #'transparent = ##t\n\t")
                post.extend([u"\\time ",
                    unicode(obj.beatCount), "/",
                    unicode(obj.denominator), u"\n\t"])
            # Key Signature
            elif isinstance(obj, key.KeySignature):
                pitch_and_mode = obj.pitchAndMode
                if invisible:
                    post.append(u"\\once \\override Staff.KeySignature #'transparent = ##t\n\t")
                if 2 == len(pitch_and_mode) and pitch_and_mode[1] is not None:
                    post.extend([u"\\key ",
                        _pitch_to_lily(pitch_and_mode[0], include_octave=False),
                        u" \\" + pitch_and_mode[1] + "\n\t"])
                else:
                    # We'll have to assume it's \major, because music21 does that.
                    post.extend([u"\\key ",
                         _pitch_to_lily(pitch_and_mode[0], include_octave=False),
                        u" \\major\n\t"])
            # Barline
            elif isinstance(obj, bar.Barline):
                # We don't need to write down a regular barline, but either way, we definitely
                # should include a bar-check symbol
                barcheck_included = True
                if 'regular' != obj.style:
                    post.extend([u'|\n', u'\t', _barline_to_lily(obj), u'\n'])
                else:
                    post.append(u'|\n')
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
            elif isinstance(obj, humdrum.spineParser.SpineComment):
                # http://mit.edu/music21/doc/html/moduleHumdrumSpineParser.html
                # These contain at least part names, and maybe also other interesting metadata(?)
                pass
            # Written expression marks (like "con fuoco" or something)
            elif isinstance(obj, expressions.TextExpression):
                the_marker = None  # store the local thing
                if obj.positionVertical > 0:  # above staff
                    the_marker = [u"^\\markup{ "]
                elif obj.positionVertical < 0:  # below staff
                    the_marker = [u"_\\markup{ "]
                else:  # LilyPond can decide above or below
                    the_marker = [u"-\\markup{ "]
                if obj.enclosure is not None:  # put a shape around the text?
                    pass  # TODO
                the_marker.extend([u'"', obj.content, u'" }'])
                if obj.enclosure is not None:  # must close the enclosure, if necessary
                    the_marker.append(u'}')
                the_marker.append(u' ')

                # Find out whether there's a previous Note or Rest to attach to
                previous_element = self._as_m21.getElementBeforeOffset(obj.offset)
                if not isinstance(previous_element, note.Note) and \
                not isinstance(previous_element, note.Rest):
                    # this variable holds text to append to the next Note/Rest
                    attach_this_markup = u''.join([attach_this_markup, the_marker])
                else:  # There was a previous Note/Rest, so we're good
                    post.append(u''.join(the_marker))
                del the_marker
            # TODO: music21.layout.StaffLayout (Lassus duos)
            # We don't know what it is, and should probably figure out!
            else:
                msg = 'Unknown object in Measure ' + unicode(self._as_m21.number) + ': ' + \
                    unicode(obj)
                print(msg)  # DEBUG
                print('   its type is ' + unicode(type(obj)))  # DEBUG
                #raise UnidentifiedObjectError(msg)

        # Append a bar-check symbol, if relevant
        if len(post) > 1 and not barcheck_included:
            post.append(u"|\n")

        # Append a note if we couldn't include a \markup{} block
        if attach_this_markup != '':
            post.extend(u'# Could not include this markup: ', attach_this_markup)

        # The final requirement of invisibility
        if invisible:
            post.append(u'\t\\startStaff\n')

        self._as_ly = u''.join(post)


class AnalysisVoiceMaker(LilyPondObjectMaker):
    """
    Processes a music21 Part that has the "lily_analysis_voice attribute" set to True.

    This is turned into a Part that has no staff lines, is printed in its score order, and has all
    "lily_markup" attributes attached to 'spacer' notes (i.e., with the letter name "s").

    Each Part should have only Note objects in it.
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
            post = u's'

            if len(lily_this.duration.components) > 1:
                for durational_component in lily_this.duration.components:
                    post = u''.join([post, _duration_to_lily(durational_component), '~ '])
                    post = post[:-2]
            else:
                post = u''.join([post, _duration_to_lily(lily_this.duration)])

            if lily_this.tie is not None:
                if lily_this.tie.type is 'start':
                    post = u''.join([post, u'~'])

            if hasattr(lily_this, 'lily_markup'):
                post = u''.join([post, unicode(lily_this.lily_markup)])

            return post

        # Just try to fill in all the stuff
        post = ''
        for obj in self._as_m21:
            post = u''.join([post, u'\t', space_for_lily(obj), u'\n'])
        self._as_ly = post


class PartMaker(LilyPondObjectMaker):
    """
    Convert a music21.stream.Part instance into its corresponding LilyPond markup.
    """

    # Instance Data
    # _setts : some settings thing

    def __init__(self, m21_obj, setts):
        """
        Create a new PartMaker instance.

        Parameters
        ----------

        setts : ???
        """
        super(PartMaker, self).__init__(m21_obj)
        self._setts = setts

    def _calculate_lily(self):
        """
        Generate the LilyPond string corresponding to the objects stored in this
        LilyPondObjectMaker.
        """
        # Start the Part
        # We used to use some of the part's .bestName, but many scores (like
        # for **kern) don't have this.
        call_this_part = _string_of_n_letters(8)
        self._setts._parts_in_this_score.append(call_this_part)
        post = call_this_part + u" =\n{\n"

        # If this part has the "lily_instruction" property set, this goes here
        if hasattr(self._as_m21, 'lily_instruction'):
            post = u''.join([post, self._as_m21.lily_instruction])

        # If the part has a .bestName property set, we'll use it to generate
        # both the .instrumentName and .shortInstrumentName for LilyPond.
        instr_name = self._as_m21.getInstrument().partName
        if instr_name is not None and len(instr_name) > 0:
            if len(instr_name) > 3:
                post = u''.join([post, u'\t%% ', instr_name, u'\n',
                    u'\t\set Staff.instrumentName = \markup{ "', instr_name, u'" }\n',
                    u'\t\set Staff.shortInstrumentName = \markup{ "', instr_name[:3], u'." }\n'])
            else:
                post = u''.join([post, u'\t%% ', instr_name, u'\n',
                    u'\t\set Staff.instrumentName = \markup{ "', instr_name, u'" }\n',
                    u'\t\set Staff.shortInstrumentName = \markup{ "', instr_name, u'" }\n'])
        elif hasattr(self._as_m21, 'lily_analysis_voice') and \
        True == self._as_m21.lily_analysis_voice:
            self._setts._analysis_notation_parts.append(call_this_part)
            post = u''.join([post, u'\t%% vis annotated analysis\n',
                AnalysisVoiceMaker(self._as_m21).get_lilypond()])
        # Custom settings for bar numbers
        if self._setts.get_property('bar numbers') is not None:
            post = u''.join([post, u"\n\t\override Score.BarNumber #'break-visibility = ",
                self._setts.get_property('bar numbers'), u'\n'])

        # If it's an analysis-annotation part, we'll handle this differently.
        if hasattr(self._as_m21, 'lily_analysis_voice') and \
        True == self._as_m21.lily_analysis_voice:
            pass
        # Otherwise, it's hopefully just a regular, everyday Part.
        else:
            # What's in the Part?
            # TODO: break this into a separate method, process_part()
            # TODO: make this less stupid
            for thing in self._as_m21:
                # Probably measures.
                if isinstance(thing, stream.Measure):
                    if 0 == thing.number:
                        post = u''.join([post, MeasureMaker(thing, True).get_lilypond()])
                    else:
                        post = u''.join([post, MeasureMaker(thing).get_lilypond()])
                elif isinstance(thing, instrument.Instrument):
                    # We can safely ignore this (for now?) because we already dealt
                    # with the part name earlier.
                    pass
                elif isinstance(thing, tempo.MetronomeMark):
                    # TODO: at some point, we'll have to deal with this nicely
                    pass
                elif isinstance(thing, meter.TimeSignature):
                    pass
                elif isinstance(thing, note.Note) or isinstance(thing, note.Rest):
                    post = u''.join([post, NoteMaker(thing).get_lilypond(), ' '])
                # **kern importer garbage... well, it's only garbage to us
                elif isinstance(thing, humdrum.spineParser.MiscTandem):
                    # http://mit.edu/music21/doc/html/moduleHumdrumSpineParser.html
                    # Is there really nothing we can use this for? Seems like these
                    # exist only to help music21 developers.
                    pass
                else:
                    msg = 'Unknown object in Stream while processing Part: '
                    print(msg)  # DEBUG
                    #raise UnidentifiedObjectError(msg + unicode(thing))
        # finally, to close the part
        post = u''.join([post, u"}\n"])

        # NOTE: you must re-implement this in subclasses
        self._as_ly = post


class MetadataMaker(LilyPondObjectMaker):
    """
    Convert a music21.metadata.Metadata instance into its corresponding LilyPond markup, which is
    the \header{} block of the resulting LilyPond file
    """

    # Instance Data
    # _setts : some settings thing

    def __init__(self, m21_obj, setts):
        """
        Create a new MetadataMaker instance.

        Parameters
        ----------

        setts : ???
        """
        super(MetadataMaker, self).__init__(m21_obj)
        self._setts = setts

    def _calculate_lily(self):
        """
        Generate the LilyPond string corresponding to the objects stored in this
        LilyPondObjectMaker.
        """
        post = u"\header {\n"

        if self._as_m21.composer is not None:
            # TODO: test this
            # NOTE: this commented line is what I used to have... unsure whether
            # I need it
            #post += '\tcomposer = \markup{ "' + self._as_m21.composer.name + '" }\n'
            post = u''.join([post, u'\tcomposer = \markup{ "', self._as_m21.composer, u'" }\n'])
        if self._as_m21.composers is not None:
            # I don't really know what to do with non-composer contributors
            pass
        if 'None' != self._as_m21.date:
            post = u''.join([post, u'\tdate = "', unicode(self._as_m21.date), u'"\n'])
        if self._as_m21.movementName is not None:
            if None != self._as_m21.movementNumber:
                post = u''.join([post, u'\tsubtitle = \markup{ "',
                    unicode(self._as_m21.movementNumber), u': ',
                    self._as_m21.movementName, u'" }\n'])
            else:
                post = u''.join([post, u'\tsubtitle = \markup{ "',
                    self._as_m21.movementName, u'" }\n'])
        if self._as_m21.opusNumber is not None:
            post = u''.join([post, u'\topus = "', unicode(self._as_m21.opusNumber), u'"\n'])
        if self._as_m21.title is not None:
            if self._as_m21.alternativeTitle is not None:
                post = u''.join([post, u'\ttitle = \markup{ \"', self._as_m21.title,
                    u'(\\"' + self._as_m21.alternativeTitle + u'\\")', u'" }\n'])
            else:
                post = u''.join([post, u'\ttitle = \markup{ \"', self._as_m21.title, u'" }\n'])
        # Extra Formatting Options
        # Tagline
        if self._setts.get_property('tagline') is None:
            post = u''.join([post, u'\ttagline = ""\n'])
        elif self._setts.get_property('tagline') == '':
            pass
        else:
            post = u''.join([post, u'\ttagline = "', self._setts.get_property('tagline'), '"\n'])
        # close the \header{} block
        post = u''.join([post, u"}\n"])

        self._as_ly = post


class ScoreMaker(LilyPondObjectMaker):
    """
    Convert a music21.stream.Score instance into its corresponding LilyPond markup.
    """

    # Instance Data
    # _setts : some settings thing

    def __init__(self, m21_obj, setts):
        """
        Create a new ScoreMaker instance.

        Parameters
        ----------

        setts : ???
        """
        super(ScoreMaker, self).__init__(m21_obj)
        self._setts = setts

    def _calculate_lily(self):
        """
        Generate the LilyPond string corresponding to the objects stored in this
        LilyPondObjectMaker.
        """

        # Things Before Parts:
        # Our mark! // Version // Paper size
        post = [u'% LilyPond output from music21 via "OutputLilyPond"\n',
            u'\\version "', self._setts.get_property('lilypond_version'), u'"\n\n',
            u'\\paper {\n\t#(set-paper-size "', self._setts.get_property('paper_size'),
            u'")\n}\n\n']

        # Parts
        # This can hold all of our parts... they might also be a StaffGroup,
        # a Metadata object, or something else.
        list_of_parts = []
        # Go through the possible parts and see what we find.
        for possible_part in self._as_m21:
            the_part_ly = _process_stream(possible_part, self._setts)
            # If _process_stream() can't deal with the object type, it returns None
            if the_part_ly is not None:
                list_of_parts.append(the_part_ly + u"\n")
        # Append the parts to the score we're building. In the future, it'll
        # be important to re-arrange the parts if necessary, or maybe to filter
        # things, so we'll keep everything in this supposedly efficient loop.
        for i in xrange(len(list_of_parts)):
            post.append(list_of_parts[i])

        # Things After Parts
        # Output the \score{} block
        post.append(u'\\score {\n\t\\new StaffGroup\n\t<<\n')
        for each_part in self._setts._parts_in_this_score:
            if each_part in self._setts._analysis_notation_parts:
                post.extend([u'\t\t\\new VisAnnotation = "', each_part,
                    u'" \\' + each_part + u'\n'])
            else:
                post.extend([u'\t\t\\new Staff = "', each_part, u'" \\' + each_part + u'\n'])
        post.append(u'\t>>\n')

        # Output the \layout{} block
        post.append(u'\t\\layout{\n')
        if self._setts.get_property('indent') is not None:
            post.extend([u'\t\tindent = ', self._setts.get_property('indent'), u'\n'])
        post.append("""\t\t% VisAnnotation Context
\t\t\context
\t\t{
\t\t\t\\type "Engraver_group"
\t\t\t\\name VisAnnotation
\t\t\t\\alias Voice
\t\t\t\consists "Output_property_engraver"
\t\t\t\consists "Script_engraver"
\t\t\t\consists "Text_engraver"
\t\t\t\consists "Skip_event_swallow_translator"
\t\t\t\consists "Axis_group_engraver"
\t\t}
\t\t% End VisAnnotation Context
\t\t
\t\t% Modify "StaffGroup" context to accept VisAnnotation context.
\t\t\context
\t\t{
\t\t\t\StaffGroup
\t\t\t\\accepts VisAnnotation
\t\t}
\t}\n}\n
""")

        self._as_ly = u''.join(post)
