"""Validate flat positional populations at the new correspondence boundaries."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError

CALLERS = {
    "molsysmt.structure.least_rmsd_align.least_rmsd_align",
    "molsysmt.structure.center.center",
    "molsysmt.form.file_pdbqt.iterators.__init__",
    "molsysmt.form.string_pdbqt_text.iterators.__init__",
    "molsysmt.form.molsysmt_PDBQTFileHandler.iterators.__init__",
    "molsysmt.build.project_atom_names.project_atom_names",
    "molsysmt.form.file_pdbqt.read_poses.read_poses",
    "molsysmt.form.string_pdbqt_text.read_poses.read_poses",
    "molsysmt.native.pdbqt_file_handler.read_poses",
    "molsysmt.native.pdbqt_file_handler.PDBQTFileHandler.read_poses",
    "molsysmt.native.pdbqt_file_handler.get_coordinates",
    "molsysmt.native.pdbqt_file_handler.PDBQTFileHandler.get_coordinates",
    "molsysmt.chemical_states.get_atom_correspondences.get_atom_correspondences",
    "molsysmt.structure.get_symmetry_corrected_rmsd.get_symmetry_corrected_rmsd",
}


SEQUENCE_CALLERS = {
    f"molsysmt.form.string_amino_acids_{width}.{function}.{function}"
    for width in (1, 3)
    for function in (
        "extract",
        "to_biopython_Seq",
        "to_biopython_SeqRecord",
        "to_string_amino_acids_1",
        "to_string_amino_acids_3",
        "to_molsysmt_Topology",
        "to_molsysmt_MolSys",
    )
}


def _has_units(value):
    return hasattr(value, "unit") or hasattr(value, "units")


def flat_axis(value, argument, caller):
    """Validate unit-free, flat positional integer axes before casting."""
    if _has_units(value) or (
        isinstance(value, (list, tuple)) and any(_has_units(item) for item in value)
    ):
        raise ArgumentError(argument, value=value, caller=caller)
    if value is None:
        return value
    if isinstance(value, str):
        if argument == "selection" or value.lower() == "all":
            return value
        raise ArgumentError(argument, value=value, caller=caller)
    if isinstance(value, (list, tuple)) and any(
        isinstance(item, (bool, np.bool_)) for item in value
    ):
        raise ArgumentError(argument, value=value, caller=caller)
    try:
        array = np.asarray(value)
        if array.ndim == 0:
            array = array.reshape(1)
        if array.ndim == 1 and array.size == 0:
            return np.empty(0, dtype=np.int64)
        if (
            array.ndim == 1
            and array.dtype.kind in "iu"
            and np.all(array >= 0)
            and np.all(array <= np.iinfo(np.int64).max)
        ):
            return array.astype(np.int64)
    except (TypeError, ValueError, OverflowError):
        pass
    raise ArgumentError(argument, value=value, caller=caller)
