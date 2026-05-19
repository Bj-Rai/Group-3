# =========================================================
# BRAIN TREK - REALISTIC FOREST EDITION
# =========================================================
# INSTALL:
# pip install pygame
#
# RUN:
# python brain_trek.py
# =========================================================

import pygame
import random
import math
import sys

pygame.init()

# =========================================================
# WINDOW
# =========================================================

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brain Trek - Realistic Forest")

clock = pygame.time.Clock()
FPS = 60

# =========================================================
# WORLD
# =========================================================

WORLD_SIZE = 5000
PLAYER_SPEED = 4

# =========================================================
# GAME SETTINGS
# =========================================================

QUIZ_TIME = 20
HINT_COST = 500
START_LIVES = 5

# =========================================================
# COLORS
# =========================================================

WHITE = (255, 255, 255)
BLACK = (10, 10, 10)

GOLD = (255, 210, 0)
RED = (255, 70, 70)

# =========================================================
# FONTS
# =========================================================

font = pygame.font.SysFont("Arial", 24, bold=True)
small_font = pygame.font.SysFont("Arial", 18, bold=True)
big_font = pygame.font.SysFont("Arial", 52, bold=True)

# =========================================================
# QUESTIONS
# =========================================================

QUESTIONS = [

    # SCIENCE
    {
        "category": "Science",
        "q": "What gas do plants absorb?",
        "a": "carbon dioxide",
        "h": "Used in photosynthesis"
    },

    {
        "category": "Science",
        "q": "Living and nonliving things together form an?",
        "a": "ecosystem",
        "h": "Starts with E"
    },

    # MATHEMATICS
    {
        "category": "Mathematics",
        "q": "Solve: 144 / 12",
        "a": "12",
        "h": "A dozen"
    },

    {
        "category": "Mathematics",
        "q": "Solve: 15 x 8",
        "a": "120",
        "h": "15 x 4 x 2"
    },

    # ECONOMICS
    {
        "category": "Economics",
        "q": "Human effort in production is called?",
        "a": "labor",
        "h": "L _ b _ r"
    },

    {
        "category": "Economics",
        "q": "Money earned from savings is?",
        "a": "interest",
        "h": "Starts with I"
    },

    # HISTORY
    {
        "category": "History",
        "q": "Who is the Father of Modern Bhutan?",
        "a": "jigme dorji wangchuck",
        "h": "The 3rd King"
    },

    {
        "category": "History",
        "q": "Bhutan National Day is celebrated in which month?",
        "a": "december",
        "h": "Last month"
    }
]

# =========================================================
# PLAYER
# =========================================================

class Player:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.walk = 0

    def rect(self):

        return pygame.Rect(self.x, self.y, 32, 42)

    def move(self, keys):

        moving = False

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= PLAYER_SPEED
            moving = True

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += PLAYER_SPEED
            moving = True

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= PLAYER_SPEED
            moving = True

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += PLAYER_SPEED
            moving = True

        if moving:
            self.walk += 0.15

        self.x = max(0, min(self.x, WORLD_SIZE))
        self.y = max(0, min(self.y, WORLD_SIZE))

    def draw(self, screen, cam_x, cam_y):

        px = self.x + cam_x
        py = self.y + cam_y

        bounce = math.sin(self.walk) * 1.5

        # SHADOW
        pygame.draw.ellipse(
            screen,
            (0, 0, 0),
            (px + 5, py + 34, 22, 8)
        )

        # LEGS
        pygame.draw.line(
            screen,
            BLACK,
            (px + 10, py + 25),
            (px + 10, py + 36 + bounce),
            3
        )

        pygame.draw.line(
            screen,
            BLACK,
            (px + 20, py + 25),
            (px + 20, py + 36 - bounce),
            3
        )

        # BODY
        pygame.draw.rect(
            screen,
            (40, 70, 200),
            (px, py + bounce, 30, 28),
            border_radius=8
        )

        # HEAD
        pygame.draw.circle(
            screen,
            (255, 220, 180),
            (int(px + 15), int(py - 2 + bounce)),
            12
        )

# =========================================================
# GAME
# =========================================================

class BrainTrek:

    def __init__(self):

        self.reset_game()

    # =====================================================
    # RESET GAME
    # =====================================================

    def reset_game(self):

        self.player = Player(
            WORLD_SIZE // 2,
            WORLD_SIZE // 2
        )

        self.cam_x = 0
        self.cam_y = 0

        self.gold = 0
        self.lives = START_LIVES

        self.state = "MENU"

        self.user_input = ""

        self.feedback = ""
        self.feedback_timer = 0

        self.hint_bought = False

        # =================================================
        # FOREST OBJECTS
        # =================================================

        self.trees = []

        for _ in range(700):

            self.trees.append((
                random.randint(0, WORLD_SIZE),
                random.randint(0, WORLD_SIZE),
                random.randint(45, 90)
            ))

        self.flowers = []

        for _ in range(2500):

            self.flowers.append((
                random.randint(0, WORLD_SIZE),
                random.randint(0, WORLD_SIZE),
                random.choice([
                    (255, 120, 120),
                    (255, 255, 120),
                    (255, 180, 255),
                    (120, 220, 255),
                    (255, 180, 90),
                    (255, 255, 255)
                ])
            ))

        self.grass = []

        for _ in range(4000):

            self.grass.append((
                random.randint(0, WORLD_SIZE),
                random.randint(0, WORLD_SIZE)
            ))

        self.rocks = []

        for _ in range(250):

            self.rocks.append((
                random.randint(0, WORLD_SIZE),
                random.randint(0, WORLD_SIZE),
                random.randint(10, 20)
            ))

        # =================================================
        # CHESTS
        # =================================================

        self.chests = []

        for _ in range(20):

            self.chests.append(
                pygame.Rect(
                    random.randint(100, WORLD_SIZE - 100),
                    random.randint(100, WORLD_SIZE - 100),
                    40,
                    30
                )
            )

    # =====================================================
    # START QUIZ
    # =====================================================

    def start_quiz(self):

        self.current_question = random.choice(QUESTIONS)

        self.user_input = ""

        self.hint_bought = False

        self.quiz_start = pygame.time.get_ticks()

        self.state = "QUIZ"

    # =====================================================
    # CORRECT ANSWER
    # =====================================================

    def correct_answer(self):

        self.gold += 1000

        self.feedback = "CORRECT! +1000 GOLD"

        self.feedback_timer = pygame.time.get_ticks()

        self.state = "PLAYING"

    # =====================================================
    # WRONG ANSWER
    # =====================================================

    def wrong_answer(self):

        self.lives -= 1

        self.feedback = "WRONG ANSWER! -1 LIFE"

        self.feedback_timer = pygame.time.get_ticks()

        self.state = "PLAYING"

        if self.lives <= 0:

            self.state = "GAMEOVER"

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self):

        keys = pygame.key.get_pressed()

        if self.state == "PLAYING":

            self.player.move(keys)

            self.cam_x = WIDTH // 2 - self.player.x
            self.cam_y = HEIGHT // 2 - self.player.y

            # CHEST COLLISION
            for chest in self.chests[:]:

                if self.player.rect().colliderect(chest):

                    self.chests.remove(chest)

                    self.start_quiz()

            # WIN
            if len(self.chests) == 0:

                self.state = "WIN"

        # QUIZ TIMER
        if self.state == "QUIZ":

            elapsed = (
                pygame.time.get_ticks() - self.quiz_start
            ) / 1000

            self.time_left = max(0, QUIZ_TIME - elapsed)

            if self.time_left <= 0:

                self.wrong_answer()

    # =====================================================
    # DRAW GROUND
    # =====================================================

    def draw_ground(self):

        tile = 64

        greens = [
            (60, 150, 60),
            (66, 160, 66),
            (72, 170, 72),
            (56, 145, 56)
        ]

        for x in range(0, WIDTH + tile, tile):

            for y in range(0, HEIGHT + tile, tile):

                c = greens[(x + y) // tile % len(greens)]

                pygame.draw.rect(
                    screen,
                    c,
                    (x, y, tile, tile)
                )

    # =====================================================
    # DRAW WORLD
    # =====================================================

    def draw_world(self):

        self.draw_ground()

        # =================================================
        # GRASS DETAILS
        # =================================================

        for g in self.grass:

            gx = g[0] + self.cam_x
            gy = g[1] + self.cam_y

            if -5 < gx < WIDTH + 5 and -5 < gy < HEIGHT + 5:

                pygame.draw.line(
                    screen,
                    (40, 130, 40),
                    (gx, gy),
                    (gx + 2, gy - 5),
                    1
                )

        # =================================================
        # FLOWERS
        # =================================================

        for flower in self.flowers:

            fx = flower[0] + self.cam_x
            fy = flower[1] + self.cam_y

            if -5 < fx < WIDTH + 5 and -5 < fy < HEIGHT + 5:

                pygame.draw.circle(
                    screen,
                    flower[2],
                    (int(fx), int(fy)),
                    2
                )

        # =================================================
        # ROCKS
        # =================================================

        for rock in self.rocks:

            rx = rock[0] + self.cam_x
            ry = rock[1] + self.cam_y

            if -40 < rx < WIDTH + 40 and -40 < ry < HEIGHT + 40:

                pygame.draw.circle(
                    screen,
                    (120, 120, 120),
                    (int(rx), int(ry)),
                    rock[2]
                )

                pygame.draw.circle(
                    screen,
                    (150, 150, 150),
                    (int(rx - 3), int(ry - 3)),
                    rock[2] - 4
                )

        # =================================================
        # TREES
        # =================================================

        for tree in self.trees:

            tx, ty, size = tree

            tx += self.cam_x
            ty += self.cam_y

            if -120 < tx < WIDTH + 120 and -120 < ty < HEIGHT + 120:

                # SHADOW
                pygame.draw.ellipse(
                    screen,
                    (0, 0, 0),
                    (tx + 12, ty + size - 8, size - 20, 18)
                )

                # TRUNK
                pygame.draw.rect(
                    screen,
                    (110, 70, 30),
                    (
                        tx + size//2 - 8,
                        ty + size - 18,
                        16,
                        32
                    )
                )

                # DARK LEAVES
                pygame.draw.circle(
                    screen,
                    (20, 90, 20),
                    (
                        int(tx + size//2),
                        int(ty + size//2)
                    ),
                    size//2
                )

                # MID LEAVES
                pygame.draw.circle(
                    screen,
                    (35, 130, 35),
                    (
                        int(tx + size//2 - 12),
                        int(ty + size//2 - 10)
                    ),
                    size//2 - 8
                )

                # LIGHT LEAVES
                pygame.draw.circle(
                    screen,
                    (60, 180, 60),
                    (
                        int(tx + size//2 + 10),
                        int(ty + size//2 - 12)
                    ),
                    size//2 - 16
                )

        # =================================================
        # CHESTS
        # =================================================

        for chest in self.chests:

            cx = chest.x + self.cam_x
            cy = chest.y + self.cam_y

            # SHADOW
            pygame.draw.ellipse(
                screen,
                BLACK,
                (cx + 4, cy + 25, 30, 8)
            )

            # BODY
            pygame.draw.rect(
                screen,
                (140, 90, 25),
                (cx, cy, 40, 28),
                border_radius=5
            )

            # TOP
            pygame.draw.rect(
                screen,
                GOLD,
                (cx + 2, cy + 2, 36, 13),
                border_radius=5
            )

            # LOCK
            pygame.draw.rect(
                screen,
                BLACK,
                (cx + 16, cy + 6, 8, 8)
            )

        # =================================================
        # PLAYER
        # =================================================

        self.player.draw(screen, self.cam_x, self.cam_y)

    # =====================================================
    # HUD
    # =====================================================

    def draw_hud(self):

        pygame.draw.rect(
            screen,
            BLACK,
            (0, 0, WIDTH, 65)
        )

        gold = font.render(
            f"GOLD: {self.gold}",
            True,
            GOLD
        )

        lives = font.render(
            f"LIVES: {self.lives}",
            True,
            RED
        )

        chests = font.render(
            f"CHESTS LEFT: {len(self.chests)}",
            True,
            WHITE
        )

        screen.blit(gold, (20, 18))
        screen.blit(lives, (220, 18))
        screen.blit(chests, (520, 18))

        if pygame.time.get_ticks() - self.feedback_timer < 2500:

            msg = font.render(
                self.feedback,
                True,
                WHITE
            )

            screen.blit(
                msg,
                (WIDTH//2 - msg.get_width()//2, 80)
            )

    # =====================================================
    # CONTROLS BAR
    # =====================================================

    def draw_controls(self):

        pygame.draw.rect(
            screen,
            BLACK,
            (0, HEIGHT - 60, WIDTH, 60)
        )

        move = small_font.render(
            "WASD = MOVE",
            True,
            WHITE
        )

        hint = small_font.render(
            "2 = BUY HINT (500 GOLD)",
            True,
            GOLD
        )

        enter = small_font.render(
            "ENTER = SUBMIT ANSWER",
            True,
            WHITE
        )

        restart = small_font.render(
            "R = RESTART",
            True,
            WHITE
        )

        screen.blit(move, (40, HEIGHT - 38))
        screen.blit(hint, (330, HEIGHT - 38))
        screen.blit(enter, (670, HEIGHT - 38))
        screen.blit(restart, (1040, HEIGHT - 38))

    # =====================================================
    # QUIZ BOX
    # =====================================================

    def draw_quiz(self):

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 190))

        screen.blit(overlay, (0, 0))

        box = pygame.Rect(180, 160, 920, 340)

        pygame.draw.rect(
            screen,
            (35, 35, 45),
            box,
            border_radius=20
        )

        pygame.draw.rect(
            screen,
            GOLD,
            box,
            3,
            border_radius=20
        )

        # CATEGORY
        cat = font.render(
            f"CATEGORY: {self.current_question['category']}",
            True,
            GOLD
        )

        screen.blit(cat, (240, 210))

        # QUESTION
        q = font.render(
            self.current_question["q"],
            True,
            WHITE
        )

        screen.blit(q, (240, 280))

        # HINT
        if self.hint_bought:

            hint = font.render(
                f"HINT: {self.current_question['h']}",
                True,
                (120, 255, 120)
            )

        else:

            hint = font.render(
                "PRESS 2 TO BUY HINT (-500 GOLD)",
                True,
                (180, 180, 180)
            )

        screen.blit(hint, (240, 340))

        # ANSWER
        ans = font.render(
            f"ANSWER: {self.user_input}",
            True,
            WHITE
        )

        screen.blit(ans, (240, 410))

        # TIMER
        timer = font.render(
            f"TIME LEFT: {int(self.time_left)}",
            True,
            RED
        )

        screen.blit(timer, (240, 460))

    # =====================================================
    # MENU
    # =====================================================

    def draw_menu(self):

        screen.fill((20, 20, 30))

        title = big_font.render(
            "BRAIN TREK",
            True,
            GOLD
        )

        sub = font.render(
            "REALISTIC FOREST EDITION",
            True,
            WHITE
        )

        start = font.render(
            "PRESS SPACE TO START",
            True,
            WHITE
        )

        screen.blit(
            title,
            (WIDTH//2 - title.get_width()//2, 220)
        )

        screen.blit(
            sub,
            (WIDTH//2 - sub.get_width()//2, 320)
        )

        screen.blit(
            start,
            (WIDTH//2 - start.get_width()//2, 420)
        )

    # =====================================================
    # GAME OVER
    # =====================================================

    def draw_gameover(self):

        screen.fill(BLACK)

        title = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        restart = font.render(
            "PRESS R TO RESTART",
            True,
            WHITE
        )

        screen.blit(
            title,
            (WIDTH//2 - title.get_width()//2, 260)
        )

        screen.blit(
            restart,
            (WIDTH//2 - restart.get_width()//2, 360)
        )

    # =====================================================
    # WIN
    # =====================================================

    def draw_win(self):

        screen.fill((25, 90, 40))

        title = big_font.render(
            "YOU WON!",
            True,
            GOLD
        )

        score = font.render(
            f"FINAL GOLD: {self.gold}",
            True,
            WHITE
        )

        restart = font.render(
            "PRESS R TO PLAY AGAIN",
            True,
            WHITE
        )

        screen.blit(
            title,
            (WIDTH//2 - title.get_width()//2, 240)
        )

        screen.blit(
            score,
            (WIDTH//2 - score.get_width()//2, 330)
        )

        screen.blit(
            restart,
            (WIDTH//2 - restart.get_width()//2, 420)
        )

    # =====================================================
    # MAIN LOOP
    # =====================================================

    def run(self):

        while True:

            clock.tick(FPS)

            # EVENTS
            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    pygame.quit()
                    sys.exit()

                # MENU
                if self.state == "MENU":

                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_SPACE:

                            self.state = "PLAYING"

                # QUIZ
                if self.state == "QUIZ":

                    if event.type == pygame.KEYDOWN:

                        # BUY HINT
                        if event.key == pygame.K_2:

                            if not self.hint_bought:

                                if self.gold >= HINT_COST:

                                    self.gold -= HINT_COST

                                    self.hint_bought = True

                                    self.feedback = "HINT PURCHASED"

                                else:

                                    self.feedback = "NOT ENOUGH GOLD"

                                self.feedback_timer = pygame.time.get_ticks()

                        # SUBMIT
                        elif event.key == pygame.K_RETURN:

                            if self.user_input.lower().strip() == self.current_question["a"]:

                                self.correct_answer()

                            else:

                                self.wrong_answer()

                        # DELETE
                        elif event.key == pygame.K_BACKSPACE:

                            self.user_input = self.user_input[:-1]

                        else:

                            self.user_input += event.unicode

                # RESTART
                if self.state in ["GAMEOVER", "WIN"]:

                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_r:

                            self.reset_game()

            # UPDATE
            self.update()

            # DRAW
            if self.state == "MENU":

                self.draw_menu()

            elif self.state in ["PLAYING", "QUIZ"]:

                self.draw_world()

                self.draw_hud()

                self.draw_controls()

                if self.state == "QUIZ":

                    self.draw_quiz()

            elif self.state == "GAMEOVER":

                self.draw_gameover()

            elif self.state == "WIN":

                self.draw_win()

            pygame.display.flip()

# =========================================================
# START GAME
# =========================================================

if __name__ == "__main__":

    game = BrainTrek()

    game.run()