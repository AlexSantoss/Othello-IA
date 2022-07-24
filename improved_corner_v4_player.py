import numpy as np
import math

class ImprovedCornerV4Player:
    def __init__(self, color):
        lista = [ 900,-100,  25,  25
                     ,-100, -50, -50
                          ,  50,  50
                               ,  50]
        self.board_scores = np.zeros((8,8))
        for x, y, s in zip(*np.triu_indices(4), lista):
            x_idx, y_idx = [x, y, 7-x,   y,   x, 7-y, 7-x, 7-y], [y, x,   y, 7-x, 7-y,   x, 7-y, 7-x]
            self.board_scores[x_idx, y_idx] = s
        self.color = color
        self.opponent = 'o' if color == '@' else '@'
        
        self.me_idx = 0 if color == 'o' else 1
        self.opponent_idx = 0 if color == '@' else 1

    def play(self, board):
        return self.minmax(board, 3)

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

    def minmax(self, board, profundidade):
        best_moves = [None]*(profundidade+1)
        scores = [-math.inf if i%2 == 0 else math.inf for i in range(profundidade+1)]

        stack = [(board, self.color, 0, 0, None)]
        opponent = lambda p: 'o' if p == '@' else '@'

        while len(stack) != 0:
            board, player, prof, no_moves, o = stack.pop()
            if prof == profundidade or no_moves == 2:
                avaliacao = self.heuristica(board)
                for i in range(prof, -1, -1):
                    if (i%2 == 0 and scores[i] <= avaliacao) or (i%2 == 1 and scores[i] >= avaliacao):
                        scores[i] = avaliacao
                        best_moves[i] = o
                    else: break
                continue
            
            moves = board.valid_moves(player)
            if len(moves) == 0:
                stack.append( (board, opponent(player), prof+1, no_moves+1, o) )
                continue
            
            for m in moves:
                b_clone = board.get_clone()
                b_clone.play(m, player)
                origin = m if prof == 0 else o
                stack.append( (b_clone, opponent(player), prof+1, 0, origin) )

        print(best_moves, scores)
        return best_moves[0]
