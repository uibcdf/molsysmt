PROFILE = "user"

SMONITOR = {
    "level": "WARNING",
    "trace_depth": 3,
    "capture_warnings": True,
    "capture_logging": True,
    "theme": "plain",
    "silence": ["pint", "networkx", "matplotlib", "astropy"],
}

PROFILES = {
    "user": {
        "level": "WARNING",
    },
    "dev": {
        "level": "INFO",
        "show_traceback": True,
    },
    "qa": {
        "level": "INFO",
        "show_traceback": True,
    },
    "agent": {
        "level": "WARNING",
    },
    "debug": {
        "level": "DEBUG",
        "show_traceback": True,
    },
}

# Keep catalog exports after the local configuration declarations.
from molsysmt._private.smonitor.catalog import CODES as CODES  # noqa: E402
from molsysmt._private.smonitor.catalog import SIGNALS as SIGNALS  # noqa: E402
