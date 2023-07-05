import librosa
import numpy as np
import tensorflow as tf
tf.version


def framing_signal(signal):
    frame_length = int(0.04 * 22050)
    frame_shift = int(0.02 * 22050)
    # Calculate the total number of frames in the signal
    num_frames = int(np.ceil(len(signal) / frame_shift))
    # Pad the signal with zeros to ensure that there are enough samples
    # for the last frame
    pad_length = num_frames * frame_shift - len(signal)
    signal= np.pad(signal, (0, pad_length), 'constant', constant_values=0)
    # Use a sliding window to extract each frame
    frames = []
    for i in range(num_frames):
        start = i * frame_shift
        end = start + frame_length
        frame = signal[start:end]
        frames.append(frame)
    # Apply a window function to each frame to reduce spectral leakage
    window = np.hamming(num_frames)
    frames = np.array(frames)
    frames *= window
    return frames



def concatenate_and_apply_fft(frames):
  the_signal=[]
  for i in range(len(frames)):
    X = np.fft.fft(frames[i])
    magnitude_spectrum = np.abs(X)
    the_signal=np.concatenate((the_signal,magnitude_spectrum),axis=0)
  return the_signal



def extract_mell_spectogram(signalm):
  mel_specto=librosa.feature.melspectrogram(y=signalm,sr=22050)
  delta_mel_specto=librosa.feature.delta(mel_specto)
  delta2_mel_specto=librosa.feature.delta(delta_mel_specto,order=2)
  comrehensive_mel_specto=np.concatenate((mel_specto,delta_mel_specto,delta2_mel_specto))
  return comrehensive_mel_specto

