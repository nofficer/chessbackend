import numpy as np
import os
from keras.models import model_from_json
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.preprocessing.text import Tokenizer
import h5py
import chess
from sys import maxsize as infinity



json_file_from = open('model.json', 'r')
loaded_from_model_json = json_file_from.read()
json_file_from.close()
loaded_from_model = model_from_json(loaded_from_model_json)

json_file_to = open('tomodel.json', 'r')
loaded_to_model_json = json_file_to.read()
json_file_to.close()
loaded_to_model = model_from_json(loaded_to_model_json)

loaded_from_model.load_weights("model.h5")
loaded_to_model.load_weights("tomodel.h5")
def makemovemap():
    movelist = []
    movedict = {}
    for num in range(1,9):
        for letter in 'hgfedcba':
            movelist.insert(0,letter + str(num))
    for move in movelist:
        movedict.update({move: movelist.index(move)})
    return(movedict)
MoveMakerDict = makemovemap()


class Bot_Engine():
    def __init__(self,board,legals,input):
    #    print("Bot Thinking...")
        self.newlegals = legals
        self.board = board
        self.BaseBoard = chess.BaseBoard(board_fen = self.board.board_fen())


    class Node():
        def __init__(self,board,legals):
            self.board = board
            self.turns = int(board.fen().split()[5])
            self.children = []
            self.legals = list(self.board.legal_moves)
            if self.turns > 15:
                self.create_children(15)
            else:
                self.create_children(50)
            if self.children == []:
                self.value = 0
            else:
                self.value = self.children[0][1]

        def create_children(self, n):


            self.best_moves = Bot_Engine.pred_moves(self.board,self.legals,self.board.build_input_board())

            self.children.extend(self.best_moves[:n])









    def get_probs(input):
        fromProbList = loaded_from_model.predict(input)
        toProbList = loaded_to_model.predict(input)
        return (fromProbList,toProbList)


    def squares_to_numbers(move, mirror=True):
        '''converts a move in uci form (i.e. a1b1) to its squares
        returns two ints
        in the above case 0, 1
        can be mirrored, which will return 56, 57'''
        # I opted for the mirror due to the format of my data
        first_square = str(move)[0:2].upper()
        second_square = str(move)[2:4].upper()
        first_square_num = getattr(chess, first_square)
        second_square_num = getattr(chess, second_square)
        if mirror is True:
            first_square_num = chess.square_mirror(first_square_num)
            second_square_num = chess.square_mirror(second_square_num)

        return (first_square_num, second_square_num)


## The speed issue stems from the checkLegal function, need to find a way to refactor this and make it faster to check if the
    def checkLegal(newvals,legals):
        LegalMoves = []
        strmoves = [(chess.Move.from_uci(Bot_Engine.conv_to_chessmove(x[0])), x[2], x[1],Bot_Engine.conv_to_chessmove(x[0])) for x in newvals if (x[0][0] != x[0][1])]
        LegalMoves = [move for move in strmoves if move[0] in legals]
        return LegalMoves


    def conv_to_tuples(arr,saveList):
        for item in arr:
            probability = format(float(item),'.12f')
            square = list(arr).index(item)
            saveList.append((square,probability))
        return saveList

    def combine(arr1,arr2):
        combinedList = []
        for item1 in arr1:
            for item2 in arr2:
                probCombine = float(item1[1])+float(item2[1])
                squareCombine = (item1[0],item2[0])
                combinedList.append((squareCombine,format(probCombine, '.12f'),probCombine*100+320))
        for val in combinedList:
            if(val[0][0]== val[0][1]):
                combinedList.pop(combinedList.index(val))
        return combinedList

    def sortList(arr):
        sortedList = []
        for item in arr:
            if(sortedList):
                if(float(item[1]) > float(sortedList[0][1])):
                    sortedList.insert(0,item)
                else:
                    sortedList.append(item)
            else:
                sortedList.append(item)
        return sortedList




    def get_key(val):
        movesDict = MoveMakerDict.items()
        for key, value in movesDict:
             if val == value:
                 return key

    def conv_to_chessmove(themove):
        coord1 = str(Bot_Engine.get_key(themove[0]))
        coord2 = str(Bot_Engine.get_key(themove[1]))
        return(coord1 + coord2)






    def get_mat_scores(board,moves):
        material_scores = []
        movesWithMatScore = []
        mat_values ={
            chess.KING: 50000,
            chess.QUEEN: 5000,
            chess.ROOK: 900,
            chess.KNIGHT: 500,
            chess.BISHOP: 500,
            chess.PAWN: 10
        }
        for move in moves:
            material_score = 0
            moveUci = move[0]
            if board.is_capture(moveUci):
                if board.is_en_passant(moveUci):
                    captured_piece = chess.PAWN
                else:
                    moved_to = getattr(chess, str(move[3][2:4].upper()))
                    captured_piece = board.piece_at(moved_to).piece_type
                material_score += mat_values[captured_piece]
            board.push(moveUci)
            if board.is_checkmate():
                material_score += mat_values[chess.KING]
            elif board.is_stalemate():
                material_score -= 100000
            else:
                material_score += 0
            board.pop()

            movesWithMatScore.append((move[0],move[1] + material_score,move[2], move[1]))
        return movesWithMatScore

    def build_output(self):
        turns = int(self.board.fen().split()[5])
        player = self.board.turn
        if turns > 15:
            sdepth = 3
        else:
            sdepth = 1
        result = self.minimax(self.Node(board=self.board,legals=self.newlegals),depth=sdepth,player=player, alpha=-1*infinity, beta=infinity)

        return result[1]


    def minimax(self,node,depth,player,alpha,beta):
        if player == chess.WHITE: ##Ok now were back up at the top and our depth is the original depth -1 so first 15 moves our depth is now zero
            player = 1 #the player is white because black just went
        elif player == chess.BLACK:
            player = -1

        if depth == 0 or node.children == []:
            #print("depth is zero")# we are going to return player*node.value here, the node.value is the matscore+prediction score which we got from pred_moves being called inside the node
            return [player*node.value] # In this case the node.value is the value of the best move predicted for the opponent if the bot were to make the current move from inside the loop below. The loop below won't run for the
            #opponents move because this return statement will break us out of the function and bring us back down to the initial loop
        if node.children[0] is not None:
            predicted_child = node.children[0][0] #e7e6 .... after the depth changes the predicted child is now the first move from the list of opponent predicted moves


        favourite_child = None
        best_advantage = -1*player*infinity #1*infinity .... after the depth changes now it's the opponent so -1*infinity.
        #This starts out as the worst possible thing for the player so basically any more predicted will trump it initially

        for move in node.children: #for each move in the list of moves that initially came from predict moves which occurs when the node is initialized
        #    print(f"This is the move currently being evaluated coming from node.children{move} the depth is currently {depth}")
            print(move)
            moveUci = move[0]
            node.board.push(moveUci) #push the move onto the board, we essentially are going to check the outcome 1 move into the future of doing each of the predicted moves
            result = self.minimax(self.Node(node.board,legals=list(node.board.legal_moves)), depth-1,-1*player,alpha,beta) # Now we run minimax again. except this time the depth is decreased to zero( if its the first 15 turns)

            # This minimax runs with the new board that has had this move pushed onto it, it also has a new list of legal moves running the minimax brings us back to the top of this function
            # We have now returned the mat+prediction score of the best possible move the opponent can make if the bot makes the current move from within the loop
            opposition_value = result[0] # opposition value is the mat+pred score of the best possible opponent move
            advantage_score = player*move[1] + opposition_value # the advantage score takes the move score from the initially predicted list and multiplies it by the player, in this case -1 , add this to the opposition value
            # This gives the advantage score which is the net of the values. If it's a really good move and the opponents move is really bad the advantage will be high, if it's a really bad move and the opponents move is really good
            #the advantage will be low
        #    print(f" This is the advantage score: {advantage_score}")
            if player == 1:
                if advantage_score > best_advantage:
                    best_advantage = advantage_score
                    favourite_child = move[0]
                    alpha = max(alpha,best_advantage)
                    if beta <= alpha:
                    #    print(f'This is alpha: {alpha} greater than or = beta: {beta}')
                    #    print(f"move {move}")
                        node.board.pop()
                        break
            elif player == -1: #since the bot is black here this is what runs
                if advantage_score < best_advantage: # if the advantage score is more negative (because the bot is black, if the bot were white then the advantage score would need to be more positive)
                # then the best advantage is the advantage score. Otherwise it stays the same and loops to the next move, this iteration occurs until it goes through all the moves
                    best_advantage = advantage_score
                    favourite_child = move[0] #puts the favorite child as the move with the best advantage score
                    beta = min(beta, best_advantage)
                    if beta <= alpha: # If the minimum of positive infinity and the best advantage is less than or equal to negative infinity then we can break out of the loop, this would only occur in situations where
                    # a move is so advantageous that the bot basically has to make it. It breaks the loop and returns the
                    #    print(f'This is beta: {beta} less than or = alpha: {alpha}')
                        #print(f"move {move}")
                        node.board.pop()
                        break
            node.board.pop() #remove the move from the stack, this is occuring so we're about to return the best move
        return [best_advantage, favourite_child, predicted_child]









    def pred_moves(board,legals,input):
        FromList = []
        ToList = []
        probs = Bot_Engine.get_probs(input)
        #print(f"This is the probs {probs[0]}")
        fromTuples = Bot_Engine.conv_to_tuples(probs[0][0],FromList)
        #print(f"This is the fromTuples {fromTuples[0]}")
        toTuples = Bot_Engine.conv_to_tuples(probs[1][0],ToList)
    #    print(f"This is the toTuples {toTuples[0]}")
        combinedParam = Bot_Engine.combine(fromTuples,toTuples)
        #print(f"This is the combinedParam {combinedParam[0]}")
        legalMovesList = Bot_Engine.checkLegal(combinedParam,legals)# This now converts it to string as well
    #    print(f"This is the legalMovesList {legalMovesList[0]}")
        matScoreMoves = Bot_Engine.get_mat_scores(board,legalMovesList)
    #    print(f"This is the matScoreMoves {matScoreMoves[0]}")
        sortedMatScoreMoves = Bot_Engine.sortList(matScoreMoves)
        #print(f"This is the sortedMatScoreMoves {sortedMatScoreMoves[0]}")
        return sortedMatScoreMoves

    def check_promo(self,move):
        squarenums = Bot_Engine.squares_to_numbers(move, mirror=False) # The piece at chess function is goofy and has a mirrored board from what I use so I mirrored the squares to numbers for correct checking
        mv_frm = int(squarenums[0])
        mv_to = int(squarenums[1])
        frm_piece = str(self.board.piece_at(mv_frm))
        to_piece = str(self.board.piece_at(mv_to))
    #    print(frm_piece)
        if frm_piece == "P":
            if chess.square_rank(mv_to) == 7:
                return move + 'Q'
            else:
                return move
        elif frm_piece == "p":
            if chess.square_rank(mv_to) == 0:
                return move + 'q'
            else:
                return move
        else:
            return move


    def bot_move(self):
        move = self.build_output()
        checkedmove = self.check_promo(move)
        return checkedmove












#Add in a function which predicts the move and checks if any piece gets taken, if a piece gets taken assign the material score for that piece.
#At the end the moves are ranked based on material score + prediction score
