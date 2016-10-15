OutputLilyPond
==============

A Python module that outputs a LilyPond file from a music21 Score stream. This module is not
intended for everyday use, and uses various strange python hacks to produce unusual LilyPond
scores for music analytic purposes.

Python 2 only. Python 3 support is forthcoming.


Install
-------

Make a virtualenv. Run this command in the same directory as this README file:

    $ pip install -e ".[devel]"

Or if you're using OutputLilyPond but not developing it, just run this:

    $ pip install .


Copyright Information
---------------------

All source code is subject to the GNU GPL 3.0 Licence. A copy of this licence is included as GPL.txt.

All other content is subject to the CC-BY-SA Unported 3.0 Licence. A copy of this licence is
included as CC-BY-SA.txt

All content in the test_corpus directory is subject to the licence in the file
test_corpus/test_corpus_licence.txt
