"""A container for a scene."""
import logging


logger = logging.getLogger('phue')


class Scene:
    """A container for a scene."""

    def __init__(self, sid, appdata=None, lastupdated=None,
                 lights=None, locked=False, name="", owner="",
                 picture="", recycle=False, version=0, type="", group="",
                 *args, **kwargs):
        self.scene_id = sid
        self.appdata = appdata or {}
        self.lastupdated = lastupdated
        if lights is not None:
            self.lights = sorted([int(x) for x in lights])
        else:
            self.lights = []
        self.locked = locked
        self.name = name
        self.owner = owner
        self.picture = picture
        self.recycle = recycle
        self.version = version
        self.type = type
        self.group = group

    def __repr__(self):
        # like default python repr function, but add scene name
        return f'<{self.__class__.__module__}.{self.__class__.__name__} id="{self.scene_id}" name="{self.name}" lights={self.lights}>'


# explicitly define the outward facing API of this module
__all__ = [Scene.__name__]
