import os
import re
import json
import time
import hashlib
import featExtractor
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pydub import AudioSegment
from collections import Counter
from operator import itemgetter
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, iterate_structure, binary_erosion
import base64
from flask import Flask, request, send_from_directory, send_file, make_response, render_template

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def main():
  if request.method == 'POST':
    return 'Bad Request.'
  return render_template('index.html')


@app.route('/js/mp3Worker.js', methods = ['GET'])
def mp3Worker():
  return app.send_static_file('js/mp3Worker.js')


@app.route('/js/recorderWorker.js', methods = ['GET'])
def recordWorker():
  return app.send_static_file('js/recorderWorker.js')

@app.route('/js/libmp3lame.min.js', methods = ['GET'])
def libmp3lame():
  return app.send_static_file('js/libmp3lame.min.js')


@app.route('/musicSearch', methods = ['POST'])
def musicSearch():
  mp3signals = request.form['data']
  pos = mp3signals.find(',')
  mp3signals = base64.b64decode(mp3signals[pos:])
  with open('./demo.mp3', 'wb') as fp:
    fp.write(mp3signals)
  
  # music search
  CORECTNESS_THRESHHOLD = 0.009
  SAMPLING_RATE = 44100
  FEATLIST = '../../storage/flist/invFeaturesList'
  TEST_CLIP = './demo.mp3'

  # load features list
  start_time = time.time()
  with open(FEATLIST, 'r') as fp:
      invidx = json.load(fp) #this is the bottle neck
  print('Time to build inverted index {0}'.format(time.time() - start_time))
  print('the length of the hash table {0}'.format(len(invidx)))
  # inverted index search
  classfy = []
  start_time = time.time()
  classfy.clear()
  sound = AudioSegment.from_file(TEST_CLIP).set_channels(1).set_frame_rate(SAMPLING_RATE)
  samples = sound.get_array_of_samples()
  thisFeats = list(featExtractor.fingerprint(samples)) 
  thisFeats = list(set([x[0] for x in thisFeats]))
  # iterate fingerprints (a.k.a. the keywords)
  for keyword in thisFeats:
      try:
          classfy.extend(invidx[keyword])
      except:
          pass
  # maximum matching
  resultlist = [[key, cnt] for key, cnt in Counter(classfy).items()]
  try:
      result = max(resultlist, key = itemgetter(1)) # 0:key, 1:cnt
      # 下次可改成先算 rate 用rate的 max來判斷
      correct_rate = result[1] / len(thisFeats)
      if correct_rate >= CORECTNESS_THRESHHOLD:
          ret = 'Result:\t{0}\tRate:{1}\tTime:{2}'.format('https://www.youtube.com/watch?v=' + result[0], correct_rate, time.time() - start_time)
          print(ret)
          return ret
      else:
          raise Exception
  except:
      ret = 'Result:\tNot Found' + str(correct_rate > CORECTNESS_THRESHHOLD)



  return ret

@app.route('/<path:dummy>', methods = ['GET', 'POST'])
def fallback(dummy):
  return 'bro......'

if __name__ == "__main__":
  app.run(port=5005, debug=True)
  # Comment the line above and use the line below if you launch on your own server
  # app.run(host='0.0.0.0', port=5005, debug = False)
