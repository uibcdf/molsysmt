# Empty-connectivity regression fixture

`topomt_geometric_tetrahedron.pdb` is copied byte-for-byte from TopoMT's frozen
geometric input at commit `88e2164c17b118327ff8fc7383a9b2a4c1e60ed0`:
[original artifact](https://github.com/uibcdf/topomt/blob/88e2164c17b118327ff8fc7383a9b2a4c1e60ed0/docs/content/showcase/dfnd/artifacts/regular_tetrahedron_v1/input_castp.pdb).
It has four DUM/C atoms, one coordinate structure, and no CONECT records.
It is a geometry fixture, not a chemically complete carbon molecule.

SHA256: `e40db4e92eb260682c4e77e43873425efda37f96a55008da0e2a0721c57bc5cb`.
The offline guard is `tests/form/molsysmt_Topology/test_empty_bond_queries.py`;
provider issue: `uibcdf/molsysmt#283`, consumer context: `uibcdf/topomt#79`.
