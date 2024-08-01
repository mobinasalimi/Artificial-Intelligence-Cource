import math
import numpy as np
from Board import BoardUtility
import random


class Player:
    def __init__(self, player_piece):
        self.piece = player_piece

    def play(self, board):
        return 0


class RandomPlayer(Player):
    def play(self, board):
        return [random.choice(BoardUtility.get_valid_locations(board)), random.choice([1, 2, 3, 4]),
                random.choice(["skip", "clockwise", "anticlockwise"])]


class HumanPlayer(Player):
    def play(self, board):
        move = input("row, col, region, rotation\n")
        move = move.split()
        print(move)
        return [[int(move[0]), int(move[1])], int(move[2]), move[3]]


class MiniMaxPlayer(Player):
    def __init__(self, player_piece, depth=5):
        super().__init__(player_piece)
        self.depth = depth

    def maximum_search(self, piece, depth, board, alpha, beta):
        if depth == 0 or BoardUtility.is_terminal_state(board) :
            return self.utility_function(board)
        else:
            value = -math.inf
            player_location = BoardUtility.get_valid_locations(board)
            for p in player_location:
                for player_region in range(1, 5):
                    for player_rotation in ["clockwise", "anticlockwise", "skip"]:
                        new_board = board.copy()
                        BoardUtility.make_move(new_board, p[0], p[1], player_region,player_rotation, self.piece)
                        value = max(value, self.minimum_search(piece, depth - 1, new_board, alpha, beta))
                        alpha = max(value, alpha)
                        if beta <= alpha:
                            return value
            return value

    def minimum_search(self, piece, depth, board, alpha, beta):
        if depth == 0 or BoardUtility.is_terminal_state(board):
            return self.utility_function(board)
        else:
            value = math.inf
            player_location = BoardUtility.get_valid_locations(board)
            for p in player_location:
                for player_region in range(1, 5):
                    for player_rotation in ["clockwise", "anticlockwise", "skip"]:
                        new_board = board.copy()
                        BoardUtility.make_move(new_board, p[0], p[1], player_region, player_rotation, self.piece)
                        value = min(value, self.maximum_search(piece, depth - 1, new_board, alpha, beta))
                        beta = min(value, beta)
                        if beta <= alpha:
                            return value
            return value

    def play(self, board):
        row = -1
        col = -1
        region = -1
        rotation = -1
        # Todo: implement minimax algorithm
        result = [[row, col], region, rotation]
        board = np.array(board)
        alpha = -math.inf
        beta = math.inf
        value = -math.inf
        player_location = BoardUtility.get_valid_locations(board)
        for p in player_location:
            for player_region in range(1, 5):
                for player_rotation in ["clockwise", "anticlockwise", "skip"]:
                    new_board = board.copy()
                    BoardUtility.make_move(new_board, p[0], p[1], player_region, player_rotation, self.piece)
                    new_value = self.minimum_search(self.piece, self.depth - 1, new_board, alpha, beta)
                    if value < new_value:
                        result = [[p[0], p[1]], player_region, player_rotation]
        return result

    def utility_function(self, board):
        score1 = 0
        score2 = 0
        for column in range(0, 6):
            for row in range(0, 6):
                # check horizontally, vertically, diagonally for player1
                if board[row][column] == '1':
                    if column < 5 and board[row][column + 1] == '1':
                        score1 += 1
                    if row < 5 and board[row + 1][column] == '1':
                        score1 += 1
                    if row < 5 and column < 5 and board[row + 1][column + 1] == '1':
                        score1 += 1
                    if row > 0 and column < 5 and board[row - 1][column + 1] == '1':
                        score1 += 1
                # check horizontally, vertically, diagonally for player2
                elif board[row][column] == '2':
                    if column < 5 and board[row][column + 1] == '2':
                        score2 += 1
                    if row < 5 and board[row + 1][column] == '2':
                        score2 += 1
                    if row < 5 and column < 5 and board[row + 1][column + 1] == '2':
                        score2 += 1
                    if row > 0 and column < 5 and board[row - 1][column + 1] == '2':
                        score2 += 1
        return score1 - score2


class MiniMaxProbPlayer(Player):
    def __init__(self, player_piece, depth=5, prob_stochastic=0.1):
        super().__init__(player_piece)
        self.depth = depth
        self.prob_stochastic = prob_stochastic

    def maximum_search(self, piece, depth, board, alpha, beta):
        if depth == 0 or BoardUtility.is_terminal_state(board) :
            return self.utility_function(board)
        else:
            value = -math.inf
            player_location = BoardUtility.get_valid_locations(board)
            for p in player_location:
                for player_region in range(1, 5):
                    for player_rotation in ["clockwise", "anticlockwise", "skip"]:
                        new_board = board.copy()
                        BoardUtility.make_move(new_board, p[0], p[1], player_region, player_rotation, self.piece)
                        value = max(value, self.minimum_search(piece, depth - 1, new_board, alpha, beta))
                        alpha = max(value, alpha)
                        if beta <= alpha:
                            return value
            return value

    def minimum_search(self, piece, depth, board, alpha, beta):
        if depth == 0 or BoardUtility.is_terminal_state(board):
            return self.utility_function(board)
        else:
            value = math.inf
            player_location = BoardUtility.get_valid_locations(board)
            for p in player_location:
                for player_region in range(1, 5):
                    for player_rotation in ["clockwise", "anticlockwise", "skip"]:
                        new_board = board.copy()
                        BoardUtility.make_move(new_board, p[0], p[1], player_region, player_rotation, self.piece)
                        value = min(value, self.maximum_search(piece, depth - 1, new_board, alpha, beta))
                        beta = min(value, beta)
                        if beta <= alpha:
                            return value
            return value

    def utility_function(self, board):
        score1 = 0
        score2 = 0
        for column in range(0, 6):
            for row in range(0, 6):
                # check horizontally, vertically, diagonally for player1
                if board[row][column] == '1':
                    if column < 5 and board[row][column + 1] == '1':
                        score1 += 1
                    if row < 5 and board[row + 1][column] == '1':
                        score1 += 1
                    if row < 5 and column < 5 and board[row + 1][column + 1] == '1':
                        score1 += 1
                    if row > 0 and column < 5 and board[row - 1][column + 1] == '1':
                        score1 += 1
                # check horizontally, vertically, diagonally for player2
                elif board[row][column] == '2':
                    if column < 5 and board[row][column + 1] == '2':
                        score2 += 1
                    if row < 5 and board[row + 1][column] == '2':
                        score2 += 1
                    if row < 5 and column < 5 and board[row + 1][column + 1] == '2':
                        score2 += 1
                    if row > 0 and column < 5 and board[row - 1][column + 1] == '2':
                        score2 += 1
        return score1 - score2

    def play(self, board):
        row = -1
        col = -1
        region = -1
        rotation = -1
        # Todo: implement minimaxProb algorithm
        result = [[row, col], region, rotation]
        alpha = -math.inf
        beta = math.inf
        board = np.array(board)
        locations = BoardUtility.get_valid_locations(board)
        max_value = -math.inf
        for p in locations:
            for player_region in range(1, 5):
                for player_rotation in ["clockwise", "anticlockwise", "skip"]:
                    new_board = board.copy()
                    BoardUtility.make_move(new_board, p[0], p[1], player_region, player_rotation, self.piece)
                    value = self.minimum_search(self.piece, self.depth - 1, new_board, alpha, beta)
                    if value > max_value:
                        result = [[p[0], p[1]], player_region, player_rotation]
        prob = random.random()
        if prob <= self.prob_stochastic:
            return result
        if prob > self.prob_stochastic:
            rots = ["clockwise", "anticlockwise", "skip"]
            return [random.choice(BoardUtility.get_valid_locations(board)), random.randint(1, 4), random.choice(rots)]



