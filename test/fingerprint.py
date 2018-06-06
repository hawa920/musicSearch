######################################################################
# Derive from Dejavu Project
# Porting from Python2 to Python3

import hashlib
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pydub import AudioSegment
from operator import itemgetter
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, iterate_structure, binary_erosion

######################################################################
# Some constant settings
# Can be tuned to obtained different results, accuracy

######################################################################
# Index of the zipped list
# [0] for frequencies, [1] for time
IDX_FREQ_I = 0
IDX_TIME_J = 1

######################################################################
# Sampling rate, related to the Nyquist conditions, which affects
# the range frequencies we can detect.
DEFAULT_FS = 44100

######################################################################
# Size of the FFT window, affects frequency granularity
DEFAULT_WINDOW_SIZE = 4096

######################################################################
# Ratio by which each sequential window overlaps the last and the
# next window. Higher overlap will allow a higher granularity of offset
# matching, but potentially more fingerprints.
DEFAULT_OVERLAP_RATIO = 0.5

######################################################################
# Degree to which a fingerprint can be paired with its neighbors --
# higher will cause more fingerprints, but potentially better accuracy.
DEFAULT_FAN_VALUE = 15

######################################################################
# Minimum amplitude in spectrogram in order to be considered a peak.
# This can be raised to reduce number of fingerprints, but can negatively
# affect accuracy.
DEFAULT_AMP_MIN = 10

######################################################################
# Number of cells around an amplitude peak in the spectrogram in order
# for Dejavu to consider it a spectral peak. Higher values mean less
# fingerprints and faster matching, but can potentially affect accuracy.
PEAK_NEIGHBORHOOD_SIZE = 20

######################################################################
# Thresholds on how close or far fingerprints can be in time in order
# to be paired as a fingerprint. If your max is too low, higher values of
# DEFAULT_FAN_VALUE may not perform as expected.
MIN_HASH_TIME_DELTA = 0
MAX_HASH_TIME_DELTA = 200

######################################################################
# If True, will sort peaks temporally for fingerprinting;
# not sorting will cut down number of fingerprints, but potentially
# affect performance.
PEAK_SORT = True

######################################################################
# Number of bits to throw away from the front of the SHA1 hash in the
# fingerprint calculation. The more you throw away, the less storage, but
# potentially higher collisions and misclassifications when identifying songs.
FINGERPRINT_REDUCTION = 20

def fingerprint(channel_samples,
                Fs=DEFAULT_FS,
                wsize=DEFAULT_WINDOW_SIZE,
                wratio=DEFAULT_OVERLAP_RATIO,
                fan_value=DEFAULT_FAN_VALUE,
                amp_min=DEFAULT_AMP_MIN):
    """
    FFT the channel, log transform output, find local maxima, then return
    locally sensitive hashes.
    """
    # FFT the signal and extract frequency components
    arr2D = mlab.specgram(
        channel_samples,
        NFFT=wsize,
        Fs=Fs,
        window=mlab.window_hanning,
        noverlap=int(wsize * wratio))[0] # 2Darr, freq, time

    # apply log transform since specgram() returns linear array
    # Has something to do with human hearing, consider MeL spectrum
    arr2D = 10 * np.log10(arr2D)
    arr2D[arr2D == -np.inf] = 0  # replace infs with zeros

    # find local maxima
    local_maxima = get_2D_peaks(arr2D, plot=False, amp_min=amp_min)

    # return hashes
    return generate_hashes(local_maxima, fan_value=fan_value)
    
def get_2D_peaks(arr2D, plot=False, amp_min=DEFAULT_AMP_MIN):

    struct = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(struct, PEAK_NEIGHBORHOOD_SIZE)

    # find local maxima using our fliter shape
    local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D
    background = (arr2D == 0)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

    # Boolean mask of arr2D with True at peaks
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""
      In Python3, boolean substract operation is deprecated
      However, since they are already in types of boolean,
      Applying XOR operation, or NEQ(!=) is equivelent to this 
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # detected_peaks = local_max - eroded_background
    detected_peaks = local_max ^ eroded_background

    # extract peaks
    amps = arr2D[detected_peaks]
    j, i = np.where(detected_peaks)

    # filter peaks
    amps = amps.flatten()
    peaks = zip(i, j, amps)
    peaks_filtered = [x for x in peaks if x[2] > amp_min]  # freq, time, amp

    # get indices for frequency and time
    frequency_idx = [x[1] for x in peaks_filtered]
    time_idx = [x[0] for x in peaks_filtered]

    if plot:
        # scatter of the peaks
        fig, ax = plt.subplots()
        ax.imshow(arr2D)
        ax.scatter(time_idx, frequency_idx)
        ax.set_xlabel('Time')
        ax.set_ylabel('Frequency')
        ax.set_title("Spectrogram")
        plt.gca().invert_yaxis()
        plt.show()

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""
      In Python3, zip() returns iterator, not list object,
      we have to transform it by calling list()
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # return zip(frequency_idx, time_idx)
    return list(zip(frequency_idx, time_idx))


def generate_hashes(peaks, fan_value=DEFAULT_FAN_VALUE):
    """
    Hash list structure (format of output):
       sha1_hash[0:20]    time_offset
    [(e05b341a9b77a51fd26, 32), ... ]
    """

    if PEAK_SORT:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Now peaks is type of class 'list', it has no attribute sort
        To sort the list, call sorted()
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # peaks.sort(key=itemgetter(1))
        sorted(peaks, key=itemgetter(1), reverse=False)
     
    for i in range(len(peaks)):
        for j in range(1, fan_value):
            if (i + j) < len(peaks):
                
                freq1 = peaks[i][IDX_FREQ_I]
                freq2 = peaks[i + j][IDX_FREQ_I]
                t1 = peaks[i][IDX_TIME_J]
                t2 = peaks[i + j][IDX_TIME_J]
                t_delta = t2 - t1

                if t_delta >= MIN_HASH_TIME_DELTA and t_delta <= MAX_HASH_TIME_DELTA:
                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    In Python3, Unicode-objects must be encoded before hashing
                    ;therefore, the code below is necessary
                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    temp = "%s|%s|%s" % (str(freq1), str(freq2), str(t_delta))
                    temp = str(temp).encode('utf-8')
                    # h = hashlib.sha1("%s|%s|%s" % (str(freq1), str(freq2), str(t_delta)))
                    h = hashlib.sha1(temp)
                    yield (h.hexdigest()[0:FINGERPRINT_REDUCTION], t1)

if __name__ == "__main__":

  
    DEFAULT_SAMPLING_RATE = 44100
    MUSICS_NAME = ['./storage/full.mp3', './storage/clip01.mp3', './storage/clip02.mp3', './storage/clip03.mp3', './storage/test01.wav', './storage/test02.wav', './storage/test03.wav', './storage/test04.wav']
    for FULL_MUSIC_NAME in MUSICS_NAME:
        sound = AudioSegment.from_file(FULL_MUSIC_NAME).set_channels(1).set_frame_rate(DEFAULT_SAMPLING_RATE)
        samples = sound.get_array_of_samples()

        # write to fingerprints to files
        items = list(fingerprint(samples))
        with open('./database/' + FULL_MUSIC_NAME[10:len(FULL_MUSIC_NAME) - 4] + '-fingerprints', 'w') as fp:
            for item in items:
                fp.write(item[0][:FINGERPRINT_REDUCTION] + '\n')
    # Is there any information lost during the conversion between mp3 and wav, how to overcome the issues like this ...?
 
