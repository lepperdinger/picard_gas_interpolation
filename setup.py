import setuptools

src_directory = 'picard_gas'

console_scripts = [
    'fits_to_h5',
    'interpolate_gas',
    'plot_h5',
]

entry_points = {
    'console_scripts': [
        f'{console_script} = '
        f'{src_directory}.console_scripts.{console_script}:main'
        for console_script in console_scripts
    ]
}

setuptools.setup(
    name='picard_gas_interpolation',
    version='1.0.0',
    description='',
    author='Stefan Lepperdinger',
    author_email='lepperdinger.stefan@gmail.com',
    url='https://github.com/lepperdinger/picard_gas_interpolation',
    packages=setuptools.find_packages(),
    entry_points=entry_points,
    install_requires=[
        'astropy==5.1',
        'attrs==21.4.0',
        'cycler==0.11.0',
        'fonttools==4.34.4',
        'h5py==3.7.0',
        'iniconfig==1.1.1',
        'kiwisolver==1.4.4',
        'matplotlib==3.5.2',
        'numpy==1.23.1',
        'packaging==21.3',
        'pandas==1.4.3',
        'Pillow==9.2.0',
        'pluggy==1.0.0',
        'py==1.11.0',
        'pyerfa==2.0.0.1',
        'pyparsing==3.0.9',
        'PyQt5==5.15.7',
        'PyQt5-Qt5==5.15.2',
        'PyQt5-sip==12.11.0',
        'pytest==7.1.2',
        'python-dateutil==2.8.2',
        'pytz==2022.1',
        'PyYAML==6.0',
        'scipy==1.8.1',
        'six==1.16.0',
        'tomli==2.0.1',
    ],
    python_requires='>=3.8'
)
