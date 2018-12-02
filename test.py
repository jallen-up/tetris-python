import random
import pygame
import time

line_piece = [[[0, 0, 1, 0],
               [0, 0, 1, 0],
               [0, 0, 1, 0],
               [0, 0, 1, 0]],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [1, 1, 1, 1],
               [0, 0, 0, 0]]]

class Piece:
    LINE_PIECE    = 0
    SQUARE_PIECE  = 1
    LEFT_L_PIECE  = 2
    RIGHT_L_PIECE = 3
    T_PIECE       = 4
    LEFT_Z_PIECE  = 5
    RIGHT_Z_PIECE = 6

    def __init__(self):
        self.shape = random.randint(0, 7)

    def rotate(self):
        `

class GameState:
    def __init__(self):
        self.running = True
        self.xpos = 50
        self.ypos = 50
        self.screen = pygame.display.set_mode((240, 180))
        self.tick_count = 0
        self.tick_mod = 100

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
            self.ypos += 16
            self.tick_count = 0

        self.draw_screen()

    def handle_keydown(self, key):
        if key == pygame.K_RIGHT:
            self.xpos += 16
        elif key == pygame.K_LEFT:
            self.xpos -= 16

    def handle_keyup(self, key):
        print("UP")

    def draw_background(self):
        self.screen.fill((0, 0, 0))

    def draw_screen(self):
        self.draw_background()
        image = pygame.image.load("block.png")
        self.screen.blit(image, (self.xpos, self.ypos))
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
