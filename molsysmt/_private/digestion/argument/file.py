from ...exceptions import ArgumentError

def digest_file(file, caller=None):

    if caller.endswith('write_topology_in_h5msm'):

        from h5py._hl.files import File as h5py_File
        from molsysmt.native import H5MSMFileHandler

        if isinstance(file, h5py_File):
            if 'type' in file.attrs:
                return file

        elif isinstance(file, H5MSMFileHandler):
                return file

        else:

            from molsysmt.form.file_h5msm.is_form import is_form as is_file_h5msm_form
            file_is_h5msm = is_file_h5msm_form(file)
            if file_is_h5msm:
                return file


    raise ArgumentError('file', value=file, caller=caller, message=None)

