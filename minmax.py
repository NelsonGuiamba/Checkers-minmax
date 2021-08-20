from copy import deepcopy
from pieces import Dado

class Bot:
    def __init__(self, depth):
        self.depth = depth
        self.change = lambda n: 1 if n == 2 else 2

    def setDepth(self, depth):
        self.depth = depth

    def whoCanMove(self, map, time):
        array = []
        capturePositions = map.someoneCanCapture(time)
        if len(capturePositions) > 0:
            for position in capturePositions:
                array.append((position, self._capture(map, position)))
        else:
            for position in map._pieceTeams[time]:
                possibilitys = []
                if isinstance(map._map[position], Dado):
                    arr = map._map[position].possibilitys()
                    for moveTo in arr:
                        if map._map[moveTo] == 0:
                            possibilitys.append(map._posToStr(moveTo))

                else:
                    arr = map._map[position].possibilitys(map._map)
                    for moveArr in arr:
                        for moveTo in moveArr:
                            if len(moveTo) == 0:
                                continue
                            if map._map[moveTo] == 0:
                                possibilitys.append(map._posToStr(moveTo))

                if len(possibilitys) > 0:
                    array.append((position, possibilitys))
        return array

    def points(self, map):
        def ev(part): return 1 if isinstance(part, Dado) else 3
        return sum([ev(map._map[pos]) for pos in map._pieceTeams[2]]) -\
            sum([ev(map._map[pos]) for pos in map._pieceTeams[1]])

    def play(self, board, player):
        return self._minimax(board, 0, player)

    def _minimax(self, board, depth, player, bestPos=None):
        if depth == self.depth:
            return self.points(board), bestPos

        if board.gameover(1):
            board.print()
            return -999, bestPos

        if board.gameover(2):
            board.print()
            return 999, bestPos

        if player == 1:
            minEval = float('inf')
            bestMove = None
            for dado, moveTo in self.whoCanMove(board, player):
                if moveTo[0] == '':
                    board.print()
                    input(board._posToStr(dado))
                for move in moveTo:
                    if move is None or dado is None:
                        continue
                    tempBoard = deepcopy(board)
                    tempBoard.move(board._posToStr(dado), move, True)
                    evaluation = self._minimax(
                        tempBoard, depth+1, self.change(player))
                    minEval = min(minEval, evaluation[0])
                    if minEval == evaluation[0]:
                        bestMove = (dado, move)
            return minEval, bestMove

        elif player == 2:
            bestMove = None
            maxEval = float('-inf')
            for dado, moveTo in self.whoCanMove(board, player):
                for move in moveTo:
                    if move is None:
                        continue
                    tempBoard = deepcopy(board)
                    tempBoard.move(board._posToStr(dado), move, True)
                    evaluation = self._minimax(
                        tempBoard, depth+1, self.change(player), (dado, move))
                    maxEval = max(maxEval, evaluation[0])
                    if maxEval == evaluation[0]:
                        bestMove = (dado, move)
            return maxEval, bestMove

    def __capture(self, board, pos, string, lista,
                  piece, prev=None, capturedPieces=[]):
        def change(i):
            if i == 0:
                return 3
            if i == 3:
                return 0
            if i == 2:
                return 1
            else:
                return 2

        def helper(string, strToPos):
            if len(string) < 2:
                return ()
            i = 0
            while True:
                if i == 0:
                    p = string[0:2]
                    yield strToPos(p)
                elif i*2 > len(string) - 1:
                    break
                else:
                    p = string[i*2:i*2+2]
                    yield strToPos(p)
                i += 1
        piece.update(pos)
        est = False
        if isinstance(piece, Dado):
            for p in piece.possibilitys():

                if p in helper(string, board._strToPos):
                    continue
                if board._map[p] != 0 and board._map[p]._team != piece._team:
                    ok, array = piece.capture(*p)
                    if ok:
                        if board._map[array] == 0:
                            est = True
                            self.__capture(
                                board, array, string+board._posToStr(p), lista, piece)
                            piece.update(pos)

            for p in piece.backward(board._map):
                if p in helper(string, board._strToPos):
                    continue
                if board._map[p] != 0 and board._map[p]._team != piece._team:
                    ok, array = piece.backCapture(*p)
                    if ok:
                        if board._map[array] == 0:
                            est = True
                            self.__capture(
                                board, array, string+board._posToStr(p), lista, piece)
            if not est:
                if string not in lista:
                    lista.append(string)
                string = ''
        else:
            for pindex, positions in enumerate(piece.possibilitys(board._map)):
                if prev and prev == pindex:
                    continue
                for index in range(len(positions)):
                    if positions[index] in capturedPieces:
                        continue
                    if board._map[positions[index]] != 0:
                        for recur in range(index+1, len(positions)):
                            if board._map[positions[recur]] != 0:
                                continue
                            est = True
                            capturedPieces.append(positions[index])
                            self.__capture(
                                board, positions[recur],
                                string + board._posToStr(positions[recur]),
                                lista, piece, change(pindex),
                                capturedPieces)
                            capturedPieces.pop()
            if not est:
                if string not in lista:
                    lista.append(string)
                string = ''
        return lista

    def _maxCapture(self, array):
        maxPosition, maxLen = 0, len(array[0])
        maxPositions = [array[0]]
        for p in range(1, len(array)):
            if len(array[p]) == maxLen:
                maxPositions.append(array[p])

            if len(array[p]) > maxLen:
                maxLen = len(array[p])
                maxPosition = p
                maxPositions = [array[p]]
        return maxPositions

    def _capture(self, board, pos):
        tmp = board._map[pos]
        board._map[pos] = 0
        l = self.__capture(board, pos, '', [], tmp)
        tmp.update(pos)
        board._map[pos] = tmp
        return l
