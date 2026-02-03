from molsysmt._private.digestion import arg_digest

@arg_digest()
def close_file(item):

    item.close()
    pass
