"""Reproduce fixed cation-pi truth with the original ProLIF release.

Run with ProLIF 2.2.2 available on PYTHONPATH to regenerate the committed oracle.
This developer fixture depends on ProLIF; the production detector does not.
"""

import argparse
import json
import platform
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'devtools/data/cation_pi_validation_systems.json'


def reference_cases():
    from rdkit import Chem
    from rdkit.Chem import rdDepictor

    cases = []
    for name, smiles in (
        ('benzene_ammonium', 'c1ccccc1.[NH4+]'),
        ('guanidinium_resonance', 'c1ccccc1.NC(=[NH2+])N'),
        ('furan_ammonium', 'o1cccc1.[NH4+]'),
        ('naphthalene_ammonium', 'c1ccc2ccccc2c1.[NH4+]'),
        ('opposite_charge_exclusion', 'c1ccccc1.[N+]([O-])(C)(C)C'),
        ('aromatic_nh', 'c1cc[nH]c1.[NH4+]'),
    ):
        molecule = Chem.MolFromSmiles(smiles)
        rdDepictor.Compute2DCoords(molecule)
        xyz = np.asarray(molecule.GetConformer().GetPositions()) / 10
        aromatic = np.flatnonzero([atom.GetIsAromatic() for atom in molecule.GetAtoms()])
        ring_center = xyz[aromatic].mean(axis=0)
        xyz -= ring_center
        tail = np.flatnonzero([not atom.GetIsAromatic() for atom in molecule.GetAtoms()])
        xyz[tail, :2] = np.linspace(-.03, .03, len(tail))[:, None] * [1, 0]
        xyz[tail, 2] = .35
        frames = []
        for displacement in ([0, 0, 0], [0, 0, .11], [.25, 0, 0], [0, 0, -.7]):
            frame = xyz.copy()
            frame[tail] += displacement
            frames.append(frame)
        cases.append(dict(name=name, smiles=smiles, coordinates_nm=np.asarray(frames).tolist(),
                          distance_nm=.45, angle_degrees=[0., 30.]))
    angles = np.arange(6) * np.pi / 3
    ring = np.column_stack((.14*np.cos(angles), .14*np.sin(angles), np.zeros(6)))
    frames = [np.vstack((ring, [x, 0, z])) for x, z in ((0, .449), (0, .451), (.17, .35), (.23, .35), (0, -.35), (.35, 0))]
    warped = ring.copy()
    warped[:, 2] = np.array([1, -1, 1, -1, 1, -1]) * .03
    frames.append(np.vstack((warped, [0, 0, .35])))
    cases.append(dict(name='analytical_and_warped', smiles='c1ccccc1.[NH4+]',
                      coordinates_nm=np.asarray(frames).tolist(), distance_nm=.45, angle_degrees=[0., 30.]))
    return cases


def original_observations(molecule, coordinates, *, distance_nm=.45, angle_degrees=(0., 30.)):
    """Execute unmodified original CationPi.detect on the same full-source graph."""
    import prolif
    from rdkit import Chem

    detector = prolif.interactions.CationPi(distance=distance_nm * 10, angle=angle_degrees)
    observations = []
    for frame, xyz in enumerate(coordinates):
        copy = Chem.Mol(molecule)
        copy.RemoveAllConformers()
        conformer = Chem.Conformer(copy.GetNumAtoms())
        conformer.SetPositions(np.asarray(xyz) * 10)
        copy.AddConformer(conformer)
        source = prolif.Molecule.from_rdkit(copy)
        for item in detector.detect(source, source):
            observations.append(dict(structure_index=frame,
                                     cation=list(item['indices']['ligand']), ring=list(item['indices']['protein']),
                                     distance_nm=item['distance']/10, normal_angle_radians=np.deg2rad(item['angle'])))
    return sorted(observations, key=lambda row: (row['structure_index'], row['cation'], sorted(row['ring'])))


def generate(path):
    import prolif
    from rdkit import Chem, rdBase

    if prolif.__version__ != '2.2.2':
        raise ValueError('The oracle is pinned to unmodified ProLIF 2.2.2.')
    cases = reference_cases()
    for case in cases:
        molecule = Chem.MolFromSmiles(case['smiles'])
        case['observations'] = original_observations(molecule, np.asarray(case['coordinates_nm']),
                                                     distance_nm=case['distance_nm'], angle_degrees=case['angle_degrees'])
    import sys
    sys.path.insert(0, str(ROOT))
    from devtools.scripts.ionic_validation_systems import prepare_system
    for name in ('trp_cage', 'villin'):
        _, reference, coordinates, molecule = prepare_system(name)
        for suffix, distance, angle in (('', .45, [0., 30.]), ('_geometry_control', .8, [0., 90.])):
            cases.append(dict(name=name + suffix, bundled_protein=name, path=reference['path'], sha256=reference['sha256'],
                              declared_state='devtools/data/ionic_validation_systems.json', distance_nm=distance,
                              angle_degrees=angle, observations=original_observations(
                                  molecule, coordinates, distance_nm=distance, angle_degrees=angle)))
    path.write_text(json.dumps(dict(schema_version='molsysmt.cation-pi-prolif-oracle@1',
                                   producer={'prolif': prolif.__version__, 'rdkit': rdBase.rdkitVersion,
                                             'python': platform.python_version(), 'date': '2026-10-01'},
                                   method_commit='19f1800218387c49536eb9d3e8cd3044fdb337ee',
                                   regeneration='python devtools/scripts/cation_pi_validation_systems.py --generate',
                                   scope='Original CationPi.detect on a full-source molecule; no residue preprocessing, PBC or fingerprint aggregation.',
                                   cases=cases), indent=2)+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--generate', action='store_true')
    args = parser.parse_args()
    if args.generate:
        generate(MANIFEST)
        print(f'Generated {MANIFEST.relative_to(ROOT)} using original ProLIF 2.2.2.')
