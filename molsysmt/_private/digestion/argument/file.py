from ...exceptions import ArgumentError

def digest_file(file, caller=None):

    if caller.endswith('write_topology_in_msmh5'):

        from h5py._hl.files import File as h5py_File
        from molsysmt.native import MSMH5FileHandler

        if isinstance(file, h5py_File):
            if 'type' in file.attrs:
                return file

        elif isinstance(file, MSMH5FileHandler):
                return file

        else:

            from molsysmt.form.file_msmh5.is_form import is_form as is_file_msmh5_form
            file_is_msmh5 = is_file_msmh5_form(file)
            if file_is_msmh5:
                return file


    raise ArgumentError('file', value=file, caller=caller, message=None)

