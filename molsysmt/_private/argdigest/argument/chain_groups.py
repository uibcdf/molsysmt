from molsysmt._private.smonitor import ArgumentError


def digest_chain_groups(chain_groups, caller=None):
    if chain_groups is None or isinstance(chain_groups, (list, tuple)):
        return chain_groups
    raise ArgumentError("chain_groups", value=chain_groups, caller=caller)
