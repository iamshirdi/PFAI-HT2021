'''
Four in a row

Author: Tony Lindgren
'''
from copy import deepcopy

class FourInARow:
    def __init__(self, player, chip):
        new_board = []
        for _ in range(7):
            new_board.append([])
        self.board = new_board
        self.action = list(range(7)) #7columns instead of rows
        if chip != 'r' and chip != 'w':
            print('The provided value is not a valid chip (must be, r or w): ', chip)
        if player == 'human' and chip == 'w':
            self.ai_player = 'r'
        else:
            self.ai_player = 'w'
        self.curr_move = chip #current move assigned initial
    
    def to_move(self): #whose move was previous
        return self.curr_move
        
    #actions return how many columns can be filled 
    #TODO
    def actions(self):
        rows_columns =[]
        for c in range(len(self.board)): # 7 columns of 6 elements
            if len(self.board[c]) <6: 
                rows_columns.append(c) 
        return rows_columns
        


    def result(self, action):                    
        dc = deepcopy(self)
        if self.to_move() == 'w':
            dc.curr_move = 'r'
            dc.board[action].append(self.to_move())   
        else:
            dc.curr_move = 'w'
            dc.board[action].append(self.to_move())            
        return dc
        
    #eval
    #TODO
    def utility(self, state):
        #edges : low score 
        for i in range(3):
            v = (2**i) * len(state[i])    #first 0,1,2
            v += (2**i) * len(state[6-i]) #last 6,5,4

        #middle score
        v += (2**3) * len(state[3])
        return v
        
    def is_terminal(self):
        #check vertical
        for c in range(0, len(self.board)):
            count = 0
            curr_chip = None
            for r in range(0, len(self.board[c])):
                if curr_chip == self.board[c][r]:
                    count = count + 1
                else:
                    curr_chip = self.board[c][r]     
                    count = 1
                if count == 4:
                    if self.ai_player == curr_chip:        
                        # print('Found vertical win')
                        return True, 1000          #MAX ai wins positive utility
                    else:
                        # print('Found vertical loss')
                        return True, -1000         #MIN player wins negative utility
                    
        #check horizontal 
        #TODO
        for r in range(0, 6): #6 rows
            curr_chip = None
            count = 0
            for c in range(0, len(self.board)):
                if len(self.board[c]) >r : # check if elements are present or not
                    if curr_chip == self.board[c][r]:
                        count = count + 1
                    else:
                        curr_chip = self.board[c][r]     
                        count = 1
                    if count == 4:
                        if self.ai_player == curr_chip:        
                            # print('Found horizontal win')
                            return True, 1000          #MAX ai wins positive utility
                        else:
                            # print('Found horizontal loss')
                            return True, -1000         #MIN player wins negative utility                
                            
        #check positive diagonal
        for c in range(7-3):  #4 (0,1,2,3)
            for r in range(6-3): #3 (0,1,2)
                if len(self.board[c]) > r and len(self.board[c+1]) > r+1 and len(self.board[c+2]) > r+2 and len(self.board[c+3]) > r+3:
                    if self.ai_player == self.board[c][r] and self.ai_player == self.board[c+1][r+1] and self.ai_player == self.board[c+2][r+2] and self.ai_player == self.board[c+3][r+3]:  
                        # print('Found positive diagonal win')
                        return True, 1000
                    elif self.ai_player != self.board[c][r] and self.ai_player != self.board[c+1][r+1] and self.ai_player != self.board[c+2][r+2] and self.ai_player != self.board[c+3][r+3]:  
                        # print('Found positive diagonal loss')
                        return True, -1000
        
        #check negative diagonal 
        #TODO   
        for c in range(4):
            for r in range(2,-1,-1):
                if len(self.board[c]) > 6- r and len(self.board[c+1]) >6-r-1 and len(self.board[c+2]) > 6-r-2 and len(self.board[c+3]) > 6-r-3:
                    if self.ai_player == self.board[c][6-r-1] and self.ai_player == self.board[c+1][6-r-2] and self.ai_player == self.board[c+2][6-r-3] and self.ai_player == self.board[c+3][6-r-4]:  
                        # print('Found negative diagonal win')
                        return True, 1000
                    elif self.ai_player == self.board[c][6-r-1] and self.ai_player == self.board[c+1][6-r-2] and self.ai_player == self.board[c+2][6-r-3] and self.ai_player == self.board[c+3][6-r-4]:  
                        # print('Found negative diagonal loss')
                        return True, -1000

        #check draw - no more positions left to win :
        # another complex check: atleast 4 positions remaining and the 4th position move shouldnt result in win or loss
        #TODO  
        col = 1
        for c in self.board: #7 columns
            if len(c) != 6:  #6 rows in column
                break 
            if col == 7:
                return True, 0
            col+=1
            
        # TODO default 0 return utlity
        u_value = self.utility(self.board)  
        # return False, 0                                       
        return False, u_value                


    #pretty_print - from bottom
    #TODO
    def pretty_print(self):
        for r in range(5,-1,-1):
            for c in range(7):
                if len(self.board[c]) > r:
                    print(self.board[c][r], end=" ")
                else:
                    print("_", end=" ")
            print()


# a=[[1,2], [3],[], [], [], [], [5,6,7,8,9,10] ]
# for r in range(5,-1,-1):
#   for c in range(7):
#       if len(a[c]) > r:
#           print(a[c][r], end=" ")
#       else:
#           print("_", end=" ")
#   print()