# test loadint *.mp3 using pydub.AudioSegment.from_mp3()
from pydub import AudioSegment

if __name__ == "__main__":

    DEFAULT_SAMPLING_RATE = 44100
    FULL_MUSIC_NAME = '../storage/full-216s.mp3'
    sound = AudioSegment.from_mp3(FULL_MUSIC_NAME).set_channels(1).set_frame_rate(DEFAULT_SAMPLING_RATE)
    samples = sound.get_array_of_samples()