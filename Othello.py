
import copy
import os

# global vars
global grid
global shifts
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

def makeBoard():
    board = []
    for i in range(8):
        row = []
        for j in range(8):
            row.append('.')
        board.append(row)
    board[3][3] = 'b'
    board[4][4] = 'b'
    board[3][4] = 'w'
    board[4][3] = 'w'
    return board

def dispBoard(board):
    print('  A B C D E F G H')
    for i in range(8):
        print(i+1, end= ' ')
        for j in range(8):
            print(board[i][j], end=' ')
        print()

def generateMoveList(board, player, opponent):
    move_list = []
    end_points = []
    for i in range(8):
        for j in range(8):
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
    while (empty_i in range(8)) and (empty_j in range(8)):
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
            while (new_i in range(8)) and (new_i in range(8)):
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

def gameIntro():
    while True:
        os.system('cls||clear')
        print('Welcome to Othello.  Please select an option:')
        print('A - Play against the computer')
        print('B - Play against a friend')
        print('Q - Quit Game')
        choice = input()
        if (choice == 'A') or (choice == 'a'):
            os.system('cls||clear')
            print('AI not currently implemented.  Please try again later.')
        elif (choice == 'B') or (choice == 'b'):
            playTwoPlayer()
            break
        elif (choice == 'Q') or (choice == 'q'):
            break
        else:
            os.system('cls||clear')
            print('Please choose choose A, B or Q.')

def getMoveInput(move_list):
    while True:
        print('Please input a move in the following form: A1, or P for pass')
        move = input()
        if move == 'P':
            return move
        else:
            try:
                move_tuple = (move[1], move[0])
                if move_tuple in move_list:
                    return move_tuple
                else:
                    print('Not a valid move...')
            except expression as identifier:
                print('Not a valid move...')

def decideWinner(board):
    b = 0
    w = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 'b':
                b += 1
            elif board[i][j] == 'w':
                w += 1
    if b > w:
        return 'Black'
    elif w > b:
        return 'White'
    elif w == b:
        return 'Tie'

def playTwoPlayer():
    
    # Make Othello Board
    board = makeBoard()
    turn, opponent = 'b', 'w'
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

        if move == 'P':
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

    if winner == 'Tie':
        print('There has been a tie')
    else:
        print('{} has won the game'.format(winner))
    cont = input('Continue?')

    gameIntro()

def main():
    gameIntro()

main()