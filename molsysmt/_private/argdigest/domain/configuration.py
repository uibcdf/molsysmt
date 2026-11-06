"""Admit only the owning module's public configuration data."""

from argdigest import Domain


def _names():
    # Discovery can run while configure itself is being initialized.
    from molsysmt.configure import _configuration_names

    return _configuration_names()


domain = Domain(
    name="configuration",
    contains=lambda name: name in _names(),
    members=_names,
    description="Existing public MolSysMT configuration data, excluding modules and callables.",
)
