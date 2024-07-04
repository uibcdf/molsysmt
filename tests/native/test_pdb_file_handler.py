"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.native import PDBFileHandler

import sys

if sys.version_info[1] in (10,11):
    from importlib.resources import files
    def path(package, file):
        return files(package).joinpath(file)
elif sys.version_info[1] in (8,9):
    from pathlib import PurePath
    parent = PurePath(__file__).parent
    def path(package, file):
        data_dir = package.split('.')[-1]
        return parent.joinpath('data/'+data_dir+'/'+file).__str__()

systems = {}

systems['3c0f.pdb'] = str(path('molsysmt.data.pdb', '3c0f.pdb'))
systems['1bnf.pdb'] = str(path('molsysmt.data.pdb', '1bnf.pdb'))
systems['3c8h.pdb'] = str(path('molsysmt.data.pdb', '3c8h.pdb'))
systems['2vgy.pdb'] = str(path('molsysmt.data.pdb', '2vgy.pdb'))
systems['5ip4.pdb'] = str(path('molsysmt.data.pdb', '5ip4.pdb'))

def test_pdb_file_handler_1():

    pdb_file_handler = PDBFileHandler(systems['3c0f.pdb'])
    pdb_file_handler.load()
    assert pdb_file_handler.entry.title.source[0].organism_scientific == 'ARCHAEOGLOBUS FULGIDUS DSM 4304'

def test_pdb_file_handler_2():

    pdb_file_handler = PDBFileHandler(systems['1bnf.pdb'])
    pdb_file_handler.load()
    assert pdb_file_handler.entry.connectivity.conect[4].atomSerNum == 1339

def test_pdb_file_handler_3():

    pdb_file_handler = PDBFileHandler(systems['3c8h.pdb'])
    pdb_file_handler.load()
    assert pdb_file_handler.entry.coordinate.model[0].record[0].anisou11 == 9993

def test_pdb_file_handler_4():

    pdb_file_handler = PDBFileHandler(systems['2vgy.pdb'])
    pdb_file_handler.load()
    assert pdb_file_handler.entry.coordinate.model[0].record[0].anisou11 == 10496

def test_pdb_file_handler_5():

    pdb_file_handler = PDBFileHandler(systems['5ip4.pdb'])
    pdb_file_handler.load()
    assert pdb_file_handler.entry.crystallographic_and_coordinate_transformation.scale.u2 == 0.0
