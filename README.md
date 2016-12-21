## xptre - Export Trello Board

Just a hack (Flask App) to explore how I can visualise a private Trello board.

Dependent on a few Python libraries. See [requirements.txt](https://github.com/abjectio/xptre/blob/master/requirements.txt) 
`$pip install -r requirements.txt`

You need some configuration settings in the `example_config.py` file :
- HOST XXX.XXX.XXX.XXX - IP address
- PORT XX - Listening on port
- THREADED True / False

## Trello
JSON - which has info on Trello boards :
- DEBUG True / False - Debug mode in Flask
- AUTH_KEY - Trello auth key.
- TOKEN - Trello token key.
- BOARDS - id of the trello boards you wish to visualise.
- MEMBERS - `True` if you wish to show names on members of a card.
- NO_DESCRIPTION - Array of strings (name on list), which should not show description in cards. E.g. a 'Done' column. Example: `['Done','ToDo / Backlog']`

Example on JSON :
```
XPTRE = { 'AUTH_KEY':'your_auth_key_to_trello',
          'TOKEN':'your_token_to_trello',
         'BOARDS' : [ {'id':'board_id_from_trello', 'url':'theurlyouwish', 'members':'True', 'no_description':'ListName'},
          {'id': 'another_board_id_form_trello','url':'anotherurl', 'members':'True', 'no_description':'another_list_in_second_board'}]
}
```

It is possible to hide lists in your Trello board by using parameter ``` hide ```.
Example: ``` http://localhost/myboard?hide=1,3,4 ``` , which will hide list number 1, 3 and 4.

## Slack
Not related to Trello, however implemented possibility to view a channel from [Slack](https://www.slack.com)
A token is needed from Slack in the configuration file. 
- SLACK = ``` {'TOKEN': 'your_token'} ```
Access the channel by using url ``` http://yourserver/slack/<channelname> ```

Default return is the last 8 rows from feed. It is possible to use parameter ``` rows ``` to specify 
number of rows returned. (Max 20 rows)

Example: ``` http://localhost/slack/mychannel?rows=10 ```
