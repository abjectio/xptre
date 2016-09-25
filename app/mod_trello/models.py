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
import json


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


class SlackFeed:
    """Trello Board wrapper class"""

    def __init__(self, slacker=None):

        self.slacker = slacker

    def feed_from_channel(self, channel_name=None):

        response = self.slacker.channels.list(True)
        channel_list = response.body['channels']

        i = 0
        while i < len(channel_list) and (channel_list[i].get('name') != channel_name):
            i = i+1

        channel_id = channel_list[i].get('id')
        history_response = self.slacker.channels.history(channel_id, '0', '0', 10, False, False)
        messages = history_response.body['messages']
        # sort messages - oldest first - ts = timestamp
        messages = sorted(messages, key=lambda message: message['ts'])

        for tmp_msg in messages:
            user_resp = self.slacker.users.info(tmp_msg['user'])
            real_name = user_resp.body['user'].get('real_name')
            tmp_msg['user_name'] = real_name

        return messages
