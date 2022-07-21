"""
For getting the final grid, i.e., the simulation grid from Picard. This grid
is specified in the Picard parameter file (*.nx).

Usage:
    parameters = parse_parameter_file(parameter_file_path)
    grid = get_final_grid(parameters)
"""
from picard_gas.parameter_file import ParameterFile
import sys
from typing import Dict
import numpy as np


def parse_parameter_file(parameter_file_path: str) -> dict:
    """
    Gets the necessary parameters from the parameter file.
    """
    parameter_file = ParameterFile(parameter_file_path)

    if parameter_file('no_section', 'n_spatial_dimensions', 0, int) != 3:
        print('Error: The value of the parameter n_spatial_dimensions in the '
              'parameter file is not 3.', file=sys.stderr)
        sys.exit(1)

    def parameter(parameter_name, type_):
        return parameter_file('Grid', parameter_name, 0, type_)

    parameters = {
        'x_min': parameter('x_min', float),
        'x_max': parameter('x_max', float),
        'n_xgrid': parameter('n_xgrid', int),

        'y_min': parameter('y_min', float),
        'y_max': parameter('y_max', float),
        'n_ygrid': parameter('n_ygrid', int),

        'z_min': parameter('z_min', float),
        'z_max': parameter('z_max', float),
        'n_zgrid': parameter('n_zgrid', int)
    }

    return parameters


def get_final_grid(parameters: dict) -> Dict[str, np.array]:
    grid: Dict[str, np.array] = dict()
    grid['x centers'] = np.linspace(parameters['x_min'],
                                    parameters['x_max'],
                                    parameters['n_xgrid'])
    grid['y centers'] = np.linspace(parameters['y_min'],
                                    parameters['y_max'],
                                    parameters['n_ygrid'])
    grid['z centers'] = np.linspace(parameters['z_min'],
                                    parameters['z_max'],
                                    parameters['n_zgrid'])
    grid['shape'] = np.array([parameters['n_xgrid'],
                              parameters['n_ygrid'],
                              parameters['n_zgrid']])
    grid['cell center limits'] = np.array([
        [parameters['x_min'], parameters['x_max']],
        [parameters['y_min'], parameters['y_max']],
        [parameters['z_min'], parameters['z_max']],
    ])
    grid_size = (grid['cell center limits'][:, 1] -
                 grid['cell center limits'][:, 0])
    cell_size = grid_size / (grid['shape'] - 1)
    lower_cell_center_limits = grid['cell center limits'][:, 0] - cell_size*0.5
    upper_cell_center_limits = grid['cell center limits'][:, 1] + cell_size*0.5
    grid['volume limits'] = np.vstack([lower_cell_center_limits,
                                       upper_cell_center_limits]).T
    return grid
