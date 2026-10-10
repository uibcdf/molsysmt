"""Regenerating ions reference tables from explicit local inputs.

Run with --help for CCD, output and optional supplementary source arguments.
Importing this module performs no parsing, download or file generation.
"""

from molsysmt.data._make._chemical_group_database import _main

if __name__ == "__main__":
    raise SystemExit(_main("ions"))
