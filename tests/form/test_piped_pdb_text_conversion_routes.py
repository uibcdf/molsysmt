"""Two-step conversions through `string:pdb_text` must reach their target.

Guard for `uibcdf/molsysmt#180`. Seven adapters imported
`molsysmt.form.string_pdb_text.to_string_pdb_text` — the identity converter of the
*target* form — instead of their own. The import resolves cleanly, so nothing failed
until call time, and these internal calls pass `skip_digestion=True`, which switches off
the form check that would have caught the wrong object. An `NGLWidget` therefore reached
`copy()` and surfaced as `NotImplementedError: Widgets cannot be copied`.

They arrived in `e6b20c77c`, a 214-file refactor titled *"make a plugin's converters
lazy, and unambiguous to import"*, and stayed for eleven days because no test crossed
these routes. That absence is what this file exists to remove.

`openmm.Topology` carries no coordinates, so the routes that need them are exercised
with coordinates supplied — that is the contract, not a workaround.
"""

import pytest

import molsysmt as msm


@pytest.fixture(scope='module')
def enkephalin():
    return msm.convert(msm.systems['Met-enkephalin']['met_enkephalin.h5msm'])


@pytest.fixture(scope='module')
def topology(enkephalin):
    return msm.convert(enkephalin, to_form='openmm.Topology')


@pytest.fixture(scope='module')
def coordinates(enkephalin):
    return msm.get(enkephalin, element='atom', coordinates=True)


def test_nglwidget_to_openmm_topology(enkephalin):
    """The route in the report: it failed inside `copy()`, far from the cause."""
    pytest.importorskip('nglview')
    widget = msm.view(enkephalin, viewer='nglview')

    result = msm.convert(widget, to_form='openmm.Topology')

    assert result.getNumAtoms() == int(msm.get(enkephalin, element='system', n_atoms=True))


def test_openmm_topology_to_file_pdb(topology, coordinates, tmp_path):
    output = str(tmp_path / 'probe.pdb')
    result = msm.convert(topology, to_form='file:pdb', coordinates=coordinates,
                         output_filename=output)
    assert result == output
    with open(output) as handle:
        assert any(line.startswith('ATOM') for line in handle)


def test_openmm_topology_to_openmm_pdbfile(topology, coordinates):
    result = msm.convert(topology, to_form='openmm.PDBFile', coordinates=coordinates)
    assert result.topology.getNumAtoms() == topology.getNumAtoms()


def test_openmm_topology_to_pdbfixer(topology, coordinates):
    pytest.importorskip('pdbfixer')
    result = msm.convert(topology, to_form='pdbfixer.PDBFixer', coordinates=coordinates)
    assert result.topology.getNumAtoms() == topology.getNumAtoms()


def test_openmm_topology_to_nglwidget(topology, coordinates):
    pytest.importorskip('nglview')
    result = msm.convert(topology, to_form='nglview.NGLWidget', coordinates=coordinates)
    assert result is not None


def test_the_identity_converter_refuses_a_foreign_item():
    """The mechanism that hid this, closed at its source.

    `skip_digestion=True` is legitimate for an internal two-step conversion, and it is
    what let a widget through. An identity converter is the one place where a wrong
    item cannot be inferred from the operation, so it checks even when digestion is
    off — turning a `NotImplementedError` raised deep inside `copy()` into a message
    that names the likely import mistake.
    """
    from molsysmt._private.smonitor import NotSupportedFormError
    from molsysmt.form.string_pdb_text.to_string_pdb_text import to_string_pdb_text

    with pytest.raises(NotSupportedFormError) as failure:
        to_string_pdb_text(object(), skip_digestion=True)

    assert 'to_string_pdb_text' in str(failure.value)


def test_no_adapter_imports_the_identity_converter():
    """The seven that did are the defect; a new one would be the same defect again."""
    import pathlib

    form_directory = pathlib.Path(msm.__file__).parent / 'form'
    offending = [
        f'{path.parent.name}/{path.name}'
        for path in sorted(form_directory.glob('*/to_*.py'))
        if path.parent.name != 'string_pdb_text'
        and 'from molsysmt.form.string_pdb_text.to_string_pdb_text import' in path.read_text()
    ]

    assert offending == [], (
        f'{len(offending)} adapter(s) import the identity converter instead of their '
        f'own: {offending}'
    )
