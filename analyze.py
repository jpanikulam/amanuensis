import numpy as np
from scipy.io import wavfile
from scipy import signal
from matplotlib import pyplot as plt

import notes


def load():
    pass


def compare_note(f):
    best_note = None
    best_error = np.inf
    best_freq = None

    for note_name, freq in notes.notes.items():
        error = np.abs(f - freq)
        if error < best_error:
            best_error = error
            best_note = note_name

    best_freq = notes.notes[best_note]
    return (best_note, best_freq)


def comparogram(note_name, audio_signal, fs):
    note_freq = notes.notes[note_name]
    T = 1.0 / fs
    signal_seconds = audio_signal.shape[0] * T
    t = np.arange(0.0, T * 5.0, T)
    note_signal = np.sin(t * (2.0 * np.pi * note_freq))

    correlation = signal.fftconvolve(audio_signal / np.std(audio_signal), note_signal / np.std(note_signal), 'same')
    times = np.arange(0.0, signal_seconds, T)
    plt.plot(times, correlation, label=' '.join(note_name))


def compare(freq, audio_signal, fs):
    T = 1.0 / fs
    t = np.arange(0.0, 0.25, T)
    note_signal = np.sin(t * (2.0 * np.pi * freq))
    correlation = signal.fftconvolve(audio_signal / np.std(audio_signal), note_signal / np.std(note_signal), 'same')
    return correlation


def detect_harmonics(note_name, audio_signal, fs):
    # MIN_POWER = 1.2e10
    T = 1.0 / fs
    signal_seconds = audio_signal.shape[0] * T
    times = np.arange(0.0, signal_seconds, T)

    fundamental_frequency = notes.notes[note_name]
    # harmonics = range(1, 4 + 1)
    harmonics = [(1.0 / 4.0), (1.0 / 3.0), (1.0 / 2.0), 1.0, 2.0, 3.0]

    present_harmonics = np.zeros((audio_signal.shape[0], len(harmonics)))

    for i in range(len(harmonics)):
        harmonic_freq = fundamental_frequency * harmonics[i]
        print harmonic_freq
        likely_note = compare_note(harmonic_freq)[0]
        correlation = compare(harmonic_freq, audio_signal, fs)
        box_filter = np.ones(fs * 0.1)
        correlation_power = np.sqrt(signal.fftconvolve(np.abs(correlation) ** 2.0, box_filter, 'same'))
        # plt.plot(times, correlation, label='{} [Hz]'.format(harmonic_freq))
        # plt.plot(times[::100], correlation_power[::100], label='${}$ : {} [Hz]'.format(likely_note, harmonic_freq))
        present_harmonics[:, i] = correlation_power

    f, axes = plt.subplots(len(harmonics), 1, sharex=True)
    plt.title(note_name)
    for i in range(len(harmonics)):
        axes[i].plot(times, present_harmonics[:, i], label="{}".format(harmonics[i]))
        axes[i].set_ylim([0.0, 400e3])
        # min_power = 0.7 * np.max(present_harmonics[:, i - 1])
        # min_power = np.percentile(present_harmonics[:, i - 1], 70.0)
        # axes[i - 1].plot(times, present_harmonics[:, i - 1] > min_power, label="{}".format(i))


def correlate(harmonic_freq, audio_signal, fs):
    correlation = compare(harmonic_freq, audio_signal, fs)
    box_filter = np.ones(fs * 0.1)
    correlation_power = np.sqrt(signal.fftconvolve(np.abs(correlation) ** 2.0, box_filter, 'same'))
    return correlation_power


# def find_integer_contributors(freq):
    # for f in

def generate_harmonic_image(audio_signal, fs):
    powers = []
    note_freqs = sorted(notes.notes.values())

    # int(0.1 * fs)

    for freq in note_freqs:
        print "f: {} Hz".format(freq)
        correlation = correlate(freq, audio_signal, fs)

        powers.append(correlation[::10000])

    np_powers = np.array(powers)
    plt.imshow(np_powers)
    plt.show()


if __name__ == '__main__':
    # fn = "/home/jacob/repos/amanuensis/data/rocky_mtn_high.wav"
    # fn = "/home/jacob/repos/amanuensis/data/country_roads.wav"
    fn = "/home/jacob/repos/amanuensis/data/reference_guitar.wav"
    # fn = "/home/jacob/repos/amanuensis/data/tuning_reference.wav"

    fs, data = wavfile.read(fn)

    # start_seconds = 1.0
    # end_seconds = 15.0
    start_seconds = 0.0
    end_seconds = 70.0
    # end_seconds = 50.0
    start_samples = fs * start_seconds
    end_samples = fs * end_seconds

    segment_seconds = 0.1
    segment_size = fs * segment_seconds

    # first_chunk_chan0 = data[5000:50000, 0]
    # first_chunk_chan0 = data[start_samples:end_samples]
    first_chunk_chan0 = data[start_samples:end_samples, 0]
    # first_chunk_chan0 = data[:, 0]

    # wavfile.write('chunk.wav', fs, first_chunk_chan0)
    # exit(0)

    # f, t, Zxx = signal.stft(first_chunk_chan0, fs, nperseg=10000)
    # f, t, Zxx = signal.spectrogram(first_chunk_chan0, fs, nperseg=segment_size)

    # detect_harmonics(('E', 2), first_chunk_chan0, fs)
    # detect_harmonics(('A', 2), first_chunk_chan0, fs)
    # detect_harmonics(('D', 3), first_chunk_chan0, fs)
    # detect_harmonics(('G', 3), first_chunk_chan0, fs)
    # detect_harmonics(('B', 3), first_chunk_chan0, fs)
    # detect_harmonics(('E', 4), first_chunk_chan0, fs)
    generate_harmonic_image(first_chunk_chan0, fs)
    # plt.legend()
    # plt.show()

    # plt.figure('Octave 2')
    # comparogram(('E', 2), first_chunk_chan0, fs)
    # comparogram(('A', 2), first_chunk_chan0, fs)
    # comparogram(('D', 3), first_chunk_chan0, fs)
    # comparogram(('G', 3), first_chunk_chan0, fs)
    # comparogram(('B', 3), first_chunk_chan0, fs)
    # comparogram(('E', 4), first_chunk_chan0, fs)
    # plt.legend()
    # plt.show()

    # plt.pcolormesh(t, f, np.abs(Zxx))
    # plt.title('STFT Magnitude')
    # plt.ylabel('Frequency [Hz]')
    # plt.xlabel('Time [sec]')
    # plt.show()
