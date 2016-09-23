# Run the server
from app import app

app.config.from_object('config')
app.run(host=app.config.get('HOST'), port=app.config.get('PORT'), debug=app.config.get('DEBUG'), threaded=app.config.get('THREADED'))
