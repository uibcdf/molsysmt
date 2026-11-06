"""Checking declared cap references against literal atoms and amide edges."""

import builtins
from copy import deepcopy
from hashlib import sha256
from importlib.resources import files

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw

CAPS = [
    (
        "ACE",
        ["CH3", "C", "O", "HH31"],
        ["C", "C", "O", "H"],
        [[0, 1], [1, 2]],
        [[0, 3]],
    ),
    (
        "NME",
        ["N", "CH3", "H", "HH31"],
        ["N", "C", "H", "H"],
        [[0, 1]],
        [[0, 2], [1, 3]],
    ),
    ("NME", ["N", "C", "H", "H1"], ["N", "C", "H", "H"], [[0, 1]], [[0, 2], [1, 3]]),
    ("NHE", ["N", "H1", "H2"], ["N", "H", "H"], [], [[0, 1], [0, 2]]),
    ("NH2", ["N", "H1", "H2"], ["N", "H", "H"], [], [[0, 1], [0, 2]]),
]


def _source(groups, *, scheme="amber", n_structures=1):
    builder = msm.MolSysBuilder()
    for name, names, elements in groups:
        atoms = [
            builder.add_atom(atom_name=atom, atom_type=element)
            for atom, element in zip(names, elements)
        ]
        builder.add_group(atoms, group_name=name)
    n_atoms = sum(len(names) for _, names, _ in groups)
    if n_structures:
        builder.set_coordinates(
            puw.quantity(np.zeros((n_structures, n_atoms, 3)), "nm")
        )
    source = builder.build()
    if scheme is not None:
        source.topology.set_group_naming_schemes(scheme)
    return source


def _capped_chain(*, scheme="amber", n_structures=1):
    source = _source(
        [
            ("ACE", ["CH3", "C", "O"], ["C", "C", "O"]),
            ("ALA", ["N", "CA", "C", "O", "CB"], ["N", "C", "C", "O", "C"]),
            ("NME", ["N", "CH3"], ["N", "C"]),
        ],
        scheme=scheme,
        n_structures=n_structures,
    )
    if n_structures:
        coordinates = np.asarray(
            [
                [-0.15, 0, 0],
                [0, 0, 0],
                [0, 0.12, 0],
                [0.133, 0, 0],
                [0.27, 0, 0],
                [0.4, 0, 0],
                [0.4, 0.12, 0],
                [0.27, -0.15, 0],
                [0.533, 0, 0],
                [0.68, 0, 0],
            ]
        )
        source.structures.coordinates = puw.quantity(
            np.repeat(coordinates[None], n_structures, axis=0), "nm"
        )
    return source


@pytest.mark.parametrize("name,names,elements,heavy,hydrogens", CAPS)
@pytest.mark.parametrize("scheme", ["amber", "legacy"])
def test_exact_cap_heavy_and_hydrogen_pairs_reuse_the_declared_catalogue(
    name, names, elements, heavy, hydrogens, scheme
):
    source = _source([(name, names, elements)], scheme=scheme)
    heavy_report = msm.build.get_covalent_bond_candidates(source)
    h_report = msm.build.get_covalent_bond_candidates(
        source, method="observed_hydrogen_template_consensus"
    )
    assert heavy_report["bonded_atom_pairs"].tolist() == heavy
    assert h_report["bonded_atom_pairs"].tolist() == hydrogens
    assert heavy_report["rule_version"] == h_report["rule_version"] == 2
    assert heavy_report["coverage"]["rule_version"] == 2
    template = heavy_report["groups"][0]["template"]
    assert template["family"] == "terminal_capping"
    assert template["backbone_roles"] == (["C"] if name == "ACE" else ["N"])
    assert template["naming_scheme"] == scheme
    package, basename = template["resource"].rsplit("/", 1)
    assert (
        template["provenance"]["packaged_sha256"]
        == sha256(files(package).joinpath(basename).read_bytes()).hexdigest()
    )
    assert heavy_report["bonded_atom_pairs"].dtype == np.int64
    assert h_report["missing_mask"].tolist() == [True] * len(hydrogens)
    assert source.chemical_states.get(n_bonds=True) == 0


@pytest.mark.parametrize("scheme", [None, "ccd", "sequence"])
def test_cap_labels_do_not_select_their_own_naming_context(scheme):
    source = _capped_chain(scheme=scheme)
    report = msm.build.get_covalent_bond_candidates(source)
    for group in (report["groups"][0], report["groups"][2]):
        assert group["status"] == "unassessed"
        assert group["template"] is None
        assert group["reason_codes"] == ["no_exact_group_template"]


def test_ambiguous_partial_nme_layout_is_not_selected_by_first_variant():
    source = _source([("NME", ["N", "H"], ["N", "H"])])
    report = msm.build.get_covalent_bond_candidates(
        source, method="observed_hydrogen_template_consensus"
    )
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert report["groups"][0]["status"] == "unassessed"
    assert report["groups"][0]["template"] is None


def test_missing_cap_atoms_have_only_the_supported_partial_pairs():
    source = _source([("ACE", ["C", "O"], ["C", "O"])])
    report = msm.build.get_covalent_bond_candidates(source)
    assert report["bonded_atom_pairs"].tolist() == [[0, 1]]
    assert report["groups"][0]["status"] == "partial"
    assert report["groups"][0]["blocked_by_missing_atom_name_pairs"] == [["C", "CH3"]]


@pytest.mark.parametrize(
    "names,elements,reason",
    [
        (["CH3", "C", "C", "O"], ["C", "C", "C", "O"], "ambiguous_atom_names"),
        (["CH3", "C", "O", "S"], ["C", "C", "O", "S"], "unexpected_heavy_atoms"),
        (["CH3", "C", "O"], ["C", "C", "N"], "heavy_element_conflict"),
    ],
)
def test_cap_conflicts_block_inference_instead_of_repairing_identity(
    names, elements, reason
):
    report = msm.build.get_covalent_bond_candidates(_source([("ACE", names, elements)]))
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert reason in report["groups"][0]["reason_codes"]


@pytest.mark.parametrize(
    "method", ["adjacent_backbone_distance", "unique_backbone_distance"]
)
def test_cap_amide_links_use_the_same_chain_and_geometry_guards(method):
    source = _capped_chain()
    with puw.context(standard_units=["pm", "ps"]):
        report = msm.build.get_peptide_bond_candidates(source, method=method)
    assert report["bonded_atom_pairs"].tolist() == [[1, 3], [5, 8]]
    assert report["group_pairs"].tolist() == [[0, 1], [1, 2]]
    np.testing.assert_allclose(
        puw.get_value(report["distances"], to_unit="nm"), [0.133, 0.133]
    )
    assert report["pbc_applied"] is False
    assert report["rule_version"] == 2
    assert "terminal_state_assignment" in report["unassessed_checks"]


@pytest.mark.parametrize("cap", ["NHE", "NH2"])
def test_amide_caps_with_no_methyl_atom_supply_the_declared_nitrogen(cap):
    source = _source(
        [
            ("ALA", ["N", "CA", "C", "O", "CB"], ["N", "C", "C", "O", "C"]),
            (cap, ["N", "H1", "H2"], ["N", "H", "H"]),
        ]
    )
    values = np.zeros((1, 8, 3))
    values[0, :5, 0] = [-0.27, -0.133, 0, 0, -0.133]
    values[0, 5:, 0] = [0.133, 0.14, 0.14]
    source.structures.coordinates = puw.quantity(values, "nm")
    report = msm.build.get_peptide_bond_candidates(
        source, method="unique_backbone_distance"
    )
    assert report["bonded_atom_pairs"].tolist() == [[2, 5]]
    assert report["group_pairs"].tolist() == [[0, 1]]


@pytest.mark.parametrize(
    "kind,order,eligible",
    [("covalent", 1, True), ("covalent", 2, False), ("dative", None, False)],
)
def test_cap_amide_candidates_respect_stored_edge_types_and_orders(
    kind, order, eligible
):
    source = _capped_chain()
    source.chemical_states.add_bonds([[1, 3]])
    msm.set(source, element="bond", bond_type=kind, bond_order=order)
    report = msm.build.get_peptide_bond_candidates(
        source, method="unique_backbone_distance"
    )
    pairs = report["bonded_atom_pairs"].tolist()
    assert ([1, 3] in pairs) is eligible
    if eligible:
        assert report["missing_mask"].tolist() == [False, True]
    else:
        assert any(
            "conflicting_stored_peptide_edge" in link["reason_codes"]
            for link in report["links"]
        )


def test_a_c_terminal_cap_methyl_is_not_an_outgoing_peptide_carbon():
    source = _source(
        [
            ("NME", ["N", "C"], ["N", "C"]),
            ("ALA", ["N", "CA", "C", "O", "CB"], ["N", "C", "C", "O", "C"]),
        ]
    )
    values = np.ones((1, 7, 3)) * 4
    values[0, 1] = [0, 0, 0]
    values[0, 2] = [0.133, 0, 0]
    source.structures.coordinates = puw.quantity(values, "nm")
    report = msm.build.get_peptide_bond_candidates(
        source, method="unique_backbone_distance"
    )
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert any(
        "unsupported_terminal_cap_direction" in link["reason_codes"]
        for link in report["links"]
    )


def test_cap_assembly_retains_all_structures_and_typed_state_history(tmp_path):
    source = _capped_chain(n_structures=3)
    source.chemical_states.append_state()
    msm.set(source, element="system", structure_chemical_state_index=[0, 1, None])
    before = source.topology.copy()
    coordinates = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    result = msm.build.infer_covalent_bonds(
        source, chemical_state="structure", structure_indices=1, return_report=True
    )
    output, report = result["molecular_system"], result["report"]
    expected = [[0, 1], [1, 2], [1, 3], [3, 4], [4, 5], [4, 7], [5, 6], [5, 8], [8, 9]]
    assert report["added_bonded_atom_pairs"].tolist() == expected
    assert output.chemical_states.get_bonds(chemical_state=0).empty
    assert output.structures.n_structures == 3
    np.testing.assert_array_equal(
        puw.get_value(output.structures.coordinates, to_unit="nm"), coordinates
    )
    for name in ("atoms", "groups", "molecules", "entities", "chains"):
        pd.testing.assert_frame_equal(
            getattr(source.topology, name), getattr(before, name)
        )
        pd.testing.assert_frame_equal(
            getattr(output.topology, name), getattr(before, name)
        )
    assert source.chemical_states.get_bonds(chemical_state=1).empty
    filename = str(tmp_path / "caps.h5msm")
    msm.convert(output, to_form=filename)
    loaded = msm.convert(filename)
    history = loaded.chemical_states.get_preparation_history(chemical_state=1)
    saved = history[0]["report"]
    assert saved["rule_version"] == 2
    assert saved["heavy_groups"][0]["template"]["family"] == "terminal_capping"
    assert saved["added_bonded_atom_pairs"].tolist() == expected
    assert saved["added_bonded_atom_pairs"].dtype == np.int64
    assert saved["peptide"]["group_pairs"].tolist() == [[0, 1], [1, 2]]
    detached = deepcopy(saved)
    detached["heavy_groups"][0]["template"]["provenance"].clear()
    assert loaded.chemical_states.get_preparation_history(chemical_state=1)[0][
        "report"
    ]["heavy_groups"][0]["template"]["provenance"]


def test_cap_template_hydrogens_do_not_use_the_protein_alias_dataset():
    source = _source([CAPS[0][:3]])
    report = msm.build.get_covalent_bond_candidates(
        source, method="observed_hydrogen_alias_consensus"
    )
    assert report["bonded_atom_pairs"].tolist() == [[0, 3]]
    assert report["hydrogen_name_policy"]["reference"] is None
    assert report["hydrogen_name_policy"]["references"] == []


@pytest.mark.parametrize(
    "selection,expected", [([3, 1, 3], [[1, 3]]), ([1], []), ([], [])]
)
def test_cap_amide_output_selection_retains_original_endpoint_indices(
    selection, expected
):
    report = msm.build.get_peptide_bond_candidates(
        _capped_chain(), selection=selection, method="unique_backbone_distance"
    )
    assert report["bonded_atom_pairs"].tolist() == expected
    assert report["bonded_atom_pairs"].shape == (len(expected), 2)


def test_unselected_competitor_blocks_a_cap_link_before_output_selection():
    source = _capped_chain()
    values = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    values[0, 1] = [0.402, 0, 0]
    source.structures.coordinates = puw.quantity(values, "nm")
    report = msm.build.get_peptide_bond_candidates(
        source, selection=[5, 8], method="unique_backbone_distance"
    )
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert "competing_backbone_partners" in report["links"][0]["reason_codes"]


@pytest.mark.parametrize(
    "pair,kind,order",
    [([0, 3], "covalent", 2), ([1, 3], "covalent", 1), ([0, 3], "dative", None)],
)
def test_conflicting_stored_cap_hydrogen_evidence_is_retained_and_blocks_addition(
    pair, kind, order
):
    source = _source([CAPS[0][:3]])
    source.chemical_states.add_bonds([pair])
    msm.set(source, element="bond", bond_type=kind, bond_order=order)
    before = source.chemical_states.get_bonds().copy(deep=True)
    report = msm.build.get_covalent_bond_candidates(
        source, method="observed_hydrogen_template_consensus"
    )
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert report["groups"][0]["hydrogen_coverage"]["issues"]
    pd.testing.assert_frame_equal(source.chemical_states.get_bonds(), before)


def test_cap_template_graph_requires_no_fabricated_coordinate_structure():
    result = msm.build.infer_covalent_bonds(
        _capped_chain(n_structures=0), return_report=True
    )
    report = result["report"]
    assert report["n_structures"] == 0
    assert report["structure_index"] is None
    assert report["peptide"]["bonded_atom_pairs"].shape == (0, 2)
    assert report["added_bonded_atom_pairs"].tolist() == [
        [0, 1],
        [1, 2],
        [3, 4],
        [4, 5],
        [4, 7],
        [5, 6],
        [8, 9],
    ]


def _cap_pdb(*, breaks=(), alternate=False):
    source = _capped_chain()
    coordinates = puw.get_value(source.structures.coordinates, to_unit="angstrom")[0]
    groups = source.topology.atoms["group_index"].tolist()
    names = source.topology.atoms["atom_name"].tolist()
    elements = msm.get(source, element="atom", atom_type=True)
    group_names = source.topology.groups["group_name"].tolist()
    lines = []
    serial = 0
    for index, (name, element, group, (x, y, z)) in enumerate(
        zip(names, elements, groups, coordinates)
    ):
        for label in ("A", "B") if alternate and index == 1 else (" ",):
            serial += 1
            lines.append(
                f"ATOM  {serial:5d} {name:^4}{label}{group_names[group]:3} A{group + 1:4d}    {x:8.3f}{y:8.3f}{z:8.3f}{1.0:6.2f}{0.0:6.2f}          {element:>2}  "
            )
        if group in breaks and (index == len(groups) - 1 or groups[index + 1] != group):
            lines.append("TER")
    return "\n".join([*lines, "END", ""])


@pytest.mark.parametrize(
    "breaks,expected", [((), [[1, 3], [5, 8]]), ((0,), [[5, 8]]), ((1,), [[1, 3]])]
)
def test_pdb_declared_cap_context_preserves_ter_segments_without_openmm(
    breaks, expected, monkeypatch
):
    original_import = builtins.__import__

    def block(name, *args, **kwargs):
        if name == "openmm" or name.startswith("openmm."):
            pytest.fail("Cap reference inference imported OpenMM")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", block)
    source = msm.convert(
        _cap_pdb(breaks=breaks), to_form="molsysmt.MolSys", get_missing_bonds=False
    )
    source.topology.set_group_naming_schemes("amber")
    report = msm.build.get_peptide_bond_candidates(
        source, method="unique_backbone_distance"
    )
    assert report["bonded_atom_pairs"].tolist() == expected
    assert source.chemical_states.get_bonds().empty


def test_alternate_cap_carbon_does_not_establish_unique_polymer_links():
    source = msm.convert(
        _cap_pdb(alternate=True), to_form="molsysmt.MolSys", get_missing_bonds=False
    )
    source.topology.set_group_naming_schemes("amber")
    report = msm.build.get_peptide_bond_candidates(
        source, method="unique_backbone_distance"
    )
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert report["discovery"]["blocked_chain_indices"].size == 1


def test_cap_reference_is_credited_as_data_in_each_capture():
    ackredit = pytest.importorskip("ackredit")
    source = _source([CAPS[0][:3]])
    with ackredit.session("terminal cap references"):
        for index in range(2):
            with ackredit.capture(str(index)) as capture:
                report = msm.build.get_covalent_bond_candidates(source)
            references = [
                item
                for item in capture.attribution.to_dict()["items"]
                if item["id"].startswith("dataset:molsysmt-terminal-cap-catalogue:")
            ]
            assert len(references) == 1
            assert references[0]["type"] == "dataset"
            assert references[0]["id"].endswith(
                report["groups"][0]["template"]["provenance"]["packaged_sha256"]
            )
