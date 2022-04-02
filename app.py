from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask import request

import os



import h5py
import chess
import bot_enginetest

import App_Engine
app = Flask(__name__)
cors = CORS(app)



def board_builder():
    return App_Engine.board_builder()


@app.route('/board/move', methods=["POST"])
def move():
    move_and_fen = request.json
    move = move_and_fen[0]
    boardfen = move_and_fen[1]
    side = move_and_fen[2]
    return jsonify(App_Engine.next_player_move(move,boardfen,side))

@app.route('/bot_move', methods=["POST"])
def bot_move():
        board_and_side = request.json
        boardfen = board_and_side[0]
        side = board_and_side[1]
        return jsonify(App_Engine.bot_move(boardfen, side))

@app.route('/reset', methods=["POST"])
def reset():
    resetList = request.json
    switchSide = resetList[0]
    side = resetList[1]
    boardfen = resetList[2]
    print(resetList)
    if(switchSide[0] == "No"):
        print('------New Game------')
        return jsonify(("New Game",board_builder(),'w'))
    else:
        return jsonify(App_Engine.bot_move(boardfen, side))



@app.route('/ping', methods=["GET"])
def ping():
        return('ping')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# thraded=False : this makes it so the server can only handle 1 request at a time. I was getting AttributeError: '_thread._local' object has no attribute 'value' when it tried to call model.predict from the bot_engine
