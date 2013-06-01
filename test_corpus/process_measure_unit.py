#! /usr/bin/python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Filename: test_corpus/process_measure_unit.py
# Purpose: Purpose-built music21 snippets for unit testing MeasureMaker()
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

from music21 import stream, note, meter, key, clef

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
