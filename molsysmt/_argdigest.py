"""
ArgDigest configuration for MolSysMT.
"""

DIGESTION_SOURCE = "molsysmt._private.arg_digestion.argument"
DIGESTION_STYLE = "package"
STANDARDIZER = "molsysmt._private.arg_digestion.argument_names_standardization:argument_names_standardization"
STRICTNESS = "warn"
SKIP_PARAM = "skip_digestion"