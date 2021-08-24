from molsysmt.basic.convert import convert

def copy(molecular_system, output_filename=None):

    return convert(molecular_system, selection='all', frame_indices='all', to_form=output_filename)

