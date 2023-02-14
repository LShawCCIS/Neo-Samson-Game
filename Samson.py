import pygame
from Weapons import *

pygame.mixer.quit()
pygame.mixer.init(44100, -16, 2, 32)
pygame.init()


class Samson:
    death_sounds = []
    for i in range(4):
        dsound = pygame.mixer.Sound(f"sounds/Samson/Samson_Death_{i + 1}.wav")
        death_sounds.append(dsound)
    def __init__(self, images, W=1200, H=680):
        self.image = pygame.image.load(images[0][0]) # get starting rect
        self.samson_images = images # 2D List
        self.rect_ = self.image.get_rect() # our samson rect
        self.rect_.x = W / 2
        self.rect_.y = H / 2
        self.dx = 2.0
        self.dy = 2.0
        self.H = H
        self.W = W
        self.direction = 0
        self.animation = 0
        self.animation_speed = 0.1
        self.target_health = 500
        self.current_health = 500
        self.maximum_health = 500
        self.health_bar_length = 200
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.health_bar_speed = 2
        self.weapon = Pistol()
        self.score = 0

    def reset_samson(self):
        self.rect_.x = self.W / 2
        self.rect_.y = self.H / 2
        self.score = 0
        self.target_health = self.maximum_health
        self.current_health = self.target_health

    def move_up(self):
        # moves samson up
        self.rect_ = self.rect_.move(0, self.dy * -1)
        if self.rect_.top < 0:
            self.rect_.y = 0
        self.animation += self.animation_speed
        if self.animation >= len(self.samson_images[self.direction]):
            self.animation = 0
        self.change_image()

    def move_down(self):
        # moves samson down
        self.rect_ = self.rect_.move(0, self.dy)
        if self.rect_.bottom > self.H:
            self.rect_.y = self.H - self.rect_.h
        self.animation += self.animation_speed
        if self.animation >= len(self.samson_images[self.direction]):
            self.animation = 0
        self.change_image()

    def move_left(self):
        # moves samson left
        self.direction = 1
        self.rect_ = self.rect_.move(self.dx * -1, 0)
        if self.rect_.left < 0:
            self.rect_.x = 0
        self.animation += self.animation_speed
        if self.animation >= len(self.samson_images[self.direction]):
            self.animation = 0
        self.change_image()

    def move_right(self):
        # moves samson right
        self.direction = 0
        self.rect_ = self.rect_.move(self.dx, 0)
        if self.rect_.left > self.W - self.rect_.w:
            self.rect_.x = self.W - self.rect_.w
        self.animation += self.animation_speed
        if self.animation >= len(self.samson_images[self.direction]):
            self.animation = 0
        self.change_image()

    def reset(self):
        # If we stop holding a direction, we need to be at the normal standing
        # pose
        self.image = pygame.image.load(self.samson_images[self.direction][0])

    def change_image(self):
        # this will flip image to the next in whichever array we are using
        self.image = \
            pygame.image.load(self.samson_images[self.direction][int(self.animation)])

    def take_damage(self, amount):
        self.target_health -= amount
        if self.target_health <= 0:
            self.target_health = 0

    def get_healing(self, amount):
        self.target_health += amount
        if self.target_health >= self.maximum_health:
            self.target_health = self.maximum_health
            

    def update(self, screen, army):
        # update our health bar
        self.health_bar(screen)
        # now check for bullet collisions
        score = self.weapon.bullet_collision(army, self.weapon.damage)
        self.score += score
        # now update bullets
        self.weapon.update_bullets(screen, self.W, self.H)

    def health_bar(self, screen):
        # this displays our health bar in the left corner
        # it draws 3 rectangles, one is an outline, the other 2 are
        # full bars. One is underneath the other to give that slow
        # decrement illusion
        t_width = 0
        t_color = (255,0,0)
        if self.current_health < self.target_health:
            self.current_health += self.health_bar_speed
            t_width = int((self.target_health - self.current_health)\
                          / self.health_ratio)
            t_color = (0,255,0)
        if self.current_health >= self.target_health:
            self.current_health -= self.health_bar_speed
            t_width = int((self.target_health - self.current_health)\
                          / self.health_ratio)
            t_color = (255,165,0)

        health_bar = pygame.Rect(10,10,self.current_health / self.health_ratio,\
                                 25)

        t_bar = pygame.Rect(health_bar.right,10, t_width, 25)
        pygame.draw.rect(screen, (255,0,0), health_bar)
        pygame.draw.rect(screen, t_color, t_bar)
        pygame.draw.rect(screen, (255,255,255), (10, 10, \
                          self.health_bar_length, 25),4)

    # we have attempted to fire our weapon
    # t_x = targetx, t_y = targety (this is our mouse position on click)
    def fire_weapon(self, t_x=1200, t_y=340, screen=None):
        fired = self.weapon.create_bullet(self.rect_.x, self.rect_.y, t_x, t_y)
        #if fired:
            #self.fire_animation(screen)
            #n = random.randint(0, 3)
            #Samson.death_sounds[n].play()
        return fired
        # do our animaitons
        #if fired:
        #    print("SHOTS:")
        #    self.fire_animation(screen)

    def fire_animation(self, screen, clock):
        if self.direction == 0:
            while self.animation < len(self.samson_images[2]):
                self.image = pygame.image.load\
                    (self.samson_images[2][int(self.animation)])
                screen.blit(self.image, self.rect_)
                self.animation += 0.3
                pygame.display.update()
            self.animation = 0
            self.reset()
            
        elif self.direction == 1:
            while self.animation < len(self.samson_images[3]):
                self.image = pygame.image.load\
                    (self.samson_images[3][int(self.animation)])
                screen.blit(self.image, self.rect_)
                self.animation += 0.3
                pygame.display.update()
            self.animation = 0
            self.reset()

        
    def play_death(self):
        sound = random.randint(0, len(Samson.death_sounds) - 1)
        Samson.death_sounds[sound].play()
        
        
        
