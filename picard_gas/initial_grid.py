"""
Specifies the initial grid, i.e., the grid of the numerical gas densities
from https://zenodo.org/record/5501196.
"""
import numpy as np

# x, y, and z limits of the volume represented by the grid
GRID_VOLUME_LIMITS = np.array([[-16, 16], [-16, 16], [-0.5, 0.5]])  # kpc

# x, y, and z limits of the cell centers
GRID_CELL_CENTER_LIMITS = np.array([[-15.96875, 15.96875],
                                    [-15.96875, 15.96875],
                                    [-0.46875, 0.46875]])  # kpc

# side length of a cell (Δx = Δy = Δz)
CELL_SIZE = 1. / 16.  # kpc

GRID_SHAPE = np.array([512, 512, 16])
