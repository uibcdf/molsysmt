"""Shared source/wheel/installed metadata contract for the redesigned addon.

These are structural package checks. Live bound scientific parity is qualified
separately; matching entry-point text alone never proves runtime compatibility.
"""

from pathlib import PurePosixPath

TOOLS_ENTRY_POINTS = {"molsysmt-tools": "molsysviewer_molsysmt.tools"}
TOOLS_FILES = frozenset(
    {
        "molsysviewer_molsysmt/__init__.py",
        "molsysviewer_molsysmt/_argdigest.py",
        "molsysviewer_molsysmt/_api.py",
        "molsysviewer_molsysmt/_pbc.py",
        "molsysviewer_molsysmt/_physchem.py",
        "molsysviewer_molsysmt/_basic.py",
        "molsysviewer_molsysmt/_topology.py",
        "molsysviewer_molsysmt/_structure.py",
        "molsysviewer_molsysmt/_geometry.py",
        "molsysviewer_molsysmt/tools.py",
        "molsysviewer_molsysmt/_private/__init__.py",
        "molsysviewer_molsysmt/_private/normalization.py",
        "molsysviewer_molsysmt/_private/function/__init__.py",
        "molsysviewer_molsysmt/_private/function/basic_set.py",
        "molsysviewer_molsysmt/_private/function/structure_get_neighbors.py",
        "molsysviewer_molsysmt/_private/argument/__init__.py",
        "molsysviewer_molsysmt/_private/argument/skip_digestion.py",
        "molsysviewer_molsysmt/_private/argument/update_view.py",
    }
)


def validate_tools_files(paths):
    """Return missing new sources and unexpected retired integration files."""
    files = {
        PurePosixPath(str(path)).as_posix()
        for path in paths
        if not str(path).endswith("/")
        and PurePosixPath(str(path)).parts
        and PurePosixPath(str(path)).parts[0] == "molsysviewer_molsysmt"
    }
    errors = []
    missing = sorted(TOOLS_FILES - files)
    if missing:
        errors.append(f"redesigned MolSysMT tools files are missing: {missing}")
    unexpected = sorted(files - TOOLS_FILES)
    if unexpected:
        errors.append(f"retired or unreviewed Viewer addon files remain: {unexpected}")
    return errors


def validate_tools_entry_points(entries):
    """Return errors when declarations differ from the admitted new route."""
    if dict(entries) != TOOLS_ENTRY_POINTS:
        return [
            "redesigned MolSysMT tools entry point is missing, retired or unsupported; "
            "expected molsysmt-tools = molsysviewer_molsysmt.tools"
        ]
    return []
