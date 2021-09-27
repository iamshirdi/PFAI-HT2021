'''
Definitions for GameNode, GameSearch and MCTS

Author: Tony Lindgren
'''
from time import process_time
import random
import math


class GameNode:
    '''
    This class defines game nodes in game search trees. It keep track of: 
    state
    '''
    def __init__(self, state, node=None, parent=None):
        self.state = state   
        self.actions_left = []
        self.visits = 0
        self.wins = 0
        self.parent = parent
        self.succesors=[]


class GameSearch:
    '''
    Class containing different game search algorithms, call it with a defined game/node
    '''                 
    def __init__(self, game, depth=3, time = 2):
        self.state = game       
        self.depth = depth
        self.time = time

    def mcts(self):                     
        start_time = process_time() 
        tree = GameNode(self.state)
        tree.actions_left = tree.state.actions()   
        elapsed_time = 0
        while elapsed_time < self.time:   
            leaf = self.select(tree)
            child = self.expand(leaf)               
            result = self.simulate(child) 
            self.back_propagate(result, child)         
            stop_time = process_time()
            elapsed_time = stop_time - start_time
        move = self.actions(tree)
        return move
    
    def select(self, tree):
        # if any actions left/unexplored its ucb is infinite we choose it
        if len(tree.actions_left) > 0:
            a = random.choice(tree.actions_left)
            tree.actions_left.pop(a)
            s_node = GameNode(tree.state.result(a), parent = tree)
            tree.succesors.append(s_node)
            return s_node
        
        #should not be terminal node return
        node = None
        ucb = float('-inf')
        for child_gn in tree.successors:
            ucb2 = child_gn.wins/child_gn.visits + 1.4 * ((math.log(tree.wins)/child_gn.visits)**0.5)
            if ucb2 > ucb :
               node = child_gn
        return node # returns highest ucb node if not visited/explored as selected child node

    def expand(self, leaf):
        if leaf.state.is_terminal:
            return leaf
        if len(leaf.actions_left) < 1:
            leaf.actions_left = leaf.state.actions()   

        s_node =self.select(leaf)
        return s_node

    def simulate(self, child):
        while True:
            if child.state.is_terminal:
                return child
            if len(child.actions_left) < 1:
                child.actions_left = child.state.actions()

            child = self.select(child)

    def back_propagate(self, result, child):
        if result.state.curr_move == result.state.ai_player:
            win = True
        else:
            win = False
        while child.parent != None: #even middle state tree parent is None when initalized
            child.visits +=1
            if win:
                child.wins +=1
            win = not win
            child = child.parent

    def actions(self, tree):
        node = None # terminal node must not be
        ucb = float('-inf')
        for child_gn in tree.successors:
            ucb2 = child_gn.wins/child_gn.visits + 1.4 * ((math.log(tree.wins)/child_gn.visits)**0.5)
           #incase initial selection is not done check if no wins
            if (child_gn.wins or tree.wins ==0) and child_gn.visits==0:
                if ucb2 > ucb :
                    node = child_gn
        #since we did not keep track of move for a action in node
        for a in tree.state.actions():
            if node.state == tree.state.result(a):
                return a
    
    def minimax_search(self): 
        start_time = process_time()   
        _, move = self.max_value(self.state, self.depth, -100000, 100000, start_time)  
        return move
    
    def max_value(self, state, depth, alpha, beta, time): #ai max player
        move = None
        terminal, value = state.is_terminal() #value = 0 if terminal = False
        if terminal or depth == 0 or process_time() - time > self.time:
            if process_time() - time > self.time:
                print("time reached")
            return value, None
        v = -100000
        actions = state.actions()
        for action in actions: 
            new_state = state.result(action) # appends element in respective column and results new state
            # print("max",action,actions, new_state.board, depth,"value:",v)
            v2, _ = self.min_value(new_state, depth - 1, alpha, beta, time)   
           
            if v2 >v:
                v,move = v2, action    # if terminal:false takes first one in tree always
               
                alpha = max(alpha, v)
            if v>= beta:
                return v,move
      
        return v, move
    
    def min_value(self, state, depth, alpha, beta, time):
        move = None
        terminal, value = state.is_terminal()
        if terminal or depth == 0 or process_time() - time > self.time  :
            return value, None  
        v = 100000
        actions = state.actions()
        for action in actions: 
            new_state = state.result(action)
            # print("min",action,actions, new_state.board,depth,"value:",v)   
            v2, _ = self.max_value(new_state, depth - 1, alpha, beta, time)     

            if v2 < v:
                # print("value changed",v2,v)
                v,move = v2, action      
                
                beta = min(beta, v)
            if v<= alpha:
                return v,move        

        return v, move
