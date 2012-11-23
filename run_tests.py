#! /usr/bin/python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Name:         output_LilyPond-run_tests.py
# Purpose:      Runs automated tests for output_LilyPond.py
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
from old_unit_tests import *
from old_integration_tests import *



#-------------------------------------------------------------------------------
# "Main" Function
#-------------------------------------------------------------------------------
if __name__ == '__main__':
   print( "###############################################################################" )
   print( "## output_LilyPond Test Suite                                                ##" )
   print( "###############################################################################" )
   print( "" )

   # Unit Tests
   unittest.TextTestRunner( verbosity = 1 ).run( detect_lilypond_suite )
   unittest.TextTestRunner( verbosity = 1 ).run( t_o_n_t_l )
   unittest.TextTestRunner( verbosity = 1 ).run( t_p_t_l )
   unittest.TextTestRunner( verbosity = 1 ).run( t_d_t_l )
   unittest.TextTestRunner( verbosity = 1 ).run( t_n_t_l )
   unittest.TextTestRunner( verbosity = 1 ).run( t_b_t_l )
   unittest.TextTestRunner( verbosity = 1 ).run( t_p_m )

   # Run Integration Tests
   unittest.TextTestRunner( verbosity = 1 ).run( process_stream_part_suite )

# TODO: Testing
# - providing a filename to process_score() actually outputs there
# - detect_lilypond() : when it works, and when it doesn't
# - whether the thing that calls LilyPond actually uses the auto-detected path
# - update existing tests for whatever stuff I've modified since they worked
