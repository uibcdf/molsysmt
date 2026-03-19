from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='string:uniprot_id')
def copy(item, skip_digestion=False):

    return item
