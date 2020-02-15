"""A method to interact with the Philips Hue UPnP Service."""
import json
import logging
from http.client import HTTPSConnection


logger = logging.getLogger('phue')


def find_bridge_address(self):
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
    return str(data[0]['internalipaddress'])


# explicitly define the outward facing API of this module
__all__ = [find_bridge_address.__name__]
