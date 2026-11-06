"""Translate declared-adapter load failures at the host diagnostic boundary."""

from depdigest import DeclaredRegistry

from molsysmt._private.smonitor import MolecularSystemVerificationError


class _FormRegistry(DeclaredRegistry):
    """Reuse provider ownership while distinguishing load failure from absence."""

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError as error:
            cause = error.__cause__
            if cause is None:
                raise
            raise MolecularSystemVerificationError(
                forms=[key],
                reason=(
                    f"Could not load declared form adapter {key!r}: "
                    f"{type(cause).__name__}: {cause}"
                ),
                caller="molsysmt.form",
            ) from error
