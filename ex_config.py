# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEBUG = True/False #Debug mode in Flask

# Trello
XPTRE = { 'AUTH_KEY':'your_auth_key_to_trello',
          'TOKEN':'your_token_to_trello',
         'BOARDS' : [ {'id':'board_id_from_trello', 'url':'theurlyouwish', 'members':'True', 'no_description':'ListName'},
          {'id': 'another_board_id_form_trello','url':'anotherurl', 'members':'True', 'no_description':'another_list_in_second_board'}]
}
