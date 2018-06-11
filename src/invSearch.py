# 產生反轉索引, 用 python dict, list, set 模擬測試
# 做 maximum matching, 當作判斷結果

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

if __name__ == "__main__":

    CORECTNESS_THRESHHOLD = 0.009
    SAMPLING_RATE = 44100
    FEATLIST = '../storage/flist/invFeaturesList'
    TEST_CLIP_DIR = '../storage/clips/'

    # load features list
    start_time = time.time()
    with open(FEATLIST, 'r') as fp:
        invidx = json.load(fp)
    print('Time to build inverted index {0}'.format(time.time() - start_time))
    print('the length of the hash table {0}'.format(len(invidx)))
    # inverted index search
    classfy = []
    items = os.listdir(TEST_CLIP_DIR)
    items = sorted(items)
    for item in items:
        start_time = time.time()
        classfy.clear()
        sound = AudioSegment.from_file(TEST_CLIP_DIR + item).set_channels(1).set_frame_rate(SAMPLING_RATE)
        samples = sound.get_array_of_samples()
        thisFeats = list(featExtractor.fingerprint(samples)) # this is the bottle neck
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
            correct_rate = result[1] / len(thisFeats)
            if correct_rate >= CORECTNESS_THRESHHOLD:
                print('{0}\t{1}\tRate:{2}\tTime:{3}'.format(item, 'https://www.youtube.com/watch?v=' + result[0], correct_rate, time.time() - start_time))
            else:
                raise Exception
        except:
            print('{0}\tNot Found'.format(item))