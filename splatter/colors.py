        # https://developers.meethue.com/develop/application-design-guidance/color-conversion-formulas-rgb-to-xy-and-back/


def xy_brightness_to_rgb(self):
    """Convert an XY-Brightness color to RGB."""
    x, y = self.xy
    z = 1.0 - x - y
    # calculate the XYZ values
    Y = self.brightness / 255.0
    X = (Y / y) * x
    Z = (Y / y) * z
    # calculate the RGB values using RGB D65 conversion
    r =  X * 1.656492 - Y * 0.354851 - Z * 0.255038
    g = -X * 0.707196 + Y * 1.655397 + Z * 0.036152
    b =  X * 0.051713 - Y * 0.121364 + Z * 1.011530

    import math

    if r <= 0.0031308:
        r *= 12.92
    else:
        (1.0 + 0.055) * pow(r, (1.0 / 2.4)) - 0.055
    if g <= 0.0031308:
        g *= 12.92
    else:
        (1.0 + 0.055) * pow(g, (1.0 / 2.4)) - 0.055
    if b <= 0.0031308:
        b *= 12.92
    else:
        (1.0 + 0.055) * pow(b, (1.0 / 2.4)) - 0.055

    r = min(255, max(0, r * 255))
    g = min(255, max(0, g * 255))
    b = min(255, max(0, b * 255))

    return r, g, b
