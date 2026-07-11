from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='MDAnalysis.AtomGroup')
def has_attribute(item, attribute, include_none=False, skip_digestion=False):

    from molsysmt.basic import has_attribute as msm_has_attribute
    return msm_has_attribute(item.universe, attribute, include_none=include_none, skip_digestion=True)
