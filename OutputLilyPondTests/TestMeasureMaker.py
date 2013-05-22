#! /usr/bin/python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Name:         TestProcessMeasure.py
# Purpose:      Unit tests for MeasureMaker
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
#from OutputLilyPond.test_corpus import
from music21 import stream, key, note, meter, converter
from OutputLilyPond import MeasureMaker


class TestMeasureMaker(unittest.TestCase):
    def test_modeless_key_signature(self):
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

    #def test_some_tuplets_2(self):
        ## Incomplete measure starts with tuplets
        ## TODO: currently this fails because the duration of the three triplets is
        ## 0.49999 and that's not equal to the 0.5 qL it should have. This is a
        ## problem in duration_to_lily()
        #test_in1 = stream.Measure()
        #test_in1.timeSignature = meter.TimeSignature('4/4')
        #test_in1.append(note.Note('C4', quarterLength=0.16666))
        #test_in1.append(note.Note('D4', quarterLength=0.16666))
        #test_in1.append(note.Note('E4', quarterLength=0.16666))
        #expect = """\t\partial 8
#\t\\time 4/4
#\t\\times 2/3 { c'16 d'16 e'16 } |
#"""
        #actual = MeasureMaker(test_in1)
        #self.assertEqual(actual.get_lilypond(), expect)

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

    #def test_bwv77_bass_part_3(self):
        #bass_part = converter.parse('test_corpus/bwv77.mxl').parts[3]
        ## final measure
        #actual = MeasureMaker(bass_part[-1])
        #expect = u'\t\\partial 2.\n\tg8 e8 fis4 b,4\n\t\\bar "|." |\n'
        #self.assertEqual(actual.get_lilypond(), expect)

    #def test_invisibility_1(self):
        ## test the .lily_invisible property, which should cause everything in a
        ## Measure to have the #'transparent property set to ##t
        #expected = '''\t\\stopStaff
    #\t\\once \\override Staff.TimeSignature #'transparent = ##t
    #\t\\time 4/4
    #\ts1 |
    #\t\\startStaff
    #'''
        #self.assertEqual(process_measure(process_measure_unit.invisibility_1),\
                            #expected)

    #def test_invisibility_2(self):
        ## test the .lily_invisible property, which should cause everything in a
        ## Measure to have the #'transparent property set to ##t
        #expected = '''\t\\stopStaff
    #\t\\once \\override Staff.TimeSignature #'transparent = ##t
    #\t\\time 4/4
    #\t\\once \\override Staff.KeySignature #'transparent = ##t
    #\t\\key b \\major
    #\ts1 |
    #\t\\startStaff
    #'''
        #self.assertEqual(process_measure(process_measure_unit.invisibility_2),\
                            #expected)

    #def test_invisibility_3(self):
        ## test the .lily_invisible property, which should cause everything in a
        ## Measure to have the #'transparent property set to ##t
        #expected = '''\t\\stopStaff
    #\t\\once \\override Staff.TimeSignature #'transparent = ##t
    #\t\\time 4/4
    #\t\\once \\override Staff.KeySignature #'transparent = ##t
    #\t\\key b \\major
    #\t\\once \\override Staff.Clef #'transparent = ##t
    #\t\\clef treble
    #\ts1 |
    #\t\\startStaff
    #'''
        #self.assertEqual(process_measure(process_measure_unit.invisibility_3),\
                            #expected)

    #def test_exception_1(self):
        ## There's a Measure in this Measure, which should raise an exception
        ## because we don't expect one
        #self.assertRaises(UnidentifiedObjectError, process_measure, \
                            #process_measure_unit.exception_1)

    #def test_ave_maris_stella(self):
    # TODO: turn this into a unit test by processing only one measure at a time
        ## "ams" is "ave maris stella"... what were you thinking?
        #ams = converter.parse('test_corpus/Jos2308.krn')
        ## First four measures, second highest part
        #first_test = """\t\clef treble
    #\t\key f \major
    #\t\\time 2/1
    #\tr1 g'1 |
    #\td''1 r1 |
    #\tg'1 d''1~ |
    #\td''2 c''2 bes'2 a'2 |
    #"""
        #result = process_measure(ams[1][7]) + process_measure(ams[1][8]) + \
            #process_measure(ams[1][9]) + process_measure(ams[1][10])
        #self.assertEqual(result, first_test)
        ## Measures 125-7, lowest part
        #second_test = """\tg\\breve~ |
    #\tg\\breve \\bar "||" |
    #\tR\\breve |
    #"""
        #result = process_measure(ams[3][131]) + process_measure(ams[3][132]) + \
            #process_measure(ams[3][133])
        #self.assertEqual(result, second_test)
        ## Measure 107, second-lowest part (tuplets)
        #third_test = "\t\\times 2/3 { e'1 c'1 d'1 } |\n"
        ##print(str(ams[2][113].duration.quarterLength) + ' andza ' + str(ams[2][113].barDuration.quarterLength))
        #result = process_measure(ams[2][113])
        #self.assertEqual(result, third_test)


#-------------------------------------------------------------------------------
# Definitions
#-------------------------------------------------------------------------------
test_measure_maker_suite = unittest.TestLoader().loadTestsFromTestCase(TestMeasureMaker)
