#!../venv/bin/python

import json
import os
import argparse
from os.path import isdir, join
from shutil import copyfile
import drivecasa
import simulate
import plot


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='BDA script runner.',
                                     epilog='')
    parser.add_argument('config', type=str, nargs='?', help='JSON config file.')
    args = parser.parse_args()
    if args.config is None:
        parser.print_usage()
        print "%s: error: too few arguments" % os.path.basename(__file__)
        exit(1)
    if not os.path.isfile(args.config):
        print "Error: Config file '%s' not found!" % args.config
        exit(1)

    try:
        settings = json.load(open(args.config))
    except ValueError as e:
        print 'ERROR: FAILED TO PARSE JSON CONFIG FILE!!'
        print e.message
        exit(1)

    # Spawn a CASA process to work with and put the config_file variable to
    # the CASA variable list.
    casa = drivecasa.Casapy(working_dir=os.path.curdir,
                            casa_logfile=False,
                            echo_to_stdout=True)
    casa.run_script(["config_file = '{}'".format(args.config)])

    # Top level simulation output directory.
    # TODO-BM use the filename of the settings file as the path?
    sim_dir = settings['path']

    # Create a copy of the settings file.
    if not os.path.isdir(sim_dir):
        os.makedirs(sim_dir)
    copyfile(args.config, join(sim_dir, args.config))

    # Simulation.
    simulate.run(settings)

    # Average.
    casa.run_script_from_file('average_ms.py')

    # Image.
    casa.run_script_from_file('image.py')

    # Plot results.
    plot.run(settings)

