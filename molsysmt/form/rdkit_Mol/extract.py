from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='rdkit.Mol')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    if is_all(atom_indices) and is_all(structure_indices):
        if copy_if_all:
            from rdkit import Chem

            return Chem.Mol(item)
        return item

    from rdkit import Chem

    output = Chem.Mol(item)
    if not is_all(atom_indices):
        selected = [int(index) for index in atom_indices]
        remaining = [index for index in range(item.GetNumAtoms()) if index not in selected]
        try:
            Chem.Kekulize(output, clearAromaticFlags=True)
        except Chem.KekulizeException:
            pass
        output = Chem.RenumberAtoms(output, selected + remaining)
        editable = Chem.RWMol(output)
        for index in range(editable.GetNumAtoms() - 1, len(selected) - 1, -1):
            editable.RemoveAtom(index)
        output = editable.GetMol()
        Chem.SanitizeMol(output)
        Chem.AssignStereochemistry(output, cleanIt=True, force=True)

    if not is_all(structure_indices):
        conformers = list(output.GetConformers())
        selected_conformers = [Chem.Conformer(conformers[index]) for index in structure_indices]
        output.RemoveAllConformers()
        for conformer in selected_conformers:
            output.AddConformer(conformer, assignId=False)

    return output
