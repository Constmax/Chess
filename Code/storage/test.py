import pygame
import sys

# initialize pygame
pygame.init()
BLACK = (0, 0, 0)
WHITE = (120, 20, 20)

# create screen
WINDOW_WIDTH = 480
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH))

# Title and Icon
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Chess")

# board
chess_board = pygame.image.load('chess_board.png')


def background():
    screen.blit(chess_board, (0, 0))


# Pieces
class Pieces:
    def __init__(self, team, type, image, killable=None):
        self.team = team
        self.type = type
        self.image = image
        self.killable = killable


"""
bp = Pieces('b', 'p', 'bp.png')
br = Pieces('b', 'r', 'bR.png')
bb = Pieces('b', 'b', 'bB.png')
bkn = Pieces('b', 'kn', 'bN.png')
bq = Pieces('b', 'q', 'bQ.png')
bk = Pieces('b', 'k', 'bK.png')

wp = Pieces('w', 'p', 'wp.png')
wr = Pieces('w', 'r', 'rooK_w.png')
wb = Pieces('w', 'b', 'wB.png')
wkn = Pieces('w', 'kn', 'wN.png')
wq = Pieces('w', 'q', 'wQ.png')
wk = Pieces('w', 'k', 'wK.png')
"""

# board
board = [['i ' for i in range(8)] for j in range(8)]

# load game

starting_order = {(0, 0): br.image, (1, 0): bkn.image, (2, 0): bb.image, (3, 0): bk.image,
                  (4, 0): bq.image, (5, 0): bb.image, (6, 0): bkn.image, (7, 0): br.image,

                  (0, 1): bp.image, (1, 1): bp.image, (2, 1): bp.image, (3, 1): bp.image,
                  (4, 1): bp.image, (5, 1): bp.image, (6, 1): bp.image, (7, 1): bp.image,

                  (0, 6): wp.image, (1, 6): wp.image, (2, 6): wp.image, (3, 6): wp.image,
                  (4, 6): wp.image, (5, 6): wp.image, (6, 6): wp.image, (7, 6): wp.image,

                  (0, 7): wr.image, (1, 7): wkn.image, (2, 7): wb.image, (3, 7): wk.image,
                  (4, 7): wq.image, (5, 7): wb.image, (6, 7): wkn.image, (7, 7): wr.image,

                  }

board = {(0, 0): br, (1, 0): bkn, (2, 0): bb, (3, 0): bk,
         (4, 0): bq, (5, 0): bb, (6, 0): bkn, (7, 0): br,

         (0, 1): bp, (1, 1): bp, (2, 1): bp, (3, 1): bp,
         (4, 1): bp, (5, 1): bp, (6, 1): bp, (7, 1): bp,

         (0, 6): wp, (1, 6): wp, (2, 6): wp, (3, 6): wp,
         (4, 6): wp, (5, 6): wp, (6, 6): wp, (7, 6): wp,

         (0, 7): wr, (1, 7): wkn, (2, 7): wb, (3, 7): wk,
         (4, 7): wq, (5, 7): wb, (6, 7): wkn, (7, 7): wr,
         }


def load_starting_characters(starting_oder):
    for i in starting_oder:
        if starting_order is not None:
            player_x = i[0] * 60
            player_y = i[1] * 60
            screen.blit(pygame.image.load(starting_order[i]), (player_x, player_y))


def get_object(board):
    try:
        board[(0, 2)] = board.pop(9)
    except:
        print("dic error")


def load_characters(board):
    for i in board:
        player_x = i[0] * 60
        player_y = i[1] * 60
        screen.blit(pygame.image.load(starting_order[i]), (player_x, player_y))


count = True
# game loop
while True:
    screen.fill((0, 0, 0))
    background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            get_object(board)
            count = False

    if count:
        load_starting_characters(starting_order)
        count = False
    if not count:
        load_characters(board)
    pygame.display.update()
