"""Validate integration controls; scientific arguments use native MolSysMT.

The facade forwards scientific arguments to their original public boundary,
without claiming trusted normalization or forcing skip_digestion=True. Missing
local value digesters are deliberate delegation, not missing scientific checks.
The setter reuses the native attribute-name domain before effect receiving.
The get/get_label **kwargs domains are delegated to those native callables:
their admissible names/aliases depend on the provider contract at call time.
"""

DIGESTION_SOURCE = "molsysviewer_molsysmt._private.argument"
DIGESTION_STYLE = "package"
STRICTNESS = "ignore"
SKIP_PARAM = "skip_digestion"
UNKNOWN_ARGUMENT = "error"
FUNCTION_SOURCE = "molsysviewer_molsysmt._private.function"
DOMAIN_SOURCE = "molsysmt._private.argdigest.domain"
