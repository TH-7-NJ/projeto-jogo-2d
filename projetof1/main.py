import pygame
import sys
from scenes import MenuScene, GameScene, ResultScene

class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("F1 Vertical")
        self.clock = pygame.time.Clock()
        self.scene = MenuScene(self)

    def change_scene(self, name, data=None):
        if name == "menu":
            self.scene = MenuScene(self)
        elif name == "game":
            self.scene = GameScene(self)
        elif name == "result":
            self.scene = ResultScene(self, data or {})

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                self.scene.handle_event(event)
            self.scene.update(dt)
            self.scene.draw(self.screen)
            pygame.display.flip()

if __name__ == "__main__":
    Game().run()
