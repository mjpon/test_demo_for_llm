# Mitchell Pon
# 1591702
# Citations: https://www.youtube.com/watch?v=zp3VMe0Jpf8&t=13s, https://www.youtube.com/watch?v=MMLtza3CZFM&t=4606s , https://www.youtube.com/watch?v=l-hh51ncgDI , https://www.youtube.com/watch?v=y7AKtWGOPAE&t=972s 
#https://courses.cs.washington.edu/courses/cse573/10au/slides/cse573-expectimax.pdf , https://cs.nyu.edu/~fergus/teaching/ai/slides/lecture7.pdf
#
#  Michelle Parent, a former student of this course explained a huge breakdown of how it worked. Anything that looks similar is NOT intentional. All below is self work. 



import numpy as np

#got tired of rewriting things
INF = 9999999
NEG_INF = -9999999

class AIPlayer:

    # apparently there is a temp var we set
    Max_Depth = 6



    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    # first empty row that is nearest
    def get_closet_empty_row(self, board, col):
        # placement of where it is on the board, and some disgusting python shortcut i keep forgetting how it works lol
        row_values = list(board[:, col])
        # print(row_values, "row values")
        # any option not use yet
        if 0 in row_values:
            # get the row with the value in it but the position where there is a zero value
            return 6 - row_values[::-1].index(0) - 1
        else:
            return -1

    # Returns all possible actions that we can take from the empty positions
    def actions(self, board):
        possibleActions = []
        # HAS TO BE COLUMN NUMBERS YOU NITWITED NINE PIN
        cols = np.arange(7)
        # print(cols, "cols")
        #which row is the first empty starting from the bottom
        for col in cols:
            
            # go throught each col starting from the bottom
            # going through every row
            # returns value that is empty, the closest empty
            row_num = self.get_closet_empty_row(board, col)
            # well if the rows actually exists
            # print(row_num, "row_num")
            if row_num != -1:
                possibleActions.append((row_num, col))
                #array of tuples
        return possibleActions   

    # checks if the game is done via a 4 line,  returns a bool
    # same as the eval function logic ugh
    #  https://www.youtube.com/watch?v=MMLtza3CZFM more diagnoal horror
    def terminal_test(self, board):
        #left and right rows
        for r in range(6):
            row = board[r]
            for c in range(7-3): # counts all the groups of 4
                vision = list(row[c:c+4])
                # remember player versus opponent thing here.
                if vision.count(self.player_number) == 4 or vision.count((self.player_number * 2) % 3) == 4:
                    return True
        # up and down vertical check
        for c in range(7):
            row_array = list(board[:, c])
            for r in range(6-3):
                vision = row_array[r:r+4]
                if vision.count(self.player_number) == 4 or vision.count((self.player_number * 2) % 3) == 4:
                    return True
        # diagonal left to right down
        for c in range(7-3):
            for r in range(6-3):
                vision = [board[r][c], board[r+1][c+1], board[r+2][c+2], board[r+3][c+3]]
                if vision.count(self.player_number) == 4 or vision.count((self.player_number * 2) % 3) == 4:
                    return True
        # # #diagonal left to right up
        for c in range(7-3):
            for r in range(3, 6):
                vision = [board[r][c], board[r-1][c+1], board[r-2][c+2], board[r-3][c+3]]
                if vision.count(self.player_number) == 4 or vision.count((self.player_number * 2) % 3) == 4:
                    return True
        return False
        


    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        depth = 0
        # action_tuple = self.max_value(board, NEG_INF, INF, depth)
        # we get the col of the action, which is the right on the tuple
        #we start out with max cuz the algorithm is like that. Look at the slides for erfernces
        action_tuple = self.max_value(board, NEG_INF, INF, depth)
        # added none check to fix the stalemate situation (out of bounds)
        return None if action_tuple[1] is None else action_tuple[1][1]

    def min_value(self, board, alpha, beta, depth):
        v = 999999999
        # ExpectedMaxDepth = 5
        # get all actions
        actions = self.actions(board)
         # set action to be the first in the array, because of the max function needs a baseline
        # print(actions, "min")

        # if we are out of moves and well its pretty much a stalemate
        # if actions[0] is None:
            # return (self.evaluation_function(board),[])
        # added none to fix the stalemate situation (out of bounds), other it would throw exception
        action_baseline = None
        if self.terminal_test(board) or depth == self.Max_Depth:
            # print(self.evaluation_function(board))
            return (self.evaluation_function(board),action_baseline)
        for action in actions:
            # always set the board(
            board[action[0]][action[1]] = (self.player_number*2)% 3
            # need to seperate since well... max() doesnt allow us to see if one is greater than other for actions
            maxV = self.max_value(board, alpha, beta, depth+1)
            # no equals greater is needed her.... typo at first
            if (v > maxV[0]):
                action_baseline = action
                v = maxV[0]
            if v <= alpha:
                #WE DONT NEED TO USE THIS, STOP!!!
                board[action[0]][action[1]] = 0
                # STOP!!! IGNORE, THIS IS THE PRUNE, NO NEED TO KEEP LOOKING!!
                return (v, action)
            beta = min(beta, v)
            board[action[0]][action[1]] = 0
        return (v,action_baseline)

    
    
    
    def max_value(self, board, alpha, beta, depth):
        v = -999999999
        # ExpectedMaxDepth = 5
        # get all actions
        actions = self.actions(board)
        # print(actions, " max")
         # set action to be the first in the array, because of the max function needs a baseline
        # if actions[0] is None:
        # added none to fix the stalemate situation (out of bounds), other it would throw exception
        action_baseline = None
        if self.terminal_test(board) or depth == self.Max_Depth:
            # print(self.evaluation_function(board))
            return (self.evaluation_function(board),action_baseline)
        for action in actions:
            # always set the board
            board[action[0]][action[1]] = self.player_number
            # need to seperate since well... max() doesnt allow us to see if one is greater than other for actions
            minV = self.min_value(board, alpha, beta, depth+1)
            if (v < minV[0]):
                action_baseline = action
                v = minV[0]
            if v >= beta:
                #WE DONT NEED TO USE THIS, STOP!!!
                board[action[0]][action[1]] = 0
                # STOP!!! IGNORE, THIS IS THE PRUNE, NO NEED TO KEEP LOOKING!!
                return (v, action)
            alpha = max(alpha, v)
            board[action[0]][action[1]] = 0
        return (v,action_baseline)

        # return self.expectimax_max_value(board, depth) if hammond is AnIdiot else self.expectimax_exp_value(board, depth)


    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.
        This will play against the random player, who chooses any valid move
        with equal probability
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them
        RETURNS:
        The 0 based index of the column that represents the next move

        Expectimax starts out with max value cuz a. top of the tree, b. we want the best move for the AI.
         Then it will factor in the expected move that the AI opponent will make, in exp_value. In exp_value, 
         it also does the same, by looking at every action and seeing the values possible for our AI.... 
         and then factors it into its calculation so this back and forth prediction keeps going till we run out of depth

        """
        # i guess do this for now until we get worse
        depth = 0 
        # we are always going to start out with max regardless, LOOK AT THE SLIDES AND THE ALGORITHM TREE STRUCTURE
        # remember get that stupid column apparently

        # None if action_tuple[1] is None else action_tuple[1][1]
        return self.bestValueWalmart(board, depth, True)[1][1]

        # raise NotImplementedError('Whoops I don\'t know what to do')

    def bestValueWalmart(self, board, depth, playerType):
        
        AnIdiot = True
        hammond = playerType
        # maxplayer is the ai , WE WANT AI TO WIN
        # checks if we are not at the depth or 
        # max depth, lower the depth, the faster it runs, we set the constant
        if self.terminal_test(board) or depth == 3:
            # print(self.evaluation_function(board))
            return self.evaluation_function(board)
        return self.expectimax_max_value(board, depth) if hammond is AnIdiot else self.expectimax_exp_value(board, depth)

    # this would be the AI
    def expectimax_max_value(self, board, depth):
        v = -999999999
        # get all actions
        actions = self.actions(board)
         # set action to be the first in the array, because of the max function needs a baseline
        action_baseline = actions[0]
        #    actions  = [()] 
        # all actions here are the head , or possible methods of advancement
        # eval for every single action sin actions
        #placing the piece all the row possiblities,  and get the ultilty
        for action in actions:
            # set the action in the board, set it equal to the player number 0 1 2 
            board[action[0]][action[1]] = self.player_number
             # determine the value, by the amount of depth we need to be, this is recursive, 
            # DFS kinda of thing, 
            # three moves into the furure for example
            #take the value, evalulate function and compare
            # also we switch functions since we going back and forth on what movies the player or ai may take
            exp_v = self.bestValueWalmart(board, depth+1, False)
            if exp_v > v:
                action_baseline = action
                v = exp_v
            # # reset the board after we make the prediction
            # we havent done that move yet       
            board[action[0]][action[1]] = 0   # reset the board back everytime we make a eval

        return (v, action_baseline)

    # handling the random player
    def expectimax_exp_value(self, board, depth):
        v = 0
        # this means the value at the current state, the best acheivle outcome ultilty
        actions = self.actions(board)
        for action in actions:
            # basically, this is some funky math in order to get it to be the opposite everytime
            # 2 * 2 mod 3  =1 the 1 * 2 mode 3  =  2
            board[action[0]][action[1]] = (self.player_number*2)% 3
            # value remember means the best achievable outcome from the succ
            # and we factor in our calcuation here to what the opponent may think of us
            value = self.bestValueWalmart(board, depth+1, True)
            #type check cuz.... sometimes it's not a tuple????
            if type(value) is tuple:
                # the TA gave this to students in the Summer session apparently?
                # , this the prob funtion, but yea look at the slides, they make sense in this case
                # each action has the same prob to be played, think of connect 4 logic. cuz we cannot say what exact move the person will take
                v += (1.0/(len(actions)))*value[0] # also check the type, since max returns a tuple, so get the first not the second item

            # you boofoon, you forgot to add this....
            board[action[0]][action[1]] = 0 # reset the board back
        return v



    #      based if this for calculations https://www.youtube.com/watch?v=y7AKtWGOPAE  
    def check_window(self, current, empty, opponent):    

        # you may ask why these numbers are the best? well, it got it to be here and now its just working well lol
        # i guess 100s or the 10s wasnt enough "change" for the algorithm
        utility = 0
        if current == 3 and empty == 1:
            utility += 200
        elif current == 2 and empty == 2:
            utility += 50
        # avoid this situation cuz if we do it, well we NEED TO STOP IT!!    Also to stop that stupid 4 bottom condtions
        elif current == 1 and opponent == 3:
            utility += 1000
        # # fix the problem of ignore the enemy's advancment into non homesoil territory    
        # elif opponent == 2 and empty == 2:
        #     utility -= 20
        # dont want to give the enemy the advantage!!!!!!    
        if opponent == 3 and empty == 1:
            utility -= INF
        return utility
    # returnt he value of the item that is being placed
    # after last move ie placed, total value of possible game win

    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them
        RETURNS:
        The utility value for the current board
        """
        # basically, this is some funky math in order to get it to be the opposite everytime
        # 2 * 2 mod 3  =1 the 1 * 2 mode 3  =  2
        # check which player we are on
        if self.player_number is 2:
            opponent_num = 1
        else: 
            opponent_num = 2

        # think of windows , 4 to win
        # @ of alll the moves that ar possible, which are the best ones 
        # temp place one at everyone, everytime i place the piece, im going to evalutet  what my ultiy is,
        # if i place my piece, and it reutrn connect 4 amazin move

        # doing the start in the middle or stop and the middle since we go out of bounces
        ulitily = 0
        BEST = 1000000000 # basically the best move, just return it since we WINNNNNNNNNN and nothin CAN STOP US
        # 6 rows, so check 
        for i in range(6):
            row = board[i]
            for col in range(7-3):
                vision = list(row[col:col+4]) # we want to check right 4
                empty = vision.count(0)
                me = vision.count(self.player_number)
                oppsite = vision.count(opponent_num)
                # count the number of pucks we see so far
                if me == 4:
                    return (BEST)
                else:
                    ulitily += self.check_window(me, empty, oppsite)
        # check for the columns
         # 7 col, so check 
        for i in range(7):
            col = list(board[:, i])
            for row in range(6-3):
                vision = col[row:row+4] # we want to check right 4
                empty = vision.count(0)
                me = vision.count(self.player_number)
                oppsite = vision.count(opponent_num)
                # count the number of pucks we see so far
                if me == 4:
                    return (BEST)
                else:
                    ulitily += self.check_window(me, empty, oppsite)
         # uphill
        for c in range(7-3):
            for r in range(6-3):
                vision = [board[r][c], board[r+1][c+1], board[r+2][c+2], board[r+3][c+3]]
                empty = vision.count(0)
                me = vision.count(self.player_number)
                oppsite = vision.count(opponent_num)
                # count the number of pucks we see so far
                if me == 4:
                    return (BEST)
                else:
                    ulitily += self.check_window(me, empty, oppsite)
        # downhill
        for c in range(7-3):
            for r in range(6-3):
                vision = [board[r][c], board[r-1][c+1], board[r-2][c+2], board[r-3][c+3]]
                empty = vision.count(0)
                me = vision.count(self.player_number)
                oppsite = vision.count(opponent_num)
                # count the number of pucks we see so far
                if me == 4:
                    return (BEST)
                else:
                    ulitily += self.check_window(me, empty, oppsite)


        return ulitily


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them
        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them
        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move