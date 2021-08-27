from pathlib import PurePath

def get_path(filename):

    return str(PurePath(__file__).parent.joinpath('files/'+filename))

filenames = [
    'pentalanine.h5',
    'pentalanine.inpcrd',
    'pentalanine.prmtop',
    'metenkephalin.pdb',
    'trp-cage.pdb',
    'trp-cage_solvated.pdb',
    '1brs.pdb',
    '1brs.mmtf',
    '1sux.pdb',
    '1sux.mmtf',
    '1tcd.pdb',
    '1tcd.mmtf',
    'caffeine.mol2',
    'proline_dipeptide_vacuum.msmpk',
    'valine_dipeptide_vacuum.msmpk',
    'lysine_dipeptide_vacuum.msmpk',
    ]

files_dict = {filename : get_path(filename) for filename in filenames}

