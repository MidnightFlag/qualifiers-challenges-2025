from flask import Flask, request, session, render_template, redirect, url_for
from random import randint
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)
FLAG = os.getenv("FLAG") or "MCTF{FAKE_FLAG_FOR_TESTING}"

class Game:
    def __init__(self, nb_batons):
        self.nb_batons = nb_batons
        self.board = self.create_board()

    def create_board(self):
        return ['|' for _ in range(self.nb_batons)]

    def last_stick(self):
        return len(self.board) == 1

    def take_stick(self, nb):
        if len(self.board) >= nb :
            self.board = self.board[nb:]

    def bot_turn(self):
        for k in range(1, 4):
            if (len(self.board) - k) % 4 == 1:
                return k
        return randint(1, 3)
    
@app.route('/')
def index():
    # Initialize a new game at refresh
    session['game'] = 20
    game = Game(session['game'])
    nb = game.bot_turn()
    game.take_stick(nb)
    session['game'] = len(game.board)
    return render_template('index.html', board=game.board)
 
@app.route('/play', methods=['POST'])
def play():
    if 'game' not in session:
        session['game'] = 20

    # Load game from session
    game = Game(session['game'])

    # Player's move
    try :
        player_choice = int(request.json['player_choice'])
        if player_choice <= 0:
            return {"win":False,"game_ended":False,"board":game.board,"error":"No dude, you can't remove a null or negative number of sticks 😈"}
        game.take_stick(player_choice)
        if game.last_stick():
            session.pop('game', None)
            return {"win":True,"game_ended":True,"board":game.board,"flag":FLAG}
    except Exception as e :
        return {"win":False,"game_ended":False,"board":game.board,"error":"Hey, don't try to trick me 👿"}

    # Bot's turn
    bot_choice = game.bot_turn()
    game.take_stick(bot_choice)
    
    # Check if bot won
    if game.last_stick():
        session.pop('game', None)
        return {"win":False,"game_ended":True,"board":game.board,"bot_move":bot_choice}

    # Save game state
    session['game'] = len(game.board)
    return {"win":False,"game_ended":False,"board":game.board,"bot_move":bot_choice}


@app.route('/reset')
def reset():
    session.pop('game', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False, port=8888, host='0.0.0.0')
