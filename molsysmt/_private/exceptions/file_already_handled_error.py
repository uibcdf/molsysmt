from smonitor.integrations import emit_from_catalog
from molsysmt._private.smonitor import CATALOG, PACKAGE_ROOT, with_meta

class FileAlreadyHandledError(Exception):

    def __init__(self, filename):

        full_message = f"The file {filename} is already handled by MolSysMT."

        try:
            emit_from_catalog(
                CATALOG["exceptions"]["FileAlreadyHandledError"],
                package_root=PACKAGE_ROOT,
                extra=with_meta({"filename": filename}),
            )
        except Exception:
            pass

        super().__init__(full_message)
