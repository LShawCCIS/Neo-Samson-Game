import pygame
import random
import math

class Bullet:
    def __init__(self, image, x, y):
        self.image = image
        self.image = pygame.image.load(image)
        self.rect_ = self.image.get_rect()
        self.rect_.x = x
        self.rect_.y = y
        self.is_alive = True

    def move_bullet(self):
        self.x += self.dx
        self.y += self.dy
        self.rect_.x = int(self.x)
        self.rect_.y = int(self.y)
        
class PistolBullet(Bullet):
    def __init__(self, image, x, y, t_x=1200, t_y=340, speed=10, damage=5):
        Bullet.__init__(self, image, x, y)
        self.speed = speed
        self.damage = damage
        angle = math.atan2(t_y - self.rect_.y, \
                           t_x - self.rect_.x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        self.x = x
        self.y = y

class SniperBullet(Bullet):
    def __init__(self, image, x, y, t_x=1200, t_y=340, speed=15, damage=10):
        Bullet.__init__(self, image, x, y)
        self.speed = speed
        self.damage = damage
        angle = math.atan2(t_y - self.rect_.y, \
                           t_x - self.rect_.x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        self.x = x
        self.y = y
  
