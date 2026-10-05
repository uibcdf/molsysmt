"""Qualifying consumer APIs on the declared, bounded 1QKU/EST provider scenario.

Run each consumer in a separate process against an explicitly selected checkout.
This is an offline scenario driver, not a general receptor-preparation operation.
"""

import argparse
import gzip
import hashlib
import importlib
import importlib.metadata as metadata
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "tests/physchem/data/chemical_templates"


def _counts(msm, molecular_system):
    return msm.get(
        molecular_system,
        n_atoms=True,
        n_bonds=True,
        n_structures=True,
        output_type="dictionary",
    )


def _assert_history_equal(before, after):
    """Compare historical typed values, including unknown numerical entries."""
    if isinstance(before, np.ndarray):
        assert isinstance(after, np.ndarray) and before.dtype == after.dtype
        np.testing.assert_array_equal(before, after)
    elif isinstance(before, dict):
        assert before.keys() == after.keys()
        for key in before:
            _assert_history_equal(before[key], after[key])
    elif isinstance(before, (tuple, list)):
        assert len(before) == len(after)
        for left, right in zip(before, after):
            _assert_history_equal(left, right)
    else:
        assert before == after


def _prepare(msm, artifacts):
    manifest = json.loads((DATA / "manifest.json").read_text())
    raw = gzip.decompress((DATA / "1qku.cif.gz").read_bytes())
    if hashlib.sha256(raw).hexdigest() != manifest["source_sha256"]:
        raise ValueError("The observed input no longer matches the qualified source.")
    source_path = artifacts / "observed-source.cif"
    source_path.write_bytes(raw)
    molecular_system = msm.convert(source_path, to_form="molsysmt.MolSys")
    original_xyz = msm.pyunitwizard.get_value(
        msm.get(molecular_system, coordinates=True), to_unit="nm"
    ).copy()
    receptor_indices = msm.select(
        molecular_system,
        selection='molecule_type == "protein" and chain_id == "A" '
        'and group_id not in ["301", "302", "303"]',
    )
    receptor = msm.extract(molecular_system, selection=receptor_indices)
    names = msm.get(receptor, element="group", group_name=True)
    definition = msm.physchem.get_peptide_chemical_template(
        ["HIE" if name == "HIS" else name for name in names],
        n_terminal_state="ammonium",
        c_terminal_state="carboxylate",
    )
    template = definition["template"]
    # This inspected correspondence is specific to the pinned observed case.
    lookup = {
        (int(row.group_index), row.atom_name): int(index)
        for index, row in receptor.topology.atoms.iterrows()
    }
    correspondence = []
    for index, row in template.topology.atoms.iterrows():
        name = row.atom_name
        if names[int(row.group_index)] == "ARG" and name in {"NH1", "NH2"}:
            name = "NH2" if name == "NH1" else "NH1"
        correspondence.append([int(index), lookup[(int(row.group_index), name)]])
    normalized = msm.physchem.normalize_aromatic_bond_orders(receptor)
    prepared_receptor = msm.physchem.apply_chemical_template(
        normalized["molecular_system"],
        template=template,
        atom_correspondence=correspondence,
        template_provenance=definition["template_provenance"],
    )["molecular_system"]
    prepared_receptor.chemical_states.append_preparation_history(
        template.chemical_states.get_preparation_history()
    )
    ligand = msm.extract(molecular_system, selection=manifest["source_selection"])
    prepared_ligand = msm.physchem.apply_chemical_template(
        ligand,
        template=DATA / "est_template.h5msm",
        atom_correspondence=manifest["atom_correspondence"],
        template_provenance=manifest["template_provenance"],
    )["molecular_system"]
    hydrogenated = []
    atom_sources = []
    for item, indices in (
        (prepared_receptor, receptor_indices),
        (prepared_ligand, manifest["source_atom_indices"]),
    ):
        output = msm.build.add_missing_hydrogens(
            item,
            mode="fixed_chemical_state",
            pH=None,
            engine="RDKit",
            attribute_policy="intersection",
            return_report=True,
        )
        hydrogenated.append(output["molecular_system"])
        atom_sources.append(
            np.r_[indices, np.full(output["report"]["n_added_hydrogens"], -1)]
        )
    interface = msm.merge(hydrogenated, to_form="molsysmt.MolSys")
    source_indices = np.concatenate(atom_sources).astype(np.int64)
    observed = np.flatnonzero(source_indices >= 0)
    xyz = msm.pyunitwizard.get_value(msm.get(interface, coordinates=True), to_unit="nm")
    np.testing.assert_array_equal(
        xyz[:, observed], original_xyz[:, source_indices[observed]]
    )
    np.testing.assert_array_equal(
        interface.topology.atoms.atom_id.iloc[observed],
        molecular_system.topology.atoms.atom_id.iloc[source_indices[observed]],
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(
            msm.get(molecular_system, coordinates=True), to_unit="nm"
        ),
        original_xyz,
    )
    assert not msm.has_attribute(molecular_system, "formal_charge")
    assert _counts(msm, interface) == dict(n_atoms=4047, n_bonds=4088, n_structures=1)
    receptor_atoms = np.arange(hydrogenated[0].get_n_atoms(), dtype=np.int64)
    ligand_atoms = np.arange(
        len(receptor_atoms), interface.get_n_atoms(), dtype=np.int64
    )
    detectors = {
        "hydrophobic": (msm.interactions.hydrophobic.get_hydrophobic_interactions, {}),
        "hbonds": (
            msm.interactions.hbonds.get_hbonds,
            dict(
                method="donor_acceptor_distance_angle", profile="smarts_donor_acceptor"
            ),
        ),
        "pi_pi": (
            msm.interactions.pi_pi.get_pi_pi_interactions,
            dict(method="plane_angle_intersection", profile="smarts_5_6"),
        ),
    }
    analyses = {}
    for name, (detector, options) in detectors.items():
        result = detector(
            interface,
            selection=receptor_atoms,
            selection_2=ligand_atoms,
            selection_mode="between",
            structure_indices=[0, 0],
            pbc=False,
            **options,
        )
        assert result.evaluated_structure_indices.tolist() == [0]
        payload = msm.convert(result, to_form="molsysmt.InteractionsDict")
        payload.data["atom_source_indices"] = source_indices.copy()
        payload.data["source_n_atoms"] = molecular_system.get_n_atoms()
        payload.data["source_id"] = "rcsb:1QKU:deposited-atom-order"
        analyses[name] = msm.convert(payload, to_form="molsysmt.Interactions")
    interface.interactions = analyses
    path = artifacts / "prepared-interface.h5msm"
    msm.convert(interface, to_form=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys")
    observations = {}
    for name, analysis in restored.interactions.items():
        assert analysis.evaluated_structure_indices.tolist() == [0]
        np.testing.assert_array_equal(analysis.atom_source_indices, source_indices)
        observations[name] = analysis.query(structure_indices=[0, 0]).n_interactions
        assert observations[name] == interface.interactions[name].n_interactions
    assert observations == dict(hydrophobic=12, hbonds=0, pi_pi=0)
    history = restored.chemical_states.get_preparation_history()
    _assert_history_equal(interface.chemical_states.get_preparation_history(), history)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(msm.get(restored, coordinates=True), to_unit="nm"),
        xyz,
    )
    receptor_report = dict(
        source_sha256=manifest["source_sha256"],
        source_counts=_counts(msm, molecular_system),
        analysis_counts=_counts(msm, restored),
        receptor_heavy_atoms=1975,
        ligand_heavy_atoms=20,
        generated_hydrogens=2052,
        observed_identity_and_coordinates_preserved=True,
        original_source_unchanged=True,
        excluded_source_group_ids=["301", "302", "303"],
        reference_declaration=definition["template_provenance"],
        model="explicit_closed_fragment_304_550_plus_EST",
        geometry_evidence="observed_heavy_atoms_and_generated_local_H",
        environmental_refinement="not_performed",
        full_receptor_acceptance=False,
        observations=observations,
        history_schemas=[record["report"]["schema"] for record in history],
        h5msm_recovered=True,
    )
    return restored, receptor_atoms, ligand_atoms, receptor_report


def qualify(consumer, artifacts):
    import argdigest

    import molsysmt as msm

    with msm.pyunitwizard.context(standard_units=["pm", "fs", "coulomb"]):
        molecular_system, receptor, ligand, report = _prepare(msm, artifacts)
        if consumer == "pharmacophoremt":
            import pharmacophoremt as phmt

            features = phmt.modeler.get_features(molecular_system, selection=ligand)
            report["consumer_features"] = dict(
                Counter(item["kind"] for item in features["features"])
            )
            assert report["consumer_features"] == {
                "hydrophobicity": 9,
                "hb donor": 2,
                "hb acceptor": 2,
                "aromatic ring": 1,
            }
            inventory = phmt.modeler.get_features(molecular_system, selection=receptor)
            report["receptor_features"] = dict(
                Counter(item["kind"] for item in inventory["features"])
            )
            query = phmt.modeler.from_interactions(
                molecular_system,
                molecular_system.interactions["hydrophobic"],
                ligand,
                radius="0.15 nm",
                name="bounded_observed_interface",
            )
            report["interaction_query_sites"] = len(query.interaction_sites)
            assert report["interaction_query_sites"] == 6
        else:
            import dockingmt as dmt

            partner = dmt.prepare_receptor(molecular_system, selection=receptor)
            probe = dmt.prepare_ligand(
                molecular_system,
                selection=ligand,
                charge_options={"method": "gasteiger_marsili"},
            )
            report["consumer_preparation"] = dict(
                receptor_pdbqt_atoms=partner.n_atoms,
                ligand_pdbqt_atoms=probe.n_atoms,
                receptor_charge_source=partner.metadata["charge_source"],
                ligand_charge_source=probe.metadata["charge_source"],
                ligand_charge_method=probe.metadata["partial_charge_assignment"][
                    "method"
                ],
                receptor_assessment=dmt.assess_preparation(partner),
                ligand_assessment=dmt.assess_preparation(probe),
                ligand_charge_audit=dmt.audit_preparation_charges(probe),
            )
            assert (
                report["consumer_preparation"]["ligand_charge_audit"]["assessment"]
                == "consistent"
            )
            assert (
                report["consumer_preparation"]["receptor_assessment"]["assessment"]
                == "provisional"
            )
            assert probe.n_atoms == 22  # Twenty heavy atoms and two polar H.
            assert (
                report["consumer_preparation"]["ligand_charge_method"]
                == "gasteiger_marsili"
            )
    report["consumer"] = consumer
    report["producer"] = dict(
        molsysmt=msm.__version__,
        python=sys.version.split()[0],
        provider_source_head=subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip(),
        argdigest_runtime=dict(
            version=argdigest.__version__,
            decorator_sha256=hashlib.sha256(
                (Path(argdigest.__file__).parent / "core/decorator.py").read_bytes()
            ).hexdigest(),
        ),
        dependencies={
            name: metadata.version(name)
            for name in (
                "argdigest",
                "rdkit",
                "numpy",
                "pandas",
                "pyunitwizard",
                "smonitor",
                "depdigest",
            )
        },
    )
    report["scope"] = "local_source_contract_qualification"
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--consumer", choices=["dockingmt", "pharmacophoremt"], required=True
    )
    parser.add_argument("--consumer-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--artifacts", type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.consumer_root.resolve()))
    importlib.invalidate_caches()
    args.artifacts.mkdir(parents=True, exist_ok=True)
    result = qualify(args.consumer, args.artifacts)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(f"PASS {args.consumer}: prepared interface, public consumer API and H5MSM")


if __name__ == "__main__":
    main()
