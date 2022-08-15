"""
Unit and regression test for the select module of the molsysmt package acting on molsysmt.MolSys
molecular systems.
"""

import molsysmt as msm
import numpy as np

def test_select_1():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, selection=[0,1,2])
    true_output = np.array([0, 1, 2])
    assert np.all(output==true_output)

def test_select_2():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, element='group', selection=[0,1,2,3,4,5,6,7,8,9,10,11])
    true_output = np.array([0, 1])
    assert np.all(output==true_output)

def test_select_3():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, element='molecule', selection=[3900, 3910, 3920])
    true_output = np.array([ 84,  94, 104])
    assert np.all(output==true_output)

def test_select_4():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'atom_name == "C" and group_index == [0,1,2,3]')
    true_output = np.array([ 2, 11, 18, 27])
    assert np.all(output==true_output)

def test_select_5():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'atom_name in ["CA","CB"] and group_index == [0,1,2,3]')
    true_output = np.array([ 1,  4, 10, 13, 17, 20, 26, 29])
    assert np.all(output==true_output)

def test_select_6():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'atom_type==["C","N"] and group_index == [2]')
    true_output = np.array([16, 17, 18, 20, 21, 22, 24])
    assert np.all(output==true_output)

def test_select_7():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'not atom_type=="H" and group_index==3')
    true_output = np.array([25, 26, 27, 28, 29, 30, 31])
    assert np.all(output==true_output)

def test_select_8():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'atom_type=="C" and not atom_name=="CA" and group_index==[2,3]')
    true_output = np.array([18, 20, 21, 22, 27, 29, 30, 31])
    assert np.all(output==true_output)

def test_select_9():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'atom_name!=["CA","CB","C"] and group_index==[2,3]')
    true_output = np.array([16, 19, 21, 22, 23, 24, 25, 28, 30, 31])
    assert np.all(output==true_output)

def test_select_10():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'atom_id<10')
    true_output = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
    assert np.all(output==true_output)

def test_select_11():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'atom_id<10 and atom_id>=3')
    true_output = np.array([2, 3, 4, 5, 6, 7, 8])
    assert np.all(output==true_output)

def test_select_12():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'molecule_type=="water" and molecule_index==[100,101]')
    true_output = np.array([3916, 3917])
    assert np.all(output==true_output)

def test_select_13():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'molecule_type=="protein" and atom_type!="H" and group_index==3')
    true_output = np.array([25, 26, 27, 28, 29, 30, 31])
    assert np.all(output==true_output)

def test_select_14():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys,  'group_name==["GLY","ALA","VAL"] and chain_id=="A" and group_index==[2,3,4,5,6]')
    true_output = np.array([40, 41, 42, 43, 44, 45, 46, 47, 48, 49])
    assert np.all(output==true_output)

def test_select_15():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    indices=[10,11,12]
    output = msm.select(molsys,  'group_index==@indices and atom_name=="N"')
    true_output = np.array([77, 86, 92])
    assert np.all(output==true_output)

def test_select_16():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    indices=list(range(10,20))
    atoms=["CA", "C", "O", "N"]
    output = msm.select(molsys, 'atom_name==@atoms & atom_index==@indices')
    true_output = np.array([10, 11, 12, 16, 17, 18, 19])
    assert np.all(output==true_output)

def test_select_17():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    indices=list(range(10,30))
    output = msm.select(molsys, 'atom_name=="C"', mask=indices)
    true_output = np.array([11, 18, 27])
    assert np.all(output==true_output)

def test_select_18():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    indices=list(range(10,30))
    output = msm.select(molsys, 'atom_name=="C" and atom_index in @indices')
    true_output = np.array([11, 18, 27])
    assert np.all(output==true_output)

def test_select_19():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    indices=[0,100,200]
    output = msm.select(molsys, 'group_index==@indices', element='group')
    true_output = np.array([  0, 100, 200])
    assert np.all(output==true_output)

def test_select_20():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'group_name=="ALA" and group_index==[2,3,4,5,6,7]', element='group')
    true_output = np.array([5, 6, 7])
    assert np.all(output==true_output)

def test_select_21():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'atom_index==[34,44,64]', element='group')
    true_output = np.array([4, 5, 9])
    assert np.all(output==true_output)

def test_select_22():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'chain_id==["A","C"] and molecule_type!="water"', element='group')
    true_output = np.array(list(range(248)))
    assert np.all(output==true_output)

def test_select_23():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'molecule_type=="water"', element='group')
    true_output = np.array(list(range(497,662)))
    assert np.all(output==true_output)

def test_select_24():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'molecule_type=="water"', element='molecule')
    true_output = np.array(list(range(2,167)))
    assert np.all(output==true_output)

def test_select_25():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'molecule_type=="water"', element='chain')
    true_output = np.array([2, 3])
    assert np.all(output==true_output)

def test_select_26():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'group_index==5', element='bond')
    true_output = np.array([37, 38, 39, 40])
    assert np.all(output==true_output)

def test_select_27():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'atom_index in [0,1,2,3,4]', mask=[0,1,2], element='atom')
    true_output = np.array([0, 1, 2])
    assert np.all(output==true_output)

def test_select_28():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'group_index in [0,1,2,3,4]', mask=[0,1,2], element='group')
    true_output = np.array([0, 1, 2])
    assert np.all(output==true_output)

def test_select_29():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'chain_id=="A" within 0.30 nm of chain_id=="B"')
    true_output = np.array([ 89, 480, 527, 547, 550, 552, 554, 566, 723, 734])
    assert np.all(output==true_output)

def test_select_30():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'chain_id=="A" not within 7.8 nanometers of chain_id=="B"')
    true_output = np.array([1521, 1522, 1723, 1724])
    assert np.all(output==true_output)

def test_select_31():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'chain_id=="A" within 0.3 nm without pbc of chain_id=="B"')
    true_output = np.array([ 89, 480, 527, 547, 550, 552, 554, 566, 723, 734])
    assert np.all(output==true_output)

def test_select_32():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, 'chain_id=="A" within 0.3 nm with pbc of chain_id=="B"')
    true_output = np.array([ 89, 480, 527, 547, 550, 552, 554, 566, 723, 734])
    assert np.all(output==true_output)

def test_select_33():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, '(atom_name=="N" and chain_id=="A") within 3 angstroms of (atom_type=="O" and molecule_type=="water")')
    true_output = np.array([ 119,  213,  473,  531,  654,  696,  799, 1049])
    assert np.all(output==true_output)

def test_select_34():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, '(atom_name=="CA" and chain_id=="A") within 0.5 nm of (atom_name=="CA" and chain_id=="B")', element='group')
    true_output = np.array([10, 42, 62, 72, 73])
    assert np.all(output==true_output)

def test_select_35():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, '(atom_name=="N" bonded to atom_type=="C") and group_index==[10, 11, 12]')
    true_output = np.array([77, 86, 92])
    assert np.all(output==true_output)

def test_select_36():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, '(all not bonded to atom_type==["H","N","C","O"]) and molecule_type=="protein"')
    true_output = np.array([ 363, 1714, 2275, 3626])
    assert np.all(output==true_output)

def test_select_37():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, '((atom_type=="O" and chain_id=="A") bonded to (atom_type=="C" and chain_id=="A")) and group_index==[3,4]')
    true_output = np.array([ 28, 35])
    assert np.all(output==true_output)

def test_select_38():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, '((atom_name=="N" and chain_id=="A") bonded to atom_type=="C") within 3 angstroms of (atom_type=="O" and molecule_type=="water")')
    true_output = np.array([ 119,  213,  473,  531,  654,  696,  799, 1049])
    assert np.all(output==true_output)

def test_select_39():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, selection='group_index==[3,4,5]', to_syntax='NGLView')
    true_output = '@25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44'
    assert np.all(output==true_output)

def test_select_40():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, selection='group_index==[3,4,5]', to_syntax='MDTraj')
    true_output = 'index 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44'
    assert np.all(output==true_output)

def test_select_41():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, element='group', selection='group_index==[3,4,5]', to_syntax='NGLView')
    true_output = '7:A 8:A 9:A'
    assert np.all(output==true_output)

def test_select_42():
    molsys = msm.convert(msm.demo['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    output = msm.select(molsys, element='group', selection='group_index==[3,4,5]', to_syntax='MDTraj')
    true_output = 'resid 3 4 5'
    assert np.all(output==true_output)


