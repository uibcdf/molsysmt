from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.files_and_directories import temp_filename
from os import remove
from os.path import exists

@arg_digest(form='string:pdb_id')
def to_mmcif_PdbxContainers_DataContainer(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from .to_file_bcif_gz import to_file_bcif_gz
    from .to_file_bcif import to_file_bcif
    from .to_file_cif_gz import to_file_cif_gz
    from .to_file_cif import to_file_cif
    from molsysmt.form.file_bcif_gz.to_mmcif_PdbxContainers_DataContainer import to_mmcif_PdbxContainers_DataContainer as file_bcif_gz_to_mmcif_PdbxContainers_DataContainer
    from molsysmt.form.file_bcif.to_mmcif_PdbxContainers_DataContainer import to_mmcif_PdbxContainers_DataContainer as file_bcif_to_mmcif_PdbxContainers_DataContainer
    from molsysmt.form.file_cif_gz.to_mmcif_PdbxContainers_DataContainer import to_mmcif_PdbxContainers_DataContainer as file_cif_gz_to_mmcif_PdbxContainers_DataContainer
    from molsysmt.form.file_cif.to_mmcif_PdbxContainers_DataContainer import to_mmcif_PdbxContainers_DataContainer as file_cif_to_mmcif_PdbxContainers_DataContainer

    strategies = [
        ("bcif.gz", "bcif.gz", to_file_bcif_gz, file_bcif_gz_to_mmcif_PdbxContainers_DataContainer),
        ("bcif", "bcif", to_file_bcif, file_bcif_to_mmcif_PdbxContainers_DataContainer),
        ("cif.gz", "cif.gz", to_file_cif_gz, file_cif_gz_to_mmcif_PdbxContainers_DataContainer),
        ("cif", "cif", to_file_cif, file_cif_to_mmcif_PdbxContainers_DataContainer),
    ]

    errors = []

    for format_name, extension, downloader, converter in strategies:
        output_filename = temp_filename(extension=extension)
        try:
            tmp_item = downloader(item, output_filename=output_filename, skip_digestion=True)
            return converter(tmp_item, skip_digestion=True)
        except Exception as exc:
            errors.append((format_name, exc))
        finally:
            if exists(output_filename):
                remove(output_filename)

    details = "; ".join(
        f"{format_name}: {type(exc).__name__}: {exc}" for format_name, exc in errors
    )
    raise RuntimeError(
        f"Unable to convert PDB ID '{item}' to mmcif.PdbxContainers.DataContainer. "
        f"Attempted formats: bcif.gz, bcif, cif.gz, cif. Causes: {details}"
    ) from errors[-1][1]
