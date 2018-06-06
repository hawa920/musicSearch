from pydub import AudioSegment

if __name__ == "__main__":
    with open('./database/full-fingerprints', 'r') as fp:
        lines = fp.readlines()

d = {}
for line in lines:
    hashval = line[2:22]
    d[hashval] = True

testFiles = [ './database/clip01-fingerprints', './database/clip02-fingerprints', './database/clip03-fingerprints',
    './database/test01-fingerprints', './database/test02-fingerprints', './database/test03-fingerprints', './database/test04-fingerprints']
for tester in testFiles:
    with open(tester, 'r') as fp:
        lines = fp.readlines()
    cnt = 0
    for line in lines:
        hashval = line[2:22]
        if hashval in d:
            # print('found')
            cnt +=1
    print(tester, ":\t", cnt)
