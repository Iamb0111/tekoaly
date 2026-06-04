import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
GRAVITY = 0.6  # Reduced gravity for easier jumping
JUMP_STRENGTH = -16  # Stronger jump
PLAYER_SPEED = 6  # Faster movement
WALL_JUMP_STRENGTH = -14  # Stronger wall jump
SLIDE_FRICTION = 0.95

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 30
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.on_wall = False
        self.wall_direction = 0  # -1 for left wall, 1 for right wall
        self.sliding = False
        self.wall_jump_timer = 0
        self.can_double_jump = True
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def update(self, platforms, walls):
        # Handle input
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
        else:
            self.vel_x *= 0.85  # Better friction control
        
        # Sliding
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.on_ground and abs(self.vel_x) > 2:
                self.sliding = True
                self.vel_x *= SLIDE_FRICTION
                self.height = 15  # Make player shorter when sliding
        else:
            self.sliding = False
            if self.height < 30:
                self.height = 30
        
        # Wall jump timer
        if self.wall_jump_timer > 0:
            self.wall_jump_timer -= 1
        
        # Apply gravity
        if not self.on_ground:
            self.vel_y += GRAVITY
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Update rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Collision detection
        self.on_ground = False
        self.on_wall = False
        
        # Platform collisions
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Top collision (landing on platform)
                if self.vel_y > 0 and self.y < platform.y:
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    self.can_double_jump = True
                # Bottom collision (hitting platform from below)
                elif self.vel_y < 0 and self.y > platform.y:
                    self.y = platform.y + platform.height
                    self.vel_y = 0
                # Side collisions
                elif self.vel_x > 0:  # Moving right
                    self.x = platform.x - self.width
                    self.vel_x = 0
                elif self.vel_x < 0:  # Moving left
                    self.x = platform.x + platform.width
                    self.vel_x = 0
        
        # Wall collisions
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if not self.on_ground and abs(self.vel_y) > 0.5:  # Easier wall grab
                    if self.x < wall.x:  # Player on left side of wall
                        self.x = wall.x - self.width
                        self.on_wall = True
                        self.wall_direction = 1
                        self.vel_y *= 0.5  # Slower wall slide
                        if self.vel_y > 2:  # Slower max wall slide speed
                            self.vel_y = 2
                        self.can_double_jump = True  # Reset double jump on wall
                    else:  # Player on right side of wall
                        self.x = wall.x + wall.width
                        self.on_wall = True
                        self.wall_direction = -1
                        self.vel_y *= 0.5
                        if self.vel_y > 2:
                            self.vel_y = 2
                        self.can_double_jump = True  # Reset double jump on wall
        
        # Screen boundaries
        if self.x < 0:
            self.x = 0
            self.vel_x = 0
        elif self.x > WINDOW_WIDTH - self.width:
            self.x = WINDOW_WIDTH - self.width
            self.vel_x = 0
            
        if self.y > WINDOW_HEIGHT:
            # Reset player position if they fall off screen
            self.x = 50
            self.y = 400
            self.vel_x = 0
            self.vel_y = 0
    
    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
        elif self.can_double_jump and not self.on_wall:
            self.vel_y = JUMP_STRENGTH * 0.85  # Better double jump
            self.can_double_jump = False
        elif self.on_wall and self.wall_jump_timer <= 0:
            self.vel_y = WALL_JUMP_STRENGTH
            self.vel_x = self.wall_direction * PLAYER_SPEED * 2  # Stronger wall jump push
            self.wall_jump_timer = 15  # Longer timer for better control
            self.on_wall = False
            self.can_double_jump = True

    def draw(self, screen):
        # Player color based on state
        if self.on_wall:
            color = ORANGE  # Orange when wall sliding
        elif self.sliding:
            color = PURPLE  # Purple when sliding
        elif not self.on_ground and not self.on_wall:
            color = RED  # Red when in air
        else:
            color = BLUE  # Blue when on ground
        
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

class Platform:
    def __init__(self, x, y, width, height, platform_type="normal"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = platform_type
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen):
        if self.type == "normal":
            color = BROWN
        elif self.type == "moving":
            color = GREEN
        elif self.type == "breakable":
            color = YELLOW
        else:
            color = GRAY
            
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

class Wall:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, DARK_GRAY, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

class Obstacle:
    def __init__(self, x, y, width, height, obstacle_type="spike"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = obstacle_type
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen):
        if self.type == "spike":
            # Draw triangular spikes
            points = []
            num_spikes = self.width // 20
            for i in range(num_spikes):
                spike_x = self.x + i * 20
                points.extend([
                    (spike_x, self.y + self.height),
                    (spike_x + 10, self.y),
                    (spike_x + 20, self.y + self.height)
                ])
            if points:
                pygame.draw.polygon(screen, RED, points)
        else:
            pygame.draw.rect(screen, RED, self.rect)

class Collectible:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 15
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.collected = False
        self.bounce = 0
    
    def update(self):
        self.bounce += 0.2
    
    def draw(self, screen):
        if not self.collected:
            bounce_offset = math.sin(self.bounce) * 3
            draw_y = self.y + bounce_offset
            pygame.draw.circle(screen, YELLOW, (self.x + self.width//2, int(draw_y + self.height//2)), self.width//2)
            pygame.draw.circle(screen, WHITE, (self.x + self.width//2, int(draw_y + self.height//2)), self.width//2, 2)

class ParkourGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Parkour Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 48)
        
        # Game state
        self.running = True
        self.score = 0
        self.level = 1
        self.time_survived = 0  # Track time for progressive difficulty
        self.difficulty_modifier = 0  # Increases over time
        self.show_difficulty_message = 0  # Timer for difficulty increase message
        self.skips_remaining = 3  # Player can skip only 3 levels
        self.game_state = "playing"  # "playing", "leaderboard"
        self.high_scores = self.load_high_scores()  # Load saved high scores
        
        # Initialize game objects
        self.player = Player(50, 400)
        self.platforms = []
        self.walls = []
        self.obstacles = []
        self.collectibles = []
        
        self.create_level()
    
    def format_time(self, frames):
        """Convert frames to hours, minutes, seconds format (60 FPS)"""
        total_seconds = frames // 60  # Convert frames to seconds (60 FPS)
        
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours}t {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    def load_high_scores(self):
        """Load high scores from file, return list of [level, time, score, name] tuples"""
        try:
            with open("parkour_highscores.txt", "r") as f:
                scores = []
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 4:  # New format: level,time,score,name
                        scores.append([int(parts[0]), int(parts[1]), int(parts[2]), parts[3]])
                    elif len(parts) == 3:  # Old format: level,time,name (backwards compatibility)
                        scores.append([int(parts[0]), int(parts[1]), 0, parts[2]])  # Score = 0 for old scores
                    elif len(parts) == 2:  # Oldest format: level,name
                        scores.append([int(parts[0]), 0, 0, parts[1]])  # Time = 0, Score = 0 for old scores
                return scores
        except FileNotFoundError:
            return []  # No file yet, start with empty list
    
    def save_high_scores(self):
        """Save high scores to file"""
        with open("parkour_highscores.txt", "w") as f:
            for level, time, score, name in self.high_scores:
                f.write(f"{level},{time},{score},{name}\n")
    
    def add_high_score(self, level, time, score, name):
        """Add new score and keep only top 3"""
        self.high_scores.append([level, time, score, name])
        # Sort by level (highest first)
        self.high_scores.sort(key=lambda x: x[0], reverse=True)
        # Keep only top 3
        self.high_scores = self.high_scores[:3]
        self.save_high_scores()
    
    def is_high_score(self, level):
        """Check if level qualifies for top 3"""
        if len(self.high_scores) < 3:
            return True
        return level > self.high_scores[-1][0]  # Better than worst score

    def create_level(self):
        # Clear existing objects
        self.platforms.clear()
        self.walls.clear()
        self.obstacles.clear()
        self.collectibles.clear()
        
        # Ground platform
        self.platforms.append(Platform(0, WINDOW_HEIGHT - 40, WINDOW_WIDTH, 40))
        
        # Level 1 platforms and obstacles
        if self.level == 1:
            # Easier starting platforms with better spacing
            self.platforms.append(Platform(150, 480, 120, 20))
            self.platforms.append(Platform(320, 420, 120, 20))
            self.platforms.append(Platform(500, 360, 120, 20))
            self.platforms.append(Platform(680, 300, 120, 20))
            self.platforms.append(Platform(850, 240, 120, 20))
            
            # Wall for wall jumping - positioned better
            self.walls.append(Wall(950, 100, 30, 300))
            
            # Fewer, better placed spikes
            self.obstacles.append(Obstacle(280, WINDOW_HEIGHT - 60, 30, 20))
            self.obstacles.append(Obstacle(470, WINDOW_HEIGHT - 60, 30, 20))
            
            # Collectibles on platforms
            self.collectibles.append(Collectible(190, 450))
            self.collectibles.append(Collectible(360, 390))
            self.collectibles.append(Collectible(540, 330))
            self.collectibles.append(Collectible(720, 270))
            self.collectibles.append(Collectible(890, 210))
        
        # More complex levels
        elif self.level == 2:
            # Better spaced platforms
            self.platforms.append(Platform(120, 480, 100, 20))
            self.platforms.append(Platform(280, 420, 80, 20))
            self.platforms.append(Platform(420, 360, 100, 20))
            self.platforms.append(Platform(580, 300, 80, 20))
            self.platforms.append(Platform(720, 240, 100, 20))
            self.platforms.append(Platform(860, 180, 100, 20))
            
            # Better positioned walls
            self.walls.append(Wall(400, 200, 30, 200))
            self.walls.append(Wall(700, 100, 30, 200))
            self.walls.append(Wall(950, 50, 30, 300))
            
            # Fewer obstacles, better placement
            self.obstacles.append(Obstacle(250, WINDOW_HEIGHT - 60, 40, 20))
            self.obstacles.append(Obstacle(550, WINDOW_HEIGHT - 60, 30, 20))
            
            # More collectibles
            self.collectibles.append(Collectible(160, 450))
            self.collectibles.append(Collectible(320, 390))
            self.collectibles.append(Collectible(460, 330))
            self.collectibles.append(Collectible(620, 270))
            self.collectibles.append(Collectible(760, 210))
            self.collectibles.append(Collectible(900, 150))
        
        else:
            # Generate easier random level
            self.generate_random_level()
    
    def generate_random_level(self):
        # Calculate difficulty based on level and time
        base_difficulty = min(self.level - 1, 5)  # Max base difficulty of 5
        time_difficulty = self.difficulty_modifier
        total_difficulty = base_difficulty + time_difficulty
        
        # Generate platforms with increasing difficulty
        platform_count = min(6 + base_difficulty, 10)  # 6-10 platforms
        min_gap = int(max(80 - total_difficulty * 10, 40))  # Platforms get closer together
        max_gap = int(max(200 - total_difficulty * 15, 120))  # Maximum gap also decreases
        
        current_x = 100
        for i in range(platform_count):
            gap = random.randint(min_gap, max_gap)
            current_x += gap
            if current_x > WINDOW_WIDTH - 150:
                break
                
            y = random.randint(180 + int(total_difficulty * 10), WINDOW_HEIGHT - 120)  # Platforms can be higher
            width = random.randint(max(60 - int(total_difficulty * 5), 40), 120)  # Platforms get narrower
            self.platforms.append(Platform(current_x, y, width, 20))
        
        # Generate walls with increasing frequency
        wall_count = min(2 + base_difficulty // 2 + int(time_difficulty), 5)
        for i in range(wall_count):
            x = random.randint(150, WINDOW_WIDTH - 100)
            y = random.randint(100, 350)
            height = random.randint(120, 250)
            self.walls.append(Wall(x, y, 30, height))
        
        # Generate more obstacles as difficulty increases
        obstacle_count = min(1 + base_difficulty + int(time_difficulty * 2), 7)
        for i in range(obstacle_count):
            x = random.randint(100, WINDOW_WIDTH - 150)
            y = WINDOW_HEIGHT - 60
            width = random.randint(30, min(60 + int(total_difficulty * 5), 80))  # Obstacles get wider
            self.obstacles.append(Obstacle(x, y, width, 20))
        
        # Collectibles become slightly rarer at higher difficulties
        collectible_chance = max(0.8 - total_difficulty * 0.05, 0.6)
        for platform in self.platforms[1:]:  # Skip ground platform
            if random.random() < collectible_chance:
                self.collectibles.append(Collectible(platform.x + platform.width//2 - 7, platform.y - 20))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.jump()
                elif event.key == pygame.K_n:
                    # Next level (skip) - only if skips remaining
                    if self.skips_remaining > 0:
                        self.level += 1
                        self.player = Player(50, 400)
                        self.skips_remaining -= 1
                        self.create_level()
                elif event.key == pygame.K_l:
                    # Leave game and go to leaderboard
                    self.leave_game()
                elif event.key == pygame.K_ESCAPE:
                    # Return to game from leaderboard
                    if self.game_state == "leaderboard":
                        self.game_state = "playing"
                elif event.key == pygame.K_r:
                    # Restart new game completely
                    self.restart_new_game()

    def restart_new_game(self):
        """Start a completely new game"""
        self.level = 1
        self.score = 0
        self.time_survived = 0
        self.difficulty_modifier = 0
        self.skips_remaining = 3
        self.player = Player(50, 400)
        self.create_level()
        self.game_state = "playing"

    def leave_game(self):
        """Leave current game and go to leaderboard"""
        # Check if this is a high score
        if self.is_high_score(self.level):
            # Simple name input - use level as identifier for now
            player_name = f"Level{self.level}_Player"
            self.add_high_score(self.level, self.time_survived, self.score, player_name)
        
        # Go to leaderboard
        self.game_state = "leaderboard"

    def update(self):
        # Only update game logic when playing
        if self.game_state != "playing":
            return
            
        # Update time and difficulty
        self.time_survived += 1
        
        # Increase difficulty every 1800 frames (30 seconds at 60 FPS)
        if self.time_survived % 1800 == 0:
            self.difficulty_modifier += 0.5
            # Show difficulty increase message
            self.show_difficulty_message = 120  # Show for 2 seconds
        
        # Update difficulty message timer
        if self.show_difficulty_message > 0:
            self.show_difficulty_message -= 1
        
        # Update player
        self.player.update(self.platforms, self.walls)
        
        # Check collision with obstacles
        for obstacle in self.obstacles:
            if self.player.rect.colliderect(obstacle.rect):
                # Reset player position but don't lose as many points
                self.player.x = 50
                self.player.y = 400
                self.player.vel_x = 0
                self.player.vel_y = 0
                self.score = max(0, self.score - 5)  # Less harsh penalty
        
        # Check collision with collectibles
        for collectible in self.collectibles:
            if not collectible.collected and self.player.rect.colliderect(collectible.rect):
                collectible.collected = True
                # Score bonus increases with difficulty (risk vs reward)
                base_score = 10
                difficulty_bonus = int(self.difficulty_modifier * 2)
                self.score += base_score + difficulty_bonus
        
        # Update collectibles
        for collectible in self.collectibles:
            collectible.update()
        
        # Check if all collectibles are collected
        all_collected = all(c.collected for c in self.collectibles)
        if all_collected and len(self.collectibles) > 0:
            # Next level
            self.level += 1
            self.player = Player(50, 400)
            self.create_level()
            # Level completion bonus increases with difficulty
            level_bonus = 50 + int(self.difficulty_modifier * 10)
            self.score += level_bonus
    
    def draw(self):
        # Clear screen
        self.screen.fill(BLACK)
        
        if self.game_state == "playing":
            self.draw_game()
        elif self.game_state == "leaderboard":
            self.draw_leaderboard()
        
        pygame.display.flip()
    
    def draw_game(self):
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen)
        
        # Draw walls
        for wall in self.walls:
            wall.draw(self.screen)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Draw collectibles
        for collectible in self.collectibles:
            collectible.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        time_text = self.font.render(f"Time: {self.format_time(self.time_survived)}", True, WHITE)
        difficulty_text = self.small_font.render(f"Difficulty: {self.difficulty_modifier:.1f}", True, YELLOW)
        skips_text = self.small_font.render(f"Skips remaining: {self.skips_remaining}", True, CYAN)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))
        self.screen.blit(time_text, (10, 90))
        self.screen.blit(difficulty_text, (10, 130))
        self.screen.blit(skips_text, (10, 150))
        
        # Show difficulty increase message
        if self.show_difficulty_message > 0:
            alpha = min(255, self.show_difficulty_message * 4)  # Fade effect
            difficulty_msg = self.big_font.render("DIFFICULTY INCREASED!", True, RED)
            msg_rect = difficulty_msg.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100))
            # Create surface with alpha for fade effect
            fade_surface = pygame.Surface(difficulty_msg.get_size())
            fade_surface.set_alpha(alpha)
            fade_surface.blit(difficulty_msg, (0, 0))
            self.screen.blit(fade_surface, msg_rect)
        
        # Draw controls
        controls = [
            "Controls:",
            "WASD/Arrow Keys - Move",
            "Space/W/Up - Jump",
            "S/Down - Slide",
            "R - New Game",
            "N - Next Level (3x max)",
            "L - Leave to Leaderboard",
            "",
            "Difficulty increases",
            "every 30 seconds!"
        ]
        
        for i, control in enumerate(controls):
            if i == 0:
                color = YELLOW
            elif i >= 7:  # Difficulty info (adjusted after removing R)
                color = RED
            else:
                color = WHITE
            text = self.small_font.render(control, True, color)
            self.screen.blit(text, (WINDOW_WIDTH - 200, 10 + i * 20))
        
        # Draw player state info
            state_info = []
        if self.player.on_ground:
            state_info.append("On Ground")
        if self.player.on_wall:
            state_info.append("Wall Sliding")
        if self.player.sliding:
            state_info.append("Sliding")
        if not self.player.can_double_jump and not self.player.on_ground:
            state_info.append("Double Jump Used")
        
        for i, info in enumerate(state_info):
            text = self.small_font.render(info, True, CYAN)
            self.screen.blit(text, (10, 100 + i * 20))
    
    def draw_leaderboard(self):
        # Draw leaderboard screen
        title = self.big_font.render("HIGH SCORES", True, YELLOW)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Draw scores
        if self.high_scores:
            for i, (level, time, score, name) in enumerate(self.high_scores):
                rank_text = f"{i+1}. {name} - Level {level}"
                time_text = f"Time: {self.format_time(time)}"
                score_text = f"Score: {score}"
                color = [YELLOW, WHITE, ORANGE][i] if i < 3 else WHITE
                
                # Draw level text
                text = self.font.render(rank_text, True, color)
                text_rect = text.get_rect(center=(WINDOW_WIDTH//2, 200 + i * 80))
                self.screen.blit(text, text_rect)
                
                # Draw time text (smaller, below level text)
                time_surface = self.small_font.render(time_text, True, color)
                time_rect = time_surface.get_rect(center=(WINDOW_WIDTH//2, 220 + i * 80))
                self.screen.blit(time_surface, time_rect)
                
                # Draw score text (smaller, below time text)
                score_surface = self.small_font.render(score_text, True, color)
                score_rect = score_surface.get_rect(center=(WINDOW_WIDTH//2, 240 + i * 80))
                self.screen.blit(score_surface, score_rect)
        else:
            no_scores = self.font.render("No high scores yet!", True, WHITE)
            no_scores_rect = no_scores.get_rect(center=(WINDOW_WIDTH//2, 300))
            self.screen.blit(no_scores, no_scores_rect)
        
        # Instructions (moved lower to accommodate score display)
        inst1 = self.small_font.render("Press ESC to return to game", True, CYAN)
        inst1_rect = inst1.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 140))
        self.screen.blit(inst1, inst1_rect)
        
        inst2 = self.small_font.render("Press L during game to leave and save score", True, CYAN)
        inst2_rect = inst2.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 110))
        self.screen.blit(inst2, inst2_rect)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

def main():
    game = ParkourGame()
    game.run()

if __name__ == "__main__":
    main()
