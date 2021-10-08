import sys

import pygame
from Code import ChessEngine

pygame.init()

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wQ", "wK", "wB", "wN", "wR", "wp"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False  # flag variable for when a move is made

    load_images()
    running = True
    sq_selected = ()  # last click of the user (row, col
    player_clicks = []  # keeps track of player clicks [(6, 4),(4, 4)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()  # x y location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):
                    sq_selected = ()  # deselect
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)  # append 1st and 2nd click
                if len(player_clicks) == 2:  # after 2nd click
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                    sq_selected = ()  # resets user clicks
                    player_clicks = []
            # key handlers
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:  # when z is pressed
                    gs.undo_move()
            if move_made:
                valid_moves = gs.get_valid_moves()
                move_made = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        pygame.display.flip()


# responsible for graphics
def drawGameState(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    x_cord = 64
    y_cord = 0
    counter_row = 0
    # draws the grey tiles of the screen -- ineffective needs work look draw pieces
    for i in range(0, 33):
        pygame.draw.rect(screen, (169, 169, 169), [x_cord, y_cord, 64, 64])
        x_cord += 128

        if x_cord >= 512 and counter_row % 2 == 0:
            x_cord = 0
            y_cord += 64
            counter_row += 1

        elif x_cord >= 512 and counter_row % 2 != 0:
            x_cord = 64
            y_cord += 64
            counter_row += 1

    # resets the cords and draws the white tiles of the screen -- ineffective
    x_cord = 0
    y_cord = 0
    counter_row = 0
    for i in range(0, 33):
        pygame.draw.rect(screen, (255, 250, 255), [x_cord, y_cord, 64, 64])
        x_cord += 128

        if x_cord >= 512 and counter_row % 2 != 0:
            x_cord = 0
            y_cord += 64
            counter_row += 1

        elif x_cord >= 512 and counter_row % 2 == 0:
            x_cord = 64
            y_cord += 64
            counter_row += 1


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
