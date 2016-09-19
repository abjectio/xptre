# Import flask and template operators
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
# Import modules
from app.mod_trello.controllers import display_board as displayboard_module
from app.mod_trello.controllers import get_lists as board_getlists

# Define the WSGI application object
app = Flask(__name__)
Bootstrap(app)

# Configurations
app.config.from_object('config')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def display_board():
    return render_template("trello/board.html", data=displayboard_module(app.config))


@app.route('/lists')
def get_lists():
    lists = board_getlists(app.config)
    return str(lists)
