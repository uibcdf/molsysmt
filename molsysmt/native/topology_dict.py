from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict

from molsysmt._private.argdigest import arg_digest


def _empty_topology_dict() -> Dict[str, Any]:
    return {
        "format": "molsysmt",
        "kind": "topology",
        "version": "0.2",
        "metadata": {},
        "atoms": [],
        "groups": [],
        "chains": [],
        "molecules": [],
        "entities": [],
    }


@dataclass
class TopologyDict:
    """Storing a declared, serializable topology representation (`molsysmt.TopologyDict`)."""

    def __repr__(self):
        """Summarizing stored metadata without reading or rendering payloads."""
        from ._repr import size, summary

        data = vars(self).get("data") or {}
        return summary(
            self,
            n_atoms=size(data.get("atoms")),
            n_groups=size(data.get("groups")),
            n_molecules=size(data.get("molecules")),
        )

    data: Dict[str, Any] = field(default_factory=_empty_topology_dict)

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
    def copy(self, *, skip_digestion=False) -> "TopologyDict":
        """Copying a declarative topology payload independently.

        Parameters
        ----------
        skip_digestion : bool, default=False
            Skip argument digestion only for inputs already satisfying this contract.

        Returns
        -------
        TopologyDict
            An independent wrapper retaining the topology record schema.

        Notes
        -----
        Python copy.copy and copy.deepcopy detach mutable payload data and
        preserve supported extension state. Immutable bytes may remain shared.
        Copying does not rebuild topology, infer components or certify that a
        supplied payload satisfies its declared schema.

        Examples
        --------
        >>> payload = TopologyDict()
        >>> duplicate = payload.copy()
        >>> duplicate is payload
        False
        >>> duplicate.data['kind']
        'topology'

        .. admonition:: User guide

           See :ref:`user-foundations-resident-copying` for native and payload copy contracts.

        .. versionadded:: 1.0.0
        """
        from ._copy import _copy_independently

        return _copy_independently(self, skip_digestion)
