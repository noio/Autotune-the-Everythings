import os

def nfo(m, done=False):
  
  x = "> "+str(m)
  
  if done:
    x = x+"."
  else:
    x = x+"..."

  print x

def wtf(content, uri):
  f = open(uri, 'wb') 
  nfo("Storing "+uri)
  f.write(content)
  nfo("Stored "+uri,True)
  f.close()

def wavToMp3(uri):
  cmd = 'ffmpeg -i "%s" "s/%s.wav"'%(uri, uri[0:(len(uri)-4)])
  os.system(cmd)