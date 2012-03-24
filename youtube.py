import subprocess
import os
from urllib import urlopen, unquote
from urlparse import parse_qs, urlparse

from util import *

import aubio

def fetch_youtube(youtube_url, output=None, silent=False):
    
    #
    # Fetches a Youtube video and audi000000
    #
    # returns (videofilename, audiofilename)
    #

    nfo("Youtube")

    if '?v=' in youtube_url:
        video_id = parse_qs(urlparse(youtube_url).query)['v'][0]
    else:
        video_id = youtube_url
    if output is None:
        output = video_id

    nfo("Downloading")
    info = parse_qs(unquote(urlopen('http://www.youtube.com/get_video_info?&video_id=' + video_id).read().decode('utf-8')))
    #print '\n'.join(map(str,info.items()))

    if 'url' in info:
        getvidurl = info['url'][0]
        fmt = 'mp4'
    else:
        getvidurl = info['url_encoded_fmt_stream_map'][0][4:]
        fmt = 'flv'
    #print getvidurl
    
    vidfilename = 'v/tmp/%s.%s' % (output, fmt)
    vidfile = open(vidfilename, 'wb')
    vidfile.write(urlopen(getvidurl).read())

    cmd = 'ffmpeg -i "%s" "%s.wav"'%(vidfilename, output)
    print cmd
    os.system(cmd)
    


    nfo("Downloaded",True)
    nfo("FFMPEG sheit")

    cmd = 'ffmpeg -i "%s" "s/tmp/%s.wav"'%(vidfilename, output)
    os.system(cmd)
    nfo("FFMPEG done",True)

    return vidfilename, "s/tmp/"+output+".wav"
