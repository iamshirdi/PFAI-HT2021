'''
Define nodes of search tree and vanilla bfs search algorithm

Author: Tony Lindgren
'''

import queue
# list operations are good when the operation is done at end of list
from time import process_time
from dataclasses import dataclass, field
from typing import Any

# (14,<obj>) (14,<obj>) are not comparable in queue because second is not string etc
@dataclass(order=True)
class PrioritizedItem:
  priority: int
  item: Any=field(compare=False)

class Node:
    '''
    This class defines nodes in search trees. It keep track of: 
    state, cost, parent, action, and depth 
    '''
    # static variables access through class. 
    # initalizes through problem definition
    search_cost = 1
    t1_start = process_time() 


    def __init__(self, state, cost=0, parent=None, action=None):
        self.parent = parent
        #self.state = MissionariesAndCannibals(init_state, goal_state)
        self.state = state 
        self.action = action
        self.cost = cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1 
    
    #Implement statstics method
    def statistics(self):
        t1_stop = process_time()
        print('----------------------------')
        print("Elapsed time (s):", t1_stop-Node.t1_start)
        print("Solution found at depth:",self.depth )
        print("Number of nodes explored:", Node.search_cost)
        print("Cost of solution:", self.cost)
        print("Estimated effective branching factor",Node.search_cost**(1/self.depth) )
        print('----------------------------')   
        

    def goal_state(self):
        #self.state = mc
        return self.state.check_goal()

    #Implement pretty_print_solution
    def pretty_print_solution(self,verbose=False):
        # self.state.pretty_print()
        if self.parent !=  None:
            self.parent.pretty_print_solution(verbose)  
            print("action: ",self.action)
        if verbose:
            self.state.pretty_print()


    def successor(self):
        successors = queue.Queue()
        for action in self.state.action:                     
            child = self.state.move(action)      
            if child != None:         
                childNode = Node(child, self.cost + 1, self, action)              
                successors.put(childNode)
        return successors  

    # Implement Stack Data Structure (LIFO)
    def stack_successor(self):
        successors = []
        for action in self.state.action:                     
            child = self.state.move(action)      
            if child != None:         
                childNode = Node(child, self.cost + 1, self, action)              
                successors.append(childNode)
        return successors  
    
    # Implement Greedy Search (Prioritized-low cost-ordered)
    def greedy_successor(self):
        successors_set = queue.PriorityQueue()
        for action in self.state.action:
            child = self.state.move(action)      
            if child != None:
                # no of tiles out of place
                h = self.state.h_val()            
                n = Node(child, self.cost + 1, self, action)
                successors_set.put(PrioritizedItem(h,n))
        return successors_set  

             
class SearchAlgorithm:
    '''
    Class for search algorithms, call it with a defined problem 
    '''
    def __init__(self, problem):
        self.start = Node(problem)        
    
    # Implement Greedy Search
    def greedy_search(self,statistics = False):
        frontier = queue.PriorityQueue()
        # initially any priority is given for set
        frontier.put(PrioritizedItem(0, self.start))   
        stop = False
        explored=[]
        while not stop:
            if frontier.empty():
                return None
            curr_node = frontier.get().item
            explored.append(curr_node.state.state)
            if curr_node.goal_state():
                stop = True 
                #Implement Statstics function
                if statistics:
                    curr_node.statistics()
                return curr_node        
                        
            successor = curr_node.greedy_successor() 
            while not successor.empty():
                node_set = successor.get()
                if node_set.item.state.state not in explored:
                    # print("current states and successor",curr_node.state.state, node_set.item.state.state,"priority" ,node_set.priority)
                    Node.search_cost+=1
                    frontier.put(PrioritizedItem(node_set.priority , node_set.item))


    def bfs(self,statistics=False):
        frontier = queue.Queue()
        frontier.put(self.start)
        stop = False
        # Implement Visited check
        explored=[]
        while not stop:
            if frontier.empty():
                return None
            curr_node = frontier.get()
            explored.append(curr_node.state.state)
            if curr_node.goal_state():
                stop = True 
                #Implement Statstics function
                if statistics:
                    curr_node.statistics()
                return curr_node        
                        
            successor = curr_node.successor() 
            while not successor.empty():
                node = successor.get()
                # print("current states and successor",curr_node.state.state, node.state.state)
                if node.state.state not in explored:
                    # print("current states and successor",curr_node.state.state, node.state.state)
                    Node.search_cost+=1
                    frontier.put(node)

    # Implement DFS
    def dfs(self,statistics = False, limit = float("inf")):
        frontier = []
        frontier.append(self.start)

        stop = False
        explored=[]
        while not stop:
            if len(frontier) == 0:
                return None
            
            curr_node = frontier.pop()
            explored.append(curr_node.state.state)
            if curr_node.goal_state():
                print("stop")
                stop = True 
                if statistics:
                    curr_node.statistics() 
                return curr_node        
            
            # Implement limit cutoff for iterative deepning            
            if limit>curr_node.depth:
                successor = curr_node.stack_successor() 
                while not len(successor) == 0:
                    node = successor.pop()
                    if node.state.state not in explored:
                        Node.search_cost+=1
                        frontier.append(node)

    # Implement IDFS
    def idfs(self,statistics = False):
        max_depth = 100000 #to stop infinite loop
        for i in range(1, max_depth):
            goal = self.dfs(limit=i,statistics = statistics )
            if goal != None:
                return goal
        print("No solution - increase max depth or there is no solution")
    
