import pygame
import time

class GameState:
    ypos = 0
    def tick(self):
        #ypos += 1
        print("ticking")
            
def main():
    state = GameState()

    pygame.init()

    screen = pygame.display.set_mode((240, 180))

    image = pygame.image.load("block.png")
    screen.blit(image, (50, 50))
    pygame.display.flip()

    running = True
    while running:
        state.tick()
        time.sleep(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__=="__main__":
    main()
