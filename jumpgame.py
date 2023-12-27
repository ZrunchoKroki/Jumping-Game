import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
GROUND_Y = HEIGHT - 50
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Скок подскок")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Player variables
player_width, player_height = 50, 50
player_x, player_y = 100, GROUND_Y - player_height
player_velocity = 0
jump = False

# Obstacle variables
obstacle_width, obstacle_height = 30, 50
obstacle_x = WIDTH
obstacle_y = GROUND_Y - obstacle_height

# Game variables
score = 0
font = pygame.font.Font(None, 36)
game_over = False

# Functions
def draw_player():
    pygame.draw.rect(window, WHITE, (player_x, player_y, player_width, player_height))

def draw_obstacle():
    pygame.draw.rect(window, WHITE, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))

def update_obstacle():
    global obstacle_x, score
    obstacle_x -= 5
    if obstacle_x < -obstacle_width:
        obstacle_x = WIDTH
        score += 1

def check_collision():
    if player_x < obstacle_x + obstacle_width and player_x + player_width > obstacle_x and player_y < obstacle_y + obstacle_height and player_y + player_height > obstacle_y:
        return True
    return False

def show_game_over_popup():
    global game_over, player_x, player_y, player_velocity, jump, obstacle_x, score
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Try Again - Restart Game
                    # Reset game variables
                    player_x, player_y = 100, GROUND_Y - player_height
                    player_velocity = 0
                    jump = False
                    obstacle_x = WIDTH
                    score = 0
                    game_over = False  # Exit the game over loop and restart the game
                elif event.key == pygame.K_ESCAPE:  # Exit Game
                    pygame.quit()
                    sys.exit()

        window.fill(BLACK)
        game_over_text = font.render("Край на играта!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70))
        window.blit(game_over_text, game_over_rect)

        score_text = font.render(f"Резултат: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        window.blit(score_text, score_rect)

        try_again_text = font.render("Натиснете Enter за да опитате отново", True, WHITE)
        try_again_rect = try_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        window.blit(try_again_text, try_again_rect)

        exit_text = font.render("Натиснете ESC за да затворите играта", True, WHITE)
        exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        window.blit(exit_text, exit_rect)

        pygame.display.update()
        clock.tick(FPS)

# Game loop
running = True
while running:
    window.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jump:
                jump = True
                player_velocity = -10

    if not game_over:
        if jump:
            player_y += player_velocity
            player_velocity += 0.5

            if player_y >= GROUND_Y - player_height:
                player_y = GROUND_Y - player_height
                jump = False

        window.blit(font.render(f"Резултат: {score}", True, WHITE), (10, 10))

        draw_player()
        draw_obstacle()
        update_obstacle()

        if check_collision():
            show_game_over_popup()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()

