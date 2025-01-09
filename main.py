import pygame
import random

# Screen dimensions and colors
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

def main():
    pygame.init()

    # Set up screen and clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ping Pong Game")
    clock = pygame.time.Clock()

    started = False

    # Define paddles and ball
    paddle_1_rect = pygame.Rect(30, SCREEN_HEIGHT / 2 - 50, 7, 100)
    paddle_2_rect = pygame.Rect(SCREEN_WIDTH - 50, SCREEN_HEIGHT / 2 - 50, 7, 100)
    paddle_1_move = 0
    paddle_2_move = 0
    ball_rect = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 25, 25)

    # Ball speed
    ball_acc_x = random.choice([-0.3, 0.3])
    ball_acc_y = random.choice([-0.3, 0.3])

    # Game loop
    while True:
        screen.fill(COLOR_BLACK)

        # Display start message
        if not started:
            font = pygame.font.SysFont('Consolas', 30)
            text = font.render('Press Space to Start', True, COLOR_WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        started = True
            continue

        delta_time = clock.tick(60)  # Run game at 60 FPS

        # Handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    paddle_1_move = -0.5
                if event.key == pygame.K_s:
                    paddle_1_move = 0.5
                if event.key == pygame.K_UP:
                    paddle_2_move = -0.5
                if event.key == pygame.K_DOWN:
                    paddle_2_move = 0.5
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_w, pygame.K_s]:
                    paddle_1_move = 0
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    paddle_2_move = 0

        # Update paddle positions
        paddle_1_rect.top += paddle_1_move * delta_time
        paddle_2_rect.top += paddle_2_move * delta_time

        # Restrict paddle movements within the screen
        paddle_1_rect.top = max(0, min(paddle_1_rect.top, SCREEN_HEIGHT - paddle_1_rect.height))
        paddle_2_rect.top = max(0, min(paddle_2_rect.top, SCREEN_HEIGHT - paddle_2_rect.height))

        # Ball movement
        ball_rect.left += ball_acc_x * delta_time
        ball_rect.top += ball_acc_y * delta_time

        # Ball collision with top and bottom
        if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
            ball_acc_y *= -1

        # Ball collision with paddles
        if paddle_1_rect.colliderect(ball_rect):
            ball_acc_x *= -1
            ball_rect.left = paddle_1_rect.right
        if paddle_2_rect.colliderect(ball_rect):
            ball_acc_x *= -1
            ball_rect.right = paddle_2_rect.left

        # Ball out of bounds
        if ball_rect.left <= 0 or ball_rect.right >= SCREEN_WIDTH:
            # Reset ball and paddles
            ball_rect = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 25, 25)
            ball_acc_x = random.choice([-0.3, 0.3])
            ball_acc_y = random.choice([-0.3, 0.3])
            started = False

        # Draw paddles and ball
        pygame.draw.rect(screen, COLOR_WHITE, paddle_1_rect)
        pygame.draw.rect(screen, COLOR_WHITE, paddle_2_rect)
        pygame.draw.ellipse(screen, COLOR_WHITE, ball_rect)

        # Update display
        pygame.display.update()

if __name__ == '__main__':
    main()