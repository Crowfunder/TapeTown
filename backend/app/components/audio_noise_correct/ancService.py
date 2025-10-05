import io
from math import gcd
from typing import Tuple

import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly

DEFAULT_TARGET_FS = 8000
DEFAULT_M = 32
DEFAULT_MU = 5e-4

def _read_wav_float_from_bytes(b: bytes) -> Tuple[int, np.ndarray]:
    bio = io.BytesIO(b)
    fs, data = wavfile.read(bio)

    # konwersja do float [-1, 1]
    if data.dtype == np.int16:
        x = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        x = data.astype(np.float32) / 2147483648.0
    elif data.dtype == np.uint8:
        x = (data.astype(np.float32) - 128.0) / 128.0
    else:
        x = data.astype(np.float32)
        m = float(np.max(np.abs(x)) + 1e-12)
        if m > 1.0:
            x /= m

    # stereo -> mono (średnia)
    if x.ndim == 2 and x.shape[1] > 1:
        x = x.mean(axis=1)

    return fs, x


def _write_wav_int16_to_bytes(fs: int, x: np.ndarray) -> bytes:
    """Zapisz float [-1,1] do WAV (int16) i zwróć jako bajty."""
    y = np.copy(x).astype(np.float32)
    m = float(np.max(np.abs(y)) + 1e-12)
    if m > 0.999:
        y = y / m * 0.999
    y16 = np.clip(y, -1.0, 1.0)
    y16 = (y16 * 32767.0).astype(np.int16)

    bio = io.BytesIO()
    wavfile.write(bio, fs, y16)
    bio.seek(0)
    return bio.read()

def _lms_predictor(signal_in: np.ndarray, M: int, mu: float, return_mode: str = "y"):

    d = signal_in.astype(np.float64, copy=False)
    N = len(d)
    h = np.zeros(M, dtype=np.float64)
    bx = np.zeros(M, dtype=np.float64)
    y = np.zeros(N, dtype=np.float64)

    for n in range(N):
        # wektor opóźnień: [d[n-1], d[n-2], ..., d[n-M]]
        bx[1:] = bx[:-1]
        bx[0] = d[n-1] if n > 0 else d[0]
        y[n] = np.dot(h, bx)
        e = d[n] - y[n]
        h += mu * e * bx

    if (return_mode or "y").lower() == "e":
        out = d - y
    else:
        out = y
    return out.astype(np.float32), h.astype(np.float32)

def denoise_lms_wav_bytes(
    wav_bytes: bytes,
    target_fs: int = DEFAULT_TARGET_FS,
    M: int = DEFAULT_M,
    mu: float = DEFAULT_MU,
    mode: str = "y",
) -> Tuple[bytes, int]:

    fs_in, x = _read_wav_float_from_bytes(wav_bytes)

    # (opcjonalnie) resampling do target_fs
    fs_out = fs_in
    x_proc = x
    if fs_in != target_fs:
        up, down = target_fs, fs_in
        g = gcd(up, down)
        up //= g
        down //= g
        x_proc = resample_poly(x, up, down).astype(np.float32)
        fs_out = target_fs

    # LMS
    out, _ = _lms_predictor(x_proc, M=M, mu=mu, return_mode=mode)

    # zapis do WAV (bajty)
    wav_out = _write_wav_int16_to_bytes(fs_out, out)
    return wav_out, fs_out
