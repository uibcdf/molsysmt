"""The contract around xdist rebuilding catalog warnings on the controller.

This is the guard for `uibcdf/molsysmt#158`: it fails if the doubled text ever
comes back, whether because a new warning class is written in a shape that
defeats the round trip, or because the base class starts transforming its
message again.

It covers every warning class rather than one, which is `uibcdf/molsysmt#161`. The
classes are **discovered** rather than listed, because a test that names eleven has
the same hole as a test that names one: the twelfth is not covered and nobody
notices.

Discovery walks every `Warning` subclass defined in
`molsysmt/_private/smonitor/warnings.py`, which is the single home for them, rather
than the subclasses of `MolSysMTCatalogWarning`. The invariant that matters is not
which base a class has but whether it renders a template in its own `__init__`:
that is what `cls(*args)` can double. `MolSysMTDeprecationWarning` inherits from
`DeprecationWarning` on purpose and would be missed by a base-class walk, and a
future class written the same way with a template would be missed with it.

Discovery alone would not be enough either — every field defaults to `None`, so
building with the defaults would pass without rendering anything — so each
discovered class must also appear in `SAMPLES` with values that exercise it. The
failure a new class produces is "add its sample values here", not silence.

What crosses the boundary is the text, and only the text. `xdist.remote.serialize_warning_message`
transfers `message_str`, the class name, and `args` when execnet can serialise them;
it never transfers `__dict__`, and the controller rebuilds with `cls(*args)`. So the
structured `extra` payload does not survive — `UnknownAtomNameWarning(atom_name='Ar')`
arrives with `'Ar'` in the sentence and `atom_name` absent from `extra`.

That is xdist's protocol rather than a defect in the warning classes, and `pickle` and
`copy.deepcopy` both preserve the payload in full because they do restore `__dict__`.
It is written here because it is the kind of thing a reader assumes the other way
round: code on the controller must branch on the text, not on `extra`.

A second test lived here until the fix landed, whose job was to fail the day the
workaround in `conftest.py` became unnecessary. It did exactly that, and both it
and the workaround are gone.
"""

import warnings

import numpy as np
import pytest

import molsysmt._private.smonitor.warnings as warnings_module
from molsysmt._private.smonitor import CATALOG

xdist_remote = pytest.importorskip("xdist.remote")
xdist_workermanage = pytest.importorskip("xdist.workermanage")


def _cross_chain_system():
    """Two atoms in two chains joined by a bond, which is what the warning reports.

    Built rather than loaded: `CrossChainCovalentBondsWarning` is the only class whose
    constructor reads a molecular system, and a demo file that happens to contain a
    cross-chain bond would make this test depend on that file continuing to have one.
    """
    import molsysmt as msm
    from molsysmt import pyunitwizard as puw

    builder = msm.build.editable()
    builder.add_atom(atom_name='CA', atom_type='C', atom_id=1)
    builder.add_atom(atom_name='CB', atom_type='C', atom_id=2)
    builder.add_group(atom_indices=[0], group_name='ALA', group_type='amino acid', group_id=1)
    builder.add_group(atom_indices=[1], group_name='GLY', group_type='amino acid', group_id=2)
    builder.add_chain(group_indices=[0], chain_id='A', chain_name='A')
    builder.add_chain(group_indices=[1], chain_id='B', chain_name='B')
    builder.add_bond(0, 1)
    builder.set_coordinates(puw.quantity(np.zeros((1, 2, 3)), 'nm'))

    return builder.build()


# Field values per class, and a fragment that must survive the round trip. The
# fragment is what proves the sample exercised the constructor rather than rendering
# defaults: a class whose sample produces nothing recognisable is a sample that is not
# testing anything.
#
# It is looked for in the rendered sentence *or* in `extra`, because the two kinds of
# catalog warning differ there. Some templates interpolate their fields into the
# sentence — `UnknownAtomNameWarning` names the atom — while others render a fixed
# sentence and carry the fields as structured payload, as
# `MolecularSystemMismatchWarning` does with `caller` and `count`. Both consumed the
# field; only one shows it.
#
# Classes that inherit their constructor supply their own `message`, since they have
# no fields of their own. They are here because they would regress if the base ever
# transformed its message again, which is the other half of #158.
SAMPLES = {
    'MolSysMTCatalogWarning': ({'message': 'a base catalog warning'}, 'a base catalog warning'),
    'MolSysMTDeprecationWarning': ({'message': 'setup_logging() is deprecated'}, 'deprecated'),
    'UserMolSysMTWarning': ({'message': 'a plain user warning'}, 'a plain user warning'),
    'SelectionWarning': ({'message': 'the selection is ambiguous'}, 'ambiguous'),
    'DownloadWarning': ({'message': 'the download fell back to a mirror'}, 'mirror'),
    'CrossChainCovalentBondsWarning': (
        {'molecular_system': _cross_chain_system, 'atom_pairs': [(0, 1)]},
        'Cross-chain covalent bonds',
    ),
    'NotDigestedArgumentWarning': ({'argument': 'selection'}, 'selection'),
    'MolecularSystemMismatchWarning': (
        {'caller': 'molsysmt.basic.compare', 'n_models': 3}, 'molsysmt.basic.compare',
    ),
    'StructuralAttributeOffAxisWarning': (
        {'attributes': ['time', 'b_factor'], 'caller': 'molsysmt.basic.convert'}, 'time',
    ),
    'StructuralAttributeDropWarning': (
        {'attributes': ['occupancy'], 'caller': 'molsysmt.append_structures'}, 'occupancy',
    ),
    'IncompatibleBoxWarning': (
        {'reason': 'the boxes differ', 'caller': 'molsysmt.basic.add'}, 'the boxes differ',
    ),
    'BioassemblyIdentifierCollisionWarning': (
        {'renamed': [('A', 'A-1'), ('B', 'B-1')],
         'caller': 'molsysmt.build.make_bioassembly'},
        'A -> A-1',
    ),
    'SlowChunkIOWarning': ({'chunk_index': 7, 'io_time_s': 12.5}, '7'),
    'MemoryPressureWarning': (
        {'chunk_index': 3, 'rss_bytes': 1383370752, 'budget_bytes': 1000000,
         'pressure_pct': 138337.0},
        '1383370752',
    ),
    'UnknownAtomNameWarning': ({'atom_name': 'Ar'}, "'Ar'"),
    'GpuNotAvailableWarning': ({'reason': 'no CUDA GPU is accessible'}, 'CUDA'),
}


def _warning_classes():
    """Every warning class this package defines, found in the module that defines them.

    Not `MolSysMTCatalogWarning.__subclasses__()`: that walk depends on the class
    having been imported, and it silently excludes any class hung off a different
    base — `MolSysMTDeprecationWarning` inherits `DeprecationWarning` deliberately,
    so Python's own tooling treats it as a deprecation.
    """
    found = set()
    for name in dir(warnings_module):
        obj = getattr(warnings_module, name)
        if isinstance(obj, type) and issubclass(obj, Warning) and obj.__module__ == warnings_module.__name__:
            found.add(obj)
    return found


DISCOVERED = sorted(_warning_classes(), key=lambda cls: cls.__name__)


def _round_trip(instance):
    """Marshal a warning the way xdist does between worker and controller."""
    carrier = warnings.WarningMessage(
        message=instance, category=type(instance), filename=__file__, lineno=0
    )
    data = xdist_remote.serialize_warning_message(carrier)
    return xdist_workermanage.unserialize_warning_message(data).message


def _build(cls):
    fields, fragment = SAMPLES[cls.__name__]
    resolved = {key: value() if callable(value) else value for key, value in fields.items()}
    if set(resolved) == {'message'}:
        # Passed positionally because that is how every `Warning` accepts it, including
        # the ones that never went through `CatalogWarning` and take no keywords at all.
        return cls(resolved['message']), fragment
    return cls(**resolved), fragment


def test_every_catalog_warning_class_has_a_sample():
    """Discovery is only useful if a new class cannot slip through unexercised."""
    missing = sorted(cls.__name__ for cls in DISCOVERED if cls.__name__ not in SAMPLES)
    assert not missing, (
        f'catalog warning classes with no sample values: {missing}. Add an entry to '
        'SAMPLES with field values that render a recognisable sentence, so the round '
        'trip is exercised rather than skipped.'
    )


def test_the_sample_registry_has_no_stale_entries():
    """A sample for a class that no longer exists is a test that stopped testing."""
    discovered = {cls.__name__ for cls in DISCOVERED}
    stale = sorted(name for name in SAMPLES if name not in discovered)
    assert not stale, f'samples for classes that no longer exist: {stale}'


@pytest.mark.parametrize('cls', DISCOVERED, ids=lambda cls: cls.__name__)
def test_catalog_warnings_are_not_re_rendered(cls):
    """A catalog warning crossing to the controller must not render twice.

    The failure this guards against is a class whose `__init__` takes a domain field
    first: `.args` carries the rendered sentence, so a naive `cls(*args)` puts the
    sentence into that field and the template wraps it again. Comparing the rebuilt
    text against the original catches that, and catches any other transformation the
    rebuild might apply, without this test needing to know each template.
    """
    probe, fragment = _build(cls)
    original = str(probe)
    rendered = original + str(getattr(probe, 'extra', ''))


    assert fragment in rendered, (
        f'the sample for {cls.__name__} produced {rendered!r}, which does not contain '
        f'{fragment!r}. Either the template changed or the sample never exercised it.'
    )

    rebuilt = _round_trip(probe)

    assert str(rebuilt) == original, str(rebuilt)
    assert probe.args == rebuilt.args
    assert type(rebuilt) is cls


def test_every_declared_catalog_key_exists_in_the_catalog():
    """A class pointing at a key the catalog does not have renders nothing.

    The failure is quiet: `_catalog_entry` returns nothing, `code` stays `None`, and
    the warning still raises — with whatever text the caller happened to pass, or
    none. Checked here because this is the file that already knows every class.
    """
    catalog_keys = set(CATALOG.get('warnings', {}))
    dangling = sorted(
        f'{cls.__name__} -> {cls.catalog_key!r}'
        for cls in DISCOVERED
        if getattr(cls, 'catalog_key', None) and cls.catalog_key not in catalog_keys
    )
    assert not dangling, f'catalog_key values with no catalog entry: {dangling}'
