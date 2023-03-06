import pygame
import os
import random
import time
import neat
from PIL import Image

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


# MARIO class, mario moving
class Mario:

    # constants
    IMGS = MARIO_IMGS

    # how much the mario is going to tilt
    #MAX_ROTATION = 0

    # how much we're going to rotate the mario in each frame every time we move the mario
    #ROT_VEL = 0

    # how fast the mario is going to flap its wings
    ANIMATION_TIME = 5

    # starting position of mario
    def __init__(self, x, y):
        self.x = 120
        self.y = 680
        self.tilt = 0
        self.tick_count = 0  # physics of mario
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = 2
        self.tick_count = 0
        self.height = self.y

    # every single frame to move our mario
    def move(self):

        # 30 frames per sec
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

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Goomba:
    IMGS = GOOMBAS_IMGS
    MAX_ROTATION = 0
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):

        self.x = 400
        self.y = y

        self.height = 0

        self.tilt = 0
        self.tick_count = 0
        self.vel = 2

        self.bottom = 680
        self.img_count = 0

        # references mario IMGS and IMGS[0] is mario_IMGS[0] is mario1.png
        self.img = self.IMGS[0]
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = 50

    def move(self):
        # 30 frames per sec
        self.tick_count += 8
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

        win.blit(self.img, (self.x, self.bottom))

    def collide(self, mario):
        mario_mask = mario.get_mask()
        goomba_mask = pygame.mask.from_surface(self.img)

        offset = (self.x - mario.x, self.y - round(mario.y))

        # point of collision or overlap between the bird mask and the bottom pipe which is the bottom_offset
        # if it doesn't collide, it returns NONE ---- point of intersection

        point = mario_mask.overlap(goomba_mask, offset)
        if point:
            return True
        return False


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
    base.draw(window)
    for mario in marios:
        mario.draw(window)
    pygame.display.update()


def main(genomes, config):

    # this is only for checking one mario at a time
    # mario = mario(230, 350)

    # Need to keep track of the neural network that controls each mario
    # because these genomes coming in are just a bunch of neural networks
    # that control each of our marios

    # Need to keep track of the mario that neural networks controlling
    # & where that position is in the screen

    # Need to keep track of our genomes so I can change their fitness based on how
    # far they moved or if they hit a pipe
    global GEN
    GEN += 1
    nets = []
    ge = []
    marios = []
    # 3 lists so each position aka INDEX will correspond to the same mario's information

    # nets[0] = ge[0] = marios[0]
    for __, g in genomes:  # genomes ia tuple that has genome ID and object
        # (1, ge) but we only want genome object so loop has to have "__," to avoid errors
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        # standard mario object that will start at the same position of all the other mario objects
        marios.append(Mario(230, 350))
        #goombas = [Goomba(10, 50)] * 10
        g.fitness = 0
        ge.append(g)
    base = Base(730)
    goombas = [Goomba(600, 250)]
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('MarioAI')
    clock = pygame.time.Clock()

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
            # no marios left, so quit game
            run = False
            break

        for x, mario in enumerate(marios):
            mario.move()
            ge[x].fitness += 0.1
            # pass values to a neural network so the mario + the associated neural network get its output value
            # then checks if that output is greater than 0.5 & if yes then mario jumps
            output = nets[x].activate((mario.y, abs(mario.y - goombas[goomba_ind].height), abs(mario.y - goombas[goomba_ind].bottom)))
            # output = nets[x].activate((mario.y, abs(mario.y - pipes[pipe_ind].height), abs(mario.y - pipes[pipe_ind].bottom)))

            # find distance between top pipe and mario & distance between bottom pipe and mario
            if output[0] > 0.5:  # output is a list & we r returning one output neuron for each example
                mario.jump()
        rem = []
        add_goomba = False

        for x, goomba in enumerate(goombas):
            # for every mario, check if each mario collides with the pipe
            # enumerating to get the position in the list of where the mario is as well
            for x, mario in enumerate(marios):
                if goomba.collide(mario):
                    ge[x].fitness -= 1
                    marios.pop(x)
                    nets.pop(x)
                    ge.pop(x)
            #         # every time a mario hits a pipe, it's going to have 1 removed from its fitness score
            #     # if the marios passed the pipe then this if statement is used
                if not goomba.passed and goomba.x < mario.x:
                    goomba.passed = True
                    add_goomba = True
            # the pipe is removed outside the loop because it is only one pipe we're removing
            #if goomba.x + goomba.PIPE_TOP.get_width() < 0:
            if goomba.x + goomba.img.get_width() < 0:
                rem.append(goomba)
            goomba.move()
        if add_goomba:
            score += 1
            for g in ge:
                g.fitness += 5
            goombas.append(Goomba(600, 250))

        for r in rem:
            goombas.remove(r)

        for x, mario in enumerate(marios):
            if mario.y + mario.img.get_height() >= 730 or mario.y < 0:
                marios.pop(x)
                nets.pop(x)
                ge.pop(x)

        if score > 30:
            break

        base.move()
        draw_window(window, marios, goombas, base, score, GEN)

    pygame.quit()
    quit()


# main()


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
