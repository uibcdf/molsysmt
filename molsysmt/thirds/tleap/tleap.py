from molsysmt._private.smonitor import StructuralInconsistencyError, InternalAlgorithmError
import functools
import os
import re
import shutil
import subprocess
import tempfile

from molsysmt import pyunitwizard as puw


def _sanitize_tleap_unit_name(function):
    """Normalizing LEaP unit names before dispatching method calls."""

    @functools.wraps(function)
    def _wrapper(*args, **kwargs):
        try:
            kwargs["unit_name"] = TLeap._sanitize_unit_name(kwargs["unit_name"])
        except KeyError:
            args = args[:1] + (TLeap._sanitize_unit_name(args[1]),) + args[2:]
        return function(*args, **kwargs)

    return _wrapper


class TLeap:
    """Building and executing tLEaP scripts in an isolated working directory."""

    @property
    def script(self):
        """Returning the current script with a trailing ``quit`` command."""

        return self._script + "\nquit\n"

    def __init__(self):
        self._script = ""
        self._input_file_paths = {}
        self._output_file_paths = {}
        self._loaded_parameters = set()
        self._tleap_executable = os.environ.get("TLEAP_BIN", "tleap")
        self._critical_patterns = [
            re.compile(r"Could not find bond parameter for:", re.IGNORECASE),
            re.compile(r"FATAL:", re.IGNORECASE),
            re.compile(r"\bError!\b", re.IGNORECASE),
        ]

    def add_commands(self, *commands):
        """Appending one or more raw LEaP commands to the script."""

        for command in commands:
            self._script += command + "\n"

    def load_parameters(self, *parameter_files):
        """Loading LEaP parameter/command files once per instance."""

        for parameter_file in parameter_files:
            if parameter_file in self._loaded_parameters:
                continue

            if os.path.isfile(parameter_file):
                local_name = os.path.basename(parameter_file)
                self._input_file_paths[local_name] = parameter_file
            else:
                local_name = parameter_file

            base_name = os.path.basename(parameter_file)
            extension = os.path.splitext(base_name)[1].lower()

            if "frcmod" in base_name or extension == ".dat":
                self.add_commands("loadAmberParams " + local_name)
            elif extension in {".off", ".lib"}:
                self.add_commands("loadOff " + local_name)
            else:
                self.add_commands("source " + local_name)

            self._loaded_parameters.add(parameter_file)

    def set_global_parameter(self, **kwargs):
        """Setting LEaP global defaults through ``set default`` commands."""

        accepted_values = {
            "OldPrmtopFormat": ["on", "off"],
            "Dielectric": ["constant", "distance"],
            "PdbWriteCharges": ["on", "off"],
            "PBRadii": ["bondi", "mbondi", "mbondi2", "mbondi3", "amber6"],
            "nocenter": ["on", "off"],
            "reorder_residues": ["on", "off"],
        }

        for parameter, value in kwargs.items():
            if parameter not in accepted_values:
                raise ArgumentChoiceError("parameter", parameter, choices="tLeap recognized parameters", caller="molsysmt.thirds.tleap.tleap")
            if value not in accepted_values[parameter]:
                raise ArgumentChoiceError(parameter, value, choices="tLeap recognized values", caller="molsysmt.thirds.tleap.tleap")
            self.add_commands(f"set default {parameter} {value}")

    @_sanitize_tleap_unit_name
    def load_unit(self, unit_name, file_path):
        """Loading a PDB/MOL2 file as a LEaP unit."""

        local_name = os.path.basename(file_path)
        extension = os.path.splitext(local_name)[1].lower()

        if extension == ".mol2":
            load_command = "loadMol2"
        elif extension == ".pdb":
            load_command = "loadPdb"
        else:
            raise FormatError(f"cannot load format {extension} in tLeap", caller="molsysmt.thirds.tleap.tleap")

        self.add_commands(f"{unit_name} = {load_command} {local_name}")
        self._input_file_paths[local_name] = file_path

    @_sanitize_tleap_unit_name
    def make_sequence(self, unit_name, sequence):
        """Creating a LEaP unit from a sequence of residue names."""

        self.add_commands(f"{unit_name} = sequence {{ {sequence} }}")

    @_sanitize_tleap_unit_name
    def check_unit(self, unit_name):
        """Running LEaP ``check`` on an existing unit."""

        self.add_commands(f"check {unit_name}")

    @_sanitize_tleap_unit_name
    def get_total_charge(self, unit_name):
        """Requesting total charge report for a LEaP unit."""

        self.add_commands(f"charge {unit_name}")

    @_sanitize_tleap_unit_name
    def combine(self, unit_name, *units):
        """Combining multiple units into a single target unit."""

        normalized_units = [self._sanitize_unit_name(unit) for unit in units]
        components = " ".join(normalized_units)
        self.add_commands(f"{unit_name} = combine {{ {components} }}")

    @_sanitize_tleap_unit_name
    def add_ions(self, unit_name, ion, num_ions=0, replace_solvent=False):
        """Adding ions to a unit using LEaP ion placement commands."""

        if replace_solvent:
            self.add_commands(f"addIonsRand {unit_name} {ion} {num_ions}")
        else:
            self.add_commands(f"addIons2 {unit_name} {ion} {num_ions}")

    @_sanitize_tleap_unit_name
    def solvate(self, unit_name, solvent_model, clearance, box_geometry="cubic"):
        """Solvating a unit with an isotropic box clearance."""

        if box_geometry == "cubic":
            solvate_command = "solvateBox"
        elif box_geometry == "truncated octahedral":
            solvate_command = "solvateOct"
        else:
            raise ValueError(
                "The argument box_geometry must be one of: "
                "'cubic' or 'truncated octahedral'."
            )

        clearance = puw.get_value(clearance, to_unit="angstroms")
        self.add_commands(f"{solvate_command} {unit_name} {solvent_model} {clearance} iso")

    @_sanitize_tleap_unit_name
    def save_unit(self, unit_name, output_path):
        """Saving a LEaP unit to prmtop/inpcrd or pdb output."""

        file_name = os.path.basename(output_path)
        stem, extension = os.path.splitext(file_name)
        extension = extension.lower()
        local_name = stem + extension

        self._output_file_paths[local_name] = output_path

        if extension in {".prmtop", ".inpcrd"}:
            companion_extension = ".prmtop" if extension == ".inpcrd" else ".inpcrd"
            companion_local_name = stem + companion_extension
            companion_output_path = os.path.join(os.path.dirname(output_path), companion_local_name)
            self._output_file_paths[companion_local_name] = companion_output_path

            if extension == ".inpcrd":
                self.add_commands(
                    f"saveAmberParm {unit_name} {companion_local_name} {local_name}"
                )
            else:
                self.add_commands(
                    f"saveAmberParm {unit_name} {local_name} {companion_local_name}"
                )

        elif extension == ".pdb":
            self.add_commands(f"savePDB {unit_name} {local_name}")

        else:
            raise FormatError(f"cannot export format {extension} from tLeap", caller="molsysmt.thirds.tleap.tleap")

    @_sanitize_tleap_unit_name
    def transform(self, unit_name, transformation):
        """Applying an affine transformation matrix to a LEaP unit."""

        command = f"transform {unit_name} {transformation}"
        command = command.replace("[", "{").replace("]", "}")
        command = command.replace("\n", "").replace("  ", " ")
        self.add_commands(command)

    def new_section(self, comment):
        """Adding a comment line to visually separate script sections."""

        self.add_commands("\n# " + comment)

    def export_script(self, file_path):
        """Writing current LEaP script to disk."""

        with open(file_path, "w", encoding="utf-8") as file_handle:
            file_handle.write(self.script)

    def _parse_diagnostics(self, leap_output):
        """Extracting structured diagnostics from LEaP output text."""

        diagnostics = []
        for line in (leap_output or "").splitlines():
            stripped = line.strip()
            if stripped.startswith("WARNING:"):
                diagnostics.append(
                    {
                        "severity": "warning",
                        "message": stripped[len("WARNING:") :].strip(),
                        "line": stripped,
                    }
                )
            elif stripped.startswith("FATAL:"):
                diagnostics.append(
                    {
                        "severity": "fatal",
                        "message": stripped[len("FATAL:") :].strip(),
                        "line": stripped,
                    }
                )
            elif stripped.startswith("ERROR:"):
                diagnostics.append(
                    {
                        "severity": "error",
                        "message": stripped[len("ERROR:") :].strip(),
                        "line": stripped,
                    }
                )
            elif re.search(r"\bError!\b", stripped):
                diagnostics.append(
                    {
                        "severity": "error",
                        "message": stripped,
                        "line": stripped,
                    }
                )
        return diagnostics

    def _collect_strict_issues(self, leap_output):
        """Collecting strict-mode issues from LEaP output."""

        strict_issues = []
        for pattern in self._critical_patterns:
            match = pattern.search(leap_output)
            if match is not None:
                strict_issues.append(match.group(0))
        return strict_issues

    def run(
        self,
        working_directory=None,
        verbose=False,
        strict=False,
        return_diagnostics=False,
        keep_working_directory=False,
    ):
        """Running tLEaP script and returning warnings or structured diagnostics."""

        current_directory = os.getcwd()
        temporary_working_directory = False

        if working_directory is None:
            temporary_working_directory = True
            working_directory = tempfile.mkdtemp()
        else:
            os.makedirs(working_directory, exist_ok=True)

        for local_file, source_path in self._input_file_paths.items():
            destination = os.path.join(working_directory, local_file)
            if os.path.abspath(source_path) != os.path.abspath(destination):
                shutil.copy(source_path, destination)

        leap_output = ""
        log_path = ""

        try:
            os.chdir(working_directory)
            self.export_script("leap.in")

            try:
                process = subprocess.run(
                    [self._tleap_executable, "-f", "leap.in"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    check=False,
                )
            except FileNotFoundError as exc:
                raise RuntimeError(
                    f"Could not execute tleap binary '{self._tleap_executable}'. "
                    "Ensure AmberTools is installed and tleap is available in PATH "
                    "or set TLEAP_BIN."
                ) from exc

            leap_output = process.stdout or ""

            if verbose:
                print(leap_output)

            for local_file, target_path in self._output_file_paths.items():
                local_path = os.path.join(working_directory, local_file)
                if os.path.exists(local_path):
                    if os.path.abspath(local_path) != os.path.abspath(target_path):
                        shutil.copy(local_path, target_path)

            if self._output_file_paths and os.path.exists(os.path.join(working_directory, "leap.log")):
                first_output_path = next(iter(self._output_file_paths.values()))
                first_output_name = os.path.basename(first_output_path).split(".")[0]
                first_output_dir = os.path.dirname(first_output_path)
                log_path = os.path.join(first_output_dir, first_output_name + ".leap.log")
                shutil.copy(os.path.join(working_directory, "leap.log"), log_path)

            known_errors = []

            if process.returncode != 0:
                known_errors.append(f"tleap exited with code {process.returncode}.")

            missing_outputs = []
            for local_file, target_path in self._output_file_paths.items():
                if not os.path.exists(os.path.join(working_directory, local_file)):
                    missing_outputs.append(target_path)
            if missing_outputs:
                known_errors.append(
                    "Could not create one or more expected output files: "
                    + ", ".join(missing_outputs)
                )

            argument_type_error = re.search(
                r"Argument #\d+ is type \S+ must be of type: \S+",
                leap_output,
            )
            if argument_type_error is not None:
                known_errors.append(argument_type_error.group(0))

            missing_ep_parameter = re.search(
                r"Could not find bond parameter for: EP - \w+W",
                leap_output,
            )
            if missing_ep_parameter is not None:
                known_errors.append(
                    "It looks like the selected water model uses virtual sites, "
                    "but some required parameters are missing."
                )

            diagnostics = self._parse_diagnostics(leap_output)
            strict_issues = self._collect_strict_issues(leap_output) if strict else []
            if strict_issues:
                known_errors.append(
                    "Strict mode flagged critical LEaP diagnostics: " + ", ".join(sorted(set(strict_issues)))
                )

            if known_errors:
                message = (
                    "Some things went wrong with LEaP\n"
                    "We caught a few but there may be more.\n"
                    "Please see the LEaP log for more information:\n{}\n"
                    "============\n{}"
                )
                raise RuntimeError(message.format(log_path, "\n---------\n".join(known_errors)))

            warning_messages = [entry["message"] for entry in diagnostics if entry["severity"] == "warning"]

            if return_diagnostics:
                return {
                    "warnings": warning_messages,
                    "diagnostics": diagnostics,
                    "log_path": log_path,
                    "working_directory": working_directory,
                    "tleap_executable": self._tleap_executable,
                    "return_code": process.returncode,
                }
            return warning_messages

        finally:
            os.chdir(current_directory)
            if temporary_working_directory and not keep_working_directory:
                shutil.rmtree(working_directory, ignore_errors=True)

    @staticmethod
    def _sanitize_unit_name(unit_name):
        """Normalizing LEaP unit names to avoid unsupported leading digits."""

        if not isinstance(unit_name, str) or len(unit_name) == 0:
            raise ValueError("Unit name must be a non-empty string.")
        if unit_name[0].isdigit():
            unit_name = "M" + unit_name
        return unit_name
