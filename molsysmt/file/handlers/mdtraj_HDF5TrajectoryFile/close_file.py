from molsysmt._private.digestion import digest

@digest()
def close_file(item):

    item.close()
    pass
