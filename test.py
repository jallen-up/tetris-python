import random
import pygame
import time

from PIL import Image

blue = pygame.image.load("blue.png")
yellow = pygame.image.load("yellow.png")
orange = pygame.image.load("orange.png")
cyan = pygame.image.load("cyan.png")
purple = pygame.image.load("purple.png")
green = pygame.image.load("green.png")
pink = pygame.image.load("pink.png")
bkgd = pygame.image.load("block_bak.png")
# TODO: Get tile_size from the actual image
tile_size = 16
pygame.font.init()
game_font = pygame.font.SysFont('Arial', 20)

screen_width = 600
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
 
# Lists of offsets to try when we have an invalid rotation
wallkick_offsets = [[(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
                    [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
                    [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
                    [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]]

wallkick_offsets_i = [[(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
                    [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
                    [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
                    [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)]]

# TODO: Rewrite how pieces are identified
class Piece:
    I_PIECE       = 0
    O_PIECE       = 1
    LEFT_L_PIECE  = 2
    RIGHT_L_PIECE = 3
    T_PIECE       = 4
    LEFT_J_PIECE  = 5
    RIGHT_J_PIECE = 6

    def __init__(self, state):
        self.shape = random.randint(0, 6)
        self.rot_index = 0
        self.x = 4
        self.y = 0
        self.state = state

        if (self.shape == self.I_PIECE):
            im = Image.open('i.png')
            self.color = blue
        elif (self.shape == self.O_PIECE):
            im = Image.open('o.png')
            self.color = yellow
        elif (self.shape == self.LEFT_L_PIECE):
            im = Image.open('left_l.png')
            self.color = orange
        elif (self.shape == self.RIGHT_L_PIECE):
            im = Image.open('right_l.png')
            self.color = cyan
        elif (self.shape == self.T_PIECE):
            im = Image.open('t.png')
            self.color = purple
        elif (self.shape == self.LEFT_J_PIECE):
            im = Image.open('left_j.png')
            self.color = green
        elif (self.shape == self.RIGHT_J_PIECE):
            im = Image.open('right_j.png')
            self.color = pink
        else:
            print("Invalid piece type")
            return None

        self.size = im.size[0]
        self.rotations = im.load()

    def get_next_rotation(self):
        ret = self.rot_index + 1
        if ret == 4:
            ret = 0

        return ret

    def block_oob(self, x, y):
        if x > self.state.board_width - 1:
            return True
        elif x < 0:
            return True
        elif y > self.state.board_height - 1:
            return True
        elif y < 0:
            return True
        else:
            return False

    def has_block_at(self, x, y, rot_index):
        return self.rotations[x, (rot_index * self.size) + y][0] == 0

    def get_blocks(self, rot_index):
        blocks = []
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.has_block_at(i, j, rot_index):
                    blocks.append((self.x + i, self.y + j))

        return blocks

    def rotation_unobstructed(self, test):
        for block in self.get_blocks(self.get_next_rotation()):
            if self.block_oob(block[0] + test[0], block[1] + test[1]):
                return False
            if self.state.board[block[0] + test[0]][block[1] + test[1]]:
                return False

        return True

    def rotate(self, width, height):
        can_rotate = False
        if self.shape == Piece.I_PIECE:
            offsets = wallkick_offsets_i
        else:
            offsets = wallkick_offsets

        for test in offsets[self.get_next_rotation()]:
            if self.rotation_unobstructed(test):
                self.x += test[0]
                self.y += test[1]
                can_rotate = True
                break

        if can_rotate == True:
            self.rot_index += 1
            if self.rot_index == 4:
                self.rot_index = 0

    def draw(self):
        for block in self.get_blocks(self.rot_index):
            screen.blit(self.color, (self.state.board_x + (block[0] * tile_size), self.state.board_y + (block[1] * tile_size)))

class Block:
    def __init__(self, color, state):
        self.color = color
        self.state = state

    def draw(self, x, y):
        screen.blit(self.color, (self.state.board_x + (x * tile_size), self.state.board_y + (y * tile_size)))

class GameState:
    def __init__(self):
        self.running = True
        self.tick_count = 0
        self.tick_thresh = 150
        self.piece = Piece(self)
        if (self.piece == None):
            print("Failed to create piece")
        self.init_board()
        self.board_x = 100
        self.board_y = 100
        self.score = 0
        self.level = 0
        self.lines_cleared = 0
        self.speedy = False
        self.speedy_thresh = 15
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.board_x, self.board_y, self.board_width * 16, self.board_height * 16))
        self.end_game = True
        self.game_over = False

    def init_board(self):
        self.board_width = 10
        self.board_height = 20

        self.board = [[None for y in range(self.board_height + 1)] for y in range(self.board_width + 1)]

    def display_start_screen(self):
        go = True
        while go:
            screen.fill((0, 0, 0))
            mouse = pygame.mouse.get_pos()
            
            # TODO: Improve size and position of the game over screen
            rect = pygame.Rect(screen_width / 2, (screen_height / 2) + 25, 100, 25)
            if rect.collidepoint(mouse):
                if pygame.mouse.get_pressed()[0] == 1:
                    return
                pygame.draw.rect(screen, (250, 250, 250), pygame.Rect(screen_width / 2, (screen_height / 2) + 25, 100, 25))
            else:
                pygame.draw.rect(screen, (230, 230, 230), pygame.Rect(screen_width / 2, (screen_height / 2) + 25, 100, 25))
            game_over = game_font.render('Tetris', False, (255, 255, 255))
            screen.blit(game_over, (screen_width / 2, screen_height / 2))
            game_over = game_font.render('Play Game', False, (0, 0, 0))
            screen.blit(game_over, (screen_width / 2, (screen_height / 2) + 25))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def display_game_over_screen(self):
        go = True
        while go:
            screen.fill((0, 0, 0))
            mouse = pygame.mouse.get_pos()
            
            # TODO: Improve size and position of the game over screen
            rect = pygame.Rect(screen_width / 2, (screen_height / 2) + 25, 100, 25)
            if rect.collidepoint(mouse):
                if pygame.mouse.get_pressed()[0] == 1:
                    return
                pygame.draw.rect(screen, (250, 250, 250), pygame.Rect(screen_width / 2, (screen_height / 2) + 25, 100, 25))
            else:
                pygame.draw.rect(screen, (230, 230, 230), pygame.Rect(screen_width / 2, (screen_height / 2) + 25, 100, 25))
            game_over = game_font.render('Game Over', False, (255, 255, 255))
            screen.blit(game_over, (screen_width / 2, screen_height / 2))
            game_over = game_font.render('Play Again', False, (0, 0, 0))
            screen.blit(game_over, (screen_width / 2, (screen_height / 2) + 25))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        
    def tick(self):
        self.tick_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
            elif event.type == pygame.KEYUP:
                self.handle_keyup(event.key)

        # BUG: "speedy" speed is not consistent across different levels
        self.tick_count += self.level + 1
        if self.tick_count >= self.tick_thresh or (self.speedy and self.tick_count >= self.speedy_thresh):
            if self.drop_piece() == 1:
                if self.end_game:
                    self.game_over = True
                    self.display_game_over_screen()
                    return 1
                
                self.piece = Piece(self)
                self.end_game = True
                num_rows = self.check_filled_rows()
                if num_rows == 4:
                    self.score += 1200 * (self.level + 1)
                elif num_rows == 3:
                    self.score += 600 * (self.level + 1)
                elif num_rows == 2:
                    self.score += 100 * (self.level + 1)
                elif num_rows == 1:
                    self.score += 40 * (self.level + 1)

                self.lines_cleared += num_rows
                if self.lines_cleared >= 10:
                    if self.level < 29:
                        self.level += 1
                        self.lines_cleared = 0
            else:
                if self.end_game:
                    self.end_game = False
                    
            self.tick_count = 0

        self.draw_screen()

    def check_filled_rows(self):
        ret = 0
        marked_rows = []
        for i in range(self.board_height):
            count = 0
            for j in range(self.board_width):
                if self.board[j][i] != None:
                    count += 1

            if count == 10:
                marked_rows.append(i)
                ret += 1
        
        for row in marked_rows:
             for i in reversed(range(0, row + 1)):
                 for j in range(self.board_width):
                     self.board[j][i] = None
                     self.board[j][i] = self.board[j][i - 1]
                     self.board[j][i - 1] = None
        return ret

    def attempt_move_right(self):
        for block in self.piece.get_blocks(self.piece.rot_index):            
            if self.piece.block_oob(block[0] + 1, block[1]):
                return False
            if self.board[block[0] + 1][block[1]] != None:
                return False
                    
        self.piece.x += 1
        return True

    def attempt_move_left(self):
        for block in self.piece.get_blocks(self.piece.rot_index):            
            if self.piece.block_oob(block[0] - 1, block[1]):
                return False
            if self.board[block[0] - 1][block[1]] != None:
                return False
        
        self.piece.x -= 1
        return True

    def handle_keydown(self, key):
        if key == pygame.K_RIGHT:
            self.attempt_move_right()
        elif key == pygame.K_LEFT:
            self.attempt_move_left()
        elif key == pygame.K_UP:
            self.piece.rotate(self.board_width, self.board_height)
        elif key == pygame.K_DOWN:
            self.speedy = True

    def handle_keyup(self, key):
        if key == pygame.K_DOWN:
            self.speedy = False

    def drop_piece(self):
        for block in self.piece.get_blocks(self.piece.rot_index):
            if block[1] + 1 > self.board_height - 1:
                self.lock_piece()
                return 1
            if self.board[block[0]][block[1] + 1] != None:
                self.lock_piece()
                return 1

        self.piece.y += 1
        return 0

    def lock_piece(self):
        for block in self.piece.get_blocks(self.piece.rot_index):
            self.board[block[0]][block[1]] = Block(self.piece.color, self)
                    
    def draw_board(self):
        for i in range(self.board_width):
            for j in range(self.board_height):
                if self.board[i][j] != None:
                    self.board[i][j].draw(i, j)
                else:
                    screen.blit(bkgd, (self.board_x + (i * tile_size), self.board_y + (j * tile_size)))

    def draw_background(self):
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.board_x, self.board_y, self.board_width * 16, self.board_height * 16))
        score = game_font.render('Score: %s' % self.score, False, (255, 255, 255))
        screen.blit(score, (400, 200))
        level = game_font.render('Level: %s' % self.level, False, (255, 255, 255))
        screen.blit(level, (400, 150))

    def draw_screen(self):
        self.draw_background()
        self.draw_board()
        self.piece.draw()
        pygame.display.flip()
            
def main():
    pygame.init()
    state = GameState()

    state.display_start_screen()
    running = True
    while state.running:
        if state.tick() == 1:
            state = GameState()
        time.sleep(0.005)


if __name__=="__main__":
    main()
