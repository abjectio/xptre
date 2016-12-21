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
import emojipy
import re


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

    def __init__(self, trello, board_id=None, members=False, nodesclists=None, hidelist=None):
        self.data = []

        self.trello = trello
        self.nodesclists = nodesclists
        self.hidelist = hidelist
        self.members = members

        self.myboard = self.trello.boards.get(board_id)

    def get_background_image(self):

        return self.myboard['prefs']['backgroundImage'] if 'backgroundImage' in self.myboard['prefs'] else None

    def populate_board(self):
        self.lists = self.trello.boards.get_list(self.myboard.get('id'), None, None, 'open', 'id,name')

        #Hrmfff - not satisfied with this hack ...
        #Create a new list where hidden columns does not exists
        if self.hidelist is not None:
            tmplist = [int(n) for n in self.hidelist.split(',')]
            tmpcolumns = []
            counter = 0
            while counter < len(self.lists):
                if counter not in tmplist:
                    tmpcolumns.append(self.lists[counter])
                counter = counter + 1
            self.lists = tmpcolumns

        for one_list in self.lists:
            get_fields = 'name' if one_list.get('name') in self.nodesclists else 'name,desc'  # name,desc
            one_list['cards'] = self.trello.lists.get_card(one_list.get('id'), None, None, str(self.members).lower(), None, None, 'open', get_fields)

        self.myboard['lists'] = self.lists

    def get_data(self):
        self.bootstrap_grid = int(round(float(12.0 / len(self.lists))))
        self.myboard['numoflists'] = self.bootstrap_grid
        self.myboard['background_img_url'] = self.get_background_image()

        return self.myboard


class SlackFeed:
    """Slack wrapper class"""

    def __init__(self, slacker=None, numberofrows=None):

        self.numberofrows = 8 if (numberofrows is None) or (int(numberofrows)>20) else numberofrows
        self.slacker = slacker
        emojies_response = self.slacker.emoji.list()
        self.slackemojies = emojies_response.body['emoji']
        self.emojione = emojipy.Emoji()

    def feed_from_channel(self, channel_name=None):

        response = self.slacker.channels.list(True)
        channel_list = response.body['channels']

        i = 0
        while i < len(channel_list) and (channel_list[i].get('name') != channel_name):
            i += 1

        channel_id = channel_list[i].get('id')
        history_response = self.slacker.channels.history(channel_id, '0', '0', self.numberofrows, False, False)
        messages = history_response.body['messages']
        # sort messages - oldest first - ts = timestamp
        messages = sorted(messages, key=lambda message: message['ts'])

        i = 0
        while i < len(messages):

            should_view = self.should_view(messages[i])
            if should_view is False:
                del messages[i]
                i -= 1

            if should_view and 'user' in messages[i]:
                self.replace_text(messages[i])
                user_resp = self.slacker.users.info(messages[i]['user'])

                if user_resp is not None:
                    real_name = user_resp.body['user'].get('real_name')
                    if len(real_name) <= 1:
                        real_name = user_resp.body['user'].get('name')
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
        if 'subtype' in message and ('channel_join' in message['subtype'] or 'bot' in message['subtype']):
            view = False
        return view

    def replace_at_user(self, message=None):

        # Find and replace userid with first name. Text could be either <@USERID> or <@USERID|nick>
        users = re.findall('<@(.*?)(?:>|\|.*?>)', message['text'])

        for user in users:
            slack_user_info_resp = self.slacker.users.info(user)
            user_name = '<span style="background:lightYellow; color:black; font-type: strong;">&nbsp;' + \
                        slack_user_info_resp.body['user']['profile']['first_name'] + '&nbsp;</span>'
            message['text'] = re.sub(r'<@' + user + '(>|\|.*?>)', user_name, message['text'])

    def replace_text(self, message=None):

        if 'subtype' in message and 'file_share' in message['subtype'] and message['file']['thumb_360']:
            message['text'] = '<img src="./image?file_name=' + message['file']['thumb_360'] + '" class="img-thumbnail">'
            if 'initial_comment' in message['file']:
                message['text'] = message['file']['initial_comment']['comment'] + '</br>' + message['text']

        if 'subtype' in message and 'me_message' in message['subtype']:
            message['text'] = '<i><strong>(Me)</strong> - ' + message['text'] + '</i>'

        # Replace newline with breaks
        message['text'] = re.sub(r'(\n)', '</br>', message['text'])

        self.replace_emojies(message)
        self.replace_at_user(message)

    def replace_emojies(self, message=None):

        # Find and replace emojies
        emojies = re.findall(':(.*?):', message['text'])
        for emoji in emojies:
            # Get the emoji short_cut code (EmojiOne)
            new_emoji = self.emojione.shortcode_to_image(':' + emoji + ':', style='height: 32px; width: 32px;')

            # If it was not found in EmojiOne - Try Slack custom emojies
            if (new_emoji == ':' + emoji + ':') and (emoji in self.slackemojies):
                new_emoji = self.slackemojies[emoji]
                new_emoji = '<img style="height: 32px; width: 32px;" class="emojione" src="' + new_emoji + '"/>'

            # Replace with new emoji
            message['text'] = re.sub(r':' + emoji + ':', new_emoji, message['text'])
