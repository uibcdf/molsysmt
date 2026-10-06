"""Create small public H5MSM 0.5 fixtures for MolSysViewer contract review.

Run from the MolSysMT repository root::

    python devtools/scripts/create_molsysviewer_interactions_fixture.py /tmp/msm-viewer-review

The observations are synthetic API examples, not scientific detections.
Existing output files are never overwritten.
"""

import argparse
from pathlib import Path

import numpy as np

import molsysmt as msm
from molsysmt.native import MolSys, Structures


def _record(
    structure_index, interaction_type, participants, distance, evidence, images=None
):
    return {
        "structure_index": structure_index,
        "interaction_type": interaction_type,
        "participants": [
            {"role": role, "atom_indices": atoms} for role, atoms in participants
        ],
        "measurements": {"distance": distance},
        "evidence": evidence,
        "images": images if images is not None else [[0, 0, 0]] * len(participants),
    }


def make_analysis():
    """Build one typed analysis with the cases requested by MolSysViewer."""

    hydrogen_bond = [
        ("donor", [0]),
        ("hydrogen", [1]),
        ("acceptor", [2]),
    ]
    records = [
        _record(0, "hbond", hydrogen_bond, 0.20, "geometry"),
        _record(
            0,
            "pi_pi",
            [
                ("ring_a", [3, 4, 5]),
                ("ring_b", [6, 7, 8]),
            ],
            0.36,
            "geometry",
        ),
        _record(
            2,
            "disulfide_candidate",
            [
                ("sulfur", [9]),
                ("sulfur", [10]),
            ],
            0.19,
            "proximity",
        ),
        _record(
            4,
            "hbond",
            hydrogen_bond,
            0.21,
            "geometry",
            images=[[0, 0, 0], [0, 0, 0], [1, 0, 0]],
        ),
        _record(4, "hbond", hydrogen_bond, 0.22, "independent_observation"),
    ]
    return msm.Interactions.from_records(
        records,
        n_atoms=11,
        n_structures=6,
        evaluated_structure_indices=[0, 1, 2, 4],
        method="synthetic_viewer_review",
        measure_units={"distance": "nm"},
        source_id="molsysviewer_contract_fixture",
        atom_source_indices=[11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        structure_source_indices=[8, 6, 4, 2, 0, -1],
        source_n_atoms=12,
        source_n_structures=9,
        software={"molsysmt": msm.__version__},
        execution_records=[
            {
                "structure_indices": [0, 1, 2],
                "details": {
                    "data_kind": "synthetic_fixture",
                    "execution": "chunked",
                    "execution_chunks": 2,
                },
            },
            {
                "structure_indices": [4],
                "details": {
                    "data_kind": "synthetic_fixture",
                    "execution": "eager",
                    "execution_chunks": 1,
                },
            },
        ],
    )


def make_lifecycle_analyses():
    """Build named synthetic snapshots for execution and edit review."""
    original = make_analysis()
    metadata = {
        name: getattr(original, name)
        for name in (
            "n_atoms",
            "n_structures",
            "method",
            "measure_units",
            "parameters",
            "source_id",
            "atom_source_indices",
            "structure_source_indices",
            "source_n_atoms",
            "source_n_structures",
            "software",
        )
    }
    participants = [("donor", [0]), ("hydrogen", [1]), ("acceptor", [2])]
    fresh = msm.Interactions.from_records(
        [
            _record(
                4,
                "hbond",
                participants,
                0.23,
                "geometry",
                images=[[0, 0, 0], [0, 0, 0], [1, 0, 0]],
            ),
            _record(4, "hbond", participants, 0.24, "independent_observation"),
        ],
        **metadata,
        evaluated_structure_indices=[1, 4],
        execution={
            "data_kind": "synthetic_fixture",
            "execution": "chunked",
            "execution_chunks": 3,
        },
    )
    invalidated = original.invalidate_structures([4])
    recalculated = invalidated.replace_structures(fresh)
    empty = msm.Interactions.from_records(
        [],
        **metadata,
        evaluated_structure_indices=[1, 5],
        execution={
            "data_kind": "synthetic_fixture",
            "execution": "eager",
            "execution_chunks": 1,
        },
    )
    return {
        "review": original,
        "invalidated": invalidated,
        "recalculated": recalculated,
        "compacted": recalculated.compact(),
        "empty": empty,
    }


def create_files(output_directory):
    """Write and verify one complete and one interaction-only H5MSM file."""

    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)
    full_file = output_directory / "molsysviewer_full.h5msm"
    analysis_file = output_directory / "molsysviewer_interactions_only.h5msm"
    for path in (full_file, analysis_file):
        if path.exists():
            raise FileExistsError(f"Refusing to overwrite {path}")

    analyses = make_lifecycle_analyses()
    analysis = analyses["review"]
    system = MolSys(n_atoms=analysis.n_atoms)
    system.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(
            np.zeros((analysis.n_structures, analysis.n_atoms, 3)), "nm"
        ),
        box=msm.pyunitwizard.quantity(
            np.repeat(np.eye(3)[None], analysis.n_structures, axis=0), "nm"
        ),
    )
    system.interactions = analyses

    msm.h5msm.write(system, str(full_file))
    msm.h5msm.write_layers(str(analysis_file), interactions=analyses)
    for path in (full_file, analysis_file):
        loaded = msm.h5msm.read(str(path))
        assert set(loaded.interactions) == set(analyses)
        for name, expected in analyses.items():
            observed = loaded.interactions[name]
            assert observed.software == expected.software
            assert [
                (record["structure_indices"].tolist(), record["details"])
                for record in observed.execution_records
            ] == [
                (record["structure_indices"].tolist(), record["details"])
                for record in expected.execution_records
            ]
            actual, wanted = observed.query().to_dict(), expected.query().to_dict()
            for column in (
                "occurrence_indices",
                "structure_indices",
                "relation_indices",
                "image_offsets",
                "image_vectors",
            ):
                np.testing.assert_array_equal(actual[column], wanted[column])
            np.testing.assert_allclose(
                actual["measurements"]["distance"], wanted["measurements"]["distance"]
            )
        result = loaded.interactions["review"]
        selected = result.query(structure_indices=[4, 1, 0, 4, 3]).to_dict()
        np.testing.assert_array_equal(selected["structure_indices"], [4, 4, 0, 0])
        np.testing.assert_array_equal(
            selected["evaluated_structure_indices"], [4, 1, 0]
        )
        assert result.query(structure_indices=[1]).n_interactions == 0
        assert (
            result.query(structure_indices=[3])
            .to_dict()["evaluated_structure_indices"]
            .size
            == 0
        )
        assert result.query(atom_indices=[0], mode="involving_selection").n_interactions == 3
        assert result.between_selections([3, 4, 5], [6, 7, 8], exclusive=True).n_interactions == 1
        assert result.measure_units == {"distance": "nm"}
        np.testing.assert_array_equal(
            result.atom_source_indices,
            [
                11,
                10,
                9,
                8,
                7,
                6,
                5,
                4,
                3,
                2,
                1,
            ],
        )
        if path == analysis_file:
            assert loaded.topology is None
            assert loaded.structures is None
            subset = loaded.extract(atom_indices=[2, 0, 1], structure_indices=[4, 1, 0])
            assert (
                subset.interactions["review"]
                .query(structure_indices=[0])
                .n_interactions
                == 2
            )
    return full_file, analysis_file


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    args = parser.parse_args()
    for path in create_files(args.output_directory):
        print(path)


if __name__ == "__main__":
    main()
