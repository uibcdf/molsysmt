"""The view update switch is independent of native scientific mutation."""

from molsysmt._private.argdigest.argument.in_place import digest_in_place


def digest_update_view(update_view, caller=None):
    return digest_in_place(update_view, caller=caller)
