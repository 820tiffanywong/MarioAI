import math
import os
import random
import time
import neat
import numpy as np
from PIL import Image
import pygame


pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800
GEN = 0

MARIO_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "meowrio1.png"))),
              pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "meowrio2.png"))),
              pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "meowrio3.png")))]

GOOMBAS_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "goomba1_copy.png"))),
                pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "goomba2_copy.png"))),
                pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "goomba3_copy.png")))]

BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "marioBase.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "mariobg.jpeg")))
STAT_FONT = pygame.font.SysFont("comicsans", 50)

#jump_sound = pygame.mixer.Sound("jump.wav")
jump_sound = 'jump.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(jump_sound)

#pygame.event.wait()


# MARIO class, mario moving
class Mario:

    # constants
    IMGS = MARIO_IMGS

    # how fast the mario is going to flap its wings
    ANIMATION_TIME = 5

    MAX_JUMP_COUNT = 10
    JUMP_VEL = 18

    # starting position of mario
    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0  # physics of mario
        self.vel = 5
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        self.jump_count = 10
        self.isJump = False
        self.isRun = True
        self.alive = True
        self.rect = self.img.get_rect()
        #self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def jump(self):
        if self.jump_count == 10:
            #jump_sound.play()
            pygame.mixer.music.play()
        self.jump_count -= 1
        self.y -= (self.jump_count * abs(self.jump_count)) * 0.5
        # if self.jumpCount < self.MAX_JUMP_COUNT:
        #     self.vel = -self.JUMP_VEL
        #     self.jumpCount += 1
    #`````````````````````````````````
        # if self.isJump:
        #     if self.jumpCount >= -10:
        #         neg = 1
        #         if self.jumpCount < 0:
        #             neg = -1
        #         self.y -= self.jumpCount ** 2 * 0.1 * neg
        #         self.jumpCount -= 1
        #     else:
        #         self.isJump = False
        #         self.jumpCount = 10

        # if self.jump:
        #     self.mario.y -= self.jump_speed * 4
        #     self.jump_speed -= 0.5
        # if self.jump_speed <= -self.jump_speed:
        #     self.jump = False
        #     self.isRun = True
        #     self.jump_speed = self.jump_speed

    # every single frame to move our mario

    def move(self):

        self.tick_count += 1


    def draw(self, window):

        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]

        # then 1st image is shown and image count is RESET
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -90:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # Tilt the image
        rotated_image = pygame.transform.rotate(self.img, self.tilt)

        # rotates image around the center so it doesn't look weird
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        window.blit(rotated_image, new_rect.topleft)

    def mario_rect(self):
        mario_rect = self.img.get_rect()

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Goomba:

    IMGS = GOOMBAS_IMGS
    MAX_ROTATION = 0
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.height = 0
        self.tilt = 0
        self.tick_count = 0
        self.vel = 7
        self.bottom = 680
        self.img_count = 0

        # references mario IMGS and IMGS[0] is mario_IMGS[0] is mario1.png
        self.img = self.IMGS[0]
        self.rect = self.img.get_rect()
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = 50

    def move(self):
        # 30 frames per sec
        self.tick_count += 1
        self.x -= self.vel

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        # if image count is less than 10, the 2nd flappy mario image is displayed
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        # if image count is less than 15, then 3rd flappy mario image is displayed
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        # then 2nd image is shown
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        # then 1st image is shown and image count is RESET
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        #win.blit(self.img, (self.x, self.bottom))
        win.blit(self.img, (self.x, self.y))

    def goombarect(self):
        goomba_rect = self.img.get_rect()

    def collide(self, mario):

        mario_mask = mario.get_mask()
        goomba_mask = pygame.mask.from_surface(self.img)
        #print(self.rect.x, mario.rect.x)

        # TODO currently returning (0,0), which causes a collision
        offset = (round(mario.x - self.x), round(self.y - mario.y))
        # offset = (int(self.rect.x - mario.rect.x), int(self.rect.y - mario.rect.y))
        #print(offset)

        # get the overlap between the two masks at the given offset
        collision = goomba_mask.overlap(mario_mask, offset)
        #collision = mario_mask.overlap(goomba_mask, offset)

        return collision


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0  # base starts at x = 0 on the screen
        self.x2 = self.WIDTH  # base starts at the end (width) so right at the end of the screen

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, window):
        window.blit(self.IMG, (self.x1, self.y))
        window.blit(self.IMG, (self.x2, self.y))


def draw_window(window, marios, goombas, base, score, gen):
    window.blit(BG_IMG, (0, 0))

    for goomba in goombas:
        goomba.draw(window)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    window.blit(text, (10, 10))

    text = STAT_FONT.render("Fitness: " + str(gen), 1, (255, 255, 255))
    window.blit(text, (10, 70))

    base.draw(window)
    for mario in marios:
        mario.draw(window)
    pygame.display.update()


clock = pygame.time.Clock()


def main(genomes, config):

    global GEN

    GEN += 1
    nets = []
    ge = []
    marios = []
    mario = Mario(100, 680)
    goomba = Goomba(500, 680)
    mario_y = 680

    distanceMarGoom = abs(mario.rect.centerx - goomba.rect.centerx) / WIN_WIDTH
    player_bottom_y = mario.rect.bottom / WIN_HEIGHT
    player_top_y = mario.rect.top / WIN_HEIGHT

    # 3 lists so each position aka INDEX will correspond to the same mario's information
    goombaAI = Goomba(400, 600)
    # nets[0] = ge[0] = marios[0]
    jumpCount = 10
    for __, g in genomes:  # genomes ia tuple that has genome ID and object
        # (1, ge) but we only want genome object so loop has to have "__," to avoid errors
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        marios.append(Mario(100, 680))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    goombas = [Goomba(500, 680)]
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('MarioAI')

    score = 0
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                raise SystemExit
                quit()

        goomba_ind = 0

        # if the len of the mario is not 0, we don't need to look at it
        if len(marios) > 0:
            if len(goombas) > 1 and marios[0].x > goombas[0].x + goombas[0].img.get_width():
                goomba_ind = 1
                # setting pipe index to 0 because the pipe that is looked at is the input to the neural network
        else:
            run = False
            break
        previous_jump = time.time()
        for x, mario in enumerate(marios):
            mario.move()
            ge[x].fitness += 0.1
            #print(time.time() - previous_time)

            if round(time.time() - previous_jump, 2) == round(np.random.uniform(), 2):
                #if np.random.choice(3) == 1:
                mario.jump()
                #    previous_jump = time.time()
            #input = (mario.y, goombas[goomba_ind].x, goombas[goomba_ind].x)
            #THIS WORKS KIND OF
            #input = (mario.y, abs(mario.y - goombas[goomba_ind].y), abs(mario.y - goombas[goomba_ind].x))
            #input = (mario.y, mario.x, distanceMarGoom)
            input = (distanceMarGoom, player_bottom_y, player_top_y)

            output = nets[x].activate(input)

        rem = []
        add_goomba = False

        for x, goomba in enumerate(goombas):
            goomba.move()
            for x, mario in enumerate(marios):
                # if pygame.sprite.collide_rect(mario, goomba):
                #     ge[x].fitness -= 1
                #     run = False
                #     marios.pop(x)
                #     ge.pop(x)
                # else:
                #     ge[x].fitness += 0.1
                #     if goomba.rect.right < 0:
                #         score += 1
                #         goomba.reset()
                #````````````````````````

                if goomba.collide(mario):
                    print('COLLISION')
                    ge[x].fitness -= 1
                    marios.pop(x)
                    nets.pop(x)
                    ge.pop(x)
            # every time a mario hits a pipe, it's going to have 1 removed from its fitness score
            # if the marios passed the pipe then this if statement is used
                if not goomba.passed and goomba.x < mario.x:
                    goomba.passed = True
                    add_goomba = True
            # the pipe is removed outside the loop because it is only one pipe we're removing
            if goomba.x + goomba.img.get_width() < 0:
                rem.append(goomba)

            if goomba.x < mario.x < goomba.x + 50 and mario.y < goomba.y:
                g.fitness += 1

        if add_goomba:
            score += 1
            for g in ge:
                g.fitness += 3
            goombas.append(Goomba(500, 680))

        for r in rem:
            goombas.remove(r)

        for x, mario in enumerate(marios):
            if mario.y + mario.img.get_height() >= 730 or mario.y < 0:
                marios.pop(x)
                #nets.pop(x)
                ge.pop(x)

        if score > 30:
            break

        base.move()
        draw_window(window, marios, goombas, base, score, GEN)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    # setting the population
    p = neat.Population(config)
    # output
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # fitness function to run 50 many generations
    # to determine our marios' fitness, we see how far it moves in the game
    #
    winner = p.run(main, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
