
def to_file_pdb(item, atom_indices='all', coordinates=None, box=None, output_filename=None, syntaxis='MolSysMT'):

    from io import StringIO
    from openmm.app import PDBFile
    from molsysmt import __version__ as msm_version
    from openmm import Platform # the openmm version is taken from this module (see: openmm/app/pdbfile.py)

    tmp_io = StringIO()
    PDBFile.writeFile(item.topology, item.positions, tmp_io, keepIds=True)
    filedata = tmp_io.getvalue()
    openmm_version = Platform.getOpenMMVersion()
    filedata = filedata.replace('WITH OPENMM '+openmm_version, 'WITH OPENMM '+openmm_version+' BY MOLSYSMT '+msm_version)
    tmp_io.close()
    del(tmp_io)

    with open(output_filename, 'w') as file:
        file.write(filedata)
    tmp_item = output_filename

    return tmp_item

