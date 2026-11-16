"""Receive #763 originals explicitly, without network or default-suite skips.

Set MOLSYS_MT_763_ORIGINALS to the directory containing the unchanged public
3WU2.cif.gz and 5XNL.cif.gz files from the committed manifest, then select this
module explicitly with pytest. Ordinary unit tests use independent tiny data.
"""

import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm

ROOT = Path(__file__).resolve().parents[3]


@pytest.mark.parametrize(
    "profile", ["default", "declared", "pm-fs-default", "pm-fs-declared"]
)
@pytest.mark.parametrize("entry", ["3WU2", "5XNL"])
def test_original_entry_identity_and_coordinates(entry, profile):
    directory = os.environ.get("MOLSYS_MT_763_ORIGINALS")
    assert directory, "Supply the exact original files through MOLSYS_MT_763_ORIGINALS"
    manifest = json.loads(
        (ROOT / "devtools/data/mmcif_entity_identity_763_manifest.json").read_text()
    )
    declared = next(row for row in manifest["files"] if row["entry"] == entry)
    path = Path(directory) / f"{entry}.cif.gz"
    original = path.read_bytes()
    assert len(original) == declared["encoded_bytes"]
    assert hashlib.sha256(original).hexdigest() == declared["sha256"]
    source = msm.convert(path, to_form="mmcif.PdbxContainers.DataContainer")
    category = source.getObj("atom_site")
    columns = {name: i for i, name in enumerate(category.getAttributeList())}
    atoms_by_id = {str(row[columns["id"]]): row for row in category.getRowList()}
    assert len(atoms_by_id) == category.getRowCount()
    entities = source.getObj("entity")
    entity_columns = {name: i for i, name in enumerate(entities.getAttributeList())}
    names = {
        str(row[entity_columns["id"]]): row[entity_columns["pdbx_description"]]
        for row in entities.getRowList()
    }
    units = (
        ["pm", "fs", "degrees"]
        if profile.startswith("pm-fs")
        else ["nm", "ps", "radians"]
    )
    options = {"get_missing_bonds": False} if profile.endswith("declared") else {}
    with msm.pyunitwizard.context(standard_units=units):
        result = msm.convert(path, to_form="molsysmt.MolSys", **options)
        assert result.structures.n_structures == 1
        ids = result.topology.atoms.atom_id.tolist()
        assert len(ids) == len(set(ids))
        expected_rows = [atoms_by_id[atom_id] for atom_id in ids]
        expected_entities = [
            str(row[columns["label_entity_id"]]) for row in expected_rows
        ]
        assert (
            list(msm.get(result, element="atom", entity_id=True)) == expected_entities
        )
        assert list(msm.get(result, element="atom", entity_name=True)) == [
            names[entity] for entity in expected_entities
        ]
        assert list(msm.get(result, element="atom", chain_id=True)) == [
            row[columns["label_asym_id"]] for row in expected_rows
        ]
        assert len(result.topology.entities) == len(set(expected_entities))
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(
                result.structures.coordinates, to_unit="angstrom"
            )[0],
            [
                [
                    float(row[columns[axis]])
                    for axis in ["Cartn_x", "Cartn_y", "Cartn_z"]
                ]
                for row in expected_rows
            ],
            rtol=1e-12,
            atol=1e-10,
        )

        # Independently join deposited labels on the retained source rows. This
        # oracle does not use the converter's endpoint resolver or native IDs
        # reconstructed from a chemical graph.
        def normalized(value):
            return "" if value in {None, "", ".", "?"} else str(value)

        retained = {
            (
                str(row[columns["label_asym_id"]]),
                str(row[columns["auth_seq_id"]]),
                normalized(row[columns["pdbx_PDB_ins_code"]]),
                str(row[columns["label_atom_id"]]),
            ): index
            for index, row in enumerate(expected_rows)
        }
        bonds = result.chemical_states.get_bonds()
        evidence = {
            tuple(sorted((int(row.atom1_index), int(row.atom2_index)))): row.evidence
            for row in bonds.itertuples()
        }
        covalent_count = 0
        if source.exists("struct_conn"):
            links = source.getObj("struct_conn")
            fields = {name: i for i, name in enumerate(links.getAttributeList())}
            for row in links.getRowList():
                if row[fields["conn_type_id"]] != "covale":
                    continue
                keys = [
                    (
                        str(row[fields[f"ptnr{partner}_label_asym_id"]]),
                        str(row[fields[f"ptnr{partner}_auth_seq_id"]]),
                        normalized(row[fields[f"pdbx_ptnr{partner}_PDB_ins_code"]]),
                        str(row[fields[f"ptnr{partner}_label_atom_id"]]),
                    )
                    for partner in (1, 2)
                ]
                expected_pair = tuple(sorted(retained[key] for key in keys))
                assert evidence[expected_pair] == "explicit"
                covalent_count += 1
        if entry == "3WU2":
            assert covalent_count > 0
        if "declared" in profile:
            assert msm.get(result, connectivity_completeness=True) == "partial"
    assert path.read_bytes() == original
