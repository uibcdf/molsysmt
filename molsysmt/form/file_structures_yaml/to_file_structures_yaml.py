from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest


@dep_digest('yaml')
@arg_digest(form='file:structures_yaml')
def to_file_structures_yaml(item, output_filename, skip_digestion=False):
    """Returning the same YAML structures file path."""
    return output_filename if item == output_filename else item
