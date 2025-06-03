from scipy.io import wavfile
import numpy as np
import math
import cmath

'''sampling_rate,data=wavfile.read('Test.wav')
data=[sum(z)/len(z) for z in data][:3000]
num_samples=len(data)'''

#function_to_evaluate=input('Enter a function, using x as the variable (imagine it is y=...): ')

sampling_rate=8
num_samples=8
# Test: 1 Hz sine wave with amplitude of 1, 8 samples and sampling rate is 8 Hz; y=sin(x)
data=[0,math.sqrt(2)/2,1,math.sqrt(2)/2,0,-math.sqrt(2)/2,-1,-math.sqrt(2)/2]
# 1 Hz cosine wave with amplitude of 1, 8 samples and sampling rate is 8 Hz;y=cos(x)
data=[1,math.sqrt(2)/2,0,-math.sqrt(2)/2,-1,-math.sqrt(2)/2,0,math.sqrt(2)/2]
# Linear function; y=x
data=[1,2,3,4,5,6,7,8]


sampling_resolution=sampling_rate/num_samples

fourier_coefficients = {}
for k in range(len(data)):
    total = 0
    for j in range(len(data)):
        x = -(2 * math.pi * j * k) / len(data)
        # Euler's formula; e**(i*x) = cos(x) + i*sin(x)
        value = data[j] * math.cos(x) + data[j] * complex(0, 1) * math.sin(x)
        total += value
    fourier_coefficients[k] = total

magnitudes = {}
for key, val in fourier_coefficients.items():
    magnitude = math.sqrt(val.imag**2 + val.real**2)
    magnitudes[key] = magnitude

# Compute the phase before scaling the Fourier coefficients
# Dividing by the Nyquist limit: sampling rate divided by 2. This prevents aliasing - unwanted frequencies will be high, and the audio will be distorted.
phase = {y: cmath.phase(fourier_coefficients[y]) for y in list(fourier_coefficients)[:sampling_rate//2]}

# Average over the number of samples - since half of the values were discarded the remaining will be scaled by 2
magnitudes = {y: (magnitudes[y] * 2) / num_samples for y in list(magnitudes)[:sampling_rate//2]}
new_magnitudes = {}
for key in magnitudes:
    new_magnitudes[key*sampling_resolution]=magnitudes[key]
new_phase={}
for key_2 in phase:
    new_phase[key_2*sampling_resolution]=phase[key_2]

fourier_coefficients = {y: (fourier_coefficients[y] * 2) for y in list(fourier_coefficients)[:sampling_rate//2]}

print(new_magnitudes)
print(new_phase)
