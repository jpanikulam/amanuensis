import numpy as np
from scipy.io import wavfile
from scipy import signal
from matplotlib import pyplot as plt

import notes

def load():
    pass


def compare_note(f, amp, min_amplitude=50000.0):
    best_note = None
    best_error = np.inf

    if amp < min_amplitude:
        return None

    for note_name, freq in notes.notes.items():
        error = np.abs(f - freq)
        if error < best_error:
            best_error = error
            best_note = note_name

    print notes.notes[best_note]
    return (best_note, amp)


def compare_notes(frequencies, times, amplitudes):
    for tn, tt in enumerate(times):
        time_notes = []
        for fn, ff in enumerate(frequencies):
            amplitude = amplitudes[fn, tn]
            note = compare_note(ff, amplitude)
            if note:
                time_notes.append(note)
                print note
        print time_notes
        if len(time_notes) >= 1:
            break


def comparogram(note_name, audio_signal, fs):
    note_freq = notes.notes[note_name]
    T = 1.0 / fs
    signal_seconds = audio_signal.shape[0] * T
    t = np.arange(0.0, 0.25, T)
    note_signal = np.sin(t * (2.0 * np.pi * note_freq))

    # correlation = np.convolve(note_signal, audio_signal / np.max(audio_signal), 'same')
    # correlation = signal.fftconvolve(audio_signal / np.max(audio_signal), note_signal, 'same')
    correlation = signal.fftconvolve(audio_signal / np.std(audio_signal), note_signal / np.std(note_signal), 'same')
    times = np.arange(0.0, signal_seconds, T)

    # plt.plot(times[::20], correlation[::20], label=' '.join(note_name))
    plt.plot(times, correlation, label=' '.join(note_name))
    # plt.plot(t, note_signal, label=' '.join(note_name))

if __name__ == '__main__':
    # fn = "/home/jacob/repos/amanuensis/data/rocky_mtn_high.wav"
    # fn = "/home/jacob/repos/amanuensis/data/john_denver_rocky_mountain_high.wav"
    # fn = "/home/jacob/repos/amanuensis/data/country_roads.wav"
    # fn = "/home/jacob/repos/amanuensis/reference_guitar.wav"
    fn = "/home/jacob/repos/amanuensis/data/tuning_reference.wav"

    fs, data = wavfile.read(fn)

    start_seconds = 70.0
    end_seconds = 80.0
    start_samples = fs * start_seconds
    end_samples = fs * end_seconds

    segment_seconds = 0.1
    segment_size = fs * segment_seconds

    # first_chunk_chan0 = data[5000:50000, 0]
    first_chunk_chan0 = data[start_samples:end_samples, 0]
    # first_chunk_chan0 = data[:, 0]

    # wavfile.write('chunk.wav', fs, first_chunk_chan0)
    # exit(0)

    # f, t, Zxx = signal.stft(first_chunk_chan0, fs, nperseg=10000)
    f, t, Zxx = signal.spectrogram(first_chunk_chan0, fs, nperseg=segment_size)

    # plt.figure('Octave 2')
    # comparogram(('E', '2'), first_chunk_chan0, fs)
    # comparogram(('A', '2'), first_chunk_chan0, fs)
    # comparogram(('D', '3'), first_chunk_chan0, fs)
    # comparogram(('G', '3'), first_chunk_chan0, fs)
    # comparogram(('B', '3'), first_chunk_chan0, fs)
    # comparogram(('E', '4'), first_chunk_chan0, fs)
    # plt.legend()
    # plt.show()

    plt.pcolormesh(t, f, np.abs(Zxx))
    plt.title('STFT Magnitude')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()
