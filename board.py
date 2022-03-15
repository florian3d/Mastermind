'''board class module'''
import tkinter
import tkinter.font
import tkinter.ttk

class Board:
    '''Board class'''

    def __init__(self, mastermind):
        '''init board object'''
        self.game = mastermind
        #
        self.b_margin = 8
        self.box = 50
        self.rad_big = self.box - self.b_margin
        self.rad_small = self.box - self.b_margin * 2
        self.pad_big = self.box - self.rad_big
        self.pad_small = self.box - self.rad_small
        self.c_margin = 8
        self.c_w = self.box * self.game.pawns*2
        self.c_h = self.box * (self.game.rounds+2)
        #
        self.root = tkinter.Tk()
        self.font = tkinter.font.Font(self.root)
        self.root.resizable(False, False)
        self.root.title('MASTERMIND')
        #
        self.root.columnconfigure(0,weight=2)
        self.root.columnconfigure(1,weight=1)
        self.root.columnconfigure(2,weight=3)
        #
        btn_new = tkinter.Button(self.root, text='NEW GAME', font=self.font)
        btn_new.grid(row=0, column=0, padx=self.c_margin, pady=self.c_margin, sticky='ewns')
        btn_new.bind('<ButtonRelease-1>', lambda event: self.reset())
        #
        self.strvr_score = tkinter.StringVar()
        lbl_score = tkinter.Label(self.root, textvariable=self.strvr_score, font=self.font, relief='sunken')
        lbl_score.grid(row=0, column=1, padx=self.c_margin//2, pady=self.c_margin, sticky='ewns')
        #
        self.strvr_msg = tkinter.StringVar()
        lbl_msg = tkinter.Label(self.root, textvariable=self.strvr_msg, font=self.font, relief='sunken')
        lbl_msg.grid(row=0, column=2, padx=self.c_margin, pady=self.c_margin, sticky='ewns')
        #
        sep = tkinter.ttk.Separator(self.root)
        sep.grid(row=1, column=0, columnspan=3, padx=self.c_margin, pady=0, sticky='ewns')
        #
        self.canvas = tkinter.Canvas(self.root, width=self.c_w, height=self.c_h)
        self.canvas.grid(row=2, column=0, padx=self.c_margin, pady=self.c_margin, sticky='ewns', columnspan=3)
        self.clicked = []
        self.pawns = []
        #
        self.draw_board()
        #
        self.root.mainloop()

    def color_pressed(self, event):
        '''click on color handler'''
        if self.game.win or self.game.round > self.game.rounds-1:
            return

        name, color, rnd, pos, current = event.widget.gettags('current')
        if '' in self.clicked:
            self.clicked[self.clicked.index('')] = color
        else:
            self.clicked.append(color)

        for i, c in enumerate(self.clicked):
            id = self.draw_pawn(c, self.game.round+1, i, outline='black', tags=['shot', c, self.game.round, i])
            self.canvas.tag_bind(id, '<Double-Button-1>', self.color_unpressed)

        if len(self.clicked) == len(self.game.guess):
            self.game.test = self.clicked
            self.game.check()
            self.clicked.clear()
            ans = self.game.game_play['answers'][self.game.round-1]['answer']
            for i, c in enumerate(ans):
                self.draw_pawn(c, self.game.round, i+4, outline='black', small=True, tags=['empty'])
            self.strvr_score.set(self.game.score)
            if self.game.win or self.game.round > self.game.rounds-1:
                self.draw_guess(game_over=True)
                self.strvr_msg.set('YOU WON!' if self.game.win else 'YOU LOST!')
            else:
                self.strvr_msg.set('{0} of {1}'.format(self.game.round+1, self.game.rounds))

    def color_unpressed(self, event):
        '''removes unwanted color'''
        name, color, rnd, pos, current = event.widget.gettags('current')
        if int(rnd) == self.game.round:
            self.clicked[int(pos)] = ''
            self.canvas.delete('current')

    def draw_pawns(self):
        '''draws all empty pawns on board'''
        for i in range(self.game.rounds):
            for j in range(self.game.pawns*2):
                self.draw_pawn('', i+1, j, small=False if j<self.game.pawns else True, tags=['pawn' if j<self.game.pawns else 'prompt', '', i, j])

    def draw_pawn(self, color, row, col, tags=None, outline='darkgray', small=False):
        '''draws pawn'''
        id = ''
        w, h, p = self.rad_big, self.rad_big, self.pad_big
        if small:
            w, h, p = self.rad_small, self.rad_small, self.pad_small
        x = col*self.box
        y = row*self.box
        if 'button' in tags:
            id = self.canvas.create_rectangle(x+p, y+p, x+w, y+h, outline=outline, fill=color, tags=tags)
        else:
            id = self.canvas.create_oval(x+p, y+p, x+w, y+h, outline=outline, fill=color, tags=tags)
        return id

    def draw_guess(self, game_over=False):
        '''draws guess pawns'''
        for i, c in enumerate(self.game.guess):
            id = self.draw_pawn(c if game_over else 'lightgray', 0, 2+i, outline='black', tags=['guess', c if game_over else '', -1, i])

    def draw_colors(self):
        '''draws colors to choose from'''
        for i, c in enumerate(self.game.colors):            
            id = self.draw_pawn(c, self.game.rounds+1, i, outline='black', tags=['button', c, -1, i])
            self.canvas.tag_bind(id, '<Button-1>', self.color_pressed)

    def draw_board(self):
        '''draws board'''
        self.strvr_score.set(self.game.score)
        self.strvr_msg.set('{0} of {1}'.format(self.game.round+1, self.game.rounds))
        self.draw_guess()
        self.draw_pawns()
        self.draw_colors()

    def reset(self):
        '''new game'''
        self.game.new()
        self.canvas.delete('all')
        self.clicked = []
        self.draw_board()
