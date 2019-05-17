
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

    'AMBER99SB-ILDN' : 'amber99sbildn.xml'
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

