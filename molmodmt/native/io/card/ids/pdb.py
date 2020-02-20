
def from_pdb_id(pdb_id):

    from mmtf import fetch as _fetch_mmtf

    mmtf = _fetch_mmtf(pdb_id)
    pdb = from_mmtf(mmtf)
    del(mmtf,_fetch_mmtf)

    return pdb

