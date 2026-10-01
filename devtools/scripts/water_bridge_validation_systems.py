"""Generate single-water path truth using original ProLIF HBDonor observations.

This independently joins the reference legs, not MolSysMT detector output.
Use the isolated unmodified ProLIF 2.2.2 installation on PYTHONPATH.
"""

import argparse
import hashlib
import itertools
import json
import platform
from pathlib import Path

import numpy as np


def generate(filename):
    import prolif
    import prolif.interactions.base as base
    import prolif.interactions.interactions as interactions
    from rdkit import Chem, rdBase

    if prolif.__version__ != '2.2.2':
        raise ValueError('Use unmodified ProLIF 2.2.2.')
    detector = prolif.interactions.HBDonor()
    cases = []
    for smiles in ['O.C=O.C=O', 'O.N.N', 'O.N.C=O']:
        molecule = Chem.AddHs(Chem.MolFromSmiles(smiles))
        xyz = np.zeros((molecule.GetNumAtoms(), 3))
        xyz[:, 2] = np.arange(molecule.GetNumAtoms()) * 3 + 3
        water_h = sorted(a.GetIdx() for a in molecule.GetAtomWithIdx(0).GetNeighbors())
        xyz[0], xyz[water_h] = [0, 0, 0], [[.1, 0, 0], [0, .1, 0]]
        endpoints = []
        for position, fragment in enumerate(Chem.GetMolFrags(molecule)[1:]):
            nitrogen = [i for i in fragment if molecule.GetAtomWithIdx(i).GetSymbol() == 'N']
            axis = np.eye(3)[position]
            if nitrogen:
                donor = nitrogen[0]
                hydrogen = min(a.GetIdx() for a in molecule.GetAtomWithIdx(donor).GetNeighbors())
                xyz[donor], xyz[hydrogen] = -.3 * axis, -.2 * axis
                endpoints.append([donor, hydrogen, 0])
            else:
                acceptor = next(i for i in fragment if molecule.GetAtomWithIdx(i).GetSymbol() == 'O')
                xyz[acceptor] = .3 * axis
                endpoints.append([0, water_h[position], acceptor])
        observations, coordinates = [], []
        for frame in range(3):
            current = xyz.copy()
            if frame == 1:
                current[[i for i in endpoints[1] if i not in [0, *water_h]]] += 2
            coordinates.append(current.tolist())
            conformer = Chem.Conformer(molecule.GetNumAtoms())
            conformer.SetPositions(current * 10)
            source = Chem.Mol(molecule)
            source.AddConformer(conformer)
            reference = prolif.Molecule.from_rdkit(source)
            legs = []
            for item in detector.detect(reference, reference):
                d, h = item['indices']['ligand']
                a = item['indices']['protein'][0]
                if (d == 0) != (a == 0):
                    external = a if d == 0 else d
                    legs.append((external, (d, h, a), item['distance'] / 10, np.deg2rad(item['DHA_angle'])))
            for left, right in itertools.combinations(sorted(legs), 2):
                if left[0] != right[0]:
                    observations.append(dict(structure_index=frame, atoms=list(left[1] + right[1]),
                                             da_nm=[left[2], right[2]], dha_radians=[left[3], right[3]]))
        cases.append(dict(smiles=smiles, coordinates_nm=coordinates, observations=observations))
    hashes = {name: hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
              for name, module in [('interactions.py', interactions), ('base.py', base)]}
    payload = dict(reference='ProLIF HBDonor + independently enumerated two-leg single-water paths',
                   version=prolif.__version__, source_sha256=hashes, coordinate_unit='nm',
                   method_commit='19f1800218387c49536eb9d3e8cd3044fdb337ee',
                   rdkit_version=rdBase.rdkitVersion, python_version=platform.python_version(),
                   system=platform.platform(), cases=cases)
    Path(filename).write_text(json.dumps(payload, indent=2) + '\n')
    print(json.dumps(dict(cases=len(cases), structures=9, observations=sum(len(c['observations']) for c in cases))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filename')
    generate(parser.parse_args().filename)
