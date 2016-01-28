# ICS32 Project 4 --------- Aaron Ko 20818450

NONE = 0
BLACK = 1
WHITE = 2

class InvalidInputError(Exception):
    pass

def _opp(color: str):
    '''chagnes 1 to 2 and 2 to 1'''
    
    if color == BLACK:
        return WHITE
    if color == WHITE:
        return BLACK
    
def tostring(string):
    '''changes 1 or 2 to B or W'''
    if string == 1:
        return 'B'
    if string == 2:
        return 'W'
    if string == 0:
        return '.'

def toint(integer):
    '''changes B or W to 1 or 2'''
    if integer == 'B':
        return 1
    if integer == 'W':
        return 2

        
class Game:
    def __init__(self, rows, cols, first, topleft, wincon):
        self._rows = rows
        self._cols = cols
        self._first = toint(first)
        self._topleft = toint(topleft)
        self._wincon = wincon

        self._bcnt = 0
        self._wcnt = 0
        self._turn = self._first

        self.board = []

    def bounded(self, x, y):
        '''Check if coordinates falls within the board's boundary'''
        if x >= 0 and x <= self._cols -1 and y>=0 and y<= self._rows -1:
            return True
        else:
            return False

    def ask_move(self):
        '''Asks for move input, returns value in list'''
        move = input()
        move = move.split()
        try:
            move[0] = int(move[0]) - 1
            move[1] = int(move[1]) - 1
        except IndexError:
            raise InvalidInputError
        return move

    def vflip(self, c, r, m):
        '''takes column row and boolean to make move or not/// returns list of pieces that need to be flipped or returns empty list if none.'''
    
        flip = []
        directions = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
        for x,y in directions:
            flip2 = []
            xadj = c+x
            yadj = r+y
            if self.bounded(xadj, yadj) == True:
                if self.board[xadj][yadj] == _opp(self._turn):
                    while self.board[xadj][yadj] == _opp(self._turn):
                        flip2.append([xadj, yadj])
                        xadj += x
                        yadj += y
                        if self.bounded(xadj, yadj)== False:
                            break
                    if self.bounded(xadj, yadj) == False:
                        continue
                    if self.board[xadj][yadj] == self._turn:
                        flip.extend(flip2)
        if len(flip) != 0 and m == True and self.board[c][r] == 0:
            self.board[c][r] = self._turn
        return flip
    
                        
    def flip(self, toflip):
        '''flips the pieces at the points listed in list'''
        for x,y in toflip:
            self.board[x][y] = self._turn
        self._turn = _opp(self._turn)
        

    def create(self):
        '''creates empty board and adds first four pieces based on top left'''
        hcol = int(self._cols/2 - 1)
        hrow = int(self._rows/2 - 1)
        tl = self._topleft
        tr = _opp(tl)
        
        for c in range(self._cols):
            self.board.append([])
            for r in range(self._rows):
                self.board[-1].append(NONE)

        self.board[hcol][hrow] = tl
        self.board[hcol + 1][hrow + 1] = tl
        self.board[hcol + 1][hrow] = tr
        self.board[hcol][hrow + 1] = tr

    def count(self):
        '''count number of black pieces and white pieces'''
        self._bcnt = 0
        self._wcnt = 0
        for c in range(self._cols):
            for r in range(self._rows):
                if self.board[c][r] == BLACK:
                    self._bcnt += 1
                if self.board[c][r] == WHITE:
                    self._wcnt +=1
        
    def printt(self):
        '''prints board'''
        print('B: ' + str(self._bcnt) + '  W: ' + str(self._wcnt))
        for r in range(self._rows):
            line = ''
            for c in range(self._cols):
                line += tostring(self.board[c][r])
            print(line)

    def print_turn(self):
        '''print's who's turn it is'''
        print('TURN: ' + tostring(self._turn))

    def _str_turn(self):
        turn = 'TURN: ' + tostring(self._turn)
        return turn

    def _str_count(self):
        self.count()
        count = 'B: ' + str(self._bcnt) + '   W: ' + str(self._wcnt)
        return count

    def over(self):
        '''checks if all spaces are filled'''
        over = True
        for r in range(self._rows):
            for c in range(self._cols):
                if self.board[c][r] == 0:
                    over = False
        return over

    def winner(self):
        '''calculates winner'''
        if self._wincon == '>':
            b = self._bcnt
            a = self._wcnt
        elif self._wincon == '<':
            b = self._wcnt
            a = self._bcnt
        if b > a:
            print('WINNER: BLACK')
        if b < a:
            print('WINNER: WHITE')
        if b == a:
            print('WINNER: NONE')

    def winner_text(self):
        '''calculates winner'''
        if self._wincon == '>':
            b = self._bcnt
            a = self._wcnt
        elif self._wincon == '<':
            b = self._wcnt
            a = self._bcnt
        if b > a:
            return 'WINNER: BLACK'
        if b < a:
            return 'WINNER: WHITE'
        if b == a:
            return 'WINNER: NONE'

    def check_moves(self):
        '''checks for valid moves'''
        avalid = False
        for cc in range(self._cols):
            for rr in range(self._rows):
                if self.board[cc][rr] == 0:
                    if len(self.vflip(cc,rr, False)) != 0:
                       avalid = True
        if avalid == False:
            self._turn = _opp(self._turn)
        return avalid

    def none_left(self):
        check1 = self.check_moves()
        check2 = self.check_moves()

        if check1 == False and check2 == False:
            return True
        else:
            return False
                
                
