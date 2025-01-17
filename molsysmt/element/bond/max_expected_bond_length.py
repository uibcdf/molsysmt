from molsysmt import pyunitwizard as puw

bond_length_tolerance = puw.quantity(0.2, 'angstroms')

max_expected_bond_length = {}

max_expected_bond_length['water'] = {}
aux_dict = max_expected_bond_length['water']
aux_dict['H'] = {}
aux_dict['O'] = {}
aux_dict['O']['H'] = puw.quantity(0.96, 'angstroms')
for ii, kk in aux_dict.items():
    for jj in kk:
        if ii not in aux_dict[jj]:
            aux_dict[jj][ii] = aux_dict[ii][jj]


max_expected_bond_length['small molecule'] = {}
aux_dict = max_expected_bond_length['small molecule']
aux_dict['C'] = {}
aux_dict['N'] = {}
aux_dict['O'] = {}
aux_dict['H'] = {}
aux_dict['C']['H'] = puw.quantity(1.09, 'angstroms')
aux_dict['C']['C'] = puw.quantity(1.54, 'angstroms') # 1.54 single bond, 1.34 double bond, 1.20 triple bond
aux_dict['C']['N'] = puw.quantity(1.47, 'angstroms')
aux_dict['C']['O'] = puw.quantity(1.43, 'angstroms') # 1.43 single bond, 1.23 double bond
aux_dict['N']['N'] = puw.quantity(1.47, 'angstroms')
aux_dict['N']['O'] = puw.quantity(1.45, 'angstroms') # 1.45 single bond, 1.25 double bond
aux_dict['O']['H'] = puw.quantity(0.96, 'angstroms')
aux_dict['H']['H'] = None
for ii, kk in aux_dict.items():
    for jj in kk:
        if ii not in aux_dict[jj]:
            aux_dict[jj][ii] = aux_dict[ii][jj]

max_expected_bond_length['amino acid'] = {}
aux_dict = max_expected_bond_length['amino acid']
aux_dict['C'] = {}
aux_dict['N'] = {}
aux_dict['O'] = {}
aux_dict['H'] = {}
aux_dict['S'] = {}
aux_dict['C']['H'] = puw.quantity(1.09, 'angstroms')
aux_dict['C']['C'] = puw.quantity(1.54, 'angstroms') # 1.54 single bond, 1.34 double bond, 1.20 triple bond
aux_dict['C']['N'] = puw.quantity(1.33, 'angstroms')
aux_dict['C']['O'] = puw.quantity(1.23, 'angstroms') # 1.23 single bond
aux_dict['C']['S'] = puw.quantity(1.82, 'angstroms')
aux_dict['N']['H'] = puw.quantity(1.01, 'angstroms')
aux_dict['O']['H'] = puw.quantity(0.96, 'angstroms')
aux_dict['H']['H'] = None
for ii, kk in aux_dict.items():
    for jj in kk:
        if ii not in aux_dict[jj]:
            aux_dict[jj][ii] = aux_dict[ii][jj]

max_expected_bond_length['terminal capping'] = max_expected_bond_length['amino acid'].copy()

max_expected_bond_length['lipid'] = {}
aux_dict = max_expected_bond_length['lipid']
aux_dict['C'] = {}
aux_dict['N'] = {}
aux_dict['O'] = {}
aux_dict['H'] = {}
aux_dict['P'] = {}
aux_dict['C']['H'] = puw.quantity(1.09, 'angstroms')
aux_dict['C']['C'] = puw.quantity(1.54, 'angstroms') # 1.54 single bond, 1.34 double bond, 1.20 triple bond
aux_dict['P']['O'] = puw.quantity(1.61, 'angstroms')
aux_dict['O']['H'] = puw.quantity(0.96, 'angstroms')
aux_dict['C']['O'] = puw.quantity(1.43, 'angstroms') # 1.43 single bond, 1.23 double bond
aux_dict['H']['H'] = None
for ii, kk in aux_dict.items():
    for jj in kk:
        if ii not in aux_dict[jj]:
            aux_dict[jj][ii] = aux_dict[ii][jj]


max_expected_bond_length['protein'] = max_expected_bond_length['amino acid'].copy()
max_expected_bond_length['protein']['S']['S'] = puw.quantity(2.05, 'angstroms')
for ii, kk in aux_dict.items():
    for jj in kk:
        if ii not in aux_dict[jj]:
            aux_dict[jj][ii] = aux_dict[ii][jj]

del aux_dict
