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
        # fundo do menu (imagem FUNDO dentro da pasta assets)
        self.bg_image = pygame.image.load("assets/FUNDO.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (game.width, game.height))
        # fontes
        self.title_font = pygame.font.Font("assets/Alphacorsa Personal Use.ttf", 72)
        self.option_font = pygame.font.Font(None, 48)
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
                    self.game.change_scene("game", {"fase": 1})
                else:
                    pygame.quit(); import sys; sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            for i, opt in enumerate(self.options):
                rect = pygame.Rect(self.game.width//2 - 100, 200 + i*60, 200, 50)
                if rect.collidepoint(mx, my):
                    if i == 0:
                        self.game.change_scene("game", {"fase": 1})
                    else:
                        pygame.quit(); import sys; sys.exit()

    def update(self, dt): 
        pass

    def draw(self, screen):
        # fundo
        screen.blit(self.bg_image, (0, 0))
        # título estilizado
        title = self.title_font.render("F1 Racing", True, WHITE)
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 100))
        # opções
        for i, opt in enumerate(self.options):
            color = (0,255,0) if i == self.idx else WHITE
            txt = self.option_font.render(opt, True, color)
            screen.blit(txt, (screen.get_width()//2 - txt.get_width()//2, 200 + i*60))


class GameScene:
    def __init__(self, game, fase=1):
        self.game = game
        self.car = Car((400, 500))
        self.obstacles = []
        self.timer = 0
        self.passed = 0
        self.target = 10
        self.font = pygame.font.Font(None, 36)
        self.finish_line = None
        self.fase = fase

        # 🛣️ Pistas mais largas
        if fase == 1:
            self.track_rect = pygame.Rect(150, 0, 500, game.height)
            self.obstacle_speed = 5
        elif fase == 2:
            self.track_rect = pygame.Rect(200, 0, 400, game.height)
            self.obstacle_speed = 7
        else:
            self.track_rect = pygame.Rect(250, 0, 300, game.height)
            self.obstacle_speed = 9

    def handle_event(self, event): 
        pass

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.car.update(keys)

        # 🚧 Saída da pista
        if self.car.rect.left < self.track_rect.left or self.car.rect.right > self.track_rect.right:
            self.game.change_scene("result", {"msg": f"Saiu da pista! Game Over na fase {self.fase}"})

        # ⏱️ Gerar obstáculos
        self.timer += 1
        if self.timer > 60:
            self.timer = 0
            lane_x = random.randint(self.track_rect.left+20, self.track_rect.right-110)
            self.obstacles.append(Obstacle(lane_x, -110, speed=self.obstacle_speed))

        # 🔄 Atualizar obstáculos
        for obs in self.obstacles[:]:
            obs.update()
            if obs.off_screen(self.game.height):
                self.obstacles.remove(obs)
                self.passed += 1

        # 💥 Colisão pixel-perfect
        car_mask = pygame.mask.from_surface(self.car.image)
        for obs in self.obstacles:
            obs_mask = pygame.mask.from_surface(obs.image)
            offset = (obs.rect.x - self.car.rect.x, obs.rect.y - self.car.rect.y)
            if car_mask.overlap(obs_mask, offset):
                self.game.change_scene("result", {"msg": f"Colisão! Game Over na fase {self.fase}"})

        # 🏁 Linha de chegada
        if self.passed >= self.target and not self.finish_line:
            self.finish_line = pygame.Rect(self.track_rect.left, -20, self.track_rect.width, 20)

        if self.finish_line:
            self.finish_line.y += 5
            if self.car.rect.colliderect(self.finish_line):
                if self.fase < 3:
                    self.game.change_scene("game", {"fase": self.fase+1})
                else:
                    self.game.change_scene("result", {"msg": "Parabéns! Você venceu todas as fases!"})

    def draw(self, screen):
        screen.fill(GREEN)
        pygame.draw.rect(screen, GREY, self.track_rect)

        self.car.draw(screen)
        for obs in self.obstacles:
            obs.draw(screen)

        if self.finish_line:
            tile_size = 20
            for i in range(self.track_rect.width // tile_size):
                color = WHITE if i % 2 == 0 else BLACK
                rect = pygame.Rect(
                    self.track_rect.left + i*tile_size,
                    self.finish_line.y,
                    tile_size,
                    self.finish_line.height
                )
                pygame.draw.rect(screen, color, rect)

        score = self.font.render(
            f"Fase {self.fase} | Carros ultrapassados: {self.passed}",
            True,
            WHITE
        )
        screen.blit(score, (10, 10))


class ResultScene:
    def __init__(self, game, data):
        self.game = game
        self.data = data
        self.font = pygame.font.Font(None, 48)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.game.change_scene("menu")

    def update(self, dt): 
        pass

    def draw(self, screen):
        screen.fill(BLACK)
        msg = self.font.render(self.data.get("msg", "Fim de jogo"), True, WHITE)
        screen.blit(msg, (
            screen.get_width()//2 - msg.get_width()//2,
            screen.get_height()//2
        ))
        tip = self.font.render("Pressione tecla ou clique para voltar", True, WHITE)
        screen.blit(tip, (
            screen.get_width()//2 - tip.get_width()//2,
            screen.get_height()//2 + 60
        ))
