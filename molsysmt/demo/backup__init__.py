import importlib.resources
from pathlib import Path

data_dir = importlib.resources('molsysmt/data')

demo = {}
# Caffeine

demo['caffeine'] = {}
demo['caffeine']['caffeine.mol2'] = parent.joinpath('caffeine/caffeine.mol2').__str__()

# NGLView

demo['nglview'] = {}
demo['nglview']['ala3.pdb'] = parent.joinpath('nglview/ala3.pdb').__str__()
demo['nglview']['md_1u19.gro'] = parent.joinpath('nglview/md_1u19.gro').__str__()
demo['nglview']['md_1u19.pdb'] = parent.joinpath('nglview/md_1u19.pdb').__str__()
demo['nglview']['md_1u19.traj'] = parent.joinpath('nglview/md_1u19.traj').__str__()
demo['nglview']['md_1u19.trr'] = parent.joinpath('nglview/md_1u19.trr').__str__()
demo['nglview']['md_1u19.xtc'] = parent.joinpath('nglview/md_1u19.xtc').__str__()

# TcTIM (to be removed)

demo['TcTIM'] = {}
demo['TcTIM']['1tcd.pdb'] = parent.joinpath('TcTIM/1tcd.pdb').__str__()
demo['TcTIM']['1tcd.mmtf'] = parent.joinpath('TcTIM/1tcd.mmtf').__str__()
demo['TcTIM']['1tcd.msmpk'] = parent.joinpath('TcTIM/1tcd.msmpk').__str__()

# Trp-Cage

demo['Trp-Cage'] = {}
demo['Trp-Cage']['1l2y.pdb'] = parent.joinpath('Trp-Cage/1l2y.pdb').__str__()
demo['Trp-Cage']['1l2y.mmtf'] = parent.joinpath('Trp-Cage/1l2y.mmtf').__str__()

# Metenkephalin

demo['Met-enkephalin'] = {}
demo['Met-enkephalin']['vacuum.pdb'] = parent.joinpath('Met-enkephalin/vacuum.pdb').__str__()
demo['Met-enkephalin']['vacuum.msmpk'] = parent.joinpath('Met-enkephalin/vacuum.msmpk').__str__()

# Two LJ particles

demo['two LJ particles'] = {}
demo['two LJ particles']['traj.trjpk'] = parent.joinpath('two_LJ_particles/traj.trjpk').__str__()

# Barnase - Barstar

demo['Barnase-Barstar'] = {}
demo['Barnase-Barstar']['barnase_barstar.pdb'] = parent.joinpath('barnase_barstar/barnase_barstar.pdb').__str__()
demo['Barnase-Barstar']['barnase_barstar.msmpk'] = parent.joinpath('barnase_barstar/barnase_barstar.msmpk').__str__()
demo['Barnase-Barstar']['1brs.mmtf'] = parent.joinpath('barnase_barstar/1brs.mmtf').__str__()

# POPC membrane
demo['membrane'] = {}
demo['membrane']['membrane.psf'] = parent.joinpath('membrane/membrane.psf').__str__()
demo['membrane']['membrane.dcd'] = parent.joinpath('membrane/membrane.dcd').__str__()
demo['membrane']['membrane.msmpk'] = parent.joinpath('membrane/membrane.msmpk').__str__()


del (PurePath, parent)
