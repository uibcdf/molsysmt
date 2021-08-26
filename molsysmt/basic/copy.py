
def copy(molecular_system, output_filename=None):

    from molsysmt.basic import convert

    return convert(molecular_system, selection='all', frame_indices='all', to_form=output_filename)

