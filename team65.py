import sys
import random
import signal
import time
import copy

class Team65:
    def __init__(self):
        self.flag = 1
        self.next_move = (0, 0)
        self.maxdepth = 3

    def returnValEval(self, arr):
         return arr[0]**arr[0] - arr[1]**arr[1]

    def returnCount(self, cell, arr):
        if cell == 'x':
            arr[0] += 1
        if cell == 'o':
            arr[1] += 1
        if cell == 'd':
            arr[2] += 1
        if cell == '-':
            arr[3] += 1
        return arr

    def checkRows(self, array):
        val = 0
        for i in range(4):
            arr = [0, 0, 0, 0]
            for j in range(4):
                arr = self.returnCount(array[i][j], arr)
            val += self.returnValEval(arr)
        return val

    def checkColumns(self, array):
        val = 0
        for j in range(4):
            arr = [0, 0, 0, 0]
            for i in range(4):
                arr = self.returnCount(array[i][j], arr)
            val += self.returnValEval(arr)
        return val

    def checkDiamond(self, array):
        val = 0
        for i in range(2):
            for j in range(1, 3):
                arr = [0, 0, 0, 0]
                arr = self.returnCount(array[i][j], arr)
                arr = self.returnCount(array[i + 1][j - 1], arr)
                arr = self.returnCount(array[i + 1][j + 1], arr)
                arr = self.returnCount(array[i + 2][j], arr)
                val += self.returnValEval(arr)
        return val

    def localheuristic(self, board):
        localheuristic = 0
        for i in range(0, 16, 4):
            for j in range(0, 16, 4):
                arr = []
                for x in range(4):
                    temp = []
                    for y in range(4):
                        temp.append(board.board_status[i + x][j + y])
                    arr.append(list(temp))
                localheuristic += self.checkRows(arr) + self.checkColumns(arr) + self.checkDiamond(arr)
        return localheuristic

    def weightedEval(self, board):
        weight = [[6, 4, 4, 6], [4, 3, 3, 4], [4, 3, 3, 4], [6, 4, 4, 6]]
        val = 0
        for i in range(4):
            for j in range(4):
                if board.block_status[i][j] == 'x':
                    val += 100 * weight[i][j]
                if board.block_status[i][j] == 'o':
                    val += -100 * weight[i][j]
        return val

    def countCenter(self, board, opflag):
        count = 0
        for i in range(1, 3):
            for j in range(1, 3):
                if board.block_status[i][j] == opflag:
                    count += 1
        if count >= 2:
            return 1
        else:
            return 0

    def evaluation(self, board, old_move):
        heuristicboard = 0
        heuristicweighted = 0
        #Calculating larger board heuristic
        heuristicboard += self.checkRows(board.block_status) + self.checkColumns(board.block_status) + self.checkDiamond(board.block_status)
        heuristiclocal = self.localheuristic(board)

        if self.countCenter(board, self.numtoflag(1 - self.flag)):
            heuristicweighted = self.weightedEval(board)
        return 2*heuristicboard + heuristiclocal + heuristicweighted

    def flagtonum(self, flag):
        if flag == 'x':
            return 1
        else:
            return 0

    def numtoflag(self, num):
        if num == 1:
            return 'x'
        else:
            return 'o'

    def move(self, board, old_move, flag):
        self.flag = self.flagtonum(flag)
        self.minimax(board, old_move, 0, -999999999, 999999999, True, self.numtoflag(self.flag))
        return (self.next_move[0], self.next_move[1])


    def checkend(self, board, old_move, depth):
        check = board.find_terminal_state()
        if depth == self.maxdepth or check[0] != 'CONTINUE':
            return (1, (self.flag + (self.flag - 1)) * self.evaluation(board, old_move))
        else:
            return (0, 0)

    def minimax(self, board, old_move, depth, alpha, beta, Player, flag):
        ifend = self.checkend(board, old_move, depth)
        if ifend[0] == 1:
            return ifend[1]
        value = Player * -999999999 + (1 - Player) * 999999999
        possibilities = board.find_valid_move_cells(old_move)
        random.shuffle(possibilities)

        for move in possibilities:
            board.update(old_move, move, flag)
            child = self.minimax(board, move, depth + 1, alpha, beta, 1 - Player, self.numtoflag(1 - self.flagtonum(flag)))
            board.board_status[move[0]][move[1]] = '-'
            board.block_status[move[0] / 4][move[1] / 4] = '-'

            if Player:
                if child > value:
                    value = child
                    if depth == 0:
                        self.next_move = copy.deepcopy(move)
                alpha = max(alpha, value)
            else:
                if child < value:
                    value = child
                    if depth == 0:
                        self.next_move = copy.deepcopy(move)
                beta = min(beta, value)
            if beta <= alpha:
                break
        return value
