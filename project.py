import pygame, sys
import random
import os.path
from pygame.key import *
from Samson import *
from Philistine import *
from Button import *
#from pygame import mixer

pygame.mixer.quit()
pygame.mixer.init(44100, -16, 2, 32)
pygame.init()


# first if our score files don't exist in this system, create them!
file_exists = os.path.exists('scores.txt')
if not file_exists:
    file = open('scores.txt', 'w')
    file.write(str(0) + '\n')
    file.close()

file_exists = os.path.exists('score_names.txt')
if not file_exists:
    file = open('score_names.txt', 'w')
    file.write('NAN\n')
    file.close()
    
def get_sprites(direc_, name, f_type, length):
    # this function takes a directory path, a common file name
    # the file type, and the amount of files
    # i.e. it assumes your files are numbered EX: "animation1png"
    # if combines the strings together and generates all your images
    # and returns a list of them
    images_list = []
    image_num = 1
    for i in range(length):
        images_list.append(direc_ + name + str(image_num) + f_type)
        image_num += 1
    return images_list

# These are all of the variables for our Game Loop
# our animation for dying
you_died = get_sprites("sprites/DeathAnimations/", "YouDied", ".png", 12)
you_died_index = 0

W, H = 1200, 680
screen = pygame.display.set_mode((W, H))
running  = True
black = 0, 0, 0
score_font = pygame.font.Font('freesansbold.ttf',32)
s_font_x = 10
s_font_y = 640
wave_font = pygame.font.Font('freesansbold.ttf',32)
w_font_x = W  - 200
w_font_y = 10

samson_images = []
# Index 0 is our right animation
xs = get_sprites("sprites/SamsonImages/", "Right_Samson", ".png", 7)
samson_images.append(xs)
# Index 1 is our left animation
xs = get_sprites("sprites/SamsonImages/", "Left_Samson", ".png", 7)
samson_images.append(xs)
# Index 2 is our right fire animation
xs = get_sprites("sprites/SamsonImages/", "Right_Fire_Samson", ".png", 3)
samson_images.append(xs)
# Index 3 is our Left fire animation
xs = get_sprites("sprites/SamsonImages/", "Left_Fire_Samson", ".png", 3)
samson_images.append(xs)

samson = Samson(samson_images, W, H)

philistine_army = []

# our philistine unit images
melee_images = [get_sprites("sprites/PhilistineAnimation/",\
                    "MeleePhilistine", ".png", 4)]
sniper_images = [get_sprites("sprites/PhilistineAnimation/",\
                    "SniperPhilistine", ".png", 4)]
sniper_images.append(["sprites/PhilistineAnimation/SniperPhilistinePrep.png"])

# Buttons for our Main Menu
button = pygame.image.load("sprites/Misc./Button.png")
play_button = pygame.transform.scale(button, (200,50))
pbutton = Button(play_button, W / 2, H - 300, "PLAY", screen)

qbutton = Button(play_button, W / 2, H - 100, "QUIT", screen)

#help_button = pygame.image.load("sprites/Misc./Button.png")
#help_button = pygame.transform.scale(help_button, (200,100))
hbutton = Button(play_button, W / 2, H - 200, "HELP", screen)

#score_button = pygame.image.load("sprites/Misc./Button.png")
#score_button = pygame.transform.scale(play_button, (200,100))
sbutton = Button(play_button, W / 2, H - 15, "SCORES", screen)


background = pygame.image.load("sprites/BackGrounds/BackGround.jpg")
main_menu_images = get_sprites("sprites/BackGrounds/", "MainMenu", ".png", 8)
clock = pygame.time.Clock()

wave_number = 0
enemy_count = 5
new_wave = (False, 0)
samson_fire = False
start, samson_died = True, False
##############################################################################
##############################################################################
##############################################################################

# These are our Game Loop Helper Functions

# generate army gets our sprites as well as creates our list of enemies.
# Melee has 1 animation
# Snipers have 2
# The different indexes relate to the specific animations
def generate_army(army_list, num_units):    
    for i in range(num_units):
        decide = random.randint(0,10)
        if decide != 10:
            p = MeleePhilistine(melee_images, W, H)
        else:
            p = SniperPhilistine(sniper_images, W, H)
        army_list.append(p)
    return army_list

# this function will trigger if a new highscore/top 5 score occurred.
def display_newRecord(new_highscore=False):
    record_menu = pygame.image.load("sprites/BackGrounds/StaticMenu.png")
    finish_font = pygame.font.SysFont('microsoftjhengheimicrosoftjhengheiuibold', 75)
    enter_name = finish_font.render('Please Enter a 3 Letter Name Into The Console', False, (255, 255, 255))
    beat_high = finish_font.render('Great Job! You Made A New Top Score!', False, (140, 33, 85))
    if new_highscore:
        beat_high = finish_font.render('HUZZAH! YOU BEAT THE HIGHSCORE!', False, (140, 33, 85))
    going = True
    name = ""
    screen.blit(record_menu, (0, 0))
    screen.blit(beat_high, (50, 100))
    screen.blit(enter_name, (25, 300))
    pygame.display.update()
    name = input()
    while len(name) != 3:
        name = input()
    return name
    
# this records our score if we made it into the top 5
def record_score():
    store_score = samson.score
    file_open = open('scores.txt', 'r')
    score_r = file_open.readlines()
    file_open.close()
    file_open = open('score_names.txt', 'r')
    name_r = file_open.readlines()
    file_open.close()
    better_score = False
    for i in range(len(score_r)):
        if store_score > int(score_r[i]) and not better_score:
            old_name = name_r[i]
            old_score = score_r[i]
            score_r[i] = str(store_score) + '\n'
            if i == 0:
                name = display_newRecord(True)
            else:
                name = display_newRecord()
            name_r[i] = name + '\n'
            better_score = True
        elif better_score:
            t = score_r[i]
            score_r[i] = old_score
            old_score = t
            t = name_r[i]
            name_r[i] = old_name
            old_name = t
        if i + 1 == len(score_r) and i < 4:
            score_r.append(str(old_score))
            name_r.append(str(old_name))
            break
    with open('scores.txt', 'w') as file:
        file.writelines(score_r)
    with open('score_names.txt', 'w') as file:
        file.writelines(name_r)  
# this displays our current score
def render_score(x, y, score):
    score = score_font.render("Score: " + str(score), True, (255,255,255))
    screen.blit(score, (x, y))
    
# this is our menu that displays scores
def display_scores(from_Menu=False):
    title_font = pygame.font.SysFont('microsoftjhengheimicrosoftjhengheiuibold', 75)
    score_font = pygame.font.SysFont('microsoftjhengheimicrosoftjhengheiuibold', 50)
    score_surface = title_font.render('TOP SCORES:', False, (140, 33, 85))
    ebutton = Button(play_button, W / 2, H - 50, "EXIT", screen)
    scores_menu = pygame.image.load("sprites/BackGrounds/StaticMenu.png")
    going = True
    scores_open = open('scores.txt', 'r')
    scores = scores_open.readlines()
    scores_open.close()
    names_open = open('score_names.txt', 'r')
    names = names_open.readlines()
    names_open.close()
    # see if we got a new highscore
    for i in range(len(scores)):
        if samson.score > int(scores[i]) or (len(scores) < 5 and not from_Menu):
            # if we did, record it and get the new file
           record_score()
           scores_open = open('scores.txt', 'r')
           scores = scores_open.readlines()
           scores_open.close()
           names_open = open('score_names.txt', 'r')
           names = names_open.readlines()
           names_open.close()
           break
    while going:
        screen.fill(black)
        score_list = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                x,y = pygame.mouse.get_pos()
                clicked_ebutton = ebutton.checkForInput((x,y))
                if clicked_ebutton:
                    going = False
        for i in range(len(scores)):
            score_list.append(score_font.render(names[i][:-1] + "    " + scores[i][:-1], False, (255, 255, 255)))
        screen.blit(scores_menu, (0, 0))
        ebutton.change_color(pygame.mouse.get_pos())
        ebutton.update()
        screen.blit(score_surface, (W / 2 - 175, 50))
        i = 150
        for score in score_list:
            screen.blit(score, (W / 2 - 100, i))
            i += 100
        pygame.display.update()
    
# this displays our wave counter
def render_wave(x, y, wave_num):
    wave = wave_font.render("Wave: " + str(wave_num), True, (255,255,255))
    screen.blit(wave, (x, y))

# this displays our main menu
def main_menu():
    m_m = True
    m_m_index = 0
    high_score = open('scores.txt', 'r')
    file = high_score.readlines()
    last = int(file[0][:-1])
    high_score.close()
    high_name = open('score_names.txt', 'r')
    file = high_name.readlines()
    name = file[0][:-1]

    high_score = pygame.font.SysFont('arial', 25)
    h_text  = high_score.render('HighScore:', False, (140, 33, 65))
    name_text = high_score.render(name + "    " + str(last), False, (255,255,255))
    
    while m_m:
        if m_m_index >= len(main_menu_images) - 1:
            m_m_index = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:# and event.button == 1:
                x,y = pygame.mouse.get_pos()
                clicked_pbutton = pbutton.checkForInput((x,y))
                if clicked_pbutton:
                    m_m = False
                else:
                    clicked_qbutton = qbutton.checkForInput((x,y))
                    if clicked_qbutton:
                        pygame.quit()
                        sys.exit()
                    else:
                        clicked_hbutton = hbutton.checkForInput((x,y))
                        if clicked_hbutton:
                            display_help()
                        else:
                            clicked_sbutton = sbutton.checkForInput((x,y))
                            if clicked_sbutton:
                                display_scores(True)

        main_menu_image = pygame.image.load(main_menu_images[int(m_m_index)])
        screen.blit(main_menu_image, (0, 0))
        pbutton.update()
        pbutton.change_color(pygame.mouse.get_pos())
        qbutton.update()
        qbutton.change_color(pygame.mouse.get_pos())
        hbutton.update()
        hbutton.change_color(pygame.mouse.get_pos())
        sbutton.update()
        sbutton.change_color(pygame.mouse.get_pos())
        screen.blit(h_text, (800,640))
        screen.blit(name_text, (930,640))
        pygame.display.update()
        m_m_index += 0.3

# Displays our help menu
def display_help():
    #exit_button = pygame.image.load("sprites/Misc./Button.png")
    #exit_button = pygame.transform.scale(play_button, (200,100))
    ebutton = Button(play_button, W / 2, H - 100, "EXIT", screen)
    
    welcome = pygame.font.SysFont('microsoftjhengheimicrosoftjhengheiuibold', 50)
    welcome_surface = welcome.render('Welcome To NEO-SAMSON!', False, (140, 33, 85))

    movement = pygame.font.SysFont('arial', 50)
    movement_surface = movement.render('Use W-A-S-D To Move', False, (255, 255, 255))

    weapon = pygame.font.SysFont('arial', 50)
    weapon_surface = weapon.render('Left-Click With Mouse To Fire', False, (255, 255, 255))

    points = pygame.font.SysFont('arial', 50)
    points_surface = points.render('Kill Enemies To Get Points', False, (255, 255, 255))

    death = pygame.font.SysFont('arial', 50)
    death_surface = points.render('''Don't Die''', False, (255, 255, 255))

    
    
    help_menu = pygame.image.load("sprites/BackGrounds/StaticMenu.png")
    going = True
    while going:
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                x,y = pygame.mouse.get_pos()
                clicked_ebutton = ebutton.checkForInput((x,y))
                if clicked_ebutton:
                    going = False
        screen.blit(help_menu, (0, 0))
        ebutton.update()
        ebutton.change_color(pygame.mouse.get_pos())
        screen.blit(welcome_surface, (275,0))
        screen.blit(movement_surface, (275,100))
        screen.blit(weapon_surface, (275,200))
        screen.blit(points_surface, (275,300))
        screen.blit(death_surface, (275,400))
        pygame.display.update()

# displays when we die
def display_death():
    pygame.transform.scale(play_button, (400,150))
    image = 1
    you_died_index = 0
    death = pygame.image.load(you_died[int(you_died_index)])
    death = pygame.transform.scale(death, (500, 500))
    death_rect = death.get_rect(center=(W / 2, H / 2 - 50))
    while you_died_index < len(you_died) - 1:
        you_died_index += 0.1
        death = pygame.image.load(you_died[int(you_died_index)])
        death = pygame.transform.scale(death, (500,500))
        screen.blit(background, (0,0))
        screen.blit(death, death_rect)
        pygame.display.update()

    count = 0
    while count < 60000:
        count += 1
##############################################################################
##############################################################################
##############################################################################

# This Is our Game Loop
while running:
    screen.fill(black)
    fired_weapon = False
    # here we have our main menu! we call our main menu function
    if start or samson_died:
        # here we need to reset everything back to normal incase we are back
        # to the menu because samson died.
        if start:
            main_menu()
            start = False
        if samson_died:
            philistine_army = []
            enemy_count = 5
            wave_number = 0
            start = False
            samson_died = False
            display_death()
            display_scores()
            samson.reset_samson()
            main_menu()
        
    # this is our wave system, once all of our guys die, send MORE!!!
    if len(philistine_army) == 0:
        wave_number += 1
        generate_army(philistine_army, int(enemy_count))
        enemy_count = (enemy_count * 1.2) + wave_number // 10
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
           pygame.quit()
           sys.exit()
        if event.type == pygame.KEYUP:
             samson.reset()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            samson_fire = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            samson_fire = False

    if samson_fire:
        x,y = pygame.mouse.get_pos()
        fired_weapon = samson.fire_weapon(x, y, screen)

    keys = pygame.key.get_pressed()  #checking pressed keys

    # These are the movement keys for Samson. 
    if keys[pygame.K_w]:
        samson.move_up()
    if keys[pygame.K_s]:
        samson.move_down()
    if keys[pygame.K_a]:
        samson.move_left()
    if keys[pygame.K_d]:
        samson.move_right()
    if keys[pygame.K_e]:
        samson.get_healing(100)
    if keys[pygame.K_SPACE]:
        x,y = pygame.mouse.get_pos()
        fired_weapon = samson.fire_weapon(x, y, screen)

    if samson.target_health <= 0:
        samson_died = True
        samson.play_death()
        
    for i in range(len(philistine_army)):
        philistine_army[i].move_towards_samson(samson)
    
    # put verything onto the screen
    screen.blit(background, (0, 0))
    screen.blit(samson.image, samson.rect_)
    # if we have a SnipterPhilistine, we need to update their bullets
    for i in range(len(philistine_army)):
        if isinstance(philistine_army[i], SniperPhilistine):
            philistine_army[i].update(screen, samson)
        philistine_army[i].animate()
        screen.blit(philistine_army[i].image, philistine_army[i].rect_)
    samson.update(screen, philistine_army)
    render_score(s_font_x, s_font_y, samson.score)
    render_wave(w_font_x, w_font_y, wave_number)
    # if we fired a bullet, play our animation
    if fired_weapon:
        samson.fire_animation(screen, clock)
        

    # display all updates and set frame rate
    pygame.display.update()
    clock.tick(60)
##############################################################################
##############################################################################
##############################################################################
