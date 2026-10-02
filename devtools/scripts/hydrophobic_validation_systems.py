"""Generate hydrophobic-site and pair oracles with unmodified ProLIF 2.2.2.

Run with an isolated reference installation on PYTHONPATH. Default MolSysMT
tests consume only the resulting offline JSON and never import ProLIF.
"""

import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np


def generate(filename):
    import prolif
    import prolif.interactions.base as base
    import prolif.interactions.interactions as interactions
    from rdkit import Chem, rdBase

    if prolif.__version__ != "2.2.2":
        raise ValueError("Use unmodified ProLIF 2.2.2 for this oracle.")
    detector = prolif.interactions.Hydrophobic()
    cases = []
    for smiles, explicit in [
        ("CCC.CCC", False),
        ("CCC.CSC", False),
        ("CC.CF.C[NH3+]", False),
        ("c1ccccc1.c1ccccc1", False),
        ("n1ccccc1.[Br-].CCO.Br.I.CS.CSC", False),
        ("CCOC.CC(=O)O", False),
        ("CCC.CSC", True),
    ]:
        molecule = Chem.MolFromSmiles(smiles)
        if explicit:
            molecule = Chem.AddHs(molecule)
        fragments = Chem.GetMolFrags(molecule)
        n_atoms = molecule.GetNumAtoms()
        coordinates, observations = [], []
        for frame, offset in enumerate((0.30, 0.70, 0.449)):
            xyz = np.zeros((n_atoms, 3), dtype=np.float64)
            for i, fragment in enumerate(fragments):
                xyz[list(fragment), 0] = np.arange(len(fragment)) * 0.137
                xyz[list(fragment), 1] = offset * i
            coordinates.append(xyz.tolist())
            source = Chem.Mol(molecule)
            conformer = Chem.Conformer(n_atoms)
            conformer.SetPositions(xyz * 10)
            source.AddConformer(conformer)
            reference = prolif.Molecule.from_rdkit(source)
            sites = sorted(
                match[0]
                for match in reference.GetSubstructMatches(detector.lig_pattern)
            )
            for item in detector.detect(reference, reference):
                a, b = item["indices"]["ligand"][0], item["indices"]["protein"][0]
                # MolSysMT's explicit single-source adaptation: distinct unordered
                # atoms only; this does not change reference site membership.
                if a < b:
                    observations.append(
                        dict(
                            structure_index=frame,
                            atoms=[a, b],
                            distance_nm=item["distance"] / 10,
                        )
                    )
        cases.append(
            dict(
                smiles=smiles,
                add_hydrogens=explicit,
                hydrophobic_atom_indices=sites,
                coordinates_nm=coordinates,
                observations=observations,
            )
        )
    hashes = {
        name: hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
        for name, module in [("interactions.py", interactions), ("base.py", base)]
    }
    payload = dict(
        reference="ProLIF Hydrophobic/Distance",
        version=prolif.__version__,
        method_commit="19f1800218387c49536eb9d3e8cd3044fdb337ee",
        source_sha256=hashes,
        rdkit_version=rdBase.rdkitVersion,
        python_version=platform.python_version(),
        system=platform.platform(),
        coordinate_unit="nm",
        adaptation="distinct_unordered_single_source_pairs",
        cases=cases,
    )
    Path(filename).write_text(json.dumps(payload, indent=2) + "\n")
    print(
        json.dumps(
            dict(
                cases=len(cases),
                structures=sum(len(c["coordinates_nm"]) for c in cases),
                observations=sum(len(c["observations"]) for c in cases),
                source_sha256=hashes,
            )
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filename")
    generate(parser.parse_args().filename)
