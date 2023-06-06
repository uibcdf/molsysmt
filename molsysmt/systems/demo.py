from importlib import resources
from pathlib import Path

data_dir = resources.files('molsysmt.data')

demo = {}

# 1SUX
demo['1SUX'] = {}
demo['1SUX']['1sux.pdb'] = Path(data_dir,'pdb/1sux.pdb')
demo['1SUX']['1sux.mmtf'] = Path(data_dir,'mmtf/1sux.mmtf')


# 5ZMZ
demo['5ZMZ'] = {}
demo['5ZMZ']['5zmz.pdb'] = Path(data_dir, 'pdb/5zmz.pdb')
demo['5ZMZ']['5zmz.mmtf'] = Path(data_dir, 'mmtf/5zmz.mmtf')


# Alanine dipeptide

demo['alanine dipeptide'] = {}
demo['alanine dipeptide']['alanine_dipeptide.msmpk'] = Path(data_dir, 'msmpk/alanine_dipeptide.msmpk')


# Proline dipeptide

demo['proline dipeptide'] = {}
demo['proline dipeptide']['proline_dipeptide.msmpk'] = Path(data_dir, 'msmpk/proline_dipeptide.msmpk')


# Valine dipeptide

demo['valine dipeptide'] = {}
demo['valine dipeptide']['valine_dipeptide.msmpk'] = Path(data_dir, 'msmpk/valine_dipeptide.msmpk')


# Lysine dipeptide

demo['lysine dipeptide'] = {}
demo['lysine dipeptide']['lysine_dipeptide.msmpk'] = Path(data_dir, 'msmpk/lysine_dipeptide.msmpk')


# Villin HP35

demo['chicken villin HP35'] = {}
demo['chicken villin HP35']['1vii.pdb'] = Path(data_dir, 'pdb/1vii.pdb')
demo['chicken villin HP35']['1vii.mmtf'] = Path(data_dir, 'mmtf/1vii.mmtf')
demo['chicken villin HP35']['chicken_villin_HP35.msmpk'] = Path(data_dir, 'msmpk/chicken_villin_HP35.msmpk')
demo['chicken villin HP35']['chicken_villin_HP35_solvated.msmpk'] = Path(data_dir, 'msmpk/chicken_villin_HP35_solvated.msmpk')
demo['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd'] = Path(data_dir, 'dcd/traj_chicken_villin_HP35_solvated.dcd')
demo['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5'] = Path(data_dir, 'h5/traj_chicken_villin_HP35_solvated.h5')


# T4 Lysozyme L99A

demo['T4 lysozyme L99A'] = {}
demo['T4 lysozyme L99A']['181l.pdb'] = Path(data_dir, 'pdb/181l.pdb')
demo['T4 lysozyme L99A']['181l.mmtf'] = Path(data_dir, 'mmtf/181l.mmtf')
demo['T4 lysozyme L99A']['181l.msmpk'] = Path(data_dir, 'msmpk/181l.msmpk')
demo['T4 lysozyme L99A']['1l17.pdb'] = Path(data_dir, 'pdb/1l17.pdb')
demo['T4 lysozyme L99A']['1l17.mmtf'] = Path(data_dir, 'mmtf/1l17.mmtf')
demo['T4 lysozyme L99A']['1l17.msmpk'] = Path(data_dir, 'msmpk/1l17.msmpk')
demo['T4 lysozyme L99A']['t4_lysozyme_L99A.msmpk'] = Path(data_dir, 'msmpk/t4_lysozyme_L99A.msmpk')


# Pentalanine

demo['pentalanine'] = {}
demo['pentalanine']['pentalanine.inpcrd'] = Path(data_dir, 'inpcrd/pentalanine.inpcrd')
demo['pentalanine']['pentalanine.prmtop'] = Path(data_dir, 'prmtop/pentalanine.prmtop')
demo['pentalanine']['traj_pentalanine.h5'] = Path(data_dir, 'h5/traj_pentalanine.h5')


# Particles_4

demo['particles 4'] = {}
demo['particles 4']['traj_particles_4.xyznpy'] = Path(data_dir, 'xyznpy/traj_particles_4.xyznpy')


# Benzamidine

demo['benzamidine'] = {}
demo['benzamidine']['benzamidine.pdb'] = Path(data_dir, 'pdb/benzamidine.pdb')


# NGLView

demo['nglview'] = {}
demo['nglview']['ala3.pdb'] = Path(data_dir, 'pdb/ala3.pdb')
demo['nglview']['md_1u19.gro'] = Path(data_dir, 'gro/md_1u19.gro')
demo['nglview']['md_1u19.pdb'] = Path(data_dir, 'pdb/md_1u19.pdb')
demo['nglview']['md_1u19.traj'] = Path(data_dir, 'traj/md_1u19.traj')
demo['nglview']['md_1u19.trr'] = Path(data_dir, 'trr/md_1u19.trr')
demo['nglview']['md_1u19.xtc'] = Path(data_dir, 'xtc/md_1u19.xtc')


# TcTIM (to be removed)

demo['TcTIM'] = {}
demo['TcTIM']['1tcd.pdb'] = Path(data_dir, 'pdb/1tcd.pdb')
demo['TcTIM']['1tcd.mmtf'] = Path(data_dir, 'mmtf/1tcd.mmtf')
demo['TcTIM']['1tcd.msmpk'] = Path(data_dir, 'msmpk/1tcd.msmpk')


# Trp-Cage

demo['Trp-Cage'] = {}
demo['Trp-Cage']['1l2y.pdb'] = Path(data_dir, 'pdb/1l2y.pdb')
demo['Trp-Cage']['1l2y.mmtf'] = Path(data_dir, 'mmtf/1l2y.mmtf')


# Metenkephalin

demo['Met-enkephalin'] = {}
demo['Met-enkephalin']['met_enkephalin.pdb'] = Path(data_dir, 'pdb/met_enkephalin.pdb')
demo['Met-enkephalin']['met_enkephalin.msmpk'] = Path(data_dir, 'msmpk/met_enkephalin.msmpk')


# Two LJ particles

demo['two LJ particles'] = {}
demo['two LJ particles']['two_lj_particles.trjpk'] = Path(data_dir, 'trjpk/two_lj_particles.trjpk')


# Barnase - Barstar

demo['Barnase-Barstar'] = {}
demo['Barnase-Barstar']['barnase_barstar.msmpk'] = Path(data_dir, 'msmpk/barnase_barstar.msmpk')
demo['Barnase-Barstar']['1brs.mmtf'] = Path(data_dir, 'mmtf/1brs.mmtf')

# POPC membrane

demo['POPC membrane'] = {}
demo['POPC membrane']['popc_membrane.psf'] = Path(data_dir, 'psf/popc_membrane.psf')
demo['POPC membrane']['popc_membrane.dcd'] = Path(data_dir, 'dcd/popc_membrane.dcd')
demo['POPC membrane']['popc_membrane.msmpk'] = Path(data_dir, 'msmpk/popc_membrane.msmpk')



del(resources, Path, data_dir)

