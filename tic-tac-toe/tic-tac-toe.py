#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
"""tic-tac-toe-oop.py at https://github.com/wilsonmar/python-samples/blob/main/tic-tac-toe-oop.py
   Not yet explained at https://wilsonmar.github.io/python-samples 
   This is a classic two-player game played to settle an arugment to simply achieve world peace.
   Thus, this program does not provide the intelligence to play a human.
   
   This program can be manually run by "chmod +x tic-tac-toe-oop.py" then "./tic-tac-toe-oop.py".
   See https://www.youtube.com/watch?v=Q6CCdCBVypg
   
   Alternately, this file is within a folder so that, during unit testing, this program can be 
   run automatically after a one-time CLI "pip install pytest" to load the popular third-party 
   testing framework with a more concise syntax and powerful features compared to unittest.
   
   Unit-testing command "pytest" auto-discovers and executes all test files named with prefix "test_".
   They determine whether outputs are correct given a sset of inputs.
      See https://www.geeksforgeeks.org/object-oriented-testing-in-python/
      https://www.youtube.com/watch?v=YbpKMIUjvK8 =  How To Write Unit Tests in Python • Pytest Tutorial
      See https://www.youtube.com/watch?v=cHYq1MRoyI0& = Freecodecamp: How to Test Python Code by @iamrithmic
   
   NOTE: In the code, 3 characters are used to indent.
   
   This program starts by executing the "create_board" function to define a 3x3 grid of underlines.
   The "show_board" function displays the grid.
   Alternately, dividing lines can be added like at https://www.youtube.com/watch?v=7Djh-Cbgi0E
   
   This program presents a text-based UI (not a Tkinter GUI) as in 
   https://realpython.com/tic-tac-toe-python/ or https://www.youtube.com/watch?v=gNCpUS4d1Oo
   https://github.com/softwareNuggets/Python_TKInter_Tic_Tac_Toe/blob/main/tic_tac_toe_pro.py
   which can be turned into a mobile app.
   https://stackoverflow.com/questions/4083796/how-do-i-run-unittest-on-a-tkinter-app

   Logic in this code uses object-oriented programming concepts important to learn and use.
   The class "TicTacToe" encapsulates attributes, methods, and behaviors of game play.
   
   The "random" module is imported to enable "random.randint(0, 1)" within 
   function "get_random_first_player".

   Within an infinite loop, the game_over flag is set after evaluating the result of each move.
   A win goes to the first player to mark three Os or Xs diagonally, horizontally, or vertically,
   as determined by function "has_player_won".
   
   Each player must also block their opponent while attempting to make their chain.
   Thus, this code has a nested loops to check for winning columns, rows, and diagonals.

   Two players in the game alternate turns to mark the board with O or X.
   
   To the prompt "Enter row & column numbers to fix spot: _"
   each player enters two numbers separated by a space, such a "1 3" for row 1 column 3.

   Alternately, a number 1-9 can be used as in https://replit.com/login?source=new-repl&goto=%2Fnew%2Fpython3

   Game play can be interrupted any time by manually pressing Control+C on macOS for a KeyboardInterrupt.

   QUESTION: What does function "fix_spot" do?
   
   TODO: Check whether a spot is already taken and request another choice.

   TODO: Recognize if a winning hand is present and alert players, as in
   https://stackoverflow.com/questions/13734121/python-oop-tic-tac-toe

   game_over is identified when the "is_board_filled()" condition is met.

   The program stops when there is a tie or a winner.

   TODO: At end of game, create another game and keep score.

   Creative Commons Copyright (c) 2024 Wilson Mar based on https://hackr.io/blog/python-projects

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
   OF ANY KIND, either express or implied. See the License for the specific
   language governing permissions and limitations under the License.

   TODO: This game can be expanded by adding a larger grid.
"""

import random

class TicTacToe:

   def __init__(self):
       self.board = []

   def create_board(self):
       for i in range(3):
           row = []
           for j in range(3):
               row.append('-')
           self.board.append(row)

   def get_random_first_player(self):
       return random.randint(0, 1)

   def fix_spot(self, row, col, player):
       self.board[row][col] = player

   def has_player_won(self, player):
       n = len(self.board)
       board_values = set()

       # check rows
       for i in range(n):
           for j in range(n):
               board_values.add(self.board[i][j])

           if board_values == {player}:
               return True
           else:
               board_values.clear()

       # check cols
       for i in range(n):
           for j in range(n):
               board_values.add(self.board[j][i])

           if board_values == {player}:
               return True
           else:
               board_values.clear()

       # check diagonals
       for i in range(n):
           board_values.add(self.board[i][i])
       if board_values == {player}:
           return True
       else:
           board_values.clear()
      
       board_values.add(self.board[0][2])
       board_values.add(self.board[1][1])
       board_values.add(self.board[2][0])
       if board_values == {player}:
           return True
       else:
           return False

   def is_board_filled(self):
       for row in self.board:
           for item in row:
               if item == '-':
                   return False
       return True

   def swap_player_turn(self, player):
       return 'X' if player == 'O' else 'O'

   def show_board(self):
       for row in self.board:
           for item in row:
               print(item, end=' ')
           print()

   def start(self):
       self.create_board()
       player = 'X' if self.get_random_first_player() == 1 else 'O'
       game_over = False

       while not game_over:
           try:
               self.show_board()
               print(f'\nPlayer {player} turn')

               row, col = list(
                   map(int, input(
                       'Enter row & column numbers to fix spot: ').split()))
                   # TODO: Add lables to rows (1 2 3) and columns (A B C)
               print()

               if col is None:
                   raise ValueError(
                       'not enough values to unpack (expected 2, got 1)')

               self.fix_spot(row - 1, col - 1, player)

               game_over = self.has_player_won(player)
               if game_over:
                   print(f'Player {player} wins the game!')
                   continue

               game_over = self.is_board_filled()
               if game_over:
                   print('Match Draw!')
                   continue

               player = self.swap_player_turn(player)

           except ValueError as err:
               print(err)

       print()
       self.show_board()

if __name__ == '__main__':
  tic_tac_toe = TicTacToe()
  tic_tac_toe.start()