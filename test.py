import random
import pygame
import time

from PIL import Image


block = pygame.image.load("block.png")
screen = pygame.display.set_mode((640, 480))

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
        self.x = 50
        self.y = 50

        if (self.shape == self.LINE_PIECE):
            self.rotations = Image.open('line.png').load()
        elif (self.shape == self.SQUARE_PIECE):
            self.rotations = Image.open('square.png').load()
        elif (self.shape == self.LEFT_L_PIECE):
            self.rotations = Image.open('left_l.png').load()
        elif (self.shape == self.RIGHT_L_PIECE):
            self.rotations = Image.open('right_l.png').load()
        elif (self.shape == self.T_PIECE):
            self.rotations = Image.open('t.png').load()
        elif (self.shape == self.LEFT_Z_PIECE):
            self.rotations = Image.open('left_z.png').load()
        elif (self.shape == self.RIGHT_Z_PIECE):
            self.rotations = Image.open('right_z.png').load()
        else:
            print("Invalid piece type")
            return None

    def rotate(self):
        self.rot_index += 1
        if (self.rot_index == 4):
            self.rot_index = 0

    def draw(self):
        for i in range(0, 4):
            for j in range(0, 4):
                if self.rotations[i, (self.rot_index * 4) + j][0] == 0:
                    screen.blit(block, (self.x + i * 16, self.y + j * 16))
                    

class GameState:
    def __init__(self):
        self.running = True
        self.tick_count = 0
        self.tick_mod = 100
        self.current_piece = Piece()
        if (self.current_piece == None):
            print("Failed to create piece")

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
            self.current_piece.y += 16
            self.tick_count = 0

        self.draw_screen()

    def handle_keydown(self, key):
        if key == pygame.K_RIGHT:
            self.current_piece.x += 16
        elif key == pygame.K_LEFT:
            self.current_piece.x -= 16
        elif key == pygame.K_UP:
            self.current_piece.rotate()

    def handle_keyup(self, key):
        pass

    def draw_background(self):
        screen.fill((0, 0, 0))

    def draw_screen(self):
        self.draw_background()
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
