from pieces import Dado, Queen
from exceptions import NonEmpty, MovementInvalid, BlankPosition


class Board:
    def __init__(self):
        self._data = []

    def __getitem__(self, pos):
        if isinstance(pos, int):
            return self._data[pos]
        elif isinstance(pos, (tuple, list)):
            return self._data[pos[0]][pos[1]]

    def append(self, element):
        self._data.append(element)

    def __setitem__(self, pos, element):
        if isinstance(pos, int):
            self._data[pos] = element
        elif isinstance(pos, (tuple, list)):
            self._data[pos[0]][pos[1]] = element
        else:
            raise TypeError(type(pos))

    def __len__(self): return len(self._data)


class GameCore:
    def __init__(self):
        self._map = Board()
        self._pieceTeams = {1: set(), 2: set()}
        self._promove = {1: 0, 2: 7}
        self._strToPos = lambda pos: (8-(int(pos[1])), ord(pos[0])-65)
        self._posToStr = lambda pos: f'{chr(pos[1]+65)}{8-pos[0]}'
        self.cor = {'del': '\033[m', 'wi': '\033[31m', 'bl': '\033[32m'}
        for posx in range(8):
            if posx <= 2:
                self._map.append(self.getl(2, st=posx))
            elif posx <= 4:
                self._map.append(self.getl(0, st=posx))
            else:
                self._map.append(self.getl(1, st=posx))

    def getl(self, vez, st):
        if vez == 0:
            return [0 for i in range(8)]
        else:
            l = []
            for i in range(8):
                if not (i+(st % 2)) % 2 == 0:
                    self._pieceTeams[vez].add((st, i))
                    l.append(Dado(st, i, vez))
                else:
                    l.append(0)
            return l

    def print(self):
        print('{:^50}'.format('='*35))
        i = 8
        for l in self._map:
            print(i, end='\t')
            for piece in l:
                if piece == 0:
                    print('_', end=' ')
                else:
                    if isinstance(piece, Queen):
                        print(self.todado(piece._team, 'Q'), end=' ')
                    else:
                        print(self.todado(piece._team, '0'), end=' ')
            print()
            i -= 1
        print('\tA B C D E F G H')

    def todado(self, i, val='0'):
        if i == 1:
            return f'{self.cor["wi"]}{val}{self.cor["del"]}'
        else:
            return f'{self.cor["bl"]}{val}{self.cor["del"]}'

    def move(self, pos, to, fast=False, return_=False, canPromove=True):
        if fast:
            return self.__fastMove(pos, to)

        pos = self._strToPos(pos)
        to = self._strToPos(to)
        if self._map[pos] != 0:
            if isinstance(self._map[pos], Queen):
                return self._moveQueen(pos, to, return_)
            if to in self._map[pos].possibilitys():
                if self._map[to] == 0:
                    self.__updateDict(pos, to)
                    temp = self._map[pos]
                    self._map[pos] = 0
                    if to[0] == self._promove[temp._team] and canPromove:
                        self._map[to] = Queen(*to, temp._team)
                        if return_:
                            return to
                        return
                    temp.update(to)
                    self._map[to] = temp
                    if return_:
                        return to

                elif self._map[to]._team != self._map[pos]._team:
                    # Captura
                    ok, array = self._map[pos].capture(*to)
                    if ok:
                        if self._map[array] == 0:
                            self.__updateDict(pos, array)
                            self.__updateDict(to)
                            temp = self._map[pos]
                            self._map[pos] = 0
                            self._map[to] = 0
                            if array[0] == self._promove[temp._team] \
                                    and canPromove:
                                self._map[array] = Queen(*array, temp._team)
                                if return_:
                                    return to
                                return
                            temp.update(array)
                            self._map[array] = temp
                            if return_:
                                return array

                else:
                    raise NonEmpty('Moving to non-empty place')

            elif to in self._map[pos].backward(self._map):
                ok, array = self._map[pos].backCapture(*to)
                if ok:
                    if self._map[array] == 0:
                        self.__updateDict(pos, array)
                        self.__updateDict(to)
                        temp = self._map[pos]
                        self._map[pos] = 0
                        self._map[to] = 0
                        temp.update(array)
                        self._map[array] = temp
                        if return_:
                            return array
            else:
                raise MovementInvalid()
        else:
            raise BlankPosition(f'position {self._posToStr(pos)}')

    def __fastMove(self, pos, to):
        i = 0
        while True:
            if i == 0:
                p = to[0:2]
                pos = self._posToStr(
                    self.move(
                        pos,
                        p,
                        return_=True,
                        canPromove=i *
                        2 +
                        2 +
                        1 > len(to) -
                        1))
            elif i*2 > len(to) - 1:
                break
            else:
                p = to[i*2:i*2+2]
                pos = self._posToStr(
                    self.move(
                        pos,
                        p,
                        return_=True,
                        canPromove=i *
                        2 +
                        2 +
                        1 > len(to) -
                        1))
            i += 1

    def someoneCanCapture(self, team):
        def helper(pos):
            if not pos[0]:
                return False
            return any(True for posi in pos if self._map[posi] == 0)
        array = []
        for i, j in self._pieceTeams[team]:
            if self._canCapture((i, j)):
                array.append((i, j))
        return array

    def _canCapture(self, pos, est=False):
        def helper(pos):
            if not pos[0]:
                return False
            return any(True for posi in pos if self._map[posi] == 0)
        i, j = pos
        team = self._map[i][j]._team
        array = []
        if not isinstance(self._map[i][j], Dado):
            possibility = self._map[i][j].possibilitys(self._map)
            for position in possibility:
                for index in range(len(position)-1, -1, -1):
                    pos = position[index]
                    if self._map[pos] != 0 and self._map[pos]._team != \
                            self._map[i][j]:
                        if est:
                            array.append(self._posToStr(position[index+1]))
                            break
                        else:
                            return True
        else:
            possibility = self._map[i][j].possibilitys()
            for posi in self._map[i][j].possibilitys():
                if self._map[posi] != 0:
                    if self._map[posi]._team != team:
                        if helper(self._map[i][j].capture(*posi)):
                            if est:
                                array.append(self._posToStr(posi))
                            else:
                                return True
            for posi in self._map[i][j].backward(self._map):
                if self._map[posi] != 0:
                    if self._map[posi]._team != team:
                        if helper(self._map[i][j].backCapture(*posi)):
                            if est:
                                array.append(self._posToStr(posi))
                            else:
                                return True

        if est:
            return (len(array) != 0, array)
        return False

    def __updateDict(self, pos, to=None):
        for time in self._pieceTeams.values():
            if pos in time:
                time.remove(pos)
                if to is not None:
                    time.add(to)

    def gameover(self, turn):
        enemy = 2 if turn == 1 else 1
        if len(self._pieceTeams[enemy]) == 0:
            return True  # winning (turn) eat all enemy pieces

        if len(self.someoneCanCapture(enemy)) == 0:
            for pos in self._pieceTeams[enemy]:
                possibility = self._map[pos].possibilitys() if isinstance(
                    self._map[pos], Dado) else \
                    self._map[pos].possibilitys(self._map)
                if isinstance(self._map[pos], Dado):
                    for moveTo in possibility:
                        if self._map[moveTo] == 0:
                            return False  # not winning enemy can move
                else:
                    for positions in possibility:
                        for moveTo in positions:
                            if self._map[moveTo] == 0:
                                return False
            return True
        else:
            return False  # not winning enemy can capture

    def create(self, lista):
        self._pieceTeams = {1: set(), 2: set()}
        for i in range(len(lista)):
            for j in range(len(lista[i])):
                if lista[i][j] != 0:
                    aux = lista[i][j]
                    print('add', aux)
                    if lista[i][j] < 0:
                        lista[i][j] = Queen(i, j, aux*-1)
                        self._pieceTeams[aux*-1].add((i, j))
                    else:
                        lista[i][j] = Dado(i, j, aux)
                        self._pieceTeams[aux].add((i, j))
        self._map._data = lista

    def _moveQueen(self, pos, to, return_=False):
        if self._map[to] == 0:
            for positions in self._map[pos].possibilitys(self._map):
                if to in positions:
                    if self._map[to] == 0:
                        for position in positions:
                            self._map[position] = 0
                            self.__updateDict(position)
                        self.__updateDict(pos, to)
                        tmp = self._map[pos]
                        self._map[pos] = 0
                        tmp.update(to)
                        self._map[to] = tmp
                        if return_:
                            return to
                        return None

            raise MovementInvalid(
                f'{self._posToStr(pos)} moving to {self._posToStr(to)}')
        raise NonEmpty()
