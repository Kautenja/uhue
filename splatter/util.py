"""Utility functions used by the application layer."""


def hex_to_rgb(value: str) -> tuple:
    """Convert a hexadecimal string to an RGB tuple."""
    hlen = len(value)
    step = hlen // 3
    return tuple(int(value[i : i + step], 16) for i in range(0, hlen, step))


# explicitly define the outward facing API of this module
__all__ = [hex_to_rgb.__name__]
