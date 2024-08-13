"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.native import H5MSMFileHandler
from molsysmt._private.files_and_directories import temp_filename

def test_pdb_file_handler_1():

    molsys = msm.systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5msm']
    handler = H5MSMFileHandler(molsys)
    assert 4648==handler.file['topology']['atoms']['name'].shape[0]

def test_pdb_file_handler_2():

    topology = msm.convert(msm.systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5msm'],
                           'molsysmt.Topology')
    tmpfile = str(temp_filename(extension='h5msm'))
    molsys = H5MSMFileHandler(tmpfile, 'w')
    molsys.write_topology(topology)
    molsys.close()

    handler = H5MSMFileHandler(tmpfile)
    assert 4648==handler.file['topology']['atoms']['name'].shape[0]

