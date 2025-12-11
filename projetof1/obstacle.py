import pygame
import random

RED = (200, 50, 50)

class Obstacle:
    def __init__(self, x, y, w=40, h=60, speed=5):
        self.image = pygame.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self):
        # obstáculo desce pela pista
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def off_screen(self, height):
        return self.rect.top > height
