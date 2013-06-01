#! /usr/bin/python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Filename: run_tests.py
# Purpose: Run automated tests for OutputLilyPond.py
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
from OutputLilyPondTests.TestSettings import test_settings_suite, detect_lilypond_suite
from OutputLilyPondTests.TestMeasureMaker import test_measure_maker_suite
from OutputLilyPondTests.unit_tests import octave_number_to_lily_suite, pitch_to_lily_suite, \
    duration_to_lily_suite, note_to_lily_suite, barline_to_lily_suite, clef_to_lily_suite, \
    chord_maker_suite
from OutputLilyPondTests.TestProcessStream import process_stream_part_suite

#-------------------------------------------------------------------------------
# "Main" Function
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    verb = 1

    # Unit Tests
    unittest.TextTestRunner(verbosity=verb).run(test_settings_suite)
    unittest.TextTestRunner(verbosity=verb).run(detect_lilypond_suite)
    unittest.TextTestRunner(verbosity=verb).run(octave_number_to_lily_suite)
    unittest.TextTestRunner(verbosity=verb).run(pitch_to_lily_suite)
    unittest.TextTestRunner(verbosity=verb).run(duration_to_lily_suite)
    unittest.TextTestRunner(verbosity=verb).run(note_to_lily_suite)
    unittest.TextTestRunner(verbosity=verb).run(barline_to_lily_suite)
    unittest.TextTestRunner(verbosity=verb).run(clef_to_lily_suite)
    unittest.TextTestRunner(verbosity=verb).run(chord_maker_suite)

    # Integration Tests
    unittest.TextTestRunner(verbosity=verb).run(test_measure_maker_suite)
    unittest.TextTestRunner(verbosity=verb).run(process_stream_part_suite)

# TODO: Testing
# - providing a filename to process_score() actually outputs there
# - detect_lilypond() : when it works, and when it doesn't
# - whether the thing that calls LilyPond actually uses the auto-detected path
# - update existing tests for whatever stuff I've modified since they worked
