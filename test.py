import random
import pygame
import time

from PIL import Image

block = pygame.image.load("block.png")
screen = pygame.display.set_mode((160, 320))

# TODO: Rewrite how pieces are identified
class Piece:
    LINE_PIECE    = 0
    SQUARE_PIECE  = 1
    LEFT_L_PIECE  = 2
    RIGHT_L_PIECE = 3
    T_PIECE       = 4
    LEFT_Z_PIECE  = 5
    RIGHT_Z_PIECE = 6

    def __init__(self):
        self.shape = random.randint(0, 6)
        self.rot_index = 0
        self.x = 4
        self.y = 0

        if (self.shape == self.LINE_PIECE):
            self.rotations = Image.open('line.png').load()
            self.color = "Blue"
        elif (self.shape == self.SQUARE_PIECE):
            self.rotations = Image.open('square.png').load()
            self.color = "Yellow"
        elif (self.shape == self.LEFT_L_PIECE):
            self.rotations = Image.open('left_l.png').load()
            self.color = "Orange"
        elif (self.shape == self.RIGHT_L_PIECE):
            self.rotations = Image.open('right_l.png').load()
            self.color = "Cyan"
        elif (self.shape == self.T_PIECE):
            self.rotations = Image.open('t.png').load()
            self.color = "Purple"
        elif (self.shape == self.LEFT_Z_PIECE):
            self.rotations = Image.open('left_z.png').load()
            self.color = "Green"
        elif (self.shape == self.RIGHT_Z_PIECE):
            self.rotations = Image.open('right_z.png').load()
            self.color = "Pink"
        else:
            print("Invalid piece type")
            return None

    def rotate(self, width, height):
        self.rot_index += 1
        if (self.rot_index == 4):
            self.rot_index = 0

        for i in range(0, 4):
            for j in range(0, 4):
                while self.rotations[i, (self.rot_index * 4) + j][0] == 0 and self.x + i > width - 1:
                    self.x - 1
                while self.rotations[i, (self.rot_index * 4) + j][0] == 0 and i <= 0:
                    self.x + 1
                

    def draw(self):
        for i in range(0, 4):
            for j in range(0, 4):
                if self.rotations[i, (self.rot_index * 4) + j][0] == 0:
                    screen.blit(block, (self.x * 16 + i * 16, self.y * 16 + j * 16))

class Block:
    def __init__(self, color):
        self.color = color

class GameState:
    def __init__(self):
        self.running = True
        self.tick_count = 0
        self.tick_mod = 50
        self.current_piece = Piece()
        if (self.current_piece == None):
            print("Failed to create piece")
        self.init_board()

    def init_board(self):
        self.board_width = 10
        self.board_height = 20

        self.board = [[None for y in range(self.board_height)] for x in range(self.board_width)]

    def tick(self):
        self.tick_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
            elif event.type == pygame.KEYUP:
                self.handle_keyup(event.key)

        if (self.tick_count % self.tick_mod == 0):
            if self.drop_piece() == 1:
                self.current_piece = Piece()
            self.tick_count = 0

        self.draw_screen()

    def handle_keydown(self, key):
        if key == pygame.K_RIGHT:
            self.current_piece.x += 1
        elif key == pygame.K_LEFT:
            self.current_piece.x -= 1
        elif key == pygame.K_UP:
            self.current_piece.rotate(self.board_width, self.board_height)

    def handle_keyup(self, key):
        pass

    # TODO: Clean this up
    def drop_piece(self):
        for i in range(0, 4):
            for j in range(0, 4):
                if self.current_piece.rotations[i, (self.current_piece.rot_index * 4) + j][0] == 0:
                    if self.current_piece.y + j + 1 > self.board_height - 1:
                        self.lock_piece()
                        return 1
                    if self.board[self.current_piece.x + i][self.current_piece.y + j + 1] != None:
                        self.lock_piece()
                        return 1

        self.current_piece.y += 1
        return 0

    # TODO: Clean this up...
    def lock_piece(self):
        for i in range(0, 4):
            for j in range(0, 4):
                if self.current_piece.rotations[i, (self.current_piece.rot_index * 4) + j][0] == 0:
                    self.board[self.current_piece.x + i][self.current_piece.y + j] = Block(self.current_piece.color)
                     
    def draw_board(self):
        for i in range(self.board_width):
            for j in range(self.board_height):
                if self.board[i][j] != None:
                    screen.blit(block, (i * 16, j * 16))

    def draw_background(self):
        screen.fill((0, 0, 0))

    def draw_screen(self):
        self.draw_background()
        self.draw_board()
        self.current_piece.draw()
        pygame.display.flip()
            
def main():
    pygame.init()
    state = GameState()

    running = True
    while state.running:
        state.tick()
        time.sleep(0.01)


if __name__=="__main__":
    main()
