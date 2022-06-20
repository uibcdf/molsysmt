import argparse
import os
import re
import glob
import shutil
import subprocess as sp
from tempfile import TemporaryDirectory
from contextlib import contextmanager
# YAML imports
import yaml  # PyYAML
loader = yaml.load

@contextmanager
def temp_cd():
    """Temporary CD Helper"""
    cwd = os.getcwd()
    with TemporaryDirectory() as td:
        try:
            os.chdir(td)
            yield
        finally:
            os.chdir(cwd)


# Args
parser = argparse.ArgumentParser(description='Creates a conda environment from file for a given Python version.')
parser.add_argument('-n', '--name', type=str,
                    help='The name of the created Python environment')
parser.add_argument('-p', '--python', type=str,
                    help='The version of the created Python environment')
parser.add_argument('conda_file',
                    help='The file for the created Python environment')

args = parser.parse_args()

# Open the base file
with open(args.conda_file, "r") as handle:
    yaml_script = loader(handle.read(), Loader=yaml.FullLoader)

python_replacement_string = "python {}*".format(args.python)

try:
    for dep_index, dep_value in enumerate(yaml_script['dependencies']):
        if re.match('python([ ><=*]+[0-9.*]*)?$', dep_value):  # Match explicitly 'python' and its formats
            yaml_script['dependencies'].pop(dep_index)
            break  # Making the assumption there is only one Python entry, also avoids need to enumerate in reverse
except (KeyError, TypeError):
    # Case of no dependencies key, or dependencies: None
    yaml_script['dependencies'] = []
finally:
    # Ensure the python version is added in. Even if the code does not need it, we assume the env does
    yaml_script['dependencies'].insert(0, python_replacement_string)

# Figure out conda path
if "CONDA_EXE" in os.environ:
    conda_path = os.environ["CONDA_EXE"]
else:
    conda_path = shutil.which("conda")
if conda_path is None:
    raise RuntimeError("Could not find a conda binary in CONDA_EXE variable or in executable search path")

print("CONDA ENV NAME  {}".format(args.name))
print("PYTHON VERSION  {}".format(args.python))
print("CONDA FILE NAME {}".format(args.conda_file))
print("CONDA PATH      {}".format(conda_path))

# Write to a temp directory which will always be cleaned up
with temp_cd():
    temp_file_name = "temp_script.yaml"
    with open(temp_file_name, 'w') as f:
        f.write(yaml.dump(yaml_script))
    sp.call("{} env create -n {} -f {}".format(conda_path, args.name, temp_file_name), shell=True)
