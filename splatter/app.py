"""The splatter web application"""
import os
import flask


# create the Flask web server
APP = flask.Flask("Splatter")


@APP.route('/site.webmanifest')
def webmanifest():
    """Return the web manifest associated with the application."""
    return flask.send_from_directory(
        os.path.join(APP.root_path, 'static'),
        'site.webmanifest', mimetype='application/manifest+json'
    )


@APP.route('/favicon.ico')
def favicon():
    """Return the favicon associated with the application."""
    return flask.send_from_directory(
        os.path.join(APP.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )


# create the route for the root URL
@APP.route("/")
def home():
    """Return the home page."""
    return flask.render_template("home.html")
