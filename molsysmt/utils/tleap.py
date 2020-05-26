#######################################################################################
### This code was developed by Andrea Rizzi  and John Chodera for the Yank project at
### John Chodera's lab. See: Yank/utils.py at https://github.com/choderalab/yank
###
### This file is at the moment an attempt to include some other functionalities
### and slight modifications just refactoring the original algorithms
###
### All credit should be given to Andrea Rizzi, John Chodera and the developers
### of Yank (https://github.com/choderalab/yank)
#######################################################################################

import os
import functools
import tempfile
import shutil
import subprocess
import re
from simtk import unit


def _sanitize_tleap_unit_name(func):
    """Decorator version of TLeap._sanitize_unit_name.
    This takes as unit name a keyword argument called "unit_name" or the
    second sequential argument (skipping self).
    """
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            kwargs['unit_name'] = TLeap._sanitize_unit_name(kwargs['unit_name'])
        except KeyError:
            # Tuples are immutable so we need to use concatenation.
            args = args[:1] + (TLeap._sanitize_unit_name(args[1]), ) + args[2:]
        func(*args, **kwargs)
    return _wrapper


class TLeap:
    """
    Programmatic interface to write and run AmberTools' ``tLEaP`` scripts.
    To avoid problems with special characters in file paths, the class run the
    tleap script in a temporary folder with hardcoded names for files and then
    copy the output files in their respective folders.
    Attributes
    ----------
    script
    """

    @property
    def script(self):
        """
        Complete and return the finalized script string
        Adds a ``quit`` command to the end of the script.
        """
        return self._script + '\nquit\n'

    def __init__(self):
        self._script = ''
        self._input_file_paths = {}  # paths of input files to copy in temp dir
        self._output_file_paths = {}  # paths of output files to copy from temp dir
        self._loaded_parameters = set()  # parameter files already loaded

    def add_commands(self, *args):
        """
        Append commands to the script
        Parameters
        ----------
        args : iterable of strings
            Individual commands to add to the script written in full as strings.
            Newline characters are added after each command
        """
        for command in args:
            self._script += command + '\n'

    def load_parameters(self, *args):
        """
        Load the LEaP parameters into the working TLEaP script if not already loaded
        This adds to the script
        Uses ``loadAmberParams`` for ``frcmod.*`` files
        Uses ``loadOff`` for ``*.off`` and ``*.lib`` files
        Uses ``source`` for other files.
        Parameters
        ----------
        args : iterable of strings
            File names for each type of leap file that can be loaded.
            Method to load them is automatically determined from file extension or base name
        """
        for par_file in args:
            # Check that this is not already loaded
            if par_file in self._loaded_parameters:
                continue

            # Check whether this is a user file or a tleap file, and
            # update list of input files to copy in temporary folder before run
            if os.path.isfile(par_file):
                local_name = par_file
                self._input_file_paths[local_name] = par_file
            else:  # tleap file
                local_name = par_file

            # use loadAmberParams if this is a frcmod file and source otherwise
            base_name = os.path.basename(par_file)
            extension = os.path.splitext(base_name)[1]
            if 'frcmod' in base_name or extension == '.dat':
                self.add_commands('loadAmberParams ' + local_name)
            elif extension == '.off' or extension == '.lib':
                self.add_commands('loadOff ' + local_name)
            else:
                self.add_commands('source ' + local_name)

            # Update loaded parameters cache
            self._loaded_parameters.add(par_file)

    def set_global_parameter(self, **kwargs):

        """
        Set global parameter value with command 'set default'.
        See the Amber manual: 'set' subsection of section 'Commands' in Leap chapter.
        Parameters
        ----------
        OldPrmtopFormat : str
            "on" or "off" (default) to write the prmtop file in Amber 6 and earlier format
        Dielectric : str
            "constant" or "distance" (default) for constant or distance dependent dielectric
        PdbWriteCharges: str
            "on" or "off" (default) to write withe savePDB the atom charges in the B-factors
            columnt
        PBRadii: str
            "bondi", "mbondi" (default), "mbondi2", "mbondi3" or "amber6" to choose the set of atomic radii
            for generalized Born or Poisson-Boltzmann calculations.
        nocenter: str
            "on" or "off" (default) to deactivate recentering coordinates.
        reorder_residues: str
            "on" (default) or "off" to place non-solvent residues before sovent residues
        """

        accepted_kwargs={'OldPrmtopFormat': ['on', 'off'],
                         'Dielectric': ['constant','distance'],
                         'PdbWriteCharges': ['on', 'off'],
                         'PBRadii': ['bondi', 'mbondi', 'mbondi2', 'mbondi3', 'amber6'],
                         'nocenter': ['on', 'off'],
                         'reorder_residues': ['on', 'off']}

        for parameter, value in kwargs.items():

            if parameter not in accepted_kwargs:
                raise ValueError("Parameter not recognized")
            if value not in accepted_kwargs[parameter]:
                raise ValueError("Value for parameter {} not recognized".format(value))

            self.add_commands('set default {} {}'.format(parameter, value))


    @_sanitize_tleap_unit_name
    def load_unit(self, unit_name, file_path):
        """
        Load a Unit into LEaP, this is typically a molecule or small complex.
        This adds to the script
        Accepts ``*.mol2`` or ``*.pdb`` files
        Parameters
        ----------
        unit_name : str
            Name of the unit as it should be represented in LEaP
        file_path : str
            Full file path with extension of the file to read into LEaP as a new unit
        """

        file_name = os.path.basename(file_path)
        file_name, extension = os.path.splitext(file_name)
        local_name = file_name+extension


        if extension == '.mol2':
            load_command = 'loadMol2'
        elif extension == '.pdb':
            load_command = 'loadPdb'
        else:
            raise ValueError('cannot load format {} in tLeap'.format(extension))

        self.add_commands('{} = {} {}'.format(unit_name, load_command, local_name))

        # Update list of input files to copy in temporary folder before run
        self._input_file_paths[local_name] = file_path

    @_sanitize_tleap_unit_name
    def make_sequence(self, unit_name, sequence):
        """
        Define a Unit with a sequence of residue names
        Parameters
        ----------
        unit_name : str
            Name of the unit as it should be represented in LEaP
        file_path : str
            Space separated equence of residue names (3-letters code)
        """
        self.add_commands('{} = sequence {{ {} }}'.format(unit_name, sequence))

    @_sanitize_tleap_unit_name
    def check_unit(self, unit_name):
        """
        Checking for internal inconsistencies in a Unit such as: long or short bonds, non-integral
        total charge, missing atoms, unwanted steric clashes between atoms.
        Parameters
        ----------
        unit_name : str
            Name of the unit as it should be represented in LEaP
        """
        self.add_commands('check {}'.format(unit_name))

    @_sanitize_tleap_unit_name
    def get_total_charge(self, unit_name):
        """
        Getting the total charge of a Unit
        Parameters
        ----------
        unit_name : str
            Name of the unit as it should be represented in LEaP
        """
        self.add_commands('charge {}'.format(unit_name))

    @_sanitize_tleap_unit_name
    def combine(self, unit_name, *args):
        """
        Combine units in LEaP
        This adds to the script
        Parameters
        ----------
        unit_name : str
            Name of LEaP unit to assign the combination to
        args : iterable of strings
            Name of LEaP units to combine into a single unit called leap_name
        """
        # Sanitize unit names.
        args = [self._sanitize_unit_name(arg) for arg in args]
        components = ' '.join(args)
        self.add_commands('{} = combine {{{{ {} }}}}'.format(unit_name, components))

    @_sanitize_tleap_unit_name
    def add_ions(self, unit_name, ion, num_ions=0, replace_solvent=False):
        """
        Add ions to a unit in LEaP
        This adds to the script
        Parameters
        ----------
        unit_name : str
            Name of the existing LEaP unit which Ions will be added into
        ion : str
            LEaP recognized name of ion to add
        num_ions : int, optional
            Number of ions of type ion to add to unit_name. If 0, the unit
            is neutralized (default is 0).
        replace_solvent : bool, optional
            If True, ions will replace solvent molecules rather than being
            added.
        """
        if replace_solvent:
            self.add_commands('addIonsRand {} {} {}'.format(unit_name, ion, num_ions))
        else:
            self.add_commands('addIons2 {} {} {}'.format(unit_name, ion, num_ions))

    @_sanitize_tleap_unit_name
    def solvate(self, unit_name, solvent_model, clearance, box_geometry="cubic"):
        """
        Solvate a unit in LEaP isometrically
        This adds to the script
        Parameters
        ----------
        unit_name : str
            Name of the existing LEaP unit which will be solvated
        solvent_model : str
            LEaP recognized name of the solvent model to use, e.g. "TIP3PBOX"
        clearance : unit.Quantity
            Add solvent up to clearance distance away (units of length) from the unit_name (radial)
        box_geometry : "cubic" or "truncated_octahedral"
            Shape of the box to be solvated (Default is "cubic").
        """
        if box_geometry=="cubic":
            solvate_command='solvateBox'
        elif box_geometry=="truncated_octahedral":
            solvate_command='solvateOct'
        else:
            raise ValueError('The argument box_geometry must take one of the following values: \
                             "cubic" or "truncated_octahedral".')

        self.add_commands('{} {} {} {} iso'.format(solvate_command, unit_name,
                                                   solvent_model, str(clearance.value_in_unit(unit.angstroms))))

    @_sanitize_tleap_unit_name
    def save_unit(self, unit_name, output_path):
        """
        Write a LEaP unit to file.
        Accepts either ``*.prmtop``, ``*.inpcrd``, or ``*.pdb`` files
        This adds to the script
        Parameters
        ----------
        unit_name : str
            Name of the unit to save
        output_path : str
            Full file path with extension to save.
            Outputs with multiple files (e.g. Amber Parameters) have their names derived from this instead
        """

        file_name = os.path.basename(output_path)
        file_name, extension = os.path.splitext(file_name)
        local_name = file_name+extension

        # Update list of output files to copy from temporary folder after run
        self._output_file_paths[local_name] = output_path

        # Add command
        if extension == '.prmtop' or extension == '.inpcrd':
            command = 'saveAmberParm ' + unit_name + ' {} {}'

            # Update list of output files with the one not explicit
            if extension == '.inpcrd':
                extension2 = '.prmtop'
                local_name2 = filename+extension2
                command = command.format(local_name2, local_name)
            else:
                extension2 = '.inpcrd'
                local_name2 = file_name+extension2
                command = command.format(local_name, local_name2)
            output_path2 = os.path.join(os.path.dirname(output_path), local_name2)
            self._output_file_paths[local_name2] = output_path2

            self.add_commands(command)
        elif extension == '.pdb':
            self.add_commands('savePDB {} {}'.format(unit_name, local_name))
        else:
            raise ValueError('cannot export format {} from tLeap'.format(extension[1:]))

    @_sanitize_tleap_unit_name
    def transform(self, unit_name, transformation):
        """Transformation is an array-like representing the affine transformation matrix."""
        command = 'transform {} {}'.format(unit_name, transformation)
        command = command.replace(r'[', '{{').replace(r']', '}}')
        command = command.replace('\n', '').replace('  ', ' ')
        self.add_commands(command)

    def new_section(self, comment):
        """Adds a comment line to the script"""
        self.add_commands('\n# ' + comment)

    def export_script(self, file_path):
        """
        Write script to file
        Parameters
        ----------
        file_path : str
            Full file path with extension of the script to save
        """
        with open(file_path, 'w') as f:
            f.write(self.script)

    def run(self, working_directory=None, verbose=False):
        """Run script and return warning messages in leap log file."""

        current_directory = os.getcwd()
        tmp_working_directory = False

        if working_directory is None:
            tmp_working_directory = True
            working_directory = tempfile.mkdtemp()
            # Copy input files
            for local_file, file_path in self._input_file_paths.items():
                shutil.copy(file_path, local_file)

        os.chdir(working_directory)

        # Save script and run tleap
        self.export_script('leap.in')
        leap_output = subprocess.check_output(['tleap', '-f', 'leap.in']).decode()

        if verbose:
            print(leap_output)

        # Save leap.log in directory of first output file
        log_path = ''
        if len(self._output_file_paths) > 0:
            # Get first output path in Py 3.X way that is also thread-safe
            for val in self._output_file_paths.values():
                first_output_path = val
                break
            first_output_name = os.path.basename(first_output_path).split('.')[0]
            first_output_dir = os.path.dirname(first_output_path)
            log_path = os.path.join(first_output_dir, first_output_name + '.leap.log')
            shutil.copy('leap.log', log_path)

        # Copy back output files. If something goes wrong, some files may not exist
        known_error_msg = []
        if tmp_working_directory:
            try:
                for local_file, file_path in self._output_file_paths.items():
                    shutil.copy(local_file, file_path)
            except IOError:
                known_error_msg.append("Could not create one of the system files.")

        # Look for errors in log that don't raise CalledProcessError
        error_patterns = ['Argument #\d+ is type \S+ must be of type: \S+']
        for pattern in error_patterns:
            m = re.search(pattern, leap_output)
            if m is not None:
                known_error_msg.append(m.group(0))
                break

        # Analyze log file for water mismatch
        m = re.search("Could not find bond parameter for: EP - \w+W", leap_output)
        if m is not None:
            # Found mismatch water and missing parameters
            known_error_msg.append('It looks like the water used has virtual sites, but '
                                   'missing parameters.\nMake sure your leap parameters '
                                   'use the correct water model as specified by '
                                   'solvent_model.')

        if len(known_error_msg) > 0:
            final_error = ('Some things went wrong with LEaP\nWe caught a few but their may be more.\n'
                           'Please see the log file for LEaP for more info:\n{}\n============\n{}')
            raise RuntimeError(final_error.format(log_path, '\n---------\n'.join(known_error_msg)))

        os.chdir(current_directory)
        if tmp_working_directory:
            shutil.rmtree(working_directory)

        # Check for and return warnings
        return re.findall('WARNING: (.+)', leap_output)

    @staticmethod
    def _sanitize_unit_name(unit_name):
        """Sanitize tleap unit names.
        Leap doesn't like names that start with digits so, in this case, we
        prepend an arbitrary character.
        This takes as unit name a keyword argument called "unit_name" or the
        second sequential argument (skipping self).
        """
        if unit_name[0].isdigit():
            unit_name = 'M' + unit_name
        return unit_name

