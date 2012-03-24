#!/usr/bin/python

from youtube import *
from grabPitch import *
from audio import *
from util import *

musicvideo = "http://www.youtube.com/watch?v=6A3JstGlHO4"
wordsvideo = "http://www.youtube.com/watch?v=bHi0-HCxf5s"

#wvidf, waudf = fetch_youtube(wordsvideo)
#mvidf, maudf = fetch_youtube(musicvideo)

key = getKey("s/test.wav",False)

#print mvidf
#print maudf
print key
'''

normalizeAudio("s/tomdehaandef.wav","s/tomdehaandef.wav")
normalizeAudio("s/testdef.wav","s/testdef2.wav")
addRevEch("s/tomdehaandef.wav","s/tomrvd.wav")
mixSound("s/testdef.wav","s/tomrvd.wav","s/test_out.wav")
'''