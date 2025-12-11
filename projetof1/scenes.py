import pygame
import random
from car import Car
from obstacle import Obstacle

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
GREY = (60, 60, 60)

class MenuScene:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 48)
        self.options = ["Jogar", "Sair"]
        self.idx = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.idx = (self.idx - 1) % len(self.options)
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.idx = (self.idx + 1) % len(self.options)
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.idx == 0:
                    self.game.change_scene("game")
                else:
                    pygame.quit(); import sys; sys.exit()

    def update(self, dt): pass

    def draw(self, screen):
        screen.fill(BLACK)
        title = self.font.render("F1 Vertical", True, WHITE)
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 100))
        for i, opt in enumerate(self.options):
            color = (0,255,0) if i == self.idx else WHITE
            txt = self.font.render(opt, True, color)
            screen.blit(txt, (screen.get_width()//2 - txt.get_width()//2, 200 + i*60))


class GameScene:
    def __init__(self, game):
        self.game = game
        self.car = Car((400, 500))
        self.obstacles = []
        self.timer = 0
        self.passed = 0
        self.target = 10
        self.font = pygame.font.Font(None, 36)
        self.finish_line = None

        # pista central
        self.track_rect = pygame.Rect(200, 0, 400, game.height)

    def handle_event(self, event): pass

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.car.update(keys)

        # verificar se carro saiu da pista
        if not self.track_rect.contains(self.car.rect):
            self.game.change_scene("result", {"msg": "Saiu da pista! Game Over!"})

        # gerar obstáculos dentro da pista
        self.timer += 1
        if self.timer > 60:
            self.timer = 0
            lane_x = random.choice([220, 300, 380, 460, 540])  # posições dentro da pista
            self.obstacles.append(Obstacle(lane_x, -60))

        # atualizar obstáculos
        for obs in self.obstacles[:]:
            obs.update()
            if obs.off_screen(self.game.height):
                self.obstacles.remove(obs)
                self.passed += 1

        # colisão com outros carros
        for obs in self.obstacles:
            if self.car.rect.colliderect(obs.rect):
                self.game.change_scene("result", {"msg": "Colisão! Game Over!"})

        # linha de chegada
        if self.passed >= self.target and not self.finish_line:
            self.finish_line = pygame.Rect(200, -20, 400, 20)

        if self.finish_line:
            self.finish_line.y += 5
            if self.car.rect.colliderect(self.finish_line):
                self.game.change_scene("result", {"msg": "Você venceu!"})

    def draw(self, screen):
        # grama
        screen.fill(GREEN)
        # pista
        pygame.draw.rect(screen, GREY, self.track_rect)

        # carro e obstáculos
        self.car.draw(screen)
        for obs in self.obstacles:
            obs.draw(screen)

        # linha de chegada
        if self.finish_line:
            pygame.draw.rect(screen, WHITE, self.finish_line)

        # HUD
        score = self.font.render(f"Carros ultrapassados: {self.passed}", True, WHITE)
        screen.blit(score, (10, 10))


class ResultScene:
    def __init__(self, game, data):
        self.game = game
        self.data = data
        self.font = pygame.font.Font(None, 48)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.game.change_scene("menu")

    def update(self, dt): pass

    def draw(self, screen):
        screen.fill(BLACK)
        msg = self.font.render(self.data["msg"], True, WHITE)
        screen.blit(msg, (screen.get_width()//2 - msg.get_width()//2, screen.get_height()//2))
        tip = self.font.render("Pressione tecla ou clique para voltar", True, WHITE)
        screen.blit(tip, (screen.get_width()//2 - tip.get_width()//2, screen.get_height()//2 + 60))
