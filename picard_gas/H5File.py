"""
Module for reading and writing to H5 files.

Author: Stefan Lepperdinger
"""
from h5py import File
import numpy as np
import os
import sys

DENSITY_DATASET_NAME = 'gas_density'


class H5File:
    def __init__(self, file_path: str, access_mode: str = 'r'):
        self.file = None
        access_modes = 'r', 'w'
        if access_mode not in access_modes:
            raise ValueError('Invalid access mode.')
        if access_mode == 'w' and os.path.exists(file_path):
            print(f'error: The file "{file_path}" already exists.',
                  file=sys.stderr)
            sys.exit(1)
        if access_mode == 'r' and not os.path.exists(file_path):
            print(f'error: The file "{file_path}" does not exist.')
            sys.exit(1)
        self.file = File(file_path, mode=access_mode)

    def __del__(self):
        if self.file is not None:
            self.file.close()

    def read_density(self) -> np.ndarray:
        density = np.array(self.file[DENSITY_DATASET_NAME], dtype=np.float64)
        return density

    def read_grid_volume_limits(self) -> np.ndarray:
        limits = np.array(self.file['grid volume limits'], dtype=np.float64)
        return limits

    def read_grid_cell_center_limits(self) -> np.ndarray:
        limits = np.array(self.file['grid cell center limits'],
                          dtype=np.float64)
        return limits

    def _write_data(self,
                    name: str,
                    data: np.ndarray,
                    unit: str,
                    description: str) -> None:
        self.file.create_dataset(name, data=data)
        self.file[name].attrs.create('unit', unit)
        self.file[name].attrs.create('description', description)

    def write_density(self, density: np.ndarray) -> None:
        self._write_data(
            name=DENSITY_DATASET_NAME,
            data=density,
            unit='cm^-3',
            description='particle density of the gas',
        )

    def write_grid_limits(self,
                          grid_volume_limits: np.ndarray,
                          grid_cell_center_limits: np.ndarray) -> None:
        self._write_data(
            name='grid volume limits',
            data=grid_volume_limits,
            unit='kpc',
            description='x, y, and z limits of the volume represented by the '
                        'grid',
        )
        self._write_data(
            name='grid cell center limits',
            data=grid_cell_center_limits,
            unit='kpc',
            description='x, y, and z limits of the cell centers'
        )
