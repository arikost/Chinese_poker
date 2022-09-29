"""
framework for the game Chinese poker:
"""

from time import time
import pyCardDeck
from treys import Card, Evaluator

cards = ["As", "Ks", "Qs", "Js", "Ts", "9s", "8s", "7s", "6s", "5s", "4s", "3s", "2s",
                "Ad", "Kd", "Qd", "Jd", "Td", "9d", "8d", "7d", "6d", "5d", "4d", "3d", "2d",
                "Ac", "Kc", "Qc", "Jc", "Tc", "9c", "8c","7c", "6c", "5c", "4c", "3c", "2c",
                "Ah", "Kh", "Qh", "Jh", "Th", "9h", "8h","7h", "6h", "5h", "4h", "3h", "2h"]
class Game:
    def __init__(self):
        

        
        self.evaluetor = Evaluator()
        self.Player1 = [[],[],[],[],[]]
        self.Player2 = [[],[],[],[],[]]
       
        self.cardDeck = pyCardDeck.Deck(cards=[Card.new(c) for c in cards])
        self.current_card = Card()
        self.reset()
    def reset(self):
        
        
        if(self.cardDeck.cards_left <= 3):
            
            
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
        
        for i in range(5):
            self.Player1[i].clear()
            self.Player2[i].clear()
            self.Player1[i].append(self.cardDeck.draw())
            self.Player2[i].append(self.cardDeck.draw())
            
        self._draw_next_card()
    def _draw_next_card(self):
        self.current_card = self.cardDeck.draw()

    def play_step(self, hand_selected, player):
        self.turn += 1
        if player == 1:
            self.Player1[hand_selected].append(self.current_card)
        else:
            self.Player2[hand_selected].append(self.current_card)
        
        if self.turn == 40:
            return True
        else: 
            self._draw_next_card()
            return False
    
    def get_score(self):
        p1_score = []
        p2_score = []
        for i in range(5):
            if self.evaluetor.evaluate(self.Player1[i][2::], self.Player1[i][0:2]) < self.evaluetor.evaluate(self.Player2[i][2::], self.Player2[i][0:2]):
                p1_score.append(i+1)
            elif self.evaluetor.evaluate(self.Player1[i][2::], self.Player1[i][0:2]) > self.evaluetor.evaluate(self.Player2[i][2::], self.Player2[i][0:2]):
                p2_score.append(i+1)
            else:
                continue
        return (p1_score, p2_score)

if __name__ == '__main__':
    # game = Game()
    # hand_selected = 0
    # current_player = 1
    # while True:
    #     print("------------\n------------\n------------\n")    
    #     print("player 1:")
    #     for h in game.Player1:
    #         Card.print_pretty_cards(h) 
    #     print("player 2:")
    #     for h in game.Player2:
    #         Card.print_pretty_cards(h)
    #     if game.play_step(hand_selected%5, current_player%2):
    #         p1 , p2 = game.get_score()
    #         print("------------\n------------\n------------\n")    
    #         print("player 1:")
    #         for h in game.Player1:
    #             Card.print_pretty_cards(h) 
    #         print("player 2:")
    #         for h in game.Player2:
    #             Card.print_pretty_cards(h)
    #         print("player1 won hands", p1, "\nplayer2 won hands",p2) 
    #         break
        
    #     hand_selected += 1
    #     current_player += 1
    # game.reset()
    x = 5
    print('blabla{}'.format(x))        

