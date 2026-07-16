"""Testing molecular-system classification and consistency evidence."""

import pytest

import molsysmt as msm
from molsysmt._private.arg_digestion.argument.molecular_system import digest_molecular_system
from molsysmt._private.arg_digestion.argument.from_molecular_system import (
    digest_from_molecular_system,
)
from molsysmt._private.arg_digestion.argument.to_molecular_system import (
    digest_to_molecular_system,
)
from molsysmt._private.molecular_system_validation import (
    MolecularSystemKind,
    ValidationStatus,
    assess_molecular_system,
)
from molsysmt._private.smonitor import (
    MolecularSystemVerificationError,
    StructuralInconsistencyError,
)


def test_two_topology_providers_are_classified_without_atom_count_reads(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError('classification must not read molecular data')

    monkeypatch.setattr(msm.basic, 'get', fail_if_called)
    assessment = assess_molecular_system(['1CRN', '2LAO'])

    assert assessment.kind is MolecularSystemKind.MULTIPLE
    assert assessment.validation is ValidationStatus.VALID


def test_inconsistent_complementary_items_are_not_multiple_systems():
    topology = msm.systems['pentalanine']['pentalanine.prmtop']
    structures = msm.systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd']
    assessment = assess_molecular_system([topology, structures])

    assert assessment.kind is MolecularSystemKind.SINGLE
    assert assessment.validation is ValidationStatus.INVALID
    for digester in (
        digest_molecular_system,
        digest_from_molecular_system,
        digest_to_molecular_system,
    ):
        with pytest.raises(StructuralInconsistencyError):
            digester([topology, structures], caller='test')


def test_crd_with_partial_topology_is_complementary_to_psf():
    crd = msm.systems['POPC']['popc.crd']
    psf = msm.systems['POPC']['popc.psf']

    assessment = assess_molecular_system([crd, psf])

    assert assessment.kind is MolecularSystemKind.SINGLE
    assert assessment.validation is ValidationStatus.VALID
    assert assessment.atom_counts == (
        msm.get(crd, n_atoms=True),
        msm.get(psf, n_atoms=True),
    )


def test_failed_consistency_probe_is_unverified_not_valid(monkeypatch):
    topology = msm.systems['pentalanine']['pentalanine.prmtop']
    structures = msm.systems['pentalanine']['pentalanine.inpcrd']

    def fail_if_called(*args, **kwargs):
        raise RuntimeError('missing getter')

    monkeypatch.setattr(msm.basic, 'get', fail_if_called)
    assessment = assess_molecular_system([topology, structures])

    assert assessment.kind is MolecularSystemKind.SINGLE
    assert assessment.validation is ValidationStatus.UNVERIFIED
    assert assessment.is_valid_single_system is False
    with pytest.raises(MolecularSystemVerificationError):
        digest_molecular_system([topology, structures], caller='test')


def test_pure_mechanical_metadata_does_not_require_an_atom_count():
    assessment = assess_molecular_system(
        [
            {'dispersion_correction': True},
            {'forcefield': 'AMBER14', 'water_model': 'TIP3P'},
        ]
    )

    assert assessment.kind is MolecularSystemKind.SINGLE
    assert assessment.validation is ValidationStatus.VALID
    assert assessment.atom_counts == ()


def test_verification_exception_is_public_and_catalog_backed():
    assert msm.MolecularSystemVerificationError is MolecularSystemVerificationError
    assert MolecularSystemVerificationError.catalog_key == 'MolecularSystemVerificationError'
