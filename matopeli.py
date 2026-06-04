import pygame
import sys
import random
import json
import os
from enum import Enum

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Matopeli - Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # High score system
        self.high_scores_file = "snake_scores.json"
        self.high_scores = self.load_high_scores()
        self.new_high_score = False
        
        self.reset_game()
    
    def reset_game(self):
        # Initialize snake in the center of the screen
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        self.snake = [(center_x, center_y)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        
        # Reset game state
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.new_high_score = False
    
    def generate_food(self):
        while True:
            food_pos = (random.randint(0, GRID_WIDTH - 1), 
                       random.randint(0, GRID_HEIGHT - 1))
            if food_pos not in self.snake:
                return food_pos
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    # Handle direction changes
                    if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                        self.next_direction = Direction.UP
                    elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                        self.next_direction = Direction.DOWN
                    elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                        self.next_direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                        self.next_direction = Direction.RIGHT
                    elif event.key == pygame.K_ESCAPE:
                        return False
        return True
    
    def update(self):
        if self.game_over:
            return
        
        # Update direction
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.game_over = True
            self.update_high_scores(self.score)
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            self.update_high_scores(self.score)
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def draw(self):
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw grid lines (optional)
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y), 1)
        
        # Draw snake
        for i, segment in enumerate(self.snake):
            x = segment[0] * GRID_SIZE
            y = segment[1] * GRID_SIZE
            color = GREEN if i == 0 else BLUE  # Head is green, body is blue
            pygame.draw.rect(self.screen, color, (x, y, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(self.screen, WHITE, (x, y, GRID_SIZE, GRID_SIZE), 1)
        
        # Draw food
        food_x = self.food[0] * GRID_SIZE
        food_y = self.food[1] * GRID_SIZE
        pygame.draw.rect(self.screen, RED, (food_x, food_y, GRID_SIZE, GRID_SIZE))
        
        # Draw score and high scores
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw high scores
        high_score_title = self.small_font.render("High Scores:", True, WHITE)
        self.screen.blit(high_score_title, (10, 50))
        
        for i, score in enumerate(self.high_scores):
            rank_text = self.small_font.render(f"{i+1}. {score}", True, WHITE)
            self.screen.blit(rank_text, (10, 75 + i * 20))
        
        # Draw high scores
        for i, score in enumerate(self.high_scores):
            high_score_text = self.small_font.render(f"{i+1}. {score}", True, WHITE)
            self.screen.blit(high_score_text, (WINDOW_WIDTH - 100, 10 + i * 30))
        
        # Draw game over screen
        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Game over text
            if self.new_high_score:
                game_over_text = self.font.render("NEW HIGH SCORE!", True, RED)
            else:
                game_over_text = self.font.render("GAME OVER", True, RED)
            
            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            
            # High scores list
            high_scores_title = self.small_font.render("High Scores:", True, WHITE)
            
            restart_text = self.small_font.render("Press SPACE to restart or ESC to quit", True, WHITE)
            
            # Center the text
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 80))
            final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 40))
            high_scores_title_rect = high_scores_title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 10))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 60))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(final_score_text, final_score_rect)
            self.screen.blit(high_scores_title, high_scores_title_rect)
            
            # Draw high scores list in game over screen
            for i, score in enumerate(self.high_scores):
                color = RED if score == self.score and self.new_high_score else WHITE
                score_text = self.small_font.render(f"{i+1}. {score}", True, color)
                score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 15 + i * 15))
                self.screen.blit(score_text, score_rect)
            
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def load_high_scores(self):
        """Load high scores from file, return default if file doesn't exist"""
        try:
            if os.path.exists(self.high_scores_file):
                with open(self.high_scores_file, 'r') as f:
                    scores = json.load(f)
                    # Ensure we have exactly 3 scores
                    while len(scores) < 3:
                        scores.append(0)
                    return scores[:3]  # Keep only top 3
            else:
                return [0, 0, 0]  # Default scores
        except:
            return [0, 0, 0]  # Return default if file is corrupted
    
    def save_high_scores(self):
        """Save high scores to file"""
        try:
            with open(self.high_scores_file, 'w') as f:
                json.dump(self.high_scores, f)
        except:
            pass  # Ignore save errors
    
    def update_high_scores(self, score):
        """Update high scores list with new score"""
        self.high_scores.append(score)
        self.high_scores.sort(reverse=True)  # Sort in descending order
        self.high_scores = self.high_scores[:3]  # Keep only top 3
        
        # Check if this is a new high score (in top 3)
        self.new_high_score = score in self.high_scores and score > 0
        
        self.save_high_scores()
    
    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(10)  # 10 FPS for snake game
        
        pygame.quit()
        sys.exit()

def main():
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main()