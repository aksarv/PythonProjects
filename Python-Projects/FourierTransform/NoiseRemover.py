"""
This program aims to remove excessively high or low frequencies the user wishes to remove using the Fast Fourier Transform package in the scipy module.
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from scipy.io import wavfile

sample_rate, data_values = wavfile.read("Test3.wav")

data_fft = fftpack.fft(data_values)

# These values can be used for further analysis/visualisation but are not needed here to remove the frequencies from the signal
amplitudes = np.abs(data_fft)
angles = np.angle(data_fft)

duration = data_values.shape[0] / sample_rate
time_step = duration / data_values.shape[0]
data_frequencies = fftpack.fftfreq(data_values.shape[0], d=time_step)

"""
# The following code allows the input wave file to be viewed in the frequency domain to aid the user in their filtering selection that is to follow.
# However due to the blocking nature of plt.show() it should be commented out first.
plt.plot(data_frequencies,amplitudes)
plt.show()
"""

threshold_frequency=int(input("Enter the threshold frequency "))
low_or_high=bool(input("Do you want to remove frequencies above this threshold or below? Enter 1 for above and 0 for below "))

denoised_fft = data_fft.copy()

if low_or_high:
    denoised_fft[np.abs(data_frequencies) > threshold_frequency] = 0
else:
    denoised_fft[np.abs(data_frequencies) < threshold_frequency] = 0

denoised_signal = fftpack.ifft(denoised_fft)

denoised_signal = np.real(denoised_signal)

if data_values.dtype == np.int16:
    denoised_signal = np.clip(denoised_signal / 2, -32768, 32767).astype(np.int16)
elif data_values.dtype == np.float32 or data_values.dtype == np.float64:
    denoised_signal = np.clip(denoised_signal / 2, -1.0, 1.0)

output_filename = f'{time.time()}.wav'
wavfile.write(output_filename, sample_rate, denoised_signal)

print(f"Modified WAV file saved as {output_filename}")
