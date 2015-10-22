# -*- coding: utf-8 -*-

import numpy
import os
from os.path import join
import shutil
import time
import sys
import math
import json
from bda import utilities
import matplotlib.pyplot as plt


def get_num_antennas(ms):
    """."""
    tb.open(ms + '/ANTENNA', nomodify=True)
    num_stations = tb.nrows()
    tb.close()
    return num_stations


if __name__ == "__main__":
    """ Copy the ref ms and populate it with averaged input ms.

    'average_group_name' is made available to the global namespace by the
                         run script.
    """
    settings = utilities.byteify(json.load(open(config_file)))
    sim_dir = settings['path']
    ms_ref = join(sim_dir, settings[average_group_name]['ref_ms'])
    ms_in = join(sim_dir, settings[average_group_name]['input_ms'])
    ms_out = join(sim_dir, settings[average_group_name]['output_ms'])

    num_antennas = get_num_antennas(ms_ref)
    num_baselines = num_antennas * (num_antennas - 1) / 2

    # Make a copy of the reference MS.
    if os.path.exists(ms_out):
        shutil.rmtree(ms_out)
    shutil.copytree(ms_ref, ms_out)

    fig = plt.figure(figsize=(6.5, 10.0))

    # TODO average the amplitudes of the input ms
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

    # Assume single, channel, scalar MS.
    assert col_data.shape[0] == 1
    assert col_data.shape[1] == 1
    assert col_data.shape[2] == num_rows
    data = numpy.squeeze(col_data)
    data = data.reshape(num_times, num_baselines)
    ave_data = numpy.mean(data, axis=0)

    tb.close()

    ave_uvdist = numpy.sqrt(ave_uu**2 + ave_vv**2)

    # ax.plot(ave_uvdist, ave_data, '.', markersize=2.0)


    print '-------------------'
    tb.open(ms_ref, nomodify=True)
    print tb.nrows()
    col_data = tb.getcol('DATA')
    col_uvw = tb.getcol('UVW')
    col_ant1 = tb.getcol('ANTENNA1')
    col_ant2 = tb.getcol('ANTENNA2')
    col_time = tb.getcol('TIME')
    uvdist = numpy.sqrt(col_uvw[0, :]**2 + col_uvw[1, :]**2)
    data = numpy.squeeze(col_data)
    # ax.plot(uvdist, data, 'x', markersize=3.0, markeredgecolor='r')
    ax = fig.add_subplot(211)
    ax.plot(uvdist / 1.e3, numpy.real(data),
            '.', markersize=2.0)
    ax.set_xlabel('uu-vv distance [km]')
    ax.set_ylabel('real(data)')

    ax = fig.add_subplot(212)
    ax.plot(ave_uvdist / 1.e3, numpy.real(data-ave_data),
            '.', markersize=2.0)
    ax.set_xlabel('uu-vv distance [km]')
    ax.set_ylabel('real(data - ave_data)')
    ax.get_yaxis().get_major_formatter().set_powerlimits((0, 0))
    tb.close()

    plt.savefig(join(sim_dir, settings[average_group_name]['plot_name']),
                dpi=600)

    tb.open(ms_out, nomodify=False)
    col_data = tb.getcol('DATA')
    print col_data[0, 0, 0]
    tb.putcol('DATA', numpy.reshape(ave_data, col_data.shape))
    col_data = tb.getcol('DATA')
    print col_data[0, 0, 0]
    tb.close()
