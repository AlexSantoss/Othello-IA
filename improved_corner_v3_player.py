import numpy as np
import math

class ImprovedCornerV3Player:
    def __init__(self, color):
        lista = [900,-20, 20, 20
                    ,-20,-10,-10
                        , 10, 10
                            ,  0]
        self.board_scores = np.zeros((8,8))
        for x, y, s in zip(*np.triu_indices(4), lista):
            x_idx, y_idx = [x, y, 7-x,   y,   x, 7-y, 7-x, 7-y], [y, x,   y, 7-x, 7-y,   x, 7-y, 7-x]
            self.board_scores[x_idx, y_idx] = s
        self.color = color
        self.opponent = 'o' if color == '@' else '@'
        
        self.me_idx = 0 if color == 'o' else 1
        self.opponent_idx = 0 if color == '@' else 1

    def play(self, board):
        vms = board.valid_moves(self.color)
        if len(vms) == 1: return vms[0]
        return self.minmax_alfabeta(board, self.color, -math.inf, +math.inf, 3)[1]

    def heuristica(self, board):
        if len(board.valid_moves(self.color)) == 0 and len(board.valid_moves(self.opponent)) == 0:
            board_score = board.score()
            score_diff = board_score[self.me_idx] - board_score[self.opponent_idx]
            return math.inf if score_diff > 0 else -math.inf

        score = 0
        for i in range(8):
            for j in range(8):
                c = board.get_square_color(i, j)
                if c == self.color: score += self.board_scores[i][j]

        return score

    def minmax_alfabeta(self, board, player, alfa, beta, profundidade, no_moves=0):
        if profundidade == 0 or no_moves == 2:
            return self.heuristica(board), None

        if player == self.color:
            moves = board.valid_moves(player)
            if len(moves) == 0:
                return self.minmax_alfabeta(board, self.opponent, alfa, beta, profundidade-1, no_moves=no_moves+1)

            score = -math.inf
            best_move = None
            for m in moves:
                b_clone = board.get_clone()
                b_clone.play(m, player)
                m_score = self.minmax_alfabeta(b_clone, self.opponent, alfa, beta, profundidade-1)[0]

                if m_score >= score:
                    score = m_score
                    best_move = m

                if m_score >= beta: break
            alfa = max(score, alfa)
            return score, best_move

        else:
            moves = board.valid_moves(player)
            if len(moves) == 0:
                return self.minmax_alfabeta(board, self.color, alfa, beta, profundidade-1, no_moves=no_moves+1)

            score = math.inf
            worst_move = None
            for m in moves:
                b_clone = board.get_clone()
                b_clone.play(m, player)
                m_score = self.minmax_alfabeta(b_clone, self.color, alfa, beta, profundidade-1)[0]

                if m_score <= score:
                    score = m_score
                    worst_move = m

                if m_score <= alfa: break
            beta = min(score, alfa)
            return score, worst_move
