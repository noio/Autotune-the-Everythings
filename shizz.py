#!/usr/bin/python

from youtube import *
from grabPitch import *

musicvideo = "http://www.youtube.com/watch?v=6A3JstGlHO4"
wordsvideo = "http://www.youtube.com/watch?v=bHi0-HCxf5s"

mvidf, maudf = fetch_youtube(wordsvideo)

key = getKey(maudf)

print mvidf
print maudf
print key