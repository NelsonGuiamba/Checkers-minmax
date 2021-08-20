from board import GameCore
from minmax import Bot


def printError(string): return print('\033[1;31mError : '+string+'\033[m')


def banner(string):
    print('='*40)
    print(f'{string:^40}')
    print('='*40)


def menu(array):
    banner('Menu')
    print('1 - Set dificulty\n2 - Start new game \n\
3 - See bot vs bot\n4 - exit')
    array[readInt(5)-1]()


def readInt(limit,  string='Your option: '):
    while True:
        op = input(string)[0]
        if op.isdigit():
            if 0 < int(op) < limit:
                return int(op)
            else:
                printError('Invalid option')
        else:
            printError('Integer invalid')


def readString(string, isvalid, limit):
    while True:
        string = input(string).upper()[:limit]
        if isvalid(string):
            return string


def setDificulty():
    banner('Choose dificulty')
    print('1 - easy\n2 - medium\n3 - difficult\n\
4 - very difficult')
    num = readInt(5) - 1
    bot.setDepth((2, 3, 6, 8)[num])


def newGame():

    def move(player):
        pieceAndMove = bot.whoCanMove(board, player)
        i = 1
        if len(pieceAndMove) > 1:
            while True:
                print('Choose a piece')
                for dado, _ in pieceAndMove:
                    print(f'\t{i} {board._posToStr(dado)}', end='\t')
                    if i % 2 == 0:
                        print()
                    i += 1
                print()
                piece = readInt(i)-1
                string = readString(
                    f'Confirm {board._posToStr(pieceAndMove[piece][0])} [Y/N]:',
                    lambda st: st in 'YN', 1)
                if string == 'Y':
                    break
                i = 1
        else:
            piece = 0
            print(
                f'Choosing piece {board._posToStr(pieceAndMove[0][0])} automatically')

        if len(pieceAndMove[piece][1]) > 1:
            print(f'Move piece {board._posToStr(pieceAndMove[piece][0])} to ')
            while True:
                i = 1
                for moveTo in pieceAndMove[piece][1]:
                    print(f'\t{i}) {moveTo}', end='\t')
                    if i % 2 == 0:
                        print()
                    i += 1

                print()
                moveTo = pieceAndMove[piece][1][readInt(i)-1]
                string = readString(
                    f'Confirm move {board._posToStr(pieceAndMove[piece][0])}\
 to ' +
                    moveTo +
                    '[Y/N]:',
                    lambda st: st in 'YN',
                    1)
                if string == 'Y':
                    break
                i = 1
        else:
            moveTo = pieceAndMove[piece][1][0]
            input(f'Moving piece {board._posToStr(pieceAndMove[piece][0])} \
to {pieceAndMove[piece][1][0]} automatically')
        board.move(board._posToStr(pieceAndMove[piece][0]), moveTo, True)

    banner('New game')
    print('1 - play as red (first player) \n2 - play as green (second player))')
    player = readInt(3)
    enemy = 2 if player == 1 else 1
    totalMoves = 0
    while True:
        totalMoves += 1
        if player == 1:
            board.print()
            print('Your turn')
            move(player)
            board.print()
            if board.gameover(1):
                print('\033[32mVoce ganhou!!\033[m')
                return
            botMove = bot.play(board, enemy)[1]
            board.move(board._posToStr(botMove[0]), botMove[1], True)
            if board.gameover(enemy):
                board.print()
                print('\033[31mComputador venceu \033[m')
                return
        else:
            botMove = bot.play(board, enemy)[1]
            board.move(board._posToStr(botMove[0]), botMove[1], True)
            board.print()
            if board.gameover(enemy):
                print('\033[31mComputador venceu \033[m')
                return
            print('Your  turn')
            move(player)
            board.print()
            if board.gameover(1):
                print('\033[32mVoce ganhou!!\033[m')
                return
        if totalMoves == 40:
            s = readString(
                'End the game as draw',
                lambda st: len(st) > 0 and st[0] in 'YN',
                1)
            if s == 'Y':
                print('Game ended in draw')
                return
            totalMoves = 30


def botvsbot():
    d1 = readInt(5, 'Select bot (red) level [1-4] ') - 1
    d2 = readInt(5, 'Select bot (green) level [1-4] ') - 1
    b1 = Bot((2, 3, 6, 8)[d1])
    b2 = Bot((2, 3, 6, 8)[d2])
    board = GameCore()
    totalMoves = 0
    board.print()
    while True:
        totalMoves += 1
        botMove = b1.play(board, 1)[1]
        print('Red\'s turn')
        board.move(board._posToStr(botMove[0]), botMove[1], True)
        board.print()
        if board.gameover(1):
            print('red wins')
            return
        botMove = b2.play(board, 2)[1]
        print('Green\'s turn')
        board.move(board._posToStr(botMove[0]), botMove[1], True)
        board.print()
        if board.gameover(2):
            print('green wins')
            return
        if totalMoves == 30:
            print('Game ended in draw')
            return

def exit():
    print('Bye')
    from sys import exit
    exit(1)


if __name__ == '__main__':
    banner('Checkers')
    bot = Bot(2)
    board = GameCore()
    setDificulty()
    while True:
        menu((setDificulty, newGame, botvsbot, exit))
        board = GameCore()
