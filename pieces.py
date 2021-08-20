class Dado:
    def __init__(self, x, y, team):
        self._x = x
        self._y = y
        self._addx = 1 if team == 2 else -1
        self._team = team

    def possibilitys(self):
        array = []
        if 0 <= self._x + self._addx < 8:
            if self._y + 1 < 8:
                array.append((self._x+self._addx, self._y+1))
            if self._y - 1 >= 0:
                array.append((self._x+self._addx, self._y-1))
        return array

    def backward(self, map):
        array = []
        if 0 <= self._x - self._addx < 8:
            if self._y + 1 < 8:
                if map[self._x-self._addx][self._y+1] != 0 and \
                        map[self._x-self._addx][self._y+1]._team != self._team:
                    array.append((self._x-self._addx, self._y+1))
            if self._y - 1 >= 0:
                if map[self._x-self._addx][self._y-1] != 0 and \
                        map[self._x-self._addx][self._y-1]._team != self._team:
                    array.append((self._x-self._addx, self._y-1))

        #print(f'{self._x} {self._y} = {array}')
        return array

    def capture(self, x, y):
        if 0 <= y + (y-self._y) < 8:
            if 0 <= x + self._addx < 8:
                return (True, (x+self._addx, y+(y-self._y)))
        return (False, None)

    def backCapture(self, x, y):
        if 0 <= y + (y-self._y) < 8:
            if 0 <= x - self._addx < 8:
                return (True, (x-self._addx, y+(y-self._y)))
        return (False, None)

    def update(self, pos):
        self._x = pos[0]
        self._y = pos[1]


class Queen:
    def __init__(self, x, y, team):
        self._x = x
        self._y = y
        self._addx = 1 if team == 2 else -1
        self._team = team

    def possibilitys(self, map):
        def helper(addx, addy, map):
            s = []
            x = self._x
            y = self._y
            while True:
                x += addx
                y += addy
                if 0 <= x < 8 and 0 <= y < 8:
                    if map[x][y] != 0:
                        if map[x][y]._team == self._team:
                            return s
                        x += addx
                        y += addy
                        if 0 <= x < 8 and 0 <= y < 8:
                            if map[x][y] == 0:
                                s.append((x-addx, y-addy))
                            else:
                                return s
                        x -= addx
                        y -= addy
                    else:
                        s.append((x, y))
                else:
                    return s

        array = []
        for addx in (1, -1):
            for addy in (1, -1):
                array.append(helper(addx, addy, map))

        return array

    def update(self, pos):
        self._x = pos[0]
        self._y = pos[1]
