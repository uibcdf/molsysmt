"""
ArgDigest adapter for MolSysMT.
This module replaces the legacy digestion engine with the standardized ArgDigest framework.
"""

from argdigest import arg_digest as _argdigest_digest

def arg_digest(*args, **kwargs):

    """

    MolSysMT argument digestion decorator.

    Delegates to the external ArgDigest library using the project-specific configuration.

    """

    # Use the MolSysMT configuration file created in Step 2.

    return _argdigest_digest(config="molsysmt._argdigest", *args, **kwargs)
