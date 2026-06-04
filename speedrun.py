import pygame
import sys
import random
import math
import time
import json
    
# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
PLAYER_SIZE = 30
JUMP_POWER = 18
WALL_JUMP_POWER = 16
GRAVITY = 0.9
GROUND_LEVEL = WINDOW_HEIGHT - 50
MAX_SPEED = 10
ACCELERATION = 0.7
FRICTION = 0.85
AIR_CONTROL = 0.3
BLOCK_SIZE = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64) 
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (135, 206, 235)
PURPLE = (128, 0, 128)

ORANGE = (255, 165, 0)
PINK = (255, 20, 147)
CYAN = (0, 255, 255)
BROWN = (139, 69, 19)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
NEON_GREEN = (57, 255, 20)
NEON_BLUE = (4, 217, 255)
NEON_PINK = (255, 16, 240)
SPIKE_GRAY = (80, 80, 80)
PULSE_PURPLE = (138, 43, 226)
SHIMMER_TEAL = (64, 224, 208)
RAINBOW_BASE = (255, 127, 80)
GRADIENT_START = (255, 100, 200)
GRADIENT_END = (100, 200, 255)
SPIRAL_BLUE = (30, 144, 255)
MATRIX_GREEN = (0, 255, 0)
LAVA_RED = (255, 69, 0)
CRYSTAL_PINK = (255, 192, 203)
GALAXY_PURPLE = (75, 0, 130)
DISCO_GOLD = (255, 215, 0)
ELECTRIC_CYAN = (0, 255, 255)
NEON_ORANGE = (255, 165, 0)

# Game settings
FPS = 60

# Game modes
GAME_MODES = {
    'classic': {'name': 'Classic Parkour', 'description': 'Free exploration with collectibles'},
    'speedrun': {'name': 'Speed Run', 'description': 'Race against time through checkpoints'},
    'survival': {'name': 'Survival Mode', 'description': 'Survive waves of obstacles and enemies'},
    'puzzle': {'name': 'Puzzle Platforms', 'description': 'Solve platform puzzles to progress'},
    'boss_rush': {'name': 'Boss Rush', 'description': 'Fight epic bosses with parkour skills'},
    'creative': {'name': 'Creative Mode', 'description': 'Build your own levels'},
    'multiplayer': {'name': 'Race Mode', 'description': 'Race against AI opponents'}
}

# Achievements system
ACHIEVEMENTS = {
    'first_jump': {'name': 'First Leap', 'description': 'Make your first jump', 'reward': 50},
    'wall_master': {'name': 'Wall Master', 'description': 'Perform 100 wall jumps', 'reward': 200},
    'coin_collector': {'name': 'Coin Collector', 'description': 'Collect 100 coins', 'reward': 300},
    'speed_demon': {'name': 'Speed Demon', 'description': 'Reach max speed 50 times', 'reward': 400},
    'survivor': {'name': 'Survivor', 'description': 'Survive 5 minutes in survival mode', 'reward': 500},
    'puzzle_solver': {'name': 'Puzzle Master', 'description': 'Complete 10 puzzle levels', 'reward': 600},
    'boss_slayer': {'name': 'Boss Slayer', 'description': 'Defeat all bosses', 'reward': 1000},
    'perfectionist': {'name': 'Perfectionist', 'description': 'Complete a level without dying', 'reward': 800},
    'explorer': {'name': 'Explorer', 'description': 'Discover all secret areas', 'reward': 750},
    'customizer': {'name': 'Fashion Designer', 'description': 'Unlock 10 character skins', 'reward': 400}
}

# Character customization
PLAYER_SKINS = {
    'default': {'name': 'Classic', 'color': NEON_PINK, 'cost': 0, 'unlocked': True},
    'fire': {'name': 'Fire Runner', 'color': (255, 69, 0), 'cost': 100, 'unlocked': False},
    'ice': {'name': 'Ice Walker', 'color': (173, 216, 230), 'cost': 150, 'unlocked': False},
    'shadow': {'name': 'Shadow Ninja', 'color': (25, 25, 25), 'cost': 200, 'unlocked': False},
    'electric': {'name': 'Electric', 'color': (255, 255, 0), 'cost': 250, 'unlocked': False},
    'rainbow': {'name': 'Rainbow', 'color': None, 'cost': 500, 'unlocked': False},  # Special animated
    'ghost': {'name': 'Ghost', 'color': (200, 200, 200), 'cost': 300, 'unlocked': False},
    'golden': {'name': 'Golden Hero', 'color': GOLD, 'cost': 1000, 'unlocked': False}
}

# Shop items
SHOP_ITEMS = {
    'double_jump_upgrade': {'name': 'Triple Jump', 'description': 'Allows triple jumping', 'cost': 500, 'type': 'ability'},
    'dash_upgrade': {'name': 'Super Dash', 'description': 'Longer dash distance', 'cost': 300, 'type': 'ability'},
    'magnet': {'name': 'Coin Magnet', 'description': 'Attracts nearby coins', 'cost': 400, 'type': 'ability'},
    'shield_upgrade': {'name': 'Super Shield', 'description': 'Shield lasts longer', 'cost': 350, 'type': 'ability'},
    'speed_boost': {'name': 'Permanent Speed', 'description': '+20% base speed', 'cost': 600, 'type': 'upgrade'},
    'jump_boost': {'name': 'Permanent Jump', 'description': '+20% jump height', 'cost': 600, 'type': 'upgrade'}
}

# Enemy types for survival mode
ENEMY_TYPES = {
    'basic': {'health': 1, 'speed': 2, 'color': RED, 'size': 20, 'points': 10},
    'fast': {'health': 1, 'speed': 4, 'color': ORANGE, 'size': 15, 'points': 20},
    'tank': {'health': 3, 'speed': 1, 'color': PURPLE, 'size': 30, 'points': 50},
    'flying': {'health': 2, 'speed': 3, 'color': CYAN, 'size': 18, 'points': 30}
}

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            return Vector2(self.x / mag, self.y / mag)
        return Vector2(0, 0)

class Achievement:
    def __init__(self, achievement_id, data):
        self.id = achievement_id
        self.name = data['name']
        self.description = data['description']
        self.reward = data['reward']
        self.unlocked = False
        self.progress = 0
        self.notification_timer = 0
    
    def unlock(self):
        if not self.unlocked:
            self.unlocked = True
            self.notification_timer = 180  # 3 seconds
            return True
        return False

class Particle:
    def __init__(self, x, y, vel_x, vel_y, color, size, lifetime):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.gravity = 0.2
    
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += self.gravity
        self.vel_x *= 0.98
        self.lifetime -= 1
        return self.lifetime > 0
    
    def draw(self, screen, camera_x):
        if self.lifetime > 0:
            # Prevent division by zero
            if self.max_lifetime > 0:
                alpha = int(255 * (self.lifetime / self.max_lifetime))
                size = max(1, int(self.size * (self.lifetime / self.max_lifetime)))
            else:
                alpha = 255
                size = max(1, int(self.size))
            x = int(self.x - camera_x)
            y = int(self.y)
            
            # Create a surface with alpha
            surf = pygame.Surface((size * 2, size * 2))
            surf.set_alpha(alpha)
            surf.fill(self.color)
            screen.blit(surf, (x - size, y - size))

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def add_explosion(self, x, y, color=ORANGE):
        for _ in range(15):
            vel_x = random.uniform(-8, 8)
            vel_y = random.uniform(-12, -2)
            size = random.uniform(3, 8)
            lifetime = random.randint(20, 40)
            self.particles.append(Particle(x, y, vel_x, vel_y, color, size, lifetime))
    
    def add_trail(self, x, y, color=NEON_BLUE):
        vel_x = random.uniform(-2, 2)
        vel_y = random.uniform(-3, 1)
        size = random.uniform(2, 4)
        lifetime = random.randint(10, 20)
        self.particles.append(Particle(x, y, vel_x, vel_y, color, size, lifetime))
    
    def add_landing(self, x, y):
        for _ in range(8):
            vel_x = random.uniform(-6, 6)
            vel_y = random.uniform(-8, -2)
            size = random.uniform(2, 5)
            lifetime = random.randint(15, 30)
            color = random.choice([WHITE, LIGHT_GRAY, GRAY])
            self.particles.append(Particle(x, y, vel_x, vel_y, color, size, lifetime))
    
    def update(self):
        self.particles = [p for p in self.particles if p.update()]
    
    def draw(self, screen, camera_x):
        for particle in self.particles:
            particle.draw(screen, camera_x)

class Platform:
    def __init__(self, x, y, width, height, platform_type="normal"):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = platform_type  # Can be "normal", "trampoline", "moving", etc.
        self.color = self.get_color()
        self.boost_power = 25 if platform_type in ["trampoline", "spring"] else 0
        self.moving = False
        self.move_speed = 0
        self.move_range = 0
        self.original_x = x
        self.move_direction = 1
        
        # Animation variables for decorative platforms
        self.animation_frame = 0
        self.pulse_intensity = 0
        self.shimmer_offset = random.uniform(0, 6.28)  # Random start phase
        self.rainbow_hue = random.uniform(0, 360)
        self.wave_offset = random.uniform(0, 6.28)
        self.spiral_angle = random.uniform(0, 6.28)
        self.matrix_drops = [random.randint(0, height) for _ in range(width // 10)]
        self.lava_bubbles = []
        self.crystal_facets = random.randint(6, 12)
        self.galaxy_stars = [(random.randint(0, width), random.randint(0, height)) for _ in range(8)]
        self.disco_rotation = 0
        self.electric_sparks = []
        self.glitch_offset = 0
        
        # Configure platform behavior based on type
        if platform_type == "moving" or platform_type == "moving_trampoline":
            self.moving = True
            self.move_speed = 2
            self.move_range = 150
            if platform_type == "moving_trampoline":
                self.boost_power = 25
    
    def get_color(self):
        colors = {
            "normal": GRAY,           # Regular platform - gray
            "trampoline": NEON_GREEN, # Bouncy platform - green
            "boost": NEON_BLUE,       # Speed boost platform
            "ice": LIGHT_BLUE,        # Slippery platform
            "moving": PURPLE,         # Moving platform
            "moving_trampoline": NEON_GREEN,  # Moving bouncy platform
            "breakable": BROWN,       # Breakable platform
            "electric": YELLOW,       # Electric platform
            "spring": NEON_GREEN,     # Spring platform (same as trampoline)
            "spikes": SPIKE_GRAY,     # Dangerous spikes platform
            "pulse": PULSE_PURPLE,    # Pulsing animated platform
            "shimmer": SHIMMER_TEAL,  # Shimmering platform
            "rainbow": RAINBOW_BASE,  # Rainbow cycling platform
            "glow": NEON_PINK,        # Glowing platform
            "wave": NEON_BLUE,        # Wave animation platform
            "gradient": GRADIENT_START, # Gradient color-shifting platform
            "spiral": SPIRAL_BLUE,    # Spiral animation platform
            "matrix": MATRIX_GREEN,   # Matrix rain effect platform
            "lava": LAVA_RED,         # Lava bubbling platform
            "crystal": CRYSTAL_PINK,  # Crystal faceted platform
            "galaxy": GALAXY_PURPLE,  # Galaxy with moving stars
            "disco": DISCO_GOLD,      # Disco ball effect platform
            "electric_storm": ELECTRIC_CYAN, # Electric storm platform
            "glitch": NEON_ORANGE     # Glitching/corrupted platform
        }
        return colors.get(self.type, GRAY)
    
    def update(self):
        # Update animation frame for all platforms
        self.animation_frame += 1
        
        # Update moving platforms
        if self.moving:
            self.rect.x += self.move_speed * self.move_direction
            if abs(self.rect.x - self.original_x) > self.move_range:
                self.move_direction *= -1
        
        # Update animation effects for decorative platforms
        if self.type == "pulse":
            self.pulse_intensity = (math.sin(self.animation_frame * 0.1) + 1) / 2  # 0 to 1
        elif self.type == "shimmer":
            self.shimmer_offset += 0.15
        elif self.type == "rainbow":
            self.rainbow_hue = (self.rainbow_hue + 2) % 360
        elif self.type == "wave":
            self.wave_offset += 0.2
        elif self.type == "gradient":
            pass  # Gradient doesn't need special update, uses animation_frame
        elif self.type == "spiral":
            self.spiral_angle += 0.1
        elif self.type == "matrix":
            # Update matrix rain drops
            for i in range(len(self.matrix_drops)):
                self.matrix_drops[i] = (self.matrix_drops[i] + 2) % (self.rect.height + 20)
        elif self.type == "lava":
            # Update lava bubbles
            if random.random() < 0.1:  # 10% chance to spawn new bubble
                self.lava_bubbles.append({
                    'x': random.randint(5, self.rect.width - 5),
                    'y': self.rect.height - 5,
                    'size': random.randint(2, 6),
                    'life': random.randint(20, 40)
                })
            # Update existing bubbles
            self.lava_bubbles = [
                {**bubble, 'y': bubble['y'] - 1, 'life': bubble['life'] - 1}
                for bubble in self.lava_bubbles if bubble['life'] > 0 and bubble['y'] > 0
            ]
        elif self.type == "galaxy":
            # Move stars slowly
            for i, (x, y) in enumerate(self.galaxy_stars):
                new_x = (x + random.uniform(-0.5, 0.5)) % self.rect.width
                new_y = (y + random.uniform(-0.5, 0.5)) % self.rect.height
                self.galaxy_stars[i] = (new_x, new_y)
        elif self.type == "disco":
            self.disco_rotation += 3
        elif self.type == "electric_storm":
            # Update electric sparks
            if random.random() < 0.3:  # 30% chance to spawn spark
                self.electric_sparks.append({
                    'x': random.randint(0, self.rect.width),
                    'y': random.randint(0, self.rect.height),
                    'life': random.randint(5, 15),
                    'branches': []
                })
            # Update existing sparks
            self.electric_sparks = [
                {**spark, 'life': spark['life'] - 1}
                for spark in self.electric_sparks if spark['life'] > 0
            ]
        elif self.type == "glitch":
            if random.random() < 0.1:  # 10% chance to glitch
                self.glitch_offset = random.randint(-5, 5)
    
    def draw(self, screen, camera_x):
        # Adjust position for camera
        draw_rect = pygame.Rect(self.rect.x - camera_x, self.rect.y, 
                               self.rect.width, self.rect.height)
        
        # Draw main platform
        pygame.draw.rect(screen, self.color, draw_rect)
        
        # Draw special effects based on platform type
        if self.type in ["trampoline", "spring", "moving_trampoline"]:
            # Modern trampoline with sleek spring mechanism
            # Draw main platform with metallic gradient
            gradient_steps = 6
            step_height = draw_rect.height / gradient_steps
            
            for i in range(gradient_steps):
                brightness = 0.8 + (i * 0.04)  # Metallic sheen
                spring_color = (
                    max(0, min(255, int(NEON_GREEN[0] * brightness))),
                    max(0, min(255, int(NEON_GREEN[1] * brightness))),
                    max(0, min(255, int(NEON_GREEN[2] * brightness)))
                )
                
                gradient_rect = pygame.Rect(
                    draw_rect.x,
                    draw_rect.y + i * step_height,
                    draw_rect.width,
                    step_height + 1
                )
                pygame.draw.rect(screen, spring_color, gradient_rect)
            
            # Add modern spring coils underneath
            spring_count = max(3, self.rect.width // 30)
            spring_width = self.rect.width // spring_count
            
            for i in range(spring_count):
                spring_x = draw_rect.x + i * spring_width + spring_width // 2
                spring_y = draw_rect.y + draw_rect.height
                
                # Draw sleek spring mechanism
                coil_height = 16
                coil_segments = 6
                
                for j in range(coil_segments):
                    coil_y = spring_y + j * (coil_height // coil_segments)
                    coil_radius = 4 + math.sin(j * 0.8) * 2  # Variable radius for spring effect
                    
                    # Spring coil with metallic effect
                    pygame.draw.circle(screen, SILVER, (spring_x, coil_y), int(coil_radius) + 1)
                    pygame.draw.circle(screen, WHITE, (spring_x, coil_y), int(coil_radius))
                    pygame.draw.circle(screen, DARK_GRAY, (spring_x, coil_y), max(1, int(coil_radius) - 1))
                
                # Spring base and top
                pygame.draw.rect(screen, DARK_GRAY, (spring_x - 6, spring_y, 12, 3))
                pygame.draw.rect(screen, DARK_GRAY, (spring_x - 6, spring_y + coil_height, 12, 3))
            
            # Modern pulsing glow effect
            pulse_intensity = (math.sin(self.animation_frame * 0.15) + 1) / 2
            for i in range(4):
                glow_rect = pygame.Rect(draw_rect.x - i*2, draw_rect.y - i*2,
                                      draw_rect.width + i*4, draw_rect.height + i*4)
                alpha = int((50 + 30 * pulse_intensity) - i * 12)
                glow_surface = pygame.Surface((glow_rect.width, glow_rect.height))
                glow_surface.set_alpha(alpha)
                glow_surface.fill(NEON_GREEN)
                screen.blit(glow_surface, glow_rect)
            
            # Clean modern bounce indicators (stylized arrows)
            indicator_count = max(1, self.rect.width // 50)
            for i in range(indicator_count):
                indicator_x = draw_rect.x + (i + 1) * self.rect.width // (indicator_count + 1)
                indicator_y = draw_rect.y - 15
                
                # Animated bounce indicator
                bounce_offset = math.sin(self.animation_frame * 0.2 + i) * 3
                arrow_y = indicator_y + bounce_offset
                
                # Modern arrow design
                arrow_points = [
                    (indicator_x, arrow_y),
                    (indicator_x - 6, arrow_y + 8),
                    (indicator_x - 3, arrow_y + 8),
                    (indicator_x - 3, arrow_y + 12),
                    (indicator_x + 3, arrow_y + 12),
                    (indicator_x + 3, arrow_y + 8),
                    (indicator_x + 6, arrow_y + 8)
                ]
                
                # Draw arrow with glow
                pygame.draw.polygon(screen, YELLOW, arrow_points)
                pygame.draw.polygon(screen, WHITE, arrow_points, 2)
                
                # Add small glow around arrow
                glow_surf = pygame.Surface((20, 20))
                glow_surf.set_alpha(int(40 + 20 * pulse_intensity))
                glow_surf.fill(YELLOW)
                screen.blit(glow_surf, (indicator_x - 10, arrow_y - 2))
            
            # Top surface highlight
            highlight_rect = pygame.Rect(draw_rect.x + 2, draw_rect.y, draw_rect.width - 4, 4)
            pygame.draw.rect(screen, WHITE, highlight_rect)
        
        elif self.type == "normal":
            # Modern clean block with subtle gradient and depth
            # Create gradient effect from light to dark
            gradient_steps = 8
            step_height = draw_rect.height / gradient_steps
            
            for i in range(gradient_steps):
                # Gradient from lighter at top to darker at bottom
                brightness = 1.0 - (i * 0.15)
                block_color = (
                    max(0, min(255, int(self.color[0] * brightness))),
                    max(0, min(255, int(self.color[1] * brightness))),
                    max(0, min(255, int(self.color[2] * brightness)))
                )
                
                gradient_rect = pygame.Rect(
                    draw_rect.x,
                    draw_rect.y + i * step_height,
                    draw_rect.width,
                    step_height + 1
                )
                pygame.draw.rect(screen, block_color, gradient_rect)
            
            # Add highlight on top edge
            highlight_color = (
                min(255, self.color[0] + 40),
                min(255, self.color[1] + 40),
                min(255, self.color[2] + 40)
            )
            pygame.draw.rect(screen, highlight_color, (draw_rect.x, draw_rect.y, draw_rect.width, 3))
            
            # Add subtle shadow on bottom edge
            shadow_color = (
                max(0, self.color[0] - 40),
                max(0, self.color[1] - 40),
                max(0, self.color[2] - 40)
            )
            pygame.draw.rect(screen, shadow_color, (draw_rect.x, draw_rect.y + draw_rect.height - 3, draw_rect.width, 3))
            
            # Add corner highlights for 3D effect
            pygame.draw.polygon(screen, highlight_color, [
                (draw_rect.x, draw_rect.y),
                (draw_rect.x + 8, draw_rect.y + 8),
                (draw_rect.x, draw_rect.y + 8)
            ])
            pygame.draw.polygon(screen, highlight_color, [
                (draw_rect.x + draw_rect.width, draw_rect.y),
                (draw_rect.x + draw_rect.width - 8, draw_rect.y + 8),
                (draw_rect.x + draw_rect.width, draw_rect.y + 8)
            ])
        
        elif self.type == "ice":
            # Modern ice platform with crystal effect
            # Base ice color with transparency layers
            ice_base = (150, 220, 255)  # Light blue base
            
            # Draw main ice block with gradient
            gradient_steps = 5
            step_height = draw_rect.height / gradient_steps
            
            for i in range(gradient_steps):
                transparency = 0.7 + (i * 0.06)  # Varying transparency
                ice_color = (
                    int(ice_base[0] * transparency),
                    int(ice_base[1] * transparency),
                    int(ice_base[2] * transparency)
                )
                
                gradient_rect = pygame.Rect(
                    draw_rect.x,
                    draw_rect.y + i * step_height,
                    draw_rect.width,
                    step_height + 1
                )
                pygame.draw.rect(screen, ice_color, gradient_rect)
            
            # Add crystalline frost patterns
            frost_points = [
                (draw_rect.x + draw_rect.width * 0.2, draw_rect.y + draw_rect.height * 0.3),
                (draw_rect.x + draw_rect.width * 0.5, draw_rect.y + draw_rect.height * 0.1),
                (draw_rect.x + draw_rect.width * 0.8, draw_rect.y + draw_rect.height * 0.4),
                (draw_rect.x + draw_rect.width * 0.3, draw_rect.y + draw_rect.height * 0.7),
                (draw_rect.x + draw_rect.width * 0.7, draw_rect.y + draw_rect.height * 0.8)
            ]
            
            for point in frost_points:
                # Draw snowflake-like patterns
                center_x, center_y = point
                for angle in range(0, 360, 60):  # 6-pointed snowflake
                    end_x = center_x + math.cos(math.radians(angle)) * 8
                    end_y = center_y + math.sin(math.radians(angle)) * 8
                    pygame.draw.line(screen, WHITE, (center_x, center_y), (end_x, end_y), 1)
                    
                    # Small branches
                    branch_x = center_x + math.cos(math.radians(angle)) * 4
                    branch_y = center_y + math.sin(math.radians(angle)) * 4
                    pygame.draw.line(screen, WHITE, 
                                   (branch_x + 2, branch_y), (branch_x - 2, branch_y), 1)
            
            # Shimmering ice effect with transparency layers
            shimmer_offset = math.sin(self.animation_frame * 0.1) * 10
            for i in range(3):
                shimmer_x = draw_rect.x + (20 + shimmer_offset + i * 15) % draw_rect.width
                if 0 <= shimmer_x <= draw_rect.width - 8:
                    shimmer_surface = pygame.Surface((8, draw_rect.height))
                    shimmer_surface.set_alpha(60 - i * 15)
                    shimmer_surface.fill(WHITE)
                    screen.blit(shimmer_surface, (shimmer_x, draw_rect.y))
            
            # Ice surface highlight
            pygame.draw.rect(screen, WHITE, (draw_rect.x, draw_rect.y, draw_rect.width, 2))
        
        elif self.type == "electric":
            # Modern electric platform with clean energy effects
            # Draw base platform with electric gradient
            gradient_steps = 6
            step_height = draw_rect.height / gradient_steps
            
            for i in range(gradient_steps):
                electric_intensity = 0.6 + math.sin(self.animation_frame * 0.2 + i) * 0.2
                electric_color = (
                    int(YELLOW[0] * electric_intensity),
                    int(YELLOW[1] * electric_intensity),
                    max(0, int(YELLOW[2] * electric_intensity - 50))  # Less blue for warmer yellow
                )
                
                gradient_rect = pygame.Rect(
                    draw_rect.x,
                    draw_rect.y + i * step_height,
                    draw_rect.width,
                    step_height + 1
                )
                pygame.draw.rect(screen, electric_color, gradient_rect)
            
            # Clean electrical conduits/lines across the platform
            conduit_count = 3
            conduit_spacing = draw_rect.height // (conduit_count + 1)
            
            for i in range(conduit_count):
                conduit_y = draw_rect.y + (i + 1) * conduit_spacing
                # Main conduit line
                pygame.draw.line(screen, WHITE, 
                               (draw_rect.x + 5, conduit_y), 
                               (draw_rect.x + draw_rect.width - 5, conduit_y), 2)
                # Electrical flow effect
                flow_offset = (self.animation_frame * 2) % 20
                for x in range(10, draw_rect.width - 10, 20):
                    flow_x = draw_rect.x + x + flow_offset
                    if flow_x < draw_rect.x + draw_rect.width - 5:
                        pygame.draw.circle(screen, CYAN, (int(flow_x), conduit_y), 2)
            
            # Clean electric sparks above platform
            spark_count = 4
            for i in range(spark_count):
                spark_x = draw_rect.x + (i + 1) * draw_rect.width // (spark_count + 1)
                spark_intensity = math.sin(self.animation_frame * 0.3 + i * 1.5) * 0.5 + 0.5
                
                if spark_intensity > 0.7:  # Only show bright sparks
                    spark_y = draw_rect.y - random.randint(3, 8)
                    spark_size = int(3 * spark_intensity)
                    
                    # Main spark
                    pygame.draw.circle(screen, WHITE, (spark_x, spark_y), spark_size)
                    # Glow around spark
                    glow_surf = pygame.Surface((spark_size * 4, spark_size * 4))
                    glow_surf.set_alpha(int(60 * spark_intensity))
                    glow_surf.fill(YELLOW)
                    screen.blit(glow_surf, (spark_x - spark_size * 2, spark_y - spark_size * 2))
            
            # Electric field border effect
            pygame.draw.rect(screen, CYAN, draw_rect, 1)
        
        elif self.type == "boost":
            # Modern speed boost platform with dynamic flow effect
            # Draw base platform with speed gradient
            flow_offset = (self.animation_frame * 3) % (draw_rect.width + 40)
            
            # Base color with gradient
            gradient_steps = 8
            step_width = draw_rect.width / gradient_steps
            
            for i in range(gradient_steps):
                flow_intensity = (math.sin((i / gradient_steps) * math.pi * 2 + self.animation_frame * 0.2) + 1) / 2
                boost_color = (
                    max(0, min(255, int(NEON_BLUE[0] * (0.6 + 0.4 * flow_intensity)))),
                    max(0, min(255, int(NEON_BLUE[1] * (0.6 + 0.4 * flow_intensity)))),
                    max(0, min(255, int(NEON_BLUE[2] * (0.6 + 0.4 * flow_intensity))))
                )
                
                step_rect = pygame.Rect(
                    draw_rect.x + i * step_width,
                    draw_rect.y,
                    step_width + 1,
                    draw_rect.height
                )
                pygame.draw.rect(screen, boost_color, step_rect)
            
            # Speed flow lines across the platform
            flow_lines = 4
            for i in range(flow_lines):
                line_y = draw_rect.y + (i + 1) * draw_rect.height // (flow_lines + 1)
                
                # Moving chevron pattern
                chevron_spacing = 25
                for x in range(-40, draw_rect.width + 40, chevron_spacing):
                    chevron_x = x + flow_offset
                    if -10 <= chevron_x <= draw_rect.width + 10:
                        # Draw speed chevron
                        chevron_points = [
                            (draw_rect.x + chevron_x, line_y),
                            (draw_rect.x + chevron_x + 15, line_y - 3),
                            (draw_rect.x + chevron_x + 15, line_y + 3)
                        ]
                        pygame.draw.polygon(screen, WHITE, chevron_points)
            
            # Boost field glow effect
            for i in range(3):
                glow_rect = pygame.Rect(draw_rect.x - i, draw_rect.y - i,
                                      draw_rect.width + i*2, draw_rect.height + i*2)
                alpha = 40 - i * 10
                glow_surface = pygame.Surface((glow_rect.width, glow_rect.height))
                glow_surface.set_alpha(alpha)
                glow_surface.fill(NEON_BLUE)
                screen.blit(glow_surface, glow_rect)
        
        elif self.type == "spikes":
            # Spikes platform - deadly spikes on top
            spike_count = max(3, self.rect.width // 15)
            spike_width = self.rect.width // spike_count
            
            for i in range(spike_count):
                spike_x = draw_rect.x + i * spike_width
                spike_base_y = draw_rect.y
                spike_tip_x = spike_x + spike_width // 2
                spike_tip_y = draw_rect.y - 12  # Spikes stick up 12 pixels
                
                # Draw individual spike as triangle
                spike_points = [
                    (spike_x, spike_base_y),
                    (spike_x + spike_width, spike_base_y),
                    (spike_tip_x, spike_tip_y)
                ]
                pygame.draw.polygon(screen, RED, spike_points)
                pygame.draw.polygon(screen, DARK_GRAY, spike_points, 2)
                
                # Add danger glow around spikes
                for j in range(2):
                    glow_points = [
                        (spike_x - j, spike_base_y),
                        (spike_x + spike_width + j, spike_base_y),
                        (spike_tip_x, spike_tip_y - j)
                    ]
                    glow_surface = pygame.Surface((spike_width + 2*j, 15 + j))
                    glow_surface.set_alpha(30 - j * 10)
                    pygame.draw.polygon(glow_surface, RED, [(p[0] - spike_x + j, p[1] - spike_tip_y + j) for p in glow_points])
                    screen.blit(glow_surface, (spike_x - j, spike_tip_y - j))
        
        elif self.type == "pulse":
            # Pulsing platform - changes brightness rhythmically
            pulse_color = (
                int(self.color[0] * (0.5 + 0.5 * self.pulse_intensity)),
                int(self.color[1] * (0.5 + 0.5 * self.pulse_intensity)),
                int(self.color[2] * (0.5 + 0.5 * self.pulse_intensity))
            )
            pygame.draw.rect(screen, pulse_color, draw_rect)
            
            # Add pulsing outline
            outline_alpha = int(100 + 155 * self.pulse_intensity)
            outline_surface = pygame.Surface((draw_rect.width + 4, draw_rect.height + 4))
            outline_surface.set_alpha(outline_alpha)
            pygame.draw.rect(outline_surface, PULSE_PURPLE, (0, 0, draw_rect.width + 4, draw_rect.height + 4))
            screen.blit(outline_surface, (draw_rect.x - 2, draw_rect.y - 2))
        
        elif self.type == "shimmer":
            # Shimmering platform - moving light bands
            for i in range(3):
                shimmer_x = (self.shimmer_offset + i * 2) % (self.rect.width + 20) - 10
                if 0 <= shimmer_x <= self.rect.width:
                    shimmer_rect = pygame.Rect(draw_rect.x + shimmer_x - 5, draw_rect.y, 10, draw_rect.height)
                    shimmer_surface = pygame.Surface((10, draw_rect.height))
                    shimmer_surface.set_alpha(80 - i * 20)
                    shimmer_surface.fill(WHITE)
                    screen.blit(shimmer_surface, (draw_rect.x + shimmer_x - 5, draw_rect.y))
        
        elif self.type == "rainbow":
            # Rainbow platform - cycles through colors
            rainbow_color = pygame.Color(0)
            rainbow_color.hsva = (self.rainbow_hue, 100, 100, 100)
            rainbow_rgb = (rainbow_color.r, rainbow_color.g, rainbow_color.b)
            pygame.draw.rect(screen, rainbow_rgb, draw_rect)
            
            # Add rainbow sparkles
            for i in range(5):
                sparkle_x = draw_rect.x + random.randint(5, draw_rect.width - 5)
                sparkle_y = draw_rect.y + random.randint(5, draw_rect.height - 5)
                sparkle_hue = (self.rainbow_hue + i * 72) % 360
                sparkle_color = pygame.Color(0)
                sparkle_color.hsva = (sparkle_hue, 100, 100, 100)
                pygame.draw.circle(screen, (sparkle_color.r, sparkle_color.g, sparkle_color.b), 
                                 (sparkle_x, sparkle_y), 2)
        
        elif self.type == "glow":
            # Glowing platform - radiating light effect
            for i in range(5):
                glow_rect = pygame.Rect(draw_rect.x - i*2, draw_rect.y - i*2,
                                      draw_rect.width + i*4, draw_rect.height + i*4)
                alpha = 60 - i * 10
                glow_surface = pygame.Surface((glow_rect.width, glow_rect.height))
                glow_surface.set_alpha(alpha)
                glow_surface.fill(NEON_PINK)
                screen.blit(glow_surface, glow_rect)
        
        elif self.type == "wave":
            # Wave platform - undulating surface
            wave_points = []
            wave_segments = max(4, self.rect.width // 20)
            for i in range(wave_segments + 1):
                x = draw_rect.x + (i * self.rect.width // wave_segments)
                wave_height = math.sin(self.wave_offset + i * 0.5) * 3
                y = draw_rect.y + wave_height
                wave_points.append((x, y))
            
            # Complete the wave shape
            wave_points.append((draw_rect.x + draw_rect.width, draw_rect.y + draw_rect.height))
            wave_points.append((draw_rect.x, draw_rect.y + draw_rect.height))
            
            if len(wave_points) >= 3:
                pygame.draw.polygon(screen, self.color, wave_points)
        
        elif self.type == "gradient":
            # Gradient platform - smooth color transition
            gradient_steps = max(4, draw_rect.width // 8)
            step_width = draw_rect.width / gradient_steps
            
            for i in range(gradient_steps):
                # Interpolate between gradient colors with animation
                progress = (i / gradient_steps + math.sin(self.animation_frame * 0.05) * 0.3) % 1.0
                
                r = int(GRADIENT_START[0] * (1 - progress) + GRADIENT_END[0] * progress)
                g = int(GRADIENT_START[1] * (1 - progress) + GRADIENT_END[1] * progress)
                b = int(GRADIENT_START[2] * (1 - progress) + GRADIENT_END[2] * progress)
                
                step_rect = pygame.Rect(
                    draw_rect.x + i * step_width,
                    draw_rect.y,
                    step_width + 1,  # +1 to avoid gaps
                    draw_rect.height
                )
                pygame.draw.rect(screen, (r, g, b), step_rect)
        
        elif self.type == "spiral":
            # Spiral platform - rotating spiral pattern
            pygame.draw.rect(screen, self.color, draw_rect)
            center_x = draw_rect.x + draw_rect.width // 2
            center_y = draw_rect.y + draw_rect.height // 2
            max_radius = min(draw_rect.width, draw_rect.height) // 2 - 5
            
            # Draw animated spiral
            for i in range(0, 360, 15):
                angle = math.radians(i + self.spiral_angle * 10)
                radius = (i / 360) * max_radius
                x = center_x + math.cos(angle) * radius
                y = center_y + math.sin(angle) * radius
                spiral_color = (
                    max(0, min(255, int(self.color[0] + 50 * math.sin(angle)))),
                    max(0, min(255, int(self.color[1] + 50 * math.cos(angle)))),
                    max(0, min(255, int(self.color[2] + 50 * math.sin(angle * 2))))
                )
                pygame.draw.circle(screen, spiral_color, (int(x), int(y)), 3)
        
        elif self.type == "matrix":
            # Matrix rain effect platform
            pygame.draw.rect(screen, (0, 20, 0), draw_rect)  # Dark green background
            
            # Draw matrix rain
            for i, drop_y in enumerate(self.matrix_drops):
                x = draw_rect.x + i * 10
                if x < draw_rect.x + draw_rect.width:
                    # Draw multiple characters in the drop
                    for j in range(5):
                        char_y = draw_rect.y + (drop_y - j * 8) % (draw_rect.height + 20)
                        if draw_rect.y <= char_y <= draw_rect.y + draw_rect.height:
                            brightness = max(0, 255 - j * 40)
                            color = (0, brightness, 0)
                            pygame.draw.circle(screen, color, (x, int(char_y)), 2)
        
        elif self.type == "lava":
            # Lava platform with bubbling effect
            pygame.draw.rect(screen, self.color, draw_rect)
            
            # Draw lava bubbles
            for bubble in self.lava_bubbles:
                bubble_x = draw_rect.x + bubble['x']
                bubble_y = draw_rect.y + bubble['y']
                size = bubble['size']
                alpha = int(255 * (bubble['life'] / 40))
                
                # Create bubble surface with alpha
                bubble_surface = pygame.Surface((size * 2, size * 2))
                bubble_surface.set_alpha(alpha)
                bubble_color = (255, min(255, self.color[1] + 100), 0)  # Bright orange
                pygame.draw.circle(bubble_surface, bubble_color, (size, size), size)
                screen.blit(bubble_surface, (bubble_x - size, bubble_y - size))
        
        elif self.type == "crystal":
            # Crystal platform with faceted appearance
            pygame.draw.rect(screen, self.color, draw_rect)
            
            # Draw crystal facets
            center_x = draw_rect.x + draw_rect.width // 2
            center_y = draw_rect.y + draw_rect.height // 2
            
            for i in range(self.crystal_facets):
                angle = (2 * math.pi * i / self.crystal_facets) + self.animation_frame * 0.01
                facet_length = min(draw_rect.width, draw_rect.height) // 3
                
                end_x = center_x + math.cos(angle) * facet_length
                end_y = center_y + math.sin(angle) * facet_length
                
                # Facet color with slight variation
                facet_intensity = (math.sin(angle + self.animation_frame * 0.05) + 1) / 2
                facet_color = (
                    max(0, min(255, int(self.color[0] * (0.7 + 0.3 * facet_intensity)))),
                    max(0, min(255, int(self.color[1] * (0.7 + 0.3 * facet_intensity)))),
                    max(0, min(255, int(self.color[2] * (0.7 + 0.3 * facet_intensity))))
                )
                
                pygame.draw.line(screen, facet_color, (center_x, center_y), (int(end_x), int(end_y)), 2)
                pygame.draw.circle(screen, WHITE, (int(end_x), int(end_y)), 2)
        
        elif self.type == "galaxy":
            # Galaxy platform with moving stars
            pygame.draw.rect(screen, (10, 10, 30), draw_rect)  # Dark space background
            
            # Draw moving stars
            for i, (star_x, star_y) in enumerate(self.galaxy_stars):
                screen_x = draw_rect.x + int(star_x)
                screen_y = draw_rect.y + int(star_y)
                
                # Different star sizes and colors
                star_size = 1 + (i % 3)
                star_brightness = 150 + int(50 * math.sin(self.animation_frame * 0.1 + i))
                star_color = (star_brightness, star_brightness, 255)
                
                pygame.draw.circle(screen, star_color, (screen_x, screen_y), star_size)
                
                # Add twinkling effect
                if random.random() < 0.1:
                    pygame.draw.circle(screen, WHITE, (screen_x, screen_y), star_size + 1)
        
        elif self.type == "disco":
            # Disco ball effect platform
            pygame.draw.rect(screen, self.color, draw_rect)
            
            # Draw rotating disco squares
            square_size = 8
            for x in range(0, draw_rect.width, square_size * 2):
                for y in range(0, draw_rect.height, square_size * 2):
                    square_x = draw_rect.x + x
                    square_y = draw_rect.y + y
                    
                    # Rotating brightness based on position and time
                    brightness_factor = (math.sin(self.disco_rotation * 0.1 + x * 0.1 + y * 0.1) + 1) / 2
                    square_color = (
                        max(0, min(255, int(self.color[0] * brightness_factor))),
                        max(0, min(255, int(self.color[1] * brightness_factor))),
                        max(0, min(255, int(self.color[2] * brightness_factor)))
                    )
                    
                    pygame.draw.rect(screen, square_color, 
                                   (square_x, square_y, square_size, square_size))
                    
                    # Add reflective highlights
                    if brightness_factor > 0.8:
                        pygame.draw.rect(screen, WHITE, 
                                       (square_x + 2, square_y + 2, square_size - 4, square_size - 4))
        
        elif self.type == "electric_storm":
            # Electric storm platform with lightning
            pygame.draw.rect(screen, (10, 10, 40), draw_rect)  # Dark background
            
            # Draw electric sparks
            for spark in self.electric_sparks:
                spark_x = draw_rect.x + spark['x']
                spark_y = draw_rect.y + spark['y']
                
                # Main spark
                spark_intensity = spark['life'] / 15
                spark_color = (
                    max(0, min(255, int(255 * spark_intensity))),
                    max(0, min(255, int(255 * spark_intensity))),
                    255
                )
                
                pygame.draw.circle(screen, spark_color, (spark_x, spark_y), 3)
                
                # Draw branching lightning
                for i in range(3):
                    branch_x = spark_x + random.randint(-15, 15)
                    branch_y = spark_y + random.randint(-15, 15)
                    if (draw_rect.x <= branch_x <= draw_rect.x + draw_rect.width and 
                        draw_rect.y <= branch_y <= draw_rect.y + draw_rect.height):
                        pygame.draw.line(screen, spark_color, 
                                       (spark_x, spark_y), (branch_x, branch_y), 1)
        
        elif self.type == "glitch":
            # Glitching platform with digital corruption
            base_rect = pygame.Rect(draw_rect.x + self.glitch_offset, draw_rect.y, 
                                  draw_rect.width, draw_rect.height)
            
            # Draw base platform with glitch offset
            pygame.draw.rect(screen, self.color, base_rect)
            
            # Add glitch lines
            if random.random() < 0.3:
                for i in range(5):
                    line_y = draw_rect.y + random.randint(0, draw_rect.height)
                    line_width = random.randint(5, draw_rect.width // 2)
                    line_x = draw_rect.x + random.randint(0, draw_rect.width - line_width)
                    
                    glitch_color = (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255)
                    )
                    
                    pygame.draw.rect(screen, glitch_color, 
                                   (line_x, line_y, line_width, 2))
            
            # Add static noise
            for _ in range(10):
                noise_x = draw_rect.x + random.randint(0, draw_rect.width)
                noise_y = draw_rect.y + random.randint(0, draw_rect.height)
                noise_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                pygame.draw.circle(screen, noise_color, (noise_x, noise_y), 1)
        
        # Draw border
        pygame.draw.rect(screen, BLACK, draw_rect, 2)
        
        # Add movement indicators for moving platforms
        if self.moving:
            # Draw directional arrow indicators
            arrow_y = draw_rect.y - 5
            arrow_spacing = draw_rect.width // 4
            
            for i in range(3):
                arrow_x = draw_rect.x + arrow_spacing + i * arrow_spacing
                
                # Direction arrow based on current movement
                if self.move_direction > 0:  # Moving right
                    arrow_points = [
                        (arrow_x - 4, arrow_y - 3),
                        (arrow_x + 4, arrow_y),
                        (arrow_x - 4, arrow_y + 3)
                    ]
                else:  # Moving left
                    arrow_points = [
                        (arrow_x + 4, arrow_y - 3),
                        (arrow_x - 4, arrow_y),
                        (arrow_x + 4, arrow_y + 3)
                    ]
                
                # Animated opacity for movement indication
                opacity = int(100 + 100 * math.sin(self.animation_frame * 0.15 + i * 0.5))
                arrow_surf = pygame.Surface((10, 8))
                arrow_surf.set_alpha(opacity)
                pygame.draw.polygon(arrow_surf, YELLOW, 
                                  [(p[0] - arrow_x + 5, p[1] - arrow_y + 4) for p in arrow_points])
                screen.blit(arrow_surf, (arrow_x - 5, arrow_y - 4))

class Collectible:
    def __init__(self, x, y, collectible_type="coin"):
        self.x = x
        self.y = y
        self.type = collectible_type
        self.collected = False
        self.animation_offset = 0
        self.color = self.get_color()
        self.value = self.get_value()
        self.size = 15
        
    def get_color(self):
        colors = {
            "coin": GOLD,
            "gem": PURPLE,
            "speed_boost": NEON_BLUE,
            "jump_boost": NEON_GREEN,
            "shield": SILVER,
            "dash_orb": NEON_PINK,
            "gravity_orb": ORANGE,
            "magnet_orb": CYAN,
            "time_orb": YELLOW,
            "health_orb": RED,
            "multi_jump_orb": LIGHT_BLUE,
            "phantom_orb": (150, 150, 255),
            "rage_orb": (255, 50, 50),
            "ice_orb": (200, 255, 255),
            "fire_orb": (255, 100, 0),
            "shield_orb": (192, 192, 255),
            "speed_orb": (0, 255, 127),
            "size_orb": (255, 182, 193),
            "bounce_orb": (255, 140, 0),
            "lightning_orb": (255, 255, 0),
            "diamond_orb": (185, 242, 255),
            "life_orb": (255, 20, 147)  # Deep pink for extra life
        }
        return colors.get(self.type, GOLD)
    
    def get_value(self):
        values = {
            "coin": 10,
            "gem": 50,
            "speed_boost": 0,
            "jump_boost": 0,
            "shield": 0,
            "dash_orb": 0,
            "gravity_orb": 0,
            "magnet_orb": 0,
            "time_orb": 0,
            "health_orb": 0,
            "multi_jump_orb": 0,
            "phantom_orb": 0,
            "rage_orb": 0,
            "ice_orb": 0,
            "fire_orb": 0,
            "shield_orb": 0,
            "speed_orb": 0,
            "size_orb": 0,
            "bounce_orb": 0,
            "lightning_orb": 0,
            "diamond_orb": 0,
            "life_orb": 0  # No score value, just gives extra life
        }
        return values.get(self.type, 10)
    
    def update(self):
        self.animation_offset += 0.2
        self.y += math.sin(self.animation_offset) * 0.5
    
    def draw(self, screen, camera_x):
        if not self.collected:
            x = int(self.x - camera_x)
            y = int(self.y + math.sin(self.animation_offset) * 3)
            
            # Draw glow effect
            for i in range(3):
                size = self.size + i * 2
                alpha = 30 - i * 10
                glow_surface = pygame.Surface((size * 2, size * 2))
                glow_surface.set_alpha(alpha)
                glow_surface.fill(self.color)
                screen.blit(glow_surface, (x - size, y - size))
            
            # Draw main collectible
            pygame.draw.circle(screen, self.color, (x, y), self.size)
            
            # Special effects for power orbs
            if "orb" in self.type:
                # Rotating inner circle
                inner_color = (min(255, self.color[0] + 50), min(255, self.color[1] + 50), min(255, self.color[2] + 50))
                inner_size = int(self.size * 0.6 + math.sin(self.animation_offset * 2) * 3)
                pygame.draw.circle(screen, inner_color, (x, y), inner_size)
                
                # Special heart shape for life orb
                if self.type == "life_orb":
                    # Draw heart shape with two circles for the top and a triangle for the bottom
                    heart_size = self.size // 2
                    # Top left circle
                    pygame.draw.circle(screen, WHITE, (x - heart_size//2, y - heart_size//3), heart_size//2)
                    # Top right circle  
                    pygame.draw.circle(screen, WHITE, (x + heart_size//2, y - heart_size//3), heart_size//2)
                    # Bottom triangle point
                    heart_points = [
                        (x - heart_size, y),
                        (x + heart_size, y),
                        (x, y + heart_size)
                    ]
                    pygame.draw.polygon(screen, WHITE, heart_points)
                else:
                    # Sparkle effect for other orbs
                    for i in range(3):
                        sparkle_x = x + math.cos(self.animation_offset + i * 2) * (self.size - 5)
                        sparkle_y = y + math.sin(self.animation_offset + i * 2) * (self.size - 5)
                        pygame.draw.circle(screen, WHITE, (int(sparkle_x), int(sparkle_y)), 2)
            
            pygame.draw.circle(screen, WHITE, (x, y), self.size, 2)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, 
                          self.size * 2, self.size * 2)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.on_wall = False
        self.wall_side = 0  # -1 for left wall, 1 for right wall
        self.can_wall_jump = True
        self.jump_buffer = 0
        self.coyote_time = 0
        self.dash_cooldown = 0
        self.dash_power = 20
        self.facing_right = True
        self.last_platform_type = "normal"  # Track last touched platform type
        
        # Advanced abilities
        self.double_jump_available = True
        self.triple_jump_available = False
        self.wall_slide_speed = 3
        self.speed_boost_timer = 0
        self.jump_boost_timer = 0
        self.shield_timer = 0
        self.magnet_timer = 0
        
        # New power-up timers
        self.dash_orb_timer = 0
        self.gravity_orb_timer = 0
        self.magnet_orb_timer = 0
        self.time_orb_timer = 0
        self.health_orb_timer = 0
        self.multi_jump_orb_timer = 0
        self.phantom_orb_timer = 0
        self.rage_orb_timer = 0
        self.ice_orb_timer = 0
        self.fire_orb_timer = 0
        self.shield_orb_timer = 0
        self.speed_orb_timer = 0
        self.size_orb_timer = 0
        self.bounce_orb_timer = 0
        self.lightning_orb_timer = 0
        self.diamond_orb_timer = 0
        
        # Power-up states
        self.infinite_dashes = False
        self.low_gravity = False
        self.super_magnet = False
        self.slow_motion = False
        self.phantom_mode = False
        self.rage_mode = False
        self.ice_mode = False
        self.fire_mode = False
        self.shield_mode = False
        self.super_speed = False
        self.giant_mode = False
        self.bounce_mode = False
        self.lightning_mode = False
        self.diamond_mode = False
        self.bonus_jumps = 0
        
        # Upgrades
        self.has_triple_jump = False
        self.has_super_dash = False
        self.has_coin_magnet = False
        self.has_super_shield = False
        self.speed_upgrade = 0  # Percentage increase
        self.jump_upgrade = 0   # Percentage increase
        
        # Stats tracking
        self.score = 0
        self.coins = 0
        self.gems = 0
        self.deaths = 0
        self.lives = 3  # Start with 3 lives
        self.max_lives = 5  # Maximum lives possible
        self.wall_jumps = 0
        self.max_speed_count = 0
        self.survival_time = 0
        self.puzzles_solved = 0
        self.bosses_defeated = 0
        self.secrets_found = 0
        self.perfect_runs = 0
        self.current_skin = 'default'
        
        # Health system
        self.max_health = 100
        self.health = self.max_health
        
        # Game state
        self.best_time = 0
        self.start_time = time.time()
        self.last_checkpoint = None
        self.invulnerable_timer = 0
        
        # Animation
        self.animation_frame = 0
        self.trail_timer = 0
        
        # Color effects
        self.base_color = PLAYER_SKINS[self.current_skin]['color']
        self.current_color = self.base_color
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self, platforms, collectibles, particle_system, game=None):
        self.animation_frame += 1
        
        # Update timers
        if self.jump_buffer > 0:
            self.jump_buffer -= 1
        if self.coyote_time > 0:
            self.coyote_time -= 1
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
        if self.jump_boost_timer > 0:
            self.jump_boost_timer -= 1
        if self.shield_timer > 0:
            self.shield_timer -= 1
        if self.magnet_timer > 0:
            self.magnet_timer -= 1
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
        
        # Handle new power-up timers
        if self.dash_orb_timer > 0:
            self.dash_orb_timer -= 1
            if self.dash_orb_timer == 0:
                self.infinite_dashes = False
        
        if self.gravity_orb_timer > 0:
            self.gravity_orb_timer -= 1
            if self.gravity_orb_timer == 0:
                self.low_gravity = False
        
        if self.magnet_orb_timer > 0:
            self.magnet_orb_timer -= 1
            if self.magnet_orb_timer == 0:
                self.super_magnet = False
        
        if self.time_orb_timer > 0:
            self.time_orb_timer -= 1
            if self.time_orb_timer == 0:
                self.slow_motion = False
        
        if self.health_orb_timer > 0:
            self.health_orb_timer -= 1
        
        if self.multi_jump_orb_timer > 0:
            self.multi_jump_orb_timer -= 1
            if self.multi_jump_orb_timer == 0:
                self.bonus_jumps = 0
        
        if self.phantom_orb_timer > 0:
            self.phantom_orb_timer -= 1
            if self.phantom_orb_timer == 0:
                self.phantom_mode = False
        
        if self.rage_orb_timer > 0:
            self.rage_orb_timer -= 1
            if self.rage_orb_timer == 0:
                self.rage_mode = False
        
        if self.ice_orb_timer > 0:
            self.ice_orb_timer -= 1
            if self.ice_orb_timer == 0:
                self.ice_mode = False
        
        if self.fire_orb_timer > 0:
            self.fire_orb_timer -= 1
            if self.fire_orb_timer == 0:
                self.fire_mode = False
        
        # New power-up timer updates
        if self.shield_orb_timer > 0:
            self.shield_orb_timer -= 1
            if self.shield_orb_timer == 0:
                self.shield_mode = False
        
        if self.speed_orb_timer > 0:
            self.speed_orb_timer -= 1
            if self.speed_orb_timer == 0:
                self.super_speed = False
        
        if self.size_orb_timer > 0:
            self.size_orb_timer -= 1
            if self.size_orb_timer == 0:
                self.giant_mode = False
                self.width = PLAYER_SIZE
                self.height = PLAYER_SIZE
        
        if self.bounce_orb_timer > 0:
            self.bounce_orb_timer -= 1
            if self.bounce_orb_timer == 0:
                self.bounce_mode = False
        
        if self.lightning_orb_timer > 0:
            self.lightning_orb_timer -= 1
            if self.lightning_orb_timer == 0:
                self.lightning_mode = False
        
        if self.diamond_orb_timer > 0:
            self.diamond_orb_timer -= 1
            if self.diamond_orb_timer == 0:
                self.diamond_mode = False
        
        # Track survival time
        self.survival_time += 1
        
        # Update color based on abilities and skin
        if self.current_skin == 'rainbow':
            # Rainbow effect
            hue = (self.animation_frame * 2) % 360
            self.current_color = pygame.Color(0)
            self.current_color.hsva = (hue, 100, 100, 100)
            self.current_color = (self.current_color.r, self.current_color.g, self.current_color.b)
        elif self.fire_mode:
            self.current_color = (255, 100, 0)  # Fire orange
        elif self.ice_mode:
            self.current_color = (200, 255, 255)  # Ice blue
        elif self.rage_mode:
            self.current_color = (255, 50, 50)  # Rage red
        elif self.phantom_mode:
            self.current_color = (150, 150, 255)  # Phantom purple
        elif self.low_gravity:
            self.current_color = ORANGE  # Gravity orb orange
        elif self.shield_mode:
            self.current_color = (192, 192, 255)  # Light purple
        elif self.super_speed:
            self.current_color = (0, 255, 127)  # Spring green
        elif self.giant_mode:
            self.current_color = (255, 182, 193)  # Light pink
        elif self.bounce_mode:
            self.current_color = (255, 140, 0)  # Dark orange
        elif self.lightning_mode:
            self.current_color = (255, 255, 0)  # Bright yellow
        elif self.diamond_mode:
            self.current_color = (185, 242, 255)  # Diamond blue
        elif self.shield_timer > 0:
            self.current_color = SILVER
        elif self.speed_boost_timer > 0:
            self.current_color = NEON_BLUE
        elif self.jump_boost_timer > 0:
            self.current_color = NEON_GREEN
        elif self.infinite_dashes:
            self.current_color = NEON_PINK
        elif self.super_magnet:
            self.current_color = CYAN
        else:
            self.current_color = self.base_color
        
        # Apply gravity
        if not self.on_ground:
            gravity_force = GRAVITY
            if self.low_gravity:
                gravity_force *= 0.3  # Reduced gravity when low_gravity is active
            self.vel_y += gravity_force
            
            # Wall sliding
            if self.on_wall and self.vel_y > 0:
                self.vel_y = min(self.vel_y, self.wall_slide_speed)
        
        # Apply movement
        old_x = self.x
        old_y = self.y
        
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Check collisions
        self.check_collisions(platforms, particle_system)
        
        # Check collectibles
        self.check_collectibles(collectibles, particle_system, game)
        
        # Coin magnet effect
        if self.has_coin_magnet or self.magnet_timer > 0:
            self.apply_coin_magnet(collectibles)
        
        # Check max speed achievement
        if abs(self.vel_x) >= MAX_SPEED * 0.9:
            self.max_speed_count += 1
        
        # Add movement trail
        self.trail_timer += 1
        if self.trail_timer > 3 and (abs(self.vel_x) > 2 or abs(self.vel_y) > 2):
            particle_system.add_trail(self.x + self.width/2, self.y + self.height/2, self.current_color)
            self.trail_timer = 0
        
        # Ground detection for coyote time
        if self.on_ground:
            self.coyote_time = 6
            self.double_jump_available = True
        
        # Death check
        if self.y > WINDOW_HEIGHT + 100:
            self.die(particle_system)
    
    def check_collisions(self, platforms, particle_system):
        """Check collisions with platforms"""
        player_rect = self.get_rect()
        self.on_ground = False
        self.on_wall = False
        
        # Check ground collision first
        if self.y >= GROUND_LEVEL - self.height:
            self.y = GROUND_LEVEL - self.height
            self.vel_y = 0
            self.on_ground = True
            self.can_wall_jump = True
        
        # Check ceiling collision
        if self.y <= 0:
            self.y = 0
            self.vel_y = max(0, self.vel_y)  # Stop upward movement, allow falling
        
        # Check left screen boundary (prevent going behind start)
        if self.x <= 0:
            self.x = 0
            self.vel_x = max(0, self.vel_x)  # Stop leftward movement
        
        # Check platform collisions
        for platform in platforms:
            if platform.rect.colliderect(player_rect):
                # Determine collision side
                overlap_left = player_rect.right - platform.rect.left
                overlap_right = platform.rect.right - player_rect.left
                overlap_top = player_rect.bottom - platform.rect.top
                overlap_bottom = platform.rect.bottom - player_rect.top
                
                min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
                
                if min_overlap == overlap_top and self.vel_y > 0:
                    # Landing on top of platform
                    self.y = platform.rect.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    self.can_wall_jump = True
                    self.last_platform_type = platform.type  # Remember platform type
                    
                    # Check if this is a bouncy platform (trampoline)
                    if platform.type in ["trampoline", "spring", "moving_trampoline"]:
                        # TRAMPOLINE BOUNCE EFFECT only for bouncy platforms!
                        bounce_power = 30 + random.randint(-5, 10)  # Variable bounce
                        if self.bounce_mode:
                            bounce_power *= 1.5  # Extra bounce with bounce orb
                        self.vel_y = -bounce_power
                        self.speed_boost_timer = 120  # 2 seconds speed boost
                        
                        # Add bouncy particle effects
                        for _ in range(20):
                            particle_system.add_explosion(
                                self.x + self.width/2 + random.randint(-20, 20), 
                                platform.rect.top, 
                                NEON_GREEN
                            )
                    elif platform.type == "boost":
                        # Speed boost platform
                        self.speed_boost_timer = 180  # 3 seconds speed boost
                        for _ in range(10):
                            particle_system.add_explosion(
                                self.x + self.width/2 + random.randint(-15, 15), 
                                platform.rect.top, 
                                NEON_BLUE
                            )
                    elif platform.type == "electric":
                        # Electric platform - gives damage but also lightning power temporarily
                        if not self.shield_timer and not self.shield_mode and not self.diamond_mode:
                            # Take damage if not protected
                            self.health = max(0, self.health - 10)
                            if self.health <= 0:
                                self.die(particle_system)
                        else:
                            # Protected - just get lightning boost
                            self.lightning_orb_timer = 120  # 2 seconds lightning mode
                            self.lightning_mode = True
                        
                        # Electric effects
                        for _ in range(15):
                            particle_system.add_explosion(
                                self.x + self.width/2 + random.randint(-25, 25), 
                                platform.rect.top, 
                                YELLOW
                            )
                    elif platform.type == "spikes":
                        # Spikes platform - deadly to touch from any side
                        if not self.shield_timer and not self.shield_mode and not self.diamond_mode:
                            # Instant death from spikes if not protected
                            self.die(particle_system)
                        else:
                            # Protected - bounce away from spikes
                            self.vel_y = -15  # Bounce up to avoid spikes
                            self.invulnerable_timer = 60  # 1 second invulnerability
                        
                        # Spike damage effects
                        for _ in range(25):
                            particle_system.add_explosion(
                                self.x + self.width/2 + random.randint(-30, 30), 
                                platform.rect.top, 
                                RED
                            )
                    else:
                        # Regular platform - no bounce, just normal landing
                        # Add small dust particles for normal landing
                        for _ in range(5):
                            particle_system.add_landing(
                                self.x + self.width/2 + random.randint(-10, 10), 
                                platform.rect.top
                            )
                    
                elif min_overlap == overlap_bottom and self.vel_y < 0:
                    # Hitting platform from below
                    if platform.type == "spikes":
                        # Spikes hurt even when hit from below
                        if not self.shield_timer and not self.shield_mode and not self.diamond_mode:
                            self.die(particle_system)
                        else:
                            # Protected - bounce away
                            self.vel_y = 5  # Bounce down
                            self.invulnerable_timer = 60
                        
                        # Spike damage effects
                        for _ in range(15):
                            particle_system.add_explosion(
                                self.x + self.width/2 + random.randint(-20, 20), 
                                platform.rect.bottom, 
                                RED
                            )
                    else:
                        self.y = platform.rect.bottom
                        self.vel_y = 0
                    
                elif min_overlap in [overlap_left, overlap_right]:
                    # Wall collision
                    if platform.type == "spikes":
                        # Spikes hurt from the sides too
                        if not self.shield_timer and not self.shield_mode and not self.diamond_mode:
                            self.die(particle_system)
                        else:
                            # Protected - push away from spikes
                            if overlap_left < overlap_right:
                                self.vel_x = -10  # Push left
                            else:
                                self.vel_x = 10   # Push right
                            self.invulnerable_timer = 60
                        
                        # Spike damage effects
                        for _ in range(15):
                            particle_system.add_explosion(
                                self.x + self.width/2, 
                                self.y + self.height/2, 
                                RED
                            )
                    else:
                        if overlap_left < overlap_right:
                            # Hit left side of platform
                            self.x = platform.rect.left - self.width
                            self.wall_side = -1
                        else:
                            # Hit right side of platform
                            self.x = platform.rect.right
                            self.wall_side = 1
                        
                        self.on_wall = True
                        if abs(self.vel_y) > 2:  # Only wall slide if moving fast enough
                            self.vel_x = 0
    
    def check_collectibles(self, collectibles, particle_system, game=None):
        """Check collisions with collectibles"""
        player_rect = self.get_rect()
        
        for collectible in collectibles:
            if not collectible.collected and player_rect.colliderect(collectible.get_rect()):
                collectible.collected = True
                
                # Notify game if an orb was collected
                if game:
                    game.check_orb_collected(collectible.type)
                
                # Apply collectible effects
                if collectible.type == "coin":
                    self.coins += 1
                    self.score += collectible.value
                elif collectible.type == "gem":
                    self.gems += 1
                    self.score += collectible.value
                elif collectible.type == "speed_boost":
                    self.speed_boost_timer = 300  # 5 seconds
                elif collectible.type == "jump_boost":
                    self.jump_boost_timer = 300  # 5 seconds
                elif collectible.type == "shield":
                    self.shield_timer = 600  # 10 seconds
                elif collectible.type == "dash_orb":
                    self.dash_orb_timer = 450  # 7.5 seconds of infinite dashes
                    self.infinite_dashes = True
                elif collectible.type == "gravity_orb":
                    self.gravity_orb_timer = 360  # 6 seconds of low gravity
                    self.low_gravity = True
                elif collectible.type == "magnet_orb":
                    self.magnet_orb_timer = 600  # 10 seconds of super magnet
                    self.super_magnet = True
                elif collectible.type == "time_orb":
                    self.time_orb_timer = 300  # 5 seconds of slow motion
                    self.slow_motion = True
                elif collectible.type == "health_orb":
                    self.health_orb_timer = 1  # Instant health restore
                    self.health = min(self.max_health, self.health + 50)
                elif collectible.type == "multi_jump_orb":
                    self.multi_jump_orb_timer = 450  # 7.5 seconds of extra jumps
                    self.bonus_jumps = 3
                elif collectible.type == "phantom_orb":
                    self.phantom_orb_timer = 240  # 4 seconds of phase through enemies
                    self.phantom_mode = True
                elif collectible.type == "rage_orb":
                    self.rage_orb_timer = 360  # 6 seconds of increased damage/speed
                    self.rage_mode = True
                elif collectible.type == "ice_orb":
                    self.ice_orb_timer = 300  # 5 seconds of ice trail/freeze enemies
                    self.ice_mode = True
                elif collectible.type == "fire_orb":
                    self.fire_orb_timer = 300  # 5 seconds of fire trail/burn enemies
                    self.fire_mode = True
                elif collectible.type == "shield_orb":
                    self.shield_orb_timer = 480  # 8 seconds of enhanced shield
                    self.shield_mode = True
                elif collectible.type == "speed_orb":
                    self.speed_orb_timer = 360  # 6 seconds of super speed
                    self.super_speed = True
                elif collectible.type == "size_orb":
                    self.size_orb_timer = 300  # 5 seconds of giant mode
                    self.giant_mode = True
                    self.width = PLAYER_SIZE * 1.5
                    self.height = PLAYER_SIZE * 1.5
                elif collectible.type == "bounce_orb":
                    self.bounce_orb_timer = 420  # 7 seconds of enhanced bouncing
                    self.bounce_mode = True
                elif collectible.type == "lightning_orb":
                    self.lightning_orb_timer = 240  # 4 seconds of lightning powers
                    self.lightning_mode = True
                elif collectible.type == "diamond_orb":
                    self.diamond_orb_timer = 600  # 10 seconds of diamond hardness
                    self.diamond_mode = True
                elif collectible.type == "life_orb":
                    self.add_life()  # Gain an extra life
                
                # Particle effect
                particle_system.add_explosion(collectible.x, collectible.y, collectible.color)
    
    def apply_coin_magnet(self, collectibles):
        """Attract nearby collectibles"""
        magnet_range = 100
        player_center = Vector2(self.x + self.width/2, self.y + self.height/2)
        
        for collectible in collectibles:
            if not collectible.collected and collectible.type in ['coin', 'gem']:
                collectible_pos = Vector2(collectible.x, collectible.y)
                distance = (player_center - collectible_pos).magnitude()
                
                if distance < magnet_range:
                    # Pull collectible towards player
                    direction = (player_center - collectible_pos).normalize()
                    pull_force = 5 * (1 - distance / magnet_range)
                    collectible.x += direction.x * pull_force
                    collectible.y += direction.y * pull_force
    
    def set_checkpoint(self, checkpoint):
        """Set a new checkpoint"""
        self.last_checkpoint = checkpoint
        checkpoint.activate()
    
    def respawn_at_checkpoint(self):
        """Respawn at last checkpoint"""
        if self.last_checkpoint:
            self.x = self.last_checkpoint.x
            self.y = self.last_checkpoint.y - self.height
        else:
            self.x = 100
            self.y = GROUND_LEVEL - self.height
        
        self.vel_x = 0
        self.vel_y = 0
        self.invulnerable_timer = 120  # 2 seconds of invulnerability
    
    def unlock_skin(self, skin_id):
        """Unlock a new skin"""
        if skin_id in PLAYER_SKINS and not PLAYER_SKINS[skin_id]['unlocked']:
            PLAYER_SKINS[skin_id]['unlocked'] = True
            return True
        return False
    
    def change_skin(self, skin_id):
        """Change current skin"""
        if skin_id in PLAYER_SKINS and PLAYER_SKINS[skin_id]['unlocked']:
            self.current_skin = skin_id
            self.base_color = PLAYER_SKINS[skin_id]['color']
            return True
        return False
    
    def buy_upgrade(self, item_id, cost):
        """Buy an upgrade from the shop"""
        if self.coins >= cost:
            self.coins -= cost
            
            if item_id == 'double_jump_upgrade':
                self.has_triple_jump = True
            elif item_id == 'dash_upgrade':
                self.has_super_dash = True
            elif item_id == 'magnet':
                self.has_coin_magnet = True
            elif item_id == 'shield_upgrade':
                self.has_super_shield = True
            elif item_id == 'speed_boost':
                self.speed_upgrade = 20
            elif item_id == 'jump_boost':
                self.jump_upgrade = 20
            
            return True
        return False
    
    def move_left(self):
        speed_multiplier = 1.0
        if self.speed_boost_timer > 0:
            speed_multiplier *= 1.5
        if self.super_speed:
            speed_multiplier *= 2.0  # Double speed with speed orb
        if self.lightning_mode:
            speed_multiplier *= 1.8  # Lightning speed boost
        if self.rage_mode:
            speed_multiplier *= 1.3  # Rage speed boost
        if self.speed_upgrade > 0:
            speed_multiplier *= (1 + self.speed_upgrade / 100)
        
        target_speed = -MAX_SPEED * speed_multiplier
        
        if self.on_ground:
            self.vel_x = max(self.vel_x - ACCELERATION, target_speed)
        else:
            self.vel_x = max(self.vel_x - ACCELERATION * AIR_CONTROL, target_speed)
        
        self.facing_right = False
    
    def move_right(self):
        speed_multiplier = 1.0
        if self.speed_boost_timer > 0:
            speed_multiplier *= 1.5
        if self.super_speed:
            speed_multiplier *= 2.0  # Double speed with speed orb
        if self.lightning_mode:
            speed_multiplier *= 1.8  # Lightning speed boost
        if self.rage_mode:
            speed_multiplier *= 1.3  # Rage speed boost
        if self.speed_upgrade > 0:
            speed_multiplier *= (1 + self.speed_upgrade / 100)
        
        target_speed = MAX_SPEED * speed_multiplier
        
        if self.on_ground:
            self.vel_x = min(self.vel_x + ACCELERATION, target_speed)
        else:
            self.vel_x = min(self.vel_x + ACCELERATION * AIR_CONTROL, target_speed)
        
        self.facing_right = True
    
    def jump(self, particle_system):
        jump_multiplier = 1.0
        if self.jump_boost_timer > 0:
            jump_multiplier *= 1.3
        if self.bounce_mode:
            jump_multiplier *= 1.5  # Extra jump power in bounce mode
        if self.giant_mode:
            jump_multiplier *= 1.2  # Bigger = stronger jumps
        if self.lightning_mode:
            jump_multiplier *= 1.4  # Lightning jump boost
        if self.jump_upgrade > 0:
            jump_multiplier *= (1 + self.jump_upgrade / 100)
        
        if self.on_ground or self.coyote_time > 0:
            # Normal jump
            self.vel_y = -JUMP_POWER * jump_multiplier
            self.on_ground = False
            self.coyote_time = 0
            particle_system.add_landing(self.x + self.width/2, self.y + self.height)
            
        elif self.on_wall and self.can_wall_jump:
            # Wall jump
            self.vel_y = -WALL_JUMP_POWER * jump_multiplier
            self.vel_x = -self.wall_side * 15  # Push away from wall
            self.on_wall = False
            self.can_wall_jump = False
            self.wall_jumps += 1
            particle_system.add_explosion(self.x + self.width/2, self.y + self.height/2, WHITE)
            
        elif self.double_jump_available and not self.on_ground:
            # Double jump
            self.vel_y = -JUMP_POWER * 0.8 * jump_multiplier
            self.double_jump_available = False
            particle_system.add_explosion(self.x + self.width/2, self.y + self.height/2, NEON_GREEN)
            
        elif self.has_triple_jump and self.triple_jump_available and not self.double_jump_available:
            # Triple jump
            self.vel_y = -JUMP_POWER * 0.7 * jump_multiplier
            self.triple_jump_available = False
            particle_system.add_explosion(self.x + self.width/2, self.y + self.height/2, GOLD)
            
        elif self.bonus_jumps > 0:
            # Bonus jumps from multi-jump orb
            self.vel_y = -JUMP_POWER * 0.6 * jump_multiplier
            self.bonus_jumps -= 1
            particle_system.add_explosion(self.x + self.width/2, self.y + self.height/2, LIGHT_BLUE)
    
    def dash(self, particle_system):
        if self.dash_cooldown <= 0 or self.infinite_dashes:
            dash_direction = 1 if self.facing_right else -1
            dash_power = self.dash_power
            
            if self.has_super_dash:
                dash_power *= 1.5
            
            self.vel_x = dash_power * dash_direction
            
            # Only set cooldown if not in infinite dash mode
            if not self.infinite_dashes:
                self.dash_cooldown = 60  # 1 second cooldown
            
            # Dash particles (more particles if infinite dashes)
            particle_count = 25 if self.infinite_dashes else (15 if self.has_super_dash else 10)
            particle_color = NEON_PINK if self.infinite_dashes else CYAN
            for _ in range(particle_count):
                particle_system.add_trail(self.x + self.width/2, self.y + self.height/2, particle_color)
    
    def apply_friction(self):
        if self.on_ground:
            # Different friction based on platform type
            if self.last_platform_type == "ice":
                self.vel_x *= 0.99  # Very slippery ice platform
            else:
                self.vel_x *= FRICTION  # Normal friction
        else:
            self.vel_x *= 0.98  # Air resistance
    
    def attack(self, enemies, bosses, particle_system):
        """Attack nearby enemies and bosses"""
        attack_range = 50
        player_center = Vector2(self.x + self.width/2, self.y + self.height/2)
        
        # Attack enemies
        for enemy in enemies:
            if enemy.alive:
                enemy_center = Vector2(enemy.x + enemy.size/2, enemy.y + enemy.size/2)
                distance = (player_center - enemy_center).magnitude()
                
                if distance < attack_range:
                    if enemy.take_damage():
                        self.score += enemy.points
                        particle_system.add_explosion(enemy.x + enemy.size/2, enemy.y + enemy.size/2, RED)
        
        # Attack bosses
        for boss in bosses:
            if boss.alive:
                boss_center = Vector2(boss.x + boss.size/2, boss.y + boss.size/2)
                distance = (player_center - boss_center).magnitude()
                
                if distance < attack_range:
                    if boss.take_damage(particle_system):
                        self.score += 1000
                        self.bosses_defeated += 1
    
    def take_damage(self, damage=1):
        """Take damage if not protected"""
        if self.invulnerable_timer <= 0 and self.shield_timer <= 0:
            self.die(None)  # For now, any damage kills
            return True
        return False
    
    def die(self, particle_system):
        self.deaths += 1
        self.lives -= 1  # Lose a life
        
        if particle_system:
            particle_system.add_explosion(self.x + self.width/2, self.y + self.height/2, RED)
        
        # Check if game over
        if self.lives <= 0:
            self.game_over()
        else:
            # Respawn at checkpoint or start
            self.respawn_at_checkpoint()
    
    def game_over(self):
        """Handle game over"""
        # Reset to start position
        self.x = 100
        self.y = GROUND_LEVEL - PLAYER_SIZE
        self.vel_x = 0
        self.vel_y = 0
        
        # Reset lives and some stats
        self.lives = 3
        self.score = max(0, self.score - 500)  # Penalty
        
        # Clear power-ups
        self.clear_all_powerups()
    
    def clear_all_powerups(self):
        """Clear all active power-ups"""
        self.speed_boost_timer = 0
        self.jump_boost_timer = 0
        self.shield_timer = 0
        self.dash_orb_timer = 0
        self.gravity_orb_timer = 0
        self.magnet_orb_timer = 0
        self.time_orb_timer = 0
        self.health_orb_timer = 0
        self.multi_jump_orb_timer = 0
        self.phantom_orb_timer = 0
        self.rage_orb_timer = 0
        self.ice_orb_timer = 0
        self.fire_orb_timer = 0
        self.shield_orb_timer = 0
        self.speed_orb_timer = 0
        self.size_orb_timer = 0
        self.bounce_orb_timer = 0
        self.lightning_orb_timer = 0
        self.diamond_orb_timer = 0
        
        # Reset power-up states
        self.infinite_dashes = False
        self.low_gravity = False
        self.super_magnet = False
        self.slow_motion = False
        self.phantom_mode = False
        self.rage_mode = False
        self.ice_mode = False
        self.fire_mode = False
        self.shield_mode = False
        self.super_speed = False
        self.giant_mode = False
        self.bounce_mode = False
        self.lightning_mode = False
        self.diamond_mode = False
        self.bonus_jumps = 0
        
        # Reset size if giant
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
    
    def add_life(self):
        """Add an extra life (from collectibles or achievements)"""
        if self.lives < self.max_lives:
            self.lives += 1
            return True
        return False
    
    def draw(self, screen, camera_x):
        # Calculate screen position
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y)
        
        # Draw special power-up effects
        if self.shield_mode:
            # Enhanced shield with multiple rings
            for ring in range(3):
                shield_radius = self.width + 15 + ring * 5
                alpha = 100 - ring * 30
                shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2))
                shield_surface.set_alpha(alpha)
                pygame.draw.circle(shield_surface, (192, 192, 255), (shield_radius, shield_radius), shield_radius, 3)
                screen.blit(shield_surface, (screen_x + self.width//2 - shield_radius, screen_y + self.height//2 - shield_radius))
        
        if self.shield_timer > 0:
            shield_radius = self.width + 10
            pygame.draw.circle(screen, SILVER, 
                             (screen_x + self.width//2, screen_y + self.height//2), 
                             shield_radius, 3)
        
        # Lightning mode electric sparks
        if self.lightning_mode:
            for _ in range(5):
                spark_x = screen_x + random.randint(-20, int(self.width) + 20)
                spark_y = screen_y + random.randint(-20, int(self.height) + 20)
                pygame.draw.circle(screen, (255, 255, 0), (spark_x, spark_y), 2)
        
        # Diamond mode sparkles
        if self.diamond_mode:
            for i in range(8):
                angle = (time.time() * 3 + i * 0.785) % (2 * 3.14159)
                sparkle_x = screen_x + int(self.width)//2 + math.cos(angle) * (int(self.width) + 15)
                sparkle_y = screen_y + int(self.height)//2 + math.sin(angle) * (int(self.height) + 15)
                pygame.draw.circle(screen, (185, 242, 255), (int(sparkle_x), int(sparkle_y)), 3)
        
        # Giant mode size indicator
        if self.giant_mode:
            # Draw growth aura
            aura_radius = int(self.width * 0.8)
            aura_surface = pygame.Surface((aura_radius * 2, aura_radius * 2))
            aura_surface.set_alpha(50)
            pygame.draw.circle(aura_surface, (255, 182, 193), (aura_radius, aura_radius), aura_radius)
            screen.blit(aura_surface, (screen_x + int(self.width)//2 - aura_radius, screen_y + int(self.height)//2 - aura_radius))
        
        # Draw player body with gradient effect
        for i in range(5):
            size_reduction = i * 2
            rect = pygame.Rect(screen_x + size_reduction//2, screen_y + size_reduction//2,
                             int(self.width) - size_reduction, int(self.height) - size_reduction)
            
            # Create lighter color for inner layers
            color = tuple(min(255, c + i * 20) for c in self.current_color)
            pygame.draw.rect(screen, color, rect)
        
        # Draw eyes
        eye_size = 4
        if self.facing_right:
            eye_x = screen_x + int(self.width) - 8
        else:
            eye_x = screen_x + 4
        
        eye_y = screen_y + 8
        pygame.draw.circle(screen, WHITE, (eye_x, eye_y), eye_size)
        pygame.draw.circle(screen, BLACK, (eye_x, eye_y), eye_size - 1)
        
        # Draw speed lines when moving fast
        if abs(self.vel_x) > 8:
            for i in range(3):
                line_x = screen_x - (10 + i * 5) if self.facing_right else screen_x + int(self.width) + (10 + i * 5)
                line_y = screen_y + 5 + i * 8
                pygame.draw.line(screen, self.current_color, 
                               (line_x, line_y), (line_x - 15, line_y), 2)

class Enemy:
    def __init__(self, x, y, enemy_type='basic'):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.data = ENEMY_TYPES[enemy_type]
        self.health = self.data['health']
        self.speed = self.data['speed']
        self.color = self.data['color']
        self.size = self.data['size']
        self.points = self.data['points']
        
        self.vel_x = random.choice([-1, 1]) * self.speed
        self.vel_y = 0
        self.alive = True
        self.animation_frame = 0
        
        if enemy_type == 'flying':
            self.vel_y = random.uniform(-2, 2)
    
    def update(self, platforms, player):
        if not self.alive:
            return
        
        self.animation_frame += 1
        
        # Basic AI - move towards player
        if abs(player.x - self.x) > 50:
            if player.x > self.x:
                self.vel_x = abs(self.vel_x)
            else:
                self.vel_x = -abs(self.vel_x)
        
        # Apply movement
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Flying enemies float up and down
        if self.type == 'flying':
            self.y += math.sin(self.animation_frame * 0.1) * 0.5
        else:
            # Apply gravity to ground enemies
            self.vel_y += GRAVITY * 0.5
            
            # Check platform collisions
            enemy_rect = pygame.Rect(self.x, self.y, self.size, self.size)
            for platform in platforms:
                if enemy_rect.colliderect(platform.rect) and self.vel_y > 0:
                    self.y = platform.rect.top - self.size
                    self.vel_y = 0
        
        # Reverse direction at edges
        if self.x < 0 or self.x > 5000:
            self.vel_x *= -1
    
    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.alive = False
            return True
        return False
    
    def draw(self, screen, camera_x):
        if not self.alive:
            return
        
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y)
        
        # Draw enemy with animation
        size_mod = int(math.sin(self.animation_frame * 0.2) * 2)
        enemy_rect = pygame.Rect(screen_x, screen_y, self.size + size_mod, self.size + size_mod)
        
        pygame.draw.rect(screen, self.color, enemy_rect)
        pygame.draw.rect(screen, BLACK, enemy_rect, 2)
        
        # Draw eyes
        eye_size = max(2, self.size // 8)
        pygame.draw.circle(screen, WHITE, (screen_x + self.size//3, screen_y + self.size//3), eye_size)
        pygame.draw.circle(screen, WHITE, (screen_x + 2*self.size//3, screen_y + self.size//3), eye_size)
        pygame.draw.circle(screen, BLACK, (screen_x + self.size//3, screen_y + self.size//3), eye_size - 1)
        pygame.draw.circle(screen, BLACK, (screen_x + 2*self.size//3, screen_y + self.size//3), eye_size - 1)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

class Boss:
    def __init__(self, x, y, boss_type='fire_demon'):
        self.x = x
        self.y = y
        self.type = boss_type
        self.max_health = 10
        self.health = self.max_health
        self.size = 80
        self.speed = 1.5
        self.alive = True
        self.phase = 1
        self.attack_timer = 0
        self.animation_frame = 0
        
        # Attack patterns
        self.attack_cooldown = 120  # 2 seconds
        self.projectiles = []
    
    def update(self, player, particle_system):
        if not self.alive:
            return
        
        self.animation_frame += 1
        self.attack_timer += 1
        
        # Move towards player slowly
        if player.x > self.x:
            self.x += self.speed
        elif player.x < self.x:
            self.x -= self.speed
        
        # Attack patterns
        if self.attack_timer >= self.attack_cooldown:
            self.attack(player, particle_system)
            self.attack_timer = 0
        
        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile['x'] += projectile['vel_x']
            projectile['y'] += projectile['vel_y']
            projectile['lifetime'] -= 1
            
            if projectile['lifetime'] <= 0:
                self.projectiles.remove(projectile)
    
    def attack(self, player, particle_system):
        # Fire projectiles at player
        for i in range(3):
            angle = math.atan2(player.y - self.y, player.x - self.x)
            angle += (i - 1) * 0.3  # Spread shots
            
            projectile = {
                'x': self.x + self.size // 2,
                'y': self.y + self.size // 2,
                'vel_x': math.cos(angle) * 5,
                'vel_y': math.sin(angle) * 5,
                'lifetime': 120,
                'size': 8
            }
            self.projectiles.append(projectile)
        
        # Explosion effect
        particle_system.add_explosion(self.x + self.size//2, self.y + self.size//2, RED)
    
    def take_damage(self, particle_system):
        self.health -= 1
        particle_system.add_explosion(self.x + self.size//2, self.y + self.size//2, ORANGE)
        
        if self.health <= 0:
            self.alive = False
            # Big explosion when defeated
            for _ in range(20):
                particle_system.add_explosion(
                    self.x + random.randint(0, self.size),
                    self.y + random.randint(0, self.size),
                    random.choice([RED, ORANGE, YELLOW])
                )
            return True
        return False
    
    def draw(self, screen, camera_x):
        if not self.alive:
            return
        
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y)
        
        # Draw boss with animation
        size_mod = int(math.sin(self.animation_frame * 0.1) * 5)
        boss_rect = pygame.Rect(screen_x, screen_y, self.size + size_mod, self.size + size_mod)
        
        # Draw with gradient effect
        for i in range(5):
            inner_rect = pygame.Rect(screen_x + i*3, screen_y + i*3, 
                                   self.size - i*6, self.size - i*6)
            color_intensity = 255 - i * 30
            boss_color = (color_intensity, color_intensity // 3, 0)  # Fire colors
            pygame.draw.rect(screen, boss_color, inner_rect)
        
        pygame.draw.rect(screen, BLACK, boss_rect, 3)
        
        # Draw health bar
        health_bar_width = self.size
        health_bar_height = 8
        health_ratio = self.health / self.max_health
        
        health_bg = pygame.Rect(screen_x, screen_y - 20, health_bar_width, health_bar_height)
        health_fill = pygame.Rect(screen_x, screen_y - 20, int(health_bar_width * health_ratio), health_bar_height)
        
        pygame.draw.rect(screen, DARK_GRAY, health_bg)
        pygame.draw.rect(screen, RED, health_fill)
        pygame.draw.rect(screen, WHITE, health_bg, 2)
        
        # Draw projectiles
        for projectile in self.projectiles:
            proj_x = int(projectile['x'] - camera_x)
            proj_y = int(projectile['y'])
            pygame.draw.circle(screen, ORANGE, (proj_x, proj_y), projectile['size'])
            pygame.draw.circle(screen, RED, (proj_x, proj_y), projectile['size'] - 2)

class Checkpoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.activated = False
        self.animation_frame = 0
        self.size = 30
    
    def update(self):
        self.animation_frame += 1
    
    def activate(self):
        if not self.activated:
            self.activated = True
            return True
        return False
    
    def draw(self, screen, camera_x):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y)
        
        # Draw checkpoint flag
        pole_rect = pygame.Rect(screen_x + self.size//2 - 2, screen_y, 4, self.size)
        pygame.draw.rect(screen, BROWN, pole_rect)
        
        # Animated flag
        flag_color = GREEN if self.activated else RED
        flag_wave = math.sin(self.animation_frame * 0.2) * 3
        
        flag_points = [
            (screen_x + self.size//2, screen_y + 5),
            (screen_x + self.size//2 + 20 + flag_wave, screen_y + 8),
            (screen_x + self.size//2 + 20 + flag_wave, screen_y + 15),
            (screen_x + self.size//2, screen_y + 18)
        ]
        pygame.draw.polygon(screen, flag_color, flag_points)
        pygame.draw.polygon(screen, BLACK, flag_points, 2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

class PuzzleBlock:
    def __init__(self, x, y, puzzle_type='switch'):
        self.x = x
        self.y = y
        self.type = puzzle_type  # 'switch', 'door', 'pressure_plate'
        self.activated = False
        self.linked_blocks = []
        self.animation_frame = 0
        self.size = BLOCK_SIZE
    
    def activate(self):
        self.activated = not self.activated
        # Activate linked blocks
        for block in self.linked_blocks:
            if block.type == 'door':
                block.activated = self.activated
    
    def update(self):
        self.animation_frame += 1
    
    def draw(self, screen, camera_x):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y)
        
        if self.type == 'switch':
            color = GREEN if self.activated else RED
            pygame.draw.rect(screen, color, (screen_x, screen_y, self.size, self.size))
            # Draw switch lever
            lever_x = screen_x + self.size//2
            lever_y1 = screen_y + self.size//2
            lever_y2 = lever_y1 + (10 if self.activated else -10)
            pygame.draw.line(screen, BLACK, (lever_x, lever_y1), (lever_x, lever_y2), 3)
            
        elif self.type == 'door':
            if not self.activated:  # Door is solid when not activated
                color = BROWN
                pygame.draw.rect(screen, color, (screen_x, screen_y, self.size, self.size))
                # Draw door pattern
                pygame.draw.rect(screen, DARK_GRAY, (screen_x + 5, screen_y + 5, self.size - 10, self.size - 10))
            
        elif self.type == 'pressure_plate':
            color = YELLOW if self.activated else GRAY
            plate_height = 5 if self.activated else 10
            pygame.draw.rect(screen, color, (screen_x, screen_y + self.size - plate_height, self.size, plate_height))
        
        pygame.draw.rect(screen, BLACK, (screen_x, screen_y, self.size, self.size), 2)
    
    def get_rect(self):
        if self.type == 'door' and self.activated:
            return None  # No collision when door is open
        return pygame.Rect(self.x, self.y, self.size, self.size)

class GameWorld:
    def __init__(self, game_mode='classic', difficulty_multiplier=1.0):
        self.platforms = []
        self.collectibles = []
        self.enemies = []
        self.bosses = []
        self.checkpoints = []
        self.puzzle_blocks = []
        self.game_mode = game_mode
        self.wave_number = 1
        self.enemies_remaining = 0
        self.level_complete = False
        self.difficulty_multiplier = difficulty_multiplier
        
        self.generate_level()
    
    def generate_level(self):
        if self.game_mode == 'classic':
            self.generate_classic_level()
        elif self.game_mode == 'speedrun':
            self.generate_speedrun_level()
        elif self.game_mode == 'survival':
            self.generate_survival_level()
        elif self.game_mode == 'puzzle':
            self.generate_puzzle_level()
        elif self.game_mode == 'boss_rush':
            self.generate_boss_level()
    
    def generate_classic_level(self):
        # Ground platforms (more gaps in higher levels)
        gap_chance = 0.3 + (self.difficulty_multiplier - 1) * 0.1
        world_length = int(5000 + (self.difficulty_multiplier - 1) * 1000)  # Longer levels
        
        for x in range(0, world_length, 200):
            if random.random() > gap_chance:  # Some gaps
                # Ground platforms are mix of normal and trampoline, with some spikes in higher levels
                if self.difficulty_multiplier > 1.5 and random.random() < 0.15:  # 15% chance for spikes in higher levels
                    platform_type = "spikes"
                elif random.random() < 0.1:  # 10% chance for decorative animated platforms
                    platform_type = random.choice(["pulse", "shimmer", "rainbow", "glow", "wave", "gradient", 
                                                  "spiral", "matrix", "lava", "crystal", "galaxy", "disco", 
                                                  "electric_storm", "glitch"])
                else:
                    platform_type = random.choices(["normal", "trampoline"], weights=[70, 30])[0]
                self.platforms.append(Platform(x, GROUND_LEVEL, 200, 50, platform_type))
        
        # Floating platforms with variety (more platforms in higher levels)
        platform_count = int(60 + (self.difficulty_multiplier - 1) * 20)
        for i in range(platform_count):
            x = random.randint(300, world_length - 200)
            y = random.randint(200, GROUND_LEVEL - 100)
            width = random.choice([80, 120, 160])
            height = random.choice([20, 30])
            
            # Different platform types - mix of normal blocks and trampolines
            platform_type = random.choices(
                ["normal", "trampoline", "moving", "moving_trampoline", "ice", "boost", "electric", "spikes", 
                 "pulse", "shimmer", "rainbow", "glow", "wave", "gradient", "spiral", "matrix", "lava", 
                 "crystal", "galaxy", "disco", "electric_storm", "glitch"],
                weights=[25, 20, 8, 7, 5, 10, 5, 5, 4, 3, 2, 3, 2, 1, 2, 2, 2, 2, 1, 1, 1, 1]
            )[0]
            
            platform = Platform(x, y, width, height, platform_type)
            self.platforms.append(platform)
        
        # Generate collectibles with MANY MORE POWER ORBS! (scaled by difficulty)
        base_collectibles = 200
        orb_count = int(base_collectibles * self.difficulty_multiplier)
        
        for i in range(orb_count):
            x = random.randint(100, world_length - 100)
            y = random.randint(100, GROUND_LEVEL - 50)
            
            # More power orbs in higher levels
            if self.difficulty_multiplier > 2:
                collectible_type = random.choices(
                    ["coin", "gem", "speed_boost", "jump_boost", "shield", 
                     "dash_orb", "gravity_orb", "magnet_orb", "time_orb", "health_orb", 
                     "multi_jump_orb", "phantom_orb", "rage_orb", "ice_orb", "fire_orb",
                     "shield_orb", "speed_orb", "size_orb", "bounce_orb", "lightning_orb", "diamond_orb", "life_orb"],
                    weights=[15, 8, 5, 5, 5, 8, 8, 8, 6, 6, 6, 5, 5, 5, 5, 4, 4, 4, 4, 3, 2, 1]
                )[0]
            else:
                collectible_type = random.choices(
                    ["coin", "gem", "speed_boost", "jump_boost", "shield", 
                     "dash_orb", "gravity_orb", "magnet_orb", "time_orb", "health_orb", 
                     "multi_jump_orb", "phantom_orb", "rage_orb", "ice_orb", "fire_orb",
                     "shield_orb", "speed_orb", "size_orb", "bounce_orb", "lightning_orb", "diamond_orb", "life_orb"],
                    weights=[25, 12, 7, 7, 7, 6, 6, 6, 4, 4, 5, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1]
                )[0]
            
            self.collectibles.append(Collectible(x, y, collectible_type))
        
        # Add checkpoints (more frequent in longer levels)
        checkpoint_interval = int(max(500, 1000 - (self.difficulty_multiplier - 1) * 100))
        for x in range(1000, world_length, checkpoint_interval):
            y = GROUND_LEVEL - 60
            self.checkpoints.append(Checkpoint(x, y))
        
        # Add some enemies (more in higher levels)
        enemy_count = int(20 + (self.difficulty_multiplier - 1) * 10)
        for i in range(enemy_count):
            x = random.randint(500, world_length - 500)
            y = GROUND_LEVEL - 30
            enemy_type = random.choice(['basic', 'fast'])
            self.enemies.append(Enemy(x, y, enemy_type))
    
    def generate_speedrun_level(self):
        # More challenging with time pressure
        self.generate_classic_level()
        
        # Add more boost platforms
        for i in range(20):
            x = random.randint(300, 4800)
            y = random.randint(300, GROUND_LEVEL - 50)
            self.platforms.append(Platform(x, y, 100, 20, "boost"))
        
        # More checkpoints for timing
        for x in range(500, 5000, 500):
            y = GROUND_LEVEL - 60
            self.checkpoints.append(Checkpoint(x, y))
    
    def generate_survival_level(self):
        # Smaller area, more enemies
        for x in range(0, 2000, 150):
            # Add some spike platforms to make survival harder
            if random.random() < 0.2:  # 20% chance for spikes
                platform_type = "spikes"
            else:
                platform_type = "normal"
            self.platforms.append(Platform(x, GROUND_LEVEL, 150, 50, platform_type))
        
        # Floating platforms for maneuvering
        for i in range(30):
            x = random.randint(100, 1900)
            y = random.randint(200, GROUND_LEVEL - 100)
            # Some floating spike platforms for extra danger
            if random.random() < 0.15:  # 15% chance for spikes
                platform_type = "spikes"
            else:
                platform_type = random.choice(["normal", "trampoline"])
            self.platforms.append(Platform(x, y, 100, 20, platform_type))
        
        # Spawn first wave
        self.spawn_enemy_wave()
    
    def generate_puzzle_level(self):
        # Create puzzle platforms and switches
        switch_positions = [(200, GROUND_LEVEL - 100), (600, GROUND_LEVEL - 200), (1000, GROUND_LEVEL - 150)]
        door_positions = [(400, GROUND_LEVEL - 50), (800, GROUND_LEVEL - 100), (1200, GROUND_LEVEL - 200)]
        
        switches = []
        doors = []
        
        # Create switches and doors
        for i, (x, y) in enumerate(switch_positions):
            switch = PuzzleBlock(x, y, 'switch')
            switches.append(switch)
            self.puzzle_blocks.append(switch)
            
            # Create corresponding door
            door_x, door_y = door_positions[i]
            door = PuzzleBlock(door_x, door_y, 'door')
            doors.append(door)
            self.puzzle_blocks.append(door)
            
            # Link switch to door
            switch.linked_blocks.append(door)
        
        # Add platforms for navigation
        for i in range(40):
            x = random.randint(100, 1400)
            y = random.randint(200, GROUND_LEVEL - 50)
            self.platforms.append(Platform(x, y, 80, 20))
    
    def generate_boss_level(self):
        # Simple platform layout for boss fights
        for x in range(0, 1500, 200):
            self.platforms.append(Platform(x, GROUND_LEVEL, 200, 50))
        
        # Add floating platforms
        for i in range(10):
            x = random.randint(200, 1300)
            y = random.randint(400, GROUND_LEVEL - 100)
            self.platforms.append(Platform(x, y, 120, 20))
        
        # Spawn boss
        boss = Boss(700, GROUND_LEVEL - 80)
        self.bosses.append(boss)
    
    def spawn_enemy_wave(self):
        """Spawn a wave of enemies for survival mode"""
        self.enemies_remaining = self.wave_number * 3 + 5
        
        for i in range(self.enemies_remaining):
            x = random.randint(100, 1900)
            y = GROUND_LEVEL - 30
            
            # More difficult enemies in later waves
            if self.wave_number < 3:
                enemy_type = random.choice(['basic', 'fast'])
            elif self.wave_number < 6:
                enemy_type = random.choice(['basic', 'fast', 'tank'])
            else:
                enemy_type = random.choice(['basic', 'fast', 'tank', 'flying'])
            
            self.enemies.append(Enemy(x, y, enemy_type))
    
    def update(self, player):
        # Update platforms
        for platform in self.platforms:
            platform.update()
        
        # Update collectibles
        for collectible in self.collectibles:
            collectible.update()
        
        # Update enemies
        for enemy in self.enemies[:]:
            if enemy.alive:
                enemy.update(self.platforms, player)
            else:
                self.enemies.remove(enemy)
                if self.game_mode == 'survival':
                    self.enemies_remaining -= 1
        
        # Update bosses
        for boss in self.bosses:
            if boss.alive:
                boss.update(player, None)  # Pass particle system if needed
        
        # Update checkpoints
        for checkpoint in self.checkpoints:
            checkpoint.update()
            if not checkpoint.activated and player.get_rect().colliderect(checkpoint.get_rect()):
                player.set_checkpoint(checkpoint)
        
        # Update puzzle blocks
        for block in self.puzzle_blocks:
            block.update()
            if block.type == 'switch' and player.get_rect().colliderect(block.get_rect()):
                block.activate()
            elif block.type == 'pressure_plate':
                block.activated = player.get_rect().colliderect(block.get_rect())
        
        # Check survival mode wave completion
        if self.game_mode == 'survival' and self.enemies_remaining <= 0 and len(self.enemies) == 0:
            self.wave_number += 1
            self.spawn_enemy_wave()
    
    def draw(self, screen, camera_x):
        # Draw platforms
        for platform in self.platforms:
            platform.draw(screen, camera_x)
        
        # Draw collectibles
        for collectible in self.collectibles:
            collectible.draw(screen, camera_x)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen, camera_x)
        
        # Draw bosses
        for boss in self.bosses:
            boss.draw(screen, camera_x)
        
        # Draw checkpoints
        for checkpoint in self.checkpoints:
            checkpoint.draw(screen, camera_x)
        
        # Draw puzzle blocks
        for block in self.puzzle_blocks:
            block.draw(screen, camera_x)

class Camera:
    def __init__(self):
        self.x = 0
        self.target_x = 0
        self.smooth_factor = 0.1
    
    def update(self, player):
        # Calculate target position (center player on screen)
        self.target_x = player.x - WINDOW_WIDTH // 2
        
        # Smooth camera movement
        self.x += (self.target_x - self.x) * self.smooth_factor
        
        # Keep camera in bounds
        self.x = max(0, self.x)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Ultimate 2D Parkour Adventure")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 72)
        
        # Game objects
        self.player = Player(100, GROUND_LEVEL - PLAYER_SIZE)
        self.world = GameWorld()
        self.camera = Camera()
        self.particle_system = ParticleSystem()
        
        # Game state
        self.running = True
        self.paused = False
        
        # Level management
        self.current_level = 1

        self.max_level = 10  # Total number of levels
        self.level_complete = False
        self.level_complete_timer = 0
        self.total_orbs_in_level = 0
        self.orbs_collected = 0
        self.game_complete = False
        
        # Simple background
        pass
        
        # Count total orbs in current level
        self.count_total_orbs()
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_SPACE:
                    self.player.jump(self.particle_system)
                elif event.key == pygame.K_x:
                    self.player.dash(self.particle_system)
        
        # Movement
        if not self.paused:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.player.move_left()
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.player.move_right()
            else:
                self.player.apply_friction()
    
    def update(self):
        if not self.paused:
            # Handle level completion timer
            if self.level_complete_timer > 0:
                self.level_complete_timer -= 1
                if self.level_complete_timer == 0:
                    self.advance_to_next_level()
            
            if not self.level_complete:
                self.player.update(self.world.platforms, self.world.collectibles, self.particle_system, self)
                self.world.update(self.player)
                self.camera.update(self.player)
            
            self.particle_system.update()
    
    def draw_background(self):
        # Simple gradient background
        for y in range(WINDOW_HEIGHT):
            ratio = y / WINDOW_HEIGHT
            r = int(30 + ratio * 40)   # Dark blue to lighter blue
            g = int(30 + ratio * 60)   
            b = int(80 + ratio * 100)  
            color = (r, g, b)
            pygame.draw.line(self.screen, color, (0, y), (WINDOW_WIDTH, y))
    
    def draw_ui(self):
        # Score and stats
        score_text = self.font.render(f"Score: {self.player.score}", True, WHITE)
        coins_text = self.font.render(f"Coins: {self.player.coins}", True, GOLD)
        gems_text = self.font.render(f"Gems: {self.player.gems}", True, PURPLE)
        
        # Level information
        level_text = self.font.render(f"Level: {self.current_level}/{self.max_level}", True, WHITE)
        orbs_text = self.font.render(f"Power Orbs: {self.orbs_collected}/{self.total_orbs_in_level}", True, NEON_GREEN)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(coins_text, (10, 50))
        self.screen.blit(gems_text, (10, 90))
        self.screen.blit(level_text, (10, 130))
        self.screen.blit(orbs_text, (10, 170))
        
        # Draw lives as hearts
        lives_text = self.font.render("Lives: ", True, WHITE)
        self.screen.blit(lives_text, (WINDOW_WIDTH - 200, 10))
        
        # Draw heart icons for lives
        heart_size = 20
        heart_spacing = 25
        start_x = WINDOW_WIDTH - 120
        for i in range(self.player.max_lives):
            heart_x = start_x + i * heart_spacing
            heart_y = 15
            
            # Draw heart shape (simplified as a red circle with a smaller pink circle inside)
            if i < self.player.lives:
                # Filled heart for remaining lives
                pygame.draw.circle(self.screen, (255, 50, 50), (heart_x, heart_y), heart_size//2)
                pygame.draw.circle(self.screen, (255, 150, 150), (heart_x, heart_y), heart_size//3)
            else:
                # Empty heart for lost lives
                pygame.draw.circle(self.screen, (100, 100, 100), (heart_x, heart_y), heart_size//2, 2)
        
        # Level completion message
        if self.level_complete:
            completion_text = self.big_font.render("LEVEL COMPLETE!", True, GOLD)
            completion_rect = completion_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
            self.screen.blit(completion_text, completion_rect)
            
            if self.current_level < self.max_level:
                next_level_text = self.font.render(f"Advancing to Level {self.current_level + 1}...", True, WHITE)
                next_rect = next_level_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 20))
                self.screen.blit(next_level_text, next_rect)
            else:
                complete_text = self.font.render("ALL LEVELS COMPLETED! YOU WIN!", True, GOLD)
                complete_rect = complete_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 20))
                self.screen.blit(complete_text, complete_rect)
        
        # Active abilities
        y_offset = 210
        if self.player.speed_boost_timer > 0:
            boost_text = self.small_font.render(f"Speed Boost: {self.player.speed_boost_timer//60 + 1}s", True, NEON_BLUE)
            self.screen.blit(boost_text, (10, y_offset))
            y_offset += 25
        
        if self.player.jump_boost_timer > 0:
            jump_text = self.small_font.render(f"Jump Boost: {self.player.jump_boost_timer//60 + 1}s", True, NEON_GREEN)
            self.screen.blit(jump_text, (10, y_offset))
            y_offset += 25
        
        if self.player.shield_timer > 0:
            shield_text = self.small_font.render(f"Shield: {self.player.shield_timer//60 + 1}s", True, SILVER)
            self.screen.blit(shield_text, (10, y_offset))
            y_offset += 25
        
        # NEW POWER ORB EFFECTS!
        if self.player.infinite_dashes:
            dash_orb_text = self.small_font.render(f"Infinite Dashes: {self.player.dash_orb_timer//60 + 1}s", True, NEON_PINK)
            self.screen.blit(dash_orb_text, (10, y_offset))
            y_offset += 25
        
        if self.player.low_gravity:
            gravity_text = self.small_font.render(f"Low Gravity: {self.player.gravity_orb_timer//60 + 1}s", True, ORANGE)
            self.screen.blit(gravity_text, (10, y_offset))
            y_offset += 25
        
        if self.player.super_magnet:
            magnet_text = self.small_font.render(f"Super Magnet: {self.player.magnet_orb_timer//60 + 1}s", True, CYAN)
            self.screen.blit(magnet_text, (10, y_offset))
            y_offset += 25
        
        if self.player.slow_motion:
            time_text = self.small_font.render(f"Slow Motion: {self.player.time_orb_timer//60 + 1}s", True, YELLOW)
            self.screen.blit(time_text, (10, y_offset))
            y_offset += 25
        
        if self.player.bonus_jumps > 0:
            multi_jump_text = self.small_font.render(f"Bonus Jumps: {self.player.bonus_jumps} ({self.player.multi_jump_orb_timer//60 + 1}s)", True, LIGHT_BLUE)
            self.screen.blit(multi_jump_text, (10, y_offset))
            y_offset += 25
        
        if self.player.phantom_mode:
            phantom_text = self.small_font.render(f"Phantom Mode: {self.player.phantom_orb_timer//60 + 1}s", True, (150, 150, 255))
            self.screen.blit(phantom_text, (10, y_offset))
            y_offset += 25
        
        if self.player.rage_mode:
            rage_text = self.small_font.render(f"Rage Mode: {self.player.rage_orb_timer//60 + 1}s", True, (255, 50, 50))
            self.screen.blit(rage_text, (10, y_offset))
            y_offset += 25
        
        if self.player.ice_mode:
            ice_text = self.small_font.render(f"Ice Mode: {self.player.ice_orb_timer//60 + 1}s", True, (200, 255, 255))
            self.screen.blit(ice_text, (10, y_offset))
            y_offset += 25
        
        if self.player.fire_mode:
            fire_text = self.small_font.render(f"Fire Mode: {self.player.fire_orb_timer//60 + 1}s", True, (255, 100, 0))
            self.screen.blit(fire_text, (10, y_offset))
            y_offset += 25
        
        # NEW POWER-UP DISPLAYS
        if self.player.shield_mode:
            shield_orb_text = self.small_font.render(f"Shield Mode: {self.player.shield_orb_timer//60 + 1}s", True, (192, 192, 255))
            self.screen.blit(shield_orb_text, (10, y_offset))
            y_offset += 25
        
        if self.player.super_speed:
            speed_orb_text = self.small_font.render(f"Super Speed: {self.player.speed_orb_timer//60 + 1}s", True, (0, 255, 127))
            self.screen.blit(speed_orb_text, (10, y_offset))
            y_offset += 25
        
        if self.player.giant_mode:
            size_orb_text = self.small_font.render(f"Giant Mode: {self.player.size_orb_timer//60 + 1}s", True, (255, 182, 193))
            self.screen.blit(size_orb_text, (10, y_offset))
            y_offset += 25
        
        if self.player.bounce_mode:
            bounce_orb_text = self.small_font.render(f"Bounce Mode: {self.player.bounce_orb_timer//60 + 1}s", True, (255, 140, 0))
            self.screen.blit(bounce_orb_text, (10, y_offset))
            y_offset += 25
        
        if self.player.lightning_mode:
            lightning_orb_text = self.small_font.render(f"Lightning Mode: {self.player.lightning_orb_timer//60 + 1}s", True, (255, 255, 0))
            self.screen.blit(lightning_orb_text, (10, y_offset))
            y_offset += 25
        
        if self.player.diamond_mode:
            diamond_orb_text = self.small_font.render(f"Diamond Mode: {self.player.diamond_orb_timer//60 + 1}s", True, (185, 242, 255))
            self.screen.blit(diamond_orb_text, (10, y_offset))
            y_offset += 25
        
        # Dash cooldown (only show if not infinite dashes)
        if self.player.dash_cooldown > 0 and not self.player.infinite_dashes:
            dash_text = self.small_font.render(f"Dash: {self.player.dash_cooldown//60 + 1}s", True, CYAN)
            self.screen.blit(dash_text, (10, y_offset))
        
        # Draw orb collection progress bar
        progress_bar_width = 300
        progress_bar_height = 20
        progress_bar_x = WINDOW_WIDTH - progress_bar_width - 20
        progress_bar_y = 20
        
        # Background bar
        progress_bg = pygame.Rect(progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height)
        pygame.draw.rect(self.screen, DARK_GRAY, progress_bg)
        
        # Progress fill
        if self.total_orbs_in_level > 0:
            progress_ratio = self.orbs_collected / self.total_orbs_in_level
            progress_width = int(progress_bar_width * progress_ratio)
            progress_fill = pygame.Rect(progress_bar_x, progress_bar_y, progress_width, progress_bar_height)
            
            # Color changes as you collect more orbs
            if progress_ratio < 0.33:
                bar_color = RED
            elif progress_ratio < 0.66:
                bar_color = ORANGE
            elif progress_ratio < 1.0:
                bar_color = YELLOW
            else:
                bar_color = NEON_GREEN
            
            pygame.draw.rect(self.screen, bar_color, progress_fill)
        
        # Border
        pygame.draw.rect(self.screen, WHITE, progress_bg, 2)
        
        # Progress text
        progress_text = self.small_font.render(f"Orb Progress: {self.orbs_collected}/{self.total_orbs_in_level}", True, WHITE)
        self.screen.blit(progress_text, (progress_bar_x, progress_bar_y + progress_bar_height + 5))
        
        # Performance info
        fps = int(self.clock.get_fps())
        fps_text = self.small_font.render(f"FPS: {fps}", True, WHITE)
        self.screen.blit(fps_text, (WINDOW_WIDTH - 100, WINDOW_HEIGHT - 30))
        
        # Pause overlay
        if self.paused:
            pause_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            pause_surface.set_alpha(128)
            pause_surface.fill(BLACK)
            self.screen.blit(pause_surface, (0, 0))
            
            pause_text = self.big_font.render("PAUSED", True, WHITE)
            pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(pause_text, pause_rect)
    
    def draw(self):
        self.draw_background()
        self.world.draw(self.screen, self.camera.x)
        self.particle_system.draw(self.screen, self.camera.x)
        self.player.draw(self.screen, self.camera.x)
        self.draw_ui()
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

    def count_total_orbs(self):
        """Count total power orbs in the current level"""
        self.total_orbs_in_level = 0
        orb_types = ["dash_orb", "gravity_orb", "magnet_orb", "time_orb", "health_orb", 
                     "multi_jump_orb", "phantom_orb", "rage_orb", "ice_orb", "fire_orb",
                     "shield_orb", "speed_orb", "size_orb", "bounce_orb", "lightning_orb", "diamond_orb"]
        
        for collectible in self.world.collectibles:
            if collectible.type in orb_types:
                self.total_orbs_in_level += 1
        
        self.orbs_collected = 0
    
    def check_orb_collected(self, collectible_type):
        """Check if a power orb was collected"""
        orb_types = ["dash_orb", "gravity_orb", "magnet_orb", "time_orb", "health_orb", 
                     "multi_jump_orb", "phantom_orb", "rage_orb", "ice_orb", "fire_orb",
                     "shield_orb", "speed_orb", "size_orb", "bounce_orb", "lightning_orb", "diamond_orb", "life_orb"]
        
        if collectible_type in orb_types:
            self.orbs_collected += 1
            
            # Check if all orbs collected
            if self.orbs_collected >= self.total_orbs_in_level:
                self.complete_level()
    
    def complete_level(self):
        """Complete the current level"""
        self.level_complete = True
        self.level_complete_timer = 300  # 5 seconds
        
        # Add completion bonus
        self.player.score += 1000 * self.current_level
        self.player.coins += 50 * self.current_level
        
        # Create celebration particles
        for _ in range(50):
            x = self.player.x + random.randint(-100, 100)
            y = self.player.y + random.randint(-100, 100)
            color = random.choice([GOLD, NEON_GREEN, NEON_BLUE, NEON_PINK, ORANGE])
            self.particle_system.add_explosion(x, y, color)
    
    def advance_to_next_level(self):
        """Advance to the next level"""
        if self.current_level < self.max_level:
            self.current_level += 1
            
            # Reset player position
            self.player.x = 100
            self.player.y = GROUND_LEVEL - PLAYER_SIZE
            self.player.vel_x = 0
            self.player.vel_y = 0
            
            # Generate new level with increased difficulty
            self.world = GameWorld(difficulty_multiplier=self.current_level)
            self.camera.x = 0
            self.level_complete = False
            self.level_complete_timer = 0
            
            # Count orbs in new level
            self.count_total_orbs()
        else:
            # Player completed all levels!
            self.game_complete = True
    
    def get_level_difficulty_multiplier(self):
        """Get difficulty multiplier based on current level"""
        return 1.0 + (self.current_level - 1) * 0.2

def main():
    """Main function to run the game"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
