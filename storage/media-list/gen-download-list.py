#################################################
# 從原始爬蟲資料(rawRecords)翠取出欲下載的音檔
import re
from operator import itemgetter
#################################################
# 選擇要按照 (___) 欄位來排序
SORT_BY = 'cview'
#################################################
# 輸出的檔名路徑
OUT_FILE = './download-list'
#################################################
# 共要從排序結果中取前 (__) 筆資料寫入 OUT_FILE
NUM_MUSIC = 10
# list that stores the extracted data
bulks = []

with open('./raw-records', 'r') as fp:
    for line in fp:

        line = line.replace('\n', '')
        if line.startswith('@url:'):
            url = line[5:]
        elif line.startswith('@title:'):
            title = line[7:]
        elif line.startswith('@vlen:'):
            vlen = line[6:]
        elif line.startswith('@cview:'):
            cview = line[7:]
            temp = re.findall('\d', cview)
            cview = ''.join(temp)
            try:
                cview = int(cview)
            except:
                cview = 0
        elif line.startswith('@clike:'):
            clike = line[7:]
            temp = clike.replace('千', '000').replace('萬', '0000').replace('億', '00000000')
            temp = re.findall('\d', temp)
            clike = ''.join(temp)
            try:
                clike = int(clike)
            except:
                clike = 0
        elif line.startswith('@chate:'):
            chate = line[7:]
            temp = chate.replace('千', '000').replace('萬', '0000').replace('億', '00000000')
            temp = re.findall('\d', temp)
            chate = ''.join(temp)
            try:
                chate = int(chate)
            except:
                chate = 0
        elif line.startswith('@owner:'):
            owner = line[7:]
        elif line.startswith('@pubtime:'):
            pubtime = line[14:18]
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

# 按照 SORT_BY 排序，預設為降序排序
bulks = sorted(bulks, key = itemgetter(SORT_BY), reverse = True)
# 輸出至檔案
with open(OUT_FILE, 'w') as fp:
    for item in bulks[:NUM_MUSIC]:
        fp.write('@title:{0}\n@url:{1}\n'.format(item['title'], item['url']))