from .engines import digest as _digest_engines

forcefields = [

    'Amber96',
    'Amber99',
    'Amber99SB',
    'Amber99SBILDN',
    'Amber99SBNMR',
    'AMBER99',
    'AMBER14',
    'CHARMM36',
    'GAFF'
]


water_models = [

    'SPC',
    'SPC/E'
    'TIP3P',
    'TIP3P-FB',
    'TIP3P-PME-B',  # Charmm36
    'TIP3P-PME-F',  # Charmm36
    'TIP4P',
    'TIP4P-EW',
    'TIP4P-FB',
    'TIP4P/2005',
    'TIP5P',
    'TIP5P-EW',

]

_openmm = {

    'AMBER96' : 'amber96.xml',
    'AMBER99SB-ILDN' : 'amber99sbildn.xml',
    'AMBER14' : 'amber14-all.xml',
    'CHARMM36' : 'charmm36.xml',
    'TIP3P' : 'tip3p.xml',
    'TIP3P_AMBER14' : 'amber14/tip3p.xml',
    'TIP3P_CHARMM36' : 'charmm36/water.xml'
}

_leap = {

    'AMBER14' : 'leaprc.protein.ff14SB',
    'AMBER96' : 'oldff/leaprc.ff96',
    'AMBER99SB-ILDN' : 'oldff/leaprc.ff99SBildn',
    'TIP3P' : 'leaprc.water.tip3p',
    'SPC' : 'leaprc.water.spc',
    'GAFF' : 'leaprc.gaff'

}

switcher = {

    'OpenMM' : _openmm,
    'LEaP' : _leap

}

def digest(forcefields, engine, implicit_solvent=None, water_model=None):

    engine = _digest_engines(engine)

    if engine == 'OpenMM':

    if type(forcefields) in [list, tuple]:
        forcefields_out=[]
        for ii in forcefields:
            forcefields_out.append(switcher[engine][ii])
        return forcefields_out
    else:
        return [switcher[engine][forcefields]]  # The output must be a list

