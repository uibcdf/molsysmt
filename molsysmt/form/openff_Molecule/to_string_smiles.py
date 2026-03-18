from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openff.Molecule')
def to_string_smiles(item, skip_digestion=False):

    return 'smiles:' + item.to_smiles()
