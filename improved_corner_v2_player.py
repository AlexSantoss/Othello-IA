import numpy as np
import math

class ImprovedCornerV2Player:
    def __init__(self, color):
        lista = [ 6, 1, 5, 5
                   , 0, 2, 2
                      , 3, 3
                         , 4 ]
        self.board_scores = np.zeros((8,8))
        for x, y, s in zip(*np.triu_indices(4), lista):
            x_idx, y_idx = [x, y, 7-x,   y,   x, 7-y, 7-x, 7-y], [y, x,   y, 7-x, 7-y,   x, 7-y, 7-x]
            self.board_scores[x_idx, y_idx] = s
        self.color = color

        self.opponent = 'o' if color == '@' else '@'
        self.opponent_idx = 0 if color == '@' else 1

    def play(self, board):
        
        scores = [ (self.getScore(m), m) for m in board.valid_moves(self.color) ]
        maxScore = max(scores, key=lambda x: x[0])[0]
        filterMax = [m for s, m in scores if s == maxScore]

        nextMoves = [(self.testPlay(board.get_clone(), m), m) for m in filterMax]
        minMoves = min(nextMoves, key=lambda x: x[0])[0]
        filterMoves = [m for s, m in nextMoves if s == minMoves]
        return filterMoves[0]

    def getScore(self, move):
        score = self.board_scores[move.x-1][move.y-1]
        return score

    def testPlay(self, board, move):
        board.play(move, self.color)
        return len(board.valid_moves(self.opponent))

    def lowerScore(self, board, move):
        score = board.get_scores()
        board.play(move, self.color)
        return score[self.opponent_idx] - board.get_scores[self.opponent_idx]
