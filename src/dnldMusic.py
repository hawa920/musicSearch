# 這隻程式會去讀取 '../storage/mlist/downloadList' 
# 把裡面欲下載的歌曲透過 youtube-dl python api 下載回來
# 在透過 ffmpeg 或者 pydub.AudioSegment 把音檔轉成單聲
# 道, 取樣頻率 44.1kHz, 為的是減少儲存空間使用
import youtube_dl
from pydub import AudioSegment
SAMPLING_RATE = 44100 # Nyquist Theorem
SRC_FILE = '../storage/mlist/downloadList'
AUDIO_FORMAT = 'mp3' # Preferred audio format, less storage cost

def audioDownload(url, sampleRate = 44100):
    """ Download the audio(soundtrack) from
    given YouTube url with youtube-dl package.
    In order to save the storage size, the audio
    file will be converted into mp3 format with 
    only 1 channel left, sampling rate set to 
    44.1 kHz as default.
    """
    token = url[32:]
    filename = '../storage/music/{0}.{1}'.format(token, AUDIO_FORMAT)
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

    AudioSegment.from_file(filename).set_channels(1).set_frame_rate(sampleRate).export(filename, format=AUDIO_FORMAT, parameters = ['-y'])


if __name__ == "__main__":
    
    with open(SRC_FILE, 'r') as fp:
        lines = fp.readlines()
    counter = 0
    for line in lines:
        if line.startswith('@url:'):
            counter += 1
            line = line[5:].replace('\n', '')
            audioDownload(line)
            print('[{0}] Finished dowloading {1}'.format(counter, line[32:]))
