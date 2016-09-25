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
from models import TreBoard
from models import SlackFeed


def init_board(trello=None, config=None):
    return TreBoard(trello, config.get('BOARD_ID'),
                    config.get('MEMBERS'), config.get('NO_DESCRIPTION'))  # TreBoard class


def display_board(trello=None, config=None):
    myboard = init_board(trello, config)
    myboard.populate_board()
    return myboard.get_data()


def feed_from_slack_channel(slacker=None, channel_name=None):

    slack_feed = SlackFeed(slacker)
    channel_feed = slack_feed.feed_from_channel(channel_name)

    return channel_feed
