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
import datetime
import emoji


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

        #emojies_response = self.slacker.emoji.list()
        #self.emojies = emojies_response.body['emoji']


    def feed_from_channel(self, channel_name=None):

        response = self.slacker.channels.list(True)
        channel_list = response.body['channels']

        i = 0
        while i < len(channel_list) and (channel_list[i].get('name') != channel_name):
            i += 1

        channel_id = channel_list[i].get('id')
        history_response = self.slacker.channels.history(channel_id, '0', '0', 10, False, False)
        messages = history_response.body['messages']
        # sort messages - oldest first - ts = timestamp
        messages = sorted(messages, key=lambda message: message['ts'])

        i = 0
        while i < len(messages):

            self.replace_text(messages[i])
            should_view = self.should_view(messages[i])
            if should_view is False:
                del messages[i]
                i -= 1

            if should_view and 'user' in messages[i]:
                user_resp = self.slacker.users.info(messages[i]['user'])

                if user_resp is not None:
                    real_name = user_resp.body['user'].get('real_name')
                    user_profile = user_resp.body['user'].get('profile')
                    user_img = user_profile['image_32']
                    ts = messages[i]['ts']
                    messages[i]['user_name'] = real_name
                    messages[i]['user_img'] = user_img
                    messages[i]['msg_time'] = datetime.datetime.fromtimestamp(float(ts)).strftime('%c')

            i += 1
        return messages

    def should_view(self, message=None):

        view = True
        if 'subtype' in message and 'channel_join' in message['subtype']:
            view = False
        return view

    def replace_text(self, message=None):

        message['text'] = emoji.emojize(message['text'])
        if 'subtype' in message and 'file_share' in message['subtype'] and message['file']['thumb_360']:
            message['text'] = '<img src="' + message['file']['thumb_360'] + '"  class="img-thumbnail">'
