"""
A class for trilinear interpolation

Author: Stefan Lepperdinger
"""
import numpy as np


class PointNotWithinGrid(ValueError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class TrilinearInterpolation:
    def __init__(self, scalar_field: np.ndarray, volume_limits: np.ndarray):
        """
        Parameters
        ----------
            scalar_field  : 3D scalar field:
                            scalar_field[x_index, y_index, z_index]
            volume_limits : size of the volume:
                            volume_limits = numpy.array([[x_min, x_max],
                                                         [y_min, y_max)],
                                                         [z_min, z_max]])
                            (x_min, x_max, ... are the positions at the outer
                             boundaries of the cells and not the positions at
                             the cell centers.)
        """
        self.scalar_field = scalar_field
        self.volume_limits = volume_limits
        self.volume_size = volume_limits[:, 1] - volume_limits[:, 0]
        self.cell_size = self.volume_size / scalar_field.shape

    def __call__(self,
                 x_location: float,
                 y_location: float,
                 z_location: float) -> float:
        """
        Determines the value of the scalar filed at (x_location, y_location,
        z_location) via trilinear interpolation. Raises PointNotWithinGrid if
        the location is not within the grid and, therefore, interpolation isn't
        possible.
        """
        location = np.array([x_location, y_location, z_location])

        float_index = ((location - self.volume_limits[:, 0])/self.cell_size
                       - 0.5)
        cell_index = np.floor(float_index).astype(int)

        minimum_index = np.zeros(3)
        maximum_index = np.array(self.scalar_field.shape) - 2
        if (np.any(cell_index < minimum_index)
                or np.any(cell_index > maximum_index)):
            raise PointNotWithinGrid('Interpolation is not possible because '
                                     'the point is not within the grid.')

        # position inside cell
        # (3 floating-point numbers within the interval [0, 1))
        position_inside_cell = float_index - cell_index

        field = self.scalar_field
        x_i, y_i, z_i = cell_index
        x_p, y_p, z_p = position_inside_cell
        # see http://paulbourke.net/miscellaneous/interpolation/
        scalar = (
            field[x_i, y_i, z_i] * (1-x_p) * (1-y_p) * (1-z_p)    # 000
            + field[x_i + 1, y_i, z_i] * x_p * (1-y_p) * (1-z_p)  # 100
            + field[x_i, y_i + 1, z_i] * (1-x_p) * y_p * (1-z_p)  # 010
            + field[x_i, y_i, z_i + 1] * (1-x_p) * (1-y_p) * z_p  # 001
            + field[x_i + 1, y_i, z_i + 1] * x_p * (1-y_p) * z_p  # 101
            + field[x_i, y_i + 1, z_i + 1] * (1-x_p) * y_p * z_p  # 011
            + field[x_i + 1, y_i + 1, z_i] * x_p * y_p * (1-z_p)  # 110
            + field[x_i + 1, y_i + 1, z_i + 1] * x_p * y_p * z_p  # 111
        )
        return scalar
