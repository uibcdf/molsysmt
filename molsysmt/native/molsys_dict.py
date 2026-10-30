from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict

from molsysmt._private.argdigest import arg_digest


def _empty_molsys_dict() -> Dict[str, Any]:
    from .topology_dict import _empty_topology_dict

    return {
        "format": "molsysmt",
        "kind": "molsys",
        "version": "0.2",
        "metadata": {},
        "topology": _empty_topology_dict(),
        "chemical_states": None,
        "structures": None,
        "structure_chemical_state_indices": None,
        "interactions": {},
    }


@dataclass
class MolSysDict:
    """Storing a declared, serializable molecular system representation (`molsysmt.MolSysDict`)."""

    def __repr__(self):
        """Summarizing stored metadata without reading or rendering payloads."""
        from ._repr import size, summary

        data = vars(self).get("data") or {}
        topology = data.get("topology") or {}
        structures = data.get("structures") or {}
        n_structures = next(
            (
                size(structures[name])
                for name in ("coordinates", "structure_id", "time", "box")
                if structures.get(name) is not None
            ),
            None,
        )
        return summary(
            self,
            n_atoms=size(topology.get("atoms")),
            n_structures=n_structures,
        )

    data: Dict[str, Any] = field(default_factory=_empty_molsys_dict)

    def to_dict(self, copy: bool = True) -> Dict[str, Any]:
        """Returning the underlying serializable dictionary."""
        return deepcopy(self.data) if copy else self.data

    def __copy__(self):
        """Copying independent mutable state through the native graph protocol."""
        return self.__deepcopy__({})

    def __deepcopy__(self, memo):
        """Copying current state with the containing graph's memo."""
        from ._copy import _clone

        return _clone(self, memo)

    @arg_digest()
    def copy(self, *, skip_digestion=False) -> "MolSysDict":
        """Copying a declarative molecular-system payload independently.

        Parameters
        ----------
        skip_digestion : bool, default=False
            Skip argument digestion only for inputs already satisfying this contract.

        Returns
        -------
        MolSysDict
            An independent wrapper retaining its declared payload and metadata.

        Notes
        -----
        Python copy.copy and copy.deepcopy also detach mutable payload data.
        Immutable byte-backed numeric storage may remain shared behind separate
        array headers. Copying preserves the concrete type and ordinary graph
        aliases; it does not validate the schema or construct a MolSys.

        Examples
        --------
        >>> payload = MolSysDict()
        >>> duplicate = payload.copy()
        >>> duplicate is payload
        False
        >>> duplicate.data['kind']
        'molsys'

        .. admonition:: User guide

           See :ref:`user-foundations-resident-copying` for native and payload copy contracts.

        .. versionadded:: 1.0.0
        """
        from ._copy import _copy_independently

        return _copy_independently(self, skip_digestion)
