import pygame
import neat
import time
import os
import random

pygame.font.init()
WIN_WIDTH = 450
WIN_HEIGHT = 700


BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(
    os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join("imgs", "bird3.png")))
]
PIPE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bg.png")))


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y  # current vertical position
        self.tilt = 0
        # A counter to keep track of how many frames have passed since the bird last jumped.
        self.tick_count = 0
        self.vel = 0
        # vertical pos when it was last drawn on the screen.
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):    # up '-', down '+'
        self.vel = -6.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5 * self.tick_count**2
        if d >= 16:  # downward
            d = 16
        if d < 0:   # upward
            d -= 2
        self.y = self.y + d

        if d < 0 or self.y < self.height + 10:   # upward
            self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:                  # downward
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1
        if self.tilt <= -20:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME - 20
        else:
            if self.img_count < self.ANIMATION_TIME:
                self.img = self.IMGS[0]
            elif self.img_count < self.ANIMATION_TIME * 2:
                self.img = self.IMGS[1]
            elif self.img_count < self.ANIMATION_TIME * 3:
                self.img = self.IMGS[2]
            elif self.img_count < self.ANIMATION_TIME * 4:
                self.img = self.IMGS[1]
            elif self.img_count < self.ANIMATION_TIME * 4 + 1:
                self.img = self.IMGS[0]
                self.img_count = 0

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200  # gap between the upper and lower pipes
    VEL = 5    # how fast the pipes move

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird, win):
        # global score
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        # distance from the top mask to the bird
        top_offset = (self.x - bird.x, self.top-round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom-round(bird.y))
        # b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        # t_point = bird_mask.overlap(top_mask, top_offset)
        if bird_mask.overlap(top_mask, top_offset):
            return True
        elif bird_mask.overlap(bottom_mask, bottom_offset):
            return True
        else:
            return False

    def display_score(self, win, score):
        WHITE = (255, 255, 255)
        font = pygame.font.Font(
            r"C:\Users\seren\OneDrive\Documents\Python project\AI\Flappy_Bird\font\slkscr.ttf", 40)
        text_surface = font.render(str(score), True, WHITE)
        text_rect = text_surface.get_rect(
            center=(WIN_WIDTH // 1.11, WIN_HEIGHT // 8))
        win.blit(text_surface, text_rect)
        pygame.display.update()


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def game_over_func(win):
    BLACK = (0, 0, 0)
    win.blit(BG_IMG, (0, -150))
    font = pygame.font.Font(
        r"C:\Users\seren\OneDrive\Documents\Python project\AI\Flappy_Bird\font\slkscr.ttf", 36)
    text_surface = font.render("GAME OVER", True, BLACK)
    text_rect = text_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 4))
    win.blit(text_surface, text_rect)

    # button
    button_width, button_height = 200, 50
    button_x, button_y = WIN_WIDTH//2 - 100, WIN_HEIGHT//2
    button_color = (255, 255, 0)
    # button_hover_color = (200, 200, 200)
    pygame.draw.rect(win, button_color, (button_x,
                     button_y, button_width, button_height))
    text = font.render("Restart", True, BLACK)
    text_rect = text.get_rect(center=(WIN_WIDTH//2, WIN_HEIGHT//2+25))
    win.blit(text, text_rect)
    # global score
    # score = 0
    pygame.display.update()


def draw_window(win, birds, pipes, base, score):
    win.blit(BG_IMG, (0, -150))

    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    for bird in birds:
        bird.draw(win)
    # for pipe in pipes:
    #     pipe.display_score(win, score)

    pygame.display.update()


def restart(win, bird):
    bird.img = None


def random_number(previous_x_pos, min_distance=100):
    return previous_x_pos + min_distance + random.randrange(200, 500)


def main(genomes, config):
    nets = []  # all the neuron network
    ge = []  # genetic information (weights and connections)
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        ge.append(g)
        g.fitness = 0

    base = Base(600)
    pipes = [Pipe(5000)]
    global win
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
        clock.tick(30)
        if pipes[0].x < -PIPE_IMG.get_width():
            pipes.pop(0)
        for pipe in pipes:
            for x, bird in enumerate(birds):
                score = 0
                pipe.move()
                bird.move()
                game_over = pipe.collide(bird, win)
                ge[x].fitness += 0.5
                if pipes[-1].x < WIN_WIDTH - pipes[-1].PIPE_TOP.get_width()-150:
                    rn = random_number(pipes[-1].x)
                    pipes.append(Pipe(rn))  # generate new pipe
                    ge[x].fitness += 1
                    # pipe.display_score(win,  score)
                    # pygame.display.update()
                output = nets[x].activate(
                    (bird.y, abs(bird.y - pipes[-1].height), abs(bird.y - pipes[-1].bottom)))
                if output[0] > 0.5:
                    bird.jump()
                if game_over:
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    # game_over_func(win)

                elif bird.y < 0 or bird.y + bird.img.get_height() >= 600:
                    game_over = True
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if len(birds) == 0:
                    run = False
                    break

        base.move()
        draw_window(win, birds, pipes, base, score)
        # check floor colision
        # for x, bird in enumerate(birds):
        #     if bird.y + bird.img.get_height() >= 600:
        #         game_over = True
        #         birds.pop(x)
        #         nets.pop(x)
        #         ge.pop(x)

    # if game_over:
    #     game_over_func(win)


'''
Input layer: bird.y, Top pipe pos, Bottom Pipe pos (3 neurons)
Activation Func / also gives probability: Tanh()
Output layer: Jump? (1 neuron)

Population size: 100 birds
Fitness Function (find the best birds): how many pipes it passed
Max generations: 30
'''


def run(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 100)   # 50 generation, 100 neuronetworks each


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
