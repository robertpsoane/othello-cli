''' Othello Game

Object Oriented implementation of Othello Game with minimax AI

'''

import copy
import random
import os

class OthelloBoard:
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

    def __init__(self, DIMS = 8):
        self.setupConstants(DIMS)
        self.DIMS = DIMS
        self.makeBoard()

    def setupConstants(self, DIMS):
        # Setting up 'global' variables. 
        self.CENTRE_LEFT, self.CENTRE_RIGHT = int(DIMS/2 - 1 ), int(DIMS/2)
        self.CORNERS = [
            (0, 0),
            (0, DIMS-1),
            (DIMS-1,0),
            (DIMS-1, DIMS-1)
        ]
        self.OFF_CORNERS = [(1, 0), (0, 1), (1, 1),
                        (0, DIMS-2), (1, DIMS-1), (DIMS-2, DIMS-2),
                        (DIMS-2, 0), (DIMS-1, 1), (DIMS-2, 1),
                        (DIMS-2, DIMS-1), (DIMS-1, DIMS-2), (DIMS-2, DIMS-2)]
        EDGES = []
        for i in [0, DIMS-1]:
            for j in range(DIMS):
                edge_space = (
                            self.GRID['I2G']['col'][str(i)],
                            self.GRID['I2G']['row'][str(j)]
                            )
                EDGES.append(edge_space)
        for j in [0, DIMS-1]:
            for i in range(DIMS):
                edge_space = (
                            self.GRID['I2G']['col'][str(i)],
                            self.GRID['I2G']['row'][str(j)]
                            )
                EDGES.append(edge_space)
        self.EDGES = list(set(EDGES))
        self.CORNER_BONUS = 30
        self.DEFAULT_DEPTH = 5
        self.GRADING_STRATEGY = self.makeGradingStrategy(DIMS)
    
    def makeGradingStrategy(self, DIMS):
        '''
        Function to make a grading matrix, inspired by code here
        https://github.com/yuxuan006/Othello/blob/ac33536bc35c7e50da93aab937e3dfee
        5c258a7f/yuchai.py#L19
        '''
        board = []
        for i in range(DIMS):
            row = []
            for j in range(DIMS):
                if (i, j) in self.CORNERS:
                    row.append(10)
                elif (i, j) in self.OFF_CORNERS:
                    row.append(-2)
                elif (i, j) in self.EDGES:
                    row.append(2)
                else:
                    row.append(1)
            board.append(row)
        return board

    # Standard Game Functions
    def makeBoard(self):
        board = []
        for i in range(self.DIMS):
            row = []
            for j in range(self.DIMS):
                row.append('.')
            board.append(row)
        board[self.CENTRE_LEFT][self.CENTRE_LEFT] = 'b'
        board[self.CENTRE_RIGHT][self.CENTRE_RIGHT] = 'b'
        board[self.CENTRE_LEFT][self.CENTRE_RIGHT] = 'w'
        board[self.CENTRE_RIGHT][self.CENTRE_LEFT] = 'w'
        self.board = board

    def dispBoard(self):
        print('  ', end = '')
        for i in range(self.DIMS):
            print(self.GRID['I2G']['col'][str(i)], end=' ')
        print()
        for i in range(self.DIMS):
            print(i+1, end= ' ')
            for j in range(self.DIMS):
                print(self.board[i][j], end=' ')
            print()
    
    def generateMoveList(self, board, player, opponent):
        move_list = []
        end_points = []
        for i in range(self.DIMS):
            for j in range(self.DIMS):
                if board[i][j] == opponent:
                    possible_moves = self.pointMove(board, player, opponent, i, j)
                    moves, end_points_ij = possible_moves[0], possible_moves[1]
                    for move in moves:
                        grid_move = (
                            self.GRID['I2G']['row'][str(move[0])],
                            self.GRID['I2G']['col'][str(move[1])]
                        )
                        move_list.append(grid_move)
                    for end_point in end_points_ij:
                        end_points.append(end_point)
        return move_list

    def pointMove(self, board, player, opponent, i, j):
        point_moves = []
        end_points = []
        for i_shift in self.SHIFTS:
            for j_shift in self.SHIFTS:
                new_i, new_j = i + i_shift, j + j_shift
                if (new_i in range(self.DIMS)) and (new_j in range(self.DIMS)):
                    if board[new_i][new_j] == '.':
                        CP = self.canPlace(board, player, opponent, (new_i, new_j), (i, j))
                        can_move, end_point = CP[0], CP[1]
                        if can_move:
                            point_moves.append((new_i, new_j))
                            end_points.append(end_point)
        return point_moves, end_points

    def canPlace(self, board, player, opponent, empty_square, opponent_square):
        opponent_i, opponent_j = opponent_square[0], opponent_square[1]
        empty_i, empty_j = empty_square[0], empty_square[1]
        step = (opponent_i - empty_i, opponent_j - empty_j)
        test_i, test_j = empty_i + step[0], empty_j + step[1]
        while (test_i in range(self.DIMS)) and (test_j in range(self.DIMS)):
            if board[test_i][test_j] == '.':
                break
            if board[test_i][test_j] == player:
                return (True, (test_i, test_j))
            test_i, test_j = test_i + step[0], test_j + step[1]
        return (False, [])
    
    def makeMove(self, board, player, opponent, move):
        board = copy.deepcopy(board)
        index_move = (self.GRID['G2I']['row'][move[0]], self.GRID['G2I']['col'][move[1]])
        i, j = index_move[0], index_move[1]
        # Placing players piece
        board[i][j] = player
        # Taking pieces
        board = self.takePieces(board, player, opponent, index_move)
        return board

    def listTakenPieces(self, board, player, opponent, move):
        i, j = move[0], move[1]
        taken = []
        for i_shift in self.SHIFTS:
            for j_shift in self.SHIFTS:
                shift = (i_shift, j_shift)
                new_i, new_j = i + i_shift, j + j_shift
                potentially_taken = []
                while (new_i in range(self.DIMS)) and (new_j in range(self.DIMS)):
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

    def takePieces(self, board, player, opponent, move):
        taken_list = self.listTakenPieces(board, player, opponent, move)
        if taken_list == []:
            print('broken')
        for piece in taken_list:
            i, j = piece[0], piece[1]
            board[i][j] = player
        return board

    def decideWinner(self, board):
        b = 0
        w = 0
        for i in range(self.DIMS):
            for j in range(self.DIMS):
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
    
    def printWinner(self, board, winner):
        os.system('cls||clear')
        self.dispBoard()
        winner, b, w = winner[0], winner[1], winner[2]
        if winner == 'Tie':
            print('There has been a tie, total points each =  {}'.format(b))
        else:
            print('{} has won the game.\n Black: {}, White: {}'.format(winner, b, w))
        cont = input('Continue?')

    def getPlayerInput(self):
        while True:
            os.system('cls||clear')
            print('Welcome to Othello.  Please select an option:')
            print('A - Play against computer')
            print('B - Play against a friend')
            print('C - Play computer against self')
            print('Q - Quit Game')
            choice = input().upper()
            if choice == 'A':
                return 'A'
            elif choice == 'B':
                return 'B'
            elif choice == 'C':
                return 'C'
            elif choice == 'Q':
                exit()
            else:
                os.system('cls||clear')
                print('Please choose choose A, B or Q.')

    def sideSelect(self):
        # Choose player
        while True:
            print('Please choose which side you wish to play on: B/W')
            choice = input().lower()
            if choice in ['b','w']:
                return choice
            else:
                print('Please choose valid choice.')
                continue

    def actionPlayerChoice(self, choice):
        if choice == 'A':
            # Playing against computer
            player_side = self.sideSelect()
            if player_side == 'b':
                self.b = HumanPlayer()
                self.w = AIPlayer('w', self)
            else:
                self.w = HumanPlayer()
                self.b = AIPlayer('b', self)
        elif choice == 'B':
            self.w = HumanPlayer()
            self.b = HumanPlayer()
        else:
            self.w = AIPlayer('w', self)
            self.b = AIPlayer('b', self)

    def playOthello(self):
        player_input_choice = self.getPlayerInput()
        self.actionPlayerChoice(player_input_choice)
        turn, opponent = 'b', 'w'
        passed = False

        while True:
            os.system('cls||clear')

            # Generate Moves List
            moves = self.generateMoveList(self.board, turn, opponent)

            if len(moves) == 0:
                # pass
                move = 'P'
            else:
                print("{}'s turn:".format(self.COLOUR[turn]))
                # Print current board to screen
                self.dispBoard()

                if turn == 'b':
                    move = self.b.getMoveInput(moves, self.board)
                else:
                    move = self.w.getMoveInput(moves, self.board)
            if (move == 'P') or (move == 'pass'):
                if passed == True:
                    break
                passed = True
                turn, opponent = opponent, turn
                continue
            else:
                passed = False

            self.board = self.makeMove(self.board, turn, opponent, move)

            if turn == 'b':
                self.b.readyToContinue()
            else:
                self.w.readyToContinue()

            turn, opponent = opponent, turn

        winner = self.decideWinner(self.board)
        self.printWinner(self.board, winner)

class HumanPlayer():
    
    def __init__(self):
        pass

    def readyToContinue(self):
        pass

    def getMoveInput(self, move_list, board):
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


class AIPlayer():
    
    def __init__(self, side, game):
        self.side = side
        if self.side == 'b':
            self.opponent = 'w'
        else:
            self.opponent = 'b'
        self.game = game
        self.depth = 5

    def readyToContinue(self):
        input('Continue?')

    def getMoveInput(self, move_list, board):
        ''' computerPlayer

        This function attempts to compute an optimal move for the computer to 
        play, using a minimax search up to a given depth (default = 5).
        The function aims to achieve the following:
        - Maximise number of moves for computer
        - Minimise number of moves for player
        '''
        min_max_board = copy.deepcopy(board)
        depth = self.depth
        score, move = self.minimax(min_max_board, self.side, self.opponent, True, 
                                depth, -999, 999)
        #print(score)
        if move != ():
            return move
        else:
            return 'pass'
    
    def minimax(self, board, player, opponent, maximising, depth, alpha, beta):
        super_move = ()
        if depth == 0:
            return self.scoreBoard(board, player, opponent), super_move
        
        if maximising:
            # players turn
            max_eval = -999999
            moves = self.game.generateMoveList(board, player, opponent)
            random.shuffle(moves)
            if len(moves) == 0:
                next_layer, M = self.minimax(board, player, opponent, False, depth - 1, alpha, beta)
            for move in moves:
                # Copy board
                old_board = copy.deepcopy(board)

                # Make chosen move
                board = self.game.makeMove(board, player, opponent, move)
                
                # Recursively call minimax
                next_layer, M = self.minimax(board, player, opponent, False, depth - 1, alpha, beta)

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
            moves = self.game.generateMoveList(board, opponent, player)
            random.shuffle(moves)
            if len(moves) == 0:
                next_layer, M = self.minimax(board, player, opponent, True, depth - 1, alpha, beta)
            for move in moves:
                # Copy board
                old_board = copy.deepcopy(board)

                # Make chosen move
                board = self.game.makeMove(board, opponent, player, move)

                # Recursively call minimax
                next_layer, M = self.minimax(board, player, opponent, True, depth - 1, alpha, beta)

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

    def scoreBoard(self, board, player, opponent):
        player_score = len(self.game.generateMoveList(board, player, opponent))*3
        opponent_score = len(self.game.generateMoveList(board, opponent, player))*3

        if (player_score == 0) and (opponent_score == 0):
            # Have reached game end
            winner = self.game.decideWinner(board)
            winner = winner[0]
            if winner[0].lower() == player:
                return 300
            elif winner[0].lower == opponent:
                return -300
            else:
                return 0

        for i in range(self.game.DIMS):
            for j in range(self.game.DIMS):
                if board[i][j] == player:
                    player_score += self.game.GRADING_STRATEGY[i][j]
                if board[i][j] == opponent:
                    opponent_score += self.game.GRADING_STRATEGY[i][j]

        return player_score - opponent_score
    
    def numCorner(self, board, colour):
        n_corners = 0
        for corner in self.game.CORNERS:
            if board[corner[0]][corner[1]] == colour:
                n_corners += 1
        return n_corners

OthelloBoard().playOthello()