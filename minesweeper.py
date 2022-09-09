import random
import pygame


class Minesweeper:
    """Import Minesweeper, instance = Minesweeper(), instance.run()"""

    CAPTION = "Minesweeper 0.1"
    ICON = "Minesweeper.PNG"
    WIDTH, HEIGHT = 400, 450

    BG_COLOR = "white"
    CELL_COLOR = "grey"
    CELL_BORDER = "black"
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
        self.CELL_FONT = pygame.font.SysFont('comicsans', 15)

        # Setup game play
        self.create_empty_mine_field(Minesweeper.ROWS, Minesweeper.COLS)
        self.generate_bomb_positions(Minesweeper.MAX_BOMBS)
        self.insert_bombs_in_field()
        self.set_neigbors_count()

        self.print_mine_field_to_console()

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

    def print_mine_field_to_console(self):
        for row in range(0, Minesweeper.ROWS):
            for col in range(0, Minesweeper.COLS):
                sep = ',' if col < Minesweeper.COLS - 1 else ''
                print(f"{self.mine_field[row][col]:3}{sep}", end='')
            print(f"")

    def play(self, event):
        # Add play functions here
        self.draw()

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
        print(f"\n")
        for bomb_pos in self.bomb_positions:
            row = bomb_pos[0]
            col = bomb_pos[1]
            self.mine_field[row][col] = Minesweeper.BOMB_ID

    def set_neigbors_count(self):
        for bomb_pos in self.bomb_positions:
            row = bomb_pos[0]
            col = bomb_pos[1]
            neighbors = self.get_valid_neigbor_positions(row, col)
            for neighbor in neighbors:
                neighbor_row = neighbor[0]
                neighbor_col = neighbor[1]                
                if not self.mine_field[neighbor_row][neighbor_col] == Minesweeper.BOMB_ID:
                    self.mine_field[neighbor_row][neighbor_col] += 1

    def get_valid_neigbor_positions(self, row, col):
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

    def draw(self):
        self.win.fill(Minesweeper.BG_COLOR)
        self.draw_mine_field_values()
        pygame.display.update()

    def draw_mine_field_values(self):
        height_offset = 0
        cell_size = Minesweeper.WIDTH // Minesweeper.COLS
        for i, row in enumerate(self.mine_field):
            row_y = cell_size * i
            for j, field_value in enumerate(row):
                col_x = cell_size * j
                pygame.draw.rect(self.win, Minesweeper.CELL_COLOR, (col_x, row_y+height_offset, cell_size, cell_size))
                pygame.draw.rect(self.win, Minesweeper.CELL_BORDER, (col_x, row_y+height_offset, cell_size, cell_size), 2)
                text = self.CELL_FONT.render(str(field_value), 1, "red")
                text_x = col_x + cell_size / 2 - text.get_width() / 2
                text_y = row_y + cell_size / 2 - text.get_height() / 2
                self.win.blit(text, (text_x, text_y))
                


def main():
    Minesweeper().run()


if __name__ == "__main__":
    main()
