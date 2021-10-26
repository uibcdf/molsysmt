from pathlib import PurePath

parent = PurePath(__file__).parent

# Alanine dipeptide

alanine_dipeptide={}
alanine_dipeptide['vacuum.msmpk']=parent.joinpath('alanine_dipeptide/vacuum.msmpk').__str__()

# Proline dipeptide

proline_dipeptide={}
proline_dipeptide['vacuum.msmpk']=parent.joinpath('proline_dipeptide/vacuum.msmpk').__str__()

# Valine dipeptide

valine_dipeptide={}
valine_dipeptide['vacuum.msmpk']=parent.joinpath('valine_dipeptide/vacuum.msmpk').__str__()

# Lysine dipeptide

lysine_dipeptide={}
lysine_dipeptide['vacuum.msmpk']=parent.joinpath('lysine_dipeptide/vacuum.msmpk').__str__()

# Villin HP35

villin_HP35={}
villin_HP35['1vii.pdb']= parent.joinpath('villin_HP35/1vii.pdb').__str__()
villin_HP35['1vii.mmtf']= parent.joinpath('villin_HP35/1vii.mmtf').__str__()
villin_HP35['vacuum.msmpk']= parent.joinpath('villin_HP35/vacuum.msmpk').__str__()
villin_HP35['solvated.msmpk']= parent.joinpath('villin_HP35/solvated.msmpk').__str__()
villin_HP35['traj_explicit_solvent.dcd']= parent.joinpath('villin_HP35/traj_explicit_solvent.dcd').__str__()
villin_HP35['traj_explicit_solvent.h5']= parent.joinpath('villin_HP35/traj_explicit_solvent.h5').__str__()

# T4 Lysozyme L99A

t4_lysozyme_L99A={}
t4_lysozyme_L99A['181l.pdb']= parent.joinpath('t4_lysozyme_L99A/181l.pdb').__str__()
t4_lysozyme_L99A['181l.mmtf']= parent.joinpath('t4_lysozyme_L99A/181l.mmtf').__str__()
t4_lysozyme_L99A['vacuum.msmpk']= parent.joinpath('t4_lysozyme_L99A/vacuum.msmpk').__str__()

# Pentalanine

pentalanine={}
pentalanine['pentalanine.inpcrd']= parent.joinpath('pentalanine/pentalanine.inpcrd').__str__()
pentalanine['pentalanine.prmtop']= parent.joinpath('pentalanine/pentalanine.prmtop').__str__()
pentalanine['traj.h5']= parent.joinpath('pentalanine/traj.h5').__str__()

# Particles_4

particles_4={}
particles_4['particles_4_frames_3.xyznpy']= parent.joinpath('particles_4/particles_4_frames_3.xyznpy').__str__()

# Benzamidine

benzamidine={}
benzamidine['benzamidine.pdb']= parent.joinpath('benzamidine/benzamidine.pdb').__str__()

# Caffeine

caffeine={}
caffeine['caffeine.mol2']= parent.joinpath('caffeine/caffeine.mol2').__str__()

# NGLView

nglview={}
nglview['1u19.gro']= parent.joinpath('nglview/1u19.gro').__str__()
nglview['1u19.xtc']= parent.joinpath('nglview/1u19.xtc').__str__()


del(PurePath, parent)

