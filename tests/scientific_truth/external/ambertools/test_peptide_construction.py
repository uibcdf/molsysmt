"""Native peptide graphs against directly scripted Amber LEaP, without a converter oracle."""

import shutil
import subprocess

import pytest

import molsysmt as msm


@pytest.mark.parametrize(
    "sequence,residue_names",
    [("GA", "GLY ALA"), ("GP", "GLY PRO"), ("ACEALAALANME", "ACE ALA ALA NME")],
)
def test_native_peptide_graph_agrees_with_independent_leap(
    tmp_path, sequence, residue_names
):
    parmed = pytest.importorskip("parmed")
    executable = shutil.which("tleap")
    if executable is None:
        pytest.skip("Amber LEaP is required for the independent peptide oracle")
    script = tmp_path / "oracle.leap"
    script.write_text(
        f"source leaprc.protein.ff14SB\nreference = sequence {{ {residue_names} }}\nsaveamberparm reference oracle.prmtop oracle.inpcrd\nquit\n"
    )
    completed = subprocess.run(
        [executable, "-s", "-f", script.name],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert (tmp_path / "oracle.prmtop").is_file(), completed.stdout + completed.stderr
    reference = parmed.load_file(
        str(tmp_path / "oracle.prmtop"), xyz=str(tmp_path / "oracle.inpcrd")
    )
    expected_atoms = [(atom.residue.idx, atom.name) for atom in reference.atoms]
    expected_bonds = {
        tuple(
            sorted(
                (
                    (bond.atom1.residue.idx, bond.atom1.name),
                    (bond.atom2.residue.idx, bond.atom2.name),
                )
            )
        )
        for bond in reference.bonds
    }
    native = msm.build.build_peptide(sequence, engine="MolSysMT")
    atoms = [
        (int(row.group_index), row.atom_name)
        for row in native.topology.atoms.itertuples()
    ]
    assert sorted(atoms) == sorted(expected_atoms)
    pairs = native.chemical_states.get_bonds()[["atom1_index", "atom2_index"]].to_numpy(
        dtype=int
    )
    observed_bonds = {
        tuple(sorted((atoms[first], atoms[second]))) for first, second in pairs
    }
    assert observed_bonds == expected_bonds
