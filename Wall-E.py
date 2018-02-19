class WallE:
	def __init__(self):
        self.symbol = ''
        self.next_move = (0, 0)

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
		self.symbol = flag
		utility = self.minimax(board, old_move, 0, -999999999, 999999999, True, flag)
		return (self.next_move[0], self.next_move[1])

    def minimax_search(self, board, old_move, depth, alpha, beta, Player, flag):
        status = board.find_terminal_state();
		if depth == 3 or status[0] != 'CONTINUE':
			if self.symbol == 'x':
				return self.evaluation(board, old_move)
			else:
				return (0 - self.evaluation(board, old_move))
        value = -1 * Player * 999999999
        valid_moves = board.find_valid_move_cells(old_move)
        random.shuffle(valid_moves)
        for move in valid_moves:
            board.update(old_move, move, flag)
            if flag == 'x':
                next_flag = 'o'
            else
                next_flag = 'x'
            child_value = self.minimax_search(board, move, depth + 1, alpha, beta, 1 - Player, next_flag)
            board.board_status[move[0]][move[1]] = '-';
            board.block_status[move[0] / 4][move[1] / 4] = '-'

            if Player:
                if child_value > value:
					value = child_value
					if depth == 0:
						self.next_move = copy.deepcopy(move)
				alpha = max(alpha, value)
            else:
                if child_value < value:
					value = child_value
					if depth == 0:
						self.next_move = copy.deepcopy(move)
				beta = min(beta, value)
            if beta <= alpha:
                break
            return value
