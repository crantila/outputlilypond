#! /usr/bin/python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Filename: TestProcessStream.py
# Purpose: Integration Tests for _process_stream()
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
from OutputLilyPond import _process_stream
from LilyPondSettings import LilyPondSettings
from music21 import converter


class Test_Process_Stream_Part(unittest.TestCase):
    # NOTE: We have to pull a bit of trickery here, because there is some
    # randomness involved in part names.
    def test_first_measures_of_bach(self):
        # first two measures of soprano part
        the_settings = LilyPondSettings()
        the_score = converter.parse('test_corpus/bwv77.mxl')
        actual = _process_stream(the_score.parts[0][:3], the_settings)
        actual = actual[8:]  # remove the randomized part name
        expect = u""" =
{
\t%% Soprano
\t\set Staff.instrumentName = \markup{ "Soprano" }
\t\set Staff.shortInstrumentName = \markup{ "Sop." }
\t\partial 4
\t\clef treble
\t\key b \minor
\t\\time 4/4
\te'8 fis'8 |
\tg'4 a'4 b'4 a'4 |
}
"""
        self.assertEqual(actual, expect)

    def test_first_measures_of_Josquin(self):
        # first three measures of highest part
        the_settings = LilyPondSettings()
        the_score = converter.parse('test_corpus/Jos2308.krn')
        actual = _process_stream(the_score.parts[0][:12], the_settings)
        actual = actual[8:]  # remove the randomized part name
        expect = u""" =
{
\t\clef treble
\t\key f \major
\t\\time 2/1
\tg'1 d''1 |
\tr1 g'1 |
\td''1 r1 |
}
"""
        self.assertEqual(actual, expect)


# Define test suites
process_stream_part_suite = unittest.TestLoader().loadTestsFromTestCase(Test_Process_Stream_Part)
