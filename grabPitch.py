#!/usr/bin/python

import sys
from aubio.task import *
from music21 import *
from util import *

def getKey(filename, midinotes=True):

  #
  # Tries to estimate the key for an audio file
  #
  # returns a list of frequencies
  #

  nfo("Start getKey")
  nfo("Calculating pitches")

  mode = "yin"
  bufsize = 4096  
  hopsize = float(bufsize) / 2

  params = taskparams()
  params.samplerate = float(sndfile(filename).samplerate())
  params.hopsize    = int(float(bufsize) / 2)
  params.bufsize    = bufsize
  params.step       = params.samplerate/float(hopsize)
  params.units      = "midi"
  params.pitchmax   = 83

  wplot,oplots,titles = [],[],[]

  pitch = []
  params.pitchmode  = mode
  filetask = taskpitch(filename,params=params)
  pitch = filetask.compute_all()

  nfo("Calculated pitches")

  pitchlist = []
  notes = stream.Stream()

  i=0
  for schnoof in pitch:
    schnooi = int(schnoof)
    if i%2==1 and schnooi!=-1:
      pitchlist.append(schnooi)
      n = note.Note()
      n.pitch.midi = schnooi
      n.quarterLength = 1
      notes.append(n)
      
    i+=1

  nfo("KrumhanslKessler")

  base = analysis.discrete.analyzeStream(notes, 'KrumhanslKessler').getScale().transpose(-36).pitches
  pitches = []

  nfo("KrumhanslKesslerized", True)

  if midinotes:
    for y in base:
      n = note.Note()
      n.pitch = y
      if not n.pitch.midi in pitches:
        pitches.append(n.pitch.midi)
      for i in range(5):
        n.pitch.midi += 12
        if not n.pitch.midi in pitches:
          pitches.append(n.pitch.midi)
  else:
    for y in base:
      n = note.Note()
      n.pitch = y
      if not n.pitch.frequency in pitches:
        pitches.append(n.pitch.frequency)
      for i in range(5):
        n.pitch.frequency += 12
        if not n.pitch.frequency in pitches:
          pitches.append(n.pitch.frequency)


  pitches.sort()
  return pitches