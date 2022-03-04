def add(to_item, item, check=True):

    if check:
        from molsysmt.tools.molsysmt_Topology.is_molsysmt_Topology import _checking_form
        _checking_form(to_item, check=check)
        _checking_form(item, check=check)

    raise NotImplementedError

