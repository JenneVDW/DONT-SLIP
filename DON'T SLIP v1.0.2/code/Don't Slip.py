import os
import sys
import pygame
import time
import random
from pynput import keyboard

groen = (0, 100, 50)
zwart = (0, 0, 0)
grijs = (50, 50, 50)
wit = (255, 255, 255)
vel_a = 0
vel_b = 2
stored_vel_a = 0
stored_vel_b = 0
name = "Local Save"

if getattr(sys, 'frozen', False):                                   # aanmaak saves folder
    base_path = os.path.dirname(os.path.abspath(sys.executable))
else:
    base_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(base_path, "game_files"))
saves_dir = os.path.join(base_path, "game_files", "saves")
os.makedirs(saves_dir, exist_ok=True)
delete_old_saves = False           
all_scores = []

pygame.init()                                           # opstart van pygame
scherm = pygame.display.set_mode((800, 600))
pygame.display.set_caption("DON'T SLIP! v1.0.1")
font = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 35)
running = True
startscherm = True
gamerunning = False
gamepaused = False

name_display = pygame.Rect(50, 25, 700, 50)           # opmaak naam input
name_input = pygame.Rect(175, 100, 450, 50)
name_being_input = False

startknop = pygame.Rect(300, 425, 200, 100)            # opmaak van startknop

img_character = pygame.image.load(os.path.join("textures", "Character1.png"))     # opmaak van character
img_character_turning_left = pygame.image.load(os.path.join("textures", "Character_turning_left.png"))
img_character_turning_right = pygame.transform.flip(img_character_turning_left, 1, False)
character = img_character.get_rect()
character.y = 425

img_banaan = pygame.image.load(os.path.join("textures", "Banana.png"))            # opmaak van banaan
banaan_variant_1 = pygame.transform.rotate(pygame.transform.flip(img_banaan, random.randint(0, 1), False), random.randint(-15,15))
banaan_variant_2 = pygame.transform.rotate(pygame.transform.flip(img_banaan, random.randint(0, 1), False), random.randint(-15,15))
banaan_1 = img_banaan.get_rect()
banaan_2 = img_banaan.get_rect()

img_rat = pygame.image.load(os.path.join("textures", "Rat1.png"))                     # opmaak van rat
rat = img_rat.get_rect()

scorecounter = pygame.Rect(0, 550, 250, 50)                # opmaak score teller

stagecounter = pygame.Rect(250, 550, 200, 50)           # opmaak stage teller

highscorecounter = pygame.Rect(450, 550, 350, 50)       # opmaak highscore teller

possibilitychecker = pygame.Rect(0, -300, 800, 250)     # opmaak possibility checker

leaderboard = pygame.Rect(150, 175, 500, 225)
leaderboard_text = pygame.Rect(150, 175, 500, 50)
leaderboard_1 = pygame.Rect(150, 250, 500, 50)          # opmaak van leaderboard
leaderboard_2 = pygame.Rect(150, 300, 500, 50)
leaderboard_3 = pygame.Rect(150, 350, 500, 50)

gamepauseddisplay = pygame.Rect(0, 0, 300, 50)

while running:

    if startscherm:

        scherm.fill(groen)

        pygame.draw.rect(scherm, zwart, name_display)                   # aanmaken naam display
        text = font.render(f"Save File: {name}", True, wit)
        text_rect = text.get_rect(center=name_display.center)
        scherm.blit(text, text_rect)

        pygame.draw.rect(scherm, zwart, name_input)                    # aanmaken naam input knop
        if name_being_input == False:
            text = font.render("Click to enter new name", True, wit)
        else:
            text = font.render("Click again to confirm", True, wit)
            pygame.draw.rect(scherm, grijs, name_input)
        text_rect = text.get_rect(center=name_input.center)
        scherm.blit(text, text_rect)

        if name_being_input == False:
            try:                                                                # get previous highscore
                with open(os.path.join(saves_dir, f"{name}.txt"), "r") as file:
                    highscore = int(file.read())
            except FileNotFoundError:
                highscore = 0
                with open(os.path.join(saves_dir, f"{name}.txt"), "w") as file:
                    file.write("0")

        pygame.draw.rect(scherm, zwart, leaderboard)                        # aanmaak leaderboard
        all_scores = []
        for x in os.listdir(saves_dir):
            with open(os.path.join(saves_dir, x), "r") as file:
                if x.startswith("."):
                    all_scores.append(("-", int(file.read())))
                else:
                    all_scores.append((os.path.splitext(x)[0], int(file.read())))
            all_scores.sort(key = lambda y: y[1], reverse = True)
        pygame.draw.rect(scherm, zwart, leaderboard_text)               # leaderboard text
        text = font.render("Local Leaderboard", True, wit)
        text_rect = text.get_rect(center=leaderboard_text.center)
        scherm.blit(text, text_rect)
        pygame.draw.rect(scherm, zwart, leaderboard_1)                  # number 1
        x, y = all_scores[0]
        text = font_small.render(f"1. {x}: {y}", True, wit)
        text_rect = text.get_rect(center=leaderboard_1.center)
        scherm.blit(text, text_rect)
        pygame.draw.rect(scherm, zwart, leaderboard_2)                  # number 2
        if len(all_scores) > 1:
            x, y = all_scores[1]
            text = font_small.render(f"2. {x}: {y}", True, wit)
            text_rect = text.get_rect(center=leaderboard_2.center)
            scherm.blit(text, text_rect)
        pygame.draw.rect(scherm, zwart, leaderboard_3)                  # number 3
        if len(all_scores) > 2:
            x, y = all_scores[2]
            text = font_small.render(f"3. {x}: {y}", True, wit)
            text_rect = text.get_rect(center=leaderboard_3.center)
            scherm.blit(text, text_rect)

        pygame.draw.rect(scherm, zwart, startknop)                      # aanmaken startknop
        text = font.render("Start", True, wit)
        text_rect = text.get_rect(center=startknop.center)
        scherm.blit(text, text_rect)

        pygame.draw.rect(scherm, zwart, highscorecounter)               # aanmaken highscorecounter
        if highscore < 1000000:
            text = font.render(f"Highscore: {highscore}", True, wit)
            text_rect = text.get_rect(center=highscorecounter.center)
            scherm.blit(text, text_rect)
        else:
            text = font.render("Cheating huh?", True, wit)
            text_rect = text.get_rect(center=highscorecounter.center)
            scherm.blit(text, text_rect)

    if gamerunning:

        scherm.fill(groen)

        character.x += vel_a                                            # aanmaken character
        if character.x in [150, 350, 550]:
            vel_a = 0
            blit_character = scherm.blit(img_character, character)
            character_frame += 1                                        # animatie van character
            if character_frame == 24:
                character_frame = 0
            if character_frame == 0:
                img_character = pygame.image.load(os.path.join("textures", "Character1.png"))
            if character_frame == 6:
                img_character = pygame.image.load(os.path.join("textures", "Character2.png"))
            if character_frame == 12:
                img_character = pygame.image.load(os.path.join("textures", "Character1.png"))
            if character_frame == 18:
                img_character = pygame.image.load(os.path.join("textures", "Character3.png"))
        if vel_a < 0:
            blit_character = scherm.blit(img_character_turning_left, character)
        if vel_a > 0:
            blit_character = scherm.blit(img_character_turning_right, character)

        if score < 10:                                                  # stage criteria
            stage = 1
            speed = 1
        elif score < 50:
            stage = 2
            speed = 2
        elif score < 100:
            stage = 3
        elif score < 150:
            stage = 4
        elif score < 200:
            stage = 5
            speed = 3
        elif score < 250:
            stage = 6
        elif score < 300:
            stage = 7
        elif score < 350:
            stage = 8
        elif score < 400:
            stage = 9
        elif score < 500:
            stage = 10

        blit_banaan = scherm.blit(banaan_variant_1, banaan_1)           # aanmaak banaan 1
        banaan_1.y += vel_b + speed*vel_b
        if banaan_1.y > 600:
            banaan_1.y = random.randint(-300, -50)
            banaan_1.x = random.choice([175, 375, 575])
            banaan_variant_1 = pygame.transform.rotate(pygame.transform.flip(img_banaan, random.randint(0, 1), False), random.randint(-15,15))
            score += 1
        if stage > 2:                                                   # aanmaak banaan 2
            blit_banaan = scherm.blit(banaan_variant_2, banaan_2)
            banaan_2.y += vel_b + speed*vel_b
            if banaan_2.y > 600:
                banaan_2.y = random.randint(-300, -50)
                banaan_2.x = random.choice([175, 375, 575])
                banaan_variant_2 = pygame.transform.rotate(pygame.transform.flip(img_banaan, random.randint(0, 1), False), random.randint(-15,15))
                score += 1

        if stage > 3:                                                   # aanmaak rat
            blit_rat = scherm.blit(img_rat, rat)
            rat_frame += 1                                              # animatie rat
            if rat_frame == 18:
                rat_frame = 0
            if rat_frame == 0:
                img_rat = pygame.image.load(os.path.join("textures", "Rat1.png"))
            if rat_frame == 6:
                img_rat = pygame.image.load(os.path.join("textures", "Rat2.png"))
            if rat_frame == 12:
                img_rat = pygame.image.load(os.path.join("textures", "Rat3.png"))
            rat.y += (vel_b + speed*vel_b + 1)
            if gamepaused:
                rat.y -= 1
            if rat.y > 600:
                rat.y = random.randint(-1000, -50)
                rat.x = random.choice([175, 375, 575])
                score += 2

        if banaan_1.x != banaan_2.x and rat.x != banaan_1.x and rat.x != banaan_2.x:                                                        # possibility checker runnen
            if possibilitychecker.colliderect(rat) or possibilitychecker.colliderect(banaan_1) or possibilitychecker.colliderect(banaan_2):
                if sum(x < 200 for x in [abs(rat.y - banaan_1.y), abs(rat.y - banaan_2.y), abs(banaan_1.y - banaan_2.y)]) > 1:
                    if banaan_1.y == min(rat.y, banaan_1.y, banaan_2.y):
                        banaan_1.y = random.randint(-300, -50)
                        banaan_1.x = random.choice([175, 375, 575])
                    elif banaan_2.y == min(rat.y, banaan_1.y, banaan_2.y):
                        banaan_2.y = random.randint(-300, -50)
                        banaan_2.x = random.choice([175, 375, 575])
                    else:
                        rat.y = random.randint(-1000, -50)
                        rat.x = random.choice([175, 375, 575])

        pygame.draw.rect(scherm, zwart, scorecounter)                     # aanmaak scorecounter
        if score < 1000000:
            text = font.render(f"Score: {score}", True, wit)
            text_rect = text.get_rect(center=scorecounter.center)
            scherm.blit(text, text_rect)
        else:
            text = font.render("Cheating huh?", True, wit)
            text_rect = text.get_rect(center=scorecounter.center)
            scherm.blit(text, text_rect)

        pygame.draw.rect(scherm, zwart, stagecounter)                   # aanmaak stagecounter
        text = font.render(f"Stage: {stage}", True, wit)
        text_rect = text.get_rect(center=stagecounter.center)
        scherm.blit(text, text_rect)

        pygame.draw.rect(scherm, zwart, highscorecounter)               # aanmaak highscorecounter
        if highscore < 1000000:
            text = font.render(f"Highscore: {highscore}", True, wit)
            text_rect = text.get_rect(center=highscorecounter.center)
            scherm.blit(text, text_rect)
        else:
            text = font.render("Cheating huh?", True, wit)
            text_rect = text.get_rect(center=highscorecounter.center)
            scherm.blit(text, text_rect)

        if score > highscore:                                           #highscore saver
            highscore = score
            with open(os.path.join(saves_dir, f"{name}.txt"), "w") as file:
                file.write(str(highscore))

        if character.colliderect(banaan_1):                             # collisionchecks
            startscherm = True
            gamerunning = False
        if character.colliderect(banaan_2):
            startscherm = True
            gamerunning = False
        if character.colliderect(rat):
            startscherm = True
            gamerunning = False

    if gamepaused:

        pygame.draw.rect(scherm, zwart, gamepauseddisplay)                   # game paused text
        text = font.render("Game Paused", True, wit)
        text_rect = text.get_rect(center=gamepauseddisplay.center)
        scherm.blit(text, text_rect)

        if stored_vel_a < 0:
            blit_character = scherm.blit(img_character_turning_left, character)
        if stored_vel_a > 0:
            blit_character = scherm.blit(img_character_turning_right, character)
        else:
            img_character = pygame.image.load(os.path.join("textures", "Character1.png"))

        img_rat = pygame.image.load(os.path.join("textures", "rat1.png"))


    for event in pygame.event.get():

        if startscherm:

            if event.type == pygame.MOUSEBUTTONDOWN:                 # acties aan start van game
                if startknop.collidepoint(event.pos):
                    startscherm = False
                    gamerunning = True
                    score = 100                         # OP 0 ZETTEN VOOR ECHTE RELEASE
                    speed = 2                           # DELETE DEZE LIJN VOOR ECHTE RELEASE
                    vel_a = 0
                    vel_b = 2
                    character.x = 350
                    character_frame = 0
                    banaan_1.y = 0
                    banaan_1.x = random.choice([175, 375, 575])
                    banaan_2.y = random.randint(-300, -50)
                    banaan_2.x = random.choice([175, 375, 575])
                    rat.y = random.randint(-1000, -50)
                    rat.x = random.choice([175, 375, 575])
                    rat_frame = 0

                if name_input.collidepoint(event.pos):              # naam input knop press check
                    if name_being_input == False:
                        name = ""
                    else:
                        for x in os.listdir(saves_dir):                           # delete save files with highscore 0
                            with open(os.path.join(saves_dir, x), "r") as file:
                                if int(file.read()) == 0:
                                    delete_old_saves = True
                                else:
                                    delete_old_saves = False
                            if delete_old_saves == True:
                                os.remove(os.path.join(saves_dir, x))
                    name_being_input = not name_being_input

            if event.type == pygame.KEYDOWN:                        # ingeven naam
                if name_being_input:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.unicode.isprintable():
                        if len(name) < 15:
                            name += event.unicode

        if gamerunning:

            if event.type == pygame.KEYDOWN:
                if gamepaused == False:                           # movement keybinds
                    if event.key == pygame.K_LEFT:
                        if character.x == 350 or character.x == 550:
                            vel_a = -20
                    if event.key == pygame.K_RIGHT:
                        if character.x == 350 or character.x == 150:
                            vel_a = 20

                    if event.key == pygame.K_SPACE:                 # turn sprinting on
                        vel_b = 4

                if event.key == pygame.K_ESCAPE:                  # game pause keybind
                    gamepaused = not gamepaused
                    if gamepaused:
                        stored_vel_a = vel_a
                        vel_a = 0
                        vel_b = 0
                    else:
                        vel_a = stored_vel_a
                        vel_b = 2

            if event.type == pygame.KEYUP:
                if gamepaused == False:
                    if event.key == pygame.K_SPACE:
                        vel_b = 2                              # turn sprinting off

        if event.type == pygame.QUIT:
            running = False
        
    # refresh scherm
    pygame.display.flip()
    time.sleep(1/60)

pygame.quit()