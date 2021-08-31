
def pentalanine(to_form='molsysmt.MolSys'):

    from molsysmt.demo import files
    from molsysmt.multitool import convert
    molsys = convert([files['pentalanine.prmtop'], files['pentalanine.inpcrd']], to_form=to_form)
    return molsys

def pentalanine_traj(to_form='molsysmt.MolSys'):

    from molsysmt.demo import files
    from molsysmt import convert
    molsys = convert(files['pentalanine.h5'], to_form=to_form)
    return molsys

def metenkephalin(to_form='molsysmt.MolSys'):

    from molsysmt.demo import files
    from molsysmt import convert
    molsys = convert(files['metenkephalin.pdb'], to_form=to_form)
    return molsys

def proline_dipeptide_vacuum(to_form='molsysmt.MolSys'):

    from molsysmt.demo import files
    from molsysmt import convert
    molsys = convert(files['proline_dipeptide_vacuum.msmpk'], to_form=to_form)
    return molsys

def valine_dipeptide_vacuum(to_form='molsysmt.MolSys'):

    from molsysmt.demo import files
    from molsysmt import convert
    molsys = convert(files['proline_dipeptide_vacuum.msmpk'], to_form=to_form)
    return molsys

def lysine_dipeptide_vacuum(to_form='molsysmt.MolSys'):

    from molsysmt.demo import files
    from molsysmt import convert
    molsys = convert(files['lysine_dipeptide_vacuum.msmpk'], to_form=to_form)
    return molsys

def T4_lysozyme_L99A_in_pdbid_181l(to_form='molsysmt.MolSys'):

    from molsysmt.demo import files
    from molsysmt import convert
    molsys = convert(files['T4_lysozyme_L99A_in_pdbid_181l.msmpk'], to_form=to_form)
    return molsys

def TcTIM_in_pdbid_1tcd(to_form='molsysmt.MolSys'):

    from molsysmt.demo import files
    from molsysmt import convert
    molsys = convert(files['TcTIM_in_pdbid_1tcd.msmpk'], to_form=to_form)
    return molsys

