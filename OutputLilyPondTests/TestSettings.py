#! /usr/bin/python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Filename: TestSettings.py
# Purpose: Unit tests for VISSettings
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
from LilyPondSettings import LilyPondSettings


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.s = LilyPondSettings()

    def test_default_init(self):
        # Ensure all the settings are initialized to the proper default value.
        # These must be removed in a later version, once the new class structure
        # is implemented.
        self.assertEqual(self.s._parts_in_this_score, [])
        self.assertEqual(self.s._analysis_notation_parts, [])
        # These will probably remain
        self.assertEqual(self.s._secret_settings['bar numbers'], None)
        self.assertEqual(self.s._secret_settings['tagline'], '')
        self.assertEqual(self.s._secret_settings['indent'], None)
        self.assertEqual(self.s._secret_settings['print_instrument_names'], True)
        self.assertEqual(self.s._secret_settings['paper_size'], 'letter')
        self.assertEqual(self.s._secret_settings['lilypond_path'], '/usr/bin/lilypond')
        self.assertEqual(self.s._secret_settings['lilypond_version'], '2.16.0')
        self.assertEqual(self.s._secret_settings['lilypond_version_numbers'], (2, 16, 0))

    # "set"
    def test_set_property_1(self):
        self.s.set_property('bar numbers', 12)
        self.assertEqual(self.s._secret_settings['bar numbers'], 12)

    def test_set_property_2(self):
        self.s.set_property('tagline', 12)
        self.assertEqual(self.s._secret_settings['tagline'], 12)

    def test_set_property_3(self):
        self.s.set_property('indent', 12)
        self.assertEqual(self.s._secret_settings['indent'], 12)

    def test_set_property_4(self):
        self.s.set_property('print_instrument_names', 12)
        self.assertEqual(self.s._secret_settings['print_instrument_names'], 12)

    def test_set_property_5(self):
        self.s.set_property('paper_size', 12)
        self.assertEqual(self.s._secret_settings['paper_size'], 12)

    def test_set_property_6(self):
        self.s.set_property('lilypond_path', 12)
        self.assertEqual(self.s._secret_settings['lilypond_path'], 12)

    def test_set_property_7(self):
        self.s.set_property('lilypond_version', 12)
        self.assertEqual(self.s._secret_settings['lilypond_version'], 12)

    def test_set_property_8(self):
        self.s.set_property('lilypond_version_numbers', 12)
        self.assertEqual(self.s._secret_settings['lilypond_version_numbers'], 12)

    # "get"
    def test_get_property_1(self):
        self.s._secret_settings['bar numbers'] = 12
        self.assertEqual(self.s.get_property('bar numbers'), 12)

    def test_get_property_2(self):
        self.s._secret_settings['tagline'] = 12
        self.assertEqual(self.s.get_property('tagline'), 12)

    def test_get_property_3(self):
        self.s._secret_settings['indent'] = 12
        self.assertEqual(self.s.get_property('indent'), 12)

    def test_get_property_4(self):
        self.s._secret_settings['print_instrument_names'] = 12
        self.assertEqual(self.s.get_property('print_instrument_names'), 12)

    def test_get_property_5(self):
        self.s._secret_settings['paper_size'] = 12
        self.assertEqual(self.s.get_property('paper_size'), 12)

    def test_get_property_6(self):
        self.s._secret_settings['lilypond_path'] = 12
        self.assertEqual(self.s.get_property('lilypond_path'), 12)

    def test_get_property_7(self):
        self.s._secret_settings['lilypond_version'] = 12
        self.assertEqual(self.s.get_property('lilypond_version'), 12)

    def test_get_property_8(self):
        self.s._secret_settings['lilypond_version_numbers'] = 12
        self.assertEqual(self.s.get_property('lilypond_version_numbers'), 12)

    # error "set"
    def test_set_error_1(self):
        self.assertRaises(KeyError, self.s.set_property, 'bananas', 12)

    def test_set_error_2(self):
        self.assertRaises(KeyError, self.s.set_property, 42, 12)

    # error "get"
    def test_get_error_1(self):
        self.assertRaises(KeyError, self.s.get_property, 'bananas')

    def test_get_error_2(self):
        self.assertRaises(KeyError, self.s.get_property, 42)


class Test_Detect_LilyPond(unittest.TestCase):
    # detect_lilypond() -------------------------------------
    def test_for_path(self):
        # NB: You have to write in your path and version!
        my_path = u'/usr/bin/lilypond'
        my_version = u'2.16.0'
        res = LilyPondSettings.detect_lilypond()
        self.assertEqual(res[0], my_path)
        self.assertEqual(res[1], my_version)

    # make_lily_version_numbers() ---------------------------
    def test_make_lily_version_numbers_1(self):
        self.assertEqual(LilyPondSettings.make_lily_version_numbers('2.14.0'), (2, 14, 0))

    def test_make_lily_version_numbers_2(self):
        self.assertEqual(LilyPondSettings.make_lily_version_numbers('2.14.2'), (2, 14, 2))

    def test_make_lily_version_numbers_3(self):
        self.assertEqual(LilyPondSettings.make_lily_version_numbers('2.16.0'), (2, 16, 0))

    def test_make_lily_version_numbers_4(self):
        self.assertEqual(LilyPondSettings.make_lily_version_numbers('2.15.31'), (2, 15, 31))

    def test_make_lily_version_numbers_5(self):
        expected = (218901289304, 1123412344, 12897795)
        actual = LilyPondSettings.make_lily_version_numbers('218901289304.1123412344.12897795')
        self.assertEqual(actual, expected)

    def test_make_lily_version_numbers_6(self):
        self.assertRaises(ValueError, LilyPondSettings.make_lily_version_numbers, '..')

#-------------------------------------------------------------------------------
# Definitions
#-------------------------------------------------------------------------------
test_settings_suite = unittest.TestLoader().loadTestsFromTestCase(TestSettings)
detect_lilypond_suite = unittest.TestLoader().loadTestsFromTestCase(Test_Detect_LilyPond)
