"""Exceptions raised by library operations; readers never terminate Python."""


class SAEError(Exception):
    """Base error for SAE."""


class ParseError(SAEError, ValueError):
    """Input is malformed or uses an unsupported representation."""


def legacy_error(message=None):
    """Translate historical reader aborts to catchable library exceptions."""
    raise ParseError(str(message) if message is not None else "Reader failed")
