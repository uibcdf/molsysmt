def concatenate_frames(item, step=None, time=None, coordinates=None, box=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Topology import is_molsymst_Topology
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_Topology(item):
            raise ItemWithWrongForm('molsysmt.Topology')

    raise NotImplementedError

