"""
framework for the game Chinese poker:
"""
import pyCardDeck
from treys import Card

class Player:
    def __init__(self, name):
        self.hands = {1:[] , 2: [],3: [],4: [],5: []}
        self.name = name
class Game:
    def __init__(self):
        card = ["AS", "KS", "QS", "JS", "10S", "9S", "8S", "7S", "6S", "5S", "4S", "3S", "2S",
                "AD", "KD", "QD", "JD", "10D", "9D", "8D", "7D", "6D", "5D", "4D", "3D", "2D",
                "AC", "KC", "QC", "JC", "10C", "9C", "8C", "7C", "6C", "5C", "4C", "3C", "2C",
                "AH", "KH", "QH", "JH", "10H", "9H", "8H", "7H", "6H", "5H", "4H", "3H", "2H"]
        self.cardDeck = pyCardDeck.Deck(cards=card)
        self.cardDeck.shuffle()
        self._Player1 = Player("Player1")
        self._Player2 = Player("Player2")
        self.round = 1
    def run(self):
        turn = int(0)

        current_player = Player
        while self.cardDeck.cards_left != 0:
            print(self._Player1.name+"\n" +
                  "hand1:  "+Card.print_pretty_cards(self._Player1.hands[1]) +
                  "hand2:  "+Card.print_pretty_cards(self._Player1.hands[2]) +
                  "hand3:  "+Card.print_pretty_cards(self._Player1.hands[3]) +
                  "hand4:  "+Card.print_pretty_cards(self._Player1.hands[4]) +
                  "hand5:  "+Card.print_pretty_cards(self._Player1.hands[5])
                  )
            print(self._Player2.name+"\n" +
                  "hand1:  "+Card.print_pretty_cards(self._Player2.hands[1]) +
                  "hand2:  "+Card.print_pretty_cards(self._Player2.hands[2]) +
                  "hand3:  "+Card.print_pretty_cards(self._Player2.hands[3]) +
                  "hand4:  "+Card.print_pretty_cards(self._Player2.hands[4]) +
                  "hand5:  "+Card.print_pretty_cards(self._Player2.hands[5])
                  )

            if turn % 2 == 0:
                current_player = self._Player1
            else:
                current_player = self._Player2
            card = self.cardDeck.draw()
            hand_selected = int(input(current_player.name + " turn\t\t card is:" + card.name))
            while len(current_player.hands[hand_selected]) == self.round:
                print("illegal move")
                hand_selected = int(input(current_player.name + " turn\t\t card is:" + card.name))
            current_player.hands[hand_selected].append(Card.new(card.name))
            if turn % 10 == 0:
                self.round += 1
            turn += 1

if __name__ == '__main__':
    game = Game()
    game.run()