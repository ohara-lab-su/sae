"""Standard-library logging for migrated readers."""

import logging


def XLogger(log_level="warning", **kwargs):
    # Do not configure root handlers, create files, or change application levels.
    return logging.getLogger("sae")


def debug_values(*values, **kwargs):
    """Historical diagnostic values go through the application logging policy."""
    logging.getLogger("sae").debug(kwargs.get("sep", " ").join(str(v) for v in values))
