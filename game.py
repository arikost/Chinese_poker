"""
framework for the game Chinese poker:
"""
from time import time
import pyCardDeck
from treys import Card, Evaluator
import random
import time
    
class Game:
    def __init__(self):
        card = ["As", "Ks", "Qs", "Js", "Ts", "9s", "8s", 
                "Ad", "Kd", "Qd", "Jd", "Td", "9d", "8d", 
                "Ac", "Kc", "Qc", "Jc", "Tc", "9c", "8c",
                "Ah", "Kh", "Qh", "Jh", "Th", "9h", "8h"]
        self.cardDeck = pyCardDeck.Deck(cards=card)
        self.evaluetor = Evaluator()
        self.Player1 = [[],[],[],[],[]]
        self.Player2 = [[],[],[],[],[]]
        self.board = []
        self.reset()
    def reset(self):
        self.cardDeck.shuffle_back()
        self.turn = 0
        for i in range(5):
            self.Player1[i].append(Card.new(self.cardDeck.draw()))
            self.Player2[i].append(Card.new(self.cardDeck.draw()))
            if i < 3:
                self.board.append(Card.new(self.cardDeck.draw()))
    def play_step(self, hand_selected,  card):
        if self.turn == 10:
            return True
        self.turn += 1
        if self.turn % 2 == 0:
            self.Player1[hand_selected].append(card)
        else:
            self.Player2[hand_selected].append(card)
        if self.turn == 11:
            return True
        else: 
            return False
    
    def get_score(self):
        p1_score = []
        p2_score = []
        for i in range(5):
            if self.evaluetor.evaluate(self.board, self.Player1[i]) < self.evaluetor.evaluate(self.board, self.Player2[i]):
                p1_score.append(i+1)
            elif self.evaluetor.evaluate(self.board, self.Player1[i]) > self.evaluetor.evaluate(self.board, self.Player2[i]):
                p2_score.append(i+1)
            else:
                continue
        return (p1_score, p2_score)

if __name__ == '__main__':
    game = Game()
    hand_selected = 0
    while True:
        new_card = Card.new(game.cardDeck.draw())
        if game.play_step(hand_selected%5, new_card):
            p1 , p2 = game.get_score()
            print("board:")
            Card.print_pretty_cards(game.board)
            print("player 1:")
            for h in game.Player1:
                Card.print_pretty_cards(h) 
            print("player 2:")
            for h in game.Player2:
                Card.print_pretty_cards(h)
            print("player1 won hands", p1, "\nplayer2 won hands",p2) 
            break
        hand_selected += 1

        
    
        

