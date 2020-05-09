from .engines import digest as _digest_engines

forcefields = [

    'AMBER96',
    'AMBER99SB-ILDN',
    'TIP3P',
    'TIP4P',
    'TIP4P-EW',
    'TIP5P',
    'SPC',
    'GAFF'

]

_openmm = {

    'AMBER99SB-ILDN' : 'amber99sbildn.xml',
    'TIP3P' : 'tip3p.xml'
}

_leap = {

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
        return switcher[engine][forcefields]

