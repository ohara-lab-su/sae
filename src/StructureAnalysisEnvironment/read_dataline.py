"""Historical line-reader interface, with text/gzip and pathlib support."""
from sae._text import read_text


def read_dataline(name):
    lines = read_text(name).splitlines()
    # Old parsers sometimes look one line ahead. Keep the terminal sentinel,
    # while counting the final physical line even without a trailing newline.
    return lines + [''], len(lines)


def read_dataline1(name):
    lines = [line for line in read_text(name).splitlines()
             if not line.lstrip().startswith(('#', '!'))]
    return lines, len(lines)
