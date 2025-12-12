import pygame
import random

class Obstacle:
    def __init__(self, x, y, speed=5):
        car_images = [
            "assets/carenemy-mclaren.png",
            "assets/carenemy-mercedes.png",
            "assets/carenemy-ferrari.png"
        ]
        img_path = random.choice(car_images)
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 110))  # tamanho fixo
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def off_screen(self, height):
        return self.rect.top > height

    def get_hitbox(self):
        return self.rect.inflate(-10, -10)  # hitbox reduzida
