"""A method to interact with the Philips Hue UPnP Service."""
import json
from .logger import logger
from http.client import HTTPSConnection


def find_bridge():
    """Get the bridge IP address from the meethue.com UPnP service."""
    # open a secure connection to the Philips Hue web server
    connection = HTTPSConnection('www.meethue.com')
    # send a GET request to the UPnP service
    connection.request('GET', '/api/nupnp')
    logger.info('Connecting to meethue.com/api/nupnp')
    # parse the JSON data from the request
    result = connection.getresponse()
    data = json.loads(str(result.read(), encoding='utf-8'))
    # close connection after read() is done, to prevent issues with read()
    connection.close()
    ip_address = str(data[0]['internalipaddress'])
    return ip_address if ip_address != '' else None


# explicitly define the outward facing API of this module
__all__ = [find_bridge.__name__]
