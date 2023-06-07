from importlib.resources import path

tests = {}

# 1SUX
tests['1SUX'] = {}
tests['1SUX']['1sux.pdb'] = path('molsysmt.data.pdb','1sux.pdb')
tests['1SUX']['1sux.mmtf'] = path('molsysmt.data.mmtf','1sux.mmtf')


# 5ZMZ
tests['5ZMZ'] = {}
tests['5ZMZ']['5zmz.pdb'] = path('molsysmt.data.pdb', '5zmz.pdb')
tests['5ZMZ']['5zmz.mmtf'] = path('molsysmt.data.mmtf', '5zmz.mmtf')


# Alanine dipeptide

tests['alanine dipeptide'] = {}
tests['alanine dipeptide']['alanine_dipeptide.msmpk'] = path('molsysmt.data.msmpk', 'alanine_dipeptide.msmpk')


# Proline dipeptide

tests['proline dipeptide'] = {}
tests['proline dipeptide']['proline_dipeptide.msmpk'] = path('molsysmt.data.msmpk', 'proline_dipeptide.msmpk')


# Valine dipeptide

tests['valine dipeptide'] = {}
tests['valine dipeptide']['valine_dipeptide.msmpk'] = path('molsysmt.data.msmpk', 'valine_dipeptide.msmpk')


# Lysine dipeptide

tests['lysine dipeptide'] = {}
tests['lysine dipeptide']['lysine_dipeptide.msmpk'] = path('molsysmt.data.msmpk', 'lysine_dipeptide.msmpk')


# Villin HP35

tests['chicken villin HP35'] = {}
tests['chicken villin HP35']['1vii.pdb'] = path('molsysmt.data.pdb', '1vii.pdb')
tests['chicken villin HP35']['1vii.mmtf'] = path('molsysmt.data.mmtf', '1vii.mmtf')
tests['chicken villin HP35']['chicken_villin_HP35.msmpk'] = path('molsysmt.data.msmpk', 'chicken_villin_HP35.msmpk')
tests['chicken villin HP35']['chicken_villin_HP35_solvated.msmpk'] = path('molsysmt.data.msmpk', 'chicken_villin_HP35_solvated.msmpk')
#tests['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd'] = path('molsysmt.data.dcd', 'traj_chicken_villin_HP35_solvated.dcd')
#tests['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5'] = path('molsysmt.data.h5', 'traj_chicken_villin_HP35_solvated.h5')


# T4 Lysozyme L99A

tests['T4 lysozyme L99A'] = {}
tests['T4 lysozyme L99A']['181l.pdb'] = path('molsysmt.data.pdb', '181l.pdb')
tests['T4 lysozyme L99A']['181l.mmtf'] = path('molsysmt.data.mmtf', '181l.mmtf')
tests['T4 lysozyme L99A']['181l.msmpk'] = path('molsysmt.data.msmpk', '181l.msmpk')
#tests['T4 lysozyme L99A']['1l17.pdb'] = path('molsysmt.data.pdb', '1l17.pdb')
#tests['T4 lysozyme L99A']['1l17.mmtf'] = path('molsysmt.data.mmtf', '1l17.mmtf')
tests['T4 lysozyme L99A']['1l17.msmpk'] = path('molsysmt.data.msmpk', '1l17.msmpk')
tests['T4 lysozyme L99A']['t4_lysozyme_L99A.msmpk'] = path('molsysmt.data.msmpk', 't4_lysozyme_L99A.msmpk')


# Pentalanine

tests['pentalanine'] = {}
tests['pentalanine']['pentalanine.inpcrd'] = path('molsysmt.data.inpcrd', 'pentalanine.inpcrd')
tests['pentalanine']['pentalanine.prmtop'] = path('molsysmt.data.prmtop', 'pentalanine.prmtop')
tests['pentalanine']['traj_pentalanine.h5'] = path('molsysmt.data.h5', 'traj_pentalanine.h5')


# Particles_4

tests['particles 4'] = {}
tests['particles 4']['traj_particles_4.xyznpy'] = path('molsysmt.data.xyznpy', 'traj_particles_4.xyznpy')


# Benzamidine

tests['benzamidine'] = {}
tests['benzamidine']['benzamidine.pdb'] = path('molsysmt.data.pdb', 'benzamidine.pdb')


# NGLView

tests['nglview'] = {}
#tests['nglview']['ala3.pdb'] = path('molsysmt.data.pdb', 'ala3.pdb')
tests['nglview']['md_1u19.gro'] = path('molsysmt.data.gro', 'md_1u19.gro')
#tests['nglview']['md_1u19.pdb'] = path('molsysmt.data.pdb', 'md_1u19.pdb')
#tests['nglview']['md_1u19.traj'] = path('molsysmt.data.traj', 'md_1u19.traj')
#tests['nglview']['md_1u19.trr'] = path('molsysmt.data.trr', 'md_1u19.trr')
tests['nglview']['md_1u19.xtc'] = path('molsysmt.data.xtc', 'md_1u19.xtc')


# TcTIM (to be removed)

tests['TcTIM'] = {}
#tests['TcTIM']['1tcd.pdb'] = path('molsysmt.data.pdb', '1tcd.pdb')
#tests['TcTIM']['1tcd.mmtf'] = path('molsysmt.data.mmtf', '1tcd.mmtf')
tests['TcTIM']['1tcd.msmpk'] = path('molsysmt.data.msmpk', '1tcd.msmpk')


# Trp-Cage

tests['Trp-Cage'] = {}
tests['Trp-Cage']['1l2y.pdb'] = path('molsysmt.data.pdb', '1l2y.pdb')
#tests['Trp-Cage']['1l2y.mmtf'] = path('molsysmt.data.mmtf', '1l2y.mmtf')


# Metenkephalin

tests['Met-enkephalin'] = {}
tests['Met-enkephalin']['met_enkephalin.pdb'] = path('molsysmt.data.pdb', 'met_enkephalin.pdb')
tests['Met-enkephalin']['met_enkephalin.msmpk'] = path('molsysmt.data.msmpk', 'met_enkephalin.msmpk')


# Two LJ particles

tests['two LJ particles'] = {}
tests['two LJ particles']['traj_two_lj_particles.trjpk'] = path('molsysmt.data.trjpk', 'traj_two_lj_particles.trjpk')


# Barnase - Barstar

tests['Barnase-Barstar'] = {}
tests['Barnase-Barstar']['barnase_barstar.msmpk'] = path('molsysmt.data.msmpk', 'barnase_barstar.msmpk')
tests['Barnase-Barstar']['1brs.mmtf'] = path('molsysmt.data.mmtf', '1brs.mmtf')


# POPC membrane

tests['POPC membrane'] = {}
tests['POPC membrane']['popc_membrane.psf'] = path('molsysmt.data.psf', 'popc_membrane.psf')
tests['POPC membrane']['popc_membrane.dcd'] = path('molsysmt.data.dcd', 'popc_membrane.dcd')
tests['POPC membrane']['popc_membrane.msmpk'] = path('molsysmt.data.msmpk', 'popc_membrane.msmpk')


### caffeine

tests['caffeine'] = {}
tests['caffeine']['caffeine.mol2'] = path('molsysmt.data.mol2', 'caffeine.mol2')


del(path)

