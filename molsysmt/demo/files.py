from pathlib import PurePath

def get_path(filename):

    return str(PurePath(__file__).parent.joinpath('files/'+filename))

files_dict={}

# Two LJ particles
files_dict['two_lj_particles_traj.trjpk'] = get_path('two_lj_particles/two_lj_particles_traj.trjpk')

# Villin HP35

files_dict['1vii.pdb'] = get_path('villin_hp35/1vii.pdb')
files_dict['1vii.mmtf'] = get_path('villin_hp35/1vii.mmtf')
files_dict['villin_hp35_vacuum.msmpk'] = get_path('villin_hp35/villin_hp35_vacuum.msmpk')
files_dict['villin_hp35_solvated.msmpk'] = get_path('villin_hp35/villin_hp35_solvated.msmpk')
files_dict['villin_hp35_solvated.dcd'] = get_path('villin_hp35/villin_hp35_solvated.dcd')
files_dict['villin_hp35_solvated.h5'] = get_path('villin_hp35/villin_hp35_solvated.h5')
files_dict['villin_hp35_solvated_last.pdb'] = get_path('villin_hp35/villin_hp35_solvated_last.pdb')


#filenames = [
#    'pentalanine.h5',
#    'pentalanine.inpcrd',
#    'pentalanine.prmtop',
#    'metenkephalin.pdb',
#    'trp-cage.pdb',
#    'trp-cage_solvated.pdb',
#    '1brs.pdb',
#    '1brs.mmtf',
#    '1sux.pdb',
#    '1sux.mmtf',
#    '1tcd.pdb',
#    '1tcd.mmtf',
#    '181l.pdb',
#    '181l.mmtf',
#    '1l17.pdb',
#    '1l17.mmtf',
#    'caffeine.mol2',
#    'nglview_demo_md_1u19.gro',
#    'nglview_demo_md_1u19.xtc',
#    'proline_dipeptide_vacuum.msmpk',
#    'valine_dipeptide_vacuum.msmpk',
#    'lysine_dipeptide_vacuum.msmpk',
#    'T4_Lysozyme_L99A_in_pdbid_181l.msmpk',
#    'TcTIM_in_pdbid_1tcd.msmpk',
#    'pentalanine_traj.msmpk',
#    'particles_4_frames_3.xyznpy',
#    'Ar_Xe_pbc_vacuum.trjpk',
#    ]

#files_dict = {filename : get_path(filename) for filename in filenames}

