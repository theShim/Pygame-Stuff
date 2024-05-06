import pygame
import numpy

W, H = 720, 720
FPS = 60

FLAGS = 0 #  | pygame.SCALED


class State:
    def __init__(self):
        self.grid = numpy.random.randint(0xFF00FF, 0xFFFF00, (W//4, H//4), numpy.int32)

    def step(self):
        shifted = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (dx, dy) != (0, 0):
                    shifted.append(numpy.roll(self.grid, (dx, dy), (0, 1)))

        rand_vals = numpy.random.randint(0, len(shifted), (W//4, H//4), numpy.int8)

        masks = []
        for i in range(len(shifted)):
            masks.append(1 * (rand_vals == i))

        self.grid[:] = 0
        for i in range(len(shifted)):
            self.grid += masks[i] * shifted[i]

    def draw(self, screen):
        pygame.surfarray.blit_array(screen, self.grid)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((W, H), flags=FLAGS)
    window = pygame.Surface((W/4, H/4))

    state = State()
    clock = pygame.time.Clock()

    running = True
    last_update_time = pygame.time.get_ticks()

    while running:
        current_time = pygame.time.get_ticks()
        dt = (current_time - last_update_time) / 1000
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    print("Resetting.")
                    state = State()
                elif e.key == pygame.K_RIGHT:
                    FPS += 10
                    print("Increased target FPS to: {}".format(FPS))
                elif e.key == pygame.K_LEFT:
                    FPS = max(10, FPS - 10)
                    print("Decreased target FPS to: {}".format(FPS))
        state.step()
        state.draw(window)
        screen.blit(pygame.transform.scale(window, pygame.math.Vector2(window.get_size())*4), (0, 0))

        pygame.display.flip()

        if current_time // 1000 > last_update_time // 1000:
            pygame.display.set_caption("Color Swirl (FPS={:.1f}, TARGET_FPS={}, SIZE={})".format(clock.get_fps(), FPS, (W, H)))

        last_update_time = current_time
        clock.tick(FPS)