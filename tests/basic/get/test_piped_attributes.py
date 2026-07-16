import molsysmt as msm
import pytest

from molsysmt.basic.get import _piped_molecular_system
from molsysmt.form import _dict_modules
from molsysmt._private.smonitor import NotWithThisFormError


def test_piped_molecular_system_for_nglview_topological_attributes():
    molsys = msm.convert(
        msm.systems['T4 lysozyme L99A']['181l.pdb'],
        to_form='molsysmt.MolSys',
    )
    view = msm.convert(molsys, to_form='nglview.NGLWidget')

    piped_systems, piped_attributes = _piped_molecular_system(
        view,
        'atom',
        ['atom_index', 'group_index', 'entity_index'],
    )

    assert len(piped_systems) == 1
    assert msm.get_form(piped_systems[0]) == 'molsysmt.Topology'
    assert piped_attributes == [['atom_index', 'group_index', 'entity_index']]


def test_piped_molecular_system_for_nglview_mixed_attributes():
    molsys = msm.convert(
        msm.systems['T4 lysozyme L99A']['181l.pdb'],
        to_form='molsysmt.MolSys',
    )
    view = msm.convert(molsys, to_form='nglview.NGLWidget')

    piped_systems, piped_attributes = _piped_molecular_system(
        view,
        'atom',
        ['atom_index', 'coordinates'],
    )

    assert len(piped_systems) == 1
    assert msm.get_form(piped_systems[0]) == 'molsysmt.MolSys'
    assert piped_attributes == [['atom_index', 'coordinates']]


def test_single_attribute_uses_direct_getter_when_available(t4_pdb_file):
    piped_systems, piped_attributes = _piped_molecular_system(
        t4_pdb_file,
        'system',
        ['n_atoms'],
    )

    assert piped_systems is None
    assert piped_attributes is None


def test_single_attribute_uses_pipe_when_direct_getter_is_missing(t4_pdb_file):
    piped_systems, piped_attributes = _piped_molecular_system(
        t4_pdb_file,
        'atom',
        ['atom_type'],
    )

    assert len(piped_systems) == 1
    assert msm.get_form(piped_systems[0]) == 'molsysmt.Topology'
    assert piped_attributes == [['atom_type']]


def test_declared_attribute_without_getter_or_pipe_raises_molsysmt_exception(
    t4_pdb_molsys,
    monkeypatch,
):
    module = _dict_modules['molsysmt.MolSys']
    monkeypatch.delattr(module, 'get_formal_charge_from_atom')

    with pytest.raises(NotWithThisFormError):
        msm.get(t4_pdb_molsys, element='atom', formal_charge=True)


def test_piped_form_metadata_for_known_bulk_extraction_forms():
    expected_pipes = {
        'nglview.NGLWidget': ('molsysmt.Topology', 'molsysmt.Structures', 'molsysmt.MolSys'),
        'file:gro': ('molsysmt.MolSys', 'molsysmt.Structures', 'molsysmt.MolSys'),
        'file:xtc': (None, 'mdtraj.XTCTrajectoryFile', None),
        'molsysviewer.MolSysView': ('molsysmt.MolSys', 'molsysmt.MolSys', 'molsysmt.MolSys'),
        'molsysmt.H5MSMFileHandler': (None, 'molsysmt.Structures', None),
        'mmcif.PdbxContainers.DataContainer': ('molsysmt.Topology', 'molsysmt.Structures', 'molsysmt.MolSys'),
        'string:pdb_text': ('molsysmt.Topology', 'molsysmt.Structures', 'molsysmt.MolSys'),
        'string:pdb_id': ('molsysmt.Topology', 'molsysmt.Structures', 'molsysmt.MolSys'),
        'string:alphafold_id': ('molsysmt.Topology', 'molsysmt.Structures', 'molsysmt.MolSys'),
    }

    for form, expected in expected_pipes.items():
        module = _dict_modules[form]
        observed = (
            module.piped_topological_attribute,
            module.piped_structural_attribute,
            module.piped_any_attribute,
        )
        assert observed == expected
