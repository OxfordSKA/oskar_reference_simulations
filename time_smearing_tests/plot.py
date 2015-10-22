# -*- coding: utf-8 -*-
"""Plot a summary of results from the BDA pipeline."""

import numpy
import os
from os.path import join
import matplotlib.pyplot as plt
import pyfits
import aplpy


def adjust_header(header):
    for i, k in enumerate(header):
        if not k or k == 'COMMENT':
            header.pop(k)
    return header


def get_hdu(file_name, flux_scale=1.0e3):
    data, header = pyfits.getdata(file_name, header=True)
    header = adjust_header(header)
    data *= flux_scale
    return pyfits.PrimaryHDU(data, header), data


def get_hdu_diff(file1, file2, flux_scale=1.0e3):
    d1, h1 = pyfits.getdata(file1, header=True)
    d2, h2 = pyfits.getdata(file2, header=True)
    h1 = adjust_header(h1)
    assert d1.shape == d2.shape
    d = d1 - d2
    d *= flux_scale
    return pyfits.PrimaryHDU(d, h1), d

def plot_model_bda(settings):
    sim_dir = settings['path']
    plotting = settings['plotting']
    stretch = 'linear'
    fig = plt.figure(figsize=(6.5, 10.0))
    subplot = (2, 1, 1)
    hdu, data = get_hdu(join(sim_dir, plotting['model']))
    cmin = data.min()
    cmax = data.max()
    f = aplpy.FITSFigure(hdu, figure=fig, subplot=subplot)
    f.add_label(0.05, 0.95, '(a)',
                relative=True,
                multialignment='center',
                fontsize=14,
                bbox=dict(color='white', alpha=0.75, edgecolor='white',
                          pad=5.0, linewidth=0.0))
    f.show_colorscale(vmin=cmin, vmax=cmax, stretch=stretch, cmap='afmhot')
    f.add_colorbar()
    f.colorbar.set_width(0.1)
    f.colorbar.set_axis_label_text(r'mJy / beam')
    f.colorbar.set_axis_label_font(size='small')
    f.tick_labels.set_font(size='small')
    f.axis_labels.set_font(size='small')
    f.set_yaxis_coord_type('scalar')
    f.set_xaxis_coord_type('scalar')
    f.tick_labels.set_yformat('%.3f')
    f.tick_labels.set_xformat('%.3f')
    f.add_grid()
    f.grid.set_color('white')
    f.grid.set_linestyle('--')
    f.grid.set_alpha(0.3)
    f.set_title('model', fontsize='small', weight='bold')

    subplot=(2, 1, 2)
    hdu, data = get_hdu_diff(join(sim_dir, plotting['model_bda']),
                             join(sim_dir, plotting['model']),
                             1.0e6)
    cmin = data.min()
    cmax = data.max()
    f = aplpy.FITSFigure(hdu, figure=fig, subplot=subplot)
    f.add_label(0.05, 0.95, '(b)',
                relative=True,
                multialignment='center',
                fontsize=14,
                bbox=dict(color='white', alpha=0.75, edgecolor='none',
                          pad=5.0, linewidth=0.0))
    f.show_colorscale(vmin=cmin, vmax=cmax, stretch=stretch, cmap='afmhot')
    f.add_colorbar()
    f.colorbar.set_width(0.1)
    f.colorbar.set_axis_label_text(r'$\mathrm{\mu}$Jy / beam')
    f.colorbar.set_axis_label_font(size='small')
    f.tick_labels.set_font(size='small')
    f.axis_labels.set_font(size='small')
    f.set_yaxis_coord_type('scalar')
    f.set_xaxis_coord_type('scalar')
    f.tick_labels.set_yformat('%.3f')
    f.tick_labels.set_xformat('%.3f')
    f.add_grid()
    f.grid.set_color('white')
    f.grid.set_linestyle('--')
    f.grid.set_alpha(0.3)
    f.set_title('bda model - model', fontsize='small', weight='bold')
    plt.savefig(join(sim_dir, 'test.png'), dpi=300)
    plt.show()

def plot_model(settings):
    sim_dir = settings['path']
    plotting = settings['plotting']
    stretch = 'linear'
    fig = plt.figure(figsize=(6.5, 5.0))
    hdu, data = get_hdu(join(sim_dir, plotting['model']))
    cmin = data.min()
    cmax = data.max()
    f = aplpy.FITSFigure(hdu, figure=fig)
    f.show_colorscale(vmin=cmin, vmax=cmax, stretch=stretch, cmap='afmhot')
    f.add_colorbar()
    f.colorbar.set_width(0.1)
    f.colorbar.set_axis_label_text(r'mJy / beam')
    f.colorbar.set_axis_label_font(size='small')
    f.tick_labels.set_font(size='x-small')
    f.axis_labels.set_font(size='x-small')
    # f.set_yaxis_coord_type('scalar')
    # f.set_xaxis_coord_type('scalar')
    # f.tick_labels.set_yformat('%.3f')
    # f.tick_labels.set_xformat('%.3f')
    f.add_grid()
    f.grid.set_color('white')
    f.grid.set_linestyle('--')
    f.grid.set_alpha(0.3)
    f.set_title('model', fontsize='small', weight='bold')
    plt.savefig(join(sim_dir, 'model.png'), dpi=300)


def plot_model_diff(settings):
    sim_dir = settings['path']
    plotting = settings['plotting']
    stretch = 'linear'
    fig = plt.figure(figsize=(13.0, 20.0))
    hdu, data = get_hdu_diff(join(sim_dir, plotting['model_1']),
                             join(sim_dir, plotting['model_1_ns']),
                             1.0e6)
    cmin = data.min()
    cmax = data.max()
    f = aplpy.FITSFigure(hdu, figure=fig, subplot=(4, 2, 1))
    f.show_colorscale(vmin=cmin, vmax=cmax, stretch=stretch, cmap='afmhot')
    f.add_colorbar()
    f.colorbar.set_width(0.1)
    f.colorbar.set_axis_label_text(r'$\mu$Jy / beam')
    f.colorbar.set_axis_label_font(size='small')
    f.tick_labels.set_font(size='x-small')
    f.axis_labels.set_font(size='x-small')
    f.add_grid()
    f.grid.set_color('white')
    f.grid.set_linestyle('--')
    f.grid.set_alpha(0.3)
    f.set_title('model_1 - model_1_ns', fontsize='small', weight='bold')
    ax = fig.add_subplot(422)
    ax.plot(data[0, 0, data.shape[2]/2, :], 'x-', markersize=2.0)
    ax.set_xlim(0, 512)
    ax.grid(True)

    hdu, data = get_hdu_diff(join(sim_dir, plotting['model_1']),
                             join(sim_dir, plotting['model_3_ave']),
                             1.0e6)
    cmin = data.min()
    cmax = data.max()
    f = aplpy.FITSFigure(hdu, figure=fig, subplot=(4, 2, 3))
    f.show_colorscale(vmin=cmin, vmax=cmax, stretch=stretch, cmap='afmhot')
    f.add_colorbar()
    f.colorbar.set_width(0.1)
    f.colorbar.set_axis_label_text(r'$\mu$Jy / beam')
    f.colorbar.set_axis_label_font(size='small')
    f.tick_labels.set_font(size='x-small')
    f.axis_labels.set_font(size='x-small')
    f.add_grid()
    f.grid.set_color('white')
    f.grid.set_linestyle('--')
    f.grid.set_alpha(0.3)
    f.set_title('model_1 - model_3_ave', fontsize='small', weight='bold')
    ax = fig.add_subplot(424)
    ax.plot(data[0, 0, data.shape[2]/2, :], 'x-', markersize=2.0)
    ax.set_xlim(0, 512)
    ax.grid(True)

    hdu, data = get_hdu_diff(join(sim_dir, plotting['model_1']),
                             join(sim_dir, plotting['model_3_ns_ave']),
                             1.0e6)
    cmin = data.min()
    cmax = data.max()
    f = aplpy.FITSFigure(hdu, figure=fig, subplot=(4, 2, 5))
    f.show_colorscale(vmin=cmin, vmax=cmax, stretch=stretch, cmap='afmhot')
    f.add_colorbar()
    f.colorbar.set_width(0.1)
    f.colorbar.set_axis_label_text(r'$\mu$Jy / beam')
    f.colorbar.set_axis_label_font(size='small')
    f.tick_labels.set_font(size='x-small')
    f.axis_labels.set_font(size='x-small')
    f.add_grid()
    f.grid.set_color('white')
    f.grid.set_linestyle('--')
    f.grid.set_alpha(0.3)
    f.set_title('model_1 - model_3_ns_ave', fontsize='small', weight='bold')
    ax = fig.add_subplot(426)
    ax.plot(data[0, 0, data.shape[2]/2, :], 'x-', markersize=2.0)
    ax.set_xlim(0, 512)
    ax.grid(True)

    hdu, data = get_hdu_diff(join(sim_dir, plotting['model_3_ave']),
                             join(sim_dir, plotting['model_3_ns_ave']),
                             1.0e6)
    cmin = data.min()
    cmax = data.max()
    f = aplpy.FITSFigure(hdu, figure=fig, subplot=(4, 2, 7))
    f.show_colorscale(vmin=cmin, vmax=cmax, stretch=stretch, cmap='afmhot')
    f.add_colorbar()
    f.colorbar.set_width(0.1)
    f.colorbar.set_axis_label_text(r'$\mu$Jy / beam')
    f.colorbar.set_axis_label_font(size='small')
    f.tick_labels.set_font(size='x-small')
    f.axis_labels.set_font(size='x-small')
    f.add_grid()
    f.grid.set_color('white')
    f.grid.set_linestyle('--')
    f.grid.set_alpha(0.3)
    f.set_title('model_3_ave - model_3_ns_ave', fontsize='small', weight='bold')
    ax = fig.add_subplot(428)
    ax.plot(data[0, 0, data.shape[2]/2, :], 'x-', markersize=2.0)
    ax.set_xlim(0, 512)
    ax.grid(True)


    plt.savefig(join(sim_dir, 'model_diff.png'), dpi=300)


def run(settings):
    # plot_model_bda(settings)
    plot_model(settings)
    plot_model_diff(settings)
