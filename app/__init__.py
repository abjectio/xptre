# Import flask and template operators
from flask import Flask, Response, render_template, request
from flask_bootstrap import Bootstrap
import requests

# Import modules
from app.mod_trello.controllers import display_board as displayboard_module
from app.mod_trello.controllers import feed_from_slack_channel as channel_feed

from trello import TrelloApi
from slacker import Slacker

# Define the WSGI application object
app = Flask(__name__)
Bootstrap(app)

# Configurations
app.config.from_object('config')
xptre_config = app.config.get('XPTRE')
trello = TrelloApi(xptre_config.get('AUTH_KEY'))
trello.set_token(xptre_config.get('TOKEN'))

slack_config = app.config.get('SLACK')
slacker = Slacker(slack_config.get('TOKEN'))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', data=error), 404


@app.route('/<board_url>', methods=['GET'])
def display_board(board_url):
    tmp_config = {'BOARD_ID': None, 'MEMBERS': None, 'NO_DESCRIPTION': None}

    tmp_boards = xptre_config.get('BOARDS')
    for one_board in tmp_boards:
        if board_url == one_board.get('url'):
            tmp_config['BOARD_ID'] = one_board.get('id')
            tmp_config['MEMBERS'] = one_board.get('members')
            tmp_config['NO_DESCRIPTION'] = one_board.get('no_description')
            tmp_config['HIDE'] = request.args.get('hide')
            return render_template("trello/board.html", data=displayboard_module(trello, tmp_config))

    return not_found({'message': 'URL not found : ' + board_url})


@app.route('/slack/<channel_name>', methods=['GET'])
def display_slack_channel(channel_name):
    numberofrows = request.args.get('rows')
    return render_template("slack/channel_feed.html", data=channel_feed(slacker, channel_name, numberofrows))


@app.route('/slack/image', methods=['GET'])
def get_slack_images():

    file_name = request.args['file_name']
    slack_headers = {'Authorization': 'Bearer ' + slack_config.get('TOKEN')}
    slack_request = requests.get(file_name, headers=slack_headers)

    img_response = Response(slack_request.content)
    img_response.headers['content-type'] = slack_request.headers['content-type']
    img_response.headers['content-length'] = slack_request.headers['content-length']

    return img_response
