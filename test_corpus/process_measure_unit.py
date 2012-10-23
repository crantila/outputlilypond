#! /usr/bin/python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Program Name:              output_LilyPond
# Program Description:       Outputs music21 Objects into LilyPond Format
#
# Filename: test_corpus/process_measure_unit.py
# Purpose: Purpose-built music21 snippets for unit testing process_measure()
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



from music21.stream import Part, Score, Measure
from music21.note import Note, Rest
from music21.meter import TimeSignature
from music21.key import KeySignature
from music21 import clef



#-------------------------------------------------------------------------------
# Everything in the Measure should be invisible... we have only one Rest and one
# TimeSignature
invisibility_1 = Measure()
invisibility_1.append( TimeSignature( '4/4' ) )
invisibility_1.append( Rest( quarterLength=4.0 ) )
invisibility_1.lily_invisible = True
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# Everything in the Measure should be invisible... we have a Rest, a
# TimeSignature, and a KeySignature
invisibility_2 = Measure()
invisibility_2.append( TimeSignature( '4/4' ) )
invisibility_2.append( KeySignature( 5 ) )
invisibility_2.append( Rest( quarterLength=4.0 ) )
invisibility_2.lily_invisible = True
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# Everything in the Measure should be invisible... we have a Rest, a
# TimeSignature, a KeySignature, and a Clef
invisibility_3 = Measure()
invisibility_3.append( TimeSignature( '4/4' ) )
invisibility_3.append( KeySignature( 5 ) )
invisibility_3.append( clef.TrebleClef() )
invisibility_3.append( Rest( quarterLength=4.0 ) )
invisibility_3.lily_invisible = True
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# This should raise an error because we shouldn't have a Measure in a Measure
exception_1 = Measure()
exception_1.append( TimeSignature( '4/4' ) )
exception_1.append( Measure() )
#-------------------------------------------------------------------------------
