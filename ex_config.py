# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEBUG = True/False #Debug mode in Flask

# Trello
AUTH_KEY= '' #Trello auth key.
TOKEN= '' #Trello token key.
BOARD_ID= '' #id of the trello board you wish to visualise.
MEMBERS= '' #True if you wish to show names on members of a card.
NO_DESCRIPTION = '' #Array of strings (name on list), which should not show description in cards. E.g. a 'Done' column. Example: ['Done','ToDo / Backlog']
