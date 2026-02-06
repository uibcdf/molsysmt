from molsysmt._private.smonitor import CATALOG
from ._emit import message_from_catalog

class FileAlreadyHandledError(Exception):

    def __init__(self, filename=None):
        safe_filename = filename or "<unknown>"
        default_message = f"The file {safe_filename} is already handled by MolSysMT."

        full_message = message_from_catalog(
            CATALOG["exceptions"]["FileAlreadyHandledError"],
            extra={"filename": safe_filename},
            default_message=default_message,
        )

        super().__init__(full_message)
