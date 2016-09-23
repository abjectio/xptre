## xptre - Export Trello Board

Just a hack (Flask App) to explore how I can visualise a private Trello board.

Dependent on the Python [trello package](https://pypi.python.org/pypi/trello) `$pip install trello`

You need some configuration settings in the `example_config.py` file :
- DEBUG True / False - Debug mode in Flask
- AUTH_KEY - Trello auth key.
- TOKEN - Trello token key.
- BOARDS - id of the trello boards you wish to visualise.
- MEMBERS - `True` if you wish to show names on members of a card.
- NO_DESCRIPTION - Array of strings (name on list), which should not show description in cards. E.g. a 'Done' column. Example: `['Done','ToDo / Backlog']`

Example:
```
XPTRE = { 'AUTH_KEY':'your_auth_key_to_trello',
          'TOKEN':'your_token_to_trello',
         'BOARDS' : [ {'id':'board_id_from_trello', 'url':'theurlyouwish', 'members':'True', 'no_description':'ListName'},
          {'id': 'another_board_id_form_trello','url':'anotherurl', 'members':'True', 'no_description':'another_list_in_second_board'}]
}
```
