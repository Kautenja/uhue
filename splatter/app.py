"""The splatter web application"""
import os
import json
import flask
from . import phue


# create the Flask web server
app = flask.Flask(__name__)


# create the connection to the Hue bridge
bridge = phue.Bridge()
# bridge.connect()


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


@app.route('/img/icon.png')
def icon():
    """Return the icon associated with the application."""
    return flask.send_from_directory(
        os.path.join(app.root_path, 'static'),
        'img/icon.png', mimetype='image/vnd.microsoft.icon'
    )


# create the route for the root URL
@app.route("/")
def home():
    """Return the home page."""
    lights = sorted(bridge.lights, key=lambda x: x.name)
    return flask.render_template("home.html", lights=lights)


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
