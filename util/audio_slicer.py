import math
import numpy as np

FREQ_MIN = 20
FREQ_MAX = 20000

def segment_log(min: int, max: int, segments: int):
    log_min = math.log10(min)
    log_max = math.log10(max)
    step = ((log_max - log_min) / segments)
    
    freq_list = [min]

    for i in range(1, segments+1):
        exponent = log_min + (step * i)
        freq_list.append(math.floor(math.pow(10, exponent)))


    return freq_list


def split_LR_channels(data: np.ndarray):
    left = data[0::2]
    right = data[1::2]

    left_bytes = np.ndarray.tobytes(left)
    right_bytes = np.ndarray.tobytes(right)


    return left_bytes, right_bytes


def extract_frequencies(data, segments: int = 20):
    data = data * np.hanning(len(data))
    fft = abs(np.fft.fft(data).real)
    freq = np.fft.fftfreq()
