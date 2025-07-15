import math
import numpy as np
import aubio

FREQ_MIN = 20
FREQ_MAX = 20000


onset = aubio.onset("default", 2048, 1024, 44100)
onset_L = aubio.onset("default", 1024, 512, 44100)
onset_R = aubio.onset("default", 1024, 512, 44100)

onset.set_threshold(0.1)
onset_L.set_threshold(0.2)
onset_R.set_threshold(0.2)

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

    return left, right


def get_timestamp_LR_balance(data: np.ndarray, curent_time: float, timestamp: float):
    left, right = split_LR_channels(data)


def get_peak_LR_balance(data: np.ndarray):
    left, right = split_LR_channels(data)

    peakL = np.abs(np.max(left))
    peakR = np.abs(np.max(right))

    return peakL, peakR


def has_onset(data: np.ndarray, type: str):
    onset_obj = None

    match type:
        case "left":
            onset_obj = onset_L
        case "right":
            onset_obj = onset_R
        case "stereo":
            onset_obj = onset


    if onset_obj(data.astype(np.float32)):
        return onset_obj.get_last_s()
    
    return False


def get_balance(left_amp: int, right_amp: int):
    left_amp = np.int32(left_amp)
    right_amp = np.int32(right_amp)
    total = np.add(left_amp, right_amp)

    if total == 0:
        return 0.5
    
    return right_amp/total


def print_balance(balance: float, width: int=31):
    balance = max(0.0, min(1.0, balance))  # clamp to [0, 1]
    center = width // 2
    pointer_pos = int(balance * width)
    pointer_pos = min(pointer_pos, width - 1)

    scale = ["-"] * width
    scale[pointer_pos] = "|"
    print("L " + "".join(scale) + " R")