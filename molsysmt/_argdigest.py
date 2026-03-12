"""
ArgDigest configuration for MolSysMT.
"""

DIGESTION_SOURCE = "molsysmt._private.arg_digestion.argument"
DIGESTION_STYLE = "package"
STANDARDIZER = "molsysmt._private.arg_digestion.argument_names_standardization:argument_names_standardization"
STRICTNESS = "warn"
SKIP_PARAM = "skip_digestion"

# Standard Scientific Pipelines for MolSysMT
# These use the 'sci' kind registered in the argdigest core

PIPELINES = {
    "as_float64_array": ["sci.to_float64_array"],
    "as_int64_array": ["sci.to_int64_array"],
    "as_nm_float64_array": [{"rule": "sci.to_quantity_array", "params": {"unit": "nm", "dtype": "float64"}}],
}
