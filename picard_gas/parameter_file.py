"""
A class for parsing Picard parameter files *.nx

Author: Stefan Lepperdinger
"""
import sys


class ParameterFile:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.parameters = dict()
        self.parse_file()

    def parse_file(self) -> None:
        """
        Parses the parameter file.
        """
        with open(self.file_path) as file:
            current_section = 'no_section'
            self.parameters[current_section] = dict()
            for line in file:
                line = line.strip()
                if len(line) == 0:
                    continue
                elif line.startswith('#'):
                    continue
                elif line.startswith('['):
                    section = line.replace('[', '')
                    section = section.replace(']', '')
                    section = section.strip()
                    current_section = section
                    self.parameters[section] = dict()
                else:
                    split_line = line.split('=')
                    parameter = split_line[0].strip()
                    values = split_line[1].split()
                    self.parameters[current_section][parameter] = values

    def __call__(self,
                 section: str,
                 parameter: str,
                 value_index: int,
                 type_=None):
        """
        Parameters
        ----------
            section     : section, e.g., 'Grid'
            parameter   : parameter, e.g., 'z_min'
            value_index : index of the values of the parameters, e.g., 0 is the
                          index of the first value after the equal sign in the
                          parameter file
            type_       : type into which the parameter should be converted

        Returns
        -------
            parameter value
        """
        try:
            parameter = self.parameters[section][parameter][value_index]
        except KeyError:
            print(f"Error: Couldn't find the value with the index "
                  f"{value_index} of the parameter '{parameter}' in the "
                  f"section '{section}' in the parameter file.",
                  file=sys.stderr)
            sys.exit(1)
        if type_ is None:
            return parameter
        else:
            return type_(parameter)
