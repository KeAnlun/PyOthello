#Aaron Ko 20818450

from Logic import Game
import tkinter

class gui:
    def __init__(self):
        
        self._root_window = tkinter.Tk()
        self._root_window.title('Reversi - Aaron Ko')

        self._canvas = tkinter.Canvas(
            master = self._root_window, width = 600, height = 600,
            background = '#ffb503')

        self._canvas.grid(
            row = 1, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self._box = tkinter.Entry(master = self._root_window, font = ('Arial Black', '14'))
        self._box.grid(row = 0, column = 0, sticky = 'E')
 
        self._text = tkinter.StringVar()
        self._text.set('Enter Rows (even int 4-16)')
        self._incount = 0
        self._inputs = []
        self._but = tkinter.Button(master = self._root_window, textvariable = self._text, command = lambda: self._get_input('fill'), font = ('Arial Black', '14'))
        self._but.grid(row = 0, column = 1, sticky = 'W')

        self._root_window.bind('<Return>', self._get_input)
        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)

        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)
        self._root_window.columnconfigure(1, weight = 1)

        self._boxes = []
        self._black = []
        self._white = []

        self._turn_text = tkinter.StringVar()
        self._count_text = tkinter.StringVar()

        #gamestuff
        self._game = 0
        


    def start(self) -> None:
        self._root_window.mainloop()

    def _get_input(self, event) -> None:
        text = ['Enter Columns (even int 4-16)', 'Enter Starting Player (B or W)', 'Enter Upper Left Starting Piece (B or W)', 'Enter Win Method (< or >)', 'Done']
        entry = self._box.get()
        if entry == 'b':
            entry = 'B'
        if entry == 'w':
            entry = 'W'
        self._inputs.append(entry)
        self._box.delete(0, 'end')
        self._text.set(text[self._incount])
        self._incount += 1
        if self._incount > 4:
            self._root_window.unbind('<Return>')
            self._box.grid_forget()
            self._but.grid_forget()
            self._create_game()
            self._create_boxes()
            self._create_stones()
            self._draw()
            self._create_header()
            
    def _create_game(self):
        inp = self._inputs
        self._game = Game(int(inp[0]), int(inp[1]), inp[2], inp[3], inp[4])
        self._game.create()
        self._game.count()

    def _create_header(self):
        self._turn_text.set(self._game._str_turn())
        self._turn =  tkinter.Label(master = self._root_window, textvariable = self._turn_text, font = ('Arial Black', '20'))
        self._turn.grid(row = 0, column = 0)

        self._count_text.set(self._game._str_count())
        self._count = tkinter.Label(master = self._root_window, textvariable = self._count_text, font = ('Arial Black', '20'))
        self._count.grid(row = 0, column = 1)

    def _update_header(self):
        self._turn_text.set(self._game._str_turn())
        self._count_text.set(self._game._str_count())
    
    def _create_boxes(self) -> None:
        x = 1/self._game._cols
        y = 1/self._game._rows
        for r in range(self._game._rows):
            for c in range(self._game._cols):
                rec = [x*c, y*r, x*(c+1), y*(r+1)]
                self._boxes.append(rec)
                
    def _create_stones(self) -> None:
        self._black = []
        self._white = []

        x = 1/self._game._cols
        y = 1/self._game._rows
        sx = x/20
        sy = y/20

        for r in range(self._game._rows):
            for c in range(self._game._cols):
                cir = [x*c +sx , y*r + sy, x*(c+1) -sx, y*(r+1) -sy]
                if self._game.board[c][r] == 1:
                    self._black.append(cir)
                elif self._game.board[c][r] == 2:
                    self._white.append(cir)
                
    def _draw(self) -> None:
        self._canvas.delete(tkinter.ALL)
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        for rec in self._boxes:
            self._canvas.create_rectangle(rec[0]*width, rec[1]*height, rec[2]*width, rec[3]*height)
        for rec in self._black:
            self._canvas.create_oval(rec[0]*width, rec[1]*height, rec[2]*width, rec[3]*height, fill= '#000000')
        for rec in self._white:
            self._canvas.create_oval(rec[0]*width, rec[1]*height, rec[2]*width, rec[3]*height, fill= '#ffffff')

    def _on_canvas_resized(self, event: tkinter.Event) -> None:
         self._draw()

    def _on_canvas_clicked(self, event: tkinter.Event) -> None:
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        xstep = 1/self._game._cols
        ystep = 1/self._game._rows

        xfrac = event.x/width
        yfrac = event.y/height

        xint = xfrac/xstep - 0.5
        yint = yfrac/ystep - 0.5

        xint = round(xint)
        yint = round(yint)

        empty = self._game.board[xint][yint]
        flip = self._game.vflip(xint, yint, True)

        if len(flip) > 0 and empty == 0:
            self._game.flip(flip)
            self._create_stones()
            self._draw()
            self._update_header()

            if self._game.over() == True or self._game.none_left() == True:
                winner = self._game.winner_text()
                self._win = tkinter.Label(master = self._root_window, text = winner, font = ('Arial Black', '20'))
                self._win.grid(row = 3, columnspan = 2)
                self._canvas.unbind('<Button-1>')
                

        

if __name__ == '__main__':
    gui = gui()
    gui.start()
