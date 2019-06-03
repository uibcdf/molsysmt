
forcefields = [

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

    'AMBER99SB-ILDN' : 'oldff/leaprc.ff99SBildn',
    'TIP3P' : 'leaprc.water.tip3p',
    'SPC' : 'leaprc.water.spc',
    'GAFF' : 'leaprc.gaff'

}

switcher = {

    'OpenMM' : _openmm,
    'LEaP' : _leap

}

def digest_forcefields(forcefields, engine):

    from .engines import digest_engines

    engine = digest_engines(engine)

    if hasattr(forcefields, '__iter__'):
        forcefields_out=[]
        for ii in forcefields:
            forcefields_out.append(switcher[engine][ii])
        return forcfields_out
    else:
        return switcher[engine][forcefields]
