# 建反轉索引表
# 存在 '../storeage/flist/invFeaturesList'
import time
import json
FEATLIST = '../storage/flist/seqFeaturesList'
OUT_FILE = '../storage/flist/invFeaturesList'
with open(FEATLIST, 'r') as fp:
    features = json.load(fp)

# build inverted index
invidx = {}
start_time = time.time()
for key, val in features.items():
    for fpt in val:
        try:
            invidx[fpt].append(key)
        except:
            invidx[fpt] = [key]

# remove redundent
for key, val in invidx.items():
    invidx[key] = list(set(invidx[key]))
with open(OUT_FILE, 'w') as fp:
    fp.write(json.dumps(invidx))
print('Time to build inverted index {0}'.format(time.time() - start_time))