"""Pinned scientific recognition rules from ProLIF 2.2.2, without a runtime import.

References name the original implementation. These chemical SMARTS expressions
and geometric definitions are reproduced by MolSysMT's general matching and
geometry tools; no ProLIF package is required to run the detector.
"""

# Chemical SMARTS reproduced from ProLIF 2.2.2 (Apache-2.0).
# Copyright 2017-2026 Cédric BOUYSSET. See interactions/cation_pi/PROLIF_LICENSE.txt.
# MolSysMT implements the geometry independently with its general tools.
PROLIF_PATTERNS = (
    "[+{1-}!$(*~[*-{1-}]),$([NX3&!$([NX3]-O)]-[C]=[NX3+])]",
    "[a;r6]1:[a;r6]:[a;r6]:[a;r6]:[a;r6]:[a;r6]:1",
    "[a;r5]1:[a;r5]:[a;r5]:[a;r5]:[a;r5]:1",
)
PROLIF_REFERENCE = {
    "software": "ProLIF", "version": "2.2.2",
    "commit": "19f1800218387c49536eb9d3e8cd3044fdb337ee",
    "implementation": "https://github.com/chemosim-lab/ProLIF/blob/19f1800218387c49536eb9d3e8cd3044fdb337ee/prolif/interactions/interactions.py",
    "geometry": "https://github.com/chemosim-lab/ProLIF/blob/19f1800218387c49536eb9d3e8cd3044fdb337ee/prolif/utils.py",
    "paper": "https://doi.org/10.1186/s13321-021-00548-6",
}

# The original HBAcceptor/HBDonor defaults are chemical recognition rules.
PROLIF_HBOND_PATTERNS = (
    "[$([O,S,#7;+0]),$([Nv4+1]),$([n+]c[nH])]-[H]",
    "[$([N&!$([NX3]-*=[O,N,P,S])&!$([ND2v3^2+0](-[H])-[CD4v4H1^3]-[CD2^2+0]=O)"
    "&!$([NX3]-[a])&!$([Nv4+1])&!$(N=C(-[C,N])-N)])"
    ",$([n+0&!X3&!$([n&r5]:[n+&r5])])"
    ",$([O&!$([OX2](C)C=O)&!$(O(~a)~a)&!$(O=N-*)&!$([O-]-N=O)])"
    ",$([o+0])"
    ",$([F&$(F-[#6])&!$(F-[#6][F,Cl,Br,I])])]",
)
