from molsysmt._private.arg_digestion import arg_digest

@arg_digest()
def close_file(item):

    item.close()
    pass
