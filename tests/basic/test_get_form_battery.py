"""A census-backed battery for `get_form`.

`get_form` answers the question every other function asks first, so a form it fails to
recognise, or recognises as the wrong thing, is a defect with unlimited blast radius. The
per-form tests in `test_get_form.py` cover a handful of forms chosen by hand. This file
covers the *catalogue*, and -- more importantly -- fails when the catalogue grows past it.

Three parts:

- `ROUTES` says how to obtain an item of a form. One test per entry asserts `get_form`
  returns exactly that form.
- `UNREACHED` records the forms this battery cannot build yet, each with the reason.
- `test_the_battery_covers_the_catalogue` asserts that every declared form appears in one
  of the two. A new form added to `molsysmt/form/` fails this test until somebody decides
  which it is. That is what stops the battery from quietly falling behind.

Shrinking `UNREACHED` is incremental work: most entries need an item built directly with
the third-party library rather than through `msm.convert`.
"""

import pytest

import molsysmt as msm
from molsysmt import systems

# --- how to obtain an item of each form -------------------------------------------------
#
#   ('system', system_name, file_key)  a file shipped with the library
#   ('convert', origin)                msm.convert from one of ORIGINS
#   ('literal', value)                 a string that names or carries the system
#   ('convert_file', name, key)        msm.convert from a file shipped with the library

ROUTES = {
    'MDAnalysis.Topology': ('convert', 'pdb_file'),
    'MDAnalysis.Universe': ('convert', 'pdb_file'),
    'MDAnalysis.topology.PDBParser': ('convert', 'pdb_file'),
    'XYZ': ('convert', 'molsys'),
    'biopython.PDBStructure': ('convert', 'molsys'),
    'file:bcif': ('system', 'chicken villin HP35', '1vii.bcif'),
    'file:bcif.gz': ('system', 'Trp-Cage', '1l2y.bcif.gz'),
    'file:crd': ('system', 'POPC', 'popc.crd'),
    'file:dcd': ('system', 'chicken villin HP35',
                 'traj_chicken_villin_HP35_solvated.dcd'),
    'file:gro': ('system', 'nglview', 'md_1u19.gro'),
    'file:h5': ('system', 'pentalanine', 'traj_pentalanine.h5'),
    'file:h5msm': ('system', 'alanine dipeptide', 'alanine_dipeptide.h5msm'),
    'file:inpcrd': ('system', 'pentalanine', 'pentalanine.inpcrd'),
    'file:mol2': ('system', 'caffeine', 'caffeine.mol2'),
    'file:pdb': ('system', 'Met-enkephalin', 'met_enkephalin.pdb'),
    'file:prmtop': ('system', 'pentalanine', 'pentalanine.prmtop'),
    'file:psf': ('system', 'POPC', 'popc.psf'),
    'file:trjpk': ('system', 'two LJ particles', 'traj_two_lj_particles.trjpk'),
    'file:xtc': ('system', 'nglview', 'md_1u19.xtc'),
    'file:xyznpy': ('system', 'particles 4', 'traj_particles_4.xyznpy'),
    'mdtraj.DCDTrajectoryFile': ('convert_file', 'chicken villin HP35',
                                 'traj_chicken_villin_HP35_solvated.dcd'),
    'mdtraj.GroTrajectoryFile': ('convert_file', 'nglview', 'md_1u19.gro'),
    'mdtraj.PDBTrajectoryFile': ('convert', 'pdb_file'),
    'mdtraj.XTCTrajectoryFile': ('convert_file', 'nglview', 'md_1u19.xtc'),
    'mdtraj.Topology': ('convert', 'molsys'),
    'mdtraj.Trajectory': ('convert', 'molsys'),
    'molsysmt.GROFileHandler': ('convert_file', 'nglview', 'md_1u19.gro'),
    'molsysmt.H5MSMFileHandler': ('convert', 'h5msm_file'),
    'molsysmt.MolSys': ('convert', 'molsys'),
    'molsysmt.MolSysBuilder': ('convert', 'molsys'),
    'molsysmt.MolSysDict': ('convert', 'molsys'),
    'molsysmt.MolecularMechanics': ('convert', 'molsys'),
    'molsysmt.PDBFileHandler': ('convert', 'pdb_file'),
    'molsysmt.Structures': ('convert', 'molsys'),
    'molsysmt.StructuresDict': ('convert', 'structures'),
    'molsysmt.Topology': ('convert', 'molsys'),
    'molsysmt.TopologyDict': ('convert', 'topology'),
    'molsysmt.ViewerJSON': ('convert', 'molsys'),
    'molsysviewer.MolSysView': ('convert', 'molsys'),
    'networkx.Graph': ('convert', 'molsys'),
    'nglview.NGLWidget': ('convert', 'molsys'),
    'openmm.AmberInpcrdFile': ('convert_file', 'pentalanine', 'pentalanine.inpcrd'),
    'openmm.AmberPrmtopFile': ('convert_file', 'pentalanine', 'pentalanine.prmtop'),
    'openmm.CharmmCrdFile': ('convert_file', 'POPC', 'popc.crd'),
    'openmm.CharmmPsfFile': ('convert_file', 'POPC membrane', 'popc_membrane.psf'),
    'openmm.GromacsGroFile': ('convert_file', 'nglview', 'md_1u19.gro'),
    'openmm.Modeller': ('convert', 'molsys'),
    'openmm.PDBFile': ('convert', 'pdb_file'),
    'openmm.Topology': ('convert', 'molsys'),
    'openff.Molecule': ('openff', 'molecule'),
    'openff.Topology': ('openff', 'topology'),
    'parmed.Structure': ('convert', 'molsys'),
    'pdbfixer.PDBFixer': ('convert', 'molsys'),
    'pytraj.Topology': ('convert', 'molsys'),
    'rdkit.Mol': ('convert', 'molsys'),
    'string:alphafold_id': ('literal', 'AF-P00720-F1'),
    'string:amino_acids_1': ('convert', 'molsys'),
    'string:amino_acids_3': ('convert', 'molsys'),
    'string:pdb_id': ('literal', 'pdb_id:1VII'),
    'string:pdb_text': ('convert', 'molsys'),
    'string:smiles': ('literal', 'smiles:CCO'),
    'string:uniprot_id': ('literal', 'uniprot_id:P00720'),
}

#: Declared forms this battery cannot build an item of yet, and why. Entries here are work
#: to do, not forms excused from being correct.
UNREACHED = {
    'pytraj.Trajectory':
        'converting into it aborts the interpreter -- see '
        'devguide/pending_bugs/convert_to_pytraj_trajectory_aborts_the_interpreter.md',
    'openmm.System':
        'unreachable from molsysmt.MolSys -- see devguide/pending_bugs/'
        'convert_molsys_to_openmm_system_passes_the_wrong_topology.md',
    'openmm.Simulation':
        'unreachable from molsysmt.MolSys -- same bug as openmm.System',
}

_NO_ROUTE = 'no conversion route from the origins this battery builds; needs an item ' \
            'constructed directly with the third-party library'

for _form in (
    'MDAnalysis.AtomGroup', 'biopython.Seq', 'biopython.SeqRecord', 'cupy_ndarray',
    'file:cif', 'file:cif.gz', 'file:fasta', 'file:mdcrd', 'file:molsys_yaml', 'file:pir',
    'file:smi', 'file:structures_yaml', 'file:top', 'file:topology_yaml', 'file:xyz',
    'mdtraj.AmberRestartFile', 'mdtraj.HDF5TrajectoryFile',
    'mmcif.PdbxContainers.DataContainer', 'molsysmt.CIFFileHandler',
    'molsysmt.MolecularMechanicsDict',
    'openmm.Context', 'openmm.GromacsTopFile', 'openmm.State',
    'parmed.GromacsTopologyFile',
):
    UNREACHED.setdefault(_form, _NO_ROUTE)


@pytest.fixture(scope='module')
def origins():
    """The systems every route converts from, built once."""

    pdb_file = systems['chicken villin HP35']['1vii.pdb']
    h5msm_file = systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    molsys = msm.convert(h5msm_file, to_form='molsysmt.MolSys')
    return {
        'pdb_file': pdb_file,
        'h5msm_file': h5msm_file,
        'molsys': molsys,
        'topology': msm.convert(molsys, to_form='molsysmt.Topology'),
        'structures': msm.convert(molsys, to_form='molsysmt.Structures'),
    }


def _build(form, origins):
    route = ROUTES[form]
    if route[0] == 'system':
        return systems[route[1]][route[2]]
    if route[0] == 'literal':
        return route[1]
    if route[0] == 'convert_file':
        return msm.convert(systems[route[1]][route[2]], to_form=form)
    if route[0] == 'openff':
        from openff.toolkit.topology import Molecule

        molecule = Molecule.from_smiles('CCO')
        if route[1] == 'topology':
            return molecule.to_topology()
        return molecule
    return msm.convert(origins[route[1]], to_form=form)


# --- the catalogue census ---------------------------------------------------------------

def test_the_battery_covers_the_catalogue():
    """Every declared form is either exercised here or recorded as not yet reachable.

    This is the test that keeps the battery honest. Adding a form to `molsysmt/form/`
    without deciding how it gets detected leaves a form nothing verifies, and that is
    exactly the kind of hole that stays open for years.
    """

    from molsysmt.form import _dict_forms_lowercase

    declared = set(_dict_forms_lowercase.values())
    covered = set(ROUTES) | set(UNREACHED)

    assert not (declared - covered), (
        'forms declared in molsysmt/form/ that this battery neither exercises nor '
        f'records as unreachable: {sorted(declared - covered)}')
    assert not (covered - declared), (
        f'forms named here that no longer exist: {sorted(covered - declared)}')


def test_no_form_is_both_covered_and_excused():
    assert not (set(ROUTES) & set(UNREACHED))


# --- detection --------------------------------------------------------------------------

@pytest.mark.parametrize('form', sorted(ROUTES))
def test_the_form_of_an_item_is_the_form_it_was_built_as(form, origins):
    assert msm.get_form(_build(form, origins)) == form


# --- how the input is spelled -----------------------------------------------------------

def test_a_path_object_is_read_like_its_string():
    from pathlib import Path

    path = systems['chicken villin HP35']['1vii.pdb']
    assert msm.get_form(Path(path)) == msm.get_form(str(path)) == 'file:pdb'


def test_a_sequence_of_items_gives_a_sequence_of_forms():
    inpcrd = systems['pentalanine']['pentalanine.inpcrd']
    prmtop = systems['pentalanine']['pentalanine.prmtop']
    assert msm.get_form([inpcrd, prmtop]) == ['file:inpcrd', 'file:prmtop']
    assert msm.get_form((inpcrd, prmtop)) == ['file:inpcrd', 'file:prmtop']


def test_asking_twice_gives_the_same_answer(origins):
    molsys = origins['molsys']
    assert msm.get_form(molsys) == msm.get_form(molsys) == 'molsysmt.MolSys'


def test_an_unsupported_item_is_refused():
    from molsysmt._private.smonitor import NotSupportedFormError

    with pytest.raises(NotSupportedFormError):
        msm.get_form(object())


def test_a_form_name_is_not_an_item():
    """`get_form` asks what form an *object* is. A form name is a name, not a system."""

    from molsysmt._private.smonitor import NotSupportedFormError

    with pytest.raises(NotSupportedFormError):
        msm.get_form('file:pdb')


# --- what detection must not cost -------------------------------------------------------

def test_recognising_a_path_does_not_import_the_whole_platform():
    """Answering a question about a *name* must not load the libraries behind the data.

    This used to fail: the registry learned a form's name by importing the module that
    declares it, so any question about forms imported all 89 plugins -- 3.9 s and every
    third-party library MolSysMT can talk to. The catalogue reads the same facts from the
    declarations without executing anything.
    """

    import subprocess
    import sys

    script = (
        'import molsysmt as msm, sys\n'
        'msm.get_form("traj.pdb")\n'
        'print(",".join(sorted({m for m in ("openmm", "rdkit", "openff", "mdtraj") '
        'if m in sys.modules})))\n'
    )
    result = subprocess.run([sys.executable, '-c', script],
                            capture_output=True, text=True, timeout=300)
    assert result.stdout.strip() == '', (
        f'imported to answer a question about a string: {result.stdout.strip()}')


# --- the predicates that ride on top of detection ---------------------------------------
#
# `is_item`, `is_file` and `is_string` answer coarser questions than `get_form`, and every
# caller assumes they agree with it. The catalogue makes the expected answer derivable:
# a form's category is written in its name, and `form_type` matches that prefix for all 89
# forms. So the whole agreement can be asserted from the same table that drives detection.

def _category(form):
    if form.startswith('file:'):
        return 'file'
    if form.startswith('string:'):
        return 'string'
    return 'class'


def test_form_type_matches_the_name_prefix():
    """The convention the indexes rely on: a form's category is readable in its name."""

    from molsysmt.form import _dict_modules

    wrong = {form: (module.form_type, _category(form))
             for form, module in _dict_modules.items()
             if module.form_type != _category(form)}
    assert not wrong, f'form_type disagrees with the name prefix: {wrong}'


@pytest.mark.parametrize('form', sorted(ROUTES))
def test_the_predicates_agree_with_the_detected_form(form, origins):
    from molsysmt.form import is_file, is_item, is_string

    item = _build(form, origins)
    category = _category(form)

    assert is_item(item) is True
    assert is_file(item) == (category == 'file'), f'is_file disagrees for {form}'
    assert is_string(item) == (category == 'string'), f'is_string disagrees for {form}'


@pytest.mark.parametrize('form', sorted(ROUTES))
def test_the_predicates_also_accept_a_form_name(form):
    """`is_file` and `is_string` are documented as taking an item *or* a form name."""

    from molsysmt.form import is_file, is_string

    category = _category(form)
    assert is_file(form) == (category == 'file')
    assert is_string(form) == (category == 'string')


@pytest.mark.parametrize('value', [
    object(), 'not a molecular system at all', b'bytes', 42, None, [], {},
])
def test_the_predicates_never_raise(value):
    """A predicate that raises is a predicate every caller has to wrap in try/except.

    `get_form` raises by design -- it has no answer to give. These three always have one.
    """

    from molsysmt.form import is_file, is_item, is_string

    assert is_item(value) in (True, False)
    assert is_file(value) in (True, False)
    assert is_string(value) in (True, False)
