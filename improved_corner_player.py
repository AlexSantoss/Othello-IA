class ImprovedCornerPlayer:
    def __init__(self, color):
        self.color = color
        self.board_scores =  [
                [ 9,  1,  8,  6],
                [ 1,  0,  3,  2],
                [ 8,  3,  7,  5],
                [ 6,  2,  5,  4],
            ]

    def play(self, board):
        return self.getBestPlay(board.valid_moves(self.color))

    def getBestPlay(self, moves):
        import math
        maxScore = -math.inf
        retMove = None

        for move in moves:
            xsp = 8-move.x if move.x > 4 else move.x-1
            ysp = 8-move.y if move.y > 4 else move.y-1

            score = self.board_scores[xsp][ysp]
            if score > maxScore:
                maxScore = score
                retMove = move

        return retMove
