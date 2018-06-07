import musicExtractor
import os
import re
import json
import hashlib
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pydub import AudioSegment
from operator import itemgetter
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, iterate_structure, binary_erosion

FINGERPRINT_REDUCTION = 20
DEFAULT_SAMPLING_RATE = 44100
MEDIA_POOL = '../../storage/media/'
features = {}
items = os.listdir(MEDIA_POOL)

for item in items:
    sound = AudioSegment.from_file(MEDIA_POOL + item).set_channels(1).set_frame_rate(DEFAULT_SAMPLING_RATE)
    samples = sound.get_array_of_samples()
    # feature list
    feats = list(musicExtractor.fingerprint(samples))
    feats = [x[0] for x in feats]
    features[item.replace('.mp3', '')] = '|'.join(feats)

with open('./featuresList', 'w') as fp:
        fp.write(json.dumps(features))

