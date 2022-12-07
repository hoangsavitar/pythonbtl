import pygame
import sys
import random
import time
import pandas as pd
import pygame.gfxdraw
from label import *
from button import Button
from data import questions
from utils import save_point
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")
image2 = pygame.image.load("assets/2.jpg")
image3 = pygame.image.load("assets/3.jpg")
image4 = pygame.image.load("assets/4.jpg")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


# 1
buttons = pygame.sprite.Group()


class Button2(pygame.sprite.Sprite):
    ''' A button treated like a Sprite... and killed too '''

    def __init__(self, position, text, size,
                 colors="white on blue",
                 hover_colors="red on green",
                 style="button1",
                 borderc=(255, 255, 255),
                 command=lambda: print("No command activated for this button")):

        # the hover_colors attribute needs to be fixed
        super().__init__()
        global num

        self.text = text
        self.command = command
        # --- colors ---
        self.colors = colors
        self.original_colors = colors
        self.fg, self.bg = self.colors.split(" on ")
        # hover_colors
        if hover_colors == "red on green":
            self.hover_colors = f"{self.bg} on {self.fg}"
        else:
            self.hover_colors = hover_colors
        # styles can be button1 or button2 (more simple this one)
        self.style = style
        self.borderc = borderc  # for the style2
        # font
        self.font = pygame.font.SysFont("Arial", size)
        self.render(self.text)
        self.x, self.y, self.w, self.h = self.text_render.get_rect()
        self.x, self.y = position
        self.rect = pygame.Rect(self.x, self.y, 500, self.h)
        self.position = position
        self.pressed = 1
        # the groups with all the buttons
        buttons.add(self)

    def render(self, text):
        # we have a surface
        self.text_render = self.font.render(text, 1, self.fg)
        # memorize the surface in the image attributes
        self.image = self.text_render

    def update(self):
        self.fg, self.bg = self.colors.split(" on ")
        if self.style == "button1":
            self.draw_button1()
        elif self.style == "button2":
            self.draw_button2()
        if self.command != None:
            self.hover()
            self.click()

    def draw_button1(self):
        ''' draws 4 lines around the button and the background '''
        # horizontal up
        lcolor = (150, 150, 150)
        lcolor2 = (50, 50, 50)
        pygame.draw.line(screen, lcolor, self.position,
                         (self.x + self.w, self.y), 5)
        pygame.draw.line(screen, lcolor, (self.x, self.y - 2),
                         (self.x, self.y + self.h), 5)
        # horizontal down
        pygame.draw.line(screen, lcolor2, (self.x, self.y + self.h),
                         (self.x + self.w, self.y + self.h), 5)
        pygame.draw.line(screen, lcolor2, (self.x + self.w, self.y + self.h),
                         [self.x + self.w, self.y], 5)
        # background of the button
        pygame.draw.rect(screen, self.bg, self.rect)

    def draw_button2(self):
        ''' a linear border '''
        # the width is set to 500 to have the same size not depending on the text size
        pygame.draw.rect(screen, self.bg, (self.x - 100, self.y, 500, self.h))
        pygame.gfxdraw.rectangle(
            screen, (self.x - 100, self.y, 500, self.h), self.borderc)

    def check_collision(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # you can change the colors when the pointer is on the button if you want
            self.colors = self.hover_colors
            # pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            self.colors = self.original_colors
            # pygame.mouse.set_cursor(*pygame.cursors.arrow)

    def hover(self):
        ''' checks if the mouse is over the button and changes the color if it is true '''

        self.check_collision()

    def click(self):
        ''' checks if you click on the button and makes the call to the action just one time'''
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and self.pressed == 1:
                print("The answer is:'" + self.text + "'")
                self.command()
                self.pressed = 0

            if pygame.mouse.get_pressed() == (0, 0, 0):
                self.pressed = 1


# ACTION FOR BUTTON CLICK ================

def on_click():
    print("Click on one answer")


def on_right():
    check_score("right")


def on_false():
    ''' if there is no 'right' as arg it means it's false '''
    check_score("wrong")


def check_score(answered="wrong"):
    ''' here we check if the answer is right '''
    global qnum, points, score, title, text
    print("qnum", qnum)
    # until there are questions (before last)
    # hit.play()  # click sound
    if qnum < len(questions):
        print(qnum, len(questions))
        if answered == "right":
            time.sleep(.1)  # to avoid adding more point when pressing too much
            points += 1
            # Show the score text
        qnum += 1  # counter for next question in the list
        score.change_text((name_player + ":" + str(points)) + " point")
        # Change the text of the question
        title.change_text(questions[qnum-1][0], color="white")
        # change the question number
        num_question.change_text("Cau so " + str(qnum)+": ")
        show_question(qnum-1)  # delete old buttons and show new

    # for the last question...
    elif qnum == len(questions):
        print(qnum, len(questions))
        if answered == "right":
            time.sleep(.1)
            points += 1
        kill()
        # title.change_text("And Game", color="cyan")
        # score.change_text("You reached a score of " + str(points))
        # nu-m_question.change_text(newtext="and game")
        # save_point(name_player=text, point=points)
    time.sleep(.5)


def show_question(qnum):
    # Kills the previous buttons/sprites
    kill()

    # The 4 position of the buttons
    pos = [200, 250, 300, 350]
    # randomized, so that the right one is not on top
    random.shuffle(pos)

    # ============== TEXT: question and answers ====================
    print(qnum)
    Button2((450, pos[0]), questions[qnum][1][0], 36, "black on white",
            hover_colors="blue on orange", style="button2", borderc=(255, 255, 0),
            command=on_right)
    Button2((450, pos[1]), questions[qnum][1][1], 36, "black on white",
            hover_colors="blue on orange", style="button2", borderc=(255, 255, 0),
            command=on_false)
    Button2((450, pos[2]), questions[qnum][1][2], 36, "black on white",
            hover_colors="blue on orange", style="button2", borderc=(255, 255, 0),
            command=on_false)
    Button2((450, pos[3]), questions[qnum][1][3], 36, "black on white",
            hover_colors="blue on orange", style="button2", borderc=(255, 255, 0),
            command=on_false)


def kill():
    for _ in buttons:
        _.kill()


qnum = 0
points = 0
name_player = 'person1'
text = ''
# ================= SOME LABELS ==========================
num_question = Label(screen, ("Cau so " + str(qnum + 1))+": ", 200, 93, 40)
score = Label(screen, name_player, 1000, 50, 25, color="cyan")
title = Label(screen, questions[qnum][0], 350, 100, 35, color="cyan")


def show_end(score):
    global points
    screen.fill((0, 0, 0))
    anh = pygame.image.load("assets/victory.jpg")
    screen.blit(pygame.transform.scale(anh, (1280, 720)), (0, 0))
    # boxx
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    text1 = pygame.font.SysFont('freesanbold.ttf', 50).render(
        'Nhap ten cua ban', True, (0, 0, 0))
    screen.blit(text1, (500, 600))
    text2 = pygame.font.SysFont('freesanbold.ttf', 50).render(
        'Ban duoc: '+str(points)+'diem', True, (0, 0, 0))
    screen.blit(text2, (490, 330))
    input_box = pygame.Rect(500, 650, 280, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('green')
    color = color_inactive
    active = False
    text = ''
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        save_point(name_player=text, point=points)
                        text = ''
                        main_menu()
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(300, txt_surface.get_width()+20)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)


def loop():
    global points, qnum
    # PLAY_BACK = Button(image=None, pos=(1220, 700),
    #                     text_input="BACK", font=get_font(25), base_color="White", hovering_color="Green")

    # # PLAY_BACK.changeColor(PLAY_MOUSE_POS)
    # PLAY_BACK.update(screen)

    show_question(qnum)
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        screen.blit(BG, (0, 0))
        buttons.update()  # update buttons
        buttons.draw(screen)
        screen.blit(pygame.transform.scale(image2, (400, 280)), (50, 400))
        screen.blit(pygame.transform.scale(image3, (400, 280)), (450, 400))
        screen.blit(pygame.transform.scale(image4, (400, 280)), (850, 400))
        Button(image=None, pos=(410, 220),
               text_input="A.", font=get_font(30), base_color="black", hovering_color="Green").update(screen)
        Button(image=None, pos=(410, 271),
               text_input="B.", font=get_font(30), base_color="black", hovering_color="Green").update(screen)
        Button(image=None, pos=(410, 322),
               text_input="C.", font=get_font(30), base_color="black", hovering_color="Green").update(screen)
        Button(image=None, pos=(410, 373),
               text_input="D.", font=get_font(30), base_color="black", hovering_color="Green").update(screen)
        show_labels()  # update labels
        clock.tick(60)
        if qnum == len(questions):
            show_end(points)
            points = 0
            qnum = 0
        PLAY_BACK = Button(image=None, pos=(1220, 700),
                           text_input="BACK", font=get_font(25), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
        pygame.display.update()


def play():
    while True:
        if __name__ == '__main__':
            pygame.init()
            loop()
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BACK = Button(image=None, pos=(1220, 700),
                           text_input="BACK", font=get_font(25), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
        pygame.display.update()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")
        df = pd.read_csv('rank.csv')
        for i in range(len(df)):
            OPTIONS_TEXT = get_font(45).render(
                str(df['name_player'][i]) + " " + str(df['score'][i]), True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100 + i*100))
            screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(1220, 700),
                              text_input="BACK", font=get_font(25), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    pygame.mixer.music.load(
        'assets\See-Tình-Remix-Hoàng-Thùy-Linh-Cukak-Remix (mp3cut.net).mp3')
    pygame.mixer.music.play(-1)
    global points, qnum
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="RANKING", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    qnum = 0
                    points = 0
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    qnum = 0
                    points = 0
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        kill()
        pygame.display.update()


main_menu()
# play()
