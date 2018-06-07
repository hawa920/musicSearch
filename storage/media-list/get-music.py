##################################################
# 把 download-list 清單裡面的歌曲依依下載下來並轉檔
import youtube_dl
from pydub import AudioSegment
SAMPLING_RATE = 44100
SOURCE_FILE = 'download-list'
AUDIO_FORMAT = 'mp3'

def audioDownload(url, sampleRate = 44100):

    tempname = url[32:]
    filename = '../media/{0}.{1}'.format(tempname, AUDIO_FORMAT)
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': AUDIO_FORMAT,
        }],
        'noplaylist': True,
        # this is a bug between youtube-dl and ffmpeg
        'outtmpl': filename+'%(ext)s'
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download( [url] )
    # 為了節省儲存空間，先轉檔再把取樣頻率、聲道數目都減低，取樣頻率先維持在 44.1 kHZ 
    AudioSegment.from_file(filename).set_channels(1).set_frame_rate(sampleRate).export(filename, format=AUDIO_FORMAT, parameters = ['-y'])


with open(SOURCE_FILE, 'r') as fp:
    lines = fp.readlines()

counter = 1
for line in lines:
    if line.startswith('@url:'):
        line = line[5:].replace('\n', '')
        audioDownload(line)
