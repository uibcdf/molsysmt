"""Curating the pinned EST chemical-template regression, without downloading data.

This fixture-specific generator is not a general CCD reader or automatic template
matcher. It requires the exact audited 1QKU/EST bytes and refuses ambiguous graph
correspondence. The produced template has no coordinates or explicit H atoms.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np

SOURCE_SHA256 = "8f06e49437b661728c5ca1e3427a4f1bdce9aee1aa9bbe27f1eab4fb2d17f02e"
CCD_SHA256 = "8b80ee77d734e62a82a27571bc1de261e8ea4cf9d053490d10a39c614a69d3a8"
SELECTION = 'group_name == "EST" and chain_id == "D"'


def curate(entry: Path, ccd: Path, output: Path):
    """Generate one deliberately curated control from the pinned source revision."""
    from rdkit import Chem, rdBase

    import molsysmt as msm

    entry_bytes = entry.read_bytes()
    if entry.suffix == ".gz":
        entry_bytes = gzip.decompress(entry_bytes)
    for name, content, digest in (
        (entry.name, entry_bytes, SOURCE_SHA256),
        (ccd.name, ccd.read_bytes(), CCD_SHA256),
    ):
        if hashlib.sha256(content).hexdigest() != digest:
            raise ValueError(f"Unexpected source revision: {name}")
    data = msm.convert(str(ccd), to_form="mmcif.PdbxContainers.DataContainer")
    atoms, bonds, descriptors = [
        data.getObj(name)
        for name in ("chem_comp_atom", "chem_comp_bond", "pdbx_chem_comp_descriptor")
    ]
    heavy = [
        i for i in range(atoms.getRowCount()) if atoms.getValue("type_symbol", i) != "H"
    ]
    names = [atoms.getValue("atom_id", i) for i in heavy]
    indices = {name: i for i, name in enumerate(names)}
    builder, graph = msm.MolSysBuilder(), Chem.RWMol()
    for row in heavy:
        name, symbol = [
            atoms.getValue(field, row) for field in ("atom_id", "type_symbol")
        ]
        builder.add_atom(atom_id=name, atom_name=name, atom_type=symbol)
        atom = Chem.Atom(symbol)
        atom.SetFormalCharge(int(atoms.getValue("charge", row)))
        atom.SetIsAromatic(atoms.getValue("pdbx_aromatic_flag", row) == "Y")
        graph.AddAtom(atom)
    hydrogen_counts, aromatic_by_pair = Counter(), {}
    order_types = {
        1: Chem.BondType.SINGLE,
        2: Chem.BondType.DOUBLE,
        3: Chem.BondType.TRIPLE,
    }
    for row in range(bonds.getRowCount()):
        first, second = [
            bonds.getValue(field, row) for field in ("atom_id_1", "atom_id_2")
        ]
        if first in indices and second in indices:
            a, b = indices[first], indices[second]
            order = {"SING": 1, "DOUB": 2, "TRIP": 3}[
                bonds.getValue("value_order", row)
            ]
            aromatic = bonds.getValue("pdbx_aromatic_flag", row) == "Y"
            builder.add_bond(a, b, bond_order=order, bond_type="covalent")
            graph.AddBond(
                a, b, Chem.BondType.AROMATIC if aromatic else order_types[order]
            )
            aromatic_by_pair[tuple(sorted((a, b)))] = aromatic
        elif first in indices:
            hydrogen_counts[first] += 1
        elif second in indices:
            hydrogen_counts[second] += 1
    rows = [
        i
        for i in range(descriptors.getRowCount())
        if descriptors.getValue("type", i) == "SMILES_CANONICAL"
        and descriptors.getValue("program", i) == "CACTVS"
    ]
    if len(rows) != 1:
        raise ValueError("The pinned canonical descriptor must be unique.")
    smiles = descriptors.getValue("descriptor", rows[0])
    reference = Chem.MolFromSmiles(smiles)
    heavy_graph = graph.GetMol()
    Chem.SanitizeMol(heavy_graph)
    # A uniquified atom-set match would hide distinct atom correspondences.
    matches = heavy_graph.GetSubstructMatches(
        reference, uniquify=False, useChirality=False
    )
    if len(matches) != 1 or len(matches[0]) != len(names):
        raise ValueError(
            "A unique exhaustive reference/CCD atom correspondence is required."
        )
    inverse = np.argsort(matches[0])
    template = builder.build()
    fields = (
        "formal_charge",
        "atom_is_aromatic",
        "n_unpaired_electrons",
        "n_implicit_hydrogens",
        "n_explicit_hydrogens",
        "allows_implicit_hydrogens",
        "atom_stereochemistry",
    )
    values = msm.get(
        reference,
        element="atom",
        output_type="dictionary",
        **dict.fromkeys(fields, True),
    )
    reordered = {}
    for field, column in values.items():
        if msm.pyunitwizard.is_quantity(column):
            column = msm.pyunitwizard.get_value(column, to_unit="elementary_charge")
        column = np.asarray(column)[inverse]
        reordered[field] = column.tolist()
        msm.set(template, element="atom", **{field: column})
    pairs = msm.get(template, element="bond", bonded_atom_pairs=True)
    msm.set(
        template,
        element="bond",
        bond_is_aromatic=[aromatic_by_pair[tuple(pair)] for pair in pairs],
    )
    for index, name in enumerate(names):
        ccd_row = heavy[index]
        if reordered["formal_charge"][index] != int(atoms.getValue("charge", ccd_row)):
            raise ValueError(f"Canonical descriptor/CCD charge disagreement: {name}")
        if reordered["atom_is_aromatic"][index] != (
            atoms.getValue("pdbx_aromatic_flag", ccd_row) == "Y"
        ):
            raise ValueError(
                f"Canonical descriptor/CCD aromaticity disagreement: {name}"
            )
        if reordered["n_unpaired_electrons"][index] != 0:
            raise ValueError(f"Unexpected radical in the pinned EST control: {name}")
        count = int(reordered["n_implicit_hydrogens"][index]) + int(
            reordered["n_explicit_hydrogens"][index]
        )
        if count != hydrogen_counts[name]:
            raise ValueError(f"Canonical descriptor/CCD hydrogen disagreement: {name}")
    if sum(hydrogen_counts.values()) != 24:
        raise ValueError("The pinned EST inventory must retain 24 virtual H atoms.")
    # Complete coverage is a fixture declaration backed by the exhaustive graph
    # and independent descriptor/inventory checks, not a generic repair rule.
    payload = msm.convert(
        template.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    ).to_dict()
    payload["states"][0]["connectivity_completeness"] = "complete"
    template.chemical_states = msm.convert(
        msm.ChemicalStatesDict(payload), to_form="molsysmt.ChemicalStates"
    )
    source = msm.convert(str(entry), to_form="molsysmt.MolSys")
    source_indices = list(msm.select(source, selection=SELECTION))
    ligand = msm.extract(source, selection=SELECTION)
    source_names = list(msm.get(ligand, element="atom", atom_name=True))
    source_by_name = {name: i for i, name in enumerate(source_names)}
    if len(source_by_name) != 20 or set(source_by_name) != set(names):
        raise ValueError(
            "The deposited ligand must contain the same 20 named heavy atoms."
        )
    correspondence = [[i, source_by_name[name]] for i, name in enumerate(names)]
    provenance = dict(
        identity="CCD EST heavy graph with CACTVS canonical stereo",
        version="2011-06-04",
        source_uri="https://files.rcsb.org/ligands/download/EST.cif",
        checksum=CCD_SHA256,
        hydrogen_policy="stored_counts",
        descriptor_provider="CACTVS",
        descriptor_version=descriptors.getValue("program_version", rows[0]),
        stereo_source="SMILES_CANONICAL",
        curation_software={"molsysmt": msm.__version__, "rdkit": rdBase.rdkitVersion},
        coordinate_policy="preserve_deposited_pose",
    )
    result = msm.physchem.apply_chemical_template(
        ligand,
        template=template,
        atom_correspondence=correspondence,
        template_provenance=provenance,
    )
    prepared = result["molecular_system"]
    declared = msm.physchem.get_cip_stereochemistry(prepared)
    observed = msm.physchem.get_cip_stereochemistry(
        prepared, structure_indices=[0], from_coordinates=True
    )
    np.testing.assert_equal(
        declared["atom_stereochemistry"], observed["atom_stereochemistry"]
    )
    expected_stereo = dict(zip(names, declared["atom_stereochemistry"].tolist()))
    if {name: value for name, value in expected_stereo.items() if value} != {
        "C8": "R",
        "C9": "S",
        "C13": "S",
        "C14": "S",
        "C17": "S",
    }:
        raise ValueError("Unexpected pinned EST stereo control.")
    stereo_disagreements = {}
    for row in heavy:
        name = atoms.getValue("atom_id", row)
        flag = atoms.getValue("pdbx_stereo_config", row)
        if flag in {"R", "S"} and flag != expected_stereo[name]:
            stereo_disagreements[name] = {
                "ccd_atom_flag": flag,
                "canonical_and_pose_cip": expected_stereo[name],
            }
    if stereo_disagreements != {
        "C8": {"ccd_atom_flag": "S", "canonical_and_pose_cip": "R"}
    }:
        raise ValueError("Unexpected CCD atom-flag/canonical-stereo disagreement.")
    output.mkdir(parents=True, exist_ok=True)
    (output / "1qku.cif.gz").write_bytes(gzip.compress(entry_bytes, mtime=0))
    (output / "EST.cif").write_bytes(ccd.read_bytes())
    msm.convert(
        template,
        to_form="file:h5msm",
        output_filename=str(output / "est_template.h5msm"),
    )
    manifest = dict(
        schema="molsysmt.est_template_fixture@1",
        source_selection=SELECTION,
        source_atom_indices=source_indices,
        source_atom_names=source_names,
        source_sha256=SOURCE_SHA256,
        ccd_sha256=CCD_SHA256,
        source_uri="https://files.rcsb.org/download/1QKU.cif",
        source_revision="1.4 (2024-05-08)",
        atom_correspondence=correspondence,
        template_provenance=provenance,
        expected_stereo=expected_stereo,
        ccd_stereo_disagreements=stereo_disagreements,
        expected_hydrogen_counts=[hydrogen_counts[name] for name in names],
        limits=[
            "No observed explicit H atoms or donor-H geometry.",
            "No protonation choice, coordinate optimization or biological pharmacophore validation.",
            "Canonical SMILES stereo selected explicitly; CCD atom flags are not substituted.",
        ],
    )
    manifest["artifact_sha256"] = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in (
            output / "1qku.cif.gz",
            output / "EST.cif",
            output / "est_template.h5msm",
        )
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(
        "Curated pinned EST fixture: 20 heavy atoms, 23 bonds, 24 stored H counts, five matching stereo centers."
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entry", required=True, type=Path)
    parser.add_argument("--ccd", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    curate(args.entry, args.ccd, args.output)


if __name__ == "__main__":
    main()
