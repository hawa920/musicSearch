# 這隻程式會把 '../storage/clips/' 的音檔一一讀入
# 依據 '../storage/flist/featuresList' 中的
# fingerprints 做 sequential search, 分類問題,
# 把搜尋分數 (maximum match) 最高的當作分類結果
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
from operator import itemgetter
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, iterate_structure, binary_erosion

if __name__ == "__main__":

    SAMPLING_RATE = 44100
    FEATLIST = '../storage/flist/seqFeaturesList'
    TEST_CLIP_DIR = '../storage/clips/'

    # load features list
    start_time = time.time()
    with open(FEATLIST, 'r') as fp:
        features = json.load(fp)
    print('Time to generate sequential index {0}'.format(time.time() - start_time))
    print('the length of the hash table {0}'.format(len(features)))
    items = os.listdir(TEST_CLIP_DIR)
    items = sorted(items)
    result = {}

    for item in items:

        result.clear()
        print('Now playing ' + item)
        sound = AudioSegment.from_file(TEST_CLIP_DIR + item).set_channels(1).set_frame_rate(SAMPLING_RATE)
        samples = sound.get_array_of_samples()
        finpnts = list(featExtractor.fingerprint(samples))
        finpnts = list(set([x[0] for x in finpnts]))
        # Sequential Search Test
        for finpnt in finpnts:
            for key, val in features.items():
                if finpnt in val:
                    try:
                        result[key] += 1
                    except:
                        result[key] = 0
        
        sort_result = sorted(result.items(), key = itemgetter(1), reverse = True)
        for iterate in sort_result:
            print(iterate)
        print('')