import math
import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1920, 1080
FPS = 24

BG = (2, 8, 2)
LINE_COLOR = (30, 140, 60)
DOT_COLOR = (180, 255, 180)
GLOW_COLOR = (40, 220, 80)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Elastic Mesh Toy")
clock = pygame.time.Clock()


def show_intro():
    font_big = pygame.font.SysFont("monospace", 64, bold=True)
    font_small = pygame.font.SysFont("monospace", 26)

    start_time = pygame.time.get_ticks()
    duration = 2500

    while True:
        now = pygame.time.get_ticks()
        elapsed = now - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return True

        if elapsed >= duration:
            return True

        screen.fill(BG)

        title = font_big.render("WELCOME TO THE MATRIX", True, DOT_COLOR)
        subtitle = font_small.render("Wake up, to reality..", True, LINE_COLOR)

        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 35))

        screen.blit(title, title_rect)
        screen.blit(subtitle, subtitle_rect)

        pygame.display.flip()
        clock.tick(60)


class Node:
    def __init__(self, x, y, pinned=False):
        self.x = x
        self.y = y
        self.base_x = x
        self.base_y = y
        self.vx = 0.0
        self.vy = 0.0
        self.pinned = pinned

    def update(self, dt):
        if self.pinned:
            self.x = self.base_x
            self.y = self.base_y
            self.vx = 0.0
            self.vy = 0.0
            return

        self.x += self.vx * dt
        self.y += self.vy * dt

    def damp(self, amount):
        self.vx *= amount
        self.vy *= amount


class Spring:
    def __init__(self, a, b, stiffness=18.0):
        self.a = a
        self.b = b
        self.rest = math.hypot(b.x - a.x, b.y - a.y)
        self.stiffness = stiffness

    def apply(self, dt):
        dx = self.b.x - self.a.x
        dy = self.b.y - self.a.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            return

        stretch = dist - self.rest
        force = self.stiffness * stretch

        nx = dx / dist
        ny = dy / dist

        fx = force * nx
        fy = force * ny

        if not self.a.pinned:
            self.a.vx += fx * dt
            self.a.vy += fy * dt

        if not self.b.pinned:
            self.b.vx -= fx * dt
            self.b.vy -= fy * dt


cols = 50
rows = 28
spacing = 36

mesh_width = (cols - 1) * spacing
mesh_height = (rows - 1) * spacing
offset_x = (WIDTH - mesh_width) // 2
offset_y = (HEIGHT - mesh_height) // 2

grid = []
nodes = []
springs = []

for r in range(rows):
    row = []
    for c in range(cols):
        x = offset_x + c * spacing
        y = offset_y + r * spacing

        pinned = (r == 0 or r == rows - 1 or c == 0 or c == cols - 1)
        node = Node(x, y, pinned)
        row.append(node)
        nodes.append(node)
    grid.append(row)

for r in range(rows):
    for c in range(cols):
        if c < cols - 1:
            springs.append(Spring(grid[r][c], grid[r][c + 1], stiffness=18.0))
        if r < rows - 1:
            springs.append(Spring(grid[r][c], grid[r + 1][c], stiffness=18.0))
        if c < cols - 1 and r < rows - 1:
            springs.append(Spring(grid[r][c], grid[r + 1][c + 1], stiffness=12.0))
        if c > 0 and r < rows - 1:
            springs.append(Spring(grid[r][c], grid[r + 1][c - 1], stiffness=12.0))


def apply_mouse_force(mx, my, pmx, pmy):
    dx = mx - pmx
    dy = my - pmy
    radius = 110
    strength = 22.0

    for node in nodes:
        if node.pinned:
            continue

        dist_x = node.x - mx
        dist_y = node.y - my
        d = math.hypot(dist_x, dist_y)

        if d < radius:
            falloff = 1.0 - (d / radius)
            node.vx += dx * strength * falloff
            node.vy += dy * strength * falloff


def draw_glow(surface, x, y):
    pygame.draw.circle(surface, GLOW_COLOR, (int(x), int(y)), 5)
    pygame.draw.circle(surface, DOT_COLOR, (int(x), int(y)), 2)


if not show_intro():
    pygame.quit()
    sys.exit()

running = True
mouse_down = False
prev_mouse = pygame.mouse.get_pos()

while running:
    dt = min(clock.tick(FPS) / 1000.0, 0.033)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_down = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False

    mx, my = pygame.mouse.get_pos()
    pmx, pmy = prev_mouse

    if mouse_down:
        apply_mouse_force(mx, my, pmx, pmy)

    physics_steps = 4
    sub_dt = dt / physics_steps

    for _ in range(physics_steps):
        for spring in springs:
            spring.apply(sub_dt)

        for node in nodes:
            if not node.pinned:
                restore_x = (node.base_x - node.x) * 3.5
                restore_y = (node.base_y - node.y) * 3.5
                node.vx += restore_x * sub_dt
                node.vy += restore_y * sub_dt

            node.damp(0.965)
            node.update(sub_dt)

    screen.fill(BG)

    for spring in springs:
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (int(spring.a.x), int(spring.a.y)),
            (int(spring.b.x), int(spring.b.y)),
            1
        )

    for node in nodes:
        draw_glow(screen, node.x, node.y)

    pygame.display.flip()
    prev_mouse = (mx, my)

pygame.quit()