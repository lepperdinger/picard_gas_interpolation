#!/usr/bin/env python
"""
Shows an X-Y plot of a gas density.

Author: Stefan Lepperdinger
"""
from picard_gas.H5File import H5File
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import colors
import argparse
import numpy as np
import sys


def plot(arguments: argparse.Namespace):
    """
    Shows an X-Y plot of the gas density.
    """
    file = H5File(arguments.h5_file_path, 'r')
    density = file.read_density()
    grid_volume_limits = file.read_grid_volume_limits()
    print('Shape of the density:', density.shape)
    z_index = (arguments.z_index if arguments.z_index is not None
               else density.shape[2] // 2)
    image = density[:, :, z_index]
    norm = colors.LogNorm() if arguments.logarithmic else None
    color_map = cm.get_cmap('magma')
    color_map.set_bad('black')
    image = plt.imshow(image.T,
                       cmap=color_map,
                       norm=norm,
                       extent=np.concatenate(grid_volume_limits[:2]),
                       origin='lower')
    plt.colorbar(image, location='bottom', label='density / (1 / cm$^3$)')
    plt.clim(arguments.lower_limit, arguments.upper_limit)
    plt.xlabel('x / kpc')
    plt.ylabel('y / kpc')
    plt.title(f'z index = {z_index}')
    plt.show()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Shows an X-Y gas density plot.',
    )
    parser.add_argument(metavar='<file .*h5>',
                        dest='h5_file_path',
                        help='h5 file')

    parser.add_argument('-z',
                        metavar='<z index>',
                        dest='z_index',
                        type=int,
                        help='z index (default = max_z_index // 2)')

    parser.add_argument('-L',
                        metavar='<lower limit>',
                        dest='lower_limit',
                        type=float,
                        help='lower density limit / cm^-3')

    parser.add_argument('-U',
                        metavar='<upper limit>',
                        dest='upper_limit',
                        type=float,
                        help='upper density limit / cm^-3')

    parser.add_argument('-l', '--logarithmic',
                        action='store_true',
                        help='logarithmic')

    parsed_arguments = parser.parse_args()

    def sign_check(value, argument_name):
        is_negative = value is not None and value < 0
        if is_negative:
            print(f'{argument_name} has to be positive.', file=sys.stderr)
            sys.exit(1)

    sign_check(parsed_arguments.z_index, 'The z index')
    sign_check(parsed_arguments.lower_limit, 'The lower limit')
    sign_check(parsed_arguments.upper_limit, 'The upper limit')

    return parsed_arguments


def main():
    arguments = parse_arguments()
    plot(arguments)


if __name__ == '__main__':
    main()
