# Copyright Kengo NAKADA; SAE class library.
def require(value, component):
    if value is None:
        raise RuntimeError("Load or prepare the {} component first".format(component))
    return value
