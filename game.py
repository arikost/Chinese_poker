"""
framework for the game Chinese poker:
"""
from ast import Delete
from time import time
import pyCardDeck
from treys import Card, Evaluator
import random
import time
cards = ["As", "Ks", "Qs", "Js", "Ts", "9s", "8s", 
                "Ad", "Kd", "Qd", "Jd", "Td", "9d", "8d", 
                "Ac", "Kc", "Qc", "Jc", "Tc", "9c", "8c",
                "Ah", "Kh", "Qh", "Jh", "Th", "9h", "8h"]
class Game:
    def __init__(self):
        

        
        self.evaluetor = Evaluator()
        self.Player1 = [[],[],[],[],[]]
        self.Player2 = [[],[],[],[],[]]
        self.board = []
        self.cardDeck = pyCardDeck.Deck(cards=[Card.new(c) for c in cards])
        self.current_card = Card()
        self.reset()
    def reset(self):
        
        
        if(self.cardDeck.cards_left == 5):
            
            self.cardDeck.add_many(cards=self.board)
            self.cardDeck.add_many(cards=self.Player1[0])
            self.cardDeck.add_many(cards=self.Player1[1])
            self.cardDeck.add_many(cards=self.Player1[2])
            self.cardDeck.add_many(cards=self.Player1[3])
            self.cardDeck.add_many(cards=self.Player1[4])
            self.cardDeck.add_many(cards=self.Player2[0])
            self.cardDeck.add_many(cards=self.Player2[1])
            self.cardDeck.add_many(cards=self.Player2[2])
            self.cardDeck.add_many(cards=self.Player2[3])
            self.cardDeck.add_many(cards=self.Player2[4])
            
        self.cardDeck.shuffle()
        self.turn = 0
        self.board.clear()
        for i in range(5):
            self.Player1[i].clear()
            self.Player2[i].clear()
            self.Player1[i].append(self.cardDeck.draw())
            self.Player2[i].append(self.cardDeck.draw())
            if i < 3:
                self.board.append(self.cardDeck.draw())
        self._draw_next_card()
    def _draw_next_card(self):
        self.current_card = self.cardDeck.draw()

    def play_step(self, hand_selected, player):
        self.turn += 1
        if player == 1:
            self.Player1[hand_selected].append(self.current_card)
        else:
            self.Player2[hand_selected].append(self.current_card)
        
        if self.turn == 10:
            return True
        else: 
            self._draw_next_card()
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
    current_player = 1
    while True:
        
        if game.play_step(hand_selected%5, current_player%2):
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
        current_player += 1
    game.reset()
        
    
        

