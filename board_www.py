#!/usr/bin/python
from trello import TrelloApi, Lists
from lib.util import populate_configs, initiate_logging, loginfo, shutdownLogger
from flask import Flask

app = Flask(__name__)
@app.route('/')

def draw_html():

    the_board = draw_board()

    html = '<html><head>'
    html += '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">'
    html += '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" >'
    html += '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>'
    html += '</head>'
    html += '<body>'

    html += '<div class="alert alert-success"><centre>' + the_board.get('name') + '</centre></div>'

    html_lists = ''
    lists = the_board.get('lists')

    html_lists = ''

    for one_list in lists:

        html_lists += '<div class="panel panel-default">'
        html_lists += '<div class="panel-heading">' + one_list.get('name') + '</div>'
        html_lists += '<div class="panel-body">'

        cards = one_list.get('cards')

        html_cards = '<td><div class="list-group">'
        for one_card in cards:
            html_cards += '<div href="#" class="list-group-item">' + one_card.get('name') + '</div>'
        html_cards += '</div></td>'

        html_lists += html_cards + "</div></div>"


    html += html_lists +  '</body></html>'
    return html

def draw_board():
    # Logging
    initiate_logging("/tmp/export_board.log")
    loginfo('[EXPORT BOARD]')

    #  Populate the configs
    parser_config = populate_configs('/home/abjectio/PhpstormProjects/xptre/testconfig.cfg')
    #
    #  Config header name
    section = "config"
    AUTH_KEY = parser_config.get(section, 'AUTH_KEY')
    TOKEN = parser_config.get(section, 'TOKEN')
    BOARD_ID = parser_config.get(section, 'BOARD_ID')

    trello = TrelloApi(AUTH_KEY)
    token = trello.set_token(TOKEN)

    your_board = trello.boards.get(BOARD_ID)
    your_board['lists'] = []
    lists = trello.boards.get_list(BOARD_ID)
    cards = trello.boards.get_card(BOARD_ID)

    for one_list in lists:
        id = one_list.get('id')
        name = one_list.get('name')

        cards_in_list = []
        for one_card in cards:
            if one_card.get('idList') == id:
                cards_in_list.append(one_card)

        one_list['cards'] = cards_in_list
        your_board['lists'].append(one_list)

    return your_board