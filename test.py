import random
import pygame
import time

from PIL import Image

block = pygame.image.load("block.png")
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
        self.game_state = state

        if (self.shape == self.I_PIECE):
            im = Image.open('i.png')
            self.color = "Blue"
        elif (self.shape == self.O_PIECE):
            im = Image.open('o.png')
            self.color = "Yellow"
        elif (self.shape == self.LEFT_L_PIECE):
            im = Image.open('left_l.png')
            self.color = "Orange"
        elif (self.shape == self.RIGHT_L_PIECE):
            im = Image.open('right_l.png')
            self.color = "Cyan"
        elif (self.shape == self.T_PIECE):
            im = Image.open('t.png')
            self.color = "Purple"
        elif (self.shape == self.LEFT_J_PIECE):
            im = Image.open('left_j.png')
            self.color = "Green"
        elif (self.shape == self.RIGHT_J_PIECE):
            im = Image.open('right_j.png')
            self.color = "Pink"
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

    def point_out_of_bounds(self, x, y):
        print("point oob")
        print(x)
        print(y)
        if x > self.game_state.board_width - 1:
            print("returning true")
            return True
        elif x < 0:
            print("x less than 0")
            return True
        elif y > self.game_state.board_height - 1:
            return True
        elif y < 0:
            return True
        else:
            return False

    def rotation_unobstructed(self, test):
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.rotations[i, (self.get_next_rotation() * self.size) + j][0] == 0:
                        print(test)
                        if self.point_out_of_bounds(self.x + i + test[0], self.y + j + test[1]):
                            return False
                        if self.game_state.board[self.x + i + test[0]][self.y + j + test[1]] != None:
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
                print("Rotation good")
                can_rotate = True
                self.x += test[0]
                self.y += test[1]
                break
            else:
                print("Rotation bad")

        if can_rotate == True:
            self.rot_index += 1
            if self.rot_index == 4:
                self.rot_index = 0

    def draw(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.rotations[i, (self.rot_index * self.size) + j][0] == 0:
                    screen.blit(block, (self.x * 16 + i * 16, self.y * 16 + j * 16))

class Block:
    def __init__(self, color):
        self.color = color

class GameState:
    def __init__(self):
        self.running = True
        self.tick_count = 0
        self.tick_mod = 200
        self.current_piece = Piece(self)
        if (self.current_piece == None):
            print("Failed to create piece")
        self.init_board()

    def init_board(self):
        self.board_width = 10
        self.board_height = 20

        self.board = [[None for y in range(self.board_height + 1)] for x in range(self.board_width + 1)]

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
                self.current_piece = Piece(self)
            self.tick_count = 0

        self.draw_screen()

    def attempt_move_right(self):
        for i in range(0, self.current_piece.size):
            for j in range(0, self.current_piece.size):
                if self.current_piece.rotations[i, (self.current_piece.get_next_rotation() * self.current_piece.size) + j][0] == 0:
                    print("Current location")
                    print(self.current_piece.x + i + 1)
                    print(self.current_piece.y + j)
                    if self.current_piece.point_out_of_bounds(self.current_piece.x + i + 1, self.current_piece.y + j):
                        return False
                    else:
                        self.current_piece.x += 1
                        return True

    def attempt_move_left(self):
        for i in range(0, self.current_piece.size):
            for j in range(0, self.current_piece.size):
                if self.current_piece.rotations[i, (self.current_piece.get_next_rotation() * self.current_piece.size) + j][0] == 0:
                    if self.current_piece.point_out_of_bounds(self.current_piece.x + i - 1, self.current_piece.y + j):
                        return False
                    else:
                        self.current_piece.x -= 1
                        return True

    def handle_keydown(self, key):
        if key == pygame.K_RIGHT:
            self.attempt_move_right()
        elif key == pygame.K_LEFT:
            self.attempt_move_left()
        elif key == pygame.K_UP:
            self.current_piece.rotate(self.board_width, self.board_height)

    def handle_keyup(self, key):
        pass

    # TODO: Clean this up
    def drop_piece(self):
        for i in range(0, self.current_piece.size):
            for j in range(0, self.current_piece.size):
                if self.current_piece.rotations[i, (self.current_piece.rot_index * self.current_piece.size) + j][0] == 0:
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
        for i in range(0, self.current_piece.size):
            for j in range(0, self.current_piece.size):
                if self.current_piece.rotations[i, (self.current_piece.rot_index * self.current_piece.size) + j][0] == 0:
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
