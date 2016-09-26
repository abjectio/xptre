# Run the server
from app import app
import os

app.config.from_object('config')

# If in development mode I need 127.0.0.1 and not 0.0.0.0 (as in docker container)
# Use environment variable HOST=127.0.0.1
# Default is what is found in the config.py file, but if environment variable is set use, then use it
host = os.getenv('HOST', app.config.get('HOST'))
port = os.getenv('PORT', app.config.get('PORT'))

app.run(host=host, port=int(port), debug=app.config.get('DEBUG'), threaded=app.config.get('THREADED'))

