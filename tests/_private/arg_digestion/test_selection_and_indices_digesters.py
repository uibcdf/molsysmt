import numpy as np
import pytest

from molsysmt._private.smonitor import ArgumentError, ArgumentLengthError
from molsysmt._private.argdigest.argument.selection import digest_selection
from molsysmt._private.argdigest.argument.selection_2 import digest_selection_2
from molsysmt._private.argdigest.argument.mask import digest_mask
from molsysmt._private.argdigest.argument.atom_indices import digest_atom_indices
from molsysmt._private.argdigest.argument.group_indices import digest_group_indices
from molsysmt._private.argdigest.argument.chain_indices import digest_chain_indices
from molsysmt._private.argdigest.argument.molecule_indices import digest_molecule_indices
from molsysmt._private.argdigest.argument.entity_indices import digest_entity_indices
from molsysmt._private.argdigest.argument.component_indices import digest_component_indices
from molsysmt._private.argdigest.argument.structure_indices import digest_structure_indices
from molsysmt._private.argdigest.argument.selections import digest_selections


def test_selection_digesters_support_molsysmt_and_alternative_syntaxes():
    assert digest_selection("atom_index==0") == "atom_index==0"
    assert digest_selection(3) == [3]
    assert digest_selection(range(3)) == [0, 1, 2]
    assert digest_selection([0, 1, 2]) == [0, 1, 2]
    assert digest_selection([[0, 1], 2]) == [[0, 1], [2]]
    assert digest_selection(None) is None

    alt = digest_selection([0, 1], syntax="OpenMM")
    assert isinstance(alt, np.ndarray)
    assert alt.tolist() == [0, 1]

    alt_scalar = digest_selection(4, syntax="OpenMM")
    assert isinstance(alt_scalar, np.ndarray)
    assert alt_scalar.tolist() == [4]

    assert digest_selection_2("group_index==1") == "group_index==1"
    assert digest_selection_2([1, 3], syntax="MDTraj").tolist() == [1, 3]
    assert digest_selection_2(None) is None


def test_selection_digesters_reject_invalid_inputs():
    with pytest.raises(ArgumentError):
        digest_selection({"bad": "selection"})

    with pytest.raises(ArgumentError):
        digest_selection_2({"bad": "selection"})


def test_mask_digester_supports_selection_and_all_semantics():
    assert digest_mask(None) is None
    assert digest_mask("all") == "all"
    assert digest_mask(np.array([True, False])).tolist() == [True, False]
    assert digest_mask([0, 2], caller="molsysmt.basic.select.select") == [0, 2]
    assert digest_mask("atom_name=='CA'", caller="molsysmt.basic.get.get") == "atom_name=='CA'"

    with pytest.raises(ArgumentError):
        digest_mask(3.14)


@pytest.mark.parametrize(
    "digester",
    [
        atom_indices := digest_atom_indices,
        group_indices := digest_group_indices,
        chain_indices := digest_chain_indices,
        molecule_indices := digest_molecule_indices,
        entity_indices := digest_entity_indices,
        component_indices := digest_component_indices,
        structure_indices := digest_structure_indices,
    ],
)
def test_indices_digesters_support_none_all_scalars_and_arrays(digester):
    kwargs = {} if digester in {atom_indices, chain_indices, structure_indices} else {"caller": None}
    assert digester(None, **kwargs) is None
    assert digester("all", **kwargs) == "all"

    scalar = digester(2, **kwargs)
    assert isinstance(scalar, np.ndarray)
    assert scalar.tolist() == [2]

    array = digester([0, 1, 3], **kwargs)
    assert isinstance(array, np.ndarray)
    assert array.tolist() == [0, 1, 3]


def test_recursive_indices_digesters_support_nested_inputs_when_declared():
    nested_atoms = digest_atom_indices([[0, 1], [2, 3]])
    assert [item.tolist() for item in nested_atoms] == [[0, 1], [2, 3]]

    nested_chains = digest_chain_indices([[0, 1], [2]], caller="digest_bioassembly")
    assert [item.tolist() for item in nested_chains] == [[0, 1], [2]]

    nested_structures = digest_structure_indices([[0, 1], [2]])
    assert [item.tolist() for item in nested_structures] == [[0, 1], [2]]


def test_merge_digesters_preserve_per_system_intent():
    molecular_systems = [object(), object()]
    caller = 'molsysmt.basic.merge.merge'

    selections = digest_selections(
        [0, [1, 2]],
        molecular_systems=molecular_systems,
        caller=caller,
    )
    assert selections == [[0], [1, 2]]

    structure_indices = digest_structure_indices(
        [0, [1, 2]],
        molecular_systems=molecular_systems,
        caller=caller,
    )
    assert [item.tolist() for item in structure_indices] == [[0], [1, 2]]


def test_merge_digesters_broadcast_non_list_collections():
    molecular_systems = [object(), object()]
    caller = 'molsysmt.basic.merge.merge'

    selections = digest_selections(
        np.array([0, 1]),
        molecular_systems=molecular_systems,
        caller=caller,
    )
    assert selections == [[0, 1], [0, 1]]

    structure_indices = digest_structure_indices(
        np.array([0, 1]),
        molecular_systems=molecular_systems,
        caller=caller,
    )
    assert [item.tolist() for item in structure_indices] == [[0, 1], [0, 1]]


def test_merge_digesters_reject_per_system_length_mismatch():
    molecular_systems = [object(), object()]
    caller = 'molsysmt.basic.merge.merge'

    with pytest.raises(ArgumentLengthError):
        digest_selections(['all'], molecular_systems=molecular_systems, caller=caller)

    with pytest.raises(ArgumentLengthError):
        digest_structure_indices([0], molecular_systems=molecular_systems, caller=caller)


@pytest.mark.parametrize(
    "digester, kwargs",
    [
        (digest_atom_indices, {}),
        (digest_group_indices, {"caller": None}),
        (digest_chain_indices, {"caller": None}),
        (digest_molecule_indices, {"caller": None}),
        (digest_entity_indices, {"caller": None}),
        (digest_component_indices, {"caller": None}),
        (digest_structure_indices, {}),
    ],
)
def test_indices_digesters_reject_invalid_inputs(digester, kwargs):
    with pytest.raises(ArgumentError):
        digester({"bad": "indices"}, **kwargs)
