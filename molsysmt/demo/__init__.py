import importlib.resources
from pathlib import Path

data_dir = importlib.resources('molsysmt/data')

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
demo['alanine dipeptide']['dialanine.msmpk'] = Path(data_dir, 'dialanine.msmpk')


# Proline dipeptide

demo['proline dipeptide'] = {}
demo['proline dipeptide']['diproline.msmpk'] = Path(data_dir, 'msmpk/diproline.msmpk')


# Valine dipeptide

demo['valine dipeptide'] = {}
demo['valine dipeptide']['divaline.msmpk'] = Path(data_dir, 'msmpk/divaline.msmpk')


# Lysine dipeptide

demo['lysine dipeptide'] = {}
demo['lysine dipeptide']['dilysine.msmpk'] = Path(data_dir, 'msmpk/dilysine.msmpk')


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


# Pentarginine

demo['pentarginine'] = {}
demo['pentarginine']['traj_pentarginine.h5'] = Path(data_dir, 'h5/traj_pentarginine.h5')


# Particles_4

demo['4 particles'] = {}
demo['4 particles']['traj_particles_4.xyznpy'] = Path(data_dir, 'xyznpy/traj_particles_4.xyznpy')


# Benzamidine

demo['benzamidine'] = {}
demo['benzamidine']['benzamidine.pdb'] = Path(data_dir, 'pdb/benzamidine.pdb')




del(importlib.resources, Path, data_dir)

