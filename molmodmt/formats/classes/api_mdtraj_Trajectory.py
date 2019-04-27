from os.path import basename as _basename
from mdtraj.core.trajectory import Trajectory as _mdtraj_Trajectory

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_Trajectory:form_name,
    'mdtraj.Trajectory':form_name
    }

def to_aminoacids3_seq(item):

    return ''.join([ r.name for r in item.topology.residues ])

def to_aminoacids1_seq(item):

    from molmodmt.formats.seqs.api_aminoacids3 import to_aminoacids1_seq as _aminoacids3_to_aminoacids1
    tmp_item = to_aminoacids3_seq(item)
    tmp_item = _aminoacids3_to_aminoacids1(tmp_item)
    del(_aminoacids3_to_aminoacids1)
    return tmp_item

def to_biopython_Seq(item):

    from molmodmt.formats.seqs.api_aminoacids1 import to_biopython_Seq as _aminoacids1_to_biopython_Seq
    tmp_item = to_aminoacids1_seq(item)
    tmp_item = _aminoacids1_to_biopython_Seq(tmp_item)
    del(_aminoacids1_to_biopython_Seq)
    return tmp_item

def to_biopython_SeqRecord(item):

    from molmodmt.formats.seqs.api_aminoacids1 import to_biopython_SeqRecord as _aminoacids1_to_biopython_SeqRecord
    tmp_item = to_aminoacids1_seq(item)
    tmp_item = _aminoacids1_to_biopython_SeqRecord(tmp_item)
    del(_aminoacids1_to_biopython_SeqRecord)
    return tmp_item

def to_molmodmt_MolMod(item, selection=None, syntaxis='mdtraj'):

    from molmodmt.native.io_molmod import from_mdtraj_Trajectory as _molmodmt_MolMod_from_mdtraj_Trajectory
    tmp_item = _molmodmt_MolMod_from_mdtraj_Trajectory(item, selection=selection, syntaxis=syntaxis)
    return tmp_item

def to_molmodmt_Trajectory(item, selection=None, syntaxis='mdtraj'):

    from molmodmt.native.io_trajectory import from_mdtraj_Trajectory as _molmodmt_Trajectory_from_mdtraj_Trajectory
    tmp_item = _molmodmt_Trajectory_from_mdtraj_Trajectory(item, selection=selection,
                                                           syntaxis=syntaxis)
    return tmp_item

def to_molmodmt_Topology(item):

    from molmodmt.native.io_topology import from_mdtraj_Topology as _molmodmt_Topology_from_mdtraj_Trajectory
    tmp_item = _molmodmt_Topology_from_mdtraj_Trajectory(item, selection=selection,
                                                         syntaxis=syntaxis)
    return tmp_item

def to_molmodmt(item, selection=None, syntaxis='mdtraj'):

    return to_molmodmt_MolMod(item, selection=selection, syntaxis=syntaxis)

def to_mdtraj_Topology(item, selection=None, syntaxis='mdtraj'):

    return item.topology

def to_mdtraj(item):
    return item

def to_openmm_Topology(item):

    from .api_mdtraj_Topology import to_openmm_Topology as _mdtraj_Topology_to_openmm_Topology

    tmp_form = to_mdtraj_Topology(item)
    tmp_form = _mdtraj_Topology_to_openmm_Topology(tmp_form)
    del(_mdtraj_Topology_to_openmm_Topology)
    return tmp_form

def to_openmm_Positions(item):

    from simtk import unit as _units
    return item.xyz*_units.nanometers

def to_yank_Topography(item):

    from .api_openmm_Topology import to_yank_Topography as _openmm_Topology_to_yank_Topography

    tmp_form = to_openmm_Topology(item)
    tmp_form = _openmm_Topology_to_yank_Topography(tmp_form)
    del(_openmm_Topology_to_yank_Topography)
    return tmp_form

def to_parmed_Structure(item):

    from .api_openmm_Topology import to_parmed_Structure as _openmm_Topology_to_parmed_Structure

    tmp_form = to_openmm_Topology(item)
    tmp_form = _openmm_Topology_to_parmed_Structure(tmp_form)
    del(_openmm_Topology_to_parmed_Structure)
    return tmp_form

def to_mdtraj_Topology(item):

    return item.topology

def to_pdbfixer_PDBFixer(item):

    from molmodmt.formats.files.api_pdb import to_pdbfixer as _pdb_to_pdbfixer
    import tempfile as _tempfile
    from os import remove as _remove

    tmp_pdbfilename = _tempfile.NamedTemporaryFile(suffix=".pdb").name
    tmp_system = to_pdb(item,tmp_pdbfilename)
    tmp_item = _pdb_to_pdbfixer(tmp_pdbfilename)
    _remove(tmp_pdbfilename)
    del(_pdb_to_pdbfixer, tmp_pdbfilename, _tempfile, _remove)
    return tmp_item

def to_pdbfixer(item):

    return to_pdbfixer_PDBFixer(item)

def to_parmed(item):

    return to_parmed_Structure(item)

def to_pdb(item,filename):

    return item.save_pdb(filename)

def to_xtc(item,filename):
    return item.save_xtc(filename)

def to_nglview(item):

    from nglview import show_mdtraj as _show_mdtraj
    from molmodmt import merge as _merge

    if type(item) in [list,tuple]:
        tmp_item = _merge(item)
        tmp_view = _show_mdtraj(tmp_item)
    else:
         tmp_view = _show_mdtraj(item)

    return tmp_view

def get(item, atoms_list=None, **kwargs):

    if atoms_list is not None:
        tmp_item = extract(item,atoms_list)
    else:
        tmp_item = item

    result=[]
    for option in kwargs:
        if option=='n_atoms' and kwargs[option]==True:
            result.append(tmp_item.n_atoms)
        if option=='n_frames' and kwargs[option]==True:
            result.append(tmp_item.n_frames)
        if option=='n_residues' and kwargs[option]==True:
            result.append(tmp_item.n_residues)
        if option=='n_molecules' and kwargs[option]==True:
            result.append(len(get_molecules(tmp_item)))
        if option=='masses' and kwargs[option]==True:
            result.append([atom.element.mass for atom in tmp_item.topology.atoms])
        if option=='bonded_atoms' and kwargs[option]==True:
            from .api_mdtraj_Topology import get as _get
            result.append(_get(item.topology,bonded_atoms=True))
        if option=='bonds' and kwargs[option]==True:
            from .api_mdtraj_Topology import get as _get
            result.append(_get(item.topology,bonds=True))
        if option=='graph' and kwargs[option]==True:
            from .api_mdtraj_Topology import get as _get
            result.append(_get(item.topology,graph=True))
        if option=='molecules' and kwargs[option]==True:
            from .api_mdtraj_Topology import get as _get
            result.append(_get(item.topology,molecules=True))
        if option=='molecule_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='residue_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='atom_type' and kwargs[option]==True:
            raise NotImplementedError


    del(tmp_item)

    if len(result)==1:
        return result[0]
    else:
        return result

def select_with_mdtraj(item, selection):

    return item.topology.select(selection)

def extract_atoms_list(item, atoms_list):

    return item.atom_slice(atoms_list)

def merge_two_items(item1, item2, in_place=False):

    tmp_item = item1.stack(item2)
    if in_place:
        item1 = tmp_item
        pass
    else:
        return tmp_item

