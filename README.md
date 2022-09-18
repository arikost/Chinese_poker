# Chinese_poker
**game discription:**

in this version of chinese poker there are 2 player each player has 5 hands of 2 cards numberd 1 to 5
and three community cards in the center of the table, The deck contains cards from 8 to Ace.
at the start of the game each player recive 5 cards and the three community are exposed to the players

![image](https://user-images.githubusercontent.com/82440808/190897578-18bcbe96-779a-4c3b-8ea0-26d1e7940bb3.png)

in each round each player drawing a card from the deck and chooses which hand to attach it to.

![image](https://user-images.githubusercontent.com/82440808/190897757-bb7aea10-2886-44b3-a4f1-a5b403720d9e.png)

At the end of the game, compare the strength of the respective hands (1 vs. 1, 2 vs. 2...). The player who won more hands wins

![image](https://user-images.githubusercontent.com/82440808/190897866-1ad10212-3ec6-4681-bb64-0313de5cb385.png)

**requirements:**

install the following packeges:
```
  pip install pyCardDeck
  pip install treys
  pip install numpy
  pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
```  
**algorithm:**

I created two players and let them play against each other for 2500 iterations, 
at each stage of the game we save the snapshot of the table in the form of a matrix,
```
        oppoenet_closeCards = np.array([x[1] if len(x)>1 else 0 for x in oppoenet_Cards])
        oppoenet_openCards = np.array([x[0] for x in oppoenet_Cards]) 
        my_cards1 = np.array([x[0] for x in my_cards])     
        my_cards2 = np.array([x[1] if len(x)>1 else 0 for x in my_cards])

        
        board_arr_temp = np.array(game.board)
        board_arr = np.concatenate((board_arr_temp, [0,game.current_card]))
        #size of state is 5x5
        state = [ oppoenet_closeCards, 
                oppoenet_openCards, 
                board_arr,
                my_cards1,
                my_cards2
                ]
        
        return np.array(state, dtype=int)
```
at the end of the game after the results are revealed we attach a score to each decision according to the victory(1) or loss(-1) of the chosen hand,
```
def set_reward(node:Node, hands_won):
    if node.action in hands_won: 
        node.set_reward(1)
    else:
        node.set_reward(-1)
```
finally we transfer to the neural network model the All the information and train it (the model).
```
def train_short_memory(self, node:Node):
        self.trainer.train_step(node.state.flatten(), node.next_state.flatten(), node.action, node.reward, node.game_over)
 ...
for node in node_list_player1:
  set_reward(node, score_p1)
  agent1.remember(node)
  agent1.train_short_memory(node)

```
Because at each stage the possibility of choice is reduced, so I make a correction in the calculation of the Balman equation for illegal choices.
```
for idx in range(len(game_over)):

        Q_new = reward[idx]
        if not game_over[idx]:
            for i in range(5):
                if next_state[idx][i+20] == 0:
                    option.append(i)

            prediction = self.model(next_state[idx])             
            hand_selected = torch.argmax(prediction).item()
            Q_new = reward[idx] + self.gamma * prediction[hand_selected] 
            if not hand_selected in option and len(option) > 1:
                Q_new *= (-1)


        option.clear()
        target[idx][action[idx]] = Q_new  
```        
Input size 25 (vector of the cards on the table)

Output size 5 (vector of the value of each decision)


