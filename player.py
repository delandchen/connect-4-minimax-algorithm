import math
import random


class Player():
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_col = False
        val = None
        while not valid_col:
            square = input(self.letter + '\'s turn. Input move (1-7): ')  # Asks for move
            try:
                val = int(square) - 1
                if val not in game.valid_moves():  # If move is not valid, try again
                    raise ValueError
                valid_col = True
            except ValueError:
                print('Invalid column. Try again.')
        return val


class ComputerPlayer(Player):
    def __init__(self, letter, difficulty):
        super().__init__(letter)
        self.difficulty = difficulty  # The player sets the depth of the mini-max algorithm in the main() function

    def get_move(self, game):
        if game.empty_squares() == 42 or game.empty_squares() == 41:  # The first move of the AI is always random
            square = random.choice(game.valid_moves())                      # to diversify the game
        else:
            square = self.minimax(game, self.letter, self.difficulty)['position']
            if square is None:
                square = random.choice(game.valid_moves())
        return square

    def minimax(self, state, player, depth):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if depth == 0 or state.is_terminal_node():
            if state.is_terminal_node():
                if state.current_winner == max_player:
                    return {'position': None, 'score': math.inf}
                elif state.current_winner == other_player:
                    return {'position': None, 'score': -math.inf}
                else:
                    return {'position': None, 'score': 0}

            else:
                return {'position': None, 'score': state.score_position(max_player) if player == max_player
                        else -1*(state.score_position(other_player))}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in state.valid_moves():
            sim_move = state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player, depth-1)

            state.board[sim_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best
