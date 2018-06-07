# 這隻程式是用來產生欲下載的音樂清單, 使用者應先透過一 youtubeCrawler 
# 先產生一資料檔(defaultPath:='../storage/mlist/crawledRecords'),
# 透過這隻程式可以將crawledRecords的資料按所選取欄位排序, 並依據NUM_MUSIC
# 去選出符合的前 K 筆將資料寫入 '../storage/mlist/downloadList' 之中。
import re
from operator import itemgetter

SORT_FIELD = 'cview' # sort by ['cview', 'clike', 'chate', 'pubtime', 'nsubscribe']
SRC_FILE = '../storage/mlist/crawledRecords'
OUT_FILE = '../storage/mlist/downloadList'
NUM_MUSIC = 10 # number of music to be returned

bulks = []
with open(SRC_FILE, 'r') as fp:
    lines = fp.readlines()

# 從原始爬蟲資料萃取資訊, 詳細可參考以下,
# https://github.com/Howard19960920/youtubeCrawler/blob/master/src/myCrawl.py

for line in lines:
    
    line = line.replace('\n', '') 
    # extract media url
    if line.startswith('@url:'):
        url = line[5:]
    # extract media title
    elif line.startswith('@title:'):
        title = line[7:]
    # extract media length
    elif line.startswith('@vlen:'):
        vlen = line[6:]
    # extract media count of views
    elif line.startswith('@cview:'):
        cview = line[7:]
        temp = re.findall('\d', cview)
        cview = ''.join(temp)
        try:
            cview = int(cview)
        except:
            cview = 0
    # extract video count of likes
    elif line.startswith('@clike:'):
        clike = line[7:]
        temp = clike.replace('千', '000').replace('萬', '0000').replace('億', '00000000')
        temp = re.findall('\d', temp)
        clike = ''.join(temp)
        try:
            clike = int(clike)
        except:
            clike = 0
    # extract media count of hates
    elif line.startswith('@chate:'):
        chate = line[7:]
        temp = chate.replace('千', '000').replace('萬', '0000').replace('億', '00000000')
        temp = re.findall('\d', temp)
        chate = ''.join(temp)
        try:
            chate = int(chate)
        except:
            chate = 0
    # extract media owner
    elif line.startswith('@owner:'):
        owner = line[7:]
    # extract media's publish time
    elif line.startswith('@pubtime:'):
        pubtime = line[14:18]
    # extract count of subscribe
    elif line.startswith('@subscribe:'):
        subscribe = line[11:]
        temp = subscribe.replace('千', '000').replace('萬', '0000').replace('億', '00000000')
        temp = re.findall('\d', temp)
        subscribe = ''.join(temp)
        try : 
            subscribe = int(subscribe)
        except:
            subscribe = 0
        bulk = {

            "url" : url,
            "title" : title,
            "vlen" : vlen,
            "cview" : cview,
            "clike" : clike,
            "chate" : chate,
            "owner" : owner,
            "pubtime" : pubtime,
            "subscribe" : subscribe 
        }
        bulks.append(bulk)

bulks = sorted(bulks, key = itemgetter(SORT_FIELD), reverse = True) # display in descending order
with open(OUT_FILE, 'w') as fp:
    for item in bulks[:NUM_MUSIC]:
        fp.write('@title:{0}\n@url:{1}\n'.format(item['title'], item['url']))