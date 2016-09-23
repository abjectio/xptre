"""
This file is part of xptre python code.

xptre is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

xptre is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with xptre.  If not, see <http://www.gnu.org/licenses/>.

"""
from trello import TrelloApi


class TreBoard:
    """Trello Board wrapper class"""
    board_id = None
    trello = None  # TrelloAPI
    myboard = None  # Boards
    lists = []
    cards = []
    nodesclists = []
    members = False
    bootstrap_grid = None

    def __init__(self, trello, board_id=None, members=False, nodesclists=None):
        self.data = []

        self.trello = trello
        self.nodesclists = nodesclists
        self.members = members

        self.myboard = self.trello.boards.get(board_id)
        self.nodesclists = nodesclists

    def populate_board(self):
        self.lists = self.trello.boards.get_list(self.myboard.get('id'), None, None, 'open', 'id,name')

        for one_list in self.lists:
            get_fields = 'name' if one_list.get('name') in self.nodesclists else 'name,desc' #name,desc
            one_list['cards'] = self.trello.lists.get_card(one_list.get('id'), None, None, str(self.members).lower(), None, None, 'open', get_fields)

        self.myboard['lists'] = self.lists

    def get_data(self):
        self.bootstrap_grid = 12 / len(self.lists)
        self.myboard['numoflists'] = self.bootstrap_grid
        return self.myboard
