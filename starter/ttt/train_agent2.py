from player import Player, StupidBot, SmartBot
from board import Board
import numpy as np
import random


N_EXPERIENCES = 200000
MIN_ALPHA = 0.01
MAX_ALPHA = 0.9
#ALPHAS = np.linspace(0.5, MIN_ALPHA, N_EXPERIENCES)
GAMMA = 0.5
EPSILON = 0.2
ACTION_SIZE = 9
MOVES = ['_', 'X', 'O']
PLAYER1 = 1
PLAYER2 = 2
PLAYER1_MOVE = 1
PLAYER2_MOVE = 2

WIN_REWARD = 100
SMART_REWARD = 30
MOVE_REWARD = -10
LOST_REWARD = -500
DRAW_REWARD = 50

WIN_REWARD_2ND = 200
DRAW_REWARD_2ND = 100
LOST_REWARD_2ND = -1000

# State: a string represents a matrix 3x3 contains _ (empty), X, O
# For example: _XO_XO_XO is corresponding to the following matrix:
# _XO
# _XO
# _XO
def de_state(state_str):
    # return a 2D array for a state string
    state = np.zeros(ACTION_SIZE, dtype=int)
    i = 0
    for move in state_str:
        state[i] = 0 if move == '_' else PLAYER1_MOVE if move == 'X' else PLAYER2_MOVE
        i += 1
    state = np.reshape(state, (3, 3))
    return state

def state_to_board(state_str):
    state = de_state(state_str)
    board = Board()
    for i in range(3):
        for j in range(3):
            board.move(i, j, state[i][j])
    return board

def board_to_state(board):
    state = ''
    for i in range(3):
        for j in range(3):
            state += '_' if board.get(i, j) == 0 else 'X' if board.get(i, j) == 1 else 'O'
    return state

def action_to_move(action):
    return action // 3, action % 3

def move_to_action(x, y):
    return x * 3 + y

class GameAgent(StupidBot):
    def __init__(self, value, name, epsilon=EPSILON):
        super().__init__(value, name)
        self.q_table = {}
        self.epsilon = epsilon
    
    def deep_copy(self):
        new_agent = GameAgent(self.value, self.name, self.epsilon)
        new_agent.q_table = self.q_table.copy()
        return new_agent
    
    def Q(self, state, action=None):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(ACTION_SIZE)
        if action is None:
            return self.q_table[state]
        return self.q_table[state][action]

    def random_policy(self, state):
        board = state_to_board(state)
        x, y = self.move(board) # random move because StupidBot is random
        return move_to_action(x, y)
    
    def greedy_policy(self, state):
        # find max value from Q table for current state
        values = self.Q(state)
        max_value = np.max(values)
        # find valid actions (not yet taken by any player)
        i_maxs = [i for i, v in enumerate(values) if v == max_value and state[i] == '_']
        if len(i_maxs) == 0:
            return self.random_policy(state)
        # choose a random action from valid actions
        return random.choice(i_maxs)
    
    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return self.random_policy(state)
        else:
            return self.greedy_policy(state)
        
class Environment:
    def __init__(self):
        self.state = '_________'
        self.n_moves = 0

    def reset(self):
        self.state = '_________'
        self.n_moves = 0

    def is_draw(self):
        board = state_to_board(self.state)
        return board.who_win() == 0

    def is_win(self, player):
        board = state_to_board(self.state)
        return board.who_win() == player
    
    def is_loose(self, player):
        board = state_to_board(self.state)
        return board.who_win() == 3 - player
    
    def update_state(self, action, player):
        x, y = action_to_move(action)
        board = state_to_board(self.state)
        board.move(x, y, player)
        self.state = board_to_state(board)
        self.n_moves += 1
    
    def count_consecutives(self, player):
        state_matrix = de_state(self.state)
        count = 0
        for row in range(len(state_matrix)):
            count += 1 if state_matrix[row, 0] == state_matrix[row, 1] == player else 0
            count += 1 if state_matrix[row, 1] == state_matrix[row, 2] == player else 0
        for col in range(len(state_matrix)):
            count += 1 if state_matrix[0, col] == state_matrix[1, col] == player else 0
            count += 1 if state_matrix[1, col] == state_matrix[2, col] == player else 0
        
        count += 1 if state_matrix[0, 0] == state_matrix[1, 1] == player else 0
        count += 1 if state_matrix[1, 1] == state_matrix[2, 2] == player else 0
        count += 1 if state_matrix[0, 2] == state_matrix[1, 1] == player else 0
        count += 1 if state_matrix[1, 1] == state_matrix[2, 0] == player else 0

        return count
    
    def perform(self, action, player):
        old_consecutives = self.count_consecutives(player)
        self.update_state(action, player)
        new_consecutives = self.count_consecutives(player)
        win = self.is_win(player)
        draw = self.is_draw()
        loose = self.is_loose(player)

        reward_player1 = WIN_REWARD if win else DRAW_REWARD if draw else LOST_REWARD if loose else \
                SMART_REWARD * (new_consecutives - old_consecutives)
        
        reward_player2 = LOST_REWARD if win else DRAW_REWARD if draw else -SMART_REWARD * (new_consecutives - old_consecutives)
        
        return self.state, reward_player1, reward_player2, win or draw or loose

class SmartBotModel:
    def train(self, verbose=False):
        player1 = GameAgent(1, 'Agent1')
        player2 = GameAgent(2, 'Agent2')
        player3 = GameAgent(3, 'Agent3', epsilon=1.0) # random agent used to train other agents
        env = Environment()
        # train agent 1 to attack the random agent
        ALPHAS = np.linspace(MAX_ALPHA, MIN_ALPHA, N_EXPERIENCES)
        for exp in range(N_EXPERIENCES):
            self.train_first_player(env, player1, player3, exp, verbose, ALPHAS[exp])
        # train agent 2 to defense the random agent
        for exp in range(N_EXPERIENCES):
            self.train_second_player(env, player3, player2, exp, verbose, ALPHAS[exp])
        # train agent 1 to attack the agent 2
        for exp in range(N_EXPERIENCES):
            self.train_first_player(env, player1, player2, exp, verbose, ALPHAS[exp])
        # train agent 2 to defense the random agent
        for exp in range(N_EXPERIENCES):
            self.train_second_player(env, player1, player2, exp, verbose, ALPHAS[exp])
        
        
        # save model of player1 to a text file each state in one line and next line is actions of that state
        with open('model.txt', 'w') as f:
            f.write(f'{len(player1.q_table.keys())}\n')
            f.write(f'{len(player2.q_table.keys())}\n')
            for state in player1.q_table.keys():
                f.write(state + '\n')
                for val in player1.q_table[state]:
                    f.write(str(val) + ',')
                f.write('\n')
            for state in player2.q_table.keys():
                f.write(state + '\n')
                for val in player2.q_table[state]:
                    f.write(str(val) + ',')
                f.write('\n')
    
    def train_both_player(self, env, player1, player2, exp, verbose, alpha):
        env.reset()
        player1_rewards = 0
        player2_rewards = 0
        done = False

        while not done:
            old_state_p1 = env.state
            player1_action = player1.choose_action(env.state)
            new_state_p1, reward_player1, reward_player2, done = env.perform(player1_action, PLAYER1_MOVE)
            
            player1_rewards += reward_player1
            player1.Q(old_state_p1)[player1_action] += alpha * (reward_player1 + GAMMA * np.max(player1.Q(new_state_p1)) \
                                                    - player1.Q(old_state_p1)[player1_action])
            
            if done:
                player2_rewards += reward_player2
                player2.Q(old_state_p2)[player2_action] += alpha * (reward_player2 + GAMMA * np.max(player2.Q(new_state_p2)) \
                                                        - player2.Q(old_state_p2)[player2_action])
            
            if not done:
                old_state_p2 = env.state
                player2_action = player2.choose_action(env.state)
                new_state_p2, reward_player2, reward_player1, done = env.perform(player2_action, PLAYER2_MOVE)
                
                player2_rewards += reward_player2
                player2.Q(old_state_p2)[player2_action] += alpha * (reward_player2 + GAMMA * np.max(player2.Q(new_state_p2)) \
                                                        - player2.Q(old_state_p2)[player2_action])
                player1_rewards += reward_player1
                if done:
                    player1.Q(old_state_p1)[player1_action] += alpha * (reward_player1 + GAMMA * np.max(player1.Q(new_state_p1)) \
                                                            - player1.Q(old_state_p1)[player1_action])
        
        if verbose and exp % 10000 == 0:
            print(f'Experience {exp} - P1 reward: {player1_rewards} - P2 reward: {player2_rewards} - states {len(player1.q_table)}')
        
    def train_first_player(self, env, player1, player2, exp, verbose, alpha):
        env.reset()
        player1_rewards = 0
        done = False

        while not done:
            old_state_p1 = env.state
            player1_action = player1.choose_action(env.state)
            new_state_p1, reward_player1, _, done = env.perform(player1_action, PLAYER1_MOVE)
            
            player1_rewards += reward_player1
            player1.Q(old_state_p1)[player1_action] += alpha * (reward_player1 + GAMMA * np.max(player1.Q(new_state_p1)) \
                                                    - player1.Q(old_state_p1)[player1_action])
            
            if not done:
                player2_action = player2.choose_action(env.state)
                _, _, reward_player1, done = env.perform(player2_action, PLAYER2_MOVE)
                
                player1_rewards += reward_player1
                if done:
                    player1.Q(old_state_p1)[player1_action] += alpha * (reward_player1 + GAMMA * np.max(player1.Q(new_state_p1)) \
                                                            - player1.Q(old_state_p1)[player1_action])
        
        if verbose and exp % 10000 == 0:
            print(f'Experience {exp} - P1 reward: {player1_rewards} - states {len(player1.q_table)}')
    
    def train_second_player(self, env, player1, player2, exp, verbose, alpha):
        env.reset()
        player2_rewards = 0
        done = False

        while not done:
            player1_action = player1.choose_action(env.state)
            _, _, reward_player2, done = env.perform(player1_action, PLAYER1_MOVE)
            if done:
                player2_rewards += reward_player2
                player2.Q(old_state_p2)[player2_action] += alpha * (reward_player2 + GAMMA * np.max(player2.Q(new_state_p2)) \
                                                        - player2.Q(old_state_p2)[player2_action])
            else:
                old_state_p2 = env.state
                player2_action = player2.choose_action(env.state)
                new_state_p2, reward_player2, _, done = env.perform(player2_action, PLAYER2_MOVE)
                
                player2_rewards += reward_player2
                player2.Q(old_state_p2)[player2_action] += alpha * (reward_player2 + GAMMA * np.max(player2.Q(new_state_p2)) \
                                                        - player2.Q(old_state_p2)[player2_action])
        
        if verbose and exp % 10000 == 0:
            print(f'Experience {exp} - P2 reward: {player2_rewards} - states {len(player2.q_table)}')

model = SmartBotModel()
model.train(verbose=True)
print('Training done!')