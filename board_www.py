#!/usr/bin/python
from trello import TrelloApi, Lists
from lib.util import populate_configs, initiate_logging, loginfo, shutdownLogger
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
@app.route('/')
def display_board():
    #Bootstrap(app)
    return render_template("board.html", board=populate_board('/home/abjectio/koding/xptre/testconfig.cfg'))

def populate_board(configfile):
    #  Populate the configs
    parser_config = populate_configs(configfile)

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

    your_board['numlists'] = 12/len(lists)

    return your_board

@app.route('/about')
def about():
    return render_template("about.html", info={'about': {'name':'me' } })

if __name__ == '__main__':
    app.run(debug=True)