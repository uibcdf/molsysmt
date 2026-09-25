(Cookbook)=
# Cookbook

Welcome to the **MolSysMT Cookbook**. Here, you will find self-contained recipes designed to solve structural biology tasks with elegance, speed, and reproducibility.

Each recipe combines multiple MolSysMT tools and demonstrates how to interface with external engines such as OpenMM, MDAnalysis, NetworkX, and NGLView.

| Recipe | Objective |
| :--- | :--- |
| **{doc}`building_complex_dimers`** | Harvesting, superimposing, and merging monomers from multi-chain PDBs into a complete complex. |
| **{doc}`spectacular_visualizations`** | Rendering molecular scenes with cartoon ribbons, pocket surfaces, and annotation vectors in NGLView. |
| **{doc}`simulation_workflow`** | Setting up, solvating, and executing an OpenMM molecular dynamics simulation with in-memory frame streaming. |
| **{doc}`big_data_trajectories`** | Streaming and slicing large trajectory datasets with constant memory using H5MSM. |
| **{doc}`from_pdb_to_solvated_box`** | Preparing, capping, and solvating experimental structures in a neutral periodic box. |
| **{doc}`binding_pocket_isolation`** | Extracting active site residues and computing ligand contact distances using spatial selections. |
| **{doc}`trajectory_performance_analysis`** | Computing RMSD, per-residue RMSF, and radius of gyration time series across trajectory structures. |
| **{doc}`structural_surgery_mutagenesis`** | Introducing point mutations in memory, rebuilding side chains, and superimposing against the wild type. |
| **{doc}`form_teleportation`** | Converting molecular systems across OpenMM, MDAnalysis, NetworkX, MDTraj, and BioPython. |

```{eval-rst}
.. toctree::
   :maxdepth: 1
   :hidden:

   building_complex_dimers.ipynb
   spectacular_visualizations.ipynb
   simulation_workflow.ipynb
   big_data_trajectories.ipynb
   from_pdb_to_solvated_box.ipynb
   binding_pocket_isolation.ipynb
   trajectory_performance_analysis.ipynb
   structural_surgery_mutagenesis.ipynb
   form_teleportation.ipynb
```

:::{tip}
:class: dropdown

Use these recipes as templates for your computational structural biology pipelines. For detailed function documentation and arguments, consult the **{doc}`Toolbox <../tools/index>`** and **{doc}`API Reference <../../../api/index>`**.
:::
