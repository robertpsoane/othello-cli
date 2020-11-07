
import copy
import os

# global vars
global grid
global shifts
global colour
global dims
global corners
global edges

grid = {
    'G2I' : {
        'row': {
            '1':0,
            '2':1,
            '3':2,
            '4':3,
            '5':4,
            '6':5,
            '7':6,
            '8':7
        },
        'col':{
            'A':0,
            'B':1,
            'C':2,
            'D':3,
            'E':4,
            'F':5,
            'G':6,
            'H':7
        },
    },
    'I2G':{
        'row':{
            '0':'1',
            '1':'2',
            '2':'3',
            '3':'4',
            '4':'5',
            '5':'6',
            '6':'7',
            '7':'8'
        },
        'col':{
            '0':'A',
            '1':'B',
            '2':'C',
            '3':'D',
            '4':'E',
            '5':'F',
            '6':'G',
            '7':'H',
        }
    }
}

colour = {
    'b': 'Black',
    'w': 'White'
}

shifts = [-1, 0, 1]

dims = 6

centre_left = int(dims/2 - 1 )
centre_right = int(dims/2)

end_letter = grid['I2G']['row'][str(dims - 1)]

corners = [
    ('1', 'A'),
    ('1', end_letter),
    (str(dims),'A'),
    (str(dims), end_letter)
]

edges = []
for i in [0, dims-1]:
    for j in range(dims):
        edge_space = (
                    grid['I2G']['col'][str(i)],
                    grid['I2G']['row'][str(j)]
                    )
        edges.append(edge_space)
for j in [0, dims-1]:
    for i in range(dims):
        edge_space = (
                    grid['I2G']['col'][str(i)],
                    grid['I2G']['row'][str(j)]
                    )
        edges.append(edge_space)
edges = list(set(edges))
        

# Standard Game Functions
def makeBoard():
    board = []
    for i in range(dims):
        row = []
        for j in range(dims):
            row.append('.')
        board.append(row)
    board[centre_left][centre_left] = 'b'
    board[centre_right][centre_right] = 'b'
    board[centre_left][centre_right] = 'w'
    board[centre_right][centre_left] = 'w'
    return board

def dispBoard(board):
    print('  ', end = '')
    for i in range(dims):
        print(grid['I2G']['col'][str(i)], end=' ')
    print()
    for i in range(dims):
        print(i+1, end= ' ')
        for j in range(dims):
            print(board[i][j], end=' ')
        print()

def generateMoveList(board, player, opponent):
    move_list = []
    end_points = []
    for i in range(dims):
        for j in range(dims):
            if board[i][j] == opponent:
                possible_moves = pointMove(board, player, opponent, i, j)
                moves, end_points_ij = possible_moves[0], possible_moves[1]
                for move in moves:
                    grid_move = (
                        grid['I2G']['row'][str(move[0])],
                        grid['I2G']['col'][str(move[1])]
                    )
                    move_list.append(grid_move)
                for end_point in end_points_ij:
                    end_points.append(end_point)
    return move_list

def pointMove(board, player, opponent, i, j):
    point_moves = []
    end_points = []
    for i_shift in shifts:
        for j_shift in shifts:
            new_i, new_j = i + i_shift, j + j_shift
            if (new_i in range(dims)) and (new_j in range(dims)):
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
    while (empty_i in range(dims)) and (empty_j in range(dims)):
        if board[empty_i][empty_j] == player:
            return (True, (empty_i, empty_j))
        empty_i, empty_j = empty_i + step[0], empty_j + step[1]
    return (False, [])

def makeMove(board, player, opponent, move):
    board = copy.deepcopy(board)
    index_move = (grid['G2I']['row'][move[0]], grid['G2I']['col'][move[1]])
    i, j = index_move[0], index_move[1]
    # Placing players piece
    board[i][j] = player
    # Taking pieces
    board = takePieces(board, player, opponent, index_move)
    return board

def listTakenPieces(board, player, opponent, move):
    i, j = move[0], move[1]
    taken = []
    for i_shift in shifts:
        for j_shift in shifts:
            shift = (i_shift, j_shift)
            new_i, new_j = i + i_shift, j + j_shift
            potentially_taken = []
            while (new_i in range(dims)) and (new_j in range(dims)):
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
    for i in range(dims):
        for j in range(dims):
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

def printWinner(winner):
    os.system('cls||clear')
    dispBoard(board)
    winner, b, w = winner[0], winner[1], winner[2]
    if winner == 'Tie':
        print('There has been a tie, total points each =  {}'.format(b))
    else:
        print('{} has won the game. Black: {}, White: {}'.format(winner, b, w))
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
            print("{}'s turn:".format(colour[turn]))

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
    printWinner(winner)


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
            print("{}'s turn:".format(colour[turn]))
            # Print current board to screen
            dispBoard(board)
            if player == turn:
                # Get user input
                move = getMoveInput(moves)
            else:
                move = computerPlayer(board, turn, player)

        if (move == 'P'):
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
    printWinner(winner)

def computerPlayer(board, computer, real, depth = 5):
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
    return move
    
    

def minimax(board, player, opponent, maximising, depth, alpha, beta):
    if depth == 0:
        return scoreBoard(board, player, opponent), ()
    
    if maximising:
        # players turn
        max_eval = -999
        moves = generateMoveList(board, player, opponent)
        for move in moves:
            old_board = copy.deepcopy(board)
            makeMove(board, player, opponent, move)
            next_layer, M = minimax(board, player, opponent, False, depth - 1, alpha, beta)
            board = old_board
            if next_layer > max_eval:
                max_eval = next_layer
                super_move = move
            alpha = max(alpha, next_layer)
            if beta < alpha:
                break
        return max_eval, super_move
    else:
        min_eval = 999
        moves = generateMoveList(board, player, opponent)
        for move in moves:
            old_board = copy.deepcopy(board)
            makeMove(board, opponent, player, move)
            next_layer, M = minimax(board, player, opponent, True, depth - 1, alpha, beta)
            board = old_board
            if next_layer < min_eval:
                min_eval = next_layer
                super_move = move
            beta = min(beta, next_layer)
            if beta < alpha:
                break
        return min_eval, super_move



def scoreBoard(board, player, opponent):
    player_score = len(generateMoveList(board, player, opponent))
    opponent_score = len(generateMoveList(board, opponent, player))
    return player_score -  opponent_score


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