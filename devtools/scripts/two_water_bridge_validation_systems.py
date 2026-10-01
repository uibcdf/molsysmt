"""Generate independent two-water path truth from original ProLIF HBDonor.

The reference program enumerates simple heavy-atom paths of three observed
hydrogen bonds. It neither imports MolSysMT nor calls its path construction.
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
    for left_donates, right_donates, middle_forward in itertools.product([False, True], repeat=3):
        molecule = Chem.AddHs(Chem.MolFromSmiles('O.O.N.N'))
        xyz = np.zeros((molecule.GetNumAtoms(), 3))
        xyz[:, 2] = np.arange(molecule.GetNumAtoms()) * 3 + 3
        xyz[:4] = [[0, 0, 0], [.3, 0, 0], [-.3, 0, 0], [.6, 0, 0]]
        hs = [sorted(a.GetIdx() for a in molecule.GetAtomWithIdx(i).GetNeighbors()) for i in range(4)]
        xyz[hs[0]], xyz[hs[1]] = [[0, .1, 0], [0, -.1, 0]], [[.3, .1, 0], [.3, -.1, 0]]
        xyz[hs[2][0] if left_donates else hs[0][0]] = [-.2 if left_donates else -.1, 0, 0]
        xyz[hs[3][0] if right_donates else hs[1][0]] = [.5 if right_donates else .4, 0, 0]
        middle_h = hs[0][1] if middle_forward else hs[1][1]
        xyz[middle_h] = [.1 if middle_forward else .2, 0, 0]
        observations, coordinates = [], []
        for frame in range(3):
            current = xyz.copy()
            if frame == 1:
                current[middle_h] += [2, 2, 2]
            coordinates.append(current.tolist())
            conformer = Chem.Conformer(molecule.GetNumAtoms())
            conformer.SetPositions(current * 10)
            source = Chem.Mol(molecule)
            source.AddConformer(conformer)
            reference = prolif.Molecule.from_rdkit(source)
            # Enumerate at most three-edge simple graph walks, independently of
            # MolSysMT's grouped water-edge fan-out implementation.
            adjacency = {}
            for item in detector.detect(reference, reference):
                d, h = item['indices']['ligand']
                a = item['indices']['protein'][0]
                leg = dict(atoms=(d, h, a), da=item['distance'] / 10,
                           dha=float(np.deg2rad(item['DHA_angle'])))
                adjacency.setdefault(d, []).append((a, leg))
                adjacency.setdefault(a, []).append((d, leg))
            for start in [2, 3]:
                stack = [(start, [start], [])]
                while stack:
                    node, visited, legs = stack.pop()
                    if len(legs) == 3:
                        if node in [2, 3] and start < node and set(visited[1:-1]) == {0, 1}:
                            observations.append(dict(structure_index=frame,
                                atoms=[atom for leg in legs for atom in leg['atoms']],
                                da_nm=[leg['da'] for leg in legs], dha_radians=[leg['dha'] for leg in legs]))
                        continue
                    for neighbor, leg in adjacency.get(node, []):
                        if neighbor not in visited:
                            stack.append((neighbor, [*visited, neighbor], [*legs, leg]))
        observations.sort(key=lambda row: (row['structure_index'], row['atoms']))
        cases.append(dict(name=f'left_{left_donates}_right_{right_donates}_forward_{middle_forward}',
                          smiles='O.O.N.N', coordinates_nm=coordinates, observations=observations))
    hashes = {name: hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
              for name, module in [('interactions.py', interactions), ('base.py', base)]}
    payload = dict(reference='ProLIF HBDonor + independently enumerated three-edge simple paths',
                   version=prolif.__version__, source_sha256=hashes, coordinate_unit='nm',
                   method_commit='19f1800218387c49536eb9d3e8cd3044fdb337ee',
                   rdkit_version=rdBase.rdkitVersion, python_version=platform.python_version(),
                   system=platform.platform(), cases=cases)
    Path(filename).write_text(json.dumps(payload, indent=2) + '\n')
    print(json.dumps(dict(cases=len(cases), structures=sum(len(c['coordinates_nm']) for c in cases),
                         observations=sum(len(c['observations']) for c in cases))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filename')
    generate(parser.parse_args().filename)
