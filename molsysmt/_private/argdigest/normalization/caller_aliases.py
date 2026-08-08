"""Aliases that belong to one function only.

These were `elif caller == ...` branches in the standardizer. Declared here they are
readable as a list, and `describe_normalization` can report them for a function's own
documentation instead of leaving them buried in a branch.
"""

from argdigest import AliasTable

TABLES = [
    AliasTable(
        applies_to='molsysmt.build.mutate.mutate',
        aliases={'mutation': 'mutations'},
        description='a single mutation reads naturally in the singular',
    ),
    AliasTable(
        applies_to='molsysmt.basic.compare.compare',
        aliases={'attributes_type': 'attribute_type'},
        description='backward-compatible alias kept in tests and user scripts',
    ),
]
