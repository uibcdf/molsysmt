"""Shared setup for the molsysviewer_molsysmt test suite.

Makes the molsysmt repo root importable so the addon can be tested from a source
checkout without installing it. MolSysViewer must be importable in the
environment (installed, or on ``PYTHONPATH``); the tests do not hardcode any
path to it.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
