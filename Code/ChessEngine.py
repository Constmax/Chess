"""
stores all the information
"""


class GameState:
    def __init__(self):
        # chess board
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.move_functions = {'p': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                               'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}

        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)

        '''
        takes move as parameter and executes it wont work for special scenarios
        '''
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # log the move to undo it later
        self.white_to_move = not self.white_to_move  # swaps plyers
        # update kings position if needed
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        if move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)

    '''
    undo the last move
    '''
    def undo_move(self):
        if len(self.move_log) != 0:
            self.white_to_move = not self.white_to_move
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)
            if move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)

    '''
    considers check
    1) generates all possible moves
    2) for each move makes the move
    3) generates all opponents moves
    4)for each of your opponents moves generates all your moves
    '''
    def get_valid_moves(self):
        moves = self.get_all_moves()   # 1)

        for i in range(len(moves) - 1, -1, -1):  # when removing from a list go backwards
            self.make_move(moves[i])  # for each move makes the move
            self.white_to_move = not self.white_to_move

            if self.in_check():
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move
            self.undo_move()
        return moves

    '''
    #determines if current player is in check
    '''
    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    '''
    #determines if the enemy can attack the square r, c
    '''
    def square_under_attack(self, r, c):
        self.white_to_move = not self.white_to_move  # switch to opponent point of view
        opp_moves = self.get_all_moves()
        self.white_to_move = not self.white_to_move  # switch turn back
        for move in opp_moves:
            if move.end_row == r and move.end_col == c:  # checks if square is under attack
                self.white_to_move = not self.white_to_move
                return True
        return False

    '''
    does not consider check
    '''
    def get_all_moves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of col in given row
                turn = self.board[r][c][0]  # saves color of the piece
                if turn == 'w' and self.white_to_move or turn == 'b' and not self.white_to_move:
                    piece = self.board[r][c][1]  # holds piece type
                    self.move_functions[piece](r, c, moves)
        return moves

    def get_pawn_moves(self, r, c, moves):
        if self.white_to_move:  # white pawn moves
            if self.board[r - 1][c] == "--":  # 1 square pawn advance
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # captures to the left
                if self.board[r - 1][c - 1][0] == 'b':  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # captures to the right
                if self.board[r - 1][c + 1][0] == 'b':  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:  # same as above for black pieces
            if not self.white_to_move:
                if self.board[r + 1][c] == "--":
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--":
                        moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def get_rook_moves(self, r, c, moves):
        if self.white_to_move:  # white rook moves
            for i in range(0, 8):  # responsible for downwards movement of the rook
                if r + i != r and r + i <= 7:
                    if self.board[r + i][c] == "--" or self.board[r + i][c][0] == "b":
                        moves.append(Move((r, c), (r + i, c), self.board))
            for i in range(0, 8):  # responsible for upwards movement of the rook
                if r - i != r and r - i >= 0:
                    if self.board[r - i][c] == "--" or self.board[r - i][c][0] == "b":
                        moves.append(Move((r, c), (r - i, c), self.board))
            for i in range(0, 8):
                if c + i != c and c + i <= 7:
                    if self.board[r][c + i] == "--" or self.board[r][c + i][0] == "b":
                        moves.append(Move((r, c), (r, c + i), self.board))
            for i in range(0, 8):
                if c - i != c and c - i >= 0:
                    if self.board[r][c - i] == "--" or self.board[r][c - i][0] == "b":
                        moves.append(Move((r, c), (r, c - i), self.board))
        else:
            for i in range(0, 8):  # responsible for downwards movement of the rook
                if r + i != r and r + i <= 7:
                    if self.board[r + i][c] == "--" or self.board[r + i][c][0] == "w":
                        moves.append(Move((r, c), (r + i, c), self.board))
            for i in range(0, 8):  # responsible for upwards movement of the rook
                if r - i != r and r - i >= 0:
                    if self.board[r - i][c] == "--" or self.board[r - i][c][0] == "w":
                        moves.append(Move((r, c), (r - i, c), self.board))
            for i in range(0, 8):  # responsible for movements to the right
                if c + i != c and c + i <= 7:
                    if self.board[r][c + i] == "--" or self.board[r][c + i][0] == "w":
                        moves.append(Move((r, c), (r, c + i), self.board))
            for i in range(0, 8):  # responsible for movements to the left
                if c - i != c and c - i >= 0:
                    if self.board[r][c - i] == "--" or self.board[r][c - i][0] == "w":
                        moves.append(Move((r, c), (r, c - i), self.board))

    def get_knight_moves(self, r, c, moves):
        if self.white_to_move:
            for row in range(-2, 3):  # goes through each row accessible for the knight
                for col in range(-2, 3):  # goes through each col accessible for the knight
                    if row ** 2 + col ** 2 == 5:  # checks if the combination of row and col is a valid one
                        if 0 <= r + row <= 7 and 0 <= c + col <= 7:  # checks if the cords are inbound
                            if self.board[r + row][c + col] == "--" or self.board[r + row][c + col][0] == "b":
                                moves.append(Move((r, c), (r + row, c + col), self.board))
        else:
            if self.white_to_move:
                for row in range(-2, 3):  # is responsible to select each tile in the knights row
                    for col in range(-2, 3):  # is responsible to select each tile in the knights col
                        if row ** 2 + col ** 2 == 5:  # checks if the combination of row and col is ...
                            if 0 <= r + row <= 7 and 0 <= c + col <= 7:  # checks if the position is inbound
                                if self.board[r + row][c + col] == "--" or self.board[r + row][c + col][0] == "w":
                                    moves.append(Move((r, c), (r + row, c + col), self.board))

    def get_queen_moves(self, r, c, moves):
        if self.white_to_move:  # white to move
            for row in range(-8, 8):  # goes through each row
                for col in range(-8, 8):  # goes through each col
                    if row ** 2 == col ** 2:  # checks if row and col are the same number works with negative too
                        if 0 <= r + row <= 7 and 0 <= c + col <= 7:  # checks if they are in bound
                            if self.board[r + row][c + col] == "--" or self.board[r + row][c + col][0] == "b":
                                moves.append(Move((r, c), (r + row, c + col), self.board))
            for i in range(0, 8):  # responsible for downwards movement of the rook
                if r + i != r and r + i <= 7:
                    if self.board[r + i][c] == "--" or self.board[r + i][c][0] == "b":
                        moves.append(Move((r, c), (r + i, c), self.board))
            for i in range(0, 8):  # responsible for upwards movement of the rook
                if r - i != r and r - i >= 0:
                    if self.board[r - i][c] == "--" or self.board[r - i][c][0] == "b":
                        moves.append(Move((r, c), (r - i, c), self.board))
            for i in range(0, 8):  # responsible for movement to the right
                if c + i != c and c + i <= 7:
                    if self.board[r][c + i] == "--" or self.board[r][c + i][0] == "b":
                        moves.append(Move((r, c), (r, c + i), self.board))
            for i in range(0, 8):  # responsible for movement to the left
                if c - i != c and c - i >= 0:
                    if self.board[r][c - i] == "--" or self.board[r][c - i][0] == "b":
                        moves.append(Move((r, c), (r, c - i), self.board))
        else:
            for row in range(-8, 8):
                for col in range(-8, 8):
                    if row ** 2 == col ** 2:
                        if 0 <= r + row <= 7 and 0 <= c + col <= 7:
                            if self.board[r + row][c + col] == "--" or self.board[r + row][c + col][0] == "w":
                                moves.append(Move((r, c), (r + row, c + col), self.board))

            for i in range(0, 8):  # responsible for downwards movement of the rook
                if r + i != r and r + i <= 7:
                    if self.board[r + i][c] == "--" or self.board[r + i][c][0] == "w":
                        moves.append(Move((r, c), (r + i, c), self.board))
            for i in range(0, 8):  # responsible for upwards movement of the rook
                if r - i != r and r - i >= 0:
                    if self.board[r - i][c] == "--" or self.board[r - i][c][0] == "w":
                        moves.append(Move((r, c), (r - i, c), self.board))
            for i in range(0, 8):  # responsible for movements to the right
                if c + i != c and c + i <= 7:
                    if self.board[r][c + i] == "--" or self.board[r][c + i][0] == "w":
                        moves.append(Move((r, c), (r, c + i), self.board))
            for i in range(0, 8):  # responsible for movements to the left
                if c - i != c and c - i >= 0:
                    if self.board[r][c - i] == "--" or self.board[r][c - i][0] == "w":
                        moves.append(Move((r, c), (r, c - i), self.board))

    def get_king_moves(self, r, c, moves):
        if self.white_to_move:
            if r - 1 >= 0:
                if self.board[r - 1][c] == "--" or self.board[r - 1][c] == "b":
                    moves.append(Move((r, c), (r - 1, c), self.board))
            if c - 1 >= 0:
                if self.board[r][c - 1] == "--" or self.board[r][c - 1] == "b":
                    moves.append(Move((r, c), (r, c - 1), self.board))
            if r - 1 >= 0 and c - 1 >= 0:
                if self.board[r - 1][c - 1] == "--" or self.board[r - 1][c - 1] == "b":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if r + 1 <= 7 and c - 1 >= 0:
                if self.board[r + 1][c - 1] == "--" or self.board[r + 1][c - 1] == "b":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if r - 1 >= 0 and c + 1 <= 7:
                if self.board[r - 1][c + 1] == "--" or self.board[r - 1][c + 1] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
            if r + 1 <= 7:
                if self.board[r + 1][c] == "--" or self.board[r + 1][c] == "b":
                    moves.append(Move((r, c), (r + 1, c), self.board))
            if c + 1 <= 7:
                if self.board[r][c + 1] == "--" or self.board[r][c + 1] == "b":
                    moves.append(Move((r, c), (r, c + 1), self.board))
            if c + 1 <= 7 and r + 1 <= 7:
                if self.board[r + 1][c + 1] == "--" or self.board[r + 1][c + 1] == "b":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

        else:
            if r - 1 >= 0:
                if self.board[r - 1][c] == "--" or self.board[r - 1][c] == "w":
                    moves.append(Move((r, c), (r - 1, c), self.board))
            if c - 1 >= 0:
                if self.board[r][c - 1] == "--" or self.board[r][c - 1] == "w":
                    moves.append(Move((r, c), (r, c - 1), self.board))
            if r - 1 >= 0 and c - 1 >= 0:
                if self.board[r - 1][c - 1] == "--" or self.board[r - 1][c - 1] == "w":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if r + 1 <= 7 and c - 1 >= 0:
                if self.board[r + 1][c - 1] == "--" or self.board[r + 1][c - 1] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if r - 1 >= 0 and c + 1 <= 7:
                if self.board[r - 1][c + 1] == "--" or self.board[r - 1][c + 1] == "w":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
            if r + 1 <= 7:
                if self.board[r + 1][c] == "--" or self.board[r + 1][c] == "w":
                    moves.append(Move((r, c), (r + 1, c), self.board))
            if c + 1 <= 7:
                if self.board[r][c + 1] == "--" or self.board[r][c + 1] == "w":
                    moves.append(Move((r, c), (r, c + 1), self.board))
            if c + 1 <= 7 and r + 1 <= 7:
                if self.board[r + 1][c + 1] == "--" or self.board[r + 1][c + 1] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def get_bishop_moves(self, r, c, moves):
        if self.white_to_move:  # white to move
            for row in range(-8, 8):  # goes through each row
                for col in range(-8, 8):  # goes through each col
                    if row ** 2 == col ** 2:  # checks if row and col are the same number works with negative too
                        if 0 <= r + row <= 7 and 0 <= c + col <= 7:  # checks if they are in bound
                            if self.board[r + row][c + col] == "--" or self.board[r + row][c + col][0] == "b":
                                moves.append(Move((r, c), (r + row, c + col), self.board))
        else:  # same as above black to move
            for row in range(-8, 8):
                for col in range(-8, 8):
                    if row ** 2 == col ** 2:
                        if 0 <= r + row <= 7 and 0 <= c + col <= 7:
                            if self.board[r + row][c + col] == "--" or self.board[r + row][c + col][0] == "w":
                                moves.append(Move((r, c), (r + row, c + col), self.board))


class Move:
    # maps keys to values
    # key : value
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}
    print(cols_to_files, rows_to_ranks)

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    '''
    overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        # need more work
        return self.get_rank_file(self.start_row, self.end_row) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
