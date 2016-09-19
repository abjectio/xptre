## xptre - Export Trello Board

Just a hack (Flask App) to explore how I can visualise a private Trello board.

Dependent on the Python [trello package](https://pypi.python.org/pypi/trello) `$pip install trello`

You need some configuration settings in the `example_config.py` file :
- DEBUG True / False - Debug mode in Flask
- AUTH_KEY - Trello auth key.
- TOKEN - Trello token key.
- BOARD_ID - id of the trello board you wish to visualise.
- MEMBERS - `True` if you wish to show names on members of a card.
- NO_DESCRIPTION - Array of strings (name on list), which should not show description in cards. E.g. a 'Done' column. Example: `['Done','ToDo / Backlog']`


