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

# Confirmed Requirements:
import unittest
from output_LilyPond import *
from music21 import note, pitch, duration, converter, tie, key



#-------------------------------------------------------------------------------
class Test_Process_Stream_Part( unittest.TestCase ):
   # NOTE: We have to pull a bit of trickery here, because there is some
   # randomness involved in part names.
   def test_first_measures_of_bach( self ):
      # first two measures of soprano part
      the_settings = LilyPond_Settings()
      the_score = converter.parse( 'test_corpus/bwv77.mxl' )
      actual = process_stream( the_score[1][:3], the_settings )
      actual = actual[8:] # remove the randomized part name
      expected = """ =
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
      self.assertEqual( actual, expected )
   # ------------------------------------------------------

   def test_first_measures_of_Josquin( self ):
      # first three measures of highest part
      the_settings = LilyPond_Settings()
      the_score = converter.parse( 'test_corpus/Jos2308.krn' )
      actual = process_stream( the_score[0][:10], the_settings )
      actual = actual[8:] # remove the randomized part name
      expected = """ =
{
\t\clef treble
\t\key f \major
\t\\time 2/1
\tg'1 d''1 |
\tr1 g'1 |
\td''1 r1 |
}
"""
      self.assertEqual( actual, expected )
   # ------------------------------------------------------
#-------------------------------------------------------------------------------



# Define test suites
process_stream_part_suite = unittest.TestLoader().loadTestsFromTestCase( Test_Process_Stream_Part )
