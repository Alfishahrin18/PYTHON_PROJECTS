import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen setup with dimensions
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quiz-ul-Islam")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (180, 180, 180)
YELLOW = (255, 215, 0)
BLUE = (70, 130, 180)

# Fonts
font = pygame.font.SysFont("Arial", 32)
big_font = pygame.font.SysFont("Arial", 48)

# ------------------------------------
# LOAD LOGO (Large for Start Screen)
# ------------------------------------
try:
    logo = pygame.image.load("logo.jpeg")
    logo = pygame.transform.scale(logo, (200, 200))
except Exception:
    logo = None

# ------------------------------------
# LOAD SMALLER LOGO FOR QUESTION PAGES
# ------------------------------------
try:
    small_logo = pygame.image.load("logo.jpeg")
    small_logo = pygame.transform.scale(small_logo, (120, 120))  # << FIXED SIZE
except Exception:
    small_logo = None


# ---------------- CLASSES ----------------
class Question:
    def __init__(self, text, options, correct_answer, image_path=None, bg_path=None):
        self.text = text
        self.options = options
        self.correct_answer = correct_answer
        self.image_path = image_path
        self.bg_path = bg_path

    def is_correct(self, choice):
        return choice == self.correct_answer


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.level = 1

    def update_score(self, points):
        self.score += points

    def advance_level(self):
        self.level += 1


class QuizGame:
    def __init__(self, player, levels):
        self.player = player
        self.levels = levels
        self.current_level = 1
        self.current_index = 0
        self.questions = self.levels[self.current_level]
        self.buttons = []
        self.feedback = None

    def current_question(self):
        return self.questions[self.current_index]

    def next_question(self):
        self.current_index += 1
        self.feedback = None
        if self.current_index >= len(self.questions):
            return False
        return True

    def draw_question(self, question):
        # Draw question-specific background
        if question.bg_path:
            try:
                bg = pygame.image.load(question.bg_path)
                bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
                screen.blit(bg, (0, 0))
            except Exception:
                screen.fill(WHITE)
        else:
            screen.fill(WHITE)

        # Header bar
        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 80))
        header = font.render(f"Level {self.current_level}  |  Score: {self.player.score}", True, WHITE)
        screen.blit(header, (20, 25))

        # -------------------------
        # SMALL LOGO ON QUESTION PAGES
        # -------------------------
        if small_logo:
            screen.blit(small_logo, (WIDTH - 150, 500))  
        # -------------------------

        # Question text
        text_surface = font.render(question.text, True, BLACK)
        screen.blit(text_surface, (50, 120))

        # Optional question image
        if question.image_path:
            try:
                qimg = pygame.image.load(question.image_path)
                qimg = pygame.transform.scale(qimg, (220, 160))
                screen.blit(qimg, (WIDTH - 260, 360))
            except Exception:
                pass

        # Options as buttons
        self.buttons = []
        for i, option in enumerate(question.options):
            rect = pygame.Rect(100, 200 + i * 90, 700, 60)
            color = GRAY
            if self.feedback and self.feedback[1] == i:
                color = GREEN if self.feedback[0] == "correct" else RED

            pygame.draw.rect(screen, color, rect, border_radius=8)
            option_surface = font.render(option, True, BLACK)
            screen.blit(option_surface, (rect.x + 20, rect.y + 15))
            self.buttons.append((rect, option))

        pygame.display.update()

    def run_level(self):
        running = True
        while running:
            question = self.current_question()
            self.draw_question(question)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for idx, (rect, option) in enumerate(self.buttons):
                        if rect.collidepoint(mouse_pos):
                            if question.is_correct(option):
                                self.player.update_score(10)
                                self.feedback = ("correct", idx)
                            else:
                                self.feedback = ("wrong", idx)

                            self.draw_question(question)
                            pygame.time.wait(600)

                            if not self.next_question():
                                running = False

        show_level_complete(self.current_level, self.player.score)

    def run(self):
        for lvl in sorted(self.levels.keys()):
            self.current_level = lvl
            self.questions = self.levels[lvl]
            random.shuffle(self.questions)
            self.current_index = 0
            self.run_level()

            if self.player.score < lvl * 20:
                screen.fill(WHITE)
                fail_text = font.render(
                    f"Game Over! You did not qualify for Level {lvl + 1}. Final Score: {self.player.score}",
                    True, RED
                )
                screen.blit(fail_text, (50, 300))
                pygame.display.update()
                pygame.time.wait(3000)
                return

            self.player.advance_level()

        screen.fill(WHITE)
        end_text = big_font.render(f"Congratulations {self.player.name}!", True, GREEN)
        score_text = font.render(f"Final Score: {self.player.score}", True, BLACK)
        screen.blit(end_text, (WIDTH//2 - end_text.get_width()//2, 250))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 320))
        pygame.display.update()
        pygame.time.wait(4000)


# ---------------- START SCREEN ----------------
def show_start_screen():
    screen.fill(WHITE)

    if logo:
        screen.blit(logo, (WIDTH // 2 - 100, 50))

    title = big_font.render("Quiz-ul-Islam", True, BLACK)
    subtitle = font.render("Learn Islam the Fun Way!", True, GREEN)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 300))
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 360))

    start_button = pygame.Rect(WIDTH // 2 - 120, 450, 240, 70)
    pygame.draw.rect(screen, YELLOW, start_button, border_radius=10)
    start_text = font.render("Start Quiz", True, BLACK)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 470))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    waiting = False


# ---------------- LEVEL COMPLETE SCREEN ----------------
def show_level_complete(level, score):
    screen.fill(WHITE)

    header = big_font.render(f"Level {level} Complete!", True, YELLOW)
    score_text = font.render(f"Your Score: {score}", True, BLACK)
    screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 250))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 320))

    next_button = pygame.Rect(WIDTH // 2 - 120, 450, 240, 70)
    pygame.draw.rect(screen, GREEN, next_button, border_radius=10)
    next_text = font.render("Next Level", True, BLACK)
    screen.blit(next_text, (WIDTH // 2 - next_text.get_width() // 2, 470))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_button.collidepoint(event.pos):
                    waiting = False


# ---------------- QUESTION BANK ----------------
levels = {
    1: [
        Question("Who was the last Prophet in Islam?",
                 ["Prophet Musa", "Prophet Isa", "Prophet Muhammad (SAW)", "Prophet Ibrahim"],
                 "Prophet Muhammad (SAW)",
                 bg_path="prophet_bg.jpeg"),
        Question("Which city is called the heart of Islam?",
                 ["Medina", "Mecca", "Jerusalem", "Baghdad"],
                 "Mecca",
                 bg_path="mecca_bg.jpeg"),
        Question("How many pillars of Islam are there?",
                 ["3", "4", "5", "6"],
                 "5",
                 bg_path="pillars_bg.jpeg"),
        Question("What is the holy book of Islam?",
                 ["Torah", "Bible", "Quran", "Zabur"],
                 "Quran",
                 bg_path="quran_bg.jpeg"),
        Question("Which pillar involves fasting?",
                 ["Shahada", "Salah", "Sawm", "Zakat"],
                 "Sawm",
                 bg_path="fasting_bg.jpeg")
    ],
    2: [
        Question("Which month do Muslims fast?",
                 ["Rajab", "Ramadan", "Muharram", "Shaban"],
                 "Ramadan",
                 bg_path="ramadan_bg.jpeg"),
        Question("Where did the Prophet (SAW) migrate to from Mecca?",
                 ["Taif", "Medina", "Jerusalem", "Baghdad"],
                 "Medina",
                 bg_path="medina_bg.jpeg"),
        Question("What is the first pillar of Islam?",
                 ["Shahada", "Salah", "Zakat", "Hajj"],
                 "Shahada",
                 bg_path="shahada_bg.jpeg"),
        Question("How many daily prayers are obligatory?",
                 ["3", "4", "5", "6"],
                 "5",
                 bg_path="salah_bg.jpeg"),
        Question("What is the charity given by Muslims called?",
                 ["Sadaqah", "Zakat", "Kaffarah", "Fitrah"],
                 "Zakat",
                 bg_path="zakat_bg.jpeg")
    ],
    3: [
        Question("Which angel brought revelation to the Prophet (SAW)?",
                 ["Mikail", "Israfil", "Jibreel", "Azrael"],
                 "Jibreel",
                 bg_path="jibreel_bg.jpeg"),
        Question("What is the pilgrimage to Mecca called?",
                 ["Umrah", "Hajj", "Tawaf", "Salah"],
                 "Hajj",
                 bg_path="hajj_bg.jpeg"),
        Question("Which battle was the first major battle in Islam?",
                 ["Battle of Uhud", "Battle of Badr", "Battle of Khandaq", "Battle of Hunayn"],
                 "Battle of Badr",
                 bg_path="badr_bg.jpeg"),
        Question("What is the night of power in Ramadan called?",
                 ["Laylat al-Qadr", "Laylat al-Miraj", "Laylat al-Baraat", "Laylat al-Isra"],
                 "Laylat al-Qadr",
                 bg_path="qadr_bg.jpeg"),
        Question("Which city contains the Kaaba?",
                 ["Mecca", "Medina", "Jerusalem", "Cairo"],
                 "Mecca",
                 bg_path="kaaba_bg.jpeg")
    ]
}

# ---------------- MAIN ----------------
def main():
    player = Player("Jannatul")
    show_start_screen()
    game = QuizGame(player, levels)
    game.run()

if __name__ == "__main__":
    main()

