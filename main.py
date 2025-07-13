import pyaudio 
import numpy as np
import wave

pya = pyaudio.PyAudio()

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"


def get_virtual_cable_index():
    for i in range(pya.get_device_count()):
        if "CABLE Output" in pya.get_device_info_by_index(i)["name"]:
            return i
        
    print("No virtual cable found!")

    return None


def main():
    with wave.open("output.wav", "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(sampwidth=pyaudio.get_sample_size(format=FORMAT))
        wf.setframerate(RATE)
        
        print("Recording...")

        stream = pya.open(rate=RATE, channels=CHANNELS, format=FORMAT, input_device_index=get_virtual_cable_index(), input=True, frames_per_buffer=CHUNK)

        for i in range((RATE//CHUNK) * RECORD_SECONDS):
            data = stream.read(CHUNK)

            wf.writeframes(data=data)
    

        print("Finished")

        
        pya.terminate()
       


if __name__ == "__main__":
    main()