from grid import Grid
from blocks import *
import random
import pygame

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = self.initialize_blocks()
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.initialize_sounds()

    def initialize_blocks(self):
        return [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]

    def initialize_sounds(self):
        self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")
        pygame.mixer.music.load("Sounds/music.ogg")
        pygame.mixer.music.play(-1)

    def update_score(self, lines_cleared, move_down_points):
        scores = {1: 100, 2: 300, 3: 500}
        self.score += scores.get(lines_cleared, 0) + move_down_points

    def get_random_block(self):
        if not self.blocks:
            self.blocks = self.initialize_blocks()
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.move_block(0, -1, 0, 1)

    def move_right(self):
        self.move_block(0, 1, 0, -1)

    def move_down(self):
        if not self.move_block(1, 0, -1, 0):
            self.lock_block()

    def move_block(self, dx, dy, undo_dx, undo_dy):
        self.current_block.move(dx, dy)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(undo_dx, undo_dy)
            return False
        return True

    def lock_block(self):
        for position in self.current_block.get_cell_positions():
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
        if not self.block_fits():
            self.game_over = True

    def reset(self):
        self.grid.reset()
        self.blocks = self.initialize_blocks()
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def block_fits(self):
        return all(self.grid.is_empty(tile.row, tile.column) for tile in self.current_block.get_cell_positions())

    def rotate(self):
        self.current_block.rotate()
        if not self.block_inside() or not self.block_fits():
            self.current_block.undo_rotation()
        else:
            self.rotate_sound.play()

    def block_inside(self):
        return all(self.grid.is_inside(tile.row, tile.column) for tile in self.current_block.get_cell_positions())

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)
        self.draw_next_block(screen)

    def draw_next_block(self, screen):
        positions = {3: (255, 290), 4: (255, 280)}
        x, y = positions.get(self.next_block.id, (270, 270))
        self.next_block.draw(screen, x, y)
