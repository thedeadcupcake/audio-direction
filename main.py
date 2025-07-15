import pyaudio 
import numpy as np

from util import audio_slicer

pya = pyaudio.PyAudio()

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 60
WAVE_OUTPUT_FILENAME = "output.wav"


def get_virtual_cable_index():
    for i in range(pya.get_device_count()):
        if "CABLE Output" in pya.get_device_info_by_index(i)["name"]:
            return i
        
    print("No virtual cable found!")

    return None


def main():
        print("Recording...")

        stream = pya.open(rate=RATE, channels=CHANNELS, format=FORMAT, input_device_index=get_virtual_cable_index(), input=True, frames_per_buffer=CHUNK)

        for i in range((RATE//CHUNK) * RECORD_SECONDS):
            data = stream.read(CHUNK)
            samples = np.frombuffer(data, dtype=np.int16)
            
            # detects sharper sounds like gunshots
            onset_timestamp = audio_slicer.has_onset(samples, "stereo")
            if onset_timestamp:
                current_timestamp = (i * CHUNK) / RATE

                peakL, peakR = audio_slicer.get_peak_LR_balance(samples)
                audio_slicer.get_timestamp_LR_balance(samples, current_timestamp, onset_timestamp/2) # onset timestamp will be double the actual due to 2 channel input

                audio_slicer.print_balance(audio_slicer.get_balance(peakL, peakR))   

        print("Finished")

        
        pya.terminate()
       

if __name__ == "__main__":
    main()