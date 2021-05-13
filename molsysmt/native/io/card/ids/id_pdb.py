
def from_id_pdb(id_pdb):

    from mmtf import fetch as _fetch_mmtf

    mmtf = _fetch_mmtf(pdb_id)
    pdb = from_mmtf(mmtf)
    del(mmtf,_fetch_mmtf)

    return pdb

