import pygame
import time

#class Piece:
#    def __init__(self):

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
