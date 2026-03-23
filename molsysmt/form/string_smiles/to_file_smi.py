from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import ArgumentError

@arg_digest(form='string:smiles')
def to_file_smi(item, output_filename=None, name=None, skip_digestion=False):

    if output_filename is None:
        raise ArgumentError(argument='output_filename', caller='molsysmt.form.string_smiles.to_file_smi',
                            message='output_filename is required to write a file:smi.')

    smiles = item[len('smiles:'):] if item.startswith('smiles:') else item

    line = smiles if name is None else f"{smiles} {name}"

    with open(output_filename, 'w') as fff:
        fff.write(line + '\n')

    return output_filename
