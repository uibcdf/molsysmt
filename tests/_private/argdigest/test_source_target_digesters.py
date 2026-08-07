import pytest

import molsysmt as msm
from molsysmt._private.argdigest.argument.from_item import digest_from_item
from molsysmt._private.argdigest.argument.to_item import digest_to_item
from molsysmt._private.argdigest.argument.from_element import digest_from_element
from molsysmt._private.argdigest.argument.to_group_names import digest_to_group_names
from molsysmt._private.argdigest.argument.output_filename import digest_output_filename
from molsysmt._private.argdigest.argument.output_form import digest_output_form
from molsysmt._private.argdigest.argument.output_indices import digest_output_indices
from molsysmt._private.argdigest.argument.output_structure_indices import digest_output_structure_indices
from molsysmt._private.smonitor import ArgumentError


def test_item_source_target_digesters(builder_pdb_molsys, tmp_path):
    assert digest_from_item(builder_pdb_molsys) is builder_pdb_molsys
    assert digest_to_item(builder_pdb_molsys) is builder_pdb_molsys
    assert digest_from_item(builder_pdb_molsys, form='molsysmt.MolSys') is builder_pdb_molsys
    assert digest_to_item(builder_pdb_molsys, form='molsysmt.MolSys') is builder_pdb_molsys

    with pytest.raises(ArgumentError):
        digest_from_item(builder_pdb_molsys, form='molsysmt.Topology')
    with pytest.raises(ArgumentError):
        digest_to_item(builder_pdb_molsys, form='molsysmt.Topology')

    assert digest_from_element('atoms') == 'atom'
    assert digest_from_element('group') == 'group'
    assert digest_from_element(None, caller='molsysmt.topology.bonds_are_required_to_get_attribute') is None
    assert digest_to_group_names('ALA', caller='x') == ['ALA']
    assert digest_to_group_names(['ALA', 'GLY'], caller='x') == ['ALA', 'GLY']

    out = tmp_path / 'output.pdb'
    assert digest_output_filename(out) == str(out)
    assert digest_output_form('MOLSYSMT.MOLSYS') == 'molsysmt.MolSys'
    assert digest_output_form(['MOLSYSMT.MOLSYS', 'molsysmt.Topology']) == ['molsysmt.MolSys', 'molsysmt.Topology']
    assert digest_output_indices('atom', caller='molsysmt.structure.get_distances.get_distances') == 'atom'
    assert digest_output_structure_indices('structure', caller='molsysmt.structure.get_neighbors.get_neighbors') == 'structure'

    with pytest.raises(ArgumentError):
        digest_to_group_names(['ALA', 1], caller='x')
    with pytest.raises(ArgumentError):
        digest_output_form('not_a_form')
    with pytest.raises(ArgumentError):
        digest_output_indices('bad', caller='molsysmt.structure.get_distances.get_distances')
    with pytest.raises(ArgumentError):
        digest_output_structure_indices('bad', caller='molsysmt.structure.get_neighbors.get_neighbors')
