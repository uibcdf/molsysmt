"""Reading stored modular mechanics through validated file-form getters."""

from molsysmt._private.attribute_catalog import mechanical_attributes as _MECHANICAL
from molsysmt.form._query_delegation import make_routed_getter as _make_routed_getter
from molsysmt.form.molsysmt_MolSys import get_mechanical_attributes as _native

from ._modular_query import route_mechanical_getter as _route

__all__ = []
for _name in _native.__all__:
    if _name[4:].rsplit("_from_", 1)[0] not in _MECHANICAL:
        continue
    _getter = _make_routed_getter(
        _name, getattr(_native, _name), "file:h5msm", _route, module=__name__
    )
    _getter.__doc__ = _getter.__doc__.replace("molsysmt.MolSys", "file:h5msm")
    globals()[_name] = _getter
    __all__.append(_name)
del _name, _getter
