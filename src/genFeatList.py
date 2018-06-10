# 建立 sequential index
# 用來做 sequential search 測試
import os
import re
import json
import hashlib
import featExtractor
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pydub import AudioSegment
from operator import itemgetter
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, iterate_structure, binary_erosion

FINGERPRINT_REDUCTION = 20
SAMPLING_RATE = 44100
OUT_FILE = '../storage/flist/featuresList'
MUSIC_POOL = '../storage/music/'
items = os.listdir(MUSIC_POOL)
features = {}
cnt = 0
existList = {}
try:
    with open(OUT_FILE, 'r') as fp:
        existList = json.load(fp)
except:
    pass
    
for item in items:
    if existList.get(re.sub('\.\w*', '', item)) != None:
        continue
    
    cnt += 1
    sound = AudioSegment.from_file(MUSIC_POOL + item).set_channels(1).set_frame_rate(SAMPLING_RATE)
    samples = sound.get_array_of_samples()
    # get fingerprint of the music
    finpnts = list(featExtractor.fingerprint(samples))
    # ignore the time ofst, remove the duplicated
    finpnts = list(set([x[0] for x in finpnts]))
    features[item.replace('.mp3', '')] = finpnts
    print('finished [{0}] extraction'.format(cnt))



with open(OUT_FILE, 'a') as fp:
        fp.write(json.dumps(features))

