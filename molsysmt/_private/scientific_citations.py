"""Offline bibliographic declarations owned by MolSysMT's scientific methods.

Audited on 2026-10-01 against the linked publications and project citation
instructions. Author lists are complete; initials are preserved when that is
what the source supplies. Declaration never records runtime use.
"""

ARTICLES = {
    "baker_hubbard": dict(
        doi="10.1016/0079-6107(84)90007-5", title="Hydrogen bonding in globular proteins",
        authors=["Baker, E. N.", "Hubbard, R. E."], year=1984,
        journal="Progress in Biophysics and Molecular Biology", volume="44", pages="97-179"),
    "wernet_nilsson": dict(
        doi="10.1126/science.1096205", title="The Structure of the First Coordination Shell in Liquid Water",
        authors=["Wernet, Ph.", "Nordlund, D.", "Bergmann, U.", "Cavalleri, M.",
                 "Odelius, M.", "Ogasawara, H.", "Näslund, L. A.", "Hirsch, T. K.",
                 "Ojamäe, L.", "Glatzel, P.", "Pettersson, L. G. M.", "Nilsson, A."],
        year=2004, journal="Science", volume="304", pages="995-999"),
    "luzar_chandler": dict(
        doi="10.1038/379055a0", title="Hydrogen-bond kinetics in liquid water",
        authors=["Luzar, Alenka", "Chandler, David"], year=1996,
        journal="Nature", volume="379", pages="55-57"),
    "prolif": dict(
        doi="10.1186/s13321-021-00548-6", title="ProLIF: a library to encode molecular interactions as fingerprints",
        authors=["Bouysset, Cédric", "Fiorucci, Sébastien"], year=2021,
        journal="Journal of Cheminformatics", volume="13", pages="72"),
    "cpptraj": dict(
        doi="10.1021/ct400341p", title="PTRAJ and CPPTRAJ: Software for Processing and Analysis of Molecular Dynamics Trajectory Data",
        authors=["Roe, Daniel R.", "Cheatham III, Thomas E."], year=2013,
        journal="Journal of Chemical Theory and Computation", volume="9", pages="3084-3095"),
    "mdtraj": dict(
        doi="10.1016/j.bpj.2015.08.015", title="MDTraj: A Modern Open Library for the Analysis of Molecular Dynamics Trajectories",
        authors=["McGibbon, Robert T.", "Beauchamp, Kyle A.", "Harrigan, Matthew P.",
                 "Klein, Christoph", "Swails, Jason M.", "Hernández, Carlos X.",
                 "Schwantes, Christian R.", "Wang, Lee-Ping", "Lane, Thomas J.", "Pande, Vijay S."],
        year=2015, journal="Biophysical Journal", volume="109", pages="1528-1532"),
    "molstar": dict(
        doi="10.1093/nar/gkab314", title="Mol* Viewer: modern web app for 3D visualization and analysis of large biomolecular structures",
        authors=["Sehnal, David", "Bittrich, Sebastian", "Deshpande, Mandar",
                 "Svobodová, Radka", "Berka, Karel", "Bazgier, Václav", "Velankar, Sameer",
                 "Burley, Stephen K.", "Koča, Jaroslav", "Rose, Alexander S."],
        year=2021, journal="Nucleic Acids Research", volume="49", pages="W431-W437"),
}

# A project whose recommended citation is its website needs no invented paper
# or author list. RDKit asks additionally for the version used; the producer
# version is attached by the consumer, without resolving a moving release DOI.
SOFTWARE = {
    "molsysmt": dict(title="MolSysMT", authors=["Prada-Gracia, Diego", "Moreno-Vargas, Liliana M."],
                    doi="10.5281/zenodo.1298752", url="https://github.com/uibcdf/molsysmt"),
    "rdkit": dict(title="RDKit: Open-source cheminformatics", url="https://www.rdkit.org",
                  how_to_cite="https://www.rdkit.org/docs/Overview.html#citing-the-rdkit"),
}
