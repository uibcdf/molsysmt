"""Structure adapters for MolSysMT analyses rendered in MolSysViewer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from smonitor import signal

from ..access import has_system
from ._telemetry import adapter_n_atoms


@dataclass(frozen=True)
class ContactPairs:
    """Contact pairs ready for MolSysViewer link rendering."""

    atom_pairs: list[list[int]]
    structures: list[list[list[int]]]
    threshold: str
    selection: Any = "all"

    @property
    def n_contacts(self) -> int:
        return len(self.atom_pairs)


@dataclass(frozen=True)
class RMSDResult:
    """RMSD values plus a scalar summary for panel display."""

    values: Any
    mean: float


@dataclass(frozen=True)
class RMSFResult:
    """RMSF values plus a scalar summary for panel display."""

    values: Any
    mean: float


@dataclass(frozen=True)
class PCAResult:
    """PCA output plus PC1 vectors and variance for viewer rendering."""

    principal_components: Any
    variances: Any
    pc1_vectors: Any
    pc1_variance: float
    atom_indices: list[int]


def contact_pairs(
    view: Any,
    *,
    selection: Any = "all",
    threshold: str = "4 angstroms",
) -> ContactPairs:
    """Return atom-index contact pairs for the active view system."""
    if not has_system(view):
        raise ValueError("No molecular system attached.")

    import molsysmt as msm

    structures = msm.structure.get_contacts(
        view,
        selection=selection,
        threshold=threshold,
        output_type="sorted pairs",
        output_indices="atom",
    )
    normalized = [
        [[int(pair[0]), int(pair[1])] for pair in structure_pairs]
        for structure_pairs in structures
    ]
    first_structure = normalized[0] if normalized else []
    return ContactPairs(
        atom_pairs=first_structure,
        structures=normalized,
        threshold=threshold,
        selection=selection,
    )


@signal(
    tags=["molsysmt-addon", "adapter", "structure"],
    extra_factory=adapter_n_atoms,
)
def rmsd(
    view: Any,
    *,
    selection: Any = 'atom_type!="H"',
    structure_indices: Any = "all",
    syntax: str = "MolSysMT",
) -> RMSDResult:
    """Compute RMSD from the active view system."""
    if not has_system(view):
        raise ValueError("No molecular system attached.")

    import numpy as np

    import molsysmt as msm

    values = msm.structure.get_rmsd(
        view,
        selection=selection,
        structure_indices=structure_indices,
        syntax=syntax,
    )
    arr = np.asarray(values).flatten()
    mean = float(arr.mean()) if len(arr) else 0.0
    return RMSDResult(values=values, mean=mean)


@signal(
    tags=["molsysmt-addon", "adapter", "structure"],
    extra_factory=adapter_n_atoms,
)
def rmsf(
    view: Any,
    *,
    selection: Any = 'atom_type!="H"',
    structure_indices: Any = "all",
    syntax: str = "MolSysMT",
) -> RMSFResult:
    """Compute RMSF from the active view system."""
    if not has_system(view):
        raise ValueError("No molecular system attached.")

    import numpy as np

    import molsysmt as msm

    values = msm.structure.get_rmsf(
        view,
        selection=selection,
        structure_indices=structure_indices,
        syntax=syntax,
    )
    arr = np.asarray(values).flatten()
    mean = float(arr.mean()) if len(arr) else 0.0
    return RMSFResult(values=values, mean=mean)


@signal(
    tags=["molsysmt-addon", "adapter", "structure"],
    extra_factory=adapter_n_atoms,
)
def pca(
    view: Any,
    *,
    selection: Any = "all",
    structure_indices: Any = "all",
    syntax: str = "MolSysMT",
) -> PCAResult:
    """Compute PCA from the active view system and expose PC1 vectors."""
    if not has_system(view):
        raise ValueError("No molecular system attached.")

    import numpy as np

    import molsysmt as msm

    principal_components, variances = msm.structure.principal_component_analysis(
        view,
        selection=selection,
        structure_indices=structure_indices,
        syntax=syntax,
    )
    variances_arr = np.asarray(variances).flatten()
    pc1_variance = float(variances_arr[0]) if len(variances_arr) else 0.0
    pc1_vectors = (
        np.asarray(principal_components[0])
        if hasattr(principal_components, "__len__")
        else np.asarray(principal_components)
    )
    return PCAResult(
        principal_components=principal_components,
        variances=variances,
        pc1_vectors=pc1_vectors,
        pc1_variance=pc1_variance,
        atom_indices=list(range(len(pc1_vectors))),
    )
