import pytest

from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.argdigest.argument.definition import digest_definition
from molsysmt._private.argdigest.argument.output_type import digest_output_type
from molsysmt._private.argdigest.argument.items import digest_items
from molsysmt._private.argdigest.argument.implicit_solvent import digest_implicit_solvent
from molsysmt.native.topology import Topology
from molsysmt.native.molsys import MolSys


def test_digest_definition_accepts_known_physchem_definitions():
    assert digest_definition('OpenMM', caller='molsysmt.physchem.get_mass.get_mass') == 'OpenMM'
    assert digest_definition('eisenberg', caller='molsysmt.physchem.get_hydrophobicity.get_hydrophobicity') == 'eisenberg'
    assert digest_definition('grantham', caller='molsysmt.physchem.get_volume.get_volume') == 'grantham'
    assert digest_definition('physical_pH7', caller='molsysmt.physchem.get_charge.get_charge') == 'physical_pH7'
    assert digest_definition('collantes', caller='molsysmt.physchem.get_surface_area.get_surface_area') == 'collantes'
    assert digest_definition('zimmerman', caller='molsysmt.physchem.get_polarity.get_polarity') == 'zimmerman'
    assert digest_definition('rose', caller='molsysmt.physchem.get_area_buried.get_area_buried') == 'rose'
    assert digest_definition('janin', caller='molsysmt.physchem.get_buried_fraction.get_buried_fraction') == 'janin'
    assert digest_definition('vdw', caller='molsysmt.physchem.get_atomic_radius.get_atomic_radius') == 'vdw'
    assert digest_definition('zhao', caller='molsysmt.physchem.get_transmembrane_tendency.get_transmembrane_tendency') == 'zhao'
    with pytest.raises(ArgumentError):
        digest_definition('bad', caller='molsysmt.physchem.get_volume.get_volume')


def test_digest_output_type_accepts_caller_specific_choices():
    assert digest_output_type('dataframe', caller='molsysmt.basic.info.info') == 'dataframe'
    assert digest_output_type('dictionary', caller='molsysmt.basic.get.get') == 'dictionary'
    assert digest_output_type('boolean', caller='molsysmt.basic.compare.compare') == 'boolean'
    assert digest_output_type('list', caller='molsysmt.basic.get_attributes.get_attributes') == 'list'
    assert digest_output_type('numpy.ndarray', caller='molsysmt.structure.get_distances.get_distances') == 'numpy.ndarray'
    assert digest_output_type('pairs', caller='molsysmt.structure.get_neighbors.get_neighbors') == 'pairs'
    assert digest_output_type('sorted pairs', caller='molsysmt.structure.get_contacts.get_contacts') == 'sorted pairs'
    assert digest_output_type('sets', caller='molsysmt.topology.get_covalent_blocks.get_covalent_blocks') == 'sets'
    assert digest_output_type('values', caller='molsysmt.some.iterator.__init__') == 'values'
    assert digest_output_type('dictionary', caller='molsysmt.hbonds.get_hbonds.get_hbonds') == 'dictionary'
    with pytest.raises(ArgumentError):
        digest_output_type('bad', caller='molsysmt.basic.get.get')


def test_digest_items_accepts_matching_form_sequences():
    topology = Topology(n_atoms=1, n_groups=1, n_chains=1, n_molecules=1, n_entities=1)
    # `MolSys.__init__` builds an empty container from element counts; a topology is
    # assigned afterwards. Passing `topology=` used to be accepted and discarded, so this
    # read as if it carried the topology when it never did.
    molsys = MolSys()
    molsys.topology = topology

    assert digest_items(molsys, caller='test') == [molsys]
    assert digest_items([topology, topology], forms='molsysmt.Topology', caller='test') == [topology, topology]
    with pytest.raises(ArgumentError):
        digest_items([topology, molsys], forms=['molsysmt.Topology', 'molsysmt.Topology'], caller='test')
    with pytest.raises(ArgumentError):
        digest_items(object(), caller='test')


def test_digest_implicit_solvent_accepts_convert_and_form_callers():
    assert digest_implicit_solvent(True, caller='molsysmt.basic.get.get') is True
    assert digest_implicit_solvent(None, caller='molsysmt.basic.convert.convert') is None
    assert digest_implicit_solvent(None, caller='molsysmt.form.file_pdb.to_openmm_System') is None
    assert digest_implicit_solvent('OBC1') == 'OBC1'
    with pytest.raises(ArgumentError):
        digest_implicit_solvent('bad-model')
