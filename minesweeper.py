import random
import pygame


class Minesweeper:
    """Import Minesweeper, instance = Minesweeper(), instance.run()"""

    CAPTION = "Minesweeper 0.1"
    ICON = "Minesweeper.PNG"
    WIDTH, HEIGHT = 500, 400
    BG_COLOR = "white"
    ROWS, COLS = 15, 15
    MAX_BOMBS = 10

    BOMB_ID = -1
    FLAG_ID = -2
    EMPTY_ID = 0

    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((Minesweeper.WIDTH, Minesweeper.HEIGHT))
        pygame.display.set_caption(Minesweeper.CAPTION)
        programIcon = pygame.image.load(Minesweeper.ICON)
        pygame.display.set_icon(programIcon)

        # Setup game play
        self.create_empty_mine_field(Minesweeper.ROWS, Minesweeper.COLS)
        self.generate_bomb_positions(Minesweeper.MAX_BOMBS)
        self.insert_bombs_in_field()
        self.set_neigbors_count()

        self.running = False

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

            self.play(event)

        pygame.quit()

    def play(self, event):
        # Add play functions here
        self.draw()

    def draw(self):
        self.win.fill(Minesweeper.BG_COLOR)
        pygame.display.update()

    def create_empty_mine_field(self, field_rows, field_cols):
        self.mine_field = [
            [Minesweeper.EMPTY_ID for _ in range(field_cols)] for _ in range(field_rows)
        ]

    def generate_bomb_positions(self, max_bombs):
        self.bomb_positions = set()
        while len(self.bomb_positions) < max_bombs:
            bomb_position = (
                random.randrange(0, Minesweeper.ROWS),
                random.randrange(0, Minesweeper.COLS),
            )
            if not bomb_position in self.bomb_positions:
                self.bomb_positions.add(bomb_position)

    def insert_bombs_in_field(self):
        bomb_num = 1
        print(f"\n")
        for bomb_pos in self.bomb_positions:
            row = bomb_pos[0]
            col = bomb_pos[1]
            self.mine_field[row][col] = Minesweeper.BOMB_ID

    def set_neigbors_count(self):
        for bomb_pos in self.bomb_positions:
            row = bomb_pos[0]
            col = bomb_pos[1]
            neighbors = self.get_neigbor_positions(row, col)
            for neighbor in neighbors:
                if not self.mine_field == Minesweeper.BOMB_ID:
                    neighbor_row = neighbor[0]
                    neighbor_col = neighbor[1]
                    self.mine_field[neighbor_row][neighbor_col] += 1

    def get_neigbor_positions(self, row, col):
        neighbors = []
        if row > 0:  # TOP
            neighbors.append((row - 1, col))
        if row < Minesweeper.ROWS - 1:  # BOTTOM
            neighbors.append((row + 1, col))
        if col > 0:  # LEFT
            neighbors.append((row, col - 1))
        if col < Minesweeper.COLS - 1:  # RIGHT
            neighbors.append((row, col + 1))
        if row > 0 and col > 0:  # TOP LEFT
            neighbors.append((row - 1, col - 1))
        if row > 0 and col < Minesweeper.COLS - 1:  # TOP RIGHT
            neighbors.append((row - 1, col + 1))
        if row < Minesweeper.ROWS - 1 and col > 0:  # BOTTOM LEFT
            neighbors.append((row + 1, col - 1))
        if row < Minesweeper.ROWS - 1 and col < Minesweeper.COLS - 1:  # BOTTOM RIGHT
            neighbors.append((row + 1, col + 1))

        return neighbors


def main():
    Minesweeper().run()


if __name__ == "__main__":
    main()
