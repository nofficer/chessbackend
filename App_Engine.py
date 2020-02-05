import numpy as np
import os
from keras.models import model_from_json
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.preprocessing.text import Tokenizer
import h5py
import chess
import bot_enginetest






turn = ''


def board_builder():
    board = chess.Board()
    return board.build_FE_board()

def build_FE_board(self):
    builder = []
    builder_append = builder.append
    for square in chess.SQUARES_180:
        mask = chess.BB_SQUARES[square]
        if not self.occupied & mask:
            builder_append(0)
        elif bool(self.occupied_co[chess.WHITE] & mask):
            if self.pawns & mask:
                builder_append(7)
            elif self.knights & mask:
                builder_append(8)
            elif self.bishops & mask:
                builder_append(9)
            elif self.rooks & mask:
                builder_append(10)
            elif self.queens & mask:
                builder_append(11)
            elif self.kings & mask:
                builder_append(12)
        elif self.pawns & mask:
            builder_append(1)
        elif self.knights & mask:
            builder_append(2)
        elif self.bishops & mask:
            builder_append(3)
        elif self.rooks & mask:
            builder_append(4)
        elif self.queens & mask:
            builder_append(5)
        elif self.kings & mask:
            builder_append(6)
    return builder
chess.BaseBoard.build_FE_board = build_FE_board

MoveMakerDict = bot_enginetest.MoveMakerDict

def conv_nums_to_fen(item):
    bf = []
    for num in item:
        if num == 4:
            bf.append('r')
        elif num == 2:
            bf.append('n')
        elif num == 3:
            bf.append('b')
        elif num == 5:
            bf.append('q')
        elif num == 6:
            bf.append('k')
        elif num == 1:
            bf.append('p')
        elif num == 0:
            bf.append(1)
        elif num == 7:
            bf.append('P')
        elif num == 10:
            bf.append('R')
        elif num == 8:
            bf.append("N")
        elif num == 9:
            bf.append("B")
        elif num ==11:
            bf.append("Q")
        elif num == 12:
            bf.append('K')
    return bf


def insert_slash(bf):
    count = -1
    start_at = -1
    for item in bf:
        count+= 1
        start_at += 1
        bfin = bf.index(item, start_at)
        if count == 8:
            bf.insert(bfin,"/")
            count = -1
        else:
            None
    return bf

def agg_blank(bf):
    newbf = ''
    counter = 0
    for item in bf:
        if item == 1:
            counter +=1
        elif item != 1:
            if counter != 0:
                newbf = newbf + str(counter)
                counter = 0
                newbf = newbf + item
            else:
                newbf = newbf + item
    return(newbf)

def get_key(val):
    movesDict = MoveMakerDict.items()
    for key, value in movesDict:
         if val == value:
             return key

def next_player_move(move,boardfen,side):
    print(f"from the player move in engine{boardfen}")
    #Need to convert the boardfen into an actual board fen
    boardfen_converted = agg_blank(insert_slash(conv_nums_to_fen(boardfen))) + " " + side
    #Set the board to be the board before the player made the move
    board = chess.Board(boardfen_converted)
    legals = [str(legal) for legal in list(board.legal_moves)]
    print(board)
    print(legals)
    sqs = move
    sq1 = sqs[0]
    sq2 = sqs[1]
    coord1 = str(get_key(int(sq1)))
    coord2 = str(get_key(int(sq2)))
    theirMove = coord1 + coord2
    #Check the legality of the move against the board receved from the front-end
    if(theirMove in legals):
        moveparsed = chess.Move.from_uci(theirMove)
        board.push(moveparsed)
        newboard = board.build_FE_board()
        if side == 'w':
            side = 'b'
        elif side == 'b':
            side = 'w'
        return (newboard,1,side)
    else:
        return (boardfen,0,side)


def build_input_board(self):
    builder = []
    builder_append = builder.append
    for square in chess.SQUARES_180:
        mask = chess.BB_SQUARES[square]

        if not self.occupied & mask:
            builder.extend([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        elif bool(self.occupied_co[chess.WHITE] & mask):
            if self.pawns & mask:
                builder.extend([0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0])
            elif self.knights & mask:
                builder.extend([0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0])
            elif self.bishops & mask:
                builder.extend([0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0])
            elif self.rooks & mask:
                builder.extend([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0])
            elif self.queens & mask:
                builder.extend([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0])
            elif self.kings & mask:
                builder.extend([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
        elif self.pawns & mask:
            builder.extend([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        elif self.knights & mask:
            builder.extend([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        elif self.bishops & mask:
            builder.extend([0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        elif self.rooks & mask:
            builder.extend([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        elif self.queens & mask:
            builder.extend([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
        elif self.kings & mask:
            builder.extend([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0])

    return np.reshape(np.array(builder), (1,8,8,12))
chess.BaseBoard.build_input_board = build_input_board

def bot_move(boardfen,side):
    boardfen_converted = agg_blank(insert_slash(conv_nums_to_fen(boardfen))) + " " + side
    board = chess.Board(boardfen_converted)
    legals = list(board.legal_moves)
    input_board = board.build_input_board()
    bot_choice = bot_enginetest.Bot_Engine(board,legals,input_board).bot_move()
    botmove = bot_choice
    print(f"Bot Chose {botmove}")
    board.push(botmove)
    turn = 'player'
    if board.is_checkmate():
        if(board.turn ==chess.WHITE):
            Winner = "Congrats Black"
            print(Winner)
            return tuple(("Game Over",board.build_FE_board()))
        else:
            Winner = "Congrats White"
            print(Winner)
            return tuple(("Game Over",board.build_FE_board()))
        print(board)
        return "Game Over"
    else:
        print(board)
        if side == 'w':
            side = 'b'
        elif side == 'b':
            side = 'w'
        return tuple((str(botmove),board.build_FE_board(), side))



#BOT ENGINE BELOW
