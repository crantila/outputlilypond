#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Filename: integration_tests.py
# Purpose: Integration tests for outputlilypond
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

# Don't worry about missing docstrings
# pylint: disable=C0111
# Don't worry about "too many public methods"
# pylint: disable=R0904

import unittest
from music21 import stream, key, note, meter, converter, note, key, clef, duration
from outputlilypond.functions import measure_to_lily, stream_to_lily
from outputlilypond.settings import LilyPondSettings


# Everything in the Measure should be invisible... we have only one Rest and one
# TimeSignature
invisibility_1 = stream.Measure()
invisibility_1.append(meter.TimeSignature('4/4'))
invisibility_1.append(note.Rest(quarterLength=4.0))
invisibility_1.lily_invisible = True

# Everything in the Measure should be invisible... we have a Rest, a
# TimeSignature, and a KeySignature
invisibility_2 = stream.Measure()
invisibility_2.append(meter.TimeSignature('4/4'))
invisibility_2.append(key.KeySignature(5))
invisibility_2.append(note.Rest(quarterLength=4.0))
invisibility_2.lily_invisible = True

# Everything in the Measure should be invisible... we have a Rest, a
# TimeSignature, a KeySignature, and a Clef
invisibility_3 = stream.Measure()
invisibility_3.append(meter.TimeSignature('4/4'))
invisibility_3.append(key.KeySignature(5))
invisibility_3.append(clef.TrebleClef())
invisibility_3.append(note.Rest(quarterLength=4.0))
invisibility_3.lily_invisible = True



class TestMeasureMaker(unittest.TestCase):
    def test_modeless_key_signature(self):
        # Silly example, unfortunately, that means we need a barcheck symbol even though there
        # were no events
        meas = stream.Measure()
        meas.append(key.KeySignature(-3))
        actual = measure_to_lily(meas)
        self.assertEqual(actual, u'\t\\key ees \\major\n\t|\n')

    def test_some_tuplets_1(self):
        # Complete measure starts with tuplets, filled with rests
        measure_contents = [
            note.Note('C4', quarterLength=0.25),
            note.Note('D4', quarterLength=0.25),
            note.Note('E4', quarterLength=0.25),
            note.Rest(quarterLength=0.5),
            note.Rest(quarterLength=1.0),
            note.Rest(quarterLength=2.0),
        ]
        measure_contents[0].duration.tuplets = (duration.Tuplet(3, 2, '16th'),)
        measure_contents[1].duration.tuplets = (duration.Tuplet(3, 2, '16th'),)
        measure_contents[2].duration.tuplets = (duration.Tuplet(3, 2, '16th'),)
        test_in1 = stream.Measure()
        test_in1.timeSignature = meter.TimeSignature('4/4')
        for thing in measure_contents:
            test_in1.append(thing)

        expect = u"\t\\time 4/4\n\t\\times 2/3 { c'16 d'16 e'16 } r8 r4 r2 |\n"
        actual = measure_to_lily(test_in1)
        self.assertEqual(actual, expect)

    def test_some_tuplets_2(self):
        # Partial measure starts with tuplets (multiple components)
        measure_contents = [
            note.Note('C4', quarterLength=0.25),
            note.Note('D4', quarterLength=0.25),
            note.Note('E4', quarterLength=0.25),
        ]
        measure_contents[0].duration.tuplets = (duration.Tuplet(3, 2, '16th'),)
        measure_contents[1].duration.tuplets = (duration.Tuplet(3, 2, '16th'),)
        measure_contents[2].duration.tuplets = (duration.Tuplet(3, 2, '16th'),)
        test_in1 = stream.Measure()
        test_in1.timeSignature = meter.TimeSignature('4/4')
        for thing in measure_contents:
            test_in1.append(thing)

        expect = """\t\\partial 8
\t\\time 4/4
\t\\times 2/3 { c'16 d'16 e'16 } |
"""
        actual = measure_to_lily(test_in1, True)
        self.assertEqual(actual, expect)

    def test_bwv77_bass_part_1(self):
        bass_part = converter.parse('test_corpus/bwv77.mxl').parts[3]
        # first measure
        actual = measure_to_lily(bass_part[1], True)
        expect = u'\t\\partial 4\n\t\\clef bass\n\t\\key b \\minor\n\t\\time 4/4\n\te4 |\n'
        # tests
        self.assertEqual(actual, expect)

    def test_bwv77_bass_part_2(self):
        bass_part = converter.parse('test_corpus/bwv77.mxl').parts[3]
        # third measure
        actual = measure_to_lily(bass_part[4])
        expect = u'\tb4 a4 g4 fis4 |\n'
        self.assertEqual(actual, expect)

    def test_bwv77_bass_part_3(self):
        bass_part = converter.parse('test_corpus/bwv77.mxl').parts[3]
        # final measure
        actual = measure_to_lily(bass_part[-1], True)
        expect = u'\t\\partial 2.\n\tg8 e8 fis4 b,4 |\n\t\\bar "|."\n'
        self.assertEqual(actual, expect)

    def test_invisibility_1(self):
        # test the .lily_invisible property, which should cause everything in a Measure to have
        # the #'transparent property set to ##t
        actual = measure_to_lily(invisibility_1)
        expect = u'''\t\\stopStaff
\t\\once \\override Staff.TimeSignature #'transparent = ##t
\t\\time 4/4
\ts1 |
\t\\startStaff
'''
        self.assertEqual(actual, expect)

    def test_invisibility_2(self):
        # test the .lily_invisible property, which should cause everything in a Measure to have
        # the #'transparent property set to ##t
        actual = measure_to_lily(invisibility_2)
        expect = '''\t\\stopStaff
\t\\once \\override Staff.TimeSignature #'transparent = ##t
\t\\time 4/4
\t\\once \\override Staff.KeySignature #'transparent = ##t
\t\\key b \\major
\ts1 |
\t\\startStaff
'''
        self.assertEqual(actual, expect)

    def test_invisibility_3(self):
        # test the .lily_invisible property, which should cause everything in a Measure to have
        # the #'transparent property set to ##t
        actual = measure_to_lily(invisibility_3)
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
        self.assertEqual(actual, expect)

    def test_ave_maris_stella_1(self):
        # "ams" is "ave maris stella"... what were you thinking?
        ams = converter.parse('test_corpus/Jos2308.krn')
        # First four measures, second highest part
        actual = measure_to_lily(ams.parts[1][9])
        actual += measure_to_lily(ams.parts[1][10])
        actual += measure_to_lily(ams.parts[1][11])
        actual += measure_to_lily(ams.parts[1][12])
        expect = u"""\t\\clef treble
\t\\key f \\major
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
        actual = measure_to_lily(ams.parts[3][133])
        actual += measure_to_lily(ams.parts[3][134])
        actual += measure_to_lily(ams.parts[3][135])
        expect = u"""\tg\\breve~ |
\tg\\breve |
\t\\bar "||"
\tR\\breve |
"""
        self.assertEqual(actual, expect)

    def test_ave_maris_stella_3(self):
        ams = converter.parse('test_corpus/Jos2308.krn')
        # Measure 107, second-lowest part (tuplets)
        actual = measure_to_lily(ams.parts[2][115])
        expect = u"\t\\times 2/3 { e'1 c'1 d'1 } |\n"
        self.assertEqual(actual, expect)


class TestProcessStreamPart(unittest.TestCase):
    # NOTE: We have to pull a bit of trickery here, because there is some
    # randomness involved in part names.
    def test_first_measures_of_bach(self):
        # first two measures of soprano part
        the_settings = LilyPondSettings()
        the_score = converter.parse('test_corpus/bwv77.mxl')
        actual = stream_to_lily(the_score.parts[0][:3], the_settings)
        actual = actual[8:]  # remove the randomized part name
        expect = u""" =
{
\t%% Soprano
\t\\set Staff.instrumentName = \\markup{ "Soprano" }
\t\\set Staff.shortInstrumentName = \\markup{ "Sop." }
\t\\partial 4
\t\\clef treble
\t\\key b \\minor
\t\\time 4/4
\te'8 fis'8 |
\tg'4 a'4 b'4 a'4 |
}
"""
        self.assertEqual(actual, expect)

    def test_first_measures_of_josquin(self):
        # first three measures of highest part
        the_settings = LilyPondSettings()
        the_score = converter.parse('test_corpus/Jos2308.krn')
        actual = stream_to_lily(the_score.parts[0][:12], the_settings)
        actual = actual[8:]  # remove the randomized part name
        expect = u""" =
{
\t\\clef treble
\t\\key f \\major
\t\\time 2/1
\tg'1 d''1 |
\tr1 g'1 |
\td''1 r1 |
}
"""
        self.assertEqual(actual, expect)
