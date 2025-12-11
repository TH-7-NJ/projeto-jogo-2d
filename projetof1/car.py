import pygame

BLUE = (40, 200, 255)

class Car:
    def __init__(self, pos):
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=pos)
        self.speed = 6

    def update(self, keys):
       
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.rect.y -= self.speed
        
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600

    def draw(self, screen):
        screen.blit(self.image, self.rect)
