"""The Splatter web server."""
import argparse
from splatter.app import app


# parse command line arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--port', '-p',
    type=int,
    help='The port to run the service at.',
    required=False,
    default=8080
)
parser.add_argument('--debug', '-d',
    help='Whether to run the server in debugging mode.',
    required=False,
    default=False,
    action='store_true'
)
args = parser.parse_args()


# run the application
app.run(port=args.port, debug=args.debug)
