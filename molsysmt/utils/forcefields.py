from .engines import digest as _digest_engines

_forcefields = {

    'AMBER96': "",
    'AMBER99': "",
    'AMBER99SB': "",
    'AMBER99SBILDN': "",
    'AMBER99SBNMR': "",
    'AMBER14': "",
    'CHARMM36': "",
    'GAFF': ""

}

_water_models = {

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
        'OBC1':["amber10.xml", "amber10_obc.xml"],
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


def digest(forcefields, engine, implicit_solvent=None, water_model=None):

    forcefields_out=[]

    if type(forcefields) not in [list, tuple]:
        forcefields=[forcefields]

    engine = _digest_engines(engine)

    for ff in forcefields:
        try:
            if implicit_solvent is not None:
                aux = switcher[engine][ff][implicit_solvent]
            elif water_model is not None:
                aux = switcher[engine][ff][water_model]
            else:
                aux = switcher[engine][ff]['vacuum']
            forcefields_out.extend(aux)
        except:
            raise NotImplementedError('{} with implicit solvent {} or water model {} and {} needs to be implemented in MolSysMT'.format(ff, implicit_solvent, water_model, engine))

    forcefields_out = list(set(forcefields_out))

    return forcefields_out

