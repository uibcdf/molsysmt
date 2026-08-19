# User Guide Cookbook Agents Guide

This guide governs the **Cookbook** section of the User Guide under `docs/content/user/cookbook`.

## Purpose and Philosophy

- Provide practical, multi-step, end-to-end recipes combining multiple MolSysMT tools (and third-party engines such as OpenMM, MDAnalysis, NetworkX, NGLView) to accomplish real-world scientific tasks.
- Keep recipes deterministic, lightweight, fast to execute (< 3 seconds each), and self-contained.
- Always use the canonical variable name `molsys` for single molecular systems (or `molsys_wt`, `molsys_mut`, `molsys_A`, `molsys_B` for comparative contexts).

## Standard Recipe Page Structure

Every recipe notebook (`*.ipynb`) MUST follow this structure:
1. **Hidden Setup Cell**: Tagged with `"remove-input"` containing warning filters.
2. **Header Block**:
   - Section anchor: `(Cookbook_<RecipeName>)=`
   - Title: `# <Short and Direct Recipe Title>`
   - Gerund summary in italics: `*<Gerund summary>.*`
   - Narrative introduction explaining the biological/computational problem.
   - Version added directive: `:::{versionadded} 1.0.0:::`
3. **Step-by-Step Sections**:
   - Clear markdown explanation introducing each phase before the executable Python cell.
   - Descriptive prints and metrics verifying each step.
4. **Closing See Also Block**:
   - Collapsible dropdown `:::{seealso} :class: dropdown` linking to relevant Toolbox functions, Foundations concepts, and API references.

## Paired Micro-Governance Contract

Every recipe `[name].ipynb` MUST be paired with its micro-governance file `[name].ipynb.AGENTS.md` defining its frozen contracts, anchors, and essential concepts.

## Recipe Catalog

1. `building_complex_dimers.ipynb`: Reconstructing Barnase-Barstar complex from multi-chain PDB (1BRS) using `msm.structure.least_rmsd_align`, `msm.merge`, and `msm.build`.
2. `spectacular_visualizations.ipynb`: Advanced multi-layered rendering (ribbons, pockets, transparent surfaces, vector arrows) with NGLView.
3. `simulation_workflow.ipynb`: System setup, solvation, OpenMM simulation, `StructuresDictReporter` streaming, and in-memory trajectory analysis.
4. `big_data_trajectories.ipynb`: Ultra-low RAM streaming, slicing, and chunked execution with H5MSM and `msm.Iterator`.
5. `from_pdb_to_solvated_box.ipynb`: Capping, neutral solvation, and PBC box validation with `msm.build.solvate`.
6. `binding_pocket_isolation.ipynb`: Spatial query syntax (`within ... of`) for active site extraction and ligand distance analysis.
7. `trajectory_performance_analysis.ipynb`: Multi-threaded calculation of RMSD, RMSF, and Radius of Gyration time series with summary plots.
8. `structural_surgery_mutagenesis.ipynb`: In-memory point mutation (`msm.build.mutate`), heavy atom side-chain reconstruction, and structural superposition.
9. `form_teleportation.ipynb`: Interoperability with OpenMM, MDAnalysis, NetworkX, MDTraj, and BioPython with conversion audit reports.
