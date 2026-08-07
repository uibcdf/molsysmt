from molsysmt._private.argdigest import arg_digest

@arg_digest()
def is_topological_attribute(attribute, skip_digestion=False):

    from . import attributes

    return attributes[attribute]['topological'] or (
        attributes[attribute]['chemical_state']
        and not attributes[attribute]['structural']
    )
