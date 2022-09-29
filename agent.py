import torch
import random
import numpy as np
from collections import deque
from game import Game
from model import Linear_QNet, QTrainer
from treys import Card

MAX_MEMORY = 100_000
BATCH_SIZE = 100
LR = 0.001
class Node:
    def __init__(self, state, next_state, action, game_over):
        self.state = state
        self.next_state = next_state
        self.action = action
        self.reward = 0
        self.game_over = game_over
    def set_reward(self, reward):
        self.reward = reward


class Agent:
    def __init__(self, player):
        self.n_games = 0
        self.player = player
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory1 = deque(maxlen=MAX_MEMORY) # popleft()
        self.memory2 = deque(maxlen=MAX_MEMORY) # popleft()
        self.memory3 = deque(maxlen=MAX_MEMORY) # popleft()
        self.memory4 = deque(maxlen=MAX_MEMORY) # popleft()
        self.model1 = Linear_QNet(51, 256, 5)
        self.model2 = Linear_QNet(51, 256, 4)
        self.model3 = Linear_QNet(51, 256, 3)
        self.model4 = Linear_QNet(51, 256, 2)
        self.trainer1 = QTrainer(self.model1, lr=LR, gamma=self.gamma)
        self.trainer2 = QTrainer(self.model2, lr=LR, gamma=self.gamma)
        self.trainer3 = QTrainer(self.model3, lr=LR, gamma=self.gamma)
        self.trainer4 = QTrainer(self.model4, lr=LR, gamma=self.gamma)
    
    def get_state(self, game:Game):
        if self.player == 1:
            oppoenet_Cards = game.Player2
            my_cards = game.Player1
        else:
            oppoenet_Cards = game.Player1
            my_cards = game.Player2
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

    def remember(self, node:Node):
        #the state has to be a vector
        self.memory.append((node.state.flatten(), node.next_state.flatten(), node.action, node.reward, node.game_over))
    def train_short_memory(self, node:Node):
        self.trainer.train_step(node.state.flatten(), node.next_state.flatten(), node.action, node.reward, node.game_over)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, next_state, hand_selected, rewards, game_over = zip(*mini_sample)
        self.trainer.train_step(states, next_state, hand_selected, rewards, game_over)

    def gat_action(self, state, flag=False):
        self.epsilon = 80 - self.n_games
        hand_selected = 0
        option = []
        for i in range(5):
            if state[4][i] == 0:
                option.append(i)
        if random.randint(0, 200) < self.epsilon or self.n_games < 80:
            if len(option) == 1:
                x = 0
            else:
                x = random.randint(0,len(option)-1)
            hand_selected = option[x]
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            #TODO: prediction based on the number of option
            prediction = self.model(state0.flatten())
            if flag:
                print(prediction)
            
             
        return hand_selected

def set_reward(node:Node, hands_won):
    if node.action in hands_won: 
        node.set_reward(1)
    else:
        node.set_reward(-1)

def train_vs_agent(game:Game, agent1:Agent, num_iter = 5000):
    agent2 = Agent(2)

    node_list_player1 = []
    node_list_player2 = []
    game_over = False
    
    current_player = 1

    while agent1.n_games < num_iter:
       
        if current_player % 2 == 1:
            state = agent1.get_state(game)
            hand_selected = agent1.gat_action(state)
            game_over = game.play_step(hand_selected, current_player % 2)
            next_state = agent1.get_state(game)
            node_list_player1.append(Node(state, next_state, hand_selected, game_over))
        else:
            state = agent2.get_state(game)
            hand_selected = agent2.gat_action(state)
            game_over = game.play_step(hand_selected, current_player % 2)
            next_state = agent2.get_state(game)
            node_list_player2.append(Node(state, next_state, hand_selected, game_over))
        if game_over:
            score_p1 , score_p2 = game.get_score()
            for node in node_list_player1:
                set_reward(node, score_p1)
                agent1.remember(node)
                agent1.train_short_memory(node)
            agent1.train_long_memory()
            node_list_player1.clear()
            for node in node_list_player2:
                set_reward(node, score_p2)
                agent2.remember(node)
                agent2.train_short_memory(node)
            agent2.train_long_memory()
            node_list_player2.clear()
            agent1.n_games += 1
            print("number of game:  -----", agent1.n_games)
            current_player = 0
            game.reset()
        current_player += 1

def train_vs_humen(game:Game, agent:Agent):
   

    node_list_player1 = []
    
    game_over = False
    
    current_player = 1

    while True:
        
        print("player 1:")
        for h in game.Player1:
            Card.print_pretty_cards(h) 
        print("player 2:")
        for h in game.Player2:
            Card.print_pretty_cards(h)
        print("current card:")
        Card.print_pretty_card(game.current_card)
        print("------------\n------------\n------------\n")    
        if current_player % 2 == 1:
            state = agent.get_state(game)
            hand_selected = agent.gat_action(state,flag=True)
            game_over = game.play_step(hand_selected, current_player % 2)
            next_state = agent.get_state(game)
            node_list_player1.append(Node(state, next_state, hand_selected, game_over))
        else:
            while True:
                hand_selected = int(input("select hand"))
                if len(game.Player2[hand_selected]) == 2:
                    print("bad choise... try again")
                else:
                    break
            game_over = game.play_step(hand_selected, current_player % 2)
        if game_over:
            p1 , p2 = game.get_score()
           
            print("player1 won hands", p1, "\nplayer2 won hands",p2)
            for node in node_list_player1:
                set_reward(node, p1)
                agent.remember(node)
                agent.train_short_memory(node)
            agent.train_long_memory()

            if int(input("Would you like to play again? (0 = no, 1 = yes)")) == 1:
                game.reset()
                current_player = 0
                node_list_player1.clear()
            else:    
                break
        current_player += 1

if __name__ == "__main__":
    game = Game()
    agent = Agent(1)
    train_vs_agent(game, agent, num_iter=2500)
    agent.model.save()
    train_vs_humen(game, agent)
    