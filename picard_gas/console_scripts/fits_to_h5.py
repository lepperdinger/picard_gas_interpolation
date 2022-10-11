#!/usr/bin/env python
"""
Converts the 3D FITS files from https://zenodo.org/record/5501196 to H5 files.

Author: Stefan Lepperdinger
"""
from astropy.io import fits
from picard_gas.H5File import H5File
import numpy as np
import argparse
import sys


def read_fits_file(fits_file_path):
    try:
        with fits.open(fits_file_path) as header_data_unit_list:
            header = header_data_unit_list[0].header
            # x, y, and z limits of the volume represented by the grid
            grid_volume_limits = []
            # x, y, and z limits of the cell centers
            grid_cell_center_limits = []
            for coordinate in range(1, 4):  # 1, 2, 3 = x, y, z
                first_cell_center = header[f'CRVAL{coordinate}']
                cell_width = header[f'CDELT{coordinate}']
                lower_volume_limit = first_cell_center - cell_width/2
                assert lower_volume_limit < 0
                # I assume the distribution is centered at the Galactic Center
                upper_volume_limit = -lower_volume_limit
                upper_cell_center = upper_volume_limit - cell_width/2
                grid_volume_limits.append([
                    lower_volume_limit,
                    upper_volume_limit,
                ])
                grid_cell_center_limits.append([
                    first_cell_center,
                    upper_cell_center,
                ])
            grid_volume_limits = np.array(grid_volume_limits)
            grid_cell_center_limits = np.array(grid_cell_center_limits)
            data = header_data_unit_list[0].data
    except FileNotFoundError:
        print(f"File '{fits_file_path}' not found.", file=sys.stderr)
        sys.exit(1)

    return data, grid_volume_limits, grid_cell_center_limits


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
    density, grid_volume_limits, grid_cell_center_limits = read_fits_file(
        arguments.source_path
    )
    h5_file = H5File(arguments.destination_path, 'w')
    h5_file.write_density(density)
    h5_file.write_grid_limits(grid_volume_limits, grid_cell_center_limits)


if __name__ == '__main__':
    main()
