
def nfo(m, done=False):
  
  x = "> "+str(m)
  
  if done:
    x = x+"."
  else:
    x = x+"..."

  print x 