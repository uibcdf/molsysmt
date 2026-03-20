"""
Extended tests for get_chain_type covering additional element and selection branches.
"""
import molsysmt as msm
import pytest


@pytest.fixture()
def tctim_molsys(tctim_h5msm_molsys):
    return tctim_h5msm_molsys


@pytest.fixture()
def hp35_solvated(hp35_solvated_molsys):
    return hp35_solvated_molsys


# ---------------------------------------------------------------------------
# redefine_types=True, various elements
# ---------------------------------------------------------------------------

def test_get_chain_type_redefine_atoms(hp35_solvated):
    """element='atom' with redefine_types=True → list length == n_atoms."""
    n_atoms = msm.get(hp35_solvated, element='system', n_atoms=True)
    output = msm.element.chain.get_chain_type(
        hp35_solvated, element='atom', selection='all', redefine_types=True
    )
    assert isinstance(output, list)
    assert len(output) == n_atoms


def test_get_chain_type_redefine_groups(hp35_solvated):
    """element='group' with redefine_types=True → list length == n_groups."""
    n_groups = msm.get(hp35_solvated, element='system', n_groups=True)
    output = msm.element.chain.get_chain_type(
        hp35_solvated, element='group', selection='all', redefine_types=True
    )
    assert isinstance(output, list)
    assert len(output) == n_groups


def test_get_chain_type_redefine_components(hp35_solvated):
    """element='component' with redefine_types=True → list length == n_components."""
    n_components = msm.get(hp35_solvated, element='system', n_components=True)
    output = msm.element.chain.get_chain_type(
        hp35_solvated, element='component', selection='all', redefine_types=True
    )
    assert isinstance(output, list)
    assert len(output) == n_components


def test_get_chain_type_redefine_molecules(hp35_solvated):
    """element='molecule' with redefine_types=True → list length == n_molecules."""
    n_molecules = msm.get(hp35_solvated, element='system', n_molecules=True)
    output = msm.element.chain.get_chain_type(
        hp35_solvated, element='molecule', selection='all', redefine_types=True
    )
    assert isinstance(output, list)
    assert len(output) == n_molecules


def test_get_chain_type_redefine_chains(hp35_solvated):
    """element='chain' with redefine_types=True → list length == n_chains."""
    n_chains = msm.get(hp35_solvated, element='system', n_chains=True)
    output = msm.element.chain.get_chain_type(
        hp35_solvated, element='chain', selection='all', redefine_types=True
    )
    assert isinstance(output, list)
    assert len(output) == n_chains


def test_get_chain_type_redefine_entities(tctim_molsys):
    """element='entity' with redefine_types=True → list of lists."""
    output = msm.element.chain.get_chain_type(
        tctim_molsys, element='entity', selection='all', redefine_types=True
    )
    assert isinstance(output, list)
    assert len(output) > 0


# ---------------------------------------------------------------------------
# redefine_types=False (else branch) — uses stored chain_type
# ---------------------------------------------------------------------------

def test_get_chain_type_no_redefine(tctim_molsys):
    """redefine_types=False uses stored chain_type attribute."""
    output = msm.element.chain.get_chain_type(
        tctim_molsys, element='chain', selection='all', redefine_types=False
    )
    assert isinstance(output, list)
    assert len(output) == msm.get(tctim_molsys, element='system', n_chains=True)


def test_get_chain_type_no_redefine_atom_element(tctim_molsys):
    """redefine_types=False, element='atom' uses stored chain_type via get."""
    n_atoms = msm.get(tctim_molsys, element='system', n_atoms=True)
    output = msm.element.chain.get_chain_type(
        tctim_molsys, element='atom', selection='all', redefine_types=False
    )
    assert isinstance(output, list)
    assert len(output) == n_atoms


# ---------------------------------------------------------------------------
# with specific selection (not 'all')
# ---------------------------------------------------------------------------

def test_get_chain_type_with_selection(tctim_molsys):
    """Specific chain selection returns correct count of types."""
    output = msm.element.chain.get_chain_type(
        tctim_molsys, element='chain', selection='chain_index==0', redefine_types=True
    )
    assert isinstance(output, list)
    assert len(output) == 1
