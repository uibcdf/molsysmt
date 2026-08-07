from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:uniprot_id')
def to_string_uniprot_id(item, atom_indices='all', skip_digestion=False):

    return item
