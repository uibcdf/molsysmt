"""
ArgDigest configuration for MolSysMT.
"""

DIGESTION_SOURCE = "molsysmt._private.argdigest.argument"
DIGESTION_STYLE = "package"
STRICTNESS = "warn"
SKIP_PARAM = "skip_digestion"

# Axis 1: the function argument contract. A closed signature is held to its own
# parameters; a function with **kwargs declares its domain in FUNCTION_SOURCE.
NORMALIZATION_SOURCE = "molsysmt._private.argdigest.normalization"
FUNCTION_SOURCE = "molsysmt._private.argdigest.function"
DOMAIN_SOURCE = "molsysmt._private.argdigest.domain"
UNKNOWN_ARGUMENT = "error"

# Standard Scientific Pipelines for MolSysMT
# These use the 'sci' kind registered in the argdigest core

PIPELINES = {
    "as_float64_array": ["sci.to_float64_array"],
    "as_int64_array": ["sci.to_int64_array"],
    "as_nm_float64_array": [{"rule": "sci.to_quantity_array", "params": {"unit": "nm", "dtype": "float64"}}],
}
