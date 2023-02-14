
from Bullet import *

class Weapon:
    def __init__(self, fire_rate):
        # fire_rate = amount of bullets allowed on the screen
        self.fire_rate = fire_rate
        # fired_bullets = array of live bullets
        self.fired_bullets = []

    def bullet_collision(self, enemies, damage):
        # look at our bullets and enemies and see if they collide. If they do
        # our bullet dies and the enemy takes damage
        t_score = 0
        for enemy in enemies:
            for bullet in self.fired_bullets:
                if  enemy.rect_.x <= bullet.rect_.x + bullet.rect_.w and \
                    enemy.rect_.x + enemy.rect_.w >= bullet.rect_.x and \
                    enemy.rect_.y <= bullet.rect_.y + bullet.rect_.h and \
                    enemy.rect_.h + enemy.rect_.y >= bullet.rect_.y:
                    enemy.take_damage(damage)
                    bullet.is_alive = False
                    if enemy.target_health <= 0:
                        if isinstance(enemy, MeleePhilistine) or \
                           isinstance(enemy, SniperPhilistine):
                            t_score += enemy.points
                        enemy.play_death()
                        enemies.remove(enemy)

                        break
        return t_score       

    def update_bullets(self, screen, W, H):
        # this function will take our array of bullets and update their
        # positions if they are alive. If they aren't alive, we delete them!
        for bullet in self.fired_bullets:
            if bullet.is_alive:
                bullet.move_bullet()
            elif not bullet.is_alive:
                self.fired_bullets.remove(bullet)
            if bullet.rect_.x < 0 or bullet.rect_.x > W + bullet.rect_.w:
                self.fired_bullets.remove(bullet)
            elif bullet.rect_.y < 0 - bullet.rect_.h \
               or bullet.rect_.y > H + bullet.rect_.h:
                self.fired_bullets.remove(bullet)

        self.draw_bullets(screen)

    def draw_bullets(self, screen):
        # draw each alive bullet in our array
        for bullet in self.fired_bullets:
            if bullet.is_alive:
                screen.blit(bullet.image, bullet.rect_)

class Pistol(Weapon):
    # first weapon type, pistol will be the weakest
    def __init__(self):
        Weapon.__init__(self, 100)
        self.damage = 5

    def create_bullet(self, x, y, t_x=1200, t_y=340):
        # When we get here that means space/mousebutton was pressed. We create
        # bullets as long as we don't exceed our fire rate.
        if len(self.fired_bullets) < self.fire_rate:
            bullet = PistolBullet("sprites/Bullets/Pistol_Bullet.png", \
                                  x+20, y+20, t_x ,t_y)
            self.fired_bullets.append(bullet)
            return True
        return False


class Sniper(Weapon):
    # enemies use this weapon. They snipe... watch out
    def __init__(self):
        Weapon.__init__(self, 100)
        self.damage = 20

    def create_bullet(self, x, y, t_x=1200, t_y=340, speed=15, damage=10):
        # we get here when a Sniper enemy is in range of Samson
        if len(self.fired_bullets) < self.fire_rate:
            bullet = SniperBullet("sprites/Bullets/Sniper_Bullet.png", \
                                  x+50, y+20, t_x ,t_y, speed, damage)
            self.fired_bullets.append(bullet)

from Philistine import *

# TODO: Add more weapons
        
