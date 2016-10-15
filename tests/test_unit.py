#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Filename: unit_tests.py
# Purpose: Unit tests for OutputLilyPond
#
# Copyright (C) 2012, 2013, 2014, 2016 Christopher Antila
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------
"""
Unit tests for the "outputlilypond" module.
"""

import unittest
import mock
import pytest
from music21 import clef, bar, duration, note, pitch, tie, chord, metadata
from outputlilypond import functions, problems, settings

# Don't worry about missing docstrings
# pylint: disable=C0111
# Don't worry about "too many public methods"
# pylint: disable=R0904


def test_octave_num_works():
    """octave_num_to_lily() when it works"""
    assert functions.octave_num_to_lily(0) == u',,,'
    assert functions.octave_num_to_lily(1) == u',,'
    assert functions.octave_num_to_lily(2) == u','
    assert functions.octave_num_to_lily(3) == u''
    assert functions.octave_num_to_lily(4) == u"'"
    assert functions.octave_num_to_lily(5) == u"''"
    assert functions.octave_num_to_lily(6) == u"'''"
    assert functions.octave_num_to_lily(7) == u"''''"
    assert functions.octave_num_to_lily(8) == u"'''''"
    assert functions.octave_num_to_lily(9) == u"''''''"
    assert functions.octave_num_to_lily(10) == u"'''''''"
    assert functions.octave_num_to_lily(11) == u"''''''''"
    assert functions.octave_num_to_lily(12) == u"'''''''''"


def test_octave_num_breaks():
    """octave_num_to_lily() when it doesn't work"""
    with pytest.raises(problems.UnidentifiedObjectError):
        functions.octave_num_to_lily(-10)
    with pytest.raises(problems.UnidentifiedObjectError):
        functions.octave_num_to_lily(-1)
    with pytest.raises(problems.UnidentifiedObjectError):
        functions.octave_num_to_lily(13)
    with pytest.raises(problems.UnidentifiedObjectError):
        functions.octave_num_to_lily(128)


class TestPitchToLily(unittest.TestCase):
    def test_pitch_to_lily_1(self):
        # Pitch with octave
        self.assertEqual(functions.pitch_to_lily(pitch.Pitch('C4')), "c'")

    def test_pitch_to_lily_2(self):
        # Pitch with octave
        self.assertEqual(functions.pitch_to_lily(pitch.Pitch('E#0')), "eis,,,")

    def test_pitch_to_lily_3(self):
        # Note with octave
        self.assertEqual(functions.pitch_to_lily(note.Note('F##3')), "fisis")

    def test_pitch_to_lily_4(self):
        # Note without octave
        self.assertEqual(functions.pitch_to_lily(pitch.Pitch('B-6'), False), "bes")

    def test_pitch_to_lily_5(self):
        # Pitch without octave
        self.assertEqual(functions.pitch_to_lily(pitch.Pitch('F--11'), False), "feses")


class TestDurationToLily(unittest.TestCase):
    def test_duration_to_lily_1(self):
        # Simple things
        self.assertEqual(functions.duration_to_lily(duration.Duration(1.0)), '4')

    def test_duration_to_lily_2(self):
        self.assertEqual(functions.duration_to_lily(duration.Duration(16.0)), '\\longa')

    def test_duration_to_lily_3(self):
        self.assertEqual(functions.duration_to_lily(duration.Duration(0.0625)), '64')

    def test_duration_to_lily_4(self):
        self.assertEqual(functions.duration_to_lily(duration.Duration(3.0)), '2.')

    def test_duration_to_lily_5(self):
        self.assertEqual(functions.duration_to_lily(duration.Duration(0.1875)), '32.')

    def test_duration_to_lily_6(self):
        self.assertEqual(functions.duration_to_lily(duration.Duration(3.5)), '2..')

    def test_duration_to_lily_7(self):
        self.assertEqual(functions.duration_to_lily(duration.Duration(3.75)), '2...')

    def test_duration_to_lily_8(self):
        self.assertEqual(functions.duration_to_lily(duration.Duration(0.12109375)), '64....')

    def test_duration_to_lily_9(self):
        # Same as above, but with known_tuplet==True... all results should be the same.
        self.assertEqual(functions.duration_to_lily(duration.Duration(1.0)), '4')

    def test_duration_to_lily_10(self):
        self.assertEqual(functions.duration_to_lily(duration.Duration(16.0)), '\\longa')

    def test_duration_to_lily_11(self):
        self.assertEqual(functions.duration_to_lily(duration.Duration(0.0625)), '64')

    def test_duration_to_lily_12(self):
        self.assertEqual(functions.duration_to_lily(duration.Duration(3.0)), '2.')

    def test_duration_to_lily_13(self):
        self.assertEqual(functions.duration_to_lily(duration.Duration(0.1875)), '32.')

    def test_duration_to_lily_14(self):
        self.assertEqual(functions.duration_to_lily(duration.Duration(3.5)), '2..')

    def test_duration_to_lily_15(self):
        self.assertEqual(functions.duration_to_lily(duration.Duration(3.75)), '2...')

    def test_duration_to_lily_16(self):
        self.assertEqual(functions.duration_to_lily(duration.Duration(0.12109375)), '64....')

    def test_duration_to_lily_17(self):
        with pytest.raises(problems.ImpossibleToProcessError):
            functions.duration_to_lily(duration.Duration(7.99609375))

    def test_duration_to_lily_18(self):
        # These take multiple Note objects, and as such cannot be portrayed by
        # the output from a single call to _functions.duration_to_lily()
        self.assertRaises(problems.ImpossibleToProcessError,
                          functions.duration_to_lily,
                          duration.Duration(16.1))

    def test_duration_to_lily_19(self):
        with pytest.raises(problems.ImpossibleToProcessError):
            functions.duration_to_lily(duration.Duration(25.0))

    def test_duration_to_lily_20(self):
        with pytest.raises(problems.ImpossibleToProcessError):
            functions.duration_to_lily(duration.Duration(0.01268128))

    def test_duration_to_lily_21(self):
        # tuplet component--shouldn't work
        self.assertRaises(problems.ImpossibleToProcessError,
                          functions.duration_to_lily,
                          duration.Duration(0.16666666))

    def test_duration_to_lily_22(self):
        # tuplet component--should work
        self.assertEqual(functions.duration_to_lily(duration.Duration(0.16666666), True), '16')

    def test_duration_to_lily_23(self):
        # offset of 0.0 -- shouldn't work
        self.assertRaises(problems.ImpossibleToProcessError,
                          functions.duration_to_lily,
                          duration.Duration(0.0))

    def test_duration_to_lily_24(self):
        expected = u"16."
        actual = functions.duration_to_lily(duration.Duration(0.375))
        self.assertEqual(actual, expected)

    def test_duration_to_lily_25(self):
        expected = u"1"
        actual = functions.duration_to_lily(duration.DurationTuple('whole', 0, 4.0))
        self.assertEqual(actual, expected)


class TestNoteToLily(unittest.TestCase):
    def test_note_to_lily_1(self):
        expected = u"c'4"
        actual = functions.note_to_lily(note.Note('C4', quarterLength=1.0))
        self.assertEqual(actual, expected)

    def test_note_to_lily_1a(self):
        expected = u"s4"
        some_note = note.Note('C4', quarterLength=1.0)
        some_note.lily_invisible = True
        actual = functions.note_to_lily(some_note)
        self.assertEqual(actual, expected)

    def test_note_to_lily_1b(self):
        expected = u"s4"
        some_note = note.Rest(quarterLength=1.0)
        some_note.lily_invisible = True
        actual = functions.note_to_lily(some_note)
        self.assertEqual(actual, expected)

    def test_note_to_lily_1c(self):
        expected = u"r4"
        some_note = note.Rest(quarterLength=1.0)
        actual = functions.note_to_lily(some_note)
        self.assertEqual(actual, expected)

    def test_note_to_lily_2(self):
        actual = functions.note_to_lily(note.Note('E#0', quarterLength=16.0))
        expected = u"eis,,,\\longa"
        self.assertEqual(actual, expected)

    def test_note_to_lily_3(self):
        actual = functions.note_to_lily(note.Note('F##3', quarterLength=0.0625))
        expected = u"fisis64"
        self.assertEqual(actual, expected)

    def test_note_to_lily_4(self):
        actual = functions.note_to_lily(note.Note('F--11', quarterLength=3.75))
        expected = u"feses''''''''2..."
        self.assertEqual(actual, expected)

    def test_note_to_lily_5(self):
        self.assertRaises(problems.UnidentifiedObjectError,
                          functions.note_to_lily,
                          note.Note('C17'))

    def test_note_to_lily_6(self):
        actual = functions.note_to_lily(note.Rest(quarterLength=16.0))
        expected = u"r\\longa"
        self.assertEqual(actual, expected)

    def test_note_to_lily_7(self):
        actual = functions.note_to_lily(note.Rest(quarterLength=0.0625))
        expected = u"r64"
        self.assertEqual(actual, expected)

    def test_note_to_lily_8(self):
        test_note_1 = note.Note('C4', quarterLength=1.0)
        test_note_1.tie = tie.Tie('start')
        actual = functions.note_to_lily(test_note_1)
        expected = u"c'4~"
        self.assertEqual(actual, expected)

    def test_note_to_lily_9(self):
        test_note_1 = note.Note('C4', quarterLength=1.0)
        test_note_1.tie = tie.Tie('start')
        test_note_1.lily_markup = '_\\markup{ "example!" }'
        actual = functions.note_to_lily(test_note_1)
        expected = u"c'4~_\\markup{ \"example!\" }"
        self.assertEqual(actual, expected)

    def test_note_to_lily_9a(self):
        test_note_1 = note.Note('C4', quarterLength=1.0)
        test_note_1.tie = tie.Tie('start')
        test_note_1.lily_markup = '_\\markup{ "example!" }'
        test_note_1.lily_invisible = True
        actual = functions.note_to_lily(test_note_1)
        expected = u"s4~_\\markup{ \"example!\" }"
        self.assertEqual(actual, expected)

    def test_note_to_lily_9b(self):
        test_note_1 = note.Rest(quarterLength=1.0)
        test_note_1.tie = tie.Tie('start')
        test_note_1.lily_markup = '_\\markup{ "example!" }'
        actual = functions.note_to_lily(test_note_1)
        expected = u"r4~_\\markup{ \"example!\" }"
        self.assertEqual(actual, expected)

    def test_note_to_lily_11(self):
        actual = functions.note_to_lily(note.Note('C4', quarterLength=7.99609375))
        expected = u"c'1~ c'2~ c'4~ c'8~ c'16~ c'32~ c'64...."
        self.assertEqual(actual, expected)

    def test_note_to_lily_11a(self):
        some_note = note.Note('C4', quarterLength=7.99609375)
        some_note.lily_invisible = True
        actual = functions.note_to_lily(some_note)
        expected = u"s1~ s2~ s4~ s8~ s16~ s32~ s64...."
        self.assertEqual(actual, expected)

    def test_note_to_lily_11b(self):
        actual = functions.note_to_lily(note.Rest(quarterLength=7.99609375))
        expected = u"r1~ r2~ r4~ r8~ r16~ r32~ r64...."
        self.assertEqual(actual, expected)


class TestBarlineToLily(unittest.TestCase):
    def test_barline_to_lily_1(self):
        bee_ell = bar.Barline('regular')
        expected = u'\\bar "|"'
        self.assertEqual(functions.barline_to_lily(bee_ell), expected)

    def test_barline_to_lily_2(self):
        bee_ell = bar.Barline('dotted')
        expected = u'\\bar ":"'
        self.assertEqual(functions.barline_to_lily(bee_ell), expected)

    def test_barline_to_lily_3(self):
        bee_ell = bar.Barline('dashed')
        expected = u'\\bar "dashed"'
        self.assertEqual(functions.barline_to_lily(bee_ell), expected)

    def test_barline_to_lily_4(self):
        bee_ell = bar.Barline('heavy')
        expected = u'\\bar "|.|"'
        self.assertEqual(functions.barline_to_lily(bee_ell), expected)

    def test_barline_to_lily_5(self):
        bee_ell = bar.Barline('double')
        expected = u'\\bar "||"'
        self.assertEqual(functions.barline_to_lily(bee_ell), expected)

    def test_barline_to_lily_6(self):
        bee_ell = bar.Barline('final')
        expected = u'\\bar "|."'
        self.assertEqual(functions.barline_to_lily(bee_ell), expected)

    def test_barline_to_lily_7(self):
        bee_ell = bar.Barline('heavy-light')
        expected = u'\\bar ".|"'
        self.assertEqual(functions.barline_to_lily(bee_ell), expected)

    def test_barline_to_lily_8(self):
        bee_ell = bar.Barline('heavy-heavy')
        expected = u'\\bar ".|."'
        self.assertEqual(functions.barline_to_lily(bee_ell), expected)

    def test_barline_to_lily_9(self):
        bee_ell = bar.Barline('tick')
        expected = u"\\bar \"'\""
        self.assertEqual(functions.barline_to_lily(bee_ell), expected)

    def test_barline_to_lily_10(self):
        bee_ell = bar.Barline('short')
        expected = u"\\bar \"'\""
        self.assertEqual(functions.barline_to_lily(bee_ell), expected)

    def test_barline_to_lily_11(self):
        bee_ell = bar.Barline('none')
        expected = u'\\bar ""'
        self.assertEqual(functions.barline_to_lily(bee_ell), expected)

    def test_barline_to_lily_12(self):
        # error
        bee_ell = bar.Barline('regular')
        bee_ell._style = u'marmalade sun for everyone'  # pylint: disable=W0212
        self.assertRaises(problems.UnidentifiedObjectError, functions.barline_to_lily, bee_ell)


class TestClefToLily(unittest.TestCase):
    # NB: because the ordering of the tests in the function itself will change the
    #     outcome of the clef it chooses, I'm going to test all the possibilities
    def test_clef_to_lily_1(self):
        bee_ell = clef.Treble8vbClef()
        expected = u"\\clef \"treble_8\"\n"
        self.assertEqual(functions.clef_to_lily(bee_ell), expected)

    def test_clef_to_lily_2(self):
        bee_ell = clef.Treble8vaClef()
        expected = u"\\clef \"treble^8\"\n"
        self.assertEqual(functions.clef_to_lily(bee_ell), expected)

    def test_clef_to_lily_3(self):
        bee_ell = clef.Bass8vbClef()
        expected = u"\\clef \"bass_8\"\n"
        self.assertEqual(functions.clef_to_lily(bee_ell), expected)

    def test_clef_to_lily_4(self):
        bee_ell = clef.Bass8vaClef()
        expected = u"\\clef \"bass^8\"\n"
        self.assertEqual(functions.clef_to_lily(bee_ell), expected)

    def test_clef_to_lily_5(self):
        bee_ell = clef.TrebleClef()
        expected = u"\\clef treble\n"
        self.assertEqual(functions.clef_to_lily(bee_ell), expected)

    def test_clef_to_lily_6(self):
        bee_ell = clef.BassClef()
        expected = u"\\clef bass\n"
        self.assertEqual(functions.clef_to_lily(bee_ell), expected)

    def test_clef_to_lily_7(self):
        bee_ell = clef.TenorClef()
        expected = u"\\clef tenor\n"
        self.assertEqual(functions.clef_to_lily(bee_ell), expected)

    def test_clef_to_lily_8(self):
        bee_ell = clef.AltoClef()
        expected = u"\\clef alto\n"
        self.assertEqual(functions.clef_to_lily(bee_ell), expected)

    def test_clef_to_lily_9(self):
        # transparent
        bee_ell = clef.TrebleClef()
        expected = u"\\once \\override Staff.Clef #'transparent = ##t\n\\clef treble\n"
        self.assertEqual(functions.clef_to_lily(bee_ell, invisible=True), expected)

    def test_clef_to_lily_10(self):
        # different thing to append
        bee_ell = clef.TrebleClef()
        expected = u"\\clef treble hello"
        self.assertEqual(functions.clef_to_lily(bee_ell, append=u' hello'), expected)

    def test_clef_to_lily_11(self):
        # transparent and different thing to append
        bee_ell = clef.TrebleClef()
        expected = u"\\once \\override Staff.Clef #'transparent = ##t hello \\clef treble hello "
        self.assertEqual(functions.clef_to_lily(bee_ell, invisible=True, append=u' hello '), expected)

    def test_clef_to_lily_12(self):
        # exception
        bee_ell = clef.NoClef()  # I haven't yet decided what to do with this
        self.assertRaises(problems.UnidentifiedObjectError, functions.clef_to_lily, bee_ell)

    def test_clef_to_lily_13(self):
        bee_ell = clef.FBaritoneClef()
        expected = u"\\clef varbaritone\n"
        self.assertEqual(functions.clef_to_lily(bee_ell), expected)

    def test_clef_to_lily_14(self):
        bee_ell = clef.CBaritoneClef()
        expected = u"\\clef baritone\n"
        self.assertEqual(functions.clef_to_lily(bee_ell), expected)

    def test_clef_to_lily_15(self):
        bee_ell = clef.FrenchViolinClef()
        expected = u"\\clef french\n"
        self.assertEqual(functions.clef_to_lily(bee_ell), expected)

    def test_clef_to_lily_16(self):
        bee_ell = clef.MezzoSopranoClef()
        expected = u"\\clef mezzosoprano\n"
        self.assertEqual(functions.clef_to_lily(bee_ell), expected)

    def test_clef_to_lily_17(self):
        bee_ell = clef.PercussionClef()
        expected = u"\\clef percussion\n"
        self.assertEqual(functions.clef_to_lily(bee_ell), expected)

    def test_clef_to_lily_18(self):
        bee_ell = clef.SopranoClef()
        expected = u"\\clef soprano\n"
        self.assertEqual(functions.clef_to_lily(bee_ell), expected)

    def test_clef_to_lily_19(self):
        bee_ell = clef.SubBassClef()
        expected = u"\\clef subbass\n"
        self.assertEqual(functions.clef_to_lily(bee_ell), expected)


class TestChordMaker(unittest.TestCase):
    # NOTE: this class actually tests functions.note_to_lily with Chord objects
    def test_chord_maker_1(self):
        expected = u"<c' e' g'>4"
        the_chord = chord.Chord('c e g')
        actual = functions.note_to_lily(the_chord)
        self.assertEqual(actual, expected)

    def test_chord_maker_2(self):
        expected = u"<c' e' g'>16."
        the_chord = chord.Chord('c e g', quarterLength=0.375)
        actual = functions.note_to_lily(the_chord)
        self.assertEqual(actual, expected)

    def test_chord_maker_3(self):
        expected = u"<c' e' g'>4__look_at_me!"
        the_chord = chord.Chord('c e g')
        the_chord.lily_markup = u'__look_at_me!'
        actual = functions.note_to_lily(the_chord)
        self.assertEqual(actual, expected)

    def test_chord_maker_4(self):
        expected = u"<c' e' g'>4~"
        the_chord = chord.Chord('c e g')
        the_chord.tie = tie.Tie('start')
        actual = functions.note_to_lily(the_chord)
        self.assertEqual(actual, expected)

    def test_chord_maker_5(self):
        expected = u"<c' e'>1~ <c' e'>2~ <c' e'>4~ <c' e'>8~ <c' e'>16~ <c' e'>32~ <c' e'>64...."
        the_chord = chord.Chord('c e', quarterLength=7.99609375)
        actual = functions.note_to_lily(the_chord)
        self.assertEqual(actual, expected)

    def test_chord_maker_6(self):
        expected = u"<c'>4"
        the_chord = chord.Chord('c')
        actual = functions.note_to_lily(the_chord)
        self.assertEqual(actual, expected)

    def test_chord_maker_7(self):
        expected = u"<feses, c cisisis ges g' bis'>4"
        the_chord = chord.Chord('f--2 c3 c###3 g-3 g4 b#4')
        actual = functions.note_to_lily(the_chord)
        self.assertEqual(actual, expected)


class TestMetadataToLily(unittest.TestCase):
    def test_metadata_1(self):
        # In this test...
        # - with date
        # - without composer
        # - with movementName not movementNumber
        # - with opusNumber
        # - with title and alternativeTitle
        # - with tagline in Settings
        # prepare the mock Metadata and Settings objects (NOTE: surely there's a better way?)
        mock_meta = mock.MagicMock(spec_set=metadata.Metadata)
        mock_date = mock.PropertyMock(return_value=u'2010')
        mock_composer = mock.PropertyMock(return_value=None)
        mock_movement_name = mock.PropertyMock(return_value=u'Winter Bones')
        mock_movement_num = mock.PropertyMock(return_value=None)
        mock_opus_num = mock.PropertyMock(return_value=5)
        mock_title = mock.PropertyMock(return_value=u'The Five Ghosts')
        mock_alt_title = mock.PropertyMock(return_value=u'The Séance')
        type(mock_meta).date = mock_date
        type(mock_meta).composer = mock_composer
        type(mock_meta).movementName = mock_movement_name
        type(mock_meta).movementNumber = mock_movement_num
        type(mock_meta).opusNumber = mock_opus_num
        type(mock_meta).title = mock_title
        type(mock_meta).alternativeTitle = mock_alt_title
        mock_sett = mock.MagicMock(spec_set=settings.LilyPondSettings)
        mock_sett.get_property.return_value = u'Silly tagline!'
        expected = u"""\\header {
\tdate = "2010"
\tsubtitle = \\markup{ "Winter Bones" }
\topus = "5"
\ttitle = \\markup{ "The Five Ghosts(\\"The Séance\\")" }
\ttagline = "Silly tagline!"
}\n"""
        # run the test
        actual = functions.metadata_to_lily(mock_meta, mock_sett)
        # verify the result
        self.assertEqual(2, mock_date.call_count)
        self.assertEqual(1, mock_composer.call_count)
        self.assertEqual(2, mock_movement_name.call_count)
        self.assertEqual(1, mock_movement_num.call_count)
        self.assertEqual(2, mock_opus_num.call_count)
        self.assertEqual(2, mock_title.call_count)
        self.assertEqual(2, mock_alt_title.call_count)
        self.assertEqual(expected, actual)

    def test_metadata_2(self):
        # In this test...
        # - with composer
        # - without date
        # - with movementName and movementNumber
        # - without opusNumber
        # - with title not alternativeTitle
        # - without tagline in Settings
        # prepare the mock Metadata and Settings objects (NOTE: surely there's a better way?)
        mock_meta = mock.MagicMock(spec_set=metadata.Metadata)
        mock_date = mock.PropertyMock(return_value=None)
        mock_composer = mock.PropertyMock(return_value=u'Stars')
        mock_movement_name = mock.PropertyMock(return_value=u'Winter Bones')
        mock_movement_num = mock.PropertyMock(return_value=11)
        mock_opus_num = mock.PropertyMock(return_value=None)
        mock_title = mock.PropertyMock(return_value=u'The Five Ghosts')
        mock_alt_title = mock.PropertyMock(return_value=None)
        type(mock_meta).date = mock_date
        type(mock_meta).composer = mock_composer
        type(mock_meta).movementName = mock_movement_name
        type(mock_meta).movementNumber = mock_movement_num
        type(mock_meta).opusNumber = mock_opus_num
        type(mock_meta).title = mock_title
        type(mock_meta).alternativeTitle = mock_alt_title
        mock_sett = mock.MagicMock(spec_set=settings.LilyPondSettings)
        mock_sett.get_property.return_value = None
        expected = u"""\\header {
\tcomposer = \\markup{ "Stars" }
\tsubtitle = \\markup{ "11: Winter Bones" }
\ttitle = \\markup{ "The Five Ghosts" }
\ttagline = ""
}\n"""
        # run the test
        actual = functions.metadata_to_lily(mock_meta, mock_sett)
        # verify the result
        self.assertEqual(1, mock_date.call_count)
        self.assertEqual(2, mock_composer.call_count)
        self.assertEqual(2, mock_movement_name.call_count)
        self.assertEqual(2, mock_movement_num.call_count)
        self.assertEqual(1, mock_opus_num.call_count)
        self.assertEqual(2, mock_title.call_count)
        self.assertEqual(1, mock_alt_title.call_count)
        self.assertEqual(expected, actual)

    def test_metadata_3(self):
        # In this test...
        # - without date
        # - with composer
        # - without movementName
        # - without opus
        # - without title
        # - without tagline in Settings
        # prepare the mock Metadata and Settings objects (NOTE: surely there's a better way?)
        mock_meta = mock.MagicMock(spec_set=metadata.Metadata)
        mock_date = mock.PropertyMock(return_value=None)
        mock_composer = mock.PropertyMock(return_value=u'Stars')
        mock_movement_name = mock.PropertyMock(return_value=None)
        mock_movement_num = mock.PropertyMock(return_value=None)
        mock_opus_num = mock.PropertyMock(return_value=None)
        mock_title = mock.PropertyMock(return_value=None)
        mock_alt_title = mock.PropertyMock(return_value=None)
        type(mock_meta).date = mock_date
        type(mock_meta).composer = mock_composer
        type(mock_meta).movementName = mock_movement_name
        type(mock_meta).movementNumber = mock_movement_num
        type(mock_meta).opusNumber = mock_opus_num
        type(mock_meta).title = mock_title
        type(mock_meta).alternativeTitle = mock_alt_title
        mock_sett = mock.MagicMock(spec_set=settings.LilyPondSettings)
        mock_sett.get_property.return_value = u'Silly tagline!'
        expected = u"""\\header {
\tcomposer = \\markup{ "Stars" }
\ttagline = "Silly tagline!"
}\n"""
        # run the test
        actual = functions.metadata_to_lily(mock_meta, mock_sett)
        # verify the result
        self.assertEqual(1, mock_date.call_count)
        self.assertEqual(2, mock_composer.call_count)
        self.assertEqual(1, mock_movement_name.call_count)
        self.assertEqual(0, mock_movement_num.call_count)
        self.assertEqual(1, mock_opus_num.call_count)
        self.assertEqual(1, mock_title.call_count)
        self.assertEqual(0, mock_alt_title.call_count)
        self.assertEqual(expected, actual)
