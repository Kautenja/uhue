"""An interface to the Hue ZigBee bridge."""
import os
import json
import logging
import platform
import socket
from http.client import HTTPConnection
from .exceptions import PhueException, PhueRegistrationException, PhueRequestTimeout
from .group import Group
from .light import Light
from .scene import Scene
from .sensor import Sensor


logger = logging.getLogger('phue')


# the default name for the configuration file
CONFIG_FILE_NAME = '.python_hue'


def unwrap_config_file_path(config_file_path: str = None):
    """
    Unwrap the path to the configuration file.

    Args:
        config_file_path: the path to the configuration file

    Returns:
        a formatted path to the configuration file

    """
    # get the user home directory
    user_home = 'USERPROFILE' if platform.system() == 'Windows' else 'HOME'
    # user specified configuration file
    if config_file_path is not None:
        return config_file_path
    # write access to user home
    if os.getenv(user_home) is not None and os.access(os.getenv(user_home), os.W_OK):
        return os.path.join(os.getenv(user_home), CONFIG_FILE_NAME)
    # iOS platform
    if 'iPad' in platform.machine() or 'iPhone' in platform.machine():
        return os.path.join(os.getenv(user_home), 'Documents', CONFIG_FILE_NAME)
    # use current working directory
    return os.path.join(os.getcwd(), CONFIG_FILE_NAME)


class Bridge:
    """
    An interface to the Hue ZigBee bridge.

    You can obtain Light objects by calling the get_light_objects method:

        >>> b = Bridge(ip='192.168.1.100')
        >>> b.get_light_objects()
        [<phue.Light at 0x10473d750>,
         <phue.Light at 0x1046ce110>]

    Or more succinctly just by accessing this Bridge object as a list or dict:

        >>> b[1]
        <phue.Light at 0x10473d750>
        >>> b['Kitchen']
        <phue.Light at 0x10473d750>

    """

    def __init__(self,
        ip_address: str = None,
        username: str = None,
        config_file_path: str = None
    ) -> None:
        """
        Initialize a connection to a Hue bridge.

        Args:
            ip_address: string IP address as dotted quad
            username: string, the username for the bridge
            config_file_path: string, the path to the configuration file

        Returns:
            None

        """
        self.ip_address = ip_address
        self.username = username
        self.config_file_path = unwrap_config_file_path(config_file_path)
        # setup structure for light objects
        self.lights_by_id = dict()
        self.lights_by_name = dict()
        # setup structures for sensor objects
        self.sensors_by_id = dict()
        self.sensors_by_name = dict()
        # setup structures for group objects
        self.groups_by_id = dict()
        self.groups_by_name = dict()

        # setup local data containers
        self._name = None

    def __getitem__(self, key):
        """ Lights are accessibly by indexing the bridge either with
        an integer index or string name. """
        if self.lights_by_id == {}:
            self.get_light_objects()

        try:
            return self.lights_by_id[key]
        except:
            try:
                return self.lights_by_name[key]
            except:
                raise KeyError(f'Not a valid key (integer index starting with 1, or light name): {key}')

    @property
    def can_login(self) -> bool:
        """Return true if connected to the bridge."""
        return self.ip_address is not None and self.username is not None

    @property
    def has_config_file(self) -> bool:
        """Return True if the configuration file exists."""
        return os.path.exists(self.config_file_path)

    def register(self) -> None:
        """Register this computer with the Hue bridge hardware."""
        if self.ip_address is None:  # IP address is required to send requests
            raise ValueError("you must set an IP address before attempting to register")
        # send the registration response to the server
        response = self.request('POST', '/api', {"devicetype": "python_hue"})
        for line in response:
            for key in line:
                if 'success' in key:
                    self.username = line['success']['username']
                    with open(self.config_file_path, 'w') as config_file:
                        logger.info('Writing configuration file to %s', self.config_file_path)
                        data = json.dumps({self.ip_address: line['success']})
                        config_file.write(data)
                if 'error' in key:
                    error_type = line['error']['type']
                    if error_type == 101:
                        raise PhueRegistrationException(error_type, 'The link button has not been pressed in the last 30 seconds.')
                    if error_type == 7:
                        raise PhueException(error_type, 'Unknown username')

    def load_config_file(self) -> None:
        """Connect to the Hue bridge."""
        logger.info('Loading bridge credentials from "%s"', self.config_file_path)
        # check for existence of the file
        if not self.has_config_file:
            raise RuntimeError("No configuration found. run register")
        # load the file into a JSON object
        with open(self.config_file_path, 'r') as config_file:
            config = json.loads(config_file.read())
        # setup the IP address
        self.ip_address = list(config.keys())[0]
        logger.info('Using ip from config: %s', self.ip_address)
        # setup the username
        self.username = config[self.ip_address]['username']
        logger.info('Using username from config: %s', self.username)

    def request(self,
        mode: str = 'GET',
        endpoint: str = None,
        data: dict = None,
        timeout: int = 10
    ) -> dict:
        """
        Perform an HTTP GET/PUT requests on the API.

        Args:
            mode: the HTTP mode to use (e.g., GET)
            endpoint: the address to send the message to
            data: the JSON data to send in the message
            timeout: the timeout for the request

        Returns:
            the response data as a dictionary

        """
        # create the HTTP connection
        connection = HTTPConnection(self.ip_address, timeout=timeout)
        # make the request using the given mode
        try:
            if mode in {'GET', 'DELETE'}:
                connection.request(mode, endpoint)
            if mode in {'PUT', 'POST'}:
                connection.request(mode, endpoint, json.dumps(data))
            logger.debug("%s %s %s", mode, endpoint, str(data))
        except socket.timeout:  # handle a socket timeout
            error = f"{mode} Request to {self.ip_address}{endpoint} timed out."
            logger.exception(error)
            raise PhueRequestTimeout(None, error)
        # parse the response data and close the connection
        result = connection.getresponse()
        response = result.read()
        connection.close()
        response = response.decode('utf-8')
        logger.debug(response)
        # parse the JSON data into a dictionary
        return json.loads(response)

    #
    # MARK: Bridge
    #

    @property
    def name(self) -> str:
        """Return the name of the bridge."""
        self._name = self.request('GET', f'/api/{self.username}/config')['name']
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the name of the bridge to a new value."""
        self._name = value
        data = {'name': self._name}
        self.request('PUT', f'/api/{self.username}/config', data)

    def get_api(self):
        """ Returns the full api dictionary """
        return self.request('GET', f'/api/{self.username}')

    #
    # MARK: Lights
    #

    def get_light_objects(self, mode: str = 'list') -> 'Union[list,dict]':
        """
        Return a collection containing the lights, either by name or id.

        Args:
            mode: the mode to use for returning the light data structure.
                  Use 'id', 'name', or 'list' as the mode

        Returns:
            the collections of lights as either:
            - a list, if in 'list' mode
            - a dict keyed by light ID (int) id in 'id' mode
            - a dict keyed by light name (str) id in 'name' mode

        """
        if not self.lights_by_id:  # the lights have not been loaded
            # load the lights from the API
            lights = self.request('GET', f'/api/{self.username}/lights/')
            for light in lights:  # iterate over the lights
                self.lights_by_id[int(light)] = Light(self, int(light))
                self.lights_by_name[lights[light]['name']] = self.lights_by_id[int(light)]
        # return the lights based on data structure
        if mode == 'id':
            return self.lights_by_id
        if mode == 'name':
            return self.lights_by_name
        if mode == 'list':
            # return lights in sorted id order, dicts have no natural order
            return [self.lights_by_id[id_] for id_ in sorted(self.lights_by_id)]

    @property
    def lights(self):
        """ Access lights as a list """
        return self.get_light_objects()

    def get_light(self, light_id=None, parameter=None):
        """ Gets state by light_id and parameter"""
        if isinstance(light_id, str):
            light_id = self.get_light_id_by_name(light_id)
        if light_id is None:
            return self.request('GET', f'/api/{self.username}/lights/')
        state = self.request(
            'GET', f'/api/{self.username}/lights/{light_id}')
        if parameter is None:
            return state
        if parameter in ['swupdate', 'type', 'name', 'modelid', 'manufacturername', 'productname', 'capabilities', 'config', 'uniqueid', 'swversion']:
            return state[parameter]
        try:
            return state['state'][parameter]
        except KeyError as e:
            raise KeyError(
                'Not a valid key, parameter %s is not associated with light %s)'
                % (parameter, light_id))

    def get_light_id_by_name(self, name: str):
        """ Lookup a light id based on string name. Case-sensitive. """
        lights = self.get_light()
        for light_id in lights:
            if name == lights[light_id]['name']:
                return light_id
        return False

    def set_light(self, light_id, parameter, value=None, transitiontime=None):
        """ Adjust properties of one or more lights.

        light_id can be a single lamp or an array of lamps
        parameters: 'on' : True|False , 'bri' : 0-254, 'sat' : 0-254, 'ct': 154-500

        transitiontime : in **deciseconds**, time for this transition to take place
                         Note that transitiontime only applies to *this* light
                         command, it is not saved as a setting for use in the future!
                         Use the Light class' transitiontime attribute if you want
                         persistent time settings.

        """
        if isinstance(parameter, dict):
            data = parameter
        else:
            data = {parameter: value}

        if transitiontime is not None:
            data['transitiontime'] = int(round(transitiontime))  # must be int for request format

        light_id_array = light_id
        if isinstance(light_id, int) or isinstance(light_id, str):
            light_id_array = [light_id]
        result = []
        for light in light_id_array:
            logger.debug(str(data))
            if parameter == 'name':
                result.append(self.request('PUT', f'/api/{self.username}/lights/{light_id}', data))
            else:
                if isinstance(light, str):
                    converted_light = self.get_light_id_by_name(light)
                else:
                    converted_light = light
                result.append(self.request('PUT', f'/api/{self.username}/lights/{converted_light}/state', data))
            if 'error' in list(result[-1][0].keys()):
                logger.warn("ERROR: {0} for light {1}".format(result[-1][0]['error']['description'], light))

        logger.debug(result)
        return result

    #
    # MARK: Groups
    #

    def create_group(self, name, lights=None):
        """ Create a group of lights

        Parameters
        ------------
        name : string
            Name for this group of lights
        lights : list
            List of lights to be in the group.

        """
        data = {'lights': [str(x) for x in lights], 'name': name}
        return self.request('POST', f'/api/{self.username}/groups/', data)

    def get_group_objects(self, mode: str = 'list') -> 'Union[list,dict]':
        """Returns a collection containing the groups, either by name or id (use 'id' or 'name' as the mode)
        The returned collection can be either a list (default), or a dict.
        Set mode='id' for a dict by sensor ID, or mode='name' for a dict by sensor name.   """
        if self.groups_by_id == {}:
            groups = self.request('GET', f'/api/{self.username}/groups/')
            for group in groups:
                self.groups_by_id[int(group)] = Group(self, int(group))
                self.groups_by_name[groups[group]['name']] = self.groups_by_id[int(group)]
        if mode == 'id':
            return self.groups_by_id
        if mode == 'name':
            return self.groups_by_name
        if mode == 'list':
            return self.groups_by_id.values()

    @property
    def groups(self):
        """ Access groups as a list """
        return [Group(self, int(groupid)) for groupid in self.get_group().keys()]

    def get_group(self, group_id=None, parameter=None):
        if isinstance(group_id, str):
            group_id = self.get_group_id_by_name(group_id)
        if group_id is False:
            logger.error('Group name does not exist')
            return
        if group_id is None:
            return self.request('GET', f'/api/{self.username}/groups/')
        if parameter is None:
            return self.request('GET', f'/api/{self.username}/groups/{group_id}')
        if parameter in {'name', 'lights'}:
            return self.request('GET', f'/api/{self.username}/groups/{group_id}')[parameter]
        return self.request('GET', f'/api/{self.username}/groups/{group_id}')['action'][parameter]

    def get_group_id_by_name(self, name):
        """ Lookup a group id based on string name. Case-sensitive. """
        groups = self.get_group()
        for group_id in groups:
            if name == groups[group_id]['name']:
                return int(group_id)
        return False

    def set_group(self, group_id, parameter, value=None, transitiontime=None):
        """ Change light settings for a group

        group_id : int, id number for group
        parameter : 'name' or 'lights'
        value: string, or list of light IDs if you're setting the lights

        """

        if isinstance(parameter, dict):
            data = parameter
        elif parameter == 'lights' and (isinstance(value, list) or isinstance(value, int)):
            if isinstance(value, int):
                value = [value]
            data = {parameter: [str(x) for x in value]}
        else:
            data = {parameter: value}

        if transitiontime is not None:
            data['transitiontime'] = int(round(
                transitiontime))  # must be int for request format

        group_id_array = group_id
        if isinstance(group_id, (int, str)):
            group_id_array = [group_id]
        result = []
        for group in group_id_array:
            logger.debug(str(data))
            if isinstance(group, str):
                converted_group = self.get_group_id_by_name(group)
            else:
                converted_group = group
            if converted_group is False:
                logger.error('Group name does not exist')
                return
            if parameter in {'name', 'lights'}:
                result.append(self.request('PUT', f'/api/{self.username}/groups/{converted_group}', data))
            else:
                result.append(self.request('PUT', f'/api/{self.username}/groups/{converted_group}/action', data))

        if 'error' in list(result[-1][0].keys()):
            logger.warn("ERROR: {0} for group {1}".format(
                result[-1][0]['error']['description'], group))

        logger.debug(result)
        return result

    def delete_group(self, group_id):
        return self.request('DELETE', f'/api/{self.username}/groups/{group_id}')

    #
    # MARK: Scenes
    #

    def get_scene(self):
        return self.request('GET', f'/api/{self.username}/scenes')

    @property
    def scenes(self):
        return [Scene(k, **v) for k, v in self.get_scene().items()]

    def delete_scene(self, scene_id):
        try:
            return self.request('DELETE', f'/api/{self.username}/scenes/{scene_id}')
        except:
            logger.debug("Unable to delete scene with ID {0}".format(scene_id))

    def activate_scene(self, group_id, scene_id, transition_time=4):
        return self.request('PUT', f'/api/{self.username}/groups/{group_id}/action', {
            "scene": scene_id,
            "transitiontime": transition_time
        })

    def run_scene(self, group_name, scene_name, transition_time=4):
        """Run a scene by group and scene name.

        As of 1.11 of the Hue API the scenes are accessable in the
        API. With the gen 2 of the official HUE app everything is
        organized by room groups.

        This provides a convenience way of activating scenes by group
        name and scene name. If we find exactly 1 group and 1 scene
        with the matching names, we run them.

        If we find more than one we run the first scene who has
        exactly the same lights defined as the group. This is far from
        perfect, but is convenient for setting lights symbolically (and
        can be improved later).

        :param transition_time: The duration of the transition from the
        light’s current state to the new state in a multiple of 100ms
        :returns True if a scene was run, False otherwise

        """
        groups = [x for x in self.groups if x.name == group_name]
        scenes = [x for x in self.scenes if x.name == scene_name]
        if len(groups) != 1:
            logger.warn("run_scene: More than 1 group found by name {}".format(group_name))
            return False
        group = groups[0]
        if len(scenes) == 0:
            logger.warn("run_scene: No scene found {}".format(scene_name))
            return False
        if len(scenes) == 1:
            self.activate_scene(group.group_id, scenes[0].scene_id, transition_time)
            return True
        # otherwise, lets figure out if one of the named scenes uses
        # all the lights of the group
        group_lights = sorted([x.light_id for x in group.lights])
        for scene in scenes:
            if group_lights == scene.lights:
                self.activate_scene(group.group_id, scene.scene_id, transition_time)
                return True
        logger.warn("run_scene: did not find a scene: {} "
                    "that shared lights with group {}".format(scene_name, group_name))
        return False

    #
    # MARK: Schedules
    #

    def create_schedule(self, name, time, light_id, data, description=' '):
        return self.request('POST', f'/api/{self.username}/schedules', {
            'name': name,
            'localtime': time,
            'description': description,
            'command': {
                'method': 'PUT',
                'address': f'/api/{self.username}/lights/{light_id}/state',
                'body': data
            }
        })

    def create_group_schedule(self, name, time, group_id, data, description=' '):
        return self.request('POST', f'/api/{self.username}/schedules', {
            'name': name,
            'localtime': time,
            'description': description,
            'command': {
                'method': 'PUT',
                'address': f'/api/{self.username}/groups/{group_id}/action',
                'body': data
            }
        })

    def get_schedule(self, schedule_id=None, parameter=None):
        if schedule_id is None:
            return self.request('GET', f'/api/{self.username}/schedules')
        if parameter is None:
            return self.request('GET', f'/api/{self.username}/schedules/{schedule_id}')

    def set_schedule_attributes(self, schedule_id, attributes):
        """
        :param schedule_id: The ID of the schedule
        :param attributes: Dictionary with attributes and their new values
        """
        return self.request('PUT', f'/api/{self.username}/schedules/{schedule_id}', data=attributes)

    def delete_schedule(self, schedule_id):
        return self.request('DELETE', f'/api/{self.username}/schedules/{schedule_id}')

    #
    # MARK: Sensors
    #

    def create_sensor(self, name, modelid, swversion, sensor_type, uniqueid, manufacturername, state={}, config={}, recycle=False):
        """ Create a new sensor in the bridge. Returns (ID,None) of the new sensor or (None,message) if creation failed. """
        data = {
            "name": name,
            "modelid": modelid,
            "swversion": swversion,
            "type": sensor_type,
            "uniqueid": uniqueid,
            "manufacturername": manufacturername,
            "recycle": recycle
        }
        if (isinstance(state, dict) and state != {}):
            data["state"] = state

        if (isinstance(config, dict) and config != {}):
            data["config"] = config

        result = self.request('POST', f'/api/{self.username}/sensors/', data)

        if ("success" in result[0].keys()):
            new_id = result[0]["success"]["id"]
            logger.debug(f"Created sensor with ID {new_id}")
            new_sensor = Sensor(self, int(new_id))
            self.sensors_by_id[new_id] = new_sensor
            self.sensors_by_name[name] = new_sensor
            return new_id, None
        else:
            logger.debug(f"Failed to create sensor: {repr(result[0])}")
            return None, result[0]

    def get_sensor_objects(self, mode: str = 'list') -> 'Union[list,dict]':
        """Returns a collection containing the sensors, either by name or id (use 'id' or 'name' as the mode)
        The returned collection can be either a list (default), or a dict.
        Set mode='id' for a dict by sensor ID, or mode='name' for a dict by sensor name.   """
        if self.sensors_by_id == {}:
            sensors = self.request('GET', f'/api/{self.username}/sensors/')
            for sensor in sensors:
                self.sensors_by_id[int(sensor)] = Sensor(self, int(sensor))
                self.sensors_by_name[sensors[sensor]['name']] = self.sensors_by_id[int(sensor)]
        if mode == 'id':
            return self.sensors_by_id
        if mode == 'name':
            return self.sensors_by_name
        if mode == 'list':
            return self.sensors_by_id.values()

    @property
    def sensors(self):
        """ Access sensors as a list """
        return self.get_sensor_objects()

    def get_sensor(self, sensor_id=None, parameter=None):
        """ Gets state by sensor_id and parameter"""
        if isinstance(sensor_id, str):
            sensor_id = self.get_sensor_id_by_name(sensor_id)
        if sensor_id is None:
            return self.request('GET', f'/api/{self.username}/sensors/')
        data = self.request('GET', f'/api/{self.username}/sensors/{sensor_id}')

        if isinstance(data, list):
            logger.debug("Unable to read sensor with ID {0}: {1}".format(sensor_id, repr(data)))
            return None

        if parameter is None:
            return data
        return data[parameter]

    def get_sensor_id_by_name(self, name):
        """ Lookup a sensor id based on string name. Case-sensitive. """
        sensors = self.get_sensor()
        for sensor_id in sensors:
            if name == sensors[sensor_id]['name']:
                return sensor_id
        return False

    def set_sensor(self, sensor_id, parameter, value=None):
        """ Adjust properties of a sensor

        sensor_id must be a single sensor.
        parameters: 'name' : string

        """
        if isinstance(parameter, dict):
            data = parameter
        else:
            data = {parameter: value}

        result = None
        logger.debug(str(data))
        result = self.request('PUT', f'/api/{self.username}/sensors/{sensor_id}', data)
        if 'error' in list(result[0].keys()):
            logger.warn("ERROR: {0} for sensor {1}".format(result[0]['error']['description'], sensor_id))

        logger.debug(result)
        return result

    def set_sensor_state(self, sensor_id, parameter, value=None):
        """ Adjust the "state" object of a sensor

        sensor_id must be a single sensor.
        parameters: any parameter(s) present in the sensor's "state" dictionary.

        """
        self.set_sensor_content(sensor_id, parameter, value, "state")

    def set_sensor_config(self, sensor_id, parameter, value=None):
        """ Adjust the "config" object of a sensor

        sensor_id must be a single sensor.
        parameters: any parameter(s) present in the sensor's "config" dictionary.

        """
        self.set_sensor_content(sensor_id, parameter, value, "config")

    def set_sensor_content(self, sensor_id, parameter, value=None, structure="state"):
        """ Adjust the "state" or "config" structures of a sensor
        """
        if (structure != "state" and structure != "config"):
            logger.debug("set_sensor_current expects structure 'state' or 'config'.")
            return False

        if isinstance(parameter, dict):
            data = parameter.copy()
        else:
            data = {parameter: value}

        # Attempting to set this causes an error.
        if "lastupdated" in data:
            del data["lastupdated"]

        result = None
        logger.debug(str(data))
        result = self.request('PUT', f'/api/{self.username}/sensors/{sensor_id}/{structure}', data)
        if 'error' in list(result[0].keys()):
            logger.warn("ERROR: {0} for sensor {1}".format(result[0]['error']['description'], sensor_id))

        logger.debug(result)
        return result

    def delete_sensor(self, sensor_id):
        try:
            name = self.sensors_by_id[sensor_id].name
            del self.sensors_by_name[name]
            del self.sensors_by_id[sensor_id]
            return self.request('DELETE', f'/api/{self.username}/sensors/{sensor_id}')
        except:
            logger.debug("Unable to delete nonexistent sensor with ID %d", sensor_id)


# explicitly define the outward facing API of this module
__all__ = [Bridge.__name__]
