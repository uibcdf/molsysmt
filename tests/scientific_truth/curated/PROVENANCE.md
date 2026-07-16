# Curated Scientific Systems

These bundled artifacts are fixed inputs to the Scientific Truth Suite. SHA-256
digests make silent replacement detectable. The external tools and MolSysMT read
the artifacts independently.

| System | Catalog artifact | Scientific role | SHA-256 |
|---|---|---|---|
| Met-enkephalin | `molsysmt/data/pdb/met_enkephalin.pdb` | Backbone distances, angles, and signed dihedrals | `51b90cab54d4c375c9559ff5617977bae4270dd240f33c68de76c3aabc6bab21` |
| Trp-cage TC5b, PDB 1L2Y | `molsysmt/data/pdb/1l2y.pdb` | Coordinates, distances, dihedrals, and least-RMSD across 38 NMR models | `5d1bbb545a312dfff1ae1e64b6d8addecb2f561ddc4011aeb5bee9d1dfcd4438` |
| Pentaalanine | `molsysmt/data/h5/traj_pentalanine.h5` | MDTraj-readable 5000-frame periodic trajectory oracle | `aedcb9817e0a398b7a718104e13dd2d94e7819f0536ccea343cf6faa3dc69475` |
| Pentaalanine | `molsysmt/data/h5msm/traj_pentalanine.h5msm` | Paired MolSysMT trajectory artifact | `3eda9e887845b27073a498ae2d6e564596abbe52d1cbdca76870dd23fd98a285` |
| Solvated chicken villin HP35 | `molsysmt/data/h5/traj_chicken_villin_HP35_solvated.h5` | Multi-molecule covalent reconstruction against MDTraj periodic bond distances | `701372a9749186302717c0c85027e6177bebdeb43a09620f43b930f692898959` |
| NGLView `md_1u19` | `molsysmt/data/gro/md_1u19.gro` | Topology for a periodic multiframe demo trajectory | `8eec93cb0b45c43abc50ec40e49f983e2c2484671077777db19bf7340c068c76` |
| NGLView `md_1u19` | `molsysmt/data/xtc/md_1u19.xtc` | Periodic coordinates and boxes for MIC comparisons | `8279bc6723a4b2e70d6ef3e83fbbcaeb3f981d80546ef4195b7b1d7ba5815af1` |

The 1L2Y file identifies the deposited NMR ensemble, authors, experimental
conditions, and primary publication in its PDB header. The other artifacts are
MolSysMT demo-catalog assets. Their hashes establish fixture identity but do not
replace missing upstream provenance; any future replacement must document its
generator or source before updating this table.
