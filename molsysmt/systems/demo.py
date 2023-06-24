import sys

if sys.version_info[1]==10:
    from importlib.resources import files
    def path(package, file):
        return files(package).joinpath(file)
elif sys.version_info[1] in (8,9):
    from pathlib import PurePath
    parent = PurePath(__file__).parent
    def path(package, file):
        data_dir = package.split('.')[-1]
        return parent.joinpath('../data/'+data_dir+'/'+file).__str__()

demo = {}

# 1SUX
demo['1SUX'] = {}
demo['1SUX']['1sux.pdb'] = path('molsysmt.data.pdb','1sux.pdb')
demo['1SUX']['1sux.mmtf'] = path('molsysmt.data.mmtf','1sux.mmtf')


# 5ZMZ
demo['5ZMZ'] = {}
demo['5ZMZ']['5zmz.pdb'] = path('molsysmt.data.pdb', '5zmz.pdb')
demo['5ZMZ']['5zmz.mmtf'] = path('molsysmt.data.mmtf', '5zmz.mmtf')


# Alanine dipeptide

demo['alanine dipeptide'] = {}
demo['alanine dipeptide']['alanine_dipeptide.msmpk'] = path('molsysmt.data.msmpk', 'alanine_dipeptide.msmpk')


# Proline dipeptide

demo['proline dipeptide'] = {}
demo['proline dipeptide']['proline_dipeptide.msmpk'] = path('molsysmt.data.msmpk', 'proline_dipeptide.msmpk')


# Valine dipeptide

demo['valine dipeptide'] = {}
demo['valine dipeptide']['valine_dipeptide.msmpk'] = path('molsysmt.data.msmpk', 'valine_dipeptide.msmpk')


# Lysine dipeptide

demo['lysine dipeptide'] = {}
demo['lysine dipeptide']['lysine_dipeptide.msmpk'] = path('molsysmt.data.msmpk', 'lysine_dipeptide.msmpk')


# Villin HP35

demo['chicken villin HP35'] = {}
demo['chicken villin HP35']['1vii.pdb'] = path('molsysmt.data.pdb', '1vii.pdb')
demo['chicken villin HP35']['1vii.mmtf'] = path('molsysmt.data.mmtf', '1vii.mmtf')
demo['chicken villin HP35']['chicken_villin_HP35.msmpk'] = path('molsysmt.data.msmpk', 'chicken_villin_HP35.msmpk')
demo['chicken villin HP35']['chicken_villin_HP35_solvated.msmpk'] = path('molsysmt.data.msmpk', 'chicken_villin_HP35_solvated.msmpk')
demo['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd'] = path('molsysmt.data.dcd', 'traj_chicken_villin_HP35_solvated.dcd')
demo['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5'] = path('molsysmt.data.h5', 'traj_chicken_villin_HP35_solvated.h5')


# T4 Lysozyme L99A

demo['T4 lysozyme L99A'] = {}
demo['T4 lysozyme L99A']['181l.pdb'] = path('molsysmt.data.pdb', '181l.pdb')
demo['T4 lysozyme L99A']['181l.mmtf'] = path('molsysmt.data.mmtf', '181l.mmtf')
demo['T4 lysozyme L99A']['181l.msmpk'] = path('molsysmt.data.msmpk', '181l.msmpk')
demo['T4 lysozyme L99A']['1l17.pdb'] = path('molsysmt.data.pdb', '1l17.pdb')
demo['T4 lysozyme L99A']['1l17.mmtf'] = path('molsysmt.data.mmtf', '1l17.mmtf')
demo['T4 lysozyme L99A']['1l17.msmpk'] = path('molsysmt.data.msmpk', '1l17.msmpk')
demo['T4 lysozyme L99A']['t4_lysozyme_L99A.msmpk'] = path('molsysmt.data.msmpk', 't4_lysozyme_L99A.msmpk')


# Pentalanine

demo['pentalanine'] = {}
demo['pentalanine']['pentalanine.inpcrd'] = path('molsysmt.data.inpcrd', 'pentalanine.inpcrd')
demo['pentalanine']['pentalanine.prmtop'] = path('molsysmt.data.prmtop', 'pentalanine.prmtop')
demo['pentalanine']['traj_pentalanine.h5'] = path('molsysmt.data.h5', 'traj_pentalanine.h5')


# Particles_4

demo['particles 4'] = {}
demo['particles 4']['traj_particles_4.xyznpy'] = path('molsysmt.data.xyznpy', 'traj_particles_4.xyznpy')


# Benzamidine

demo['benzamidine'] = {}
demo['benzamidine']['benzamidine.pdb'] = path('molsysmt.data.pdb', 'benzamidine.pdb')


# NGLView

demo['nglview'] = {}
demo['nglview']['ala3.pdb'] = path('molsysmt.data.pdb', 'ala3.pdb')
demo['nglview']['md_1u19.gro'] = path('molsysmt.data.gro', 'md_1u19.gro')
demo['nglview']['md_1u19.pdb'] = path('molsysmt.data.pdb', 'md_1u19.pdb')
demo['nglview']['md_1u19.traj'] = path('molsysmt.data.traj', 'md_1u19.traj')
demo['nglview']['md_1u19.trr'] = path('molsysmt.data.trr', 'md_1u19.trr')
demo['nglview']['md_1u19.xtc'] = path('molsysmt.data.xtc', 'md_1u19.xtc')


# TcTIM (to be removed)

demo['TcTIM'] = {}
demo['TcTIM']['1tcd.pdb'] = path('molsysmt.data.pdb', '1tcd.pdb')
demo['TcTIM']['1tcd.mmtf'] = path('molsysmt.data.mmtf', '1tcd.mmtf')
demo['TcTIM']['1tcd.msmpk'] = path('molsysmt.data.msmpk', '1tcd.msmpk')


# Trp-Cage

demo['Trp-Cage'] = {}
demo['Trp-Cage']['1l2y.pdb'] = path('molsysmt.data.pdb', '1l2y.pdb')
demo['Trp-Cage']['1l2y.mmtf'] = path('molsysmt.data.mmtf', '1l2y.mmtf')


# Metenkephalin

demo['Met-enkephalin'] = {}
demo['Met-enkephalin']['met_enkephalin.pdb'] = path('molsysmt.data.pdb', 'met_enkephalin.pdb')
demo['Met-enkephalin']['met_enkephalin.msmpk'] = path('molsysmt.data.msmpk', 'met_enkephalin.msmpk')


# Two LJ particles

demo['two LJ particles'] = {}
demo['two LJ particles']['traj_two_lj_particles.trjpk'] = path('molsysmt.data.trjpk', 'traj_two_lj_particles.trjpk')


# Barnase - Barstar

demo['Barnase-Barstar'] = {}
demo['Barnase-Barstar']['barnase_barstar.msmpk'] = path('molsysmt.data.msmpk', 'barnase_barstar.msmpk')
demo['Barnase-Barstar']['1brs.mmtf'] = path('molsysmt.data.mmtf', '1brs.mmtf')


# POPC membrane

demo['POPC membrane'] = {}
demo['POPC membrane']['popc_membrane.psf'] = path('molsysmt.data.psf', 'popc_membrane.psf')
demo['POPC membrane']['popc_membrane.dcd'] = path('molsysmt.data.dcd', 'popc_membrane.dcd')
demo['POPC membrane']['popc_membrane.msmpk'] = path('molsysmt.data.msmpk', 'popc_membrane.msmpk')


### caffeine

demo['caffeine'] = {}
demo['caffeine']['caffeine.mol2'] = path('molsysmt.data.mol2', 'caffeine.mol2')


