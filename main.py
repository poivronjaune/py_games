import pygame


class Minesweeper():
    CAPTION = "Minesweeper 0.1"
    ICON    = 'Minesweeper.PNG'
    WIDTH, HEIGHT  = 500, 400

    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((Minesweeper.WIDTH, Minesweeper.HEIGHT))
        pygame.display.set_caption(Minesweeper.CAPTION)
        programIcon = pygame.image.load(Minesweeper.ICON)
        pygame.display.set_icon(programIcon)
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                else:
                    self.play(event)

        pygame.quit()

    def play(self, event):
        pass


def main():
    game_instance = Minesweeper()
    game_instance.run()

if __name__ == "__main__":
    main()