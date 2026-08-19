"""The chain termini must titrate with the pH argument, like the side chains do.

Guard for `uibcdf/molsysmt#176`. `add_missing_hydrogens` placed `HXT` on the C-terminal
carboxylate at every pH, and a COOH terminus has no template in AMBER or CHARMM, so no
natively prepared protein reached a force field.

Every case here sweeps pH rather than asserting at 7.4. A test fixed at one pH would
pass against a rule that ignores pH entirely, which is exactly what the defect was.

The two termini are asserted through different routes, because they are decided in
different places. The C-terminal proton comes from `get_expected_hydrogens` and can be
checked end to end. The third N-terminal proton is placed by
`add_missing_terminal_cappings`, and the systems shipped with MolSysMT are NMR
structures that already carry it — neither function removes a hydrogen, so the rule
cannot be observed on them. It is asserted at unit level instead, which is honest about
what is covered rather than quietly leaving the N-terminus untested.
"""

import pytest

import molsysmt as msm
from molsysmt.element.group.amino_acid.get_expected_hydrogens import get_expected_hydrogens

C_TERMINAL_THRESHOLD = 3.2
N_TERMINAL_THRESHOLD = 9.6

METHIONINE_HEAVY = ['N', 'CA', 'C', 'O', 'CB', 'CG', 'SD', 'CE']


@pytest.fixture(scope='module')
def villin():
    """1VII carries no OXT, so the C-terminal proton seen afterwards is one we placed."""
    molecular_system = msm.extract(
        msm.convert(msm.systems['chicken villin HP35']['1vii.pdb'], to_form='molsysmt.MolSys'),
        structure_indices=[0],
    )
    assert len(msm.select(molecular_system, selection="atom_name=='HXT'")) == 0
    return molecular_system


@pytest.mark.parametrize('pH', [1.0, 2.0, 3.0])
def test_c_terminus_is_protonated_below_its_pka(villin, pH):
    prepared = msm.build.add_missing_terminal_cappings(villin, pH=pH, engine='MolSysMT')
    prepared = msm.build.add_missing_hydrogens(prepared, pH=pH, engine='MolSysMT')
    assert len(msm.select(prepared, selection="atom_name=='HXT'")) == 1


@pytest.mark.parametrize('pH', [4.0, 7.4, 9.0, 12.0])
def test_c_terminus_is_a_carboxylate_above_its_pka(villin, pH):
    prepared = msm.build.add_missing_terminal_cappings(villin, pH=pH, engine='MolSysMT')
    prepared = msm.build.add_missing_hydrogens(prepared, pH=pH, engine='MolSysMT')
    assert len(msm.select(prepared, selection="atom_name=='HXT'")) == 0, (
        f'the C-terminal carboxylate is protonated at pH {pH}; no standard force field '
        f'has a template for a COOH terminus'
    )


def test_a_natively_prepared_protein_reaches_a_force_field(villin):
    """The failure this defect produced, asserted as the behaviour it blocked."""
    openmm = pytest.importorskip('openmm')
    assert openmm is not None

    prepared = msm.build.add_missing_terminal_cappings(villin, pH=7.4, engine='MolSysMT')
    prepared = msm.build.add_missing_hydrogens(prepared, pH=7.4, engine='MolSysMT')
    prepared = msm.build.solvate(
        prepared, box_shape='cubic', clearance='12 angstroms',
        water_model='TIP3P', ionic_strength='0.15 molar', engine='MolSysMT')

    simulation = msm.convert(prepared, to_form='openmm.Simulation', forcefield='AMBER14')
    assert simulation is not None


@pytest.mark.parametrize(
    ('pH', 'expects_third_proton'),
    [(1.0, True), (7.4, True), (9.0, True), (10.0, False), (12.0, False)],
)
def test_n_terminal_amine_titrates(pH, expects_third_proton):
    """Charged NH3+ below the amine's pKa, neutral NH2 above it.

    Asserted on the expected-hydrogen list rather than on a prepared system: this one
    never raises downstream, because NH3+ has a template in every force field, so a
    test that only ran a force field would report success either way.
    """
    expected = get_expected_hydrogens(
        'MET', present_atom_names=METHIONINE_HEAVY + ['H1', 'H2'],
        pH=pH, is_n_terminal=True)

    assert ('H3' in expected) is expects_third_proton


def test_the_side_chain_rules_still_hold():
    """The termini were added to a table that already worked; it must keep working.

    `HB2`/`HB3` are in the input on purpose. Variant selection prefers the tightest
    fit, and a bare heavy-atom set selects a variant that has no `HD2` at all — the
    pH rule then has nothing to act on and the assertion would pass without ever
    exercising it.
    """
    aspartate = ['N', 'CA', 'C', 'O', 'CB', 'CG', 'OD1', 'OD2', 'HB2', 'HB3']
    assert 'HD2' in get_expected_hydrogens('ASP', present_atom_names=aspartate, pH=3.0)
    assert 'HD2' not in get_expected_hydrogens('ASP', present_atom_names=aspartate, pH=7.4)
