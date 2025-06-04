import sounddevice as sd
import numpy as np
import pyautogui
from scipy.io import wavfile

sample_rate = 44100
block_size = 512
channels = 1

pyautogui.moveTo(500, 300)


def audio_callback(indata, frames, time, status):
    if status:
        print("Status:", status)

    audio_block = indata[:, 0]
    rms = np.sqrt(np.mean(audio_block ** 2))
    if rms > 0.01:
        pyautogui.keyDown("up")
    else:
        pyautogui.keyUp("up")


with sd.InputStream(callback=audio_callback, channels=channels, samplerate=sample_rate, blocksize=block_size):
    print("Listening...")
    try:
        while True:
            sd.sleep(1000)
    except KeyboardInterrupt:
        print("...stopped")
