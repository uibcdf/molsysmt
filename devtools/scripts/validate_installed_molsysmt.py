#!/usr/bin/env python
"""Validating representative public APIs from an installed MolSysMT wheel."""

from __future__ import annotations

from importlib import metadata, resources
import json
from pathlib import Path
import sys


def _is_editable(distribution: metadata.Distribution) -> bool:
    content = distribution.read_text("direct_url.json")
    if not content:
        return False
    payload = json.loads(content)
    return bool(payload.get("dir_info", {}).get("editable", False))


def _require_installed_path(path: Path) -> None:
    prefix = Path(sys.prefix).resolve()
    if not path.resolve().is_relative_to(prefix):
        raise RuntimeError(f"installed module resolves outside the environment: {path}")


def validate_public_runtime() -> dict[str, object]:
    """Running representative installed-wheel operations."""

    import numpy as np
    import molsysmt as msm
    import molsysmt._rust as rust

    distribution = metadata.distribution("molsysmt")
    if _is_editable(distribution):
        raise RuntimeError("installed MolSysMT distribution is editable")

    package_path = Path(msm.__file__).resolve()
    extension_path = Path(rust.__file__).resolve()
    _require_installed_path(package_path)
    _require_installed_path(extension_path)

    manifest = resources.files("molsysmt.data").joinpath("demo_manifest.json")
    if not manifest.is_file():
        raise RuntimeError("installed demo manifest is missing")

    entry_points = [
        entry
        for entry in metadata.entry_points(group="molsysviewer.addons")
        if entry.name == "molsysmt" and entry.value == "molsysviewer_molsysmt"
    ]
    if len(entry_points) != 1:
        raise RuntimeError("installed MolSysViewer addon entry point is missing")

    trp_cage = msm.convert(
        msm.systems["Trp-Cage"]["1l2y.h5msm"],
        to_form="molsysmt.MolSys",
    )
    n_atoms = msm.get(trp_cage, n_atoms=True)
    if n_atoms <= 0:
        raise RuntimeError("installed get() returned an empty system")
    alpha_carbons = msm.select(trp_cage, selection='atom_name == "CA"')
    if len(alpha_carbons) == 0:
        raise RuntimeError("installed select() returned no alpha carbons")

    center = msm.structure.get_center(
        trp_cage,
        selection=alpha_carbons,
        structure_indices=[0, 1],
    )
    distances = msm.structure.get_distances(
        trp_cage,
        selection=alpha_carbons[:4],
        structure_indices=[0, 1],
    )
    rmsd = msm.structure.get_rmsd(
        trp_cage,
        selection=alpha_carbons,
        structure_indices=[0, 1, 2],
        reference_structure_index=0,
    )
    eigenvectors, eigenvalues = msm.structure.principal_component_analysis(
        trp_cage,
        selection=alpha_carbons,
    )
    sasa = msm.physchem.get_sasa(
        trp_cage,
        element="atom",
        structure_indices=[0],
        engine="MolSysMT",
        n_sphere_points=20,
        use_cell_list=True,
    )
    covalent_blocks = msm.topology.get_covalent_blocks(trp_cage)

    pentalanine = msm.convert(
        msm.systems["pentalanine"]["traj_pentalanine.h5msm"],
        to_form="molsysmt.MolSys",
        structure_indices=[0, 1],
    )
    wrapped = msm.pbc.wrap_to_mic(pentalanine)

    if center.shape != (2, 1, 3):
        raise RuntimeError(f"unexpected center shape: {center.shape}")
    if distances.shape != (2, 4, 4):
        raise RuntimeError(f"unexpected distance shape: {distances.shape}")
    if rmsd.shape != (3,):
        raise RuntimeError(f"unexpected RMSD shape: {rmsd.shape}")
    if eigenvectors.ndim != 2 or eigenvalues.ndim != 1:
        raise RuntimeError("installed PCA returned an invalid shape contract")
    if np.asarray(msm.pyunitwizard.get_value(sasa)).shape[0] != 1:
        raise RuntimeError("installed SASA returned an invalid structure axis")
    if len(covalent_blocks) == 0:
        raise RuntimeError("installed topology component discovery returned no blocks")
    if msm.get(wrapped, n_structures=True) != 2:
        raise RuntimeError("installed PBC operation lost structures")

    return {
        "version": msm.__version__,
        "package": str(package_path),
        "extension": str(extension_path),
        "n_atoms": int(n_atoms),
        "n_alpha_carbons": int(len(alpha_carbons)),
        "n_covalent_blocks": int(len(covalent_blocks)),
    }


def main() -> int:
    """Printing a compact installed-runtime verdict."""

    result = validate_public_runtime()
    print(
        "MolSysMT installed public runtime validation passed: "
        f"version={result['version']} | n_atoms={result['n_atoms']} | "
        f"n_alpha_carbons={result['n_alpha_carbons']} | "
        f"n_covalent_blocks={result['n_covalent_blocks']} | "
        f"package={result['package']} | extension={result['extension']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
