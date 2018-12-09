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
# TODO: Get tile_size from the actual image
tile_size = 16
screen = pygame.display.set_mode((600, 480))

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
            screen.blit(self.color, (block[0] * tile_size, block[1] * tile_size))

class Block:
    def __init__(self, color):
        self.color = color

    def draw(self, x, y):
        screen.blit(self.color, (x * tile_size, y * tile_size))

class GameState:
    def __init__(self):
        self.running = True
        self.tick_count = 0
        self.tick_mod = 25
        self.piece = Piece(self)
        if (self.piece == None):
            print("Failed to create piece")
        self.init_board()

    def init_board(self):
        self.board_width = 10
        self.board_height = 20

        self.board = [[None for y in range(self.board_height + 1)] for y in range(self.board_width + 1)]

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
                self.piece = Piece(self)
                num_rows = self.check_filled_rows()
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

    def handle_keyup(self, key):
        pass

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
            self.board[block[0]][block[1]] = Block(self.piece.color)
                    
    def draw_board(self):
        for i in range(self.board_width):
            for j in range(self.board_height):
                if self.board[i][j] != None:
                    self.board[i][j].draw(i, j)

    def draw_background(self):
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, self.board_width * 16, self.board_height * 16))

    def draw_screen(self):
        self.draw_background()
        self.draw_board()
        self.piece.draw()
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
