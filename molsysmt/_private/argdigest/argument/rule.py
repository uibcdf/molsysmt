from molsysmt._private.smonitor import ArgumentError


def digest_rule(rule, caller=None):

    if caller in {
        "molsysmt.basic.compare.compare",
        "molsysmt.native.topology.compare",
    }:
        if rule in ["equal", "in"]:
            return rule

    raise ArgumentError("rule", value=rule, caller=caller, message=None)
