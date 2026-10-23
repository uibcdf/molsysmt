"""Validating the PDBQT handler's explicit source-storage policy."""

from molsysmt._private.smonitor import ArgumentError


def digest_storage_mode(storage_mode, caller=None):
    if isinstance(storage_mode, str) and storage_mode in {"resident", "indexed"}:
        return storage_mode
    raise ArgumentError("storage_mode", value=storage_mode, caller=caller)
