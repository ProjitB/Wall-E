class WallE:
	def __init__(self):
		pass
	def move(self, board, old_move, flag):
        # Steps:
        #  1. Using board.find_valid_move_cells(self, old_move) we acquire the possible next moves.
        #     These are the possible next moves that would change the state of the board correctly.
        #     Our next move must be one of these. Worst case randomly select.
        #
        #  2. For each of the =next moves= compute their heuristic value.
        #     This is used to determine the cost of doing the next move. However minimax implementation
        #     is what helps us decide what may be the best move after lets say 3 moves.
        #     Thus heuristic value at each point is still important, but the aim then is to maximize the
        #     heuristic value after n moves.
        #
        #  3. We expand the game tree by looking at the next(2nd) moves for each of the next moves(1st).
        #     To decrease the size of the search space, we use various functions(not alpha beta) which
        #     help determine the likelihood of a win by following a certain path
        #
        #  4. Once we have created the game tree, we apply minimax and alpha beta pruning. Minimax itself
        #     is a brute force search of the tree. Alpha beta pruning helps decrease the number of nodes that
        #     need to be evaluated.


		return (int(mvp[0]), int(mvp[1]))
