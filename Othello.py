
import copy
import random
import os

# global vars
global GRID
global SHIFTS
global COLOUR
global DIMS
global CORNERS
global OFF_CORNERS
global EDGES
global CORNER_BONUS
global DEFAULT_DEPTH
global CENTRE_LEFT
global CENTRE_RIGHT
global GRADING_STRATEGY

GRID = {
    'G2I' : {'row': {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, 
                    '8': 7},
            'col':{'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6,
                    'H': 7},
            },
    'I2G':{'row': {'0': '1', '1': '2', '2': '3', '3': '4', '4': '5',
                    '5': '6', '6': '7', '7': '8'},
        'col': {'0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E', '5': 'F',
                    '6': 'G', '7': 'H', }
            }
        } 

COLOUR = {
    'b': 'Black',
    'w': 'White'
}

SHIFTS = [-1, 0, 1]
DIMS = 6

CENTRE_LEFT, CENTRE_RIGHT = int(DIMS/2 - 1 ), int(DIMS/2)

CORNERS = [
    (0, 0),
    (0, DIMS-1),
    (DIMS-1,0),
    (DIMS-1, DIMS-1)
]

OFF_CORNERS = [(1, 0), (0, 1), (1, 1),
                (0, DIMS-2), (1, DIMS-1), (DIMS-2, DIMS-2),
                (DIMS-2, 0), (DIMS-1, 1), (DIMS-2, 1),
                (DIMS-2, DIMS-1), (DIMS-1, DIMS-2), (DIMS-2, DIMS-2)]

EDGES = []
for i in [0, DIMS-1]:
    for j in range(DIMS):
        edge_space = (
                    GRID['I2G']['col'][str(i)],
                    GRID['I2G']['row'][str(j)]
                    )
        EDGES.append(edge_space)
for j in [0, DIMS-1]:
    for i in range(DIMS):
        edge_space = (
                    GRID['I2G']['col'][str(i)],
                    GRID['I2G']['row'][str(j)]
                    )
        EDGES.append(edge_space)
EDGES = list(set(EDGES))
    
CORNER_BONUS = 30
DEFAULT_DEPTH = 5

def makeGradingStrategy():
    '''
    Function to make a grading matrix, inspired by code here
    https://github.com/yuxuan006/Othello/blob/ac33536bc35c7e50da93aab937e3dfee5c258a7f/yuchai.py#L19
    '''
    board = []
    for i in range(DIMS):
        row = []
        for j in range(DIMS):
            if (i, j) in CORNERS:
                row.append(10)
            elif (i, j) in OFF_CORNERS:
                row.append(-2)
            elif (i, j) in EDGES:
                row.append(2)
            else:
                row.append(1)
        board.append(row)
    return board

GRADING_STRATEGY = makeGradingStrategy()

# Standard Game Functions
def makeBoard():
    board = []
    for i in range(DIMS):
        row = []
        for j in range(DIMS):
            row.append('.')
        board.append(row)
    board[CENTRE_LEFT][CENTRE_LEFT] = 'b'
    board[CENTRE_RIGHT][CENTRE_RIGHT] = 'b'
    board[CENTRE_LEFT][CENTRE_RIGHT] = 'w'
    board[CENTRE_RIGHT][CENTRE_LEFT] = 'w'
    return board

def dispBoard(board):
    print('  ', end = '')
    for i in range(DIMS):
        print(GRID['I2G']['col'][str(i)], end=' ')
    print()
    for i in range(DIMS):
        print(i+1, end= ' ')
        for j in range(DIMS):
            print(board[i][j], end=' ')
        print()

def generateMoveList(board, player, opponent):
    move_list = []
    end_points = []
    for i in range(DIMS):
        for j in range(DIMS):
            if board[i][j] == opponent:
                possible_moves = pointMove(board, player, opponent, i, j)
                moves, end_points_ij = possible_moves[0], possible_moves[1]
                for move in moves:
                    grid_move = (
                        GRID['I2G']['row'][str(move[0])],
                        GRID['I2G']['col'][str(move[1])]
                    )
                    move_list.append(grid_move)
                for end_point in end_points_ij:
                    end_points.append(end_point)
    return move_list

def pointMove(board, player, opponent, i, j):
    point_moves = []
    end_points = []
    for i_shift in SHIFTS:
        for j_shift in SHIFTS:
            new_i, new_j = i + i_shift, j + j_shift
            if (new_i in range(DIMS)) and (new_j in range(DIMS)):
                if board[new_i][new_j] == '.':
                    CP = canPlace(board, player, opponent, (new_i, new_j), (i, j))
                    can_move, end_point = CP[0], CP[1]
                    if can_move:
                        point_moves.append((new_i, new_j))
                        end_points.append(end_point)
    return point_moves, end_points

def canPlace(board, player, opponent, empty_square, opponent_square):
    opponent_i, opponent_j = opponent_square[0], opponent_square[1]
    empty_i, empty_j = empty_square[0], empty_square[1]
    step = (opponent_i - empty_i, opponent_j - empty_j)
    while (empty_i in range(DIMS)) and (empty_j in range(DIMS)):
        if board[empty_i][empty_j] == player:
            return (True, (empty_i, empty_j))
        empty_i, empty_j = empty_i + step[0], empty_j + step[1]
    return (False, [])

def makeMove(board, player, opponent, move):
    board = copy.deepcopy(board)
    index_move = (GRID['G2I']['row'][move[0]], GRID['G2I']['col'][move[1]])
    i, j = index_move[0], index_move[1]
    # Placing players piece
    board[i][j] = player
    # Taking pieces
    board = takePieces(board, player, opponent, index_move)
    return board

def listTakenPieces(board, player, opponent, move):
    i, j = move[0], move[1]
    taken = []
    for i_shift in SHIFTS:
        for j_shift in SHIFTS:
            shift = (i_shift, j_shift)
            new_i, new_j = i + i_shift, j + j_shift
            potentially_taken = []
            while (new_i in range(DIMS)) and (new_j in range(DIMS)):
                if board[new_i][new_j] == opponent:
                    potentially_taken.append((new_i, new_j))
                    # Carrying on in the shift direction until reach a player
                    # piece
                    new_i, new_j = new_i + shift[0], new_j + shift[1]
                elif board[new_i][new_j] == player:
                    taken.append(potentially_taken)
                    break
                elif board[new_i][new_j] == '.':
                    break
    taken_list = []
    for takes in taken:
        for el in takes:
            taken_list.append(el)
    return taken_list

def takePieces(board, player, opponent, move):
    taken_list = listTakenPieces(board, player, opponent, move)
    for piece in taken_list:
        i, j = piece[0], piece[1]
        board[i][j] = player
    return board

def getMoveInput(move_list):
    while True:
        print('Please input a move in the following form: A1, or P for pass')
        move = input().upper()
        if move == 'P':
            return move
        else:
            try:
                move_tuple = (move[1], move[0])
                if move_tuple in move_list:
                    return move_tuple
                else:
                    print('Not a valid move...')
            except:
                print('Not a valid move...')

def decideWinner(board):
    b = 0
    w = 0
    for i in range(DIMS):
        for j in range(DIMS):
            if board[i][j] == 'b':
                b += 1
            elif board[i][j] == 'w':
                w += 1
    if b > w:
        return 'Black', b, w
    elif w > b:
        return 'White', b, w
    elif w == b:
        return 'Tie', b, w

def printWinner(board, winner):
    os.system('cls||clear')
    dispBoard(board)
    winner, b, w = winner[0], winner[1], winner[2]
    if winner == 'Tie':
        print('There has been a tie, total points each =  {}'.format(b))
    else:
        print('{} has won the game.\n Black: {}, White: {}'.format(winner, b, w))
    cont = input('Continue?')

# Two Player Game Fuction
def playTwoPlayer():
    
    # Make Othello Board
    board = makeBoard()
    turn, opponent = 'b', 'w'
    passed = False
    while True:
        os.system('cls||clear')

        # generate move list
        moves = generateMoveList(board, turn, opponent)

        if len(moves) == 0:
            # pass
            move = 'P'
        else:
            print("{}'s turn:".format(COLOUR[turn]))

            # Print current board to screen
            dispBoard(board)

            # Get user input
            move = getMoveInput(moves)

        if (move == 'P'):
            if passed == True:
                break
            passed = True
            turn, opponent = opponent, turn
            continue
        else:
            passed = False
        
        board = makeMove(board, turn, opponent, move)
        turn, opponent = opponent, turn
    
    winner = decideWinner(board)
    printWinner(board, winner)

# Play v PC function
def playvPC():

    # Choose player
    while True:
        print('Please choose which side you wish to play on: B/W')
        choice = input().lower()
        if choice in ['b','w']:
            break
        else:
            print('Please choose valid choice.')
            continue
    
    player = choice
    
    # Make Othello Board
    board = makeBoard()
    turn, opponent = 'b', 'w'
    passed = False
    while True:
        os.system('cls||clear')

        # generate move list
        moves = generateMoveList(board, turn, opponent)

        if len(moves) == 0:
            # pass
            move = 'P'
        else:
            print("{}'s turn:".format(COLOUR[turn]))
            # Print current board to screen
            dispBoard(board)
            if player == turn:
                # Get user input
                move = getMoveInput(moves)
            else:
                move = computerPlayer(board, turn, player)

        if (move == 'P') or (move == 'pass'):
            if passed == True:
                break
            passed = True
            turn, opponent = opponent, turn
            continue
        else:
            passed = False
        
        board = makeMove(board, turn, opponent, move)
        if turn != player:
            input('Continue?')
        turn, opponent = opponent, turn
    
    winner = decideWinner(board)
    printWinner(board, winner)

def computerPlayer(board, computer, real, depth = DEFAULT_DEPTH):
    ''' computerPlayer

    This function attempts to compute an optimal move for the computer to 
    play, using a minimax search up to a given depth (default = 5).
    The function aims to achieve the following:
    - Maximise number of moves for computer
    - Minimise number of moves for player
    '''
    min_max_board = copy.deepcopy(board)

    score, move = minimax(min_max_board, computer, real, True, depth, -999, 999)
    #print(score)
    if move != ():
        return move
    else:
        return 'pass'
    
def numCorner(board, colour):
    n_corners = 0
    for corner in CORNERS:
        if board[corner[0]][corner[1]] == colour:
            n_corners += 1
    return n_corners

def minimax(board, player, opponent, maximising, depth, alpha, beta):
    super_move = ()
    if depth == 0:
        return scoreBoard(board, player, opponent), super_move
    
    if maximising:
        # players turn
        max_eval = -999999
        moves = generateMoveList(board, player, opponent)
        random.shuffle(moves)
        if len(moves) == 0:
            next_layer, M = minimax(board, player, opponent, False, depth - 1, alpha, beta)
        for move in moves:
            # Copy board
            old_board = copy.deepcopy(board)

            # Make chosen move
            board = makeMove(board, player, opponent, move)
            
            # Recursively call minimax
            next_layer, M = minimax(board, player, opponent, False, depth - 1, alpha, beta)

            # Calculate corner addition, subtraction
            #next_layer += numCorner(board, player) * depth
            #next_layer -= numCorner(board, opponent) * depth

            # Resetting board
            board = old_board
            
            # Updating score based on minimax
            if next_layer > max_eval:
                max_eval = next_layer
                super_move = move
            alpha = max(alpha, next_layer)
            if beta <= alpha:
                break
        return max_eval, super_move
    else:
        min_eval = 999999
        moves = generateMoveList(board, opponent, player)
        random.shuffle(moves)
        if len(moves) == 0:
            next_layer, M = minimax(board, player, opponent, True, depth - 1, alpha, beta)
        for move in moves:
            # Copy board
            old_board = copy.deepcopy(board)

            # Make chosen move
            board = makeMove(board, opponent, player, move)

            # Recursively call minimax
            next_layer, M = minimax(board, player, opponent, True, depth - 1, alpha, beta)

            # Calculate corner addition, subtraction
            #next_layer -= numCorner(board, player) * depth
            #next_layer += numCorner(board, opponent) * depth

            # Resetting board
            board = old_board

            # Updating score based on minimax
            if next_layer < min_eval:
                min_eval = next_layer
                super_move = move
            beta = min(beta, next_layer)
            if beta <= alpha:
                break
        return min_eval, super_move

def scoreBoard(board, player, opponent):
    player_score = len(generateMoveList(board, player, opponent))*3
    opponent_score = len(generateMoveList(board, opponent, player))*3

    if (player_score == 0) and (opponent_score == 0):
        # Have reached game end
        winner = decideWinner(board)
        winner = winner[0]
        if winner[0].lower() == player:
            return 300
        elif winner[0].lower == opponent:
            return -300
        else:
            return 0

    for i in range(DIMS):
        for j in range(DIMS):
            if board[i][j] == player:
                player_score += GRADING_STRATEGY[i][j]
            if board[i][j] == opponent:
                opponent_score += GRADING_STRATEGY[i][j]

    return player_score - opponent_score

# Main Game Function    
def othello():
    while True:
        os.system('cls||clear')
        print('Welcome to Othello.  Please select an option:')
        print('A - Play against the computer')
        print('B - Play against a friend')
        print('Q - Quit Game')
        choice = input().upper()
        if choice == 'A':
            playvPC()
        elif choice == 'B':
            playTwoPlayer()
        elif choice == 'Q':
            break
        else:
            os.system('cls||clear')
            print('Please choose choose A, B or Q.')


othello()
