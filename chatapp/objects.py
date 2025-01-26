from flaskext.markdown import Markdown
from flask_socketio    import SocketIO
from flask             import Flask

# create Flask app
app    = Flask(__name__)

# change settings to remove whitespace
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# load extension to allow markdown to html conversion (via jinja)
Markdown(app)

# link socket.io to Flask app (enable talking with JavaScript)
socket = SocketIO(app)