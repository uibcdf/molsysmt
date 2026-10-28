"""Evaluate built-in and user role rules in their explicitly owned languages."""


def select_role_atoms(
    molecular_system,
    selection,
    syntax,
    inclusion_rules,
    exclusion_rules,
    default_inclusion,
    default_exclusion,
):
    from molsysmt.basic import select

    mask = select(molecular_system, selection=selection, syntax=syntax)
    output = set()
    for rules, language in ((inclusion_rules, syntax), (default_inclusion, "MolSysMT")):
        for rule in rules:
            output.update(
                select(molecular_system, selection=rule, mask=mask, syntax=language)
            )
    for rules, language in ((exclusion_rules, syntax), (default_exclusion, "MolSysMT")):
        for rule in rules:
            output.difference_update(
                select(molecular_system, selection=rule, mask=mask, syntax=language)
            )
    return output
