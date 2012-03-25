#!/usr/bin/python

#
# Music Hack Day 2012 Amsterdam
# Tom Aizenberg, Gilles de Hollander & Thomas van den Berg
#
# Usage: python shizz.py musicyoutubeURL textyoutubeURL
#
# You will need all kinds of craaaazy libraries like scipy and aubio!
#

from youtube import *
from grabPitch import *
from audio import *
from util import *
from harmonizer import *
import random
import string


if sys.argv[1]:
  # Music
  musicvideo = sys.argv[1]
else:
  # Music
  musicvideo = "http://www.youtube.com/watch?v=censWqgjqno"

if sys.argv[2]:
  # Music
  wordsvideo = sys.argv[2]
else:
  # Words
  wordsvideo = "http://www.youtube.com/watch?v=EGLPADW_kUw"

# GET THE AV
wvidf, waudf = fetch_youtube(wordsvideo)
mvidf, maudf = fetch_youtube(musicvideo)

'''
Sad piano music: http://www.youtube.com/watch?v=TzrYvXT1o8s
Tomdehaan: http://www.youtube.com/watch?v=bHi0-HCxf5s

wvidf = "v/tmp/gJkSaidnpx8.flv"
waudf = "s/tmp/gJkSaidnpx8.wav"
mvidf = "v/tmp/censWqgjqno.flv"
maudf = "s/tmp/censWqgjqno.wav"
'''

mixed = "s/tmp/audiomixdown.wav"

r_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
outfile = "v/mixdown_"+r_string+".flv"

# Get the key for the audio
frequencies = getKey(maudf,False)

waudf_n = waudf.replace(".wav","_n.wav")
waudf_h = waudf.replace(".wav","_harm.wav")
waudf_r = waudf.replace(".wav","_r.wav")

maudf_n = maudf.replace(".wav","_n.wav")
maudf_m = maudf_n.replace(".wav","_mono.wav")

# Autotune
harmonize_wav_file(waudf, frequencies)

# Normalize audio
normalizeAudio(waudf_h,waudf_n)
normalizeAudio(maudf,maudf_n)

# Add reverb and echo
addRevEch(waudf_n,waudf_r)

# Make music mono
monoize(maudf_n, maudf_m)

# Mix the sound
mixSound(waudf_r, maudf_m, mixed)

# Put sound to the video
addSoundToVideo(mixed, wvidf, outfile)

# Clear temp files
clearFolder("s/tmp/")
clearFolder("v/tmp/")