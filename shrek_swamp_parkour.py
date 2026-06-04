import pygame
import random
import math
import sys

pygame.init()

# Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
GRAVITY = 0.9
JUMP_STRENGTH = -20
PLAYER_SPEED = 8
WALL_JUMP_STRENGTH = -18
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
SWAMP_GREEN = (107, 142, 35)
MUD_BROWN = (101, 67, 33)
ONION_PURPLE = (186, 85, 211)
FAIRY_PINK = (255, 182, 193)
MAGIC_BLUE = (138, 43, 226)

class ShrekPlayer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 50
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.on_wall = False
        self.wall_direction = 0
        self.can_double_jump = True
        self.can_fart_jump = True
        self.fart_power = 0
        self.onion_power = False
        self.onion_timer = 0
        self.roar_cooldown = 0
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Shrek special abilities
        self.swamp_mode = False
        self.swamp_timer = 0
        self.mud_trail = []
        self.onion_layers = 3  # Like ogres!
        
    def update(self, platforms, walls, moving_platforms):
        keys = pygame.key.get_pressed()
        
        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
            if self.swamp_mode:
                self.vel_x *= 1.5  # Faster in swamp mode
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
            if self.swamp_mode:
                self.vel_x *= 1.5
        else:
            self.vel_x *= 0.8
        
        # Cooldowns
        if self.roar_cooldown > 0:
            self.roar_cooldown -= 1
        if self.onion_timer > 0:
            self.onion_timer -= 1
            self.onion_power = True
        else:
            self.onion_power = False
        if self.swamp_timer > 0:
            self.swamp_timer -= 1
            self.swamp_mode = True
        else:
            self.swamp_mode = False
            
        # Apply gravity
        if not self.on_ground:
            self.vel_y += GRAVITY
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Add mud trail when in swamp mode
        if self.swamp_mode and len(self.mud_trail) < 20:
            self.mud_trail.append((self.x + self.width//2, self.y + self.height))
        elif len(self.mud_trail) > 20:
            self.mud_trail.pop(0)
        elif not self.swamp_mode and len(self.mud_trail) > 0:
            self.mud_trail.pop(0)
        
        # Update rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Reset collision flags
        self.on_ground = False
        self.on_wall = False
        
        # Platform collisions
        for platform in platforms + moving_platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0 and self.y < platform.y:
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    self.can_double_jump = True
                    self.can_fart_jump = True
                elif self.vel_y < 0 and self.y > platform.y:
                    self.y = platform.y + platform.height
                    self.vel_y = 0
                elif self.vel_x > 0:
                    self.x = platform.x - self.width
                    self.vel_x = 0
                elif self.vel_x < 0:
                    self.x = platform.x + platform.width
                    self.vel_x = 0
        
        # Wall collisions
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if not self.on_ground and abs(self.vel_y) > 0.5:
                    if self.x < wall.x:
                        self.x = wall.x - self.width
                        self.on_wall = True
                        self.wall_direction = 1
                        self.vel_y *= 0.4
                        if self.vel_y > 4:
                            self.vel_y = 4
                        self.can_double_jump = True
                        self.can_fart_jump = True
                    else:
                        self.x = wall.x + wall.width
                        self.on_wall = True
                        self.wall_direction = -1
                        self.vel_y *= 0.4
                        if self.vel_y > 4:
                            self.vel_y = 4
                        self.can_double_jump = True
                        self.can_fart_jump = True
        
        # Screen boundaries
        if self.x < 0:
            self.x = 0
            self.vel_x = 0
        elif self.x > WINDOW_WIDTH - self.width:
            self.x = WINDOW_WIDTH - self.width
            self.vel_x = 0
            
        if self.y > WINDOW_HEIGHT:
            self.reset_position()
    
    def reset_position(self):
        self.x = 100
        self.y = 600
        self.vel_x = 0
        self.vel_y = 0
        self.onion_layers = 3
    
    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
        elif self.can_double_jump and not self.on_wall:
            self.vel_y = JUMP_STRENGTH * 0.8
            self.can_double_jump = False
        elif self.on_wall:
            self.vel_y = WALL_JUMP_STRENGTH
            self.vel_x = self.wall_direction * PLAYER_SPEED * 2
            self.on_wall = False
            self.can_double_jump = True
    
    def fart_jump(self):
        # Special Shrek ability - fart jump!
        if self.can_fart_jump:
            self.vel_y = JUMP_STRENGTH * 1.5  # Extra powerful jump
            self.can_fart_jump = False
            return True  # Return true to create fart particles
        return False
    
    def roar_attack(self):
        # Shrek's roar destroys nearby obstacles
        if self.roar_cooldown <= 0:
            self.roar_cooldown = 120  # 2 seconds
            return True
        return False
    
    def use_onion_layer(self):
        # Use onion layer for temporary invincibility
        if self.onion_layers > 0:
            self.onion_layers -= 1
            self.onion_timer = 180  # 3 seconds of power
            return True
        return False
    
    def activate_swamp_mode(self):
        self.swamp_timer = 300  # 5 seconds of swamp power
    
    def draw(self, screen):
        # Draw mud trail
        for i, (x, y) in enumerate(self.mud_trail):
            alpha = int((i / len(self.mud_trail)) * 255)
            size = int((i / len(self.mud_trail)) * 10) + 3
            pygame.draw.circle(screen, MUD_BROWN, (int(x), int(y)), size)
        
        # Player color based on state
        if self.swamp_mode:
            color = SWAMP_GREEN
            # Draw swamp aura
            for i in range(3):
                glow_size = self.width + i * 8
                pygame.draw.ellipse(screen, SWAMP_GREEN, 
                                  (self.x - i*4, self.y - i*4, glow_size, self.height + i*8))
        elif self.onion_power:
            color = ONION_PURPLE
        elif self.on_wall:
            color = BROWN
        elif not self.on_ground:
            color = GREEN
        else:
            color = DARK_GREEN
        
        # Draw Shrek (simplified ogre shape)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 3)
        
        # Draw ogre ears
        ear_size = 8
        pygame.draw.circle(screen, color, (int(self.x + 5), int(self.y + 10)), ear_size)
        pygame.draw.circle(screen, color, (int(self.x + self.width - 5), int(self.y + 10)), ear_size)
        
        # Draw onion layer indicator
        for i in range(self.onion_layers):
            pygame.draw.circle(screen, ONION_PURPLE, 
                             (int(self.x + 10 + i * 8), int(self.y - 15)), 4)
        
        # Draw ability cooldowns
        if self.roar_cooldown > 0:
            cooldown_width = 40
            cooldown_height = 4
            cooldown_ratio = 1 - (self.roar_cooldown / 120)
            pygame.draw.rect(screen, RED, (self.x, self.y - 25, cooldown_width, cooldown_height))
            pygame.draw.rect(screen, GREEN, (self.x, self.y - 25, cooldown_width * cooldown_ratio, cooldown_height))

class SwampPlatform:
    def __init__(self, x, y, width, height, platform_type="normal"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = platform_type
        self.rect = pygame.Rect(x, y, width, height)
        self.bounce_power = 0
        self.magic_timer = 0
        
        if platform_type == "mushroom":
            self.bounce_power = -30
        elif platform_type == "magic":
            self.magic_timer = 0
    
    def update(self):
        if self.type == "magic":
            self.magic_timer += 1
    
    def draw(self, screen):
        colors = {
            "normal": BROWN,
            "mushroom": RED,
            "magic": MAGIC_BLUE,
            "mud": MUD_BROWN,
            "fairy": FAIRY_PINK
        }
        color = colors.get(self.type, BROWN)
        
        if self.type == "magic":
            # Glowing magic platform
            glow_intensity = int(50 + 30 * math.sin(self.magic_timer * 0.1))
            glow_color = (color[0], color[1], min(255, color[2] + glow_intensity))
            pygame.draw.rect(screen, glow_color, self.rect)
        else:
            pygame.draw.rect(screen, color, self.rect)
            
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Special platform decorations
        if self.type == "mushroom":
            # Draw mushroom spots
            spot_size = 4
            for i in range(3):
                spot_x = self.x + 10 + i * 15
                spot_y = self.y + 5
                pygame.draw.circle(screen, WHITE, (spot_x, spot_y), spot_size)

class MovingPlatform:
    def __init__(self, x, y, width, height, move_type="horizontal", speed=3, distance=150):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.move_type = move_type
        self.speed = speed
        self.distance = distance
        self.direction = 1
        self.timer = 0
        self.rect = pygame.Rect(x, y, width, height)
    
    def update(self):
        self.timer += 1
        
        if self.move_type == "horizontal":
            self.x += self.speed * self.direction
            if abs(self.x - self.start_x) >= self.distance:
                self.direction *= -1
        elif self.move_type == "vertical":
            self.y += self.speed * self.direction
            if abs(self.y - self.start_y) >= self.distance:
                self.direction *= -1
        elif self.move_type == "dragon":
            # Dragon flight pattern
            angle = self.timer * 0.03
            self.x = self.start_x + math.cos(angle) * self.distance
            self.y = self.start_y + math.sin(angle * 2) * (self.distance // 2)
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        if self.move_type == "dragon":
            color = RED  # Dragon platform
        else:
            color = SWAMP_GREEN
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

class SwampCollectible:
    def __init__(self, x, y, collectible_type="coin"):
        self.x = x
        self.y = y
        self.type = collectible_type
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.collected = False
        self.bounce = 0
        self.rotation = 0
    
    def update(self):
        self.bounce += 0.3
        self.rotation += 5
    
    def draw(self, screen):
        if not self.collected:
            bounce_y = self.y + math.sin(self.bounce) * 6
            
            colors = {
                "coin": YELLOW,
                "fairy_dust": FAIRY_PINK,
                "onion": ONION_PURPLE,
                "swamp_gas": GREEN
            }
            color = colors.get(self.type, WHITE)
            
            center_x = self.x + self.width // 2
            center_y = bounce_y + self.height // 2
            
            if self.type == "fairy_dust":
                # Sparkling effect
                for i in range(5):
                    spark_x = center_x + math.cos(self.rotation + i * 72) * 8
                    spark_y = center_y + math.sin(self.rotation + i * 72) * 8
                    pygame.draw.circle(screen, FAIRY_PINK, (int(spark_x), int(spark_y)), 2)
            
            pygame.draw.circle(screen, color, (int(center_x), int(center_y)), self.width // 2)
            pygame.draw.circle(screen, WHITE, (int(center_x), int(center_y)), self.width // 2, 2)

class FartParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-8, -3)
        self.lifetime = random.randint(30, 60)
        self.size = random.randint(4, 12)
        self.color = random.choice([GREEN, SWAMP_GREEN, YELLOW])
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # Gravity on particles
        self.lifetime -= 1
        self.size = max(1, self.size - 0.2)
    
    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

class ShrekParkourGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Shrek Swamp Parkour!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # Game state
        self.running = True
        self.score = 0
        self.level = 1
        self.time = 0
        
        # Camera
        self.camera_x = 0
        self.camera_y = 0
        
        # Initialize objects
        self.player = ShrekPlayer(100, 600)
        self.platforms = []
        self.moving_platforms = []
        self.collectibles = []
        self.fart_particles = []
        
        # Cheats/Hacks (as requested!)
        self.god_mode = False
        self.super_speed = False
        self.infinite_jumps = False
        self.no_gravity = False
        
        self.create_swamp_level()
    
    def create_swamp_level(self):
        # Clear existing objects
        self.platforms.clear()
        self.moving_platforms.clear()
        self.collectibles.clear()
        
        # Ground
        self.platforms.append(SwampPlatform(0, WINDOW_HEIGHT - 60, 400, 60, "mud"))
        
        if self.level == 1:
            # Tutorial swamp
            self.platforms.append(SwampPlatform(500, 650, 120, 25, "normal"))
            self.platforms.append(SwampPlatform(700, 590, 120, 25, "mushroom"))
            self.platforms.append(SwampPlatform(900, 530, 120, 25, "magic"))
            self.platforms.append(SwampPlatform(1100, 470, 120, 25, "fairy"))
            
            # Moving dragon platform
            self.moving_platforms.append(MovingPlatform(1300, 400, 100, 25, "dragon", 2, 100))
            
            # Collectibles
            self.collectibles.append(SwampCollectible(540, 620, "coin"))
            self.collectibles.append(SwampCollectible(740, 560, "onion"))
            self.collectibles.append(SwampCollectible(940, 500, "fairy_dust"))
            self.collectibles.append(SwampCollectible(1140, 440, "swamp_gas"))
            
        elif self.level == 2:
            # Advanced swamp course
            self.platforms.append(SwampPlatform(400, 680, 100, 20, "mushroom"))
            
            # Bouncing mushroom section
            for i in range(5):
                self.platforms.append(SwampPlatform(600 + i * 150, 600 - i * 40, 80, 20, "mushroom"))
            
            # Magic platform maze
            magic_platforms = [
                (1200, 400), (1300, 350), (1400, 300), (1500, 250),
                (1600, 300), (1700, 350), (1800, 400), (1900, 350)
            ]
            for x, y in magic_platforms:
                self.platforms.append(SwampPlatform(x, y, 70, 20, "magic"))
            
            # Moving platforms
            self.moving_platforms.append(MovingPlatform(2100, 300, 100, 20, "vertical", 3, 200))
            self.moving_platforms.append(MovingPlatform(2400, 200, 100, 20, "dragon", 2, 150))
            
            # Special collectibles
            for i in range(10):
                x = 500 + i * 200
                y = 500 - random.randint(0, 200)
                collectible_type = random.choice(["coin", "onion", "fairy_dust", "swamp_gas"])
                self.collectibles.append(SwampCollectible(x, y, collectible_type))
        
        else:
            # Procedural crazy swamp levels
            self.generate_crazy_swamp_level()
    
    def generate_crazy_swamp_level(self):
        current_x = 400
        current_y = 600
        
        platform_types = ["normal", "mushroom", "magic", "fairy", "mud"]
        
        for i in range(20):
            gap = random.randint(80, 250)
            current_x += gap
            y_change = random.randint(-100, 50)
            current_y = max(200, min(700, current_y + y_change))
            
            platform_type = random.choice(platform_types)
            platform_width = random.randint(60, 140)
            
            self.platforms.append(SwampPlatform(current_x, current_y, platform_width, 20, platform_type))
            
            # Add moving platforms
            if random.random() < 0.3:
                move_type = random.choice(["horizontal", "vertical", "dragon"])
                self.moving_platforms.append(
                    MovingPlatform(current_x + 200, current_y - 150, 80, 20, 
                                 move_type, random.randint(2, 5), random.randint(100, 200))
                )
            
            # Add collectibles
            if random.random() < 0.7:
                collectible_type = random.choice(["coin", "onion", "fairy_dust", "swamp_gas"])
                self.collectibles.append(SwampCollectible(current_x + 20, current_y - 40, collectible_type))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # Normal controls
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.jump()
                elif event.key == pygame.K_f:
                    # Fart jump!
                    if self.player.fart_jump():
                        # Create fart particles
                        for _ in range(15):
                            self.fart_particles.append(FartParticle(
                                self.player.x + self.player.width//2,
                                self.player.y + self.player.height
                            ))
                elif event.key == pygame.K_r:
                    # Roar attack
                    self.player.roar_attack()
                elif event.key == pygame.K_o:
                    # Use onion layer
                    self.player.use_onion_layer()
                elif event.key == pygame.K_m:
                    # Swamp mode
                    self.player.activate_swamp_mode()
                
                # CHEAT CODES / HACKS!
                elif event.key == pygame.K_F1:
                    self.god_mode = not self.god_mode
                    print("God Mode:", "ON" if self.god_mode else "OFF")
                elif event.key == pygame.K_F2:
                    self.super_speed = not self.super_speed
                    print("Super Speed:", "ON" if self.super_speed else "OFF")
                elif event.key == pygame.K_F3:
                    self.infinite_jumps = not self.infinite_jumps
                    print("Infinite Jumps:", "ON" if self.infinite_jumps else "OFF")
                elif event.key == pygame.K_F4:
                    self.no_gravity = not self.no_gravity
                    print("No Gravity:", "ON" if self.no_gravity else "OFF")
                elif event.key == pygame.K_F5:
                    # Teleport to end
                    self.player.x = 2500
                    self.player.y = 300
                    print("Teleported to end!")
                elif event.key == pygame.K_F6:
                    # Give all collectibles
                    for collectible in self.collectibles:
                        if not collectible.collected:
                            collectible.collected = True
                            self.score += 1000
                    print("All collectibles collected!")
                elif event.key == pygame.K_F7:
                    # Max onion layers
                    self.player.onion_layers = 10
                    print("Max onion layers!")
                elif event.key == pygame.K_F8:
                    # Skip level
                    self.next_level()
                    print("Level skipped!")
                elif event.key == pygame.K_n:
                    self.next_level()
    
    def next_level(self):
        self.level += 1
        self.player.x = 100
        self.player.y = 600
        self.player.vel_x = 0
        self.player.vel_y = 0
        self.player.onion_layers = min(10, self.player.onion_layers + 1)
        self.create_swamp_level()
    
    def update_camera(self):
        target_x = self.player.x - WINDOW_WIDTH // 3
        target_y = self.player.y - WINDOW_HEIGHT // 2
        
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_y += (target_y - self.camera_y) * 0.1
        
        self.camera_y = max(-300, min(300, self.camera_y))
    
    def update(self):
        self.time += 1
        
        # Apply cheat effects
        if self.super_speed:
            self.player.vel_x *= 2
        if self.infinite_jumps:
            self.player.can_double_jump = True
            self.player.can_fart_jump = True
        if self.no_gravity and not self.player.on_ground:
            self.player.vel_y *= 0.5
        
        # Update player (skip collision if god mode)
        if not self.god_mode:
            self.player.update(self.platforms, [], self.moving_platforms)
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.x -= 10
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.x += 10
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.player.y -= 10
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.player.y += 10
        
        # Update moving platforms
        for platform in self.moving_platforms:
            platform.update()
        
        # Update magic platforms
        for platform in self.platforms:
            platform.update()
        
        # Update collectibles
        for collectible in self.collectibles:
            collectible.update()
            if not collectible.collected and self.player.rect.colliderect(collectible.rect):
                collectible.collected = True
                if collectible.type == "coin":
                    self.score += 100
                elif collectible.type == "onion":
                    self.player.onion_layers = min(10, self.player.onion_layers + 1)
                    self.score += 500
                elif collectible.type == "fairy_dust":
                    self.player.activate_swamp_mode()
                    self.score += 1000
                elif collectible.type == "swamp_gas":
                    self.player.can_fart_jump = True
                    self.score += 300
        
        # Update fart particles
        for particle in self.fart_particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.fart_particles.remove(particle)
        
        # Handle bouncing platforms
        for platform in self.platforms:
            if platform.type == "mushroom" and self.player.rect.colliderect(platform.rect):
                if self.player.vel_y > 0:
                    self.player.vel_y = platform.bounce_power
        
        # Check for level completion (reach far right)
        if self.player.x > 2500:
            self.next_level()
        
        self.update_camera()
    
    def draw(self):
        # Swamp background gradient
        for y in range(WINDOW_HEIGHT):
            color_ratio = y / WINDOW_HEIGHT
            r = int(34 * (1 - color_ratio) + 107 * color_ratio)
            g = int(139 * (1 - color_ratio) + 142 * color_ratio)
            b = int(34 * (1 - color_ratio) + 35 * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))
        
        # Calculate offsets
        offset_x = -self.camera_x
        offset_y = -self.camera_y
        
        # Draw platforms
        for platform in self.platforms:
            original_rect = platform.rect.copy()
            platform.rect = pygame.Rect(platform.rect.x + offset_x, platform.rect.y + offset_y, 
                                       platform.rect.width, platform.rect.height)
            platform.x += offset_x
            platform.y += offset_y
            platform.draw(self.screen)
            platform.x -= offset_x
            platform.y -= offset_y
            platform.rect = original_rect
        
        # Draw moving platforms
        for platform in self.moving_platforms:
            original_rect = platform.rect.copy()
            platform.rect = pygame.Rect(platform.rect.x + offset_x, platform.rect.y + offset_y, 
                                       platform.rect.width, platform.rect.height)
            platform.draw(self.screen)
            platform.rect = original_rect
        
        # Draw collectibles
        for collectible in self.collectibles:
            if not collectible.collected:
                collectible.x += offset_x
                collectible.y += offset_y
                collectible.draw(self.screen)
                collectible.x -= offset_x
                collectible.y -= offset_y
        
        # Draw fart particles
        for particle in self.fart_particles:
            particle.x += offset_x
            particle.y += offset_y
            particle.draw(self.screen)
            particle.x -= offset_x
            particle.y -= offset_y
        
        # Draw player
        self.player.x += offset_x
        self.player.y += offset_y
        trail_copy = [(x + offset_x, y + offset_y) for x, y in self.player.mud_trail]
        original_trail = self.player.mud_trail.copy()
        self.player.mud_trail = trail_copy
        self.player.draw(self.screen)
        self.player.mud_trail = original_trail
        self.player.x -= offset_x
        self.player.y -= offset_y
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))
        
        # Controls
        controls = [
            "WASD - Move",
            "Space - Jump",
            "F - Fart Jump!",
            "R - Roar Attack",
            "O - Use Onion Layer",
            "M - Swamp Mode",
            "",
            "CHEATS/HACKS:",
            "F1 - God Mode",
            "F2 - Super Speed", 
            "F3 - Infinite Jumps",
            "F4 - No Gravity",
            "F5 - Teleport to End",
            "F6 - Get All Items",
            "F7 - Max Onion Layers",
            "F8 - Skip Level"
        ]
        
        for i, control in enumerate(controls):
            color = YELLOW if "CHEATS" in control or control.startswith("F") else WHITE
            if control == "":
                continue
            text = pygame.font.Font(None, 20).render(control, True, color)
            self.screen.blit(text, (WINDOW_WIDTH - 200, 10 + i * 18))
        
        # Cheat status indicators
        cheats_active = []
        if self.god_mode:
            cheats_active.append("GOD MODE")
        if self.super_speed:
            cheats_active.append("SUPER SPEED")
        if self.infinite_jumps:
            cheats_active.append("INFINITE JUMPS")
        if self.no_gravity:
            cheats_active.append("NO GRAVITY")
        
        for i, cheat in enumerate(cheats_active):
            text = pygame.font.Font(None, 24).render(cheat, True, RED)
            self.screen.blit(text, (10, 100 + i * 25))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    game = ShrekParkourGame()
    game.run()

if __name__ == "__main__":
    main()