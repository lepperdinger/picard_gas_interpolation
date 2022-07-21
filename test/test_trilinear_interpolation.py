import pytest
import numpy as np
from picard_gas.trilinear_interpolation import TrilinearInterpolation
from picard_gas.final_grid import get_final_grid
from typing import Dict
from typing import List


def continuous_linear_scalar_field(x: float, y: float, z: float) -> float:
    c0 = -3.42
    cx = 0.435
    cy = 3.21
    cz = -.3
    return c0 + cx * x + cy * y + cz * z


def get_discrete_linear_scalar_field(grid: Dict[str, np.array]) -> np.array:
    discrete_field = np.zeros(grid['shape'])
    for x_index, x in enumerate(grid['x centers']):
        for y_index, y in enumerate(grid['y centers']):
            for z_index, z in enumerate(grid['z centers']):
                value = continuous_linear_scalar_field(x, y, z)
                discrete_field[x_index][y_index][z_index] = value
    return discrete_field


parameters = {
    'x_min': -44.31,
    'x_max': 20.1,
    'n_xgrid': 9,

    'y_min': -35.9,
    'y_max': 11.07,
    'n_ygrid': 19,

    'z_min': -29.92,
    'z_max': 35.84,
    'n_zgrid': 25,
}
grid = get_final_grid(parameters)
discrete_linear_scalar_field = get_discrete_linear_scalar_field(grid)
interpolation = TrilinearInterpolation(discrete_linear_scalar_field,
                                       grid['volume limits'])
test_tolerance = 1e-10


@pytest.mark.parametrize(
    ['xyz_location'],
    (
        [[19.32, -5.32, 19.37]],
        [[-13.74, -9.82, 1.12]],
        [[-16.74, -29.7, 11.68]],
        [[-39.32, -24.28, 31.94]],
    )
)
def test_evaluate_evenness(xyz_location: List[float]):
    expected = continuous_linear_scalar_field(*xyz_location)
    result = interpolation(*xyz_location)
    deviation = abs(expected - result)
    assert deviation < test_tolerance
