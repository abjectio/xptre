from trello import TrelloApi

AUTH_KEY = ''
TOKEN = ''
BOARD_ID = ''


trello = TrelloApi(AUTH_KEY)
token = trello.set_token(TOKEN)
your_board = trello.boards.get(BOARD_ID)



