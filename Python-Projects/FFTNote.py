import soundfile as sf
import numpy as np
import plotly.graph_objs as go

note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def freq_to_note(f):
    midi_note = int(round(69 + 12 * np.log2(f / 440)))
    octave = (midi_note // 12) - 1
    note = note_names[midi_note % 12]
    return f"{note}{octave}"

# Read in the .wav file
data, sample_rate = sf.read("test.wav")

# If the data is stereo we only need one dimension
if data.ndim > 1:
    data = data[:, 0]

window_size = 4096
windows = []

for i in range(0, len(data), window_size):
    windows.append(data[i:i + window_size])

notes = []
    
for window in windows:
    fft = np.abs(np.fft.fft(window))
    fft_freq = np.fft.fftfreq(len(window), d=1/sample_rate)

    pos_mask = fft_freq >= 0
    fft = fft[pos_mask]
    fft_freq = fft_freq[pos_mask]

    # Get most prominent frequency
    max_index = np.argmax(fft)
    max_freq = fft_freq[max_index]

    notes.append(freq_to_note(max_freq))
    
print(notes)
