"""Pinned sources for scientific criteria actively implemented by MolSysMT."""

MOLSTAR_REFERENCE = {
    "software": "Mol*", "commit": "4807179589f43c20f38d689e4acbc3fc8590df14",
    "implementation": "https://github.com/molstar/molstar/blob/4807179589f43c20f38d689e4acbc3fc8590df14/src/mol-model-props/computed/interactions/charged.ts",
    "paper": "https://doi.org/10.1093/nar/gkab314",
}
MDTRAJ_REFERENCE = {
    "software": "MDTraj", "commit": "80f7cf2ddb43dd0d32905e490464f2d8765329df",
    "pi_pi": "https://github.com/mdtraj/mdtraj/blob/80f7cf2ddb43dd0d32905e490464f2d8765329df/mdtraj/geometry/pi_stacking.py",
    "hbonds": "https://github.com/mdtraj/mdtraj/blob/80f7cf2ddb43dd0d32905e490464f2d8765329df/mdtraj/geometry/hbond.py",
    "paper": "https://doi.org/10.1016/j.bpj.2015.08.015",
    "hydrogen_bond_definitions": {
        "baker_hubbard": "https://doi.org/10.1016/0079-6107(84)90007-5",
        "wernet_nilsson": "https://doi.org/10.1126/science.1096205",
    },
}
CPPTRAJ_REFERENCE = {
    "software": "CPPTRAJ", "version": "6.24.0",
    "commit": "0793fd579c5bb41377462d70df0b249a48bc9eb7",
    "implementation": "https://github.com/Amber-MD/cpptraj/blob/0793fd579c5bb41377462d70df0b249a48bc9eb7/src/Action_HydrogenBond.cpp",
    "paper": "https://doi.org/10.1021/ct400341p",
    "pytraj_commit": "96083c77ee6f355a6cbffd66518401e832a8f8c2",
}
MDANALYSIS_REFERENCE = {
    "software": "MDAnalysis", "commit": "9531c6e157d0211bfcc086374e3da429d1e3c8d1",
    "implementation": "https://github.com/MDAnalysis/mdanalysis/blob/9531c6e157d0211bfcc086374e3da429d1e3c8d1/package/MDAnalysis/analysis/hydrogenbonds/hbond_analysis.py",
    "documentation": "https://docs.mdanalysis.org/stable/documentation_pages/analysis/hydrogenbonds.html",
}
