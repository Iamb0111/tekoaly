import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15
PADDLE_SPEED = 5
BALL_SPEED_X = 4
BALL_SPEED_Y = 4

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = PADDLE_SPEED
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    def move_up(self):
        if self.y > 0:
            self.y -= self.speed
            self.rect.y = self.y
    
    def move_down(self):
        if self.y < WINDOW_HEIGHT - PADDLE_HEIGHT:
            self.y += self.speed
            self.rect.y = self.y
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.speed_x = BALL_SPEED_X * random.choice([-1, 1])
        self.speed_y = BALL_SPEED_Y * random.choice([-1, 1])
        self.rect = pygame.Rect(self.x, self.y, BALL_SIZE, BALL_SIZE)
    
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Bounce off top and bottom walls
        if self.y <= 0 or self.y >= WINDOW_HEIGHT - BALL_SIZE:
            self.speed_y = -self.speed_y
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class PongGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 72)
        self.score_font = pygame.font.Font(None, 36)
        
        # Create paddles
        self.left_paddle = Paddle(20, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(WINDOW_WIDTH - 20 - PADDLE_WIDTH, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        
        # Create ball
        self.ball = Ball()
        
        # Scores
        self.left_score = 0
        self.right_score = 0
        
        # Game state
        self.game_paused = False
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Right paddle controls (UP/DOWN arrows)
        if keys[pygame.K_UP]:
            self.right_paddle.move_up()
        if keys[pygame.K_DOWN]:
            self.right_paddle.move_down()
        
        # AI controls for left paddle
        self.update_ai_paddle()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.game_paused = not self.game_paused
                elif event.key == pygame.K_r:
                    self.reset_game()
        
        return True
    
    def update_ai_paddle(self):
        # AI follows the ball with some reaction delay and occasional mistakes
        paddle_center = self.left_paddle.y + PADDLE_HEIGHT // 2
        ball_center = self.ball.y + BALL_SIZE // 2
        
        # Add some difficulty adjustment - AI isn't perfect
        ai_speed = PADDLE_SPEED * 0.7  # Make AI slower than player
        
        # Add randomness - AI makes mistakes occasionally
        mistake_chance = random.random()
        
        # AI sometimes moves in wrong direction or doesn't move at all
        if mistake_chance < 0.05:  # 5% chance to move wrong direction
            if paddle_center < ball_center - 15:
                # Move wrong way (up instead of down)
                if self.left_paddle.y > 0:
                    self.left_paddle.y -= ai_speed
                    self.left_paddle.rect.y = self.left_paddle.y
            elif paddle_center > ball_center + 15:
                # Move wrong way (down instead of up)
                if self.left_paddle.y < WINDOW_HEIGHT - PADDLE_HEIGHT:
                    self.left_paddle.y += ai_speed
                    self.left_paddle.rect.y = self.left_paddle.y
        elif mistake_chance < 0.15:  # 10% chance to not move at all (freeze)
            pass  # Do nothing - AI "freezes" for this frame
        else:  # Normal AI behavior 85% of the time
            if paddle_center < ball_center - 15:  # Larger dead zone for more realistic play
                if self.left_paddle.y < WINDOW_HEIGHT - PADDLE_HEIGHT:
                    self.left_paddle.y += ai_speed
                    self.left_paddle.rect.y = self.left_paddle.y
            elif paddle_center > ball_center + 15:
                if self.left_paddle.y > 0:
                    self.left_paddle.y -= ai_speed
                    self.left_paddle.rect.y = self.left_paddle.y
    
    def update(self):
        if self.game_paused:
            return
        
        # Move ball
        self.ball.move()
        
        # Check paddle collisions
        if self.ball.rect.colliderect(self.left_paddle.rect):
            if self.ball.speed_x < 0:  # Only bounce if moving towards paddle
                self.ball.speed_x = -self.ball.speed_x
                # Add some spin based on where ball hits paddle
                hit_pos = (self.ball.y - self.left_paddle.y) / PADDLE_HEIGHT
                self.ball.speed_y += (hit_pos - 0.5) * 2
        
        if self.ball.rect.colliderect(self.right_paddle.rect):
            if self.ball.speed_x > 0:  # Only bounce if moving towards paddle
                self.ball.speed_x = -self.ball.speed_x
                # Add some spin based on where ball hits paddle
                hit_pos = (self.ball.y - self.right_paddle.y) / PADDLE_HEIGHT
                self.ball.speed_y += (hit_pos - 0.5) * 2
        
        # Check if ball goes off screen (scoring)
        if self.ball.x < 0:
            self.right_score += 1
            self.ball.reset()
        elif self.ball.x > WINDOW_WIDTH:
            self.left_score += 1
            self.ball.reset()
    
    def reset_game(self):
        self.left_score = 0
        self.right_score = 0
        self.ball.reset()
        self.game_paused = False
    
    def draw(self):
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw center line
        for y in range(0, WINDOW_HEIGHT, 20):
            pygame.draw.rect(self.screen, GRAY, (WINDOW_WIDTH // 2 - 2, y, 4, 10))
        
        # Draw paddles and ball
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        
        # Draw scores
        left_score_text = self.font.render(str(self.left_score), True, WHITE)
        right_score_text = self.font.render(str(self.right_score), True, WHITE)
        
        self.screen.blit(left_score_text, (WINDOW_WIDTH // 4, 50))
        self.screen.blit(right_score_text, (3 * WINDOW_WIDTH // 4, 50))
        
        # Draw controls text
        if self.game_paused:
            pause_text = self.score_font.render("PAUSED - Press SPACE to continue", True, WHITE)
            pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(pause_text, pause_rect)
        
        controls_text = self.score_font.render("AI Player | Player: UP/DOWN | SPACE: Pause | R: Reset | ESC: Quit", True, GRAY)
        controls_rect = controls_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
        self.screen.blit(controls_text, controls_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

def main():
    game = PongGame()
    game.run()

if __name__ == "__main__":
    main()