import os
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

jump_sound = 'jump.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(jump_sound)


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

        self.img_count = 0
        self.img = self.IMGS[0]
        self.rect = self.img.get_rect()
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.vel = 5
        self.is_jumping = False
        self.jump_vel = 10
        self.jump_timer = 0
        self.left = False
        self.right = False
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel
            self.left = True
            self.right = False
        elif keys[pygame.K_RIGHT] and self.x < WIN_WIDTH - self.x:
            self.x += self.vel
            self.right = True
            self.left = False
        else:
            self.right = False
            self.left = False

        if not self.is_jumping:
            if keys[pygame.K_SPACE]:
                self.is_jumping = True
                self.jump_vel = 40
                self.jump_timer = 0
        else:
            if self.jump_timer < 10:
                self.y -= self.jump_vel
                self.hitbox.move_ip(0, -self.jump_vel)
                self.jump_vel -= 10
                self.jump_timer += 1
            else:
                self.is_jumping = False
                self.jump_vel = 15

        if self.hitbox.bottom >= 730:
            self.hitbox.bottom = 730
            self.y = self.hitbox.bottom - self.height

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
        self.vel = 5
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

        win.blit(self.img, (self.x, self.y))

    def goombarect(self):
        goomba_rect = self.img.get_rect()


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

    base.draw(window)
    for mario in marios:
        mario.draw(window)
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    mario = [Mario(100, 680)]

    base = Base(730)
    goombas = [Goomba(500, 680)] * 4
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

        mario[0].move()
        rem = []
        add_goomba = False

        for x, goomba in enumerate(goombas):
            goomba.move()

            if goomba.x + goomba.img.get_width() < 0:
                rem.append(goomba)

        if add_goomba:
            goombas.append(Goomba(500, 680))

        for r in rem:
            goombas.remove(r)

        base.move()
        draw_window(window, mario, goombas, base, score, GEN)


if __name__ == '__main__':
    main()
