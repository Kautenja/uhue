"""The splatter web application"""
import os
import flask
from . import phue


# create the Flask web server
app = flask.Flask(__name__)


# create the connection to the Hue bridge
bridge = phue.Bridge()
# check for a configuration file and load it
if bridge.has_config_file:
    bridge.load_config_file()


@app.route('/site.webmanifest')
def webmanifest():
    """Return the web manifest associated with the application."""
    return flask.send_from_directory(
        os.path.join(app.root_path, 'static'),
        'site.webmanifest', mimetype='application/manifest+json'
    )


@app.route('/favicon.ico')
def favicon():
    """Return the favicon associated with the application."""
    return flask.send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )


@app.route('/img/android-chrome-192x192.png')
def icon192():
    """Return the icon associated with the application."""
    return flask.send_from_directory(
        os.path.join(app.root_path, 'static'),
        'img/android-chrome-192x192.png', mimetype='image/vnd.microsoft.icon'
    )


@app.route('/img/android-chrome-512x512.png')
def icon512():
    """Return the icon associated with the application."""
    return flask.send_from_directory(
        os.path.join(app.root_path, 'static'),
        'img/android-chrome-512x512.png', mimetype='image/vnd.microsoft.icon'
    )


@app.route('/img/apple-touch-icon.png')
def apple_touch_icon():
    """Return the icon associated with the application."""
    return flask.send_from_directory(
        os.path.join(app.root_path, 'static'),
        'img/apple-touch-icon.png', mimetype='image/vnd.microsoft.icon'
    )


# create the route for the root URL
@app.route("/")
def home():
    """Return the home page."""
    if bridge.can_login:
        lights = sorted(bridge.lights, key=lambda x: x.name)
        return flask.render_template("home.html", lights=lights)
    bridge.ip_address = phue.find_bridge()
    if bridge.ip_address is None:  # TODO: bridge not found page
        return 400
    return flask.render_template("register.html", ip_address=bridge.ip_address)


# create the route for firing the registration
@app.route("/register", methods=['POST'])
def register():
    """Return the home page."""
    try:
        bridge.register()
    except phue.PhueRegistrationException:
        return {'PhueRegistrationException': 0}
    if bridge.can_login:
        lights = sorted(bridge.lights, key=lambda x: x.name)
        return flask.render_template("home.html", lights=lights)
    # TODO get IP from UPnP before returning register (return fail is no IP found)
    return flask.render_template("register.html")


@app.route("/lights", methods=['POST'])
def light():
    """Handle a light command"""
    data = flask.request.json
    if data['parameter'] == 'color':
        value = data['value'].lstrip('#')
        hlen = len(value)
        rgb = tuple(int(value[i : i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))
        bridge[int(data['light_id'])].color = rgb
        return 'set value'
    bridge.set_light(int(data['light_id']), data['parameter'], int(data['value']))
    return 'set value'
