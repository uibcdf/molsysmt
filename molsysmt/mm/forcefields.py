from molsysmt._private.exceptions import *

forcefields = {

    'AMBER14': "",
    'AMBER10': "",
    'AMBER03': "",
    'AMBER99': "",
    'AMBER99SB': "",
    'AMBER99SBILDN': "",
    'AMBER99SBNMR': "",
    'AMBER96': "",
    'CHARMM36': "",
    'GAFF': ""

}

water_models = {

    'SPC': "",
    'SPC/E': "",
    'TIP3P': "",
    'TIP3P-FB': "",
    'TIP3P-PME-B': "TIP3P from Charmm36",
    'TIP3P-PME-F': "TIP3P from Charmm36",
    'TIP4P': "",
    'TIP4P-EW': "",
    'TIP4P-FB': "",
    'TIP4P-2005': "",
    'TIP5P': "",
    'TIP5P-EW': ""

}

implicit_solvent_models = {

    'OBC1': "",

}

switcher={}

switcher['OpenMM'] = {

    'AMBER14':{
        'vacuum':["amber14-all.xml"],
        'SPC/E':["amber14-all.xml", "amber14/spce.xml"],
        'TIP3P':["amber14-all.xml", "amber14/tip3p.xml"],
        'TIP3P-FB':["amber14-all.xml", "amber14/tip3pfb.xml"],
        'TIP4P-EW':["amber14-all.xml", "amber14/tip4pew.xml"],
        'TIP4P-FB':["amber14-all.xml", "amber14/tip4pfb.xml"],
        'OBC1':["amber14-all.xml"],
    },

    'AMBER10':{
        'vacuum':["amber10.xml"],
        'SPC/E':["amber10.xml", "spce.xml"],
        'TIP3P':["amber10.xml", "tip3p.xml"],
        'TIP3P-FB':["amber10.xml", "tip3pfb.xml"],
        'TIP4P-EW':["amber10.xml", "tip4pew.xml"],
        'TIP4P-FB':["amber10.xml", "tip4pfb.xml"],
        'OBC1':["amber10.xml", "amber10_obc.xml"],
    },

    'AMBER03':{
        'vacuum':["amber03.xml"],
        'SPC/E':["amber03.xml", "spce.xml"],
        'TIP3P':["amber03.xml", "tip3p.xml"],
        'TIP3P-FB':["amber03.xml", "tip3pfb.xml"],
        'TIP4P-EW':["amber03.xml", "tip4pew.xml"],
        'TIP4P-FB':["amber03.xml", "tip4pfb.xml"],
        'OBC1':["amber03.xml", "amber03_obc.xml"],
    },

    'AMBER99SB':{
        'vacuum':["amber99sb.xml"],
        'SPC/E':["amber99sb.xml", "spce.xml"],
        'TIP3P':["amber99sb.xml", "tip3p.xml"],
        'TIP3P-FB':["amber99sb.xml", "tip3pfb.xml"],
        'TIP4P-EW':["amber99sb.xml", "tip4pew.xml"],
        'TIP4P-FB':["amber99sb.xml", "tip4pfb.xml"],
        'OBC1':["amber99sb.xml", "amber99_obc.xml"],
    },

    'AMBER99SBILDN':{
        'vacuum':["amber99sbildn.xml"],
        'SPC/E':["amber99sbildn.xml", "spce.xml"],
        'TIP3P':["amber99sbildn.xml", "tip3p.xml"],
        'TIP3P-FB':["amber99sbildn.xml", "tip3pfb.xml"],
        'TIP4P-EW':["amber99sbildn.xml", "tip4pew.xml"],
        'TIP4P-FB':["amber99sbildn.xml", "tip4pfb.xml"],
        'OBC1':["amber99sbildn.xml", "amber99_obc.xml"],
    },

    'AMBER99SBNMR':{
        'vacuum':["amber99sbnmr.xml"],
        'SPC/E':["amber99sbnmr.xml", "spce.xml"],
        'TIP3P':["amber99sbnmr.xml", "tip3p.xml"],
        'TIP3P-FB':["amber99sbnmr.xml", "tip3pfb.xml"],
        'TIP4P-EW':["amber99sbnmr.xml", "tip4pew.xml"],
        'TIP4P-FB':["amber99sbnmr.xml", "tip4pfb.xml"],
        'OBC1':["amber99sbnmr.xml", "amber99_obc.xml"],
    },

    'AMBER96':{
        'vacuum':["amber96.xml"],
        'SPC/E':["amber96.xml", "spce.xml"],
        'TIP3P':["amber96.xml", "tip3p.xml"],
        'TIP3P-FB':["amber96.xml", "tip3pfb.xml"],
        'TIP4P-EW':["amber96.xml", "tip4pew.xml"],
        'TIP4P-FB':["amber96.xml", "tip4pfb.xml"],
        'OBC1':["amber96.xml", "amber96_obc.xml"],
    },

    'CHARMM36':{
        'vacuum':["charmm36.xml"],
        'SPC/E':["charmm36.xml", "charmm36/spce.xml"],
        'TIP3P':["charmm36.xml", "charmm36/water.xml"],
        'TIP3P-PME-B':["charmm36.xml", "charmm36/tip3p-pme-b.xml"],
        'TIP3P-PME-F':["charmm36.xml", "charmm36/tip3p-pme-f.xml"],
        'TIP4P-EW':["charmm36.xml", "charmm36/tip4pew.xml"],
        'TIP4P-2005':["charmm36.xml", "charmm36/tip4p2005.xml"],
        'TIP5P':["charmm36.xml", "charmm36/tip5p.xml"],
        'TIP5P-EW':["charmm36.xml", "charmm36/tip5pew.xml"],
    },

}

switcher['LEaP'] = {

    'AMBER14':{
        'vacuum':["leaprc.protein.ff14SB"],
        'SPC':["leaprc.protein.ff14SB", "leaprc.water.spc"],
        'TIP3P':["leaprc.protein.ff14SB", "leaprc.water.tip3p"],
        'OBC1':["leaprc.protein.ff14SB"],
    },

    'AMBER99SBILDN':{
        'vacuum':["oldff/leaprc.ff99SBildn"],
        'SPC':["oldff/leaprc.ff99SBildn", "leaprc.water.spc"],
        'TIP3P':["oldff/leaprc.ff99SBildn", "leaprc.water.tip3p"],
        'OBC1':["oldff/leaprc.ff99SBildn"],
    },

    'AMBER96':{
        'vacuum':["oldff/leaprc.ff96"],
        'SPC':["oldff/leaprc.ff96", "leaprc.water.spc"],
        'TIP3P':["oldff/leaprc.ff96", "leaprc.water.tip3p"],
        'OBC1':["oldff/leaprc.ff96"],
    },

    'GAFF':{
        'vacuum':["leaprc.gaff"],
    },

}

def get_forcefield(molecular_system, engine=None):

    from molsysmt.basic import get

    forcefield, implicit_solvent, water_model = get(molecular_system, forcefield=True, implicit_solvent=True, water_model=True)
    if engine is None:
        return forcefield
    elif forcefield is None:
        return None
    else:
        return _translate_forcefield_to_engine(forcefield, engine, implicit_solvent=implicit_solvent, water_model=water_model)

def _translate_forcefield_to_engine(forcefield, engine, implicit_solvent=None, water_model=None):

    forcefields_out=[]

    if type(forcefield) not in [list, tuple]:
        forcefield=[forcefield]

    for ff in forcefield:
        try:
            if implicit_solvent is not None:
                if implicit_solvent in implicit_solvent_models:
                    aux = switcher[engine][ff][implicit_solvent]
                    forcefields_out.extend(aux)
                else:
                    raise ValueError('The implicit solvent {} is unknown for MolSysMT. Either it is mispelled or either it needs to be implemented in MolSysMT'.format(implicit_solvent))
            elif water_model is not None:
                if water_model in water_models:
                    aux = switcher[engine][ff][water_model]
                    forcefields_out.extend(aux)
                else:
                    raise ValueError('The water model {} is unknown for MolSysMT. Either it is mispelled or it needs to be implemented in MolSysMT'.format(water_model))
            else:
                aux = switcher[engine][ff]['vacuum']
                forcefields_out.extend(aux)
        except:
            raise NotImplementedError('{} with implicit solvent {} or water model {} and {} needs to be implemented in MolSysMT'.format(ff, implicit_solvent, water_model, engine))

    forcefields_out = list(set(forcefields_out))

    return forcefields_out

