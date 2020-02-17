"""A group of hue lights tracked by the bridge."""
import logging
from .light import Light


logger = logging.getLogger('phue')


# TODO: can't access "reachable"
# TODO: can't access "uniqueid"
# TODO: can't access "modelid"
# TODO: can't access "manufacturername"
# TODO: can't access "productname"
# TODO: can't access "type"
# TODO: can't access "config"
# TODO: can't access "capabilities"


class Group(Light):
    """
    A group of hue lights tracked by the bridge.

    Example:

        >>> b = Bridge()
        >>> g1 = Group(b, 1)
        >>> g1.hue = 50000 # all lights in that group turn blue
        >>> g1.on = False # all will turn off

        >>> g2 = Group(b, 'Kitchen')  # you can also look up groups by name
        >>> # will raise a LookupError if the name doesn't match

    """

    def __init__(self, bridge, group_id):
        super().__init__(bridge, None)
        del self.light_id  # not relevant for a group
        try:
            self.group_id = int(group_id)
        except:
            name = group_id
            groups = bridge.get_group()
            for idnumber, info in groups.items():
                if info['name'] == name:
                    self.group_id = int(idnumber)
                    break
            else:
                raise LookupError("Could not find a group by that name.")

    # Wrapper functions for get/set through the bridge, adding support for
    # remembering the transitiontime parameter if the user has set it
    def _get(self, *args, **kwargs):
        return self.bridge.get_group(self.group_id, *args, **kwargs)

    def _set(self, *args, **kwargs):
        # let's get basic group functionality working first before adding
        # transition time...
        if self.transitiontime is not None:
            kwargs['transitiontime'] = self.transitiontime
            logger.debug("Setting with transitiontime = {0} ds = {1} s".format(self.transitiontime, float(self.transitiontime) / 10))

            if (args[0] == 'on' and args[1] is False) or (
                    kwargs.get('on', True) is False):
                self._reset_bri_after_on = True
        return self.bridge.set_group(self.group_id, *args, **kwargs)

    @property
    def name(self):
        '''Get or set the name of the light group [string]'''
        return self._get('name')

    @name.setter
    def name(self, value):
        old_name = self.name
        self._name = value
        logger.debug("Renaming light group from '{0}' to '{1}'".format(
            old_name, value))
        self._set('name', self._name)

    @property
    def lights(self):
        """ Return a list of all lights in this group"""
        # response = self.bridge.request('GET', '/api/{0}/groups/{1}'.format(self.bridge.username, self.group_id))
        # return [Light(self.bridge, int(l)) for l in response['lights']]
        return [Light(self.bridge, int(l)) for l in self._get('lights')]

    @lights.setter
    def lights(self, value):
        """ Change the lights that are in this group"""
        logger.debug("Setting lights in group {0} to {1}".format(
            self.group_id, str(value)))
        self._set('lights', value)


# explicitly define the outward facing API of this module
__all__ = [Group.__name__]
