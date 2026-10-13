"""Retain the native PDB attribute contract for compressed input."""

from molsysmt.form.molsysmt_PDBFileHandler.attributes import (
    attributes as _native_attributes,
)

attributes = _native_attributes.copy()
