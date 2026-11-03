"""Read declared PDBQT inventory and chemistry without discarding its document."""

from molsysmt.form._query_delegation import make_native_getter
from molsysmt.form.molsysmt_MolSys import get_topological_attributes as _native

from .attributes import attributes as _attributes


def _read_source(item):
    return item._native()


__all__ = []
for _name in _native.__all__:
    _attribute, _element = _name[4:].rsplit("_from_", 1)
    if _attributes.get(_attribute, False) and _attribute != "n_structures":
        globals()[_name] = make_native_getter(
            _name, getattr(_native, _name), "molsysmt.PDBQTFileHandler", _read_source
        )
        __all__.append(_name)
