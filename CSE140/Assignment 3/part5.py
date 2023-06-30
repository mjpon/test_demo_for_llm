import numpy as np
import sys
import math
import random
import copy

 
def make_maze(n: int,  x: int ):
    maze = np.random.randint(1,n, size=(n, x))

    for i in range(n):
        for j in range(n):
            min1 = 1
            max1 = max(i, n-1-i, n-1-j, j)
            # print(max1)
            maze[i][j]= random.randint(min1,max1)
    maze[n-1][x-1] = 0
    return maze
def print_arr(board):
    n = len(board)
    niceBoard = " "
    #not sure why the heck its off by one? but ok?????
    for r in range(n):
        for c in range(n-1):
            if board[r][c] is None:
                niceBoard += "-- "
            else:
                #remember to case
                niceBoard += str(board[r][c]) + "  " 
        if board[r][n-1] is None:
            niceBoard += "--\n "
        else:
            # end of the line buddy
            niceBoard += str(board[r][n-1]) + "\n "
    print(niceBoard)

# check if we can actually add this value to the graph, cuz it may not be possible iwth length
def impossibleYes(curr_node, length):
    if curr_node[0] < 0 or curr_node[1] < 0:
        return False
    if curr_node[0] >= length or curr_node[1] >= length:
        return False
    return True

def get_score(part2: list,n:int):
    # print(part2)
    # score = np.sum(grant)
    if None is part2[n-1][n-1]:
        return 10000000
    return part2[n-1][n-1] * -1

def generate_randomRange(i, j, n: int):
    # for i in range(n):
    #     for j in range(n):
    min1 = 1
    max1 = max(i, n-1-i, n-1-j, j)
    # print(max1)
    return random.randint(min1,max1)

def solve_maze(board,length: int):

    # frontier = []
    # explored = []
    # dist =  np.empty((length, length))
    dist = [None] * length
    for i in range(length):
        dist[i] = [None] * length
    dist[0][0] = 0
    depth = 0
    # print(dist)
    # frontier.append(board[0][0])
    while True:
        connected_nodes = []
      
        #do an iterative search to find nodes farthest traveled
        for r in range(length):
            for c in range(length):
                #find the nodes that have the next depth, so we can check them
                # and then visit them to keep checking their possible succ
                if dist[r][c] == depth:
                    connected_nodes.append((r, c))
        if len(connected_nodes) == 0:
            break 
        #handling the stupid tuple and checking the children
        # check if the child? nodes are in this. Return the child node if it is, or at least add it 
        # print("HASMMOND!", connected_nodes)

        #look at all the successors and ssing where there possible lengths go and then adding them to the dist board
        for i in range(len(connected_nodes)):
        # for i in range(len(connected_nodes)):
            curr_node = connected_nodes.pop()
            jump_dist = board[curr_node[0]][curr_node[1]] # get the array cube's value we are on now to do the jump
            # check the jumps
            up = (curr_node[0] - jump_dist, curr_node[1])
            down = (curr_node[0] + jump_dist, curr_node[1])
            left = (curr_node[0], curr_node[1] - jump_dist)
            right = (curr_node[0], curr_node[1] + jump_dist)


            # if the jump is valid and we haven't visited it yet, set the depth to be + 1
            # each step is +1
            if impossibleYes(up,length):
                if dist[up[0]][up[1]] is None:
                    dist[up[0]][up[1]] = depth + 1
            if impossibleYes(down, length):
                if dist[down[0]][down[1]] is None:
                    dist[down[0]][down[1]] = depth + 1
            if impossibleYes(left, length):
                if dist[left[0]][left[1]] is None:
                    dist[left[0]][left[1]] = depth + 1
            if impossibleYes(right, length):
                if dist[right[0]][right[1]] is None:
                    dist[right[0]][right[1]] = depth + 1
            # print(dist)
        # increase the depth for the next interation if there is one from the placement above
        depth+=1

    return dist

def hill_climbStoich(board, length, iterations:int):
    ''' j =  board that is randomly generated
        j' = that is randomly generated, the orignal board that is changed with one single cell
        step = function to chose one cell in j to change
        this is wherere one cell is picked randomly out of j (not goal) than placed with a new number

        e = the item where we would compare for the min
        moves previous j vs now j'

   '''
    i = 0
   #numpy to make things a bit easier
    part2= np.array(solve_maze(board, length))
    score_best = get_score(part2,int(the_input))
    # score_je = get_score(part2,int(the_input))
    best_board = board
    boardJ = board
    curr_board = board
    # print(part2)
    # print(get_score(part2,int(the_input)))

    # while
    randomCol = random.randint(0,length-1)
    randomRow = random.randint(0,length-1)

    while (randomCol == length-1 and randomRow == length-1):
        randomCol = random.randint(0,length-1)
        randomRow = random.randint(0,length-1)
    
    for i in range(iterations):
         # #change the board apparently 


        # prev_board, calc
        # curr_board = boardJ
        j_s = np.array(solve_maze(curr_board, length))
        score_e = get_score(j_s,int(the_input))
    
        
        # calculate the new board
        new_board_cell = generate_randomRange(randomCol, randomRow,length)
        boardJ[randomCol][randomRow] = new_board_cell
        j_s = np.array(solve_maze(boardJ, length))
        # energy function
        score_je = get_score(j_s,int(the_input))

        # compare the values of the board new vs old
        if score_je <= score_e:
            curr_board = boardJ
            if score_je <= score_best:
                best_board = boardJ
                score_best = score_je

        # print_arr(curr_board)
        # i+=1

    return best_board

def hill_climb4(board, length, iterations:int, searches: int):
    ''' j =  board that is randomly generated
        j' = that is randomly generated, the orignal board that is changed with one single cell
        step = function to chose one cell in j to change
        this is wherere one cell is picked randomly out of j (not goal) than placed with a new number

        e = the item where we would compare for the min
        moves previous j vs now j'

   '''
    i = 0
   #numpy to make things a bit easier
    part2= np.array(solve_maze(board, length))
    score_best = get_score(part2,length)
    best_board = board
    curr_board = board

    # intialize the board
    boardJ = board


    # randomCol = random.randint(0,length-1)
    # randomRow = random.randint(0,length-1)
    # print(part2)
    # print(get_score(part2,int(the_input)))
    for j in range(searches):
        for i in range(iterations):
            # #change the board apparently 


            # prev_board, calc
            # curr_board = boardJ
            j_s = np.array(solve_maze(curr_board, length))
            # energy function
            score_e = get_score(j_s,length)
            
            randomCol = random.randint(0,length-1)
            randomRow = random.randint(0,length-1)
            
            # calculate the new board
            new_board_cell = generate_randomRange(randomCol, randomRow,length)
            boardJ[randomCol][randomRow] = new_board_cell
            j_s = np.array(solve_maze(boardJ, length))
            score_je = get_score(j_s,length)

                # compare the values of the board new vs old
            if score_je <=  score_e:
                curr_board = boardJ
                if score_je <= score_best:
                    best_board = boardJ
                    score_best = score_je

            # print(i)
            # i+=1

    return best_board
def hill_climb5(board, length, iterations:int, probability: float):
    ''' j =  board that is randomly generated
        j' = that is randomly generated, the orignal board that is changed with one single cell
        step = function to chose one cell in j to change
        this is wherere one cell is picked randomly out of j (not goal) than placed with a new number

        e = the item where we would compare for the min
        moves previous j vs now j'

   '''
    i = 0
   #numpy to make things a bit easier
    part2= np.array(solve_maze(board, length))
    score_best = get_score(part2,int(length))
    # score_je = get_score(part2,int(the_input))
    best_board = copy.deepcopy(board)
    boardJ = copy.deepcopy(board)
    curr_board = copy.deepcopy(board)
    # print(part2)
    # print(get_score(part2,int(the_input)))
    randomCol = random.randint(0,length-1)
    randomRow = random.randint(0,length-1)


    while (randomCol == length-1 and randomRow == length-1):
        randomCol = random.randint(0,length-1)
        randomRow = random.randint(0,length-1)
    

    for i in range(iterations):
         # #change the board apparently 


        # prev_board, calc
        # curr_board = board
        j_s = np.array(solve_maze(curr_board, length))
        score_e = get_score(j_s,int(length))
        
        randomCol = random.randint(0,length-1)
        randomRow = random.randint(0,length-1)


        while (randomCol == length-1 and randomRow == length-1):
            randomCol = random.randint(0,length-1)
            randomRow = random.randint(0,length-1)
        
        # calculate the new board
        boardJ = curr_board
        new_board_cell = generate_randomRange(randomCol, randomRow,length)
        boardJ[randomCol][randomRow] = new_board_cell
        j_s = np.array(solve_maze(boardJ, length))
        # energy function
        score_je = get_score(j_s,int(length))

        # compare the values of the board new vs old
        if score_je <=  score_e:
            curr_board = copy.deepcopy(boardJ)
            if score_je <= score_best:
                best_board = copy.deepcopy(boardJ)
                score_best = score_je
        elif probability > random.uniform(0,1):
            curr_board = copy.deepcopy(boardJ)
            if score_je <= score_best:
                best_board = copy.deepcopy(boardJ)
                score_best = score_je
        else:
            board_J = copy. deepcopy(curr_board)


        # print(i)
        # i+=1

    return best_board
def hill_climb6(board, length, iterations:int, temp: float, decay: float):
    ''' j =  board that is randomly generated
        j' = that is randomly generated, the orignal board that is changed with one single cell
        step = function to chose one cell in j to change
        this is wherere one cell is picked randomly out of j (not goal) than placed with a new number

        e = the item where we would compare for the min
        moves previous j vs now j'

   '''
    i = 0
   #numpy to make things a bit easier
    part2= np.array(solve_maze(board, length))
    score_best = get_score(part2,int(the_input))
    # score_je = get_score(part2,int(the_input))
    best_board = board.deepcopy()
    boardJ = board.deepcopy()
    curr_board = board.deepcopy()
    # print(part2)
    # print(get_score(part2,int(the_input)))
    temptemp = temp


    randomCol = random.randint(0,length-1)
    randomRow = random.randint(0,length-1)

    while (randomCol == length-1 and randomRow == length-1):
        randomCol = random.randint(0,length-1)
        randomRow = random.randint(0,length-1)
    

    for i in range(iterations):
         # #change the board apparently 


        # prev_board, calc
        # curr_board = boardJ
        j_s = np.array(solve_maze(curr_board, length))
        score_e = get_score(j_s,int(length))
        
        # randomCol = random.randint(0,length-1)
        # randomRow = random.randint(0,length-1)
        
        # calculate the new board
        new_board_cell = generate_randomRange(randomCol, randomRow,length)
        boardJ[randomCol][randomRow] = new_board_cell
        j_s = np.array(solve_maze(boardJ, length))
        # energy function
        score_je = get_score(j_s,int(length))
        workyouuselessmachine = random.uniform(0,1) # not probablity
        # compare the values of the board new vs old
        if score_je <= score_e:
            curr_board = boardJ.deepcopy()
            if score_je <= score_best:
                best_board = boardJ
                score_best = score_je
        elif (workyouuselessmachine < math.exp((score_e-score_je)/temptemp)):
            curr_board = boardJ.deepcopy()
            if score_je <= score_best:
                best_board = boardJ.deepcopy()
                score_best = score_je

        # print(i)
        # i+=1
        temptemp = temptemp*decay #where d is the iteration temperature decay

    return best_board

# part 1
the_input = input("Rook Jumping Maze size (5-10)?: ")
# stupid casting lol, other it gives type errors
# grant = make_maze(int(the_input),int(the_input))
# grant = np.array([[1, 4, 2, 2, 2,],[3, 2, 1, 3, 3],[2, 2, 1 ,2 ,2], [3, 1, 2, 2, 4], [1, 4 ,2 ,3 ,0]])


# part 4
# grant = np.array([[2, 1, 1, 4, 3],[2, 2, 3, 1, 4],[3, 2, 2 ,3 ,3], [3, 3, 1, 1, 3], [4, 1 ,3 ,4 ,0]])

# part 5
grant = np.array([[1, 4, 3, 1, 1,],[3, 2, 3, 2, 1],[2, 2, 1 ,3 ,1], [2, 1, 3, 2, 1], [1, 4 ,1 ,4 ,0]])

#part 6 check
# grant = np.array([[1, 3, 1, 3, 3,],[4, 3, 3, 2, 4],[1, 1, 2 ,3 ,2], [2, 3, 2, 2, 4], [3, 1 ,4 ,2 ,0]])
# 3 2 1 3 3
# 2 2 1 2 2
# 3 1 2 2 4
# 1 4 2 3 0
# iterations = input("Iterations?: ")
# print_arr(grant)

# part 2
# print("Moves from start:")
# part2= np.array(solve_maze(grant, int(the_input)))
# print_arr(part2)
# print(get_score(part2,int(the_input)))
# print_arr(part2)
n = int(the_input)  


# part 3
# iterations = input("Iterations?: ")
# new board that is is placed with x random changes
# board_J = hill_climbStoich(grant,int(n), int(iterations))
# part2= np.array(solve_maze(board_J, int(the_input)))
# print("Moves from start:")
# # print(part2)
# print_arr(part2)
# print(get_score(part2,int(the_input)))

# part 4
# iterations = input("Iterations?: ")
# searches = input("Hill descents?: ")
# print_arr(grant)
# # new board that is is placed with x random changes and y searches
# board_J = hill_climb4(grant,n, int(iterations), int(searches))
# part4= np.array(solve_maze(board_J, int(the_input)))
# # print(part4)
# print_arr(part4)
# print(get_score(part4,int(the_input)))


# # part 5

iterations = input("Iterations?: ")
probability = input("Uphill step probability?: ")
# new board that is is placed with x random changes and y searches
board_J = hill_climb5(grant,n, int(iterations), float(probability))
part4= np.array(solve_maze(board_J, n))
print_arr(part4)
print("Moves from start:")
print_arr(part4)
# print_arr(part4)
print(get_score(part4,int(the_input)))
# print(int(the_input))


# part 6
# iterations = input("Iterations?: ")
# temp = input("Initial temperature?: ")
# decay = input("Decay rate?: ")
# # new board that is is placed with x random changes and y searches
# board_J = hill_climb6(grant,int(n), int(iterations), float(temp), float(decay))
# part4= np.array(solve_maze(board_J, int(the_input)))
# print(part4)
# print_arr(part4)
# print(get_score(part4,int(the_input)))



#knapsack problem?
# is this using a DP method?
# Sample Transcripts:
# 2 2 2 4 3
# 2 2 3 3 3
# 3 3 2 3 3
# 4 3 2 2 2
# 1 2 1 4 0
# Moves from start:
# 0 3 1 4 2
# 7 5 5 6 4
# 1 4 2 2 3
# 5 6 4 -- 3
# -- 4 3 4 5
# -5