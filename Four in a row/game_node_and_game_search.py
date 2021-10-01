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
        while True:
            # if any actions left/unexplored its ucb is infinite:visits:0 we choose it
            if len(tree.actions_left) >0:
                return tree
                
            ucb = float('-inf') # can keep large negative since highest ucb outlier usually is not recommeneded
            # as it causes more weight to that move and negative consequences - refer lecture
            for child_gn in tree.succesors:
                if child_gn.visits==0 or tree.wins ==0 :
                    ucb = float('inf')
                    node = child_gn
                    break

                ucb2 = child_gn.wins/child_gn.visits + 1.4 * ((math.log(tree.wins)/child_gn.visits)**0.5)
                if ucb2 > ucb :
                    ucb = ucb2
                    node = child_gn # returns highest ucb node if not visited/explored as selected child node      

            #if no more leaf nodes all exlpored and reached terminal node select highest ucb and return
            terminal, value = node.state.is_terminal()    
            if terminal:
                return node

            if len(node.succesors)<1:
                node.actions_left = node.state.actions()  
            tree = node

    def expand(self, leaf):
        terminal, value = leaf.state.is_terminal()
        if terminal:
            return leaf
        a = random.choice(leaf.actions_left)
        leaf.actions_left.remove(a)
        s_node = GameNode(leaf.state.result(a), parent = leaf)
        leaf.succesors.append(s_node)
        return s_node

    def simulate(self, child):
        terminal, value = child.state.is_terminal()
        if terminal:
            return child
        # Dont store or add simulated nodes
        a = random.choice(child.state.actions())
        s_node = GameNode(child.state.result(a), parent = child)
        r = self.simulate(s_node)
        return r

    def back_propagate(self, result, child):
        terminal, value = result.state.is_terminal()
        if value > 0:
            win = True
        elif value <0 :
            win = False
        
        if value == 0:
            return  # dont add visits or wins : will it return same move ?
            
        # if child == child.parent: #terminal selection if no more leafs
        #     child = child.parent

        #this indicates that its human turn
        if child.state.curr_move == child.state.ai_player:
            win = not win

        # from child node update visits,wins
        while True:
            child.visits +=1
            if win:
                child.wins +=1

            if child.parent==None:
                break
            child = child.parent
            win = not win


    def actions(self, tree):
        node = None # terminal node must not be
        ucb = float('-inf')
        for s in tree.succesors:
            # #incase initial selection is not done add check for wins only
            # if child_gn.visits!=0 and tree.wins !=0 :
            ucb2 = s.wins/s.visits + 1.4 * ((math.log(tree.wins)/s.visits)**0.5)
            if ucb2 > ucb :
                print(s.state.board, ucb2)
                ucb = ucb2
                node = s
        #since we did not keep track of move for a action in node
        for a in tree.state.actions():
            if node.state.board == tree.state.result(a).board:
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
