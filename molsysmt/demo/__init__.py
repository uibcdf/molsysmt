from pathlib import PurePath

parent = PurePath(__file__).parent

demo = {}

# Alanine dipeptide

demo['alanine dipeptide'] = {}
demo['alanine dipeptide']['vacuum.msmpk'] = parent.joinpath('alanine_dipeptide/vacuum.msmpk').__str__()

# Proline dipeptide

demo['proline dipeptide'] = {}
demo['proline dipeptide']['vacuum.msmpk'] = parent.joinpath('proline_dipeptide/vacuum.msmpk').__str__()

# Valine dipeptide

demo['valine dipeptide'] = {}
demo['valine dipeptide']['vacuum.msmpk'] = parent.joinpath('valine_dipeptide/vacuum.msmpk').__str__()

# Lysine dipeptide

demo['lysine dipeptide'] = {}
demo['lysine dipeptide']['vacuum.msmpk'] = parent.joinpath('lysine_dipeptide/vacuum.msmpk').__str__()

# Villin HP35

demo['chicken villin HP35'] = {}
demo['chicken villin HP35']['1vii.pdb'] = parent.joinpath('villin_HP35/1vii.pdb').__str__()
demo['chicken villin HP35']['1vii.mmtf'] = parent.joinpath('villin_HP35/1vii.mmtf').__str__()
demo['chicken villin HP35']['vacuum.msmpk'] = parent.joinpath('villin_HP35/vacuum.msmpk').__str__()
demo['chicken villin HP35']['solvated.msmpk'] = parent.joinpath('villin_HP35/solvated.msmpk').__str__()
demo['chicken villin HP35']['traj_explicit_solvent.dcd'] = parent.joinpath(
    'villin_HP35/traj_explicit_solvent.dcd').__str__()
demo['chicken villin HP35']['traj_explicit_solvent.h5'] = parent.joinpath(
    'villin_HP35/traj_explicit_solvent.h5').__str__()

# T4 Lysozyme L99A

demo['T4 lysozyme L99A'] = {}
demo['T4 lysozyme L99A']['181l.pdb'] = parent.joinpath('t4_lysozyme_L99A/181l.pdb').__str__()
demo['T4 lysozyme L99A']['181l.mmtf'] = parent.joinpath('t4_lysozyme_L99A/181l.mmtf').__str__()
demo['T4 lysozyme L99A']['181l.msmpk'] = parent.joinpath('t4_lysozyme_L99A/181l.msmpk').__str__()
demo['T4 lysozyme L99A']['vacuum.msmpk'] = parent.joinpath('t4_lysozyme_L99A/vacuum.msmpk').__str__()
demo['T4 lysozyme L99A']['1l17.pdb'] = parent.joinpath('t4_lysozyme_L99A/1l17.pdb').__str__()
demo['T4 lysozyme L99A']['1l17.mmtf'] = parent.joinpath('t4_lysozyme_L99A/1l17.mmtf').__str__()
demo['T4 lysozyme L99A']['1l17.msmpk'] = parent.joinpath('t4_lysozyme_L99A/1l17.msmpk').__str__()

# Pentalanine

demo['pentalanine'] = {}
demo['pentalanine']['pentalanine.inpcrd'] = parent.joinpath('pentalanine/pentalanine.inpcrd').__str__()
demo['pentalanine']['pentalanine.prmtop'] = parent.joinpath('pentalanine/pentalanine.prmtop').__str__()
demo['pentalanine']['traj.h5'] = parent.joinpath('pentalanine/traj.h5').__str__()

# Pentarginine

demo['pentarginine'] = {}
demo['pentarginine']['traj.h5'] = parent.joinpath('pentarginine/traj.h5').__str__()

# Particles_4

demo['4 particles'] = {}
demo['4 particles']['traj.xyznpy'] = parent.joinpath('particles_4/traj.xyznpy').__str__()

# Benzamidine

demo['benzamidine'] = {}
demo['benzamidine']['benzamidine.pdb'] = parent.joinpath('benzamidine/benzamidine.pdb').__str__()

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

# 1SUX
demo['1SUX'] = {}
demo['1SUX']['1sux.pdb'] = parent.joinpath('1sux/1sux.pdb').__str__()
demo['1SUX']['1sux.mmtf'] = parent.joinpath('1sux/1sux.mmtf').__str__()

# 5ZMZ
demo['5ZMZ'] = {}
demo['5ZMZ']['5zmz.pdb'] = parent.joinpath('5zmz/5zmz.pdb').__str__()
demo['5ZMZ']['5zmz.mmtf'] = parent.joinpath('5zmz/5zmz.mmtf').__str__()

del (PurePath, parent)
