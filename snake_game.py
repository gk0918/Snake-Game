import pygame
import random
import sys

# ---------- SETTINGS ----------
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
FPS = 60

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 180, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)

# ---------- INIT ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Modern Snake Game 🐍")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)
big_font = pygame.font.SysFont("consolas", 48)

# ---------- SOUND (OPTIONAL) ----------
try:
    eat_sound = pygame.mixer.Sound("sounds/eat.wav")
    gameover_sound = pygame.mixer.Sound("sounds/gameover.wav")
except:
    eat_sound = gameover_sound = None

# ---------- FUNCTIONS ----------
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def random_food():
    x = random.randrange(0, WIDTH, CELL_SIZE)
    y = random.randrange(0, HEIGHT, CELL_SIZE)
    return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

def draw_text(text, font, color, x, y, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)

# ---------- MAIN GAME ----------
def main():
    snake = [
        pygame.Rect(300, 300, CELL_SIZE, CELL_SIZE),
        pygame.Rect(280, 300, CELL_SIZE, CELL_SIZE),
        pygame.Rect(260, 300, CELL_SIZE, CELL_SIZE)
    ]

    direction = pygame.Vector2(1, 0)
    food = random_food()
    score = 0
    level = 1
    speed = 10

    game_over = False

    move_timer = 0
    move_delay = 120  # milliseconds

    while True:
        dt = clock.tick(FPS)
        move_timer += dt

        # ---------- EVENTS ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP and direction.y != 1:
                        direction = pygame.Vector2(0, -1)
                    elif event.key == pygame.K_DOWN and direction.y != -1:
                        direction = pygame.Vector2(0, 1)
                    elif event.key == pygame.K_LEFT and direction.x != 1:
                        direction = pygame.Vector2(-1, 0)
                    elif event.key == pygame.K_RIGHT and direction.x != -1:
                        direction = pygame.Vector2(1, 0)
                else:
                    if event.key == pygame.K_SPACE:
                        main()

        # ---------- UPDATE ----------
        if not game_over and move_timer >= move_delay:
            move_timer = 0

            new_head = snake[0].copy()
            new_head.x += int(direction.x * CELL_SIZE)
            new_head.y += int(direction.y * CELL_SIZE)

            # Wall collision
            if (
                new_head.left < 0 or new_head.right > WIDTH or
                new_head.top < 0 or new_head.bottom > HEIGHT
            ):
                game_over = True
                if gameover_sound:
                    gameover_sound.play()

            # Self collision
            if new_head in snake:
                game_over = True
                if gameover_sound:
                    gameover_sound.play()

            snake.insert(0, new_head)

            # Food collision
            if new_head.colliderect(food):
                score += 10
                if eat_sound:
                    eat_sound.play()
                food = random_food()

                if score % 50 == 0:
                    level += 1
                    move_delay = max(50, move_delay - 10)
            else:
                snake.pop()

        # ---------- DRAW ----------
        screen.fill(BLACK)
        draw_grid()

        # Food
        pygame.draw.rect(screen, RED, food)

        # Snake
        for i, part in enumerate(snake):
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(screen, color, part)

        # UI
        draw_text(f"Score: {score}", font, WHITE, 10, 10)
        draw_text(f"Level: {level}", font, WHITE, 10, 40)

        if game_over:
            draw_text("GAME OVER", big_font, RED, WIDTH // 2, HEIGHT // 2 - 30, True)
            draw_text("Press SPACE to Restart", font, WHITE, WIDTH // 2, HEIGHT // 2 + 20, True)

        pygame.display.flip()

# ---------- RUN ----------
if __name__ == "__main__":
    main()

