from os.path import dirname as _dirname

_path_examples=_dirname(__file__)+'/data'

_path_pdb=_path_examples+'/pdb'
pdb = {
    '1l2y' : _path_pdb+'/1l2y.pdb',
    '1li2' : _path_pdb+'/1li2.pdb'
}

_path_mol2=_path_examples+'/mol2'
mol2 = {
    'caffeine' : _path_mol2+'/caffeine.mol2',
}

_path_smi=_path_examples+'/smi'
smi = {
    'caffeine' : _path_smi+'/caffeine.smi',
}

_path_sdf=_path_examples+'/sdf'
sdf = {
    'caffeine' : _path_sdf+'/caffeine.sdf',
}

_path_ddb=_path_examples+'/ddb'
ddb = {
    'caffeine' : _path_ddb+'/caffeine.ddb',
}
