'''
Missionaries and Cannibal problem

Author: Tony Lindgren
'''
from copy import deepcopy

class EightPuzzle:
    
    def __init__(self, initial_state, goal):
        self.state = initial_state
        self.goal = goal             
        self.action = ['l','r', 'u', 'd'] 
        self.goal_axis = {'e': (0, 0), 1: (0, 1), 2: (0, 2), 3: (1, 0), 4: (1, 1), 5: (1, 2), 6: (2, 0), 7: (2, 1), 8: (2, 2)}
    
    # Static value for faster processing instead of / or //, enumerate by 3
    # g = [['e',1,2],[3,4,5],[6,7,8]]
    # goal_axis ={}
    # row_index=0
    # for row in g:
    # col_index = 0
    # for value in row:
    #     goal_axis[value] = (row_index, col_index)
    #     col_index+=1
    # row_index+=1
    # print(goal_axis)    

           
    def check_goal(self):                                
        if self.state == self.goal:        
            return True
        else:
            return False

    # Implement heuristic distance
    def h_val(self):
        # no of tiles out of place
        h_1 = 0
        # manhattan distance
        h_2 = 0

        # keep track of row and column index 
        row_index = 0
        for state_row, goal_row in zip(self.state, self.goal):
            col_index = 0
            # each row check out of place elements by comparing it to goal
            for i,j in zip(state_row, goal_row):
                # empty/blank tile is not considered : only 8 numbers
                if i!=j and i!='e':
                    h_1 += 1
                    h_2 = h_2 + abs (row_index - self.goal_axis[i][0]) + abs (col_index - self.goal_axis[i][1])
                col_index += 1
            row_index += 1
        
        h_0 = h_1 + h_2
        return h_0

    def move(self, move):                               
        if move =='l':
            # To prevent present state changing when calculating all actions of the state
            # deep copy copies values to inner lists instead of references
            dc = deepcopy(self)
            if dc.l():
                return dc
        elif move =='r':
            dc = deepcopy(self)
            if dc.r():
                return dc
        elif move =='u':
            dc = deepcopy(self)
            if dc.u():
                return dc    
        elif move =='d':
            dc = deepcopy(self)
            if dc.d():
                return dc

            
    def l(self):
        for row in self.state:
            if 'e' in row:
            # check if not in 1st column so that left action is possible
                if 'e' != row[0]:
                    empty_index = row.index('e')
                    #swap to left / update state
                    row[empty_index-1], row[empty_index] = row[empty_index], row[empty_index-1]  
                    return True 

    def r(self):
        for row in self.state:
            if 'e' in row:
               if 'e' != row[-1]:
                    empty_index = row.index('e')
                    row[empty_index+1], row[empty_index] = row[empty_index], row[empty_index+1]  
                    return True 

    def u(self):
        for i,row in enumerate(self.state):
            # return if e in top row since no up action is possible
            if 'e' in row: 
                if i==0:
                    return    
                empty_index = row.index('e')
                self.state[i][empty_index], self.state[i-1][empty_index] = self.state[i-1][empty_index], self.state[i][empty_index]  
                return True 
            
    def d(self):
            for i,row in enumerate(self.state):
                # elimate bottom row for down action to be possible       
                if i!=2 and 'e' in row:
                    empty_index = row.index('e')
                    self.state[i][empty_index], self.state[i+1][empty_index] = self.state[i+1][empty_index], self.state[i][empty_index]  
                    return True 
        
    
    def pretty_print(self):
        print('----------------------------')
        print(' # Current State: ', self.state)
        # print(' #Final State: ', self.goal)
        print('----------------------------')