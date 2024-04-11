import numpy as np

a = np.arange(10)

def rolling_window(a, window, step_size):
  shape = a.shape[:-1] + (a.shape[-1] - window + 1 - step_size + 1, window)
  strides = a.strides + (a.strides[-1] * step_size,)
  return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

b = rolling_window(a, 3, 1)
print(b)