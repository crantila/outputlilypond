#! /usr/bin/python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Name:         output_LilyPond-test.py
# Purpose:      Unit tests for output_LilyPond.py
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

import unittest
from OutputLilyPond import _octave_num_to_lily, _pitch_to_lily, _duration_to_lily, NoteMaker
from music21 import note, pitch, duration, tie
# from test_corpus import process_measure_unit
from LilyPondProblems import UnidentifiedObjectError, ImpossibleToProcessError


class Test_octave_num_to_lily(unittest.TestCase):
    def test_octave_num_to_lily_1(self):
        self.assertRaises(UnidentifiedObjectError, _octave_num_to_lily, -10)

    def test_octave_num_to_lily_2(self):
        self.assertRaises(UnidentifiedObjectError, _octave_num_to_lily, -1)

    def test_octave_num_to_lily_3(self):
        self.assertEqual(_octave_num_to_lily(0), u',,,')

    def test_octave_num_to_lily_4(self):
        self.assertEqual(_octave_num_to_lily(1), u',,')

    def test_octave_num_to_lily_5(self):
        self.assertEqual(_octave_num_to_lily(2), u',')

    def test_octave_num_to_lily_6(self):
        self.assertEqual(_octave_num_to_lily(3), u'')

    def test_octave_num_to_lily_7(self):
        self.assertEqual(_octave_num_to_lily(4), u"'")

    def test_octave_num_to_lily_8(self):
        self.assertEqual(_octave_num_to_lily(5), u"''")

    def test_octave_num_to_lily_9(self):
        self.assertEqual(_octave_num_to_lily(6), u"'''")

    def test_octave_num_to_lily_10(self):
        self.assertEqual(_octave_num_to_lily(7), u"''''")

    def test_octave_num_to_lily_11(self):
        self.assertEqual(_octave_num_to_lily(8), u"'''''")

    def test_octave_num_to_lily_12(self):
        self.assertEqual(_octave_num_to_lily(9), u"''''''")

    def test_octave_num_to_lily_13(self):
        self.assertEqual(_octave_num_to_lily(10), u"'''''''")

    def test_octave_num_to_lily_14(self):
        self.assertEqual(_octave_num_to_lily(11), u"''''''''")

    def test_octave_num_to_lily_15(self):
        self.assertEqual(_octave_num_to_lily(12), u"'''''''''")

    def test_octave_num_to_lily_16(self):
        self.assertRaises(UnidentifiedObjectError, _octave_num_to_lily, 13)

    def test_octave_num_to_lily_17(self):
        self.assertRaises(UnidentifiedObjectError, _octave_num_to_lily, 128)


class Test_Pitch_to_Lily(unittest.TestCase):
    def test_pitch_to_lily_1(self):
        # Pitch with octave
        self.assertEqual(_pitch_to_lily(pitch.Pitch('C4')), "c'")

    def test_pitch_to_lily_2(self):
        # Pitch with octave
        self.assertEqual(_pitch_to_lily(pitch.Pitch('E#0')), "eis,,,")

    def test_pitch_to_lily_3(self):
        # Note with octave
        self.assertEqual(_pitch_to_lily(note.Note('F##3')), "fisis")

    def test_pitch_to_lily_4(self):
        # Note without octave
        self.assertEqual(_pitch_to_lily(pitch.Pitch('B-6'), False), "bes")

    def test_pitch_to_lily_5(self):
        # Pitch without octave
        self.assertEqual(_pitch_to_lily(pitch.Pitch('F--11'), False), "feses")


class Test_duration_to_lily(unittest.TestCase):
    def test_duration_to_lily_1(self):
        # Simple things
        self.assertEqual(_duration_to_lily(duration.Duration(1.0)), '4')

    def test_duration_to_lily_2(self):
        self.assertEqual(_duration_to_lily(duration.Duration(16.0)), '\longa')

    def test_duration_to_lily_3(self):
        self.assertEqual(_duration_to_lily(duration.Duration(0.0625)), '64')

    def test_duration_to_lily_4(self):
        self.assertEqual(_duration_to_lily(duration.Duration(3.0)), '2.')

    def test_duration_to_lily_5(self):
        self.assertEqual(_duration_to_lily(duration.Duration(0.1875)), '32.')

    def test_duration_to_lily_6(self):
        self.assertEqual(_duration_to_lily(duration.Duration(3.5)), '2..')

    def test_duration_to_lily_7(self):
        self.assertEqual(_duration_to_lily(duration.Duration(3.75)), '2...')

    def test_duration_to_lily_8(self):
        self.assertEqual(_duration_to_lily(duration.Duration(0.12109375)), '64....')

    def test_duration_to_lily_9(self):
        # Same as above, but with known_tuplet==True... all results should be the same.
        self.assertEqual(_duration_to_lily(duration.Duration(1.0)), '4', True)

    def test_duration_to_lily_10(self):
        self.assertEqual(_duration_to_lily(duration.Duration(16.0)), '\longa', True)

    def test_duration_to_lily_11(self):
        self.assertEqual(_duration_to_lily(duration.Duration(0.0625)), '64', True)

    def test_duration_to_lily_12(self):
        self.assertEqual(_duration_to_lily(duration.Duration(3.0)), '2.', True)

    def test_duration_to_lily_13(self):
        self.assertEqual(_duration_to_lily(duration.Duration(0.1875)), '32.', True)

    def test_duration_to_lily_14(self):
        self.assertEqual(_duration_to_lily(duration.Duration(3.5)), '2..', True)

    def test_duration_to_lily_15(self):
        self.assertEqual(_duration_to_lily(duration.Duration(3.75)), '2...', True)

    def test_duration_to_lily_16(self):
        self.assertEqual(_duration_to_lily(duration.Duration(0.12109375)), '64....', True)

    def test_duration_to_lily_17(self):
        # This should be rounded to qL==8.0 ... but I don't know how to make a
        # single-component duration with this qL, so I can't run this test as it
        # gets rounded, only as it produces an error.
        #self.assertEqual(__duration_to_lily(duration.Duration(7.99609375)), '\\breve')
        self.assertRaises(ImpossibleToProcessError, _duration_to_lily, duration.Duration(7.99609375))

    def test_duration_to_lily_18(self):
        # These take multiple Note objects, and as such cannot be portrayed by
        # the output from a single call to __duration_to_lily()
        self.assertRaises(ImpossibleToProcessError, _duration_to_lily, duration.Duration(16.1))

    def test_duration_to_lily_19(self):
        self.assertRaises(ImpossibleToProcessError, _duration_to_lily, duration.Duration(25.0))

    def test_duration_to_lily_20(self):
        self.assertRaises(ImpossibleToProcessError, _duration_to_lily, duration.Duration(0.01268128))

    def test_duration_to_lily_21(self):
        # tuplet component--shouldn't work
        self.assertRaises(ImpossibleToProcessError, _duration_to_lily, duration.Duration(0.16666666))

    def test_duration_to_lily_22(self):
        # tuplet component--should work
        self.assertEqual(_duration_to_lily(duration.Duration(0.16666666), True), '16')


class Test_note_to_lily(unittest.TestCase):
    def test_note_to_lily_1(self):
        expected = u"c'4"
        actual = NoteMaker(note.Note('C4', quarterLength=1.0))
        self.assertEqual(actual.get_lilypond(), expected)
        
    def test_note_to_lily_1a(self):
        expected = u"s4"
        some_note = note.Note('C4', quarterLength=1.0)
        some_note.lily_invisible = True
        actual = NoteMaker(some_note)
        self.assertEqual(actual.get_lilypond(), expected)

    def test_note_to_lily_1b(self):
        expected = u"s4"
        some_note = note.Rest(quarterLength=1.0)
        some_note.lily_invisible = True
        actual = NoteMaker(some_note)
        self.assertEqual(actual.get_lilypond(), expected)

    def test_note_to_lily_1c(self):
        expected = u"r4"
        some_note = note.Rest(quarterLength=1.0)
        actual = NoteMaker(some_note)
        self.assertEqual(actual.get_lilypond(), expected)

    def test_note_to_lily_2(self):
        actual = NoteMaker(note.Note('E#0', quarterLength=16.0))
        expected = u"eis,,,\longa"
        self.assertEqual(actual.get_lilypond(), expected)

    def test_note_to_lily_3(self):
        actual = NoteMaker(note.Note('F##3', quarterLength=0.0625))
        expected = u"fisis64"
        self.assertEqual(actual.get_lilypond(), expected)

    def test_note_to_lily_4(self):
        actual = NoteMaker(note.Note('F--11', quarterLength=3.75))
        expected = u"feses''''''''2..."
        self.assertEqual(actual.get_lilypond(), expected)

    def test_note_to_lily_5(self):
        actual = NoteMaker(note.Note('C17'))
        self.assertRaises(UnidentifiedObjectError, actual.get_lilypond)

    def test_note_to_lily_6(self):
        actual = NoteMaker(note.Rest(quarterLength=16.0))
        expected = u"r\longa"
        self.assertEqual(actual.get_lilypond(), expected)

    def test_note_to_lily_7(self):
        actual = NoteMaker(note.Rest(quarterLength=0.0625))
        expected = u"r64"
        self.assertEqual(actual.get_lilypond(), expected)

    def test_note_to_lily_8(self):
        test_Note_1 = note.Note('C4', quarterLength=1.0)
        test_Note_1.tie = tie.Tie('start')
        actual = NoteMaker(test_Note_1)
        expected = u"c'4~"
        self.assertEqual(actual.get_lilypond(), expected)

    def test_note_to_lily_9(self):
        test_Note_1 = note.Note('C4', quarterLength=1.0)
        test_Note_1.tie = tie.Tie('start')
        test_Note_1.lily_markup = '_\markup{ "example!" }'
        actual = NoteMaker(test_Note_1)
        expected = u"c'4~_\markup{ \"example!\" }"
        self.assertEqual(actual.get_lilypond(), expected)
        
    def test_note_to_lily_9a(self):
        test_Note_1 = note.Note('C4', quarterLength=1.0)
        test_Note_1.tie = tie.Tie('start')
        test_Note_1.lily_markup = '_\markup{ "example!" }'
        test_Note_1.lily_invisible = True
        actual = NoteMaker(test_Note_1)
        expected = u"s4~_\markup{ \"example!\" }"
        self.assertEqual(actual.get_lilypond(), expected)
        
    def test_note_to_lily_9b(self):
        test_Note_1 = note.Rest(quarterLength=1.0)
        test_Note_1.tie = tie.Tie('start')
        test_Note_1.lily_markup = '_\markup{ "example!" }'
        actual = NoteMaker(test_Note_1)
        expected = u"r4~_\markup{ \"example!\" }"
        self.assertEqual(actual.get_lilypond(), expected)

    def test_note_to_lily_11(self):
        actual = NoteMaker(note.Note('C4', quarterLength=7.99609375))
        expected = u"c'1~ c'2~ c'4~ c'8~ c'16~ c'32~ c'64...."
        self.assertEqual(actual.get_lilypond(), expected)
    
    def test_note_to_lily_11a(self):
        some_note = note.Note('C4', quarterLength=7.99609375)
        some_note.lily_invisible = True
        actual = NoteMaker(some_note)
        expected = u"s1~ s2~ s4~ s8~ s16~ s32~ s64...."
        self.assertEqual(actual.get_lilypond(), expected)
        
    def test_note_to_lily_11b(self):
        actual = NoteMaker(note.Rest(quarterLength=7.99609375))
        expected = u"r1~ r2~ r4~ r8~ r16~ r32~ r64...."
        self.assertEqual(actual.get_lilypond(), expected)

# Define test suites
octave_number_to_lily_suite = unittest.TestLoader().loadTestsFromTestCase(Test_octave_num_to_lily)
pitch_to_lily_suite = unittest.TestLoader().loadTestsFromTestCase(Test_Pitch_to_Lily)
duration_to_lily_suite = unittest.TestLoader().loadTestsFromTestCase(Test_duration_to_lily)
note_to_lily_suite = unittest.TestLoader().loadTestsFromTestCase(Test_note_to_lily)
