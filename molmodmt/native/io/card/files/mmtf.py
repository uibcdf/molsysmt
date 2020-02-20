from numpy import column_stack as _column_stack
from molmodel import PDB as _PDB
from .to_bioassembly import from_mmtf as _bioassembly_from_mmtf
from .to_chain import from_bioassembly as _chain_from_bioassembly
from .to_entity import from_bioassembly as _entity_from_bioassembly
from .to_segment import from_bioassembly as _segment_from_bioassembly
from .to_group import from_bioassembly as _group_from_bioassembly
from .to_atom import from_bioassembly as _atom_from_bioassembly

def from_mmtf(mmtf):

    pdb=_PDB()

    pdb.id = mmtf.structure_id
    pdb.method = mmtf.experimental_methods
    pdb.title = mmtf.title
    pdb.resolution = mmtf.resolution
    pdb.deposition_date = mmtf.deposition_date
    pdb.unit_cell = mmtf.unit_cell
    pdb.num_models = mmtf.num_models

    pdb.bioassembly = _bioassembly_from_mmtf(mmtf)
    pdb.chain = _chain_from_bioassembly(pdb.bioassembly)
    pdb.entity = _entity_from_bioassembly(pdb.bioassembly)
    pdb.segment = _segment_from_bioassembly(pdb.bioassembly)
    pdb.group = _group_from_bioassembly(pdb.bioassembly)
    pdb.atom = _atom_from_bioassembly(pdb.bioassembly)

    pdb.num_bioassemblies = len(mmtf.bio_assembly)
    pdb.num_chains = len(pdb.chain)
    pdb.num_segments = len(pdb.segment)
    pdb.num_entities = len(pdb.entity)
    pdb.num_groups = len(pdb.group)
    pdb.num_atoms = len(pdb.atom)

    pdb.coordinates = _column_stack([mmtf.x_coord_list,
                                     mmtf.y_coord_list,
                                     mmtf.z_coord_list])
    pdb.coordinates = pdb.coordinates.reshape(pdb.num_models, pdb.num_atoms, 3)

    pdb.b_factors = mmtf.b_factor_list.reshape(pdb.num_models, pdb.num_atoms)

    return pdb

