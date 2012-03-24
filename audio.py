from echonest import audio
from util import *

def mixSound(fnem1,fnem2,foutnem):
  
  nfo("Mixing")
  
  cmd = 'sox -m "%s" "%s" "%s"'%(fnem1, fnem2, foutnem)
  os.system(cmd)
  
  nfo("Done",True)

def addRevEch(f_in, f_out):

  nfo("Adding effects")
  cmd = 'sox "%s" "%s" echo 0.8 0.6 300 0.1 gain -2 reverb'%(f_in,f_out)
  os.system(cmd)
  
  nfo("Done",True)