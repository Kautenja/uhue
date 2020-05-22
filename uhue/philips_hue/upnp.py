"""A method to interact with the Philips Hue UPnP Service."""
import json
from .logger import logger
from http.client import HTTPSConnection


# the URL for the UPnP service
_URL = 'discovery.meethue.com'


def request_UPnP():
    """Return a list of bridges found using the UPnP service."""
    logger.info('Connecting to "%s"' % _URL)
    # open a secure connection to the Philips Hue web server
    connection = HTTPSConnection(_URL)
    # send a GET request to the UPnP service
    connection.request('GET', '/')
    # load the result of the UPnP GET request
    response = connection.getresponse()
    response_text = str(response.read(), encoding='utf-8')
    logger.info('meethue.com/api/nupnp returned "%s"' % response_text)
    # parse the JSON into a list of objects
    bridges = json.loads(response_text)
    # close connection
    connection.close()

    return bridges


def find_bridge():
    """Get the bridge IP address from the meethue.com UPnP service."""
    # TODO: support for handling multiple bridges?
    bridge = request_UPnP()[0]
    # get the ID and IP address from the JSON packet
    id_ = str(bridge['id'])
    address = str(bridge['internalipaddress'])
    logger.info('bridge with ID "%s" and IP address "%s"' % (id_, address))

    return address if address != '' else None


# explicitly define the outward facing API of this module
__all__ = [
    request_UPnP.__name__,
    find_bridge.__name__,
]
