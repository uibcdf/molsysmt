"""Generate offline observations with unmodified ProLIF 2.2.2.

Install the reference only in an isolated development directory and put it on
PYTHONPATH. ProLIF is not a MolSysMT production or default-test dependency.
"""

import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np


def reference_cases():
    cases = []
    grid = [
        (0.30, 180.0, 120.0),
        (0.349, 131.0, 81.0),
        (0.35, 130.0, 80.0),
        (0.351, 180.0, 120.0),
        (0.30, 129.0, 120.0),
        (0.30, 180.0, 79.0),
        (0.30, 180.0, 141.0),
        (0.30, 179.0, 139.0),
        (0.30, 140.0, 90.0),
    ]
    for smiles in ("CCl.C=O", "CBr.C=O", "CI.C=O", "CF.C=O", "CCl.N#C", "CCl.C[NH3+]"):
        coordinates = []
        for distance, donor, acceptor in grid:
            theta, phi = np.deg2rad([donor, 180 - acceptor])
            coordinates.append(
                [
                    [0.15 * np.cos(theta), 0.15 * np.sin(theta), 0],
                    [0, 0, 0],
                    [distance + 0.12 * np.cos(phi), 0.12 * np.sin(phi), 0],
                    [distance, 0, 0],
                ]
            )
        cases.append(
            dict(
                smiles=smiles,
                coordinates_nm=coordinates,
                boundary_structure_indices=[2],
            )
        )
    cases.append(
        dict(
            smiles="CCl.COC",
            coordinates_nm=[
                [
                    [-0.15, 0, 0],
                    [0, 0, 0],
                    [0.36, 0.1, 0],
                    [0.3, 0, 0],
                    [0.36, -0.1, 0],
                ],
                [[-0.15, 0, 0], [0, 0, 0], [0.36, 0.1, 0], [0.3, 0, 0], [0.18, 0, 0]],
            ],
        )
    )
    return cases


def generate(filename):
    import prolif
    from rdkit import Chem, rdBase

    if prolif.__version__ != "2.2.2":
        raise ValueError("Use unmodified ProLIF 2.2.2 for this oracle.")
    detector = prolif.interactions.XBAcceptor()
    cases = reference_cases()
    for case in cases:
        molecule = Chem.MolFromSmiles(case["smiles"])
        observations = []
        for frame, xyz in enumerate(case["coordinates_nm"]):
            source = Chem.Mol(molecule)
            conformer = Chem.Conformer(source.GetNumAtoms())
            conformer.SetPositions(np.asarray(xyz) * 10)
            source.AddConformer(conformer)
            reference = prolif.Molecule.from_rdkit(source)
            for item in detector.detect(reference, reference):
                observations.append(
                    dict(
                        structure_index=frame,
                        donor_halogen=list(item["indices"]["protein"]),
                        acceptor_reference=list(item["indices"]["ligand"]),
                        distance_nm=item["distance"] / 10,
                        donor_angle_radians=np.deg2rad(item["AXD_angle"]),
                        acceptor_angle_radians=np.deg2rad(item["XAR_angle"]),
                    )
                )
        case["observations"] = sorted(
            observations,
            key=lambda row: (
                row["structure_index"],
                row["donor_halogen"],
                row["acceptor_reference"],
            ),
        )
    import prolif.interactions.base as base
    import prolif.interactions.interactions as interactions

    hashes = {
        name: hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
        for name, module in (("interactions.py", interactions), ("base.py", base))
    }
    result = dict(
        reference="ProLIF XBAcceptor/DoubleAngle",
        version=prolif.__version__,
        method_commit="19f1800218387c49536eb9d3e8cd3044fdb337ee",
        source_sha256=hashes,
        rdkit_version=rdBase.rdkitVersion,
        python_version=platform.python_version(),
        system=platform.platform(),
        coordinate_unit="nm",
        cases=cases,
    )
    Path(filename).write_text(json.dumps(result, indent=2) + "\n")
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
