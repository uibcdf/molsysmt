import logging
import warnings
from pathlib import Path
from typing import IO


def _parse_level(level: int | str) -> int:
    if isinstance(level, int):
        return level
    return logging._nameToLevel.get(str(level).upper(), logging.WARNING)


def setup_logging(
    level: int | str = "WARNING",
    *,
    stream: IO | None = None,
    capture_warnings: bool = True,
    simplify_warning_format: bool = True,
    logger_name: str = "molsysmt",
) -> logging.Logger:
    """
    Configure MolSysMT logging and (optionally) capture Python warnings.

    Effects
    -------
    - Creates/gets logger `logger_name` (default: "molsysmt")
    - Attaches a StreamHandler if not present, with formatter:
          "MOLSYSMT %(levelname)s [%(name)s] | %(message)s"
    - If capture_warnings is True:
        - logging.captureWarnings(True)
        - The "py.warnings" logger reuses the same handler/formatter
        - If simplify_warning_format is True:
            warnings.formatwarning(message, category, filename, lineno, line=None)
            -> "CategoryName (filename:lineno): message\\n"
          (includes origin so callers can trace the warning source)
    """
    lvl = _parse_level(level)

    # Main package logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(lvl)
    logger.propagate = False

    # Ensure a single stream handler with the desired formatter
    stream_handler = None
    for h in logger.handlers:
        if isinstance(h, logging.StreamHandler):
            stream_handler = h
            break

    if stream_handler is None:
        stream_handler = logging.StreamHandler(stream)  # None -> sys.stderr
        # EXACT desired format for warnings:
        # "MOLSYSMT WARNING | <Category>: <message>"
        # (For normal logs, <Category> won't appear, but the prefix still matches.)
        formatter = logging.Formatter("MOLSYSMT %(levelname)s [%(name)s] | %(message)s")
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    # Capture Python warnings and route to logging via "py.warnings"
    if capture_warnings:
        # Simplify the warning text so it contains the category, origin file, and originating package hint
        if simplify_warning_format:
            def _simple_formatwarning(message, category, filename, lineno, line=None):
                fname = Path(filename).name if filename else ""
                location = f" ({fname}:{lineno})" if fname else ""
                module_hint = ""
                if filename:
                    parts = Path(filename).parts
                    if "site-packages" in parts:
                        idx = parts.index("site-packages")
                        if idx + 1 < len(parts):
                            module_hint = parts[idx + 1]
                    elif "dist-packages" in parts:
                        idx = parts.index("dist-packages")
                        if idx + 1 < len(parts):
                            module_hint = parts[idx + 1]
                    else:
                        module_hint = Path(filename).stem
                    module_hint = f" [{module_hint}]" if module_hint else ""
                return f"{category.__name__}{module_hint}{location}: {message}\n"
            warnings.formatwarning = _simple_formatwarning

        logging.captureWarnings(True)

        pyw = logging.getLogger("py.warnings")
        pyw.setLevel(lvl)
        pyw.handlers.clear()       # avoid duplicate handlers
        pyw.addHandler(stream_handler)
        pyw.propagate = False

    return logger
