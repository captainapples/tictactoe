"""
Tic Tac Toe Player
"""

import math, copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count # of Xs and Os on board

    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    # If x_count <= o_count, then it's X's turn
    if x_count <= o_count:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Initialize empty set for all possible actions
    possible_actions = set()

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            # If cell is empty, add tuple to possible_actions
            if cell == EMPTY:
                possible_actions.add((i,j))
    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Need to make a deepcopy of board bc minimax function needs to evaluate many different board states
    board_copy = copy.deepcopy(board)
    i, j = action

    # If action results in marking a spot in an already occupied cell, then raise exception
    if board[i][j] != None:
        raise Exception
    
    # Call function player on incoming board to see whose turn it is,then mark X or O in the cell of the deepcopy board_copy
    # because we don't want to change original board
    else:
        board_copy[i][j] = player(board)

    return board_copy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]
    
    # Check columns
    for column in range(3):
        if board[0][column] == board[1][column] == board[2][column] and board[0][column] is not None:
            return board[0][column]
    
    # Check diagonols
    if board[0][0] == board[1][1] == board[2][2] and board [0][0] is not None:
        return board[0][0]
    if board [2][0] == board[1][1] == board[0][2] and board[2][0] is not None:
        return board[2][0]
    
    # return none if no winner yet
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If there is a winner or there are no empty cells, then game is over
    if winner(board) is not None or any(None in row for row in board) == False:
        return True
    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # this function is only called if terminal(board) is True
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    # game is over and tied
    return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        print(f"Terminal board: {board}")
        return utility(board)

    if player(board) == X: # If current player is max player
        # Use a generator expression that doesn't store entire list in memory. Send a new board state, with -math.inf (worst score for
        # max player), math.inf (worst score for min player), and action that we send to ab_pruning function. Call
        # ab_pruning function for every action in actions generates a tuple: (best_value for max player, action that leads to
        # that board state). Return best action [1] for player X after evaluating every possible action on the board
        return max((ab_pruning(result(board, action), -math.inf, math.inf, False), action) for action in actions(board))[1]
    else: # If current player is min player
        # Same logic as above but for min player
        return min((ab_pruning(result(board, action), -math.inf, math.inf, True), action) for action in actions(board))[1]
        
def ab_pruning(board, alpha, beta, max_player):
    """
    Implementation of Alpha Beta Pruning & evaluation of board states via DFS. alpha = best value player X has found so far. beta = best value
    player O has found so far. alpha and beta are labeled for every parent node in the tree while best_value is just the best value for the current
    player at the current node in tree & this is what is returned. alpha and beta values are evaluated to see if branches can be pruned
    """
    if terminal(board):
        return utility(board)
    if max_player:
        # initialize best_value to neg infinity so any value will be better
        best_value = -math.inf

        # Find best values for every possible move down the tree 
        for action in actions(board):
            # eval_action is the optimal move that min player will make after this move from max player
            eval_action = ab_pruning(result(board, action), alpha, beta, False) # last argument is False to get min player's best_value
            # Compare best_value for player X and best value for player O (eval_action) & update best_value for player X as that value
            best_value = max(best_value, eval_action)
            # Update alpha = best option for player X so far
            alpha = max(alpha, best_value)
            # If the best option found (alpha) >= beta (best option for min player), stop evaluating bc min player will never choose this branch
            if beta <= alpha:
                break
        return best_value

    # If current player is min player
    else:
        best_value = math.inf

        for action in actions(board):
            # Evaluate the board from taking that action
            eval_action = ab_pruning(result(board, action), alpha, beta, True) # last argument is True so we can then evaluate for player X
            # If eval_action returns a smaller value than current best_value, updeate it to new best_value
            best_value = min(best_value, eval_action)
            # Update beta = best option for Player O so far
            beta = min(beta, best_value)
            # If the best ooption found (beta) <= alpha (best option for max player), stop evaluating bc max player will never choose this branch
            if beta <= alpha:
                break
        return best_value


    
