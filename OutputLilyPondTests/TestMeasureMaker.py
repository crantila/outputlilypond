#! /usr/bin/python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Name:         TestProcessMeasure.py
# Purpose:      Integration tests for MeasureMaker
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

import unittest
from test_corpus import process_measure_unit
from music21 import stream, key, note, meter, converter
from OutputLilyPond import MeasureMaker


class TestMeasureMaker(unittest.TestCase):
    def test_modeless_key_signature(self):
        # Silly example, unfortunately, that means we need a barcheck symbol even though there
        # were no events
        meas = stream.Measure()
        meas.append(key.KeySignature(-3))
        actual = MeasureMaker(meas)
        self.assertEqual(actual.get_lilypond(), u'\t\key ees \major\n\t|\n')

    def test_some_tuplets_1(self):
        # Complete measure starts with tuplets, filled with rests
        test_in1 = stream.Measure()
        test_in1.timeSignature = meter.TimeSignature('4/4')
        test_in1.append(note.Note('C4', quarterLength=0.16666))
        test_in1.append(note.Note('D4', quarterLength=0.16666))
        test_in1.append(note.Note('E4', quarterLength=0.16666))
        test_in1.append(note.Rest(quarterLength=0.5))
        test_in1.append(note.Rest(quarterLength=1.0))
        test_in1.append(note.Rest(quarterLength=2.0))
        expect = u"\t\\time 4/4\n\t\\times 2/3 { c'16 d'16 e'16 } r8 r4 r2 |\n"
        actual = MeasureMaker(test_in1)
        self.assertEqual(actual.get_lilypond(), expect)

    def test_some_tuplets_2(self):
        # Partial measure starts with tuplets (multiple components)
        test_in1 = stream.Measure()
        test_in1.timeSignature = meter.TimeSignature('4/4')
        test_in1.append(note.Note('C4', quarterLength=0.16666))
        test_in1.append(note.Note('D4', quarterLength=0.16666))
        test_in1.append(note.Note('E4', quarterLength=0.16666))
        expect = """\t\partial 8
\t\\time 4/4
\t\\times 2/3 { c'16 d'16 e'16 } |
"""
        actual = MeasureMaker(test_in1)
        self.assertEqual(actual.get_lilypond(), expect)

    def test_bwv77_bass_part_1(self):
        bass_part = converter.parse('test_corpus/bwv77.mxl').parts[3]
        # first measure
        actual = MeasureMaker(bass_part[1])
        expect = u'\t\partial 4\n\t\clef bass\n\t\key b \minor\n\t\\time 4/4\n\te4 |\n'
        # tests
        self.assertEqual(actual.get_lilypond(), expect)

    def test_bwv77_bass_part_2(self):
        bass_part = converter.parse('test_corpus/bwv77.mxl').parts[3]
        # third measure
        actual = MeasureMaker(bass_part[4])
        expect = u'\tb4 a4 g4 fis4 |\n'
        self.assertEqual(actual.get_lilypond(), expect)

    def test_bwv77_bass_part_3(self):
        bass_part = converter.parse('test_corpus/bwv77.mxl').parts[3]
        # final measure
        actual = MeasureMaker(bass_part[-1])
        expect = u'\t\\partial 2.\n\tg8 e8 fis4 b,4 |\n\t\\bar "|."\n'
        self.assertEqual(actual.get_lilypond(), expect)

    def test_invisibility_1(self):
        # test the .lily_invisible property, which should cause everything in a Measure to have
        # the #'transparent property set to ##t
        actual = MeasureMaker(process_measure_unit.invisibility_1)
        expect = u'''\t\\stopStaff
\t\\once \\override Staff.TimeSignature #'transparent = ##t
\t\\time 4/4
\ts1 |
\t\\startStaff
'''
        self.assertEqual(actual.get_lilypond(), expect)

    def test_invisibility_2(self):
        # test the .lily_invisible property, which should cause everything in a Measure to have
        # the #'transparent property set to ##t
        actual = MeasureMaker(process_measure_unit.invisibility_2)
        expect = '''\t\\stopStaff
\t\\once \\override Staff.TimeSignature #'transparent = ##t
\t\\time 4/4
\t\\once \\override Staff.KeySignature #'transparent = ##t
\t\\key b \\major
\ts1 |
\t\\startStaff
'''
        self.assertEqual(actual.get_lilypond(), expect)

    def test_invisibility_3(self):
        # test the .lily_invisible property, which should cause everything in a Measure to have
        # the #'transparent property set to ##t
        actual = MeasureMaker(process_measure_unit.invisibility_3)
        expect = '''\t\\stopStaff
\t\\once \\override Staff.TimeSignature #'transparent = ##t
\t\\time 4/4
\t\\once \\override Staff.KeySignature #'transparent = ##t
\t\\key b \\major
\t\\once \\override Staff.Clef #'transparent = ##t
\t\\clef treble
\ts1 |
\t\\startStaff
'''
        self.assertEqual(actual.get_lilypond(), expect)

    def test_ave_maris_stella_1(self):
        # "ams" is "ave maris stella"... what were you thinking?
        ams = converter.parse('test_corpus/Jos2308.krn')
        # First four measures, second highest part
        actual = MeasureMaker(ams.parts[1][9]).get_lilypond()
        actual += MeasureMaker(ams.parts[1][10]).get_lilypond()
        actual += MeasureMaker(ams.parts[1][11]).get_lilypond()
        actual += MeasureMaker(ams.parts[1][12]).get_lilypond()
        expect = u"""\t\clef treble
\t\key f \major
\t\\time 2/1
\tr1 g'1 |
\td''1 r1 |
\tg'1 d''1~ |
\td''2 c''2 bes'2 a'2 |
"""
        self.assertEqual(actual, expect)

    def test_ave_maris_stella_2(self):
        ams = converter.parse('test_corpus/Jos2308.krn')
        # Measures 125-7, lowest part
        actual = MeasureMaker(ams.parts[3][133]).get_lilypond()
        actual += MeasureMaker(ams.parts[3][134]).get_lilypond()
        actual += MeasureMaker(ams.parts[3][135]).get_lilypond()
        expect = u"""\tg\\breve~ |
\tg\\breve |
\t\\bar "||"
\tR\\breve |
"""
        self.assertEqual(actual, expect)

    def test_ave_maris_stella_3(self):
        ams = converter.parse('test_corpus/Jos2308.krn')
        # Measure 107, second-lowest part (tuplets)
        actual = MeasureMaker(ams.parts[2][115]).get_lilypond()
        expect = u"\t\\times 2/3 { e'1 c'1 d'1 } |\n"
        self.assertEqual(actual, expect)


#-------------------------------------------------------------------------------
# Definitions
#-------------------------------------------------------------------------------
test_measure_maker_suite = unittest.TestLoader().loadTestsFromTestCase(TestMeasureMaker)
