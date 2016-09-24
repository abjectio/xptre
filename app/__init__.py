# Import flask and template operators
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
# Import modules
from app.mod_trello.controllers import display_board as displayboard_module

from trello import TrelloApi

# Define the WSGI application object
app = Flask(__name__)
Bootstrap(app)

# Configurations
app.config.from_object('config')
xptre_config = app.config.get('XPTRE')
trello = TrelloApi(xptre_config.get('AUTH_KEY'))
trello.set_token(xptre_config.get('TOKEN'))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', data=error), 404


@app.route('/<board_url>')
def display_board(board_url):
    tmp_config = {'BOARD_ID': None, 'MEMBERS': None, 'NO_DESCRIPTION': None}

    tmp_boards = xptre_config.get('BOARDS')
    for one_board in tmp_boards:
        if board_url == one_board.get('url'):
            tmp_config['BOARD_ID'] = one_board.get('id')
            tmp_config['MEMBERS'] = one_board.get('members')
            tmp_config['NO_DESCRIPTION'] = one_board.get('no_description')
            return render_template("trello/board.html", data=displayboard_module(trello, tmp_config))

    return not_found( {'message':'URL not found : ' + board_url} )


@app.route('/table/<board_url>')
def display_board_as_table(board_url):
    tmp_config = {'BOARD_ID': None, 'MEMBERS': None, 'NO_DESCRIPTION': None}

    tmp_boards = xptre_config.get('BOARDS')
    for one_board in tmp_boards:
        if board_url == one_board.get('url'):
            tmp_config['BOARD_ID'] = one_board.get('id')
            tmp_config['MEMBERS'] = one_board.get('members')
            tmp_config['NO_DESCRIPTION'] = one_board.get('no_description')
            return render_template("trello/tblboard.html", data=displayboard_module(trello, tmp_config))

    return not_found( {'message':'URL not found : ' + board_url} )
