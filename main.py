import time
from player import HumanPlayer, ComputerPlayer


class ConnectFour():
    # KEEP IN MIND: instead of using matrices (ex: board[row][column]) to represent
    # and manipulate board squares, this game uses index math instead (ex: board[index*i])
    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None

    @staticmethod
    # Creates an array to represent the 6x7 row/column board
    def make_board():
        return [' ' for _ in range(42)]

    # Prints the board to the console
    def print_board(self):
        for row in [self.board[i*7:((i+1) * 7)] for i in range(6)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    # Prints the column numbers to make moves placement easier
    def print_board_nums():
        # 0 | 1 | 2
        number_board = [str(j+1) for j in range(7)]
        print('| ' + ' | '.join(number_board) + ' |')

    def make_move(self, column, letter):
        # Places the letter on the lowest square/index in the chosen column
        squares_in_column = [i for i in range(column+35, column-2, -7)]

        # Checks each square in the column starting from the bottom
        # and places the piece on the first empty square
        for index in squares_in_column:
            if self.board[index] == ' ':
                self.board[index] = letter
                # If the move is a winning move, then current_winner is set
                if self.winner(index, letter):
                    self.current_winner = letter
                return index
        return False

    def winner(self, square, letter):
        # Checks for 4 in a row
        # Check every row
        row_ind = square // 7
        if self.check_row(row_ind, letter):
            return True

        # Check every column
        col_ind = square % 7
        if self.check_column(col_ind, letter):
            return True

        # Check all diagonals
        if self.check_diagonals(letter):
            return True

        return False

    def check_row(self, index, letter):
        # Uses a stack to 'stack' consecutive pieces, if there is 4 in a row, returns True
        stack = []

        for let in self.board[index*7:(index*7)+7]:
            if len(stack) == 0 and let == letter:
                stack.append(letter)
            elif let in stack:
                stack.append(letter)
            else:
                # Empties the stack if there is an ' ' or different piece in the square
                stack = []

            if len(stack) == 4:
                return True
        return False

    def check_column(self, index, letter):
        # Uses a stack to 'stack' consecutive pieces, if there is 4 in a row, returns True
        stack = []

        for let in self.board[index:index+36:7]:
            if len(stack) == 0 and let == letter:
                stack.append(letter)
            elif let in stack:
                stack.append(letter)
            else:
                # Empties the stack if there is an ' ' or different piece in the square
                stack = []

            if len(stack) == 4:
                return True
        return False

    def check_diagonals(self, letter):

        # Check all negatively sloped diagonals using starting indexes (top left to bottom right)
        for i in [0, 1, 2, 3, 7, 8, 9, 10, 14, 15, 16, 17]:
            if (self.board[i] == letter and self.board[i+8] == letter
                    and self.board[i+16] == letter and self.board[i+24] == letter):
                return True

        # Check all positively sloped diagonals using starting indexes (top right to bottom left)
        for j in [3, 4, 5, 6, 10, 11, 12, 13, 17, 18, 19, 20]:
            if (self.board[j] == letter and self.board[j+6] == letter
                    and self.board[j+12] == letter and self.board[j+18] == letter):
                return True

        return False

    def score_position(self, letter):
        # Returns the score position/value of the given board/state to determine next best move
        # Increases score based on the # of consecutive pieces
        score = 0

        # Center column evaluation, we want to prioritize the center
        center_column = self.board[3:36:7]
        center_section = self.evaluate_window(center_column, letter)
        score += center_section * 4

        # Horizontal evaluation/all columns
        for row_index in range(7):
            row_array = [x for x in self.board[row_index*7:(row_index*7)+7]]
            # Checking sections of 4
            for col_ind in range(4):
                section = row_array[col_ind:col_ind+4]
                score += self.evaluate_window(section, letter)

        # Vertical evaluation/all rows
        for col_index in range(8):
            col_array = [y for y in self.board[col_index:col_index+36:7]]
            # check sections of 4
            for row_ind in range(3):
                section = col_array[row_ind:row_ind+4]
                score += self.evaluate_window(section, letter)

        # Evaluate all positively sloped diagonals
        for j in [3, 4, 5, 6, 10, 11, 12, 13, 17, 18, 19, 20]:
            # check sections of 4
            section = [self.board[j], self.board[j+6], self.board[j+12], self.board[j+18]]
            score += self.evaluate_window(section, letter)

        # Evaluate all negatively sloped diagonals
        for i in [0, 1, 2, 3, 7, 8, 9, 10, 14, 15, 16, 17]:
            # check sections of 4
            section = [self.board[i], self.board[i+8], self.board[i+16] + self.board[i+24]]
            score += self.evaluate_window(section, letter)

        return score

    @staticmethod
    def evaluate_window(section, letter):
        # Returns the value of the section
        # IMPORTANT: Adjust the score value to tune the algorithm's decision-making
        score = 0
        other_letter = 'X' if letter == 'O' else 'O'

        if section.count(letter) == 4:
            score += 100
        elif section.count(letter) == 3 and section.count(' ') == 1:
            score += 5
        elif section.count(letter) == 2 and section.count(' ') == 2:
            score += 2

        # EXAMPLE: a higher score for this line would make the algorithm play more defensively
        if section.count(other_letter) == 3 and section.count(' ') == 1:
            score -= 4

        return score

    def empty_squares(self):
        # Returns the # of empty squares in the self.board
        return len([1 for j in self.board if j == ' '])

    def valid_moves(self):
        # Returns an array of columns indexes that are available moves/choices
        return [k for k in range(7) if self.board[k] == ' ']

    def is_terminal_node(self):
        # Returns true if there is a winner or if there are no more available moves left
        return self.current_winner is not None or self.empty_squares() == 0


def play(game, x_player, o_player, print_game=True):

    if print_game:
        game.print_board_nums()

    letter = 'X'
    while True:
        # Asks players for their move
        if letter == 'O':
            column = o_player.get_move(game)
        else:
            column = x_player.get_move(game)

        if game.make_move(column, letter) is not False:
            # Prints visuals to console
            if print_game:
                print(letter + ' makes a move to column {}'.format(column+1))
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter  # Ends the loop and exits the game
            letter = 'O' if letter == 'X' else 'X'  # Switches player

        time.sleep(.8)


if __name__ == '__main__':
    print('Welcome to Connect-4!')
    difficulty = int(input('How hard would you like the algorithm to think? (Difficulty: 1-6): '))
    first = int(input('Would you like to go first (1) or second (2)?: '))
    x_player = HumanPlayer('X') if first == 1 else ComputerPlayer('X', difficulty)
    o_player = ComputerPlayer('O', difficulty) if first == 1 else HumanPlayer('O')
    t = ConnectFour()

    t.print_board()

    play(t, x_player, o_player, print_game=True)
