"""Keep independent RDKit CTAB output with explicit fixed-state hydrogen evidence."""

import shlex


def rdkit_v3000_with_declared_valences(molecule):
    """Add missing VAL fields without replacing conflicting writer chemistry."""
    from rdkit import Chem

    lines = Chem.MolToV3KMolBlock(molecule).splitlines(keepends=True)
    in_atoms = False
    for index, line in enumerate(lines):
        body = line.rstrip("\r\n")
        if body == "M  V30 BEGIN ATOM":
            in_atoms = True
        elif body == "M  V30 END ATOM":
            in_atoms = False
        elif in_atoms:
            fields = shlex.split(body)
            atom_index = int(fields[2]) - 1
            valence = molecule.GetAtomWithIdx(atom_index).GetTotalValence()
            expected = valence if valence else -1
            declared = [field[4:] for field in fields[8:] if field.startswith("VAL=")]
            if len(declared) > 1:
                raise ValueError(
                    f"Repeated VAL on RDKit reference atom {atom_index + 1}."
                )
            if declared:
                if int(declared[0]) != expected:
                    raise ValueError(
                        f"Writer VAL={declared[0]} conflicts with declared "
                        f"VAL={expected} on reference atom {atom_index + 1}."
                    )
            else:
                ending = line[len(body) :]
                lines[index] = f"{body} VAL={expected}{ending}"
    return "".join(lines)
