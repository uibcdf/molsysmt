from . import file

def pentalanine(to_form='molsysmt.MolSys'):

    from molsysmt.multitool import convert
    tmp_item = convert([file['pentalanine.prmtop'], file['pentalanine.inpcrd']], to_form=to_form)
    return tmp_item

def pentalanine_traj(to_form='molsysmt.MolSys'):

    from molsysmt import convert
    tmp_item = convert(file['pentalanine.h5'], to_form=to_form)
    return tmp_item

def metenkephalin(to_form='molsysmt.MolSys'):

    from molsysmt import convert
    tmp_item = convert(file['metenkephalin.pdb'], to_form=to_form)
    return tmp_item

