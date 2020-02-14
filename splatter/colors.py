"""Methods for converting color spaces for hue devices.

Reference: https://developers.meethue.com/develop/application-design-guidance/color-conversion-formulas-rgb-to-xy-and-back/

"""


def correct_xyz2rgb_gamma(channel):
    """
    Correct the gamma of a channel during an XYZ to sRGB conversion.

    Args:
        channel: the channel to correct the gamma of

    Returns:
        the channel after correcting the gamma

    """
    # apply the correction
    if channel <= 0.0031308:
        channel = channel * 12.92
    else:
        channel = (1.0 + 0.055) * pow(channel, (1.0 / 2.4)) - 0.055
    # normalize channel as int in [0, 255]
    return min(255, max(0, int(channel * 255)))


def xy_bri_to_rgb(x, y, brightness):
    """
    Convert an XY-Brightness color to RGB.

    Args:
        x: the x value of the color [0.0, 1.0]
        y: the y value of the color [0.0, 1.0]
        brightness: the brightness value of the color [0, 254]

    Returns:
        an RGB tuple

    """
    z = 1.0 - x - y
    # calculate the XYZ values
    Y = brightness / 255.0
    X = (Y / y) * x
    Z = (Y / y) * z
    # Wide gamut conversion D65
    r =  X * 1.656492 - Y * 0.354851 - Z * 0.255038
    g = -X * 0.707196 + Y * 1.655397 + Z * 0.036152
    b =  X * 0.051713 - Y * 0.121364 + Z * 1.011530
    # correct gamma
    return tuple(map(correct_xyz2rgb_gamma, (r, g, b)))


def correct_rgb2xyz_gamma(channel):
    """
    Correct the gamma of a channel during an XYZ to sRGB conversion.

    Args:
        channel: the channel to correct the gamma of

    Returns:
        the channel after correcting the gamma

    """
    # normalize channel in [0, 1]
    channel /= 255
    # apply the correction
    if channel > 0.04045:
        channel = pow((channel + 0.055) / (1.0 + 0.055), 2.4)
    else:
        channel = channel / 12.92
    return channel


def rgb_to_xy_bri(rgb):
    """
    Convert a color from RGB color space to x,y Brightness for Philips hue.

    Args:
        rgb: an RGB tuple

    Returns:
        a tuple of
        - the x,y values
        - the brightness

    """
    r, g, b = tuple(map(correct_rgb2xyz_gamma, rgb))
    # Wide gamut conversion D65
    X = r * 0.664511 + g * 0.154324 + b * 0.162028
    Y = r * 0.283881 + g * 0.668433 + b * 0.047685
    Z = r * 0.000088 + g * 0.072310 + b * 0.986039

    cx = X / (X + Y + Z)
    cy = Y / (X + Y + Z)

    return (cx, cy), min(255, max(0, int(Y * 255.0)))
