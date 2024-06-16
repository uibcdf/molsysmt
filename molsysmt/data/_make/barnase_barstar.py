import molsysmt as msm
import os
import shutil
from pathlib import Path
import numpy as np

data_dir = Path('../.')

# purge
print('Removing old files...')

files_to_be_purged = [
    'pdb/barnase_barstar.pdb',
    'h5msm/barnase_barstar.msmpk',
    'mmtf/1brs.mmtf']

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)

# make
print('Making new files...')
molecular_system = msm.convert('1BRS')
molecular_system = msm.convert(molecular_system)
molecular_system = msm.extract(molecular_system, selection='molecule_type=="protein"')
barnase = msm.extract(molecular_system, selection="chain_name=='B'")
barstar_E = msm.extract(molecular_system, selection="chain_name=='E'")
barstar_F = msm.extract(molecular_system, selection="chain_name=='F'")
barstar_F_over_E = msm.structure.least_rmsd_align(barstar_F, selection='atom_name=="CA"',
                                                  reference_molecular_system=barstar_E,
                                                  reference_selection='atom_name=="CA"')
barnase_barstar = msm.merge([barnase, barstar_F_over_E])
barnase_barstar = msm.build.add_missing_heavy_atoms(barnase_barstar)
barnase_barstar = msm.build.add_missing_hydrogens(barnase_barstar, pH=7.4)
msm.molecular_mechanics.potential_energy_minimization(barnase_barstar, in_place=True)
msm.build.define_new_chain(barnase_barstar, selection='all', chain_id=0, chain_name='A')
_ = msm.convert(barnase_barstar, to_form='barnase_barstar.pdb')
_ = msm.convert(barnase_barstar, to_form='barnase_barstar.h5msm')
shutil.move('barnase_barstar.pdb', Path(data_dir, 'h5msm/barnase_barstar.pdb'))
shutil.move('barnase_barstar.h5msm', Path(data_dir, 'h5msm/barnase_barstar.h5msm'))

