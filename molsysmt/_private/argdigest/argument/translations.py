import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError

from .translation import digest_translation


def digest_translations(translations, caller=None):

    if caller is not None:
        if caller.endswith("digest_bioassembly"):
            if puw.is_quantity(translations):
                if len(translations.shape) != 2 or translations.shape[1] != 3:
                    raise ArgumentError(
                        "translations",
                        value=translations,
                        caller=caller,
                        message="Assembly translations must have shape (n_operations, 3).",
                    )
                translations = [
                    translations[index] for index in range(len(translations))
                ]
            if isinstance(translations, (np.ndarray, list, tuple)):
                vectors = []
                for translation in translations:
                    vector = digest_translation(translation, caller=caller)
                    if vector.shape != (1, 1, 3):
                        raise ArgumentError(
                            "translations",
                            value=translations,
                            caller=caller,
                            message="Each assembly operation requires exactly one translation vector.",
                        )
                    vectors.append(puw.get_value(vector, to_unit="nm")[0, 0])
                values = np.asarray(vectors, dtype=np.float64).reshape(-1, 3)
                if not np.all(np.isfinite(values)):
                    raise ArgumentError(
                        "translations",
                        value=translations,
                        caller=caller,
                        message="Assembly translations must contain only finite values.",
                    )
                return puw.standardize(puw.quantity(values, "nm"))

    raise ArgumentError("translations", value=translations, caller=caller, message=None)
