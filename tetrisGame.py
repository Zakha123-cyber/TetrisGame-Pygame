import pygame
import random

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]


class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    def __init__(self, height, width):
        self.level = 1
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = height
        self.width = width
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.figure = None

        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if (
                        i + self.figure.y > self.height - 1
                        or j + self.figure.x > self.width - 1
                        or j + self.figure.x < 0
                        or self.field[i + self.figure.y][j + self.figure.x] > 0
                    ):
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


def draw_button(screen, text, x, y, width, height, color, font_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.SysFont("Calibri", 30, True)
    label = font.render(text, True, font_color)
    screen.blit(label, (x + 10, y + 10))


# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Main loop to choose level
choose_level = True
fps = 15
fall_speed = 1

# Tambahkan tampilan awal SUPER TETRIS
def draw_initial_screen(screen):
    screen.fill(WHITE)
    font = pygame.font.SysFont("Calibri", 60, True)  # Besar font untuk judul
    title = font.render("SUPER TETRIS", True, BLACK)
    screen.blit(title, (50, 100))

    draw_button(screen, "Next", 50, 250, 300, 50, GREEN, BLACK)  # Tombol "Next"
    pygame.display.flip()

# Main loop untuk tampilan awal
initial_screen = True

while initial_screen:
    screen.fill(WHITE)

    # Tampilkan tampilan judul
    draw_initial_screen(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 50 <= x <= 350 and 250 <= y <= 300:  # Tombol Next
                initial_screen = False  # Pergi ke menu level

    pygame.display.flip()

# Main loop untuk memilih level setelah tombol "Next" ditekan
fps = 15
fall_speed = 1

# Fungsi untuk menggambar tombol Play Again dan Back to Menu
def draw_game_over_screen(screen, score):
    screen.fill(WHITE)
    font_title = pygame.font.SysFont("Calibri", 60, True)
    title = font_title.render("GAME OVER", True, BLACK)
    screen.blit(title, (50, 100))

    # Menampilkan score
    font_score = pygame.font.SysFont("Calibri", 30, True)
    score_text = font_score.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (150, 200))

    # Tombol Play Again
    draw_button(screen, "Play Again", 50, 300, 300, 50, GREEN, BLACK)
    
    # Tombol Back to Menu
    draw_button(screen, "Back to Menu", 50, 400, 300, 50, BLUE, BLACK)

    pygame.display.flip()

# Main game loop
done = False
clock = pygame.time.Clock()
game = Tetris(20, 10)
counter = 0
pressing_down = False

# Tambahkan state untuk menentukan posisi game
current_state = "menu"  # Bisa bernilai "menu", "playing", "gameover"

while not done:
    if current_state == "menu":  # Menu untuk memilih level
        screen.fill(WHITE)
        draw_button(screen, "Easy", 50, 150, 300, 50, GREEN, BLACK)
        draw_button(screen, "Medium", 50, 250, 300, 50, BLUE, BLACK)
        draw_button(screen, "Hard", 50, 350, 300, 50, RED, BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 50 <= x <= 350:
                    if 150 <= y <= 200:  # Easy
                        fps = 10
                        fall_speed = 1
                        current_state = "playing"
                        game = Tetris(20, 10)  # Reset game
                    elif 250 <= y <= 300:  # Medium
                        fps = 15
                        fall_speed = 1.5
                        current_state = "playing"
                        game = Tetris(20, 10)  # Reset game
                    elif 350 <= y <= 400:  # Hard
                        fps = 25
                        fall_speed = 2
                        current_state = "playing"
                        game = Tetris(20, 10)  # Reset game

        pygame.display.flip()

    elif current_state == "playing":  # Logika permainan
        if game.figure is None:
            game.new_figure()
        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (fps // game.level // fall_speed) == 0 or pressing_down:
            if game.state == "start":
                game.go_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_LEFT:
                    game.go_side(-1)
                if event.key == pygame.K_RIGHT:
                    game.go_side(1)
                if event.key == pygame.K_SPACE:
                    game.go_space()
                if event.key == pygame.K_ESCAPE:
                    game.__init__(20, 10)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False

        if game.state == "gameover":
            current_state = "gameover"  # Pindah ke state game over

        else:
            screen.fill(WHITE)
            for i in range(game.height):
                for j in range(game.width):
                    pygame.draw.rect(
                        screen,
                        GRAY,
                        [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom],
                        1,
                    )
                    if game.field[i][j] > 0:
                        pygame.draw.rect(
                            screen,
                            colors[game.field[i][j]],
                            [
                                game.x + game.zoom * j + 1,
                                game.y + game.zoom * i + 1,
                                game.zoom - 2,
                                game.zoom - 2,
                            ],
                        )

            if game.figure is not None:
                for i in range(4):
                    for j in range(4):
                        if i * 4 + j in game.figure.image():
                            pygame.draw.rect(
                                screen,
                                colors[game.figure.color],
                                [
                                    game.x + game.zoom * (game.figure.x + j) + 1,
                                    game.y + game.zoom * (game.figure.y + i) + 1,
                                    game.zoom - 2,
                                    game.zoom - 2,
                                ],
                            )

            # Menampilkan skor di kiri atas
            font_score = pygame.font.SysFont("Calibri", 30, True)
            score_text = font_score.render(f"Score: {game.score}", True, BLACK)
            screen.blit(score_text, (10, 10))  # Posisi skor di kiri atas

        pygame.display.flip()

        clock.tick(fps)

    elif current_state == "gameover":  # Layar Game Over
        draw_game_over_screen(screen, game.score)

        waiting_for_action = True
        while waiting_for_action:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    waiting_for_action = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 50 <= x <= 350 and 300 <= y <= 350:  # Tombol Play Again
                        game.__init__(20, 10)  # Reset permainan
                        game.state = "start"
                        current_state = "playing"  # Mulai ulang permainan
                        waiting_for_action = False
                    elif 50 <= x <= 350 and 400 <= y <= 450:  # Tombol Back to Menu
                        current_state = "menu"  # Kembali ke menu level
                        waiting_for_action = False

    else:
        # Game aktif, tampilkan permainan
        screen.fill(WHITE)
        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(
                    screen,
                    GRAY,
                    [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom],
                    1,
                )
                if game.field[i][j] > 0:
                    pygame.draw.rect(
                        screen,
                        colors[game.field[i][j]],
                        [
                            game.x + game.zoom * j + 1,
                            game.y + game.zoom * i + 1,
                            game.zoom - 2,
                            game.zoom - 2,
                        ],
                    )

        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in game.figure.image():
                        pygame.draw.rect(
                            screen,
                            colors[game.figure.color],
                            [
                                game.x + game.zoom * (game.figure.x + j) + 1,
                                game.y + game.zoom * (game.figure.y + i) + 1,
                                game.zoom - 2,
                                game.zoom - 2,
                            ],
                        )
        # Menampilkan skor di kiri atas
        font_score = pygame.font.SysFont("Calibri", 30, True)
        score_text = font_score.render(f"Score: {game.score}", True, BLACK)
        screen.blit(score_text, (10, 10))  # Posisi skor di kiri atas
        
    pygame.display.flip()

    clock.tick(fps)

pygame.quit()
