#!/usr/bin/env python
"""
Converts the 3D FITS files from https://zenodo.org/record/5501196 to H5 files.

Author: Stefan Lepperdinger
"""
from astropy.io import fits
from picard_gas.H5File import H5File
from picard_gas.initial_grid import GRID_VOLUME_LIMITS
from picard_gas.initial_grid import GRID_CELL_CENTER_LIMITS
from picard_gas.initial_grid import GRID_SHAPE
import numpy as np
import argparse
import sys


def read_fits_file(fits_file_path):
    try:
        with fits.open(fits_file_path) as header_data_unit_list:
            data = header_data_unit_list[0].data
    except FileNotFoundError:
        print(f"File '{fits_file_path}' not found.", file=sys.stderr)
        sys.exit(1)

    assert np.all(data.shape == GRID_SHAPE), 'invalid grid shape'

    return data


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Converts the 3D FITS files from '
                    'https://zenodo.org/record/5501196 to H5 files.',
    )

    parser.add_argument(metavar='<source *.fits>',
                        dest='source_path',
                        help='path of the fits file')

    parser.add_argument(metavar='<destination *.h5>',
                        dest='destination_path',
                        help='path of the H5 file')

    arguments = parser.parse_args()

    return arguments


def main():
    arguments = parse_arguments()
    density = read_fits_file(arguments.source_path)
    h5_file = H5File(arguments.destination_path, 'w')
    h5_file.write_density(density)
    h5_file.write_grid_limits(GRID_VOLUME_LIMITS, GRID_CELL_CENTER_LIMITS)


if __name__ == '__main__':
    main()
