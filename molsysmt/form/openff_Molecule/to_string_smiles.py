from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Molecule')
def to_string_smiles(item, skip_digestion=False):

    return 'smiles:' + item.to_smiles()
