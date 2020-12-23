'''
Modified from librosa.  
YIN pitch detection.  
'''
import numpy as np
from librosa import util

def _cumulative_mean_normalized_difference(
  y, frame_length, win_length, min_period, max_period
):
  # Autocorrelation.
  a = np.fft.rfft(y, frame_length)
  b = np.fft.rfft(y[win_length::-1], frame_length)
  acf = np.fft.irfft(a * b, frame_length)[win_length:]
  acf[np.abs(acf) < 1e-6] = 0

  # Energy terms.
  energy = np.cumsum(y ** 2)
  energy = energy[win_length:] - energy[:-win_length]
  energy[np.abs(energy) < 1e-6] = 0

  # Difference function.
  yin_frame = energy[0] + energy - 2 * acf

  # Cumulative mean normalized difference function.
  yin_numerator = yin_frame[min_period : max_period + 1]
  tau_range = np.arange(1, max_period + 1)
  cumulative_mean = np.cumsum(yin_frame[1 : max_period + 1]) / tau_range
  yin_denominator = cumulative_mean[min_period - 1 : max_period]
  yin_frame = yin_numerator / (yin_denominator + util.tiny(yin_denominator))
  return yin_frame

def _parabolic_interpolation(y):
  parabolic_shifts = np.zeros_like(y)
  parabola_a = (y[:-2] + y[2:] - 2 * y[1:-1]) / 2
  parabola_b = (y[2:] - y[:-2]) / 2
  # pylint may incorrectly underline the below two lines. 
  parabolic_shifts[1:-1] = -parabola_b / (2 * parabola_a + util.tiny(parabola_a))
  parabolic_shifts[np.abs(parabolic_shifts) > 1] = 0
  return parabolic_shifts

def yin(
  y, sr, frame_length, fmin = 65, fmax = 1600, trough_threshold = 0.1, 
  win_length = None,
):
  if win_length is None:
      win_length = frame_length // 2
  min_period = max(int(np.floor(sr / fmax)), 1)
  max_period = min(int(np.ceil(sr / fmin)), frame_length - win_length - 1)
  
  yin_frame = _cumulative_mean_normalized_difference(
      y, frame_length, win_length, min_period, max_period
  )

  # Parabolic interpolation.
  parabolic_shifts = _parabolic_interpolation(yin_frame)

  # Find local minima.
  is_trough = util.localmin(yin_frame)
  is_trough[0] = yin_frame[0] < yin_frame[1]

  # Find minima below peak threshold.
  is_threshold_trough = np.logical_and(is_trough, yin_frame < trough_threshold)

  # Absolute threshold.
  # "The solution we propose is to set an absolute threshold and choose the
  # smallest value of tau that gives a minimum of d' deeper than
  # this threshold. If none is found, the global minimum is chosen instead."
  yin_period = np.argmax(is_threshold_trough)
  if np.all(~is_threshold_trough):
      yin_period = np.argmin(yin_frame)  # global_min

  # Refine peak by parabolic interpolation.
  yin_period = (
    min_period
    + yin_period
    + parabolic_shifts[yin_period]
  )

  # Convert period to fundamental frequency.
  f0 = sr / yin_period
  return f0
