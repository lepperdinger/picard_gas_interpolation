#!/usr/bin/env python
"""
Projects the numerical distribution onto the grid specified by the Picard
parameter file. It evaluates the gas densities at the grid points of the Picard
simulation via trilinear interpolation.

Author: Stefan Lepperdinger
"""
from picard_gas.trilinear_interpolation import TrilinearInterpolation
from picard_gas.trilinear_interpolation import PointNotWithinGrid
from picard_gas.H5File import H5File
from picard_gas.final_grid import get_final_grid
from picard_gas.final_grid import parse_parameter_file
import sys
import argparse
import numpy as np
import os
from typing import Dict


def interpolate(distribution: np.ndarray,
                grid_volume_limits: np.ndarray,
                picard_grid: Dict[str, np.ndarray]) -> np.ndarray:
    interpolation = TrilinearInterpolation(distribution, grid_volume_limits)

    x_centers = picard_grid['x centers']
    y_centers = picard_grid['y centers']
    z_centers = picard_grid['z centers']
    grid_shape = picard_grid['shape']
    converted_distribution = np.zeros(shape=grid_shape)

    for x_index, x_center in enumerate(x_centers):
        percent = round(x_index / (len(x_centers) - 1) * 100)
        print(f'{percent} %', end='\r', flush=True)
        for y_index, y_center in enumerate(y_centers):
            for z_index, z_center in enumerate(z_centers):
                try:
                    density = interpolation(x_center, y_center, z_center)
                except PointNotWithinGrid:
                    density = 0.
                converted_distribution[x_index, y_index, z_index] = density
    print(flush=True)
    return converted_distribution


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Projects the numerical distribution onto the grid '
                    'specified by the Picard parameter file.',
    )

    parser.add_argument(metavar='<source *.h5>',
                        dest='source_file_path',
                        help='H5 file file that contains the gas distribution '
                             'that should be interpolated at the simulation '
                             'grid points')

    parser.add_argument(metavar='<destination *.h5>',
                        dest='destination_file_path',
                        help='H5 file into which the interpolated gas '
                             'distribution should be saved')

    parser.add_argument(metavar='<parameter *.nx>',
                        dest='parameter_file_path',
                        help='Picard parameter file')

    parsed_arguments = parser.parse_args()

    destination = parsed_arguments.destination_file_path
    if os.path.exists(destination):
        print(f"Error: The file '{destination}' already exists.",
              file=sys.stderr)
        sys.exit(1)

    return parsed_arguments


def main():
    arguments = parse_arguments()

    source_file = H5File(arguments.source_file_path, 'r')
    destination_file = H5File(arguments.destination_file_path, 'w')

    parameters = parse_parameter_file(arguments.parameter_file_path)
    final_grid = get_final_grid(parameters)
    density = source_file.read_density()
    grid_volume_limits = source_file.read_grid_volume_limits()
    interpolated_density = interpolate(density, grid_volume_limits, final_grid)

    destination_file.write_density(interpolated_density)
    destination_file.write_grid_limits(final_grid['volume limits'],
                                       final_grid['cell center limits'])


if __name__ == '__main__':
    main()
