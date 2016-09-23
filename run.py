# Run the server
from app import app

app.config.from_object('config')
app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
