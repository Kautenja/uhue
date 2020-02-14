"""The splatter web application"""
import os
import flask
import phue


# create the Flask web server
app = flask.Flask(__name__)

# create the connection to the Hue bridge
bridge = phue.Bridge()


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


# create the route for the root URL
@app.route("/")
def home():
    """Return the home page."""
    print(bridge.ip)
    return flask.render_template("home.html")
