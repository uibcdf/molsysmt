from pathlib import PurePath as _Path

files={
    'pentalanine.h5' : str(_Path(__file__).parent.joinpath('pentalanine.h5')),
    'pentalanine.inpcrd' : str(_Path(__file__).parent.joinpath('pentalanine.inpcrd')),
    'pentalanine.prmtop' : str(_Path(__file__).parent.joinpath('pentalanine.prmtop')),
    'metenkephalin.pdb' : str(_Path(__file__).parent.joinpath('metenkephalin.pdb')),
    'trp-cage.pdb' : str(_Path(__file__).parent.joinpath('trp-cage.pdb')),
    'trp-cage_solvated.pdb' : str(_Path(__file__).parent.joinpath('trp-cage_solvated.pdb')),
    '1brs.pdb' : str(_Path(__file__).parent.joinpath('1brs.pdb')),
    '1brs.mmtf' : str(_Path(__file__).parent.joinpath('1brs.mmtf')),
    '1sux.pdb' : str(_Path(__file__).parent.joinpath('1sux.pdb')),
    '1sux.mmtf' : str(_Path(__file__).parent.joinpath('1sux.mmtf')),
    '1tcd.pdb' : str(_Path(__file__).parent.joinpath('1tcd.pdb')),
    '1tcd.mmtf' : str(_Path(__file__).parent.joinpath('1tcd.mmtf')),
    'caffeine.mol2' : str(_Path(__file__).parent.joinpath('caffeine.mol2')),
    'HIF1_HS_Mod.pdb' : str(_Path(__file__).parent.joinpath('HIF1_HS_Mod.pdb'))
}

