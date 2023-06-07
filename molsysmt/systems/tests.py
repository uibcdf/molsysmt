from importlib import resources
from pathlib import Path

data_dir = resources.files('molsysmt.data')

tests = {}

### 1SUX

tests['1SUX'] = {}
tests['1SUX']['1sux.pdb'] = Path(data_dir,'pdb/1sux.pdb')
tests['1SUX']['1sux.mmtf'] = Path(data_dir,'mmtf/1sux.mmtf')


### 5ZMZ

tests['5ZMZ'] = {}
tests['5ZMZ']['5zmz.pdb'] = Path(data_dir, 'pdb/5zmz.pdb')
tests['5ZMZ']['5zmz.mmtf'] = Path(data_dir, 'mmtf/5zmz.mmtf')


### Alanine dipeptide

tests['alanine dipeptide'] = {}
tests['alanine dipeptide']['alanine_dipeptide.msmpk'] = Path(data_dir, 'msmpk/alanine_dipeptide.msmpk')


### Proline dipeptide

tests['proline dipeptide'] = {}
tests['proline dipeptide']['proline_dipeptide.msmpk'] = Path(data_dir, 'msmpk/proline_dipeptide.msmpk')


### Valine dipeptide

tests['valine dipeptide'] = {}
tests['valine dipeptide']['valine_dipeptide.msmpk'] = Path(data_dir, 'msmpk/valine_dipeptide.msmpk')


### Lysine dipeptide

tests['lysine dipeptide'] = {}
tests['lysine dipeptide']['lysine_dipeptide.msmpk'] = Path(data_dir, 'msmpk/lysine_dipeptide.msmpk')


### Villin HP35

tests['chicken villin HP35'] = {}
tests['chicken villin HP35']['1vii.pdb'] = Path(data_dir, 'pdb/1vii.pdb')
tests['chicken villin HP35']['1vii.mmtf'] = Path(data_dir, 'mmtf/1vii.mmtf')
tests['chicken villin HP35']['chicken_villin_HP35.msmpk'] = Path(data_dir, 'msmpk/chicken_villin_HP35.msmpk')
tests['chicken villin HP35']['chicken_villin_HP35_solvated.msmpk'] = Path(data_dir, 'msmpk/chicken_villin_HP35_solvated.msmpk')
##tests['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd'] = Path(data_dir, 'dcd/traj_chicken_villin_HP35_solvated.dcd')
##tests['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5'] = Path(data_dir, 'h5/traj_chicken_villin_HP35_solvated.h5')


### T4 Lysozyme L99A

tests['T4 lysozyme L99A'] = {}
tests['T4 lysozyme L99A']['181l.pdb'] = Path(data_dir, 'pdb/181l.pdb')
tests['T4 lysozyme L99A']['181l.mmtf'] = Path(data_dir, 'mmtf/181l.mmtf')
tests['T4 lysozyme L99A']['181l.msmpk'] = Path(data_dir, 'msmpk/181l.msmpk')
##tests['T4 lysozyme L99A']['1l17.pdb'] = Path(data_dir, 'pdb/1l17.pdb')
##tests['T4 lysozyme L99A']['1l17.mmtf'] = Path(data_dir, 'mmtf/1l17.mmtf')
tests['T4 lysozyme L99A']['1l17.msmpk'] = Path(data_dir, 'msmpk/1l17.msmpk')
tests['T4 lysozyme L99A']['t4_lysozyme_L99A.msmpk'] = Path(data_dir, 'msmpk/t4_lysozyme_L99A.msmpk')


### Pentalanine

tests['pentalanine'] = {}
tests['pentalanine']['pentalanine.inpcrd'] = Path(data_dir, 'inpcrd/pentalanine.inpcrd')
tests['pentalanine']['pentalanine.prmtop'] = Path(data_dir, 'prmtop/pentalanine.prmtop')
tests['pentalanine']['traj_pentalanine.h5'] = Path(data_dir, 'h5/traj_pentalanine.h5')


### Particles_4

tests['particles 4'] = {}
tests['particles 4']['traj_particles_4.xyznpy'] = Path(data_dir, 'xyznpy/traj_particles_4.xyznpy')


### Benzamidine

tests['benzamidine'] = {}
tests['benzamidine']['benzamidine.pdb'] = Path(data_dir, 'pdb/benzamidine.pdb')


### NGLView

tests['nglview'] = {}
##tests['nglview']['ala3.pdb'] = Path(data_dir, 'pdb/ala3.pdb')
tests['nglview']['md_1u19.gro'] = Path(data_dir, 'gro/md_1u19.gro')
##tests['nglview']['md_1u19.pdb'] = Path(data_dir, 'pdb/md_1u19.pdb')
##tests['nglview']['md_1u19.traj'] = Path(data_dir, 'traj/md_1u19.traj')
##tests['nglview']['md_1u19.trr'] = Path(data_dir, 'trr/md_1u19.trr')
tests['nglview']['md_1u19.xtc'] = Path(data_dir, 'xtc/md_1u19.xtc')


### TcTIM (to be removed)

tests['TcTIM'] = {}
#tests['TcTIM']['1tcd.pdb'] = Path(data_dir, 'pdb/1tcd.pdb')
#tests['TcTIM']['1tcd.mmtf'] = Path(data_dir, 'mmtf/1tcd.mmtf')
tests['TcTIM']['1tcd.msmpk'] = Path(data_dir, 'msmpk/1tcd.msmpk')


### Trp-Cage

tests['Trp-Cage'] = {}
tests['Trp-Cage']['1l2y.pdb'] = Path(data_dir, 'pdb/1l2y.pdb')
##tests['Trp-Cage']['1l2y.mmtf'] = Path(data_dir, 'mmtf/1l2y.mmtf')


### Metenkephalin

tests['Met-enkephalin'] = {}
tests['Met-enkephalin']['met_enkephalin.pdb'] = Path(data_dir, 'pdb/met_enkephalin.pdb')
tests['Met-enkephalin']['met_enkephalin.msmpk'] = Path(data_dir, 'msmpk/met_enkephalin.msmpk')


### Two LJ particles

tests['two LJ particles'] = {}
tests['two LJ particles']['traj_two_lj_particles.trjpk'] = Path(data_dir, 'trjpk/traj_two_lj_particles.trjpk')


### Barnase - Barstar
##
tests['Barnase-Barstar'] = {}
tests['Barnase-Barstar']['barnase_barstar.msmpk'] = Path(data_dir, 'msmpk/barnase_barstar.msmpk')
tests['Barnase-Barstar']['1brs.mmtf'] = Path(data_dir, 'mmtf/1brs.mmtf')


### POPC membrane

tests['POPC membrane'] = {}
tests['POPC membrane']['popc_membrane.psf'] = Path(data_dir, 'psf/popc_membrane.psf')
tests['POPC membrane']['popc_membrane.dcd'] = Path(data_dir, 'dcd/popc_membrane.dcd')
tests['POPC membrane']['popc_membrane.msmpk'] = Path(data_dir, 'msmpk/popc_membrane.msmpk')


### caffeine

tests['caffeine'] = {}
tests['caffeine']['caffeine.mol2'] = Path(data_dir, 'mol2/caffeine.mol2')


del(resources, Path, data_dir)

