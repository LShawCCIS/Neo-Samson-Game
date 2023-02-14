import pygame
import math
import random
import copy
from Weapons import *
from Bullet import *

pygame.mixer.quit()
pygame.mixer.init(44100, -16, 2, 32)
pygame.init()

class Philistine:
    death_sounds = []
    for i in range(7):
        dsound = pygame.mixer.Sound(f"sounds/Philistines/Phil_Death_{i + 1}.wav")
        death_sounds.append(dsound)
    def __init__(self, images, W=1200, H=680, health=1):
        self.image = pygame.image.load(images[0][0])
        self.images = images # starting sprite image
        self.rect_ = self.image.get_rect() # rect
        self.rect_.x = random.randint(-200, -50) # start off of the screen
        self.rect_.y = random.randint(0, H)
        self.dx = 2.0
        self.dy = 2.0
        self.W = W
        self.H = H
        self.direction = 0
        self.animation = 0
        self.animation_speed = 0.1
        self.target_health = health

    def take_damage(self, damage):
        self.target_health -= damage

    def get_heals(self, heals):
        self.target_health += heals

    def play_death(self):
        sound = random.randint(0, len(Philistine.death_sounds) - 1)
        Philistine.death_sounds[sound].play()

    def animate(self):
        if self.animation < len(self.images[self.direction]):
            self.animation += self.animation_speed
        else:
            self.animation = 0
        self.change_image()
        
    def change_image(self):
        if self.animation >= len(self.images[self.direction]):
            self.animation = 0
        self.image = \
            pygame.image.load(self.images[self.direction][int(self.animation)])
        

class MeleePhilistine(Philistine):
    def __init__(self, images, W=1200, H=680):
        Philistine.__init__(self, images, W, H, 15)
        self.points = 5
        self.speed = random.randint(1,100)
        
    def move_towards_samson(self, samson):
        hit_samson = False
        vector = pygame.math.Vector2((samson.rect_.x) - self.rect_.x,
                                     (samson.rect_.y) - self.rect_.y)
        if vector.length() != 0:
            vector.normalize()
            vector.scale_to_length(self.dx)
            if self.speed >= 99:
                self.rect_.move_ip(vector * 2)
            elif self.speed >= 75:
                self.rect_.move_ip(vector * 1.5)
            else:
                self.rect_.move_ip(vector)
                # this is rectangle collision
            if  (samson.rect_.x) < self.rect_.x + self.rect_.w and \
                (samson.rect_.x) + self.rect_.w > self.rect_.x and \
                (samson.rect_.y) < self.rect_.y + self.rect_.h and \
                (samson.rect_.h) + samson.rect_.y > self.rect_.y:
                hit_samson = True
        else:
            hit_samson = True
        if hit_samson:
            # if the rectangles collide, samson is hurt
            samson.take_damage(1)
            

class SniperPhilistine(Philistine):
    def __init__(self, images, W=1200, H=680):
        Philistine.__init__(self, images, W, H, 10)
        self.frame = 0
        self.points = 10
        self.weapon = Sniper()
        

    def move_towards_samson(self, samson):
        hit_samson = False
        vector = pygame.math.Vector2((samson.rect_.x + 25) - self.rect_.x,
                                     (samson.rect_.y + 20) - self.rect_.y)
        if vector.length() >= 600:
            self.direction = 0
            self.frame = 0
            vector.normalize()
            vector.scale_to_length(self.dx)
            self.rect_.move_ip(vector)
            
            if  (samson.rect_.x+25) < self.rect_.x + self.rect_.w and \
                (samson.rect_.x+25) + samson.rect_.w > self.rect_.x and \
                (samson.rect_.y+20) < self.rect_.y + self.rect_.h and \
                (samson.rect_.h-10) + samson.rect_.y > self.rect_.y:
                hit_samson = True
        else:
            self.direction = 1
            self.frame += 1
            if  (samson.rect_.x+25) < self.rect_.x + self.rect_.w and \
                (samson.rect_.x+25) + samson.rect_.w > self.rect_.x and \
                (samson.rect_.y+20) < self.rect_.y + self.rect_.h and \
                (samson.rect_.h-10) + samson.rect_.y > self.rect_.y:
                hit_samson = True
            if self.frame % 60 == 0:
                self.fire_weapon(samson.rect_.x+20, samson.rect_.y+20)
        if hit_samson:
            samson.take_damage(10)
            

    def fire_weapon(self, t_x=1200, t_y=340, speed=10, d=25):
        self.weapon.create_bullet(self.rect_.x, self.rect_.y, t_x, t_y, speed, d)

    def update(self, screen, samson):
        #samson.rect_.x -= 10
        #samson.rect_.y -= 10
        self.weapon.bullet_collision([samson], self.weapon.damage)
        self.weapon.update_bullets(screen, self.W, self.H)
        #samson.rect_.x += 10
        #samson.rect_.y += 10
