import random

class Mastermind:

    def __init__(self):

        self.colors = ('red', 'green', 'blue', 'black', 'white', 'orange', 'yellow', 'brown')
        self.pawns = len(self.colors)//2
        self.guess = None # tuple with colors to guess
        self.rounds = 12
        self.new()

    def new(self):

        self.round = 0
        self.score = self.rounds*self.pawns*3 # 4 pawns, max 3 points for pawn on its position
        self.win = False
        self.test = [] # keeps current user input
        self.game_play = {'colors': self.colors, 'answers':[]} # keeps answers
        self.generate_guess()

    def generate_guess(self):

        max = len(self.colors)-1
        c0 = random.randint(0, max)
        c1 = random.randint(0, max)
        c2 = random.randint(0, max)
        c3 = random.randint(0, max)

        self.guess = (self.colors[c0], self.colors[c1], self.colors[c2], self.colors[c3])
        self.game_play['guess'] = self.guess

    def check(self):
        if self.win or self.round > self.rounds-1:
            return
        test = [c for c in self.test]
        guess = [c for c in self.guess]
        answer =  ['lightgrey' for x in range(len(guess))]
        for i in range(len(guess)):
            if guess[i] == test[i]:
                answer[i] = 'black'
                test[i] = None
                guess[i] = None
        for i in range(len(guess)):
            if guess[i] is not None:
                if guess[i] in test:
                    answer[i] = 'white'
                    test[test.index(guess[i])] = None
                    guess[i] = None
        # 
        answer = [c for c in answer if c == 'black'] + [c for c in answer if c == 'white'] + [c for c in answer if c == 'lightgrey']
        self.score -= sum([{'black':0, 'white':1, 'lightgrey':3}[v] for v in answer])
        self.win = answer[0] == 'black' and answer[1] == 'black' and answer[2] == 'black' and answer[3] == 'black'
        self.game_play['answers'].append({'test': self.test, 'answer': answer})
        self.round += 1
