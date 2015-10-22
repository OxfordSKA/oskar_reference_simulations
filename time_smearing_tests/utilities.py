# -*- coding: utf-8 -*-
"""Module containing utility bda for BDA simulation steps."""

import numpy as np
import os
import shutil


def adev(data, dt, tau):
    """Evaluate the Allan deviation of a time series.

    Args:
        data (np.array): Time series data.
        dt (float): Time series data increment, in seconds.
        tau (float): Averaging period, in seconds.

    Returns:
        The allan deviation of the series and error on the deviation.
    """
    rate = 1. / dt
    m = int(rate * tau)
    # Truncate to an even multiple of this tau value
    freq = data[0:len(data) - int(np.remainder(len(data), m))]
    f = np.reshape(freq, (m, -1), order='F')
    fa = np.mean(f, 0)
    fd = np.diff(fa)
    n = len(fa) - 1
    sm = np.sqrt(0.5 / n * (np.sum(fd**2)))
    sme = sm / np.sqrt(n)
    return sm, sme, n


def fbm(n, hurst):
    """Generate Fractional brownian motion noise.

    http://www.maths.uq.edu.au/~kroese/ps/MCSpatial.pdf

    Args:
        n (int): Length of the time series.
        H (float): Hurst parameter.

    Kwargs:
        seed (int): Random generator number seed.

    Returns:
        Time series array.
    """
    r = np.empty((n + 1,)) * np.NaN
    r[0] = 1
    for k in range(1, n + 1):
        a = 2.0 * hurst
        r[k] = 0.5 * ((k + 1)**a - 2 * k**a + (k - 1)**a)
    r = np.append(r, r[-2:0:-1])  # first row of circulant matrix
    lambda_ = np.real(np.fft.fft(r)) / (2 * n)  # Eigenvalues
    W = np.fft.fft(np.sqrt(lambda_) * (np.random.randn(2 * n) +
                                       1j * np.random.randn(2 * n)))
    W = n**(-hurst) * np.cumsum(np.real(W[0:n + 1]))  # Rescale
    return W


def eval_gain_amp(length, tstep, hurst, adev_fbm, sigma_wn, tau):
    """."""
    g_fbm = fbm(length, hurst)
    g_fbm *= adev_fbm / adev(g_fbm, tstep, tau)[0]
    g_wn = np.random.randn(length + 1,) * sigma_wn
    return (g_fbm + g_wn) + 1.0


def eval_gain_phase(n, tstep, H, adev_fbm, sigma_wn, tau):
    """."""
    p_fbm = fbm(n, H)
    p_fbm *= adev_fbm / adev(p_fbm, tstep, tau)[0]
    p_wn = np.random.randn(n + 1,) * sigma_wn
    phase = p_fbm + p_wn  # Combine FBM and WN signals
    return phase


def eval_complex_gain(n, dt, amp_H, amp_adev_fbm, amp_sigma_wn,
                      phase_H, phase_adev_fbm, phase_sigma_wn,
                      amp_std_t0, phase_std_t0, tau):
    """."""
    amp = eval_gain_amp(n, dt, amp_H, amp_adev_fbm, amp_sigma_wn, tau)
    phase = eval_gain_phase(n, dt, phase_H, phase_adev_fbm, phase_sigma_wn,
                            tau) * np.pi / 180.0
    amp_t0 = np.random.randn() * amp_std_t0
    phase_t0 = np.random.randn() * phase_std_t0 * (np.pi / 180.)
    gain = (amp + amp_t0) * np.exp(1.0j * (phase + phase_t0))
    return gain[0:n]


def copytree(src, dst, symlinks=False, ignore=None):
    """Copy a directory tree."""
    shutil.copytree(src, dst, symlinks, ignore)
#    for item in os.listdir(src):
#        s = os.path.join(src, item)
#        d = os.path.join(dst, item)
#        print s, '->', d,
#        if os.path.isdir(s):
#            print 'shutil.copytree()...'
#            shutil.copytree(s, d, symlinks, ignore)
#        else:
#            print 'shutil.copy2()...'
#            shutil.copy2(s, d)


def byteify(input):
    """Convert unicode string."""
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
