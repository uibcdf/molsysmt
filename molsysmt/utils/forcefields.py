from .engines import digest as _digest_engines

forcefields = [

    'AMBER96',
    'AMBER99SB-ILDN',
    'AMBER14',
    'CHARMM36',
    'TIP3P',
    'TIP3P_AMBER14',
    'TIP3P_CHARMM36',
    'TIP4P',
    'TIP4P-EW',
    'TIP5P',
    'SPC',
    'GAFF'

]

_openmm = {

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

def digest(forcefields, engine):

    engine = _digest_engines(engine)

    if type(forcefields) in [list, tuple]:
        forcefields_out=[]
        for ii in forcefields:
            forcefields_out.append(switcher[engine][ii])
        return forcefields_out
    else:
        return [switcher[engine][forcefields]]  # The output must be a list

