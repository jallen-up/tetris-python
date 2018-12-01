import pygame

def main():
    pygame.init()

    screen = pygame.display.set_mode((240, 180))

    image = pygame.image.load("/home/jallen/Pictures/test.png")
    screen.blit(image, (50, 50))
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__=="__main__":
    main()
