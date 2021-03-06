"""The web server command line interface."""
import argparse
from uhue.app import app


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


app.run(port=args.port, debug=args.debug)
