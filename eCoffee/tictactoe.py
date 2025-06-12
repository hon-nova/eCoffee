"""
Tic Tac Toe Player
"""

import math

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
   # Count X's and O's on the board
   x_count = sum(row.count("X") for row in board)
   o_count = sum(row.count("O") for row in board)

    # If X and O counts are equal, it's X's turn (X always starts)
   if x_count == o_count:
      return "X"
   else:
      return "O"
   # raise NotImplementedError


def actions(board):
   """
   Returns set of all possible actions (i, j) available on the board.
   """
  
   action_set= set()
   for y, row in enumerate(board):
      for x, cell in enumerate(row):
         if cell == EMPTY:
            action_set.add((y,x))
   return action_set   


def result(board, action):
   """
   Returns the board that results from making move (i, j) on the board.
   """
   execute_board = [row.copy() for row in board]   
   
   current_player = player(board)   
   
   i,j = action
   execute_board[i][j] = current_player
   
   return execute_board   


def winner(board):
   """
   Returns the winner of the game, if there is one.
   """
   
   #check 3 rows
   for row in board:
      if row[0] == row [1] == row[2] and row[0]!=EMPTY:
         return row[0]      
  
   #check 3 cols
   for col in range(3):
      if board[0][col] == board[1][col] == board[2][col] and board[0][col] !=EMPTY:
         return board[0][col]
      
   #check 2 diagonals
   if board[0][0] == board[1][1] == board[2][2] and board[0][0]!=EMPTY:
      return board[0][0]  
   
   if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
      return board[0][2]   
  
   return None

def terminal(board):
   """
   Returns True if game is over, False otherwise.
   """
   x_count = sum(row.count("X") for row in board)
   o_count = sum(row.count("O") for row in board)
   if winner(board) is not None:
      return True
   
   if all(cell!= EMPTY for row in board for cell in row):
      return True
   
   return False

def utility(board):
   """
   Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
   """
   if winner(board) == "X":
      return 1
   elif winner(board) == "O":
      return -1
   else:
      return 0 

def min_value(board):
   if terminal(board):
      return utility(board)
    
   v = float("inf")
   for action in actions(board):
      v = min(v, max_value(result(board, action)))
   return v

def max_value(board):
   if terminal(board):
      return utility(board)
    
   v = float("-inf")
   for action in actions(board):
      v = max(v, min_value(result(board, action)))
   return v

def minimax(board):
   if terminal(board):
      return None

   turn = player(board)
   best_move = None

   if turn == "X":
      best_score = float("-inf")
      for action in actions(board):
         score = min_value(result(board, action))
         if score > best_score:
            best_score = score
            best_move = action

   else:  # turn == "O"
      best_score = float("inf")
      for action in actions(board):
         score = max_value(result(board, action))
         if score < best_score:
            best_score = score
            best_move = action

   return best_move


# def minimax(board):
#    """
#    Returns the optimal action for the current player on the board.
#    """
#    if terminal(board):
#       return None
#    current_player = player(board)  
   
   
#    # try all possible actions by calling
#    # result(board, action) action here is from actions(board)
#    for action in actions(board):
#       new_board = result(board,action)
      
#       if current_player == "X":
#          max_value(board)
#       elif current_player == "O":
#          min_value(board)
      
   
