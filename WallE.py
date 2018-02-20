import sys
import random
import signal
import time
import copy

class WallE:
    def __init__(self):
        self.flag = 1
        self.next_move = (0, 0)


    def gainEstimate(self, countd, countx, counto):
        gain = 0
        if(countx == 4 and countd == 0 and counto == 0):
            gain = 1000
        if(counto == 4 and countd == 0 and countx == 0):
            gain = -1000
        if(countx == 3 and countd == 1 and counto == 0):
            gain = 100
        if(counto == 3 and countd == 1 and countx == 0):
            gain = -100
        if(countx == 2 and countd == 2 and counto == 0):
            gain = 10
        if(counto == 2 and countd == 2 and countx == 0):
            gain = -10
        if(countx == 1 and countd == 3 and counto == 0):
            gain = 1
        if(counto == 1 and countd == 3 and countx == 0):
            gain = -1

        return gain

    def evaluation(self, board, old_move):
        blockx = old_move[0] / 4
        blocky = old_move[1] / 4
        cellx = old_move[0] % 4
        celly = old_move[1] % 4
        block_no = cellx * 4 + celly
        gain = 0

        for i in range(0, 4):
            countx = 0
            counto = 0
            countd = 0
            for j in range(0, 4):
                if board.block_status[i][j] == '-':
                    countd += 1
                elif board.block_status[i][j] == 'o':
                    counto += 1
                elif board.block_status[i][j] == 'x':
                    countx += 1

            if countx == 4:
                gain = 100 * self.gainEstimate(countd, countx, counto)
                return gain
            elif counto == 4:
                gain = 100 * self.gainEstimate(countd, countx, counto)
                return gain
            else:
                gain += 100 * self.gainEstimate(countd, countx, counto)


        for j in range(0, 4):
            countx = 0
            counto = 0
            countd = 0
            for i in range(0, 4):
                if board.block_status[i][j] == '-':
                    countd += 1
                elif board.block_status[i][j] == 'o':
                    counto += 1
                elif board.block_status[i][j] == 'x':
                    countx += 1

            if countx == 4 :
                gain = 100 * self.gainEstimate(countd, countx, counto)
                return gain
            elif counto == 4 :
                gain = 100 * self.gainEstimate(countd, countx, counto)
                return gain
            else:
                gain += 100 * self.gainEstimate(countd, countx, counto)

        countx = 0
        counto = 0
        countd = 0
        for i in range(0, 4):
            if board.block_status[i][i] == '-':
                countd += 1
            elif board.block_status[i][i] == 'o':
                counto += 1
            elif board.block_status[i][i] == 'x':
                countx += 1

        if countx == 4 :
            gain = 100 * self.gainEstimate(countd, countx, counto)
            return gain
        elif counto == 4 :
            gain = 100 * self.gainEstimate(countd, countx, counto)
            return gain
        else :
            gain += 100 * self.gainEstimate(countd, countx, counto)

        countx = 0
        counto = 0
        countd = 0
        for i in range(0, 4):
            if board.block_status[i][3 - i] == '-':
                countd += 1
            elif board.block_status[i][3 - i] == 'o':
                counto += 1
            elif board.block_status[i][3 - i] == 'x':
                countx += 1

        if countx == 4:
            gain = 100 * self.gainEstimate(countd, countx, counto)
            return gain
        elif counto == 4:
            gain = 100 * self.gainEstimate(countd, countx, counto)
            return gain
        else :
            gain += 100 * self.gainEstimate(countd, countx, counto)

        for checkx in range(0, 13, 4):
            for checky in range(0, 13, 4):
                local_gain = 0
                local_flag = 0
                for i in range(0, 4):
                    countx = 0
                    counto = 0
                    countd = 0
                    for j in range(0, 4):
                        if board.board_status[checkx + i][checky + j] == '-':
                            countd += 1
                        elif board.board_status[checkx + i][checky + j] == 'o':
                            counto += 1
                        elif board.board_status[checkx + i][checky + j] == 'x':
                            countx += 1

                    if countx == 4:
                        local_gain = self.gainEstimate(countd, countx, counto)
                        local_flag = 1
                        break
                    elif counto == 4:
                        local_gain = self.gainEstimate(countd, countx, counto)
                        local_flag = 1
                        break
                    else:
                        local_gain += self.gainEstimate(countd, countx, counto)

                    if local_flag == 1:
                        break
                if local_flag == 1:
                    gain += local_gain
                    continue

                for j in range(0, 4):
                    countx = 0
                    counto = 0
                    countd = 0
                    for i in range(0, 4):
                        if board.board_status[checkx + i][checky + j] == '-':
                            countd += 1
                        elif board.board_status[checkx + i][checky + j] == 'o':
                            counto += 1
                        elif board.board_status[checkx + i][checky + j] == 'x':
                            countx += 1

                    if countx == 4 :
                        local_gain = self.gainEstimate(countd, countx, counto)
                        local_flag = 1
                        break
                    elif counto == 4 :
                        local_gain = self.gainEstimate(countd, countx, counto)
                        local_flag = 1
                        break
                    else:
                        local_gain += self.gainEstimate(countd, countx, counto)
                    if local_flag == 1:
                        break
                if local_flag == 1:
                    gain += local_gain
                    continue

                countx = 0
                counto = 0
                countd = 0
                for i in range(0, 4):
                    if board.board_status[checkx + i][checky + i] == '-':
                        countd += 1
                    elif board.board_status[checkx + i][checky + i] == 'o':
                        counto += 1
                    elif board.board_status[checkx + i][checky + i] == 'x':
                        countx += 1

                if countx == 4 :
                    local_gain = self.gainEstimate(countd, countx, counto)
                    local_flag = 1
                elif counto == 4 :
                    local_gain = self.gainEstimate(countd, countx, counto)
                    local_flag = 1
                else :
                    local_gain += self.gainEstimate(countd, countx, counto)

                if local_flag == 1:
                    gain += local_gain
                    continue

                countx = 0
                counto = 0
                countd = 0
                for i in range(0, 4):
                    if board.board_status[checkx + i][checky + 3 - i] == '-':
                        countd += 1
                    elif board.board_status[checkx + i][checky + 3 - i] == 'o':
                        counto += 1
                    elif board.board_status[checkx + i][checky + 3 - i] == 'x':
                        countx += 1

                if countx == 4:
                    local_gain = self.gainEstimate(countd, countx, counto)
                    local_flag = 1
                elif counto == 4:
                    local_gain = self.gainEstimate(countd, countx, counto)
                    local_flag = 1
                else :
                    local_gain += self.gainEstimate(countd, countx, counto)

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
        if depth == 3:
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
