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

# 1SUX
#systems['1SUX'] = {}
#systems['1SUX']['1sux.pdb'] = path('molsysmt.data.pdb','1sux.pdb')
#systems['1SUX']['1sux.mmtf'] = path('molsysmt.data.mmtf','1sux.mmtf')


# 5ZMZ
#systems['5ZMZ'] = {}
#systems['5ZMZ']['5zmz.pdb'] = path('molsysmt.data.pdb', '5zmz.pdb')
#systems['5ZMZ']['5zmz.mmtf'] = path('molsysmt.data.mmtf', '5zmz.mmtf')


# Alanine dipeptide

systems['alanine dipeptide'] = {}
systems['alanine dipeptide']['alanine_dipeptide.h5msm'] = path('molsysmt.data.h5msm', 'alanine_dipeptide.h5msm')


# Proline dipeptide

systems['proline dipeptide'] = {}
systems['proline dipeptide']['proline_dipeptide.h5msm'] = path('molsysmt.data.h5msm', 'proline_dipeptide.h5msm')


# Valine dipeptide

systems['valine dipeptide'] = {}
systems['valine dipeptide']['valine_dipeptide.h5msm'] = path('molsysmt.data.h5msm', 'valine_dipeptide.h5msm')


# Lysine dipeptide

systems['lysine dipeptide'] = {}
systems['lysine dipeptide']['lysine_dipeptide.h5msm'] = path('molsysmt.data.h5msm', 'lysine_dipeptide.h5msm')


# Villin HP35

systems['chicken villin HP35'] = {}
systems['chicken villin HP35']['1vii.pdb'] = path('molsysmt.data.pdb', '1vii.pdb')
systems['chicken villin HP35']['1vii.mmtf'] = path('molsysmt.data.mmtf', '1vii.mmtf')
systems['chicken villin HP35']['chicken_villin_HP35.h5msm'] = path('molsysmt.data.h5msm', 'chicken_villin_HP35.h5msm')
systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'] = path('molsysmt.data.h5msm', 'chicken_villin_HP35_solvated.h5msm')
systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd'] = path('molsysmt.data.dcd', 'traj_chicken_villin_HP35_solvated.dcd')
systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5'] = path('molsysmt.data.h5', 'traj_chicken_villin_HP35_solvated.h5')


# T4 Lysozyme L99A

systems['T4 lysozyme L99A'] = {}
systems['T4 lysozyme L99A']['181l.pdb'] = path('molsysmt.data.pdb', '181l.pdb')
systems['T4 lysozyme L99A']['181l.mmtf'] = path('molsysmt.data.mmtf', '181l.mmtf')
systems['T4 lysozyme L99A']['181l.h5msm'] = path('molsysmt.data.h5msm', '181l.h5msm')
systems['T4 lysozyme L99A']['1l17.pdb'] = path('molsysmt.data.pdb', '1l17.pdb')
systems['T4 lysozyme L99A']['1l17.mmtf'] = path('molsysmt.data.mmtf', '1l17.mmtf')
systems['T4 lysozyme L99A']['1l17.h5msm'] = path('molsysmt.data.h5msm', '1l17.h5msm')
systems['T4 lysozyme L99A']['t4_lysozyme_L99A.h5msm'] = path('molsysmt.data.h5msm', 't4_lysozyme_L99A.h5msm')


# Pentalanine

systems['pentalanine'] = {}
systems['pentalanine']['pentalanine.inpcrd'] = path('molsysmt.data.inpcrd', 'pentalanine.inpcrd')
systems['pentalanine']['pentalanine.prmtop'] = path('molsysmt.data.prmtop', 'pentalanine.prmtop')
systems['pentalanine']['traj_pentalanine.h5'] = path('molsysmt.data.h5', 'traj_pentalanine.h5')


# Particles_4

systems['particles 4'] = {}
systems['particles 4']['traj_particles_4.xyznpy'] = path('molsysmt.data.xyznpy', 'traj_particles_4.xyznpy')


# Benzamidine

systems['benzamidine'] = {}
systems['benzamidine']['benzamidine.pdb'] = path('molsysmt.data.pdb', 'benzamidine.pdb')


# NGLView

systems['nglview'] = {}
systems['nglview']['ala3.pdb'] = path('molsysmt.data.pdb', 'ala3.pdb')
systems['nglview']['md_1u19.gro'] = path('molsysmt.data.gro', 'md_1u19.gro')
systems['nglview']['md_1u19.pdb'] = path('molsysmt.data.pdb', 'md_1u19.pdb')
systems['nglview']['md_1u19.traj'] = path('molsysmt.data.traj', 'md_1u19.traj')
systems['nglview']['md_1u19.trr'] = path('molsysmt.data.trr', 'md_1u19.trr')
systems['nglview']['md_1u19.xtc'] = path('molsysmt.data.xtc', 'md_1u19.xtc')


# TcTIM (to be removed)

systems['TcTIM'] = {}
systems['TcTIM']['1tcd.pdb'] = path('molsysmt.data.pdb', '1tcd.pdb')
systems['TcTIM']['1tcd.mmtf'] = path('molsysmt.data.mmtf', '1tcd.mmtf')
systems['TcTIM']['1tcd.h5msm'] = path('molsysmt.data.h5msm', '1tcd.h5msm')


# Trp-Cage

systems['Trp-Cage'] = {}
systems['Trp-Cage']['1l2y.pdb'] = path('molsysmt.data.pdb', '1l2y.pdb')
systems['Trp-Cage']['1l2y.h5msm'] = path('molsysmt.data.h5msm', '1l2y.h5msm')


# Metenkephalin

systems['Met-enkephalin'] = {}
systems['Met-enkephalin']['met_enkephalin.pdb'] = path('molsysmt.data.pdb', 'met_enkephalin.pdb')
systems['Met-enkephalin']['met_enkephalin.h5msm'] = path('molsysmt.data.h5msm', 'met_enkephalin.h5msm')


# Two LJ particles

systems['two LJ particles'] = {}
systems['two LJ particles']['traj_two_lj_particles.trjpk'] = path('molsysmt.data.trjpk', 'traj_two_lj_particles.trjpk')


# Barnase - Barstar

systems['Barnase-Barstar'] = {}
systems['Barnase-Barstar']['barnase_barstar.h5msm'] = path('molsysmt.data.h5msm', 'barnase_barstar.h5msm')
systems['Barnase-Barstar']['1brs.mmtf'] = path('molsysmt.data.mmtf', '1brs.mmtf')


# POPC membrane

systems['POPC membrane'] = {}
systems['POPC membrane']['popc_membrane.psf'] = path('molsysmt.data.psf', 'popc_membrane.psf')
systems['POPC membrane']['popc_membrane.dcd'] = path('molsysmt.data.dcd', 'popc_membrane.dcd')
systems['POPC membrane']['popc_membrane.msmpk'] = path('molsysmt.data.msmpk', 'popc_membrane.msmpk')

# POPC

systems['POPC'] = {}
systems['POPC']['popc.crd'] = path('molsysmt.data.crd', 'popc.crd')
systems['POPC']['popc.psf'] = path('molsysmt.data.psf', 'popc.psf')



### caffeine

systems['caffeine'] = {}
systems['caffeine']['caffeine.mol2'] = path('molsysmt.data.mol2', 'caffeine.mol2')


