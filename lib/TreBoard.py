"""
:mod:`lib.TreBoard` -- Trello class wrapper
==================================================================

.. module:: TreBoard
   :platform: Unix, Windows
   :synopsis: Class handling Trello board
.. moduleauthor:: Knut Erik Hollund <knut.erik@unlike.no>

This file is part of xptre python code.

import_events is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

import_events is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with import_events.  If not, see <http://www.gnu.org/licenses/>.

"""
from trello import TrelloApi


class TreBoard:
    """A simple example class"""
    trello = None  # TrelloAPI
    myboard = None  # Boards
    lists = []
    cards = []
    bootstrap_grid = None

    def __init__(self, auth_key=None, token=None, board_id=None):
        self.data = []

        self.trello = TrelloApi(auth_key)
        self.trello.set_token(token)

        self.myboard = self.trello.boards.get(board_id)
        self.lists = self.trello.boards.get_list(board_id)

        self.populate_board()

    def populate_board(self):

        for one_list in self.lists:
            list_id = one_list.get('id')
            tmp_cards = self.trello.lists.get_card(list_id)
            # for one_card in tmp_cards:
                #members = self.trello.cards.get_member(one_card.get('id'))
                #members = []
                #one_card['members'] = members
            one_list['cards'] = tmp_cards

        self.myboard['lists'] = self.lists
        self.bootstrap_grid = 12 / len(self.lists)
        self.myboard['numoflists'] = self.bootstrap_grid

    def get_lists(self):
        return self.lists

    def get_data(self):
        return self.myboard
