"""
framework for the game Chinese poker:
"""
from time import time
import pyCardDeck
from treys import Card, Evaluator
import random
import time
class Player:
    def __init__(self, name):
        self.hands = {1:[] , 2: [],3: [],4: [],5: []}
        self.name = name
class Game:
    def __init__(self):
        card = ["As", "Ks", "Qs", "Js", "Ts", "9s", "8s", "7s", "6s", "5s", "4s", "3s", "2s",
                "Ad", "Kd", "Qd", "Jd", "Td", "9d", "8d", "7d", "6d", "5d", "4d", "3d", "2d",
                "Ac", "Kc", "Qc", "Jc", "Tc", "9c", "8c", "7c", "6c", "5c", "4c", "3c", "2c",
                "Ah", "Kh", "Qh", "Jh", "Th", "9h", "8h", "7h", "6h", "5h", "4h", "3h", "2h"]
        self.cardDeck = pyCardDeck.Deck(cards=card)
        self.cardDeck.shuffle()
        self._Player1 = Player("Player1")
        self._Player2 = Player("Player2")
        self.round = 1
        self.evaluetor = Evaluator()
    def run(self):
        
        turn = int(0)
        current_player = Player
        for i in range(5):
            card = self.cardDeck.draw()
            self._Player1.hands[i+1].append(Card.new(card))
        for i in range(5):
            card = self.cardDeck.draw()
            self._Player2.hands[i+1].append(Card.new(card))

        while self.cardDeck.cards_left > 0:
            print("-------------------------------------------------------------------------------------------")
            print("-------------------------------------------------------------------------------------------")
            print("-------------------------------------------------------------------------------------------")
            print(self._Player1.name + "-------------------")
            print("hand1:  "); Card.print_pretty_cards(self._Player1.hands[1]) 
            print("hand2:  "); Card.print_pretty_cards(self._Player1.hands[2]) 
            print("hand3:  "); Card.print_pretty_cards(self._Player1.hands[3]) 
            print("hand4:  "); Card.print_pretty_cards(self._Player1.hands[4]) 
            print("hand5:  "); Card.print_pretty_cards(self._Player1.hands[5]) 
            
            print("\n"+self._Player2.name + "-------------------")
            print("hand1:  "); Card.print_pretty_cards(self._Player2.hands[1]) 
            print("hand2:  "); Card.print_pretty_cards(self._Player2.hands[2]) 
            print("hand3:  "); Card.print_pretty_cards(self._Player2.hands[3]) 
            print("hand4:  "); Card.print_pretty_cards(self._Player2.hands[4]) 
            print("hand5:  "); Card.print_pretty_cards(self._Player2.hands[5]) 
            
            if turn % 2 == 0:
                current_player = self._Player1
            else:
                current_player = self._Player2
            turn += 1
            card = Card.new(self.cardDeck.draw())
            print("cards left:", self.cardDeck.cards_left, "turn: ", turn)

            print("----------------------"+current_player.name + " Turn------------------------")
            print("New Card Is:")
            Card.print_pretty_card(card)
            if turn > 40 :
                hand_selected = random.randint(0,5)
                if hand_selected != 0:
                    current_player.hands[hand_selected].pop()
                    current_player.hands[hand_selected].append(card)
            else:
            #hand_selected = int(input(" choose hand: "))
                hand_selected = random.randint(1, 5)
                while len(current_player.hands[hand_selected]) > self.round:# or hand_selected < 1 or hand_selected > 5:
                    print("illegal move")
                    print("New Card Is:"); Card.print_pretty_card(card)
                    #hand_selected = int(input(" choose hand: "))
                    hand_selected = random.randint(1, 5)
                
            
                current_player.hands[hand_selected].append(card)
            
            if turn % 10 == 0:
                self.round += 1

            

            time.sleep(1)
    def getWinner(self):
        player1_scorre = 0
        player2_scorre = 0
        for i in range(5):
            p1 = self.evaluetor.evaluate(self._Player1.hands[i+1][0:2], self._Player1.hands[i+1][2:5]) 
            p2 = self.evaluetor.evaluate(self._Player2.hands[i+1][0:2], self._Player2.hands[i+1][2:5])
            if p1 < p2:
                player1_scorre += 1
            elif p1 > p2:
                player2_scorre += 1
            else:
                continue
        if player1_scorre > player2_scorre:
            return "The Winner is" + self._Player1.name
        elif player1_scorre < player2_scorre:
            return "The Winner is" +self._Player2.name
        else:
            return "It's a Draw"
        

if __name__ == '__main__':
    game = Game()
    game.run()
    print(game.getWinner())