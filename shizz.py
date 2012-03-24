#!/usr/bin/python

from youtube import *
from grabPitch import *
from audio import *
from util import *


# Music
musicvideo = "http://www.youtube.com/watch?v=censWqgjqno"

# Words
wordsvideo = "http://www.youtube.com/watch?v=EGLPADW_kUw"

# GET THE AV
wvidf, waudf = fetch_youtube(wordsvideo)
mvidf, maudf = fetch_youtube(musicvideo)

mixed = "s/OUT.wav"
outfile = "v/mixdown.flv"

# Get the key for the audio
frequencies = getKey(maudf,False)

# TODO
# AUTOTUNE

waudf_n = waudf.replace(".wav","_n.wav")
waudf_r = waudf.replace(".wav","_r.wav")
maudf_n = maudf.replace(".wav","_n.wav")

# Normalize audio
normalizeAudio(waudf,waudf_n)
normalizeAudio(maudf,maudf_n)

# Add reverb and echo
addRevEch(waudf_n,waudf_r)

# Mix the sound
mixSound(waudf_r, maudf_n, mixed)

# Put sound to the video
addSoundToVideo(mixed, wvidf, outfile)

# Clear temp files
clearFolder("s/tmp/")
clearFolder("v/tmp/")