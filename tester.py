import chess

board = chess.Board()

print(bool(board.castling_rights))
moveparsed = chess.Move.from_uci('e2e3')
board.push(moveparsed)
moveparsed = chess.Move.from_uci('f1e2')
board.push(moveparsed)
moveparsed = chess.Move.from_uci('g1f3')
board.push(moveparsed)

print(board.has_castling_rights(chess.WHITE))
moveparsed = chess.Move.from_uci('e1f1')
board.push(moveparsed)
print(board)
print(board.has_castling_rights(chess.WHITE))
