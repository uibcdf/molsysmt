"""
Extended tests for molsysmt.element.molecule.get_molecule_type covering:

- redefine_types=True with element='chain' (line 112-117)
- redefine_types=True with element='entity' (line 118-123)
- redefine_types=True with element='component' on a solvated system
- redefine_indices=True with element='chain' (line 61-65)
- _get_molecule_type_from_group_names_and_types logic exercised indirectly via
  redefine_types=True on systems with protein, peptide, water and ion molecules
"""

import molsysmt as msm
import numpy as np
import pytest


# ---------------------------------------------------------------------------
# Fixtures used
#   hp35_solvated_molsys  – protein (35 aa, peptide) + 1254 waters + 2 ions
#   met_enkephalin_h5msm_molsys – Met-enkephalin peptide (5 aa, < min_length_protein)
#   t4_h5msm_molsys       – T4 lysozyme (protein, > min_length_protein)
#   builder_pdb_molsys    – minimal builder: 1 protein group + 1 water group
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# redefine_types=True, element='chain'
# ---------------------------------------------------------------------------

class TestRedefineTypesChain:

    def test_chain_solvated_returns_list_of_lists(self, hp35_solvated_molsys):
        """redefine_types + element='chain' returns a list of lists."""
        result = msm.element.molecule.get_molecule_type(
            hp35_solvated_molsys,
            element='chain',
            selection='all',
            redefine_types=True,
        )
        assert isinstance(result, list)
        # Each entry corresponds to one chain; each entry is a list of molecule types
        for entry in result:
            assert isinstance(entry, list)

    def test_chain_solvated_types_consistent(self, hp35_solvated_molsys):
        """redefine_types + element='chain' molecule types are non-empty and string."""
        result = msm.element.molecule.get_molecule_type(
            hp35_solvated_molsys,
            element='chain',
            selection='all',
            redefine_types=True,
        )
        for entry in result:
            for mol_type in entry:
                assert isinstance(mol_type, str)
                assert len(mol_type) > 0

    def test_chain_t4_protein_type(self, t4_h5msm_molsys):
        """redefine_types + element='chain' on T4 lysozyme gives protein type entries."""
        result = msm.element.molecule.get_molecule_type(
            t4_h5msm_molsys,
            element='chain',
            selection='all',
            redefine_types=True,
        )
        # Flatten all types
        all_types = [t for chain_types in result for t in chain_types]
        # T4 lysozyme is a large protein (163 residues > min_length_protein=50)
        assert 'protein' in all_types


# ---------------------------------------------------------------------------
# redefine_types=True, element='entity'
# ---------------------------------------------------------------------------

class TestRedefineTypesEntity:

    def test_entity_solvated_returns_list_of_lists(self, hp35_solvated_molsys):
        """redefine_types + element='entity' returns a list of lists."""
        result = msm.element.molecule.get_molecule_type(
            hp35_solvated_molsys,
            element='entity',
            selection='all',
            redefine_types=True,
        )
        assert isinstance(result, list)
        for entry in result:
            assert isinstance(entry, list)

    def test_entity_types_are_strings(self, hp35_solvated_molsys):
        """redefine_types + element='entity': all returned type strings are non-empty."""
        result = msm.element.molecule.get_molecule_type(
            hp35_solvated_molsys,
            element='entity',
            selection='all',
            redefine_types=True,
        )
        for entry in result:
            for mol_type in entry:
                assert isinstance(mol_type, str)
                assert len(mol_type) > 0

    def test_entity_t4_protein_type(self, t4_h5msm_molsys):
        """redefine_types + element='entity' on T4 lysozyme sees protein type."""
        result = msm.element.molecule.get_molecule_type(
            t4_h5msm_molsys,
            element='entity',
            selection='all',
            redefine_types=True,
        )
        all_types = [t for entity_types in result for t in entity_types]
        assert 'protein' in all_types


# ---------------------------------------------------------------------------
# redefine_types=True – _get_molecule_type_from_group_names_and_types paths
# ---------------------------------------------------------------------------

class TestRedefineTypesHelperPaths:

    def test_water_path_via_redefine_types(self, hp35_solvated_molsys):
        """redefine_types correctly identifies water molecules (first_group_type='water')."""
        types = msm.element.molecule.get_molecule_type(
            hp35_solvated_molsys,
            element='molecule',
            selection='all',
            redefine_types=True,
        )
        # The solvated system has ~1254 water molecules
        assert 'water' in types

    def test_ion_path_via_redefine_types(self, hp35_solvated_molsys):
        """redefine_types correctly identifies ion molecules (first_group_type='ion')."""
        types = msm.element.molecule.get_molecule_type(
            hp35_solvated_molsys,
            element='molecule',
            selection='all',
            redefine_types=True,
        )
        assert 'ion' in types

    def test_peptide_path_via_redefine_types(self, met_enkephalin_h5msm_molsys):
        """redefine_types identifies short amino-acid chains as 'peptide' (< min_length_protein)."""
        types = msm.element.molecule.get_molecule_type(
            met_enkephalin_h5msm_molsys,
            element='molecule',
            selection='all',
            redefine_types=True,
        )
        # Met-enkephalin: 5 residues, below min_length_protein=50
        assert 'peptide' in types

    def test_protein_path_via_redefine_types(self, t4_h5msm_molsys):
        """redefine_types identifies long amino-acid chains as 'protein' (>= min_length_protein)."""
        types = msm.element.molecule.get_molecule_type(
            t4_h5msm_molsys,
            element='molecule',
            selection='all',
            redefine_types=True,
        )
        assert 'protein' in types

    def test_redefine_types_molecule_count(self, hp35_solvated_molsys):
        """redefine_types: length of output for element='molecule' equals total n_molecules."""
        n_molecules = msm.get(hp35_solvated_molsys, element='system', n_molecules=True)
        types = msm.element.molecule.get_molecule_type(
            hp35_solvated_molsys,
            element='molecule',
            selection='all',
            redefine_types=True,
        )
        assert len(types) == n_molecules


# ---------------------------------------------------------------------------
# redefine_indices=True – chain element path (line 61-65)
# ---------------------------------------------------------------------------

class TestRedefineIndicesChain:

    def test_chain_redefine_indices_returns_list_of_lists(self, hp35_solvated_molsys):
        """redefine_indices + element='chain' returns a list-of-lists structure."""
        result = msm.element.molecule.get_molecule_type(
            hp35_solvated_molsys,
            element='chain',
            selection='all',
            redefine_indices=True,
        )
        assert isinstance(result, list)
        for entry in result:
            assert isinstance(entry, list)

    def test_chain_redefine_indices_protein_present(self, t4_h5msm_molsys):
        """redefine_indices + element='chain' on T4 lysozyme contains protein type."""
        result = msm.element.molecule.get_molecule_type(
            t4_h5msm_molsys,
            element='chain',
            selection='all',
            redefine_indices=True,
        )
        all_types = [t for chain_types in result for t in chain_types]
        assert 'protein' in all_types

    def test_chain_redefine_indices_solvated_water_present(self, hp35_solvated_molsys):
        """redefine_indices + element='chain' on solvated system includes water type."""
        result = msm.element.molecule.get_molecule_type(
            hp35_solvated_molsys,
            element='chain',
            selection='all',
            redefine_indices=True,
        )
        all_types = [t for chain_types in result for t in chain_types]
        assert 'water' in all_types


# ---------------------------------------------------------------------------
# Consistency: redefine_types vs plain get for element='molecule'
# ---------------------------------------------------------------------------

class TestRedefineTypesConsistency:

    def test_redefine_types_vs_plain_same_length(self, hp35_solvated_molsys):
        """redefine_types output has same length as plain molecule_type output."""
        types_plain = msm.element.molecule.get_molecule_type(
            hp35_solvated_molsys,
            element='molecule',
            selection='all',
        )
        types_redefined = msm.element.molecule.get_molecule_type(
            hp35_solvated_molsys,
            element='molecule',
            selection='all',
            redefine_types=True,
        )
        assert len(types_redefined) == len(types_plain)

    def test_redefine_types_atom_length_matches_n_atoms(self, hp35_solvated_molsys):
        """redefine_types + element='atom' gives one type per atom."""
        n_atoms = msm.get(hp35_solvated_molsys, element='system', n_atoms=True)
        types = msm.element.molecule.get_molecule_type(
            hp35_solvated_molsys,
            element='atom',
            selection='all',
            redefine_types=True,
        )
        assert len(types) == n_atoms

    def test_redefine_types_group_length_matches_n_groups(self, hp35_solvated_molsys):
        """redefine_types + element='group' gives one type per group."""
        n_groups = msm.get(hp35_solvated_molsys, element='system', n_groups=True)
        types = msm.element.molecule.get_molecule_type(
            hp35_solvated_molsys,
            element='group',
            selection='all',
            redefine_types=True,
        )
        assert len(types) == n_groups

    def test_redefine_types_component_length_matches_n_components(self, hp35_solvated_molsys):
        """redefine_types + element='component' gives one type per component."""
        n_components = msm.get(hp35_solvated_molsys, element='system', n_components=True)
        types = msm.element.molecule.get_molecule_type(
            hp35_solvated_molsys,
            element='component',
            selection='all',
            redefine_types=True,
        )
        assert len(types) == n_components
