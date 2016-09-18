"""
:mod:`board_www` -- Flask app which displays a Trello board
==================================================================

.. module:: board_www
   :platform: Unix, Windows
   :synopsis: Flask app which displays a Trello bord
.. moduleauthor:: Knut Erik Hollund <knut.erik@unlike.no>

This file is part of xptre python code.

import_events is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

import_events is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with import_events.  If not, see <http://www.gnu.org/licenses/>.

"""
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from lib.TreBoard import TreBoard

app = Flask(__name__)
Bootstrap(app)
app.config.from_envvar('XPTRE_SETTINGS')
myboard = TreBoard(app.config.get('AUTH_KEY'), app.config.get('TOKEN'), app.config.get('BOARD_ID'), app.config.get('MEMBERS'),app.config.get('NO_DESCRIPTION'))  # TreBoard class


@app.route('/')
def display_board():
    myboard.populate_board()
    return render_template("board.html", data=myboard.get_data())


@app.route('/about')
def about():
    return render_template("about.html", info={'about': {'name':'me' } })


@app.route('/lists')
def get_lists():
    return str(myboard.get_lists())

if __name__ == '__main__':
    app.run()