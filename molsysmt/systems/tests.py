import importlib.resources
from pathlib import Path

data_dir = importlib.resources.files('molsysmt.data')


tests = {}


del(importlib.resources, Path, data_dir)

