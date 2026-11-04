"""Keep source naming context and group positions during sequence comparison."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import MolSys, Structures, Topology


@pytest.fixture
def mixed():
    topology = Topology(n_atoms=5, n_groups=5, n_molecules=1, n_entities=1, n_chains=1)
    topology.atoms["group_index"] = pd.array(range(5), dtype="Int64")
    topology.atoms["chain_index"] = pd.array([0] * 5, dtype="Int64")
    topology.atoms["atom_id"] = [str(index) for index in range(5)]
    topology.groups["group_name"] = ["HOH", "GLH", "GLH", "HID", "LYN"]
    topology.groups["group_type"] = ["water"] + ["amino acid"] * 4
    topology.groups["group_id"] = [str(10 + index) for index in range(5)]
    topology.groups["molecule_index"] = pd.array([0] * 5, dtype="Int64")
    topology.molecules["entity_index"] = pd.array([0], dtype="Int64")
    topology.chains["chain_id"] = ["A"]
    topology.set_group_naming_schemes(["ccd", "amber", "legacy", "amber", "ccd"])
    return MolSys._from_partial_domains(
        topology=topology,
        structures=Structures(
            coordinates=msm.pyunitwizard.quantity(np.zeros((3, 5, 3)), "nm")
        ),
    )


@pytest.mark.parametrize(
    "form", ["system", "topology", "system_dict", "topology_dict", "file"]
)
def test_identity_reads_mixed_stored_profiles_without_parent_replacement(
    mixed, form, tmp_path
):
    names = mixed.topology.groups.group_name.tolist()
    if form == "topology":
        source = mixed.topology
    elif form in {"system_dict", "topology_dict"}:
        source = msm.convert(
            mixed,
            to_form="molsysmt.MolSysDict"
            if form == "system_dict"
            else "molsysmt.TopologyDict",
        )
    elif form == "file":
        source = msm.convert(mixed, to_form=str(tmp_path / "mixed.h5msm"))
    else:
        source = mixed
    assert msm.topology.get_sequence_identity(
        source, reference_molecular_system="EQHK"
    ) == (100.0, [1, 2, 3, 4], [0, 1, 2, 3])
    assert mixed.topology.groups.group_name.tolist() == names
    assert mixed.topology.group_naming_schemes == (
        "ccd",
        "amber",
        "legacy",
        "amber",
        "ccd",
    )


@pytest.mark.parametrize("selection", [[4, 1, 0, 2, 4], "group_index in [1,2,3,4]"])
def test_identity_keeps_independent_group_maps_and_predicates(mixed, selection):
    repeated = not isinstance(selection, str)
    reference = "KEQK" if repeated else "EQHK"
    assert msm.topology.get_sequence_identity(
        mixed, selection=selection, reference_molecular_system=reference
    ) == (100.0, [4, 1, 2, 4] if repeated else [1, 2, 3, 4], list(range(4)))


def test_complementary_native_inputs_read_context_from_the_name_owner(mixed):
    assert msm.topology.get_sequence_identity(
        [mixed.topology, mixed.structures], reference_molecular_system="EQHK"
    ) == (100.0, [1, 2, 3, 4], [0, 1, 2, 3])


def test_alignment_uses_the_same_native_projection(mixed):
    assert msm.topology.get_sequence_alignment(
        mixed, reference_molecular_system="EQHK"
    ) == ("EQHK", "EQHK")


@pytest.mark.parametrize(
    "operation", ["get_sequence_identity", "get_sequence_alignment"]
)
def test_unqualified_state_labels_fail_with_structured_context_diagnostic(
    mixed, operation
):
    mixed.topology.set_group_naming_schemes(None)
    with pytest.raises(msm.ArgumentError, match="context-dependent") as refusal:
        getattr(msm.topology, operation)(mixed, reference_molecular_system="EQHK")
    assert refusal.value.extra["argument"] == "naming_scheme"


@pytest.mark.parametrize(
    "operation", ["get_sequence_identity", "get_sequence_alignment"]
)
def test_nonpeptide_ccd_label_cannot_be_used_as_an_amino_acid(mixed, operation):
    mixed.topology.set_group_naming_schemes("ccd", group_indices=3)
    with pytest.raises(msm.ArgumentError, match="no supported amino-acid"):
        getattr(msm.topology, operation)(mixed, reference_molecular_system="EQHK")


def test_native_identity_copies_no_domain_and_leaves_coordinates_untouched(
    mixed, monkeypatch
):
    geometry = mixed.structures._coordinates

    def refuse(*args, **kwargs):
        raise AssertionError("Sequence identity must not copy a molecular domain.")

    for cls in (MolSys, Topology, Structures):
        monkeypatch.setattr(cls, "copy", refuse)
    assert msm.topology.get_sequence_identity(mixed) == (
        100.0,
        [1, 2, 3, 4],
        [1, 2, 3, 4],
    )
    assert mixed.structures._coordinates is geometry


def test_dictionary_identity_does_not_decode_unrelated_domains(mixed, monkeypatch):
    from molsysmt.form import _native_dict

    source = msm.convert(mixed, to_form="molsysmt.MolSysDict")

    def refuse(*args, **kwargs):
        raise AssertionError("A sequence query must only decode the topology payload.")

    monkeypatch.setattr(_native_dict, "decode_molsys", refuse)
    monkeypatch.setattr(_native_dict, "decode_structures", refuse)
    assert msm.topology.get_sequence_identity(source) == (
        100.0,
        [1, 2, 3, 4],
        [1, 2, 3, 4],
    )


def test_modular_h5msm_identity_reads_only_requested_topology_data(
    mixed, tmp_path, monkeypatch
):
    import h5py

    path = msm.convert(mixed, to_form=str(tmp_path / "topology-only-read.h5msm"))
    original = h5py.Dataset.__getitem__

    def checked(dataset, key):
        assert not dataset.name.startswith(
            ("/structures/", "/chemical_states/", "/interactions/")
        ), dataset.name
        return original(dataset, key)

    monkeypatch.setattr(h5py.Dataset, "__getitem__", checked)
    assert msm.topology.get_sequence_identity(path) == (
        100.0,
        [1, 2, 3, 4],
        [1, 2, 3, 4],
    )


@pytest.mark.parametrize("name", ["GLH", "HID", "HIE", "CYX", "XAA", "XLE"])
def test_three_letter_default_does_not_select_a_legacy_state_meaning(name):
    from molsysmt.form.string_amino_acids_3.to_string_amino_acids_1 import (
        to_string_amino_acids_1,
    )

    if name in {"XAA", "XLE"}:
        assert (
            to_string_amino_acids_1("amino_acids_3:" + name)
            == {"XAA": "X", "XLE": "J"}[name]
        )
    else:
        with pytest.raises(msm.ArgumentError, match="context-dependent"):
            to_string_amino_acids_1("amino_acids_3:" + name)


def test_three_letter_projection_has_explicit_profiles_and_no_legacy_fallback():
    from molsysmt.form.string_amino_acids_3.to_string_amino_acids_1 import (
        to_string_amino_acids_1,
    )

    assert to_string_amino_acids_1("GlhHidHie", from_naming_scheme="amber") == "EHH"
    assert to_string_amino_acids_1("Glh", from_naming_scheme="legacy") == "Q"
    assert to_string_amino_acids_1("amino_acids_3:AceMseSepTpoPtrNme") == "MSTY"
    with pytest.raises(msm.ArgumentError):
        to_string_amino_acids_1("Glh", from_naming_scheme="ccd")
    with pytest.raises(msm.ArgumentError):
        to_string_amino_acids_1("Xle", from_naming_scheme="ccd")


@pytest.mark.parametrize(
    "function_name", ["get_sequence_alignment", "get_sequence_identity"]
)
def test_biopython_dependency_is_checked_only_for_the_selected_engine(
    monkeypatch, function_name
):
    from depdigest import is_installed
    from depdigest.core import checker

    from molsysmt._private.smonitor import (
        LibraryNotFoundError,
        NotImplementedMethodError,
    )

    original = checker.find_spec

    def absent(name, *args, **kwargs):
        return None if name == "Bio" else original(name, *args, **kwargs)

    try:
        monkeypatch.setattr(checker, "find_spec", absent)
        is_installed.cache_clear()
        function = getattr(msm.topology, function_name)
        with pytest.raises(LibraryNotFoundError) as refusal:
            function("AG", reference_molecular_system="AG")
        assert refusal.value.extra["library"] == "biopython"
        with pytest.raises(NotImplementedMethodError):
            function("AG", reference_molecular_system="AG", engine="OpenMM")
    finally:
        monkeypatch.setattr(checker, "find_spec", original)
        is_installed.cache_clear()


def test_biopython_installation_hint_uses_the_distribution_name():
    from depdigest import get_info

    dependency = next(
        item
        for item in get_info("molsysmt", format="dict")["dependencies"]
        if item["library"] == "Bio"
    )
    assert dependency["package_name"] == {"pypi": "biopython", "conda": "biopython"}
    assert dependency["install"]["conda"] == "conda install -c conda-forge biopython"


def test_real_attribution_retains_mixed_reference_data_in_reused_captures(mixed):
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("mixed naming comparisons"):
        with ackredit.capture("first") as first:
            actual = msm.topology.get_sequence_identity(
                mixed, reference_molecular_system="EQHK"
            )
        with ackredit.capture("second") as second:
            assert (
                msm.topology.get_sequence_identity(
                    mixed, reference_molecular_system="EQHK"
                )
                == actual
            )
        first_ids = {item["id"] for item in first.attribution.to_dict()["items"]}
        second_ids = {item["id"] for item in second.attribution.to_dict()["items"]}
        assert first_ids == second_ids
        assert "ddbj-amino-acid-code-alphabet" in first_ids
        assert "rcsb-ccd-group-names-20261104" in first_ids
        assert any(name.startswith("molsysmt-group-names:amber:") for name in first_ids)
        assert any(
            name.startswith("molsysmt-group-names:legacy:") for name in first_ids
        )
        assert "ensembler-sequence-identity-reference" in first_ids
    mixed.topology.set_group_naming_schemes("ccd", group_indices=3)
    with ackredit.session("refused comparison"):
        with pytest.raises(msm.ArgumentError):
            msm.topology.get_sequence_identity(mixed, reference_molecular_system="EQHK")
        assert not ackredit.get_used_items()


def test_native_comparison_preserves_results_without_optional_attribution(
    mixed, monkeypatch
):
    from molsysmt import _ackredit
    from molsysmt._private.smonitor.warnings import AckreditTrackingWarning

    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    expected = msm.topology.get_sequence_identity(
        mixed, reference_molecular_system="EQHK"
    )

    def broken():
        raise RuntimeError("Attribution provider deliberately unavailable")

    monkeypatch.setattr(_ackredit, "backend", broken)
    with pytest.warns(AckreditTrackingWarning):
        actual = msm.topology.get_sequence_identity(
            mixed, reference_molecular_system="EQHK"
        )
    assert actual == expected


def test_alignment_credits_the_actual_executed_provider(mixed):
    from Bio import __version__ as version

    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("direct alignment"):
        with ackredit.capture("alignment") as run:
            assert msm.topology.get_sequence_alignment(
                mixed, reference_molecular_system="EQHK"
            ) == ("EQHK", "EQHK")
        items = {item["id"]: item for item in run.attribution.to_dict()["items"]}
        assert items[f"software:biopython:{version}"]["version"] == version


@pytest.mark.parametrize(
    "operation",
    ["scalar", "convert", "topology", "system", "text", "identity", "alignment"],
)
@pytest.mark.parametrize("flag", ["true", 1, np.bool_(True)])
def test_only_literal_boolean_can_control_the_public_validation_bypass(
    mixed, operation, flag
):
    from molsysmt.form.molsysmt_MolSys.to_string_amino_acids_1 import (
        to_string_amino_acids_1 as system_projection,
    )
    from molsysmt.form.molsysmt_Topology.to_string_amino_acids_1 import (
        to_string_amino_acids_1 as topology_projection,
    )
    from molsysmt.form.string_amino_acids_3.to_string_amino_acids_1 import (
        to_string_amino_acids_1 as text_projection,
    )

    cases = {
        "scalar": (msm.element.group.get_1_letter_code_from_name, ["ALA"], {}),
        "convert": (
            msm.convert,
            [mixed],
            {"to_form": "string:amino_acids_1", "group_indices": [1]},
        ),
        "topology": (topology_projection, [mixed.topology], {"group_indices": [1]}),
        "system": (system_projection, [mixed], {"group_indices": [1]}),
        "text": (text_projection, ["Ala"], {}),
        "identity": (
            msm.topology.get_sequence_identity,
            [mixed],
            {"reference_molecular_system": "EQHK"},
        ),
        "alignment": (
            msm.topology.get_sequence_alignment,
            [mixed],
            {"reference_molecular_system": "EQHK"},
        ),
    }
    function, arguments, options = cases[operation]
    with pytest.raises(msm.ArgumentError) as refusal:
        function(*arguments, **options, skip_digestion=flag)
    assert refusal.value.extra["argument"] == "skip_digestion"
