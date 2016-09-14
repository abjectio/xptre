#!/usr/bin/python
from trello import TrelloApi, Boards
from lib.util import populate_configs, initiate_logging, loginfo, shutdownLogger

def main():
    """main function"""

    #Logging
    initiate_logging("/tmp/export_board.log")
    loginfo('[EXPORT BOARD]')

    #Populate the configs
    parser_config = populate_configs()
    
    #Config header name
    section = "config"
    AUTH_KEY = parser_config.get(section, 'AUTH_KEY')
    TOKEN = parser_config.get(section, 'TOKEN')
    BOARD_ID = parser_config.get(section, 'BOARD_ID')

    trello = TrelloApi(AUTH_KEY)
    token = trello.set_token(TOKEN)
    
    your_board = trello.boards.get(BOARD_ID)
    my_lists = trello.boards.get_list(BOARD_ID)

    print 'JOJO %s ' % my_lists


    
#############
#Execute main
if __name__ == '__main__':
    main()
