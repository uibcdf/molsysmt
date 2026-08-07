from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:uniprot_id')
def copy(item, skip_digestion=False):

    return item
