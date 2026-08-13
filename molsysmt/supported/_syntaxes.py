syntax_capabilities = {
    'MolSysMT': {
        'select': True,
        'to_syntax': False,
        'scope': 'Any supported molecular-system form',
    },
    'MDTraj': {
        'select': True,
        'to_syntax': True,
        'scope': 'Any input convertible to mdtraj.Topology',
    },
    'MDAnalysis': {
        'select': True,
        'to_syntax': False,
        'scope': 'Inputs convertible to MDAnalysis.Universe',
    },
    'NGLView': {
        'select': False,
        'to_syntax': True,
        'scope': 'Atom, group, and chain translations',
    },
}

selection_syntaxes = tuple(
    name for name, capabilities in syntax_capabilities.items()
    if capabilities['select']
)
translation_syntaxes = tuple(
    name for name, capabilities in syntax_capabilities.items()
    if capabilities['to_syntax']
)

# Backward-compatible introspection union. Direction-specific validation uses the two
# collections above so accepting a syntax never promises an unavailable direction.
syntaxes = tuple(syntax_capabilities)
lowercase_syntaxes = {name.lower(): name for name in syntaxes}
lowercase_selection_syntaxes = {name.lower(): name for name in selection_syntaxes}
lowercase_translation_syntaxes = {name.lower(): name for name in translation_syntaxes}
