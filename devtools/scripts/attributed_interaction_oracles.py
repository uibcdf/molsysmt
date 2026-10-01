"""Generate fixed decisions by executing original scientific reference cores.

Requires original ProLIF 2.2.2, MDTraj, MDAnalysis, RDKit, CPPTRAJ and esbuild.
Reference packages are developer dependencies, never production dependencies.
Mol* geometry is executed from unchanged tester excerpts plus original Vec3;
this does not execute Mol* feature discovery or contact refinement.
"""

import argparse
import hashlib
import importlib.util
import inspect
import json
import platform
import re
import shutil
import subprocess
import tempfile
from importlib.metadata import version
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]


def load_original(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_record(path):
    return dict(file=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def rdkit_source(smiles, coordinates):
    from rdkit import Chem

    molecule = Chem.MolFromSmiles(smiles)
    molecule.RemoveAllConformers()
    for frame in coordinates:
        conformer = Chem.Conformer(molecule.GetNumAtoms())
        conformer.SetPositions(np.asarray(frame) * 10)
        molecule.AddConformer(conformer, assignId=True)
    return molecule


def mdtraj_source(molecule, coordinates):
    import mdtraj as md

    top = md.Topology()
    residue = top.add_residue("RES", top.add_chain())
    for atom in molecule.GetAtoms():
        top.add_atom(f"a{atom.GetIdx()}", md.element.get_by_symbol(atom.GetSymbol()), residue)
    for bond in molecule.GetBonds():
        top.add_bond(top.atom(bond.GetBeginAtomIdx()), top.atom(bond.GetEndAtomIdx()))
    return md.Trajectory(np.asarray(coordinates), top)


def pi_cases():
    angles = np.arange(6) * np.pi / 3
    ring = np.column_stack((.14 * np.cos(angles), .14 * np.sin(angles), np.zeros(6)))
    frames = []
    for distance in (.35, .54, .56, .64, .66):
        for angle in (0, 29, 39, 51, 74, 89):
            theta = np.deg2rad(angle)
            rotation = np.array([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])
            for x in (0, .14, .21):
                frames.append(np.concatenate((ring, ring @ rotation.T + [x, 0, distance])))
    theta = np.deg2rad(89)
    edge = ring @ np.array([[np.cos(theta), 0, -np.sin(theta)], [0, 1, 0], [np.sin(theta), 0, np.cos(theta)]]) + [0, .19, .4]
    frames.extend((np.concatenate((ring, edge)), np.concatenate((edge, ring))))
    warped = ring.copy()
    warped[:, 2] = [.02, -.02, .03, -.03, .01, -.01]
    frames.append(np.concatenate((ring, warped + [0, 0, .35])))
    return [dict(name="benzene_orientation_distance_offset", smiles="c1ccccc1.c1ccccc1",
                 coordinates_nm=np.asarray(frames).tolist(), ring_a=list(range(6)), ring_b=list(range(6, 12)))]


def cation_cases():
    ring = np.asarray(pi_cases()[0]["coordinates_nm"])[0, :6]
    points = [(x, 0, z) for z in (.15, .35, .59, .61, -.35) for x in (.0, .19, .21)]
    warped = ring.copy()
    warped[:, 2] = [.02, -.02, .03, -.03, .01, -.01]
    frames = [np.vstack((ring, point)) for point in points] + [np.vstack((warped, [0, 0, .35]))]
    return [dict(name="cation_offset_and_warped_ring", smiles="c1ccccc1.[Na+]",
                 coordinates_nm=np.asarray(frames).tolist(), ring=list(range(6)), cation=[6])]


def hbond_cases():
    from rdkit import Chem
    from rdkit.Chem import rdDepictor

    cases = []
    for name, smiles in (("water", "O.O"), ("amide", "NC(=O)N.O"),
                         ("thiol", "S.O"), ("fluoride", "F.O"), ("aromatic_nh", "c1cc[nH]c1.O")):
        molecule = Chem.AddHs(Chem.MolFromSmiles(smiles))
        # Explicit H SMILES fixes the source atom order independently of converters.
        fixed_smiles = Chem.MolToSmiles(molecule, canonical=False, allHsExplicit=True)
        params = Chem.SmilesParserParams()
        params.removeHs = False
        molecule = Chem.MolFromSmiles(fixed_smiles, params)
        rdDepictor.Compute2DCoords(molecule)
        coordinates = np.asarray(molecule.GetConformer().GetPositions()) / 10
        donor = next(atom.GetIdx() for atom in molecule.GetAtoms()
                     if atom.GetSymbol() in {"O", "N", "S", "F"}
                     and any(neighbor.GetSymbol() == "H" for neighbor in atom.GetNeighbors()))
        hydrogen = next(atom.GetIdx() for atom in molecule.GetAtomWithIdx(donor).GetNeighbors() if atom.GetSymbol() == "H")
        fragments = Chem.GetMolFrags(molecule)
        acceptor = next(i for i in fragments[-1] if molecule.GetAtomWithIdx(i).GetSymbol() == "O")
        coordinates -= coordinates[donor]
        coordinates[hydrogen] = [.1, 0, 0]
        frames = []
        for ha in (.15, .249, .251, .29, .32):
            for dha in (100, 121, 129, 131, 134, 136, 149, 151, 179):
                frame = coordinates.copy()
                theta = np.deg2rad(180 - dha)
                target = [.1 + ha * np.cos(theta), ha * np.sin(theta), 0]
                frame[list(fragments[-1])] += np.asarray(target) - frame[acceptor]
                frames.append(frame)
        all_pairs = sorted((neighbor.GetIdx(), atom.GetIdx()) for atom in molecule.GetAtoms()
                           if atom.GetSymbol() == "H" for neighbor in atom.GetNeighbors()
                           if neighbor.GetSymbol() != "H")
        all_acceptors = [atom.GetIdx() for atom in molecule.GetAtoms() if atom.GetSymbol() in {"O", "N"}]
        cases.append(dict(name=name, smiles=fixed_smiles, explicit_hydrogens=True,
                          coordinates_nm=np.asarray(frames).tolist(),
                          explicit_donor_hydrogen_pairs=all_pairs, explicit_acceptor_atom_indices=all_acceptors))
    return cases


def read_molecule(case):
    from rdkit import Chem

    params = Chem.SmilesParserParams()
    params.removeHs = not case.get("explicit_hydrogens", False)
    return Chem.MolFromSmiles(case["smiles"], params)


def prolif_pi(case):
    import prolif
    from rdkit import Chem

    molecule = read_molecule(case)
    records = []
    for frame, xyz in enumerate(case["coordinates_nm"]):
        copy = Chem.Mol(molecule)
        conformer = Chem.Conformer(copy.GetNumAtoms())
        conformer.SetPositions(np.asarray(xyz) * 10)
        copy.AddConformer(conformer)
        fragments = Chem.GetMolFrags(copy, asMols=True)
        first, second = [prolif.Molecule.from_rdkit(fragment) for fragment in fragments]
        for kind, detector in (("parallel", prolif.interactions.FaceToFace()), ("edge_to_face", prolif.interactions.EdgeToFace())):
            for item in detector.detect(first, second):
                records.append(dict(structure_index=frame, geometry=kind,
                                    ring_a=list(item["indices"]["ligand"]),
                                    ring_b=[i + 6 for i in item["indices"]["protein"]],
                                    distance_nm=item["distance"] / 10))
    return records


def cpptraj_hbonds(molecule, coordinates, executable, work):
    """Execute CPPTRAJ itself and decode its individual solute time series."""
    trajectory = mdtraj_source(molecule, coordinates)
    top = work / "source.mol2"
    atom_lines = []
    for atom, xyz in zip(molecule.GetAtoms(), np.asarray(coordinates)[0] * 10):
        i = atom.GetIdx()
        symbol = atom.GetSymbol()
        tripos = {"O": "O.3", "N": "N.3", "C": "C.3", "S": "S.3"}.get(symbol, symbol)
        atom_lines.append(f"{i + 1} {symbol}{i} {xyz[0]} {xyz[1]} {xyz[2]} {tripos} 1 RES 0.0")
    bonds = [f"{i + 1} {bond.GetBeginAtomIdx() + 1} {bond.GetEndAtomIdx() + 1} 1" for i, bond in enumerate(molecule.GetBonds())]
    top.write_text(f"@<TRIPOS>MOLECULE\nreference\n{molecule.GetNumAtoms()} {len(bonds)} 1 0 0\nSMALL\nUSER_CHARGES\n\n@<TRIPOS>ATOM\n"
                   + "\n".join(atom_lines) + "\n@<TRIPOS>BOND\n" + "\n".join(bonds) + "\n@<TRIPOS>SUBSTRUCTURE\n1 RES 1\n")
    trajectory.save_netcdf(str(work / "frames.nc"))
    (work / "input").write_text(f"parm {top}\ntrajin {work / 'frames.nc'}\nhbond HB series avgout {work / 'average'} uuseries {work / 'series'} printatomnum\nrun\n")
    run = subprocess.run([executable, "-i", str(work / "input")], text=True, capture_output=True, check=True)
    if "V6.24.0" not in run.stdout:
        raise ValueError("This CPPTRAJ oracle is pinned to V6.24.0.")
    if not (work / "series").exists():
        if "0 solute-solute hydrogen bonds." not in run.stdout:
            raise ValueError("CPPTRAJ did not produce its series or a verified zero-observation analysis: " + run.stdout + run.stderr)
        return []
    lines = (work / "series").read_text().splitlines()
    columns = []
    for label in lines[0].split()[1:]:
        match = re.search(r"@[A-Za-z]+(\d+)-.*@[A-Za-z]+(\d+)-[A-Za-z]+(\d+)", label)
        if match is None:
            raise ValueError(f"Unrecognized CPPTRAJ label: {label}")
        a, d, h = map(int, match.groups())
        columns.append([d, h, a])
    records = []
    for line in lines[1:]:
        values = list(map(int, line.split()))
        for triple, present in zip(columns, values[1:]):
            if present:
                records.append(dict(structure_index=values[0] - 1, atoms=triple))
    return records


def hbond_originals(case, hb, mda_hb, cpptraj, work):
    import MDAnalysis as mda
    import prolif
    from rdkit import Chem

    molecule = read_molecule(case)
    xyz = np.asarray(case["coordinates_nm"])
    traj = mdtraj_source(molecule, xyz)
    decisions = {}
    decisions["baker_hubbard"] = [dict(structure_index=frame, atoms=triple.tolist())
                                  for frame in range(len(xyz))
                                  for triple in hb.baker_hubbard(traj[frame:frame + 1], freq=0, exclude_water=False, periodic=False)]
    decisions["wernet_nilsson"] = [dict(structure_index=frame, atoms=triple.tolist())
                                   for frame, rows in enumerate(hb.wernet_nilsson(traj, exclude_water=False, periodic=False)) for triple in rows]
    decisions["cpptraj"] = cpptraj_hbonds(molecule, xyz, cpptraj, work)
    universe = mda.Universe.empty(molecule.GetNumAtoms(), trajectory=True)
    universe.add_TopologyAttr("bonds", [(bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()) for bond in molecule.GetBonds()])
    universe.load_new(xyz * 10)
    hydrogens = sorted({pair[1] for pair in case["explicit_donor_hydrogen_pairs"]})
    analysis = mda_hb.HydrogenBondAnalysis(universe, donors_sel=None,
                                         hydrogens_sel="index " + " ".join(map(str, hydrogens)),
                                         acceptors_sel="index " + " ".join(map(str, case["explicit_acceptor_atom_indices"])),
                                         update_selections=False).run()
    decisions["mdanalysis_geometry"] = [dict(structure_index=int(row[0]), atoms=list(map(int, row[1:4]))) for row in analysis.results.hbonds]
    rows = []
    for frame, coordinates in enumerate(xyz):
        copy = Chem.Mol(molecule)
        conformer = Chem.Conformer(copy.GetNumAtoms())
        conformer.SetPositions(coordinates * 10)
        copy.AddConformer(conformer)
        source = prolif.Molecule.from_rdkit(copy)
        for item in prolif.interactions.HBDonor().detect(source, source):
            rows.append(dict(structure_index=frame, atoms=list(item["indices"]["ligand"]) + list(item["indices"]["protein"])))
    decisions["prolif"] = rows
    return decisions


def braced(text, marker):
    start = text.index(marker)
    opening = text.index("{", start)
    level = 1
    index = opening + 1
    while level:
        level += (text[index] == "{") - (text[index] == "}")
        index += 1
    return text[start:index]


def molstar_originals(root, cases, esbuild, work):
    charged_path = root / "src/mol-model-props/computed/interactions/charged.ts"
    charged = charged_path.read_text()
    common = (charged_path.parent / "common.ts").read_text()
    features_path = charged_path.parent / "features.ts"
    features = features_path.read_text()
    vector = root / "src/mol-math/linear-algebra/3d/vec3.ts"
    # Excerpts are unchanged executable source; only export visibility is adapted.
    fragments = [braced(common, "export enum InteractionType"), braced(common, "export const enum FeatureType")]
    fragments += [braced(charged, marker) for marker in ("function isPiStacking", "function isCationPi", "function getNormal", "const getOffset = function", "function testPiStacking", "function testCationPi")]
    fragments.append(braced(features, "export function position").replace("export function", "function", 1))
    preamble = f"import {{ Vec3 }} from {json.dumps(str(vector))};\n"
    preamble += "const Features = {position}; const deg180InRad=Math.PI, deg90InRad=Math.PI/2;\nconst tmpVecA=Vec3(), tmpVecB=Vec3(), tmpVecC=Vec3(), tmpVecD=Vec3(), tmpNormalA=Vec3(), tmpNormalB=Vec3();\n"
    wrapper = r'''
import {readFileSync, writeFileSync} from 'node:fs';
const cases=JSON.parse(readFileSync(process.argv[2],'utf8'));
function info(xyz, members, type) {
  const center=members.map(i=>xyz[i]).reduce((sum,p)=>sum.map((v,j)=>v+p[j]/members.length),[0,0,0]);
  return {feature:0,types:[type],offsets:[0,members.length],members,x:[center[0]],y:[center[1]],z:[center[2]],
    unit:{elements:xyz.map((_,i)=>i),conformation:{position:(i,out)=>{for(let j=0;j<3;j++)out[j]=xyz[i][j];return out;},operator:{matrix:[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]}}}};
}
const results=cases.map(test=>test.coordinates_nm.map((frame,index)=>{
 const xyz=frame.map(point=>point.map(v=>v*10));
 const ring=info(xyz,test.ring || test.ring_a,FeatureType.AromaticRing);
 const second=info(xyz,test.cation || test.ring_b,test.cation ? FeatureType.PositiveCharge : FeatureType.AromaticRing);
 const dx=ring.x[0]-second.x[0],dy=ring.y[0]-second.y[0],dz=ring.z[0]-second.z[0];
 const dist2=dx*dx+dy*dy+dz*dz;
 // The original contact builder bounds tester calls by the centroid cutoff.
 const cutoff=test.cation ? 6 : 5.5;
 const detected=test.cation ? testCationPi({},ring,second,dist2,{offsetMax:2}) : testPiStacking({},ring,second,dist2,{offsetMax:2,angleDevMax:Math.PI/6});
 return {structure_index:index,present:dist2<=cutoff*cutoff && detected!==undefined};
}));
writeFileSync(process.argv[3],JSON.stringify(results));
'''
    source = work / "molstar-reference.ts"
    source.write_text(preamble + "\n".join(fragments) + wrapper)
    subprocess.run([esbuild, str(source), "--bundle", "--platform=node", "--format=cjs", f"--outfile={work / 'reference.cjs'}"], check=True, capture_output=True)
    (work / "input.json").write_text(json.dumps(cases))
    subprocess.run(["node", str(work / "reference.cjs"), str(work / "input.json"), str(work / "output.json")], check=True)
    return json.loads((work / "output.json").read_text()), [source_record(path) for path in (charged_path, features_path, vector)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--references", type=Path, required=True, help="Directory containing mdtraj, mdanalysis and molstar source checkouts.")
    parser.add_argument("--cpptraj", default="cpptraj")
    parser.add_argument("--esbuild", required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "devtools/data/attributed_interaction_oracles.json")
    args = parser.parse_args()
    import prolif

    if prolif.__version__ != "2.2.2":
        raise ValueError("The ProLIF oracle requires unmodified 2.2.2.")
    hb_path = args.references / "mdtraj/mdtraj/geometry/hbond.py"
    pi_path = hb_path.parent / "pi_stacking.py"
    mda_path = args.references / "mdanalysis/package/MDAnalysis/analysis/hydrogenbonds/hbond_analysis.py"
    hb = load_original(hb_path, "reference_mdtraj_hbonds")
    pi = load_original(pi_path, "reference_mdtraj_pi")
    mda_hb = load_original(mda_path, "MDAnalysis.analysis.hydrogenbonds.reference_hbond_analysis")
    rings, cations, hbonds = pi_cases(), cation_cases(), hbond_cases()
    with tempfile.TemporaryDirectory(prefix="molsysmt-reference-") as temporary:
        work = Path(temporary)
        for case in rings:
            case["prolif"] = prolif_pi(case)
            result = pi.pi_stacking(mdtraj_source(read_molecule(case), case["coordinates_nm"]),
                                    [tuple(case["ring_a"])], [tuple(case["ring_b"])])
            case["mdtraj_geometry"] = [dict(structure_index=frame, ring_a=list(a), ring_b=list(b))
                                       for frame, rows in enumerate(result) for a, b in rows]
        molstar_rows, molstar_sources = molstar_originals(args.references / "molstar", rings + cations, args.esbuild, work)
        for case, rows in zip(rings + cations, molstar_rows):
            case["molstar_geometry"] = [row["structure_index"] for row in rows if row["present"]]
        for case in hbonds:
            case_work = work / case["name"]
            case_work.mkdir()
            case["observations"] = hbond_originals(case, hb, mda_hb, args.cpptraj, case_work)
    payload = dict(schema_version="molsysmt.attributed-interaction-oracles@1", produced="2026-10-01",
                   python=platform.python_version(), runtimes={name: version(name) for name in ("mdtraj", "MDAnalysis", "rdkit", "prolif")},
                   cpptraj=dict(version="V6.24.0", commit="0793fd579c5bb41377462d70df0b249a48bc9eb7",
                                binary_sha256=source_record(Path(shutil.which(args.cpptraj) or args.cpptraj))["sha256"]),
                   precision="float64 in ProLIF/Mol*; float32 trajectory coordinates in MDTraj/MDAnalysis/CPPTRAJ",
                   boundary_policy="External decision grids avoid exact angle/offset boundaries; analytic tests cover exact endpoints separately.",
                   sources=[source_record(path) for path in (hb_path, pi_path, mda_path, Path(inspect.getsourcefile(prolif.interactions.FaceToFace)))] + molstar_sources,
                   scope="original_chemical_cores_and_supplied_feature_geometry_no_full_fingerprints_or_refinement",
                   pi_pi=rings, cation_pi=cations, hbonds=hbonds)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Generated {args.output.name}: pi-pi {len(rings)}, cation-pi {len(cations)}, hbond {len(hbonds)} cases.")


if __name__ == "__main__":
    main()
