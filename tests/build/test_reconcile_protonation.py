"""Preparation must not stay silent about a protonation it will not touch.

Guard for `uibcdf/molsysmt#178`. `add_missing_hydrogens` compares expected against
present in one direction: it adds what is absent and never looks at what is present and
unwanted. A system arriving over-protonated — an NMR structure, or one prepared at a
different pH — therefore went through preparation unchanged and unremarked.

The silence is the part that made it dangerous. The C-terminal defect in
`uibcdf/molsysmt#176` produced a visible failure, because a COOH terminus has no
force-field template. NH3+ has one everywhere, so an over-protonated amine simulates at
the wrong charge without anything raising.

`reconcile_protonation` supplies the other direction, and `add_missing_hydrogens` now
warns rather than acting, so both are asserted here. Detection is shared between them,
and the tests check that they agree rather than trusting that they do.
"""

import warnings

import pytest

import molsysmt as msm
from molsysmt._private.smonitor import UnexpectedProtonationWarning
from molsysmt.build._protonation import unexpected_hydrogens

# 1VII is an NMR structure: 301 hydrogens of 596 atoms, including H3 on the N-terminal
# amine and HZ3 on every lysine. At pH 7.4 all of them belong; at pH 12 they do not.
PHYSIOLOGICAL = 7.4
ALKALINE = 12.0


@pytest.fixture(scope='module')
def villin():
    return msm.extract(
        msm.convert(msm.systems['chicken villin HP35']['1vii.pdb'], to_form='molsysmt.MolSys'),
        structure_indices=[0],
    )


def _n_atoms(molecular_system):
    return int(msm.get(molecular_system, element='system', n_atoms=True))


def test_nothing_is_removed_when_the_input_already_matches(villin):
    """The physiological case must be untouched, or the function is unusable by default."""
    before = _n_atoms(villin)
    result = msm.build.reconcile_protonation(villin, pH=PHYSIOLOGICAL)
    assert _n_atoms(result) == before
    assert unexpected_hydrogens(villin, pH=PHYSIOLOGICAL) == []


def test_hydrogens_the_ph_contradicts_are_removed(villin):
    before = _n_atoms(villin)
    unexpected = unexpected_hydrogens(villin, pH=ALKALINE)
    assert unexpected, 'the case must actually carry unwanted hydrogens to be a test'

    result = msm.build.reconcile_protonation(villin, pH=ALKALINE)

    assert _n_atoms(result) == before - len(unexpected)
    assert len(msm.select(result, selection="atom_name=='H3'")) == 0
    assert unexpected_hydrogens(result, pH=ALKALINE) == [], 'one pass must be enough'


def test_the_input_is_not_modified_by_default(villin):
    """`in_place=False` is the default precisely because this one destroys data."""
    before = _n_atoms(villin)
    msm.build.reconcile_protonation(villin, pH=ALKALINE)
    assert _n_atoms(villin) == before


def test_the_side_chain_rules_are_applied_too(villin):
    """Not only the termini: the table that was already there governs this as well."""
    unexpected = unexpected_hydrogens(villin, pH=ALKALINE)
    names = {name for _, name, _, _ in unexpected}
    assert 'H3' in names, 'the N-terminal amine, pKa around 9.6'
    assert 'HZ3' in names, 'lysine NZ, pKa 10.5 — a rule that predates this work'


def test_add_missing_hydrogens_warns_about_what_it_leaves(villin):
    with pytest.warns(UnexpectedProtonationWarning) as recorded:
        msm.build.add_missing_hydrogens(villin, pH=ALKALINE, engine='MolSysMT')

    reported = ' '.join(str(record.message) for record in recorded)
    assert 'reconcile_protonation' in reported, 'the warning must name the remedy'
    assert '12.0' in reported, 'and the pH it is judging against'


def test_add_missing_hydrogens_is_quiet_when_there_is_nothing_to_report(villin):
    """A warning that fires on the ordinary case would be trained away immediately."""
    with warnings.catch_warnings(record=True) as recorded:
        warnings.simplefilter('always')
        msm.build.add_missing_hydrogens(villin, pH=PHYSIOLOGICAL, engine='MolSysMT')

    assert not [w for w in recorded
                if issubclass(w.category, UnexpectedProtonationWarning)]


def test_add_missing_hydrogens_still_only_adds(villin):
    """The warning reports; it must not have quietly become an action."""
    before = _n_atoms(villin)
    result = msm.build.add_missing_hydrogens(villin, pH=ALKALINE, engine='MolSysMT')
    assert _n_atoms(result) >= before


def test_an_unsupported_engine_is_refused(villin):
    from molsysmt._private.smonitor import NotImplementedMethodError

    with pytest.raises(NotImplementedMethodError):
        msm.build.reconcile_protonation(villin, pH=PHYSIOLOGICAL, engine='OpenMM')
