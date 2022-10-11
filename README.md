PICARD Gas Interpolation
========================
Author: Stefan Lepperdinger

Software for projecting the Galactic HI and H2 gas distributions by Philipp Mertsch and Andrea Vittino onto the simulation grid of PICARD via trilinear interpolation.

### Installation

1. Clone the git repository:
```
git clone https://github.com/lepperdinger/picard_gas_interpolation
cd picard_gas_interpolation
```
3. Create a virtual environment:
```
virtualenv venv
```
2. Activate the virtual environment:
```
. venv/bin/activate
```
3. Install the software in the virtual environment:
```
pip install .
```

### Usage

1. Download the HI or H2 gas distribution `<gas type>_dens_mean_<gas flow model>.fits` from https://zenodo.org/record/5956696 or https://zenodo.org/record/5501196
2. Convert the gas distribution into the HDF5 format via the `fits_to_h5` command:
```
fits_to_h5 <source *.fits> <destination *.h5>
```
3. You can take a quick peek at the distribution via
```
plot_h5 -l <distribution *.h5>
```
H2 example:

![before_H2](https://user-images.githubusercontent.com/69904414/195127005-63d4eae4-4550-4a29-bd5c-818dc6b0de87.png)

HI example:

![before_HI](https://user-images.githubusercontent.com/69904414/195127183-aa770771-4820-4c5b-be75-54f28db954dc.png)

4. Project the gas onto the PICARD simulation grid via
```
interpolate_gas <source *.h5> <destination *.h5> <parameter *.nx>
```
5. You can again take a quick peek at the projected distribution via
```
plot_h5 -l <distribution *.h5>
```

H2 example:

![after_H2](https://user-images.githubusercontent.com/69904414/195127439-3a54f805-3b97-48fe-b4bf-1829b425ea9e.png)

HI example:

![after_HI](https://user-images.githubusercontent.com/69904414/195127578-de423658-eefd-4bd6-9c13-dc326c2bcaea.png)

### Tests

Command for running the tests:
```
pytest -v test
```