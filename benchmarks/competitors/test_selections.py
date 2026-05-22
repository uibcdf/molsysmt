"""Competitive Benchmark for Selection Language.

This module compares the atom selection speed and parsing overhead of MolSysMT,
MDTraj, and MDAnalysis on a realistic PDB structure (solvated chicken villin, 4369 atoms).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Add repository root to python path to ensure robust imports
repo_root = str(Path(__file__).resolve().parents[2])
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import molsysmt as msm
from benchmarks.harness import BenchmarkHarness


def run_selection_benchmarks(pdb_path: str, output_results: list | None = None) -> list[dict]:
    """Execute selection benchmarks comparing MolSysMT, MDTraj, and MDAnalysis.

    Parameters
    ----------
    pdb_path : str
        Path to the reference PDB topology file.
    output_results : list, optional
        A list to append benchmark results to.

    Returns
    -------
    list[dict]
        Benchmark timing results.
    """
    # Initialize MolSysMT system
    structure = msm.convert(pdb_path, to_form='molsysmt.MolSys')

    # Initialize MDTraj system
    import mdtraj
    mdt_structure = mdtraj.load(pdb_path)

    # Initialize MDAnalysis system
    import MDAnalysis
    mda_structure = MDAnalysis.Universe(pdb_path)

    # 1. Standard CA query
    msm_query_simple = 'atom_name == "CA"'
    mdt_query_simple = 'name CA'
    mda_query_simple = 'name CA'

    h_msm_simple = BenchmarkHarness("competitor_selection_molsysmt_simple", iterations=50, repeats=5)
    h_mdt_simple = BenchmarkHarness("competitor_selection_mdtraj_simple", iterations=50, repeats=5)
    h_mda_simple = BenchmarkHarness("competitor_selection_mdanalysis_simple", iterations=50, repeats=5)

    def select_msm_simple():
        return msm.select(structure, msm_query_simple)

    def select_mdt_simple():
        return mdt_structure.topology.select(mdt_query_simple)

    def select_mda_simple():
        return mda_structure.select_atoms(mda_query_simple)

    # 2. Complex query
    msm_query_complex = '(atom_name == "CA" or atom_name == "CB") and group_name in ["ALA", "VAL", "LEU"]'
    mdt_query_complex = '(name CA or name CB) and resname ALA VAL LEU'
    mda_query_complex = '(name CA or name CB) and resname ALA VAL LEU'

    h_msm_complex = BenchmarkHarness("competitor_selection_molsysmt_complex", iterations=50, repeats=5)
    h_mdt_complex = BenchmarkHarness("competitor_selection_mdtraj_complex", iterations=50, repeats=5)
    h_mda_complex = BenchmarkHarness("competitor_selection_mdanalysis_complex", iterations=50, repeats=5)

    def select_msm_complex():
        return msm.select(structure, msm_query_complex)

    def select_mdt_complex():
        return mdt_structure.topology.select(mdt_query_complex)

    def select_mda_complex():
        return mda_structure.select_atoms(mda_query_complex)

    results = []

    print("Running simple selection benchmarks...")
    results.append(h_msm_simple.run(warmup_func=select_msm_simple, timed_func=select_msm_simple))
    results.append(h_mdt_simple.run(warmup_func=select_mdt_simple, timed_func=select_mdt_simple))
    results.append(h_mda_simple.run(warmup_func=select_mda_simple, timed_func=select_mda_simple))

    print("Running complex selection benchmarks...")
    results.append(h_msm_complex.run(warmup_func=select_msm_complex, timed_func=select_msm_complex))
    results.append(h_mdt_complex.run(warmup_func=select_mdt_complex, timed_func=select_mdt_complex))
    results.append(h_mda_complex.run(warmup_func=select_mda_complex, timed_func=select_mda_complex))

    if output_results is not None:
        output_results.extend(results)

    return results


if __name__ == "__main__":
    pdb_file = os.path.join(repo_root, "solvated_villin.pdb")
    if not os.path.exists(pdb_file):
        print(f"Generating temporary PDB file: {pdb_file}")
        h5 = msm.systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5']
        msm.convert(h5, to_form='file:pdb', output_filename=pdb_file)

    run_selection_benchmarks(pdb_file)
