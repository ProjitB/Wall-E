import sys
import random
import signal
import time
import copy

class WallE:
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

    def evaluation(self, board, old_move):
        heuristicboard = 0
        #Calculating larger board heuristic
        heuristicboard += self.checkRows(board.block_status) + self.checkColumns(board.block_status) + self.checkDiamond(board.block_status)
        return heuristicboard



    def gainEstimate(self, d, x, o):
        gain = 0
        if(x == 4 and d == 0 and o == 0):
            gain = 1000
        if(o == 4 and d == 0 and x == 0):
            gain = -1000
        if(x == 3 and d == 1 and o == 0):
            gain = 100
        if(o == 3 and d == 1 and x == 0):
            gain = -100
        if(x == 2 and d == 2 and o == 0):
            gain = 10
        if(o == 2 and d == 2 and x == 0):
            gain = -10
        if(x == 1 and d == 3 and o == 0):
            gain = 1
        if(o == 1 and d == 3 and x == 0):
            gain = -1

        return gain

    def evaluation1(self, board, old_move):
        blockx = old_move[0] / 4
        blocky = old_move[1] / 4
        cellx = old_move[0] % 4
        celly = old_move[1] % 4
        block_no = cellx * 4 + celly
        gain = 0

        for i in range(4):
            x = 0
            o = 0
            d = 0
            for j in range(4):
                if board.block_status[i][j] == '-':
                    d += 1
                elif board.block_status[i][j] == 'o':
                    o += 1
                elif board.block_status[i][j] == 'x':
                    x += 1

            if x == 4:
                gain = 100 * self.gainEstimate(d, x, o)
                return gain
            elif o == 4:
                gain = 100 * self.gainEstimate(d, x, o)
                return gain
            else:
                gain += 100 * self.gainEstimate(d, x, o)


        for j in range(0, 4):
            x = 0
            o = 0
            d = 0
            for i in range(0, 4):
                if board.block_status[i][j] == '-':
                    d += 1
                elif board.block_status[i][j] == 'o':
                    o += 1
                elif board.block_status[i][j] == 'x':
                    x += 1

            if x == 4 :
                gain = 100 * self.gainEstimate(d, x, o)
                return gain
            elif o == 4 :
                gain = 100 * self.gainEstimate(d, x, o)
                return gain
            else:
                gain += 100 * self.gainEstimate(d, x, o)

        x = 0
        o = 0
        d = 0
        for i in range(0, 4):
            if board.block_status[i][i] == '-':
                d += 1
            elif board.block_status[i][i] == 'o':
                o += 1
            elif board.block_status[i][i] == 'x':
                x += 1

        if x == 4 :
            gain = 100 * self.gainEstimate(d, x, o)
            return gain
        elif o == 4 :
            gain = 100 * self.gainEstimate(d, x, o)
            return gain
        else :
            gain += 100 * self.gainEstimate(d, x, o)

        x = 0
        o = 0
        d = 0
        for i in range(0, 4):
            if board.block_status[i][3 - i] == '-':
                d += 1
            elif board.block_status[i][3 - i] == 'o':
                o += 1
            elif board.block_status[i][3 - i] == 'x':
                x += 1

        if x == 4:
            gain = 100 * self.gainEstimate(d, x, o)
            return gain
        elif o == 4:
            gain = 100 * self.gainEstimate(d, x, o)
            return gain
        else :
            gain += 100 * self.gainEstimate(d, x, o)

        for checkx in range(0, 13, 4):
            for checky in range(0, 13, 4):
                local_gain = 0
                local_flag = 0
                for i in range(0, 4):
                    x = 0
                    o = 0
                    d = 0
                    for j in range(0, 4):
                        if board.board_status[checkx + i][checky + j] == '-':
                            d += 1
                        elif board.board_status[checkx + i][checky + j] == 'o':
                            o += 1
                        elif board.board_status[checkx + i][checky + j] == 'x':
                            x += 1

                    if x == 4:
                        local_gain = self.gainEstimate(d, x, o)
                        local_flag = 1
                        break
                    elif o == 4:
                        local_gain = self.gainEstimate(d, x, o)
                        local_flag = 1
                        break
                    else:
                        local_gain += self.gainEstimate(d, x, o)

                    if local_flag == 1:
                        break
                if local_flag == 1:
                    gain += local_gain
                    continue

                for j in range(0, 4):
                    x = 0
                    o = 0
                    d = 0
                    for i in range(0, 4):
                        if board.board_status[checkx + i][checky + j] == '-':
                            d += 1
                        elif board.board_status[checkx + i][checky + j] == 'o':
                            o += 1
                        elif board.board_status[checkx + i][checky + j] == 'x':
                            x += 1

                    if x == 4 :
                        local_gain = self.gainEstimate(d, x, o)
                        local_flag = 1
                        break
                    elif o == 4 :
                        local_gain = self.gainEstimate(d, x, o)
                        local_flag = 1
                        break
                    else:
                        local_gain += self.gainEstimate(d, x, o)
                    if local_flag == 1:
                        break
                if local_flag == 1:
                    gain += local_gain
                    continue

                x = 0
                o = 0
                d = 0
                for i in range(0, 4):
                    if board.board_status[checkx + i][checky + i] == '-':
                        d += 1
                    elif board.board_status[checkx + i][checky + i] == 'o':
                        o += 1
                    elif board.board_status[checkx + i][checky + i] == 'x':
                        x += 1

                if x == 4 :
                    local_gain = self.gainEstimate(d, x, o)
                    local_flag = 1
                elif o == 4 :
                    local_gain = self.gainEstimate(d, x, o)
                    local_flag = 1
                else :
                    local_gain += self.gainEstimate(d, x, o)

                if local_flag == 1:
                    gain += local_gain
                    continue

                x = 0
                o = 0
                d = 0
                for i in range(0, 4):
                    if board.board_status[checkx + i][checky + 3 - i] == '-':
                        d += 1
                    elif board.board_status[checkx + i][checky + 3 - i] == 'o':
                        o += 1
                    elif board.board_status[checkx + i][checky + 3 - i] == 'x':
                        x += 1

                if x == 4:
                    local_gain = self.gainEstimate(d, x, o)
                    local_flag = 1
                elif o == 4:
                    local_gain = self.gainEstimate(d, x, o)
                    local_flag = 1
                else :
                    local_gain += self.gainEstimate(d, x, o)

                gain += local_gain

        return gain

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
