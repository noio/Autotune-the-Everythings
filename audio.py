#from echonest import *
from util import *

def mixSound(fnem1,fnem2,foutnem):
  
  nfo("Mixing")
  
  cmd = 'sox -m "%s" -v 0.15 "%s" "%s"'%(fnem1, fnem2, foutnem)
  os.system(cmd)
  
  nfo("Done",True)

def monoize(f_in, f_out):

  nfo("To mono")
  
  cmd = 'sox "%s" -c 1 "%s"'%(f_in, f_out)

  os.system(cmd)
  
  nfo("Done",True)

def addRevEch(f_in, f_out):

  nfo("Adding effects")
  cmd = 'sox "%s" "%s" echo 0.8 0.6 300 0.1 gain -2 reverb'%(f_in,f_out)
  os.system(cmd)
  
  nfo("Done",True)

def normalizeAudio(f_in, f_out):

  nfo("Normalizing")

  cmd = 'sox --norm "%s" "%s"'%(f_in,f_out)
  os.system(cmd)
  
  nfo("Done",True)

def addSoundToVideo(audio, video, out):

  nfo("Merging audio and video")

  cmd = 'ffmpeg -i "%s" -i "%s" -shortest "%s"'%(audio,video,out)
  os.system(cmd)

  nfo("Done",True)