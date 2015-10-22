# -*- coding: utf-8 -*-

import numpy
import os
from os.path import join
import shutil
import time
import sys
import math
import json
import utilities
import matplotlib.pyplot as plt


def get_num_antennas(ms):
    """."""
    tb.open(ms + '/ANTENNA', nomodify=True)
    num_stations = tb.nrows()
    tb.close()
    return num_stations


def average_ms(ms_ref, ms_in, ms_out, overwrite=True):
    if not overwrite and os.path.isdir(ms_out):
        return
    # Create output MS by making a copy of the reference MS.
    if os.path.exists(ms_out):
        shutil.rmtree(ms_out)
    print 'Averaging MS:', ms_in
    shutil.copytree(ms_ref, ms_out)
    tb.open(ms_in, nomodify=True)
    num_rows = tb.nrows()
    num_times = num_rows / num_baselines
    col_data = tb.getcol('DATA')
    col_uvw = tb.getcol('UVW')
    col_ant1 = tb.getcol('ANTENNA1')
    col_ant2 = tb.getcol('ANTENNA2')
    col_time = tb.getcol('TIME')
    uu = col_uvw[0, :]
    uu = uu.reshape(num_times, num_baselines)
    ave_uu = numpy.mean(uu, axis=0)
    vv = col_uvw[1, :]
    vv = vv.reshape(num_times, num_baselines)
    ave_vv = numpy.mean(vv, axis=0)
    ww = col_uvw[2, :]
    ww = ww.reshape(num_times, num_baselines)
    ave_ww = numpy.mean(ww, axis=0)
    t = col_time
    t = t.reshape(num_times, num_baselines)
    ave_t = numpy.mean(t, axis=0)
    # Assert that the MS has 1 channel and is stokes-I only.
    assert col_data.shape[0] == 1
    assert col_data.shape[1] == 1
    assert col_data.shape[2] == num_rows
    data = numpy.squeeze(col_data)
    data = data.reshape(num_times, num_baselines)
    ave_data = numpy.mean(data, axis=0)
    tb.close()
    tb.open(ms_out, nomodify=False)
    col_data = tb.getcol('DATA')
    tb.putcol('DATA', numpy.reshape(ave_data, col_data.shape))
    col_data = tb.getcol('DATA')
    tb.close()


if __name__ == "__main__":
    """Copy the ref ms and populate it with averaged input ms."""
    settings = utilities.byteify(json.load(open(config_file)))
    sim_dir = settings['path']
    ms_ref = join(sim_dir, 'n0001.ms')
    num_antennas = get_num_antennas(ms_ref)
    num_baselines = num_antennas * (num_antennas - 1) / 2

    for n in settings['sim']['observation']['num_times']:
        if n == 1:
            continue

        # === No smearing ===
        ms_in = join(sim_dir, 'n%04i.ms' % n)
        ms_out = join(sim_dir, 'ave_n%04i.ms' % n)
        average_ms(ms_ref, ms_in, ms_out, overwrite=False)

        # === With analytical smearing ===
        ms_in = join(sim_dir, 'n%04i_smearing.ms' % n)
        ms_out = join(sim_dir, 'ave_n%04i_smearing.ms' % n)
        average_ms(ms_ref, ms_in, ms_out, overwrite=False)
