import random
import pygame

#TODO: Implement uncover the field when clicked a blank cell, upto cells that contain a value or user flag


class Minesweeper:
    """Import Minesweeper, instance = Minesweeper(), instance.run()"""

    CAPTION = "Minesweeper 0.1"
    ICON = "Minesweeper.PNG"
    WIDTH, HEIGHT = 401, 450

    BG_COLOR = "white"
    CELL_COLOR_HIDDEN = (128, 128, 128)
    CELL_COLOR_VISIBLE = (200, 200, 200)
    CELL_BORDER = "black"
    ROWS, COLS = 15, 15
    MAX_BOMBS = 10

    BOMB_ID = -1
    FLAG_ID = -2
    EMPTY_ID = 0
    CELL_STATE_HIDDEN = 0
    CELL_STATE_VISIBLE = 1
    N_COLORS = {1:"black", 2:"blue", 3:"yellow", 4:"orange", 5:"purple", 6:"pink", 7:"cyan", 8:"magenta"}
    CELL_SIZE = round(WIDTH / COLS, 0)

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            row, col = self.get_grid_pos(pygame.mouse.get_pos())
            if row < Minesweeper.ROWS or col < Minesweeper.COLS:
              self.cover_field[row][col] = Minesweeper.CELL_STATE_VISIBLE
        self.draw()

    def get_grid_pos(self, mouse_pos):
        mx, my = mouse_pos
        row = int(my / Minesweeper.CELL_SIZE)
        col = int(mx / Minesweeper.CELL_SIZE)
        return row,col

    def create_empty_mine_field(self, field_rows, field_cols):
        self.mine_field = [
            [Minesweeper.EMPTY_ID for _ in range(field_cols)] for _ in range(field_rows)
        ]
        self.cover_field = [
            [Minesweeper.CELL_STATE_HIDDEN for _ in range(field_cols)] for _ in range(field_rows)
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
        cell_size = Minesweeper.CELL_SIZE
        for i, row in enumerate(self.mine_field):
            row_y = cell_size * i
            for j, field_value in enumerate(row):
                col_x = cell_size * j
                is_covered = self.cover_field[i][j] == 0
                if not is_covered:
                    pygame.draw.rect(self.win, Minesweeper.CELL_COLOR_VISIBLE, (col_x, row_y, cell_size, cell_size))
                    pygame.draw.rect(self.win, Minesweeper.CELL_BORDER, (col_x, row_y, cell_size, cell_size), 2)
                    if field_value > 0:
                        text = self.CELL_FONT.render(str(field_value), 1, Minesweeper.N_COLORS[field_value])
                        text_x = col_x + cell_size / 2 - text.get_width() / 2
                        text_y = row_y + cell_size / 2 - text.get_height() / 2
                        self.win.blit(text, (text_x, text_y))
                    if field_value == -1:
                        pygame.draw.rect(self.win, 'red', (col_x, row_y, cell_size, cell_size))
                        pygame.draw.rect(self.win, Minesweeper.CELL_BORDER, (col_x, row_y, cell_size, cell_size), 2)                        
                else:
                    pygame.draw.rect(self.win, Minesweeper.CELL_COLOR_HIDDEN, (col_x, row_y, cell_size, cell_size))
                    pygame.draw.rect(self.win, Minesweeper.CELL_BORDER, (col_x, row_y, cell_size, cell_size), 2)



def main():
    Minesweeper().run()


if __name__ == "__main__":
    main()
