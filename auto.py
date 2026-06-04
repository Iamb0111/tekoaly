import pygame
import sys
import random
import json
import os

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
LANE_WIDTH = WINDOW_WIDTH // 3
CAR_WIDTH = 45
CAR_HEIGHT = 75
ENEMY_CAR_WIDTH = 60
ENEMY_CAR_HEIGHT = 80
CAR_SPEED = 5
ENEMY_SPEED = 2  # Slower enemy cars
SPAWN_RATE = 90  # Less frequent spawning (higher = slower)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
DARK_GRAY = (64, 64, 64)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

class PlayerCar:
    def __init__(self):
        self.lane = 1  # Start in middle lane (0, 1, 2)
        self.x = self.lane * LANE_WIDTH + LANE_WIDTH // 2 - CAR_WIDTH // 2
        self.y = WINDOW_HEIGHT - CAR_HEIGHT - 20
        self.rect = pygame.Rect(self.x, self.y, CAR_WIDTH, CAR_HEIGHT)
        self.moving = False
        self.target_x = self.x
        self.invincible = False
        self.invincible_timer = 0
        self.speed_boost = False
        self.speed_boost_timer = 0
        self.rocket_boost = False
        self.rocket_boost_timer = 0
        self.slow_boost = False
        self.slow_boost_timer = 0
        self.laser_boost = False
        self.laser_boost_timer = 0
        self.agile_boost = False
        self.agile_boost_timer = 0
        self.agile_position = 1  # Position on lane dividers (0=left divider, 1=right divider)
    
    def move_left(self):
        if not self.moving:
            if self.agile_boost:
                # In agile mode, move between lane dividers only
                if self.agile_position > 0:
                    self.agile_position -= 1
                    # Lane divider positions: left=133, right=267
                    divider_positions = [133, 267]
                    self.target_x = divider_positions[self.agile_position] - CAR_WIDTH // 4  # Thin car
                    self.moving = True
            else:
                # Normal movement restricted to lanes
                if self.lane > 0:
                    self.lane -= 1
                    self.target_x = self.lane * LANE_WIDTH + LANE_WIDTH // 2 - CAR_WIDTH // 2
                    self.moving = True
    
    def move_right(self):
        if not self.moving:
            if self.agile_boost:
                # In agile mode, move between lane dividers only
                if self.agile_position < 1:
                    self.agile_position += 1
                    # Lane divider positions: left=133, right=267
                    divider_positions = [133, 267]
                    self.target_x = divider_positions[self.agile_position] - CAR_WIDTH // 4  # Thin car
                    self.moving = True
            else:
                # Normal movement restricted to lanes
                if self.lane < 2:
                    self.lane += 1
                    self.target_x = self.lane * LANE_WIDTH + LANE_WIDTH // 2 - CAR_WIDTH // 2
                    self.moving = True
    
    def update(self):
        # Update boost timers
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        
        if self.speed_boost:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.speed_boost = False
        
        if self.rocket_boost:
            self.rocket_boost_timer -= 1
            if self.rocket_boost_timer <= 0:
                self.rocket_boost = False
        
        if self.slow_boost:
            self.slow_boost_timer -= 1
            if self.slow_boost_timer <= 0:
                self.slow_boost = False
        
        if self.laser_boost:
            self.laser_boost_timer -= 1
            if self.laser_boost_timer <= 0:
                self.laser_boost = False
        
        if self.agile_boost:
            self.agile_boost_timer -= 1
            if self.agile_boost_timer <= 0:
                self.agile_boost = False
                # Return to normal lane when agile boost ends
                # Find the closest normal lane based on current position
                if self.agile_position == 0:  # Was on left divider (133)
                    self.lane = 0  # Go to left lane
                else:  # Was on right divider (267)
                    self.lane = 1  # Go to middle lane
                
                # Set target position to the normal lane
                self.target_x = self.lane * LANE_WIDTH + LANE_WIDTH // 2 - CAR_WIDTH // 2
                self.moving = True
        
        if self.moving:
            # Smooth movement to target position
            move_speed = CAR_SPEED * 2 if self.speed_boost else CAR_SPEED
            if abs(self.x - self.target_x) > move_speed:
                if self.x < self.target_x:
                    self.x += move_speed
                else:
                    self.x -= move_speed
            else:
                self.x = self.target_x
                self.moving = False
            
            self.rect.x = self.x
        
        # Update collision rect for agile boost
        if self.agile_boost:
            # Make collision box much thinner
            new_width = int(CAR_WIDTH * 0.6)
            width_reduction = CAR_WIDTH - new_width
            # Ensure the car doesn't go completely off-screen
            safe_x = max(-10, min(WINDOW_WIDTH - new_width + 10, self.x + width_reduction // 2))
            self.rect = pygame.Rect(safe_x, self.y, new_width, CAR_HEIGHT)
        else:
            # Normal collision box
            self.rect = pygame.Rect(self.x, self.y, CAR_WIDTH, CAR_HEIGHT)
    
    def draw(self, screen):
        # Choose car color based on active boosts
        car_color = BLUE
        if self.invincible:
            # Flash between cyan and blue when invincible
            car_color = CYAN if (self.invincible_timer // 5) % 2 else BLUE
        elif self.speed_boost:
            car_color = ORANGE
        elif self.rocket_boost:
            car_color = RED
        elif self.slow_boost:
            car_color = PURPLE
        elif self.laser_boost:
            car_color = (0, 255, 127)  # Bright green for laser boost
        elif self.agile_boost:
            car_color = (255, 100, 255)  # Bright pink/magenta for agile boost
        
        # Modify car width when agile boost is active
        car_rect = self.rect.copy()
        if self.agile_boost:
            # Make car much thinner (60% of original width)
            new_width = int(CAR_WIDTH * 0.6)
            width_reduction = CAR_WIDTH - new_width
            car_rect.width = new_width
            car_rect.x = self.x + width_reduction // 2
            # Allow drawing partially off-screen
            car_rect.x = max(-new_width//2, min(WINDOW_WIDTH - new_width//2, car_rect.x))
        
        # Draw car body
        pygame.draw.rect(screen, car_color, car_rect)
        pygame.draw.rect(screen, WHITE, car_rect, 2)
        
        # Draw car details
        # Windows
        if self.agile_boost:
            # Thinner windows for agile boost
            new_width = int(CAR_WIDTH * 0.6)
            width_reduction = CAR_WIDTH - new_width
            window_x = self.x + width_reduction // 2 + 6
            # Ensure window is visible if car is partially off-screen
            window_x = max(0, min(WINDOW_WIDTH - (new_width - 12), window_x))
            window_rect = pygame.Rect(window_x, self.y + 8, max(0, new_width - 12), 20)
            if window_rect.width > 0:  # Only draw if window has positive width
                pygame.draw.rect(screen, WHITE, window_rect)
        else:
            window_rect = pygame.Rect(self.x + 8, self.y + 8, CAR_WIDTH - 16, 20)
            pygame.draw.rect(screen, WHITE, window_rect)
        
        # Draw slightly visible wheels on the sides
        wheel_color = BLACK  # Black wheels
        wheel_radius = 6
        
        if self.agile_boost:
            # Adjust wheel positions for agile boost and off-screen capability
            new_width = int(CAR_WIDTH * 0.6)
            width_reduction = CAR_WIDTH - new_width
            car_center_x = self.x + width_reduction // 2 + new_width // 2
            
            # Left wheels - only draw if visible
            left_wheel_x = car_center_x - new_width // 2 - 2
            if left_wheel_x + wheel_radius > 0:  # Wheel is at least partially visible
                pygame.draw.circle(screen, wheel_color, (max(wheel_radius, left_wheel_x), self.y + 15), wheel_radius)
                pygame.draw.circle(screen, wheel_color, (max(wheel_radius, left_wheel_x), self.y + CAR_HEIGHT - 15), wheel_radius)
            
            # Right wheels - only draw if visible
            right_wheel_x = car_center_x + new_width // 2 + 2
            if right_wheel_x - wheel_radius < WINDOW_WIDTH:  # Wheel is at least partially visible
                pygame.draw.circle(screen, wheel_color, (min(WINDOW_WIDTH - wheel_radius, right_wheel_x), self.y + 15), wheel_radius)
                pygame.draw.circle(screen, wheel_color, (min(WINDOW_WIDTH - wheel_radius, right_wheel_x), self.y + CAR_HEIGHT - 15), wheel_radius)
        else:
            # Normal wheel positions
            # Left wheels
            pygame.draw.circle(screen, wheel_color, (self.x - 2, self.y + 15), wheel_radius)
            pygame.draw.circle(screen, wheel_color, (self.x - 2, self.y + CAR_HEIGHT - 15), wheel_radius)
            # Right wheels
            pygame.draw.circle(screen, wheel_color, (self.x + CAR_WIDTH + 2, self.y + 15), wheel_radius)
            pygame.draw.circle(screen, wheel_color, (self.x + CAR_WIDTH + 2, self.y + CAR_HEIGHT - 15), wheel_radius)

class EnemyCar:
    def __init__(self, lane):
        self.lane = lane
        self.x = lane * LANE_WIDTH + LANE_WIDTH // 2 - ENEMY_CAR_WIDTH // 2
        self.y = -ENEMY_CAR_HEIGHT
        self.rect = pygame.Rect(self.x, self.y, ENEMY_CAR_WIDTH, ENEMY_CAR_HEIGHT)
        self.color = random.choice([RED, GREEN, YELLOW, GRAY])
    
    def update(self, slow_factor=1.0):
        self.y += ENEMY_SPEED * slow_factor
        self.rect.y = self.y
    
    def is_off_screen(self):
        return self.y > WINDOW_HEIGHT
    
    def draw(self, screen):
        # Draw car body
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Draw car details
        # Windows
        window_rect = pygame.Rect(self.x + 10, self.y + ENEMY_CAR_HEIGHT - 35, ENEMY_CAR_WIDTH - 20, 25)
        pygame.draw.rect(screen, WHITE, window_rect)
        
        # Draw slightly visible wheels on the sides
        wheel_color = BLACK  # Black wheels
        wheel_radius = 6
        # Left wheels
        pygame.draw.circle(screen, wheel_color, (self.x - 2, self.y + 15), wheel_radius)
        pygame.draw.circle(screen, wheel_color, (self.x - 2, self.y + ENEMY_CAR_HEIGHT - 15), wheel_radius)
        # Right wheels
        pygame.draw.circle(screen, wheel_color, (self.x + ENEMY_CAR_WIDTH + 2, self.y + 15), wheel_radius)
        pygame.draw.circle(screen, wheel_color, (self.x + ENEMY_CAR_WIDTH + 2, self.y + ENEMY_CAR_HEIGHT - 15), wheel_radius)

class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 8
        self.height = WINDOW_HEIGHT + 100  # Full screen height plus some extra
        self.rect = pygame.Rect(self.x - self.width // 2, 0, self.width, self.height)
        self.particles = []
        self.energy_pulse = 0
        self.side_bolts = []
        self.electric_arcs = []
        self.core_fluctuation = 0
        self.intensity_multiplier = 1.0
        
        # Create enhanced energy particles along the laser
        for i in range(25):
            self.particles.append({
                'y': random.randint(0, WINDOW_HEIGHT),
                'x_offset': random.uniform(-10, 10),
                'speed': random.uniform(4, 12),
                'size': random.randint(1, 5),
                'brightness': random.uniform(0.3, 1.0),
                'rotation': random.uniform(0, 360),
                'rotation_speed': random.uniform(-5, 5),
                'life': random.randint(30, 90),
                'max_life': random.randint(30, 90)
            })
        
        # Create side lightning bolts
        for i in range(12):
            self.side_bolts.append({
                'offset': random.uniform(-20, 20),
                'length': random.uniform(15, 35),
                'timer': random.randint(0, 25),
                'intensity': random.uniform(0.5, 1.0)
            })
        
        # Create electric arcs
        for i in range(8):
            self.electric_arcs.append({
                'start_y': random.randint(0, WINDOW_HEIGHT),
                'arc_points': [],
                'timer': random.randint(0, 15),
                'color_phase': random.uniform(0, 6.28)
            })
    
    def update(self):
        import math
        self.energy_pulse += 0.4
        self.core_fluctuation += 0.2
        
        # Dynamic intensity based on energy pulse
        self.intensity_multiplier = 0.8 + 0.4 * abs(math.sin(self.energy_pulse * 0.5))
        
        # Update enhanced particles
        for particle in self.particles:
            particle['y'] -= particle['speed']
            particle['x_offset'] += random.uniform(-0.5, 0.5)  # Slight horizontal drift
            particle['rotation'] += particle['rotation_speed']
            particle['life'] -= 1
            
            # Constrain horizontal drift
            particle['x_offset'] = max(-15, min(15, particle['x_offset']))
            
            if particle['y'] < -10 or particle['life'] <= 0:
                particle['y'] = WINDOW_HEIGHT + 10
                particle['x_offset'] = random.uniform(-10, 10)
                particle['speed'] = random.uniform(4, 12)
                particle['life'] = random.randint(30, 90)
                particle['max_life'] = random.randint(30, 90)
        
        # Update side bolts with enhanced behavior
        for bolt in self.side_bolts:
            bolt['timer'] -= 1
            if bolt['timer'] <= 0:
                bolt['offset'] = random.uniform(-20, 20)
                bolt['length'] = random.uniform(15, 35)
                bolt['timer'] = random.randint(8, 35)
                bolt['intensity'] = random.uniform(0.5, 1.0)
        
        # Update electric arcs
        for arc in self.electric_arcs:
            arc['timer'] -= 1
            arc['color_phase'] += 0.3
            
            if arc['timer'] <= 0:
                arc['start_y'] = random.randint(0, WINDOW_HEIGHT)
                arc['timer'] = random.randint(5, 20)
                
                # Generate new arc points
                arc['arc_points'] = []
                start_x = self.x + random.uniform(-8, 8)
                current_x, current_y = start_x, arc['start_y']
                
                for i in range(random.randint(3, 7)):
                    current_x += random.uniform(-8, 8)
                    current_y += random.uniform(10, 30)
                    arc['arc_points'].append((current_x, current_y))
    
    def draw(self, screen):
        import time
        import math
        
        # Ultra-enhanced pulsing effects with multiple frequencies and phases
        time_factor = time.time()
        pulse1 = abs(math.sin(time_factor * 15))
        pulse2 = abs(math.sin(time_factor * 10 + 1))
        pulse3 = abs(math.sin(time_factor * 18 + 2))
        pulse4 = abs(math.sin(time_factor * 25 + 0.5))
        combined_pulse = (pulse1 + pulse2 + pulse3 + pulse4) / 4
        
        # Apply intensity multiplier for dynamic effects
        effective_pulse = combined_pulse * self.intensity_multiplier
        
        # Draw massive outer energy field with multiple layers
        for layer in range(10):
            glow_width = self.width + layer * 6 + int(effective_pulse * 15)
            glow_alpha = int(90 / (layer + 1) * (0.4 + effective_pulse * 0.6))
            
            if glow_alpha > 0:
                glow_rect = pygame.Rect(self.x - glow_width // 2, 0, glow_width, self.height)
                glow_surface = pygame.Surface((glow_width, self.height))
                glow_surface.set_alpha(glow_alpha)
                
                # Advanced color gradients with shifting hues
                layer_ratio = layer / 10.0
                phase_shift = math.sin(time_factor * 3 + layer * 0.5)
                
                if layer < 3:
                    # Outer layers: electric blue to cyan
                    r = int(phase_shift * 50 + 50)
                    g = int(255 * (0.8 + 0.2 * phase_shift))
                    b = 255
                elif layer < 6:
                    # Middle layers: cyan to green
                    r = 0
                    g = 255
                    b = int(255 * (1 - layer_ratio) + 127 * layer_ratio)
                else:
                    # Inner layers: green to white
                    intensity = int(127 + 128 * effective_pulse)
                    r = intensity
                    g = 255
                    b = intensity
                
                glow_surface.fill((r, g, b))
                screen.blit(glow_surface, glow_rect)
        
        # Draw electric arcs with enhanced visuals
        for arc in self.electric_arcs:
            if arc['timer'] > 3 and len(arc['arc_points']) > 1:
                # Color cycling for arcs
                color_r = int(128 + 127 * math.sin(arc['color_phase']))
                color_g = 255
                color_b = int(200 + 55 * math.cos(arc['color_phase'] * 1.3))
                arc_color = (color_r, color_g, color_b)
                
                # Draw main arc
                if len(arc['arc_points']) > 1:
                    pygame.draw.lines(screen, (255, 255, 255), False, arc['arc_points'], 3)
                    pygame.draw.lines(screen, arc_color, False, arc['arc_points'], 1)
                
                # Draw glow around each arc segment
                for i in range(len(arc['arc_points']) - 1):
                    start = arc['arc_points'][i]
                    end = arc['arc_points'][i + 1]
                    
                    # Multiple glow layers for each segment
                    for glow_size in [8, 5, 3]:
                        glow_alpha = int(60 / glow_size * effective_pulse)
                        if glow_alpha > 0:
                            glow_surface = pygame.Surface((glow_size * 2, glow_size * 2))
                            glow_surface.set_alpha(glow_alpha)
                            glow_surface.fill(arc_color)
                            
                            mid_x = (start[0] + end[0]) // 2
                            mid_y = (start[1] + end[1]) // 2
                            screen.blit(glow_surface, (mid_x - glow_size, mid_y - glow_size))
        
        # Draw enhanced side lightning bolts with branching
        for bolt in self.side_bolts:
            if bolt['timer'] > 5:
                bolt_x = self.x + bolt['offset'] * self.intensity_multiplier
                bolt_start_y = random.randint(20, WINDOW_HEIGHT - 20)
                bolt_end_y = bolt_start_y + bolt['length'] * bolt['intensity']
                
                # Main lightning bolt with branches
                main_points = [(bolt_x, bolt_start_y)]
                branch_points = []
                
                current_y = bolt_start_y
                while current_y < bolt_end_y:
                    current_y += random.uniform(4, 12)
                    jag_x = bolt_x + random.uniform(-5, 5)
                    main_points.append((jag_x, current_y))
                    
                    # Add branching bolts
                    if random.random() < 0.3:
                        branch_x = jag_x + random.uniform(-15, 15)
                        branch_y = current_y + random.uniform(5, 20)
                        branch_points.append([(jag_x, current_y), (branch_x, branch_y)])
                
                # Draw main bolt
                if len(main_points) > 1:
                    pygame.draw.lines(screen, (255, 255, 255), False, main_points, 3)
                    pygame.draw.lines(screen, (150, 255, 255), False, main_points, 2)
                    pygame.draw.lines(screen, (0, 255, 255), False, main_points, 1)
                
                # Draw branch bolts
                for branch in branch_points:
                    pygame.draw.lines(screen, (255, 255, 255), False, branch, 2)
                    pygame.draw.lines(screen, (100, 255, 255), False, branch, 1)
        
        # Draw enhanced energy particles with rotation and trails
        for particle in self.particles:
            if particle['life'] > 0:
                life_ratio = particle['life'] / particle['max_life']
                particle_x = self.x + particle['x_offset']
                particle_alpha = int(255 * particle['brightness'] * life_ratio * (0.6 + effective_pulse * 0.4))
                
                if particle_alpha > 0:
                    # Create rotating particle effect
                    particle_size = int(particle['size'] * (0.5 + life_ratio * 0.5))
                    
                    # Multiple particle layers for depth
                    for layer_size in [particle_size + 2, particle_size, particle_size - 1]:
                        if layer_size > 0:
                            layer_alpha = particle_alpha // (3 - layer_size + particle_size)
                            particle_surface = pygame.Surface((layer_size * 4, layer_size * 4))
                            particle_surface.set_alpha(layer_alpha)
                            
                            # Dynamic particle colors based on life and rotation
                            rotation_factor = math.sin(math.radians(particle['rotation']))
                            if life_ratio > 0.8:
                                color = (255, 255, 255)  # Bright white when fresh
                            elif life_ratio > 0.5:
                                r = int(200 + 55 * rotation_factor)
                                color = (r, 255, 255)  # Cyan variations
                            else:
                                g = int(150 + 105 * rotation_factor)
                                color = (0, g, 255)  # Blue to green fade
                            
                            pygame.draw.circle(particle_surface, color, 
                                             (layer_size * 2, layer_size * 2), layer_size)
                            
                            screen.blit(particle_surface, 
                                      (particle_x - layer_size * 2, particle['y'] - layer_size * 2))
        
        # Draw ultra-enhanced main laser core with multiple gradient layers
        core_fluctuation = math.sin(self.core_fluctuation)
        core_width = int(self.width + pulse1 * 4 + abs(core_fluctuation) * 3)
        
        # Multi-layered core with complex gradients
        for layer in range(5):
            layer_width = core_width - layer * 2
            if layer_width > 0:
                layer_alpha = 255 - layer * 40
                layer_rect = pygame.Rect(self.x - layer_width // 2, 0, layer_width, self.height)
                layer_surface = pygame.Surface((layer_width, self.height))
                layer_surface.set_alpha(layer_alpha)
                
                # Complex core coloring with pulsing
                pulse_intensity = effective_pulse
                if layer == 0:
                    # Ultra-hot white core with color flashes
                    if pulse_intensity > 0.8:
                        layer_surface.fill((255, 255, 255))  # Pure white
                    elif pulse_intensity > 0.6:
                        layer_surface.fill((255, 255, 200))  # Slight yellow
                    else:
                        layer_surface.fill((255, 255, 255))  # White
                elif layer == 1:
                    # Bright cyan inner layer
                    g_val = int(255 * (0.8 + 0.2 * pulse_intensity))
                    layer_surface.fill((200, g_val, 255))
                elif layer == 2:
                    # Green middle layer
                    r_val = int(100 * pulse_intensity)
                    layer_surface.fill((r_val, 255, 150))
                elif layer == 3:
                    # Blue-green transition
                    layer_surface.fill((0, 200, 200))
                else:
                    # Outer green layer
                    layer_surface.fill((0, 150, 100))
                
                screen.blit(layer_surface, layer_rect)
        
        # Draw enhanced energy crackles and sparks
        crackle_count = int(8 + effective_pulse * 12)
        for i in range(crackle_count):
            if random.random() < (0.4 + effective_pulse * 0.4):
                crackle_x = self.x + random.uniform(-20, 20)
                crackle_y = random.randint(0, WINDOW_HEIGHT)
                crackle_length = random.uniform(8, 25)
                
                # Multiple crackle variations
                end_x = crackle_x + random.uniform(-crackle_length, crackle_length)
                end_y = crackle_y + random.uniform(-crackle_length, crackle_length)
                
                # Main crackle
                pygame.draw.line(screen, (255, 255, 255), 
                               (crackle_x, crackle_y), (end_x, end_y), 2)
                
                # Colored overlay
                crackle_colors = [(0, 255, 255), (100, 255, 200), (200, 255, 255)]
                color = random.choice(crackle_colors)
                pygame.draw.line(screen, color, (crackle_x, crackle_y), (end_x, end_y), 1)
                
                # Add small sparks at crackle endpoints
                if random.random() < 0.5:
                    spark_size = random.randint(2, 4)
                    spark_surface = pygame.Surface((spark_size * 2, spark_size * 2))
                    spark_surface.set_alpha(200)
                    spark_surface.fill((255, 255, 255))
                    pygame.draw.circle(spark_surface, (255, 255, 255), 
                                     (spark_size, spark_size), spark_size)
                    screen.blit(spark_surface, (end_x - spark_size, end_y - spark_size))

class Rocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 8
        self.height = 15
        self.speed = 8
        self.rect = pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)
    
    def update(self):
        self.y -= self.speed
        self.rect.y = self.y
    
    def is_off_screen(self):
        return self.y < -self.height
    
    def draw(self, screen):
        # Draw rocket body
        pygame.draw.rect(screen, RED, self.rect)
        # Draw rocket tip
        pygame.draw.polygon(screen, YELLOW, [
            (self.x, self.y),
            (self.x - 4, self.y + 8),
            (self.x + 4, self.y + 8)
        ])

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.max_radius = 40
        self.growth_rate = 3
        self.duration = 20  # frames
        self.timer = 0
        self.particles = []
        # Create explosion particles
        for _ in range(8):
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(2, 6)
            self.particles.append({
                'x': x, 'y': y,
                'vx': speed * random.uniform(-1, 1),
                'vy': speed * random.uniform(-1, 1),
                'life': random.randint(15, 25)
            })
    
    def update(self):
        self.timer += 1
        if self.timer < 10:  # Expand phase
            self.radius = min(self.radius + self.growth_rate, self.max_radius)
        
        # Update particles
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            particle['vx'] *= 0.95  # Slow down
            particle['vy'] *= 0.95
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def is_finished(self):
        return self.timer >= self.duration and len(self.particles) == 0
    
    def draw(self, screen):
        if self.timer < 15:
            # Draw main explosion circle
            alpha = max(0, 255 - (self.timer * 17))
            if alpha > 0:
                # Create explosion colors that fade
                if self.timer < 5:
                    color = (255, 255, 0)  # Yellow
                elif self.timer < 10:
                    color = (255, 165, 0)  # Orange
                else:
                    color = (255, 0, 0)    # Red
                
                # Draw multiple circles for explosion effect
                for i in range(3):
                    radius = max(1, self.radius - i * 5)
                    if radius > 0:
                        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), radius)
        
        # Draw particles
        for particle in self.particles:
            if particle['life'] > 0:
                alpha = min(255, particle['life'] * 10)
                color = (255, 255, 0) if particle['life'] > 15 else (255, 165, 0)
                pygame.draw.circle(screen, color, (int(particle['x']), int(particle['y'])), 3)

class Boost:
    def __init__(self, lane, boost_type):
        self.lane = lane
        self.x = lane * LANE_WIDTH + LANE_WIDTH // 2 - 15  # 30x30 boost
        self.y = -30
        self.rect = pygame.Rect(self.x, self.y, 30, 30)
        self.boost_type = boost_type  # 'line', 'invincible', or 'rocket'
        self.speed = ENEMY_SPEED
    
    def update(self, slow_factor=1.0):
        self.y += self.speed * slow_factor
        self.rect.y = self.y
    
    def is_off_screen(self):
        return self.y > WINDOW_HEIGHT
    
    def draw(self, screen):
        if self.boost_type == 'line':
            color = ORANGE
            symbol = "L"
        elif self.boost_type == 'rocket':
            color = RED
            symbol = "R"
        elif self.boost_type == 'slow':
            color = PURPLE
            symbol = "S"
        elif self.boost_type == 'laser':
            color = (0, 255, 127)  # Bright green
            symbol = "Z"
        elif self.boost_type == 'agile':
            color = (255, 100, 255)  # Bright pink/magenta
            symbol = "A"
        else:  # invincible
            color = CYAN
            symbol = "I"
        
        # Draw boost background
        pygame.draw.circle(screen, color, (self.x + 15, self.y + 15), 15)
        pygame.draw.circle(screen, WHITE, (self.x + 15, self.y + 15), 15, 2)
        
        # Draw symbol
        font = pygame.font.Font(None, 24)
        text = font.render(symbol, True, BLACK)
        text_rect = text.get_rect(center=(self.x + 15, self.y + 15))
        screen.blit(text, text_rect)

class CarDodgeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Car Dodge - 3 Lanes")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        
        self.player = PlayerCar()
        self.enemy_cars = []
        self.boosts = []
        self.rockets = []  # List to manage active rockets
        self.lasers = []  # List to manage active lasers
        self.explosions = []  # List to manage explosion effects
        self.score = 0
        self.spawn_timer = 0
        self.boost_spawn_timer = 0
        self.game_over = False
        self.paused = False  # New pause state
        self.speed_increase_timer = 0
        self.boost_selection = True  # New state for boost selection
        self.selected_boost = None  # Currently selected boost
        self.boost_given = False  # Whether the initial boost has been given
        
        # High score system
        self.high_scores_file = "high_scores.json"
        self.high_scores = self.load_high_scores()
        self.new_high_score = False
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.boost_selection:
                    # Boost selection screen
                    if event.key == pygame.K_1:
                        self.selected_boost = 'line'
                        self.start_game_with_boost()
                    elif event.key == pygame.K_2:
                        self.selected_boost = 'invincible'
                        self.start_game_with_boost()
                    elif event.key == pygame.K_3:
                        self.selected_boost = 'rocket'
                        self.start_game_with_boost()
                    elif event.key == pygame.K_4:
                        self.selected_boost = 'slow'
                        self.start_game_with_boost()
                    elif event.key == pygame.K_5:
                        self.selected_boost = 'laser'
                        self.start_game_with_boost()
                    elif event.key == pygame.K_6:
                        self.selected_boost = 'agile'
                        self.start_game_with_boost()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                elif self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                elif self.paused:
                    # Pause screen - only allow unpausing or quitting
                    if event.key == pygame.K_p:
                        self.paused = False
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.move_left()
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.move_right()
                    elif event.key == pygame.K_SPACE and self.player.rocket_boost:
                        self.shoot_rocket()
                    elif event.key == pygame.K_p:
                        self.paused = True
                    elif event.key == pygame.K_ESCAPE:
                        return False
        return True
    
    def load_high_scores(self):
        """Load high scores from file, return default if file doesn't exist"""
        try:
            if os.path.exists(self.high_scores_file):
                with open(self.high_scores_file, 'r') as f:
                    scores = json.load(f)
                    # Ensure we have exactly 5 scores
                    while len(scores) < 5:
                        scores.append(0)
                    return scores[:5]  # Keep only top 5
            else:
                return [0, 0, 0, 0, 0]  # Default scores
        except:
            return [0, 0, 0, 0, 0]  # Return default if file is corrupted
    
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
        self.high_scores = self.high_scores[:5]  # Keep only top 5
        
        # Check if this is a new high score (in top 5)
        self.new_high_score = score in self.high_scores and score > 0
        
        self.save_high_scores()
    
    def start_game_with_boost(self):
        """Start the game and give the selected boost to the player"""
        self.boost_selection = False
        if self.selected_boost == 'line':
            self.player.speed_boost = True
            self.player.speed_boost_timer = 600  # 10 seconds (was 6)
        elif self.selected_boost == 'invincible':
            self.player.invincible = True
            self.player.invincible_timer = 720  # 12 seconds (was 8)
        elif self.selected_boost == 'rocket':
            self.player.rocket_boost = True
            self.player.rocket_boost_timer = 540  # 9 seconds (was 5)
        elif self.selected_boost == 'slow':
            self.player.slow_boost = True
            self.player.slow_boost_timer = 1200  # 20 seconds
        elif self.selected_boost == 'laser':
            self.player.laser_boost = True
            self.player.laser_boost_timer = 660  # 11 seconds
        elif self.selected_boost == 'agile':
            self.player.agile_boost = True
            self.player.agile_boost_timer = 600  # 10 seconds
        self.boost_given = True
    
    def shoot_rocket(self):
        """Shoot a rocket from the player's position"""
        if self.player.rocket_boost:
            rocket = Rocket(self.player.x + CAR_WIDTH // 2, self.player.y)
            self.rockets.append(rocket)
    
    def spawn_enemy(self):
        # Choose a random lane
        lane = random.randint(0, 2)
        
        # Don't spawn if there's already a car too close in that lane
        for car in self.enemy_cars:
            if car.lane == lane and car.y < 150:  # Larger safety distance
                return
        
        self.enemy_cars.append(EnemyCar(lane))
    
    def spawn_boost(self):
        # Choose a random lane
        lane = random.randint(0, 2)
        
        # Don't spawn if there's already something too close in that lane
        for car in self.enemy_cars:
            if car.lane == lane and car.y < 150:  # Larger safety distance
                return
        for boost in self.boosts:
            if boost.lane == lane and boost.y < 150:  # Larger safety distance
                return
        
        # Random boost type - slow boost, laser boost, and agile boost are very rare
        boost_types = ['line', 'line', 'line', 'invincible', 'invincible', 'invincible', 'rocket', 'rocket', 'rocket', 'slow', 'laser', 'agile']
        boost_type = random.choice(boost_types)  # Slow, laser, and agile boost only 1/12 chance each - very rare
        self.boosts.append(Boost(lane, boost_type))
    
    def update(self):
        global ENEMY_SPEED, SPAWN_RATE
        
        if self.boost_selection or self.game_over or self.paused:
            return
        
        # Update player
        self.player.update()
        
        # Update laser
        if self.player.laser_boost:
            # Create laser at player position
            laser = Laser(self.player.x + CAR_WIDTH // 2, self.player.y)
            self.lasers = [laser]  # Only one laser at a time
        else:
            self.lasers = []  # Clear lasers when boost is not active
        
        # Spawn enemies
        self.spawn_timer += 1
        if self.spawn_timer >= SPAWN_RATE:
            self.spawn_enemy()
            self.spawn_timer = 0
        
        # Spawn boosts occasionally
        self.boost_spawn_timer += 1
        if self.boost_spawn_timer >= 240:  # Every 4 seconds (more frequent)
            if random.random() < 0.8:  # 80% chance to spawn boost (higher chance)
                self.spawn_boost()
            self.boost_spawn_timer = 0
        
        # Update enemy cars
        slow_factor = 0.5 if self.player.slow_boost else 1.0  # Half speed when slow boost is active
        for car in self.enemy_cars[:]:
            car.update(slow_factor)
            
            # Check laser collision
            for laser in self.lasers:
                if laser.rect.colliderect(car.rect):
                    # Create explosion at car's position
                    explosion = Explosion(car.rect.centerx, car.rect.centery)
                    self.explosions.append(explosion)
                    
                    self.enemy_cars.remove(car)
                    self.score += 15  # Points for laser destruction
                    break
            else:
                # Only check other conditions if car wasn't destroyed by laser
                # Remove cars that are off screen and increase score
                if car.is_off_screen():
                    self.enemy_cars.remove(car)
                    self.score += 10
                
                # Check collision only if not invincible
                elif not self.player.invincible and car.rect.colliderect(self.player.rect):
                    self.game_over = True
                    self.update_high_scores(self.score)
        
        # Update boosts
        for boost in self.boosts[:]:
            boost.update(slow_factor)
            
            # Remove boosts that are off screen
            if boost.is_off_screen():
                self.boosts.remove(boost)
            
            # Check boost collection
            if boost.rect.colliderect(self.player.rect):
                self.boosts.remove(boost)
                self.score += 20  # Bonus points for collecting boost
                
                # Apply boost effect
                if boost.boost_type == 'line':
                    self.player.speed_boost = True
                    self.player.speed_boost_timer = 600  # 10 seconds (was 6)
                elif boost.boost_type == 'invincible':
                    self.player.invincible = True
                    self.player.invincible_timer = 720  # 12 seconds (was 8)
                elif boost.boost_type == 'rocket':
                    self.player.rocket_boost = True
                    self.player.rocket_boost_timer = 540  # 9 seconds (was 5)
                elif boost.boost_type == 'slow':
                    self.player.slow_boost = True
                    self.player.slow_boost_timer = 1200  # 20 seconds
                elif boost.boost_type == 'laser':
                    self.player.laser_boost = True
                    self.player.laser_boost_timer = 660  # 11 seconds
                elif boost.boost_type == 'agile':
                    self.player.agile_boost = True
                    self.player.agile_boost_timer = 600  # 10 seconds
                    # Automatically move to the appropriate divider position
                    if self.player.lane == 0:  # Left lane
                        self.player.agile_position = 0  # Left divider
                    else:  # Middle or right lane
                        self.player.agile_position = 1  # Right divider
                    
                    # Set target position to the divider line
                    divider_positions = [133, 267]  # Left=133, right=267
                    self.player.target_x = divider_positions[self.player.agile_position] - CAR_WIDTH // 4  # Thin car
                    self.player.moving = True
        
        # Update rockets
        for rocket in self.rockets[:]:
            rocket.update()
            
            # Remove rockets that are off screen
            if rocket.is_off_screen():
                self.rockets.remove(rocket)
                continue
            
            # Check rocket collision with enemy cars
            for car in self.enemy_cars[:]:
                if rocket.rect.colliderect(car.rect):
                    # Create explosion at car's position
                    explosion = Explosion(car.rect.centerx, car.rect.centery)
                    self.explosions.append(explosion)
                    
                    self.rockets.remove(rocket)
                    self.enemy_cars.remove(car)
                    self.score += 15   # Points for explosion effect
                    break
        
        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.is_finished():
                self.explosions.remove(explosion)
        
        # Increase difficulty over time
        self.speed_increase_timer += 1
        if self.speed_increase_timer >= 900:  # Every 15 seconds (slower progression)
            ENEMY_SPEED = min(ENEMY_SPEED + 0.15, 6)  # Smaller speed increases, lower max speed
            SPAWN_RATE = max(SPAWN_RATE - 3, 30)  # Smaller spawn rate changes, higher min rate
            self.speed_increase_timer = 0
    
    def reset_game(self):
        global ENEMY_SPEED, SPAWN_RATE
        self.player = PlayerCar()
        self.enemy_cars = []
        self.boosts = []
        self.rockets = []  # Reset rockets
        self.lasers = []  # Reset lasers
        self.explosions = []  # Reset explosions
        self.score = 0
        self.spawn_timer = 0
        self.boost_spawn_timer = 0
        self.game_over = False
        self.paused = False  # Reset pause state
        self.speed_increase_timer = 0
        self.new_high_score = False
        self.boost_selection = True  # Reset to boost selection
        self.selected_boost = None
        self.boost_given = False
        ENEMY_SPEED = 2
        SPAWN_RATE = 90
    
    def draw_road(self):
        # Draw road background
        self.screen.fill(DARK_GRAY)
        
        # Draw lane dividers
        for i in range(1, 3):
            x = i * LANE_WIDTH
            for y in range(0, WINDOW_HEIGHT, 40):
                pygame.draw.rect(self.screen, WHITE, (x - 2, y, 4, 20))
        
        # Draw road edges
        pygame.draw.rect(self.screen, WHITE, (0, 0, 4, WINDOW_HEIGHT))
        pygame.draw.rect(self.screen, WHITE, (WINDOW_WIDTH - 4, 0, 4, WINDOW_HEIGHT))
    
    def draw(self):
        # Draw boost selection screen
        if self.boost_selection:
            self.screen.fill(BLACK)
            
            # Title
            title_text = self.font.render("Choose Your Starting Boost", True, WHITE)
            title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, 100))
            self.screen.blit(title_text, title_rect)
            
            # Boost options
            y_start = 150
            spacing = 70
            
            # Line Boost (1)
            line_text = self.font.render("1. Line Boost", True, ORANGE)
            line_desc = self.small_font.render("Faster lane changes", True, WHITE)
            line_rect = line_text.get_rect(center=(WINDOW_WIDTH//2, y_start))
            line_desc_rect = line_desc.get_rect(center=(WINDOW_WIDTH//2, y_start + 25))
            self.screen.blit(line_text, line_rect)
            self.screen.blit(line_desc, line_desc_rect)
            
            # Invincible Boost (2)
            inv_text = self.font.render("2. Invincible", True, CYAN)
            inv_desc = self.small_font.render("No collision damage", True, WHITE)
            inv_rect = inv_text.get_rect(center=(WINDOW_WIDTH//2, y_start + spacing))
            inv_desc_rect = inv_desc.get_rect(center=(WINDOW_WIDTH//2, y_start + spacing + 25))
            self.screen.blit(inv_text, inv_rect)
            self.screen.blit(inv_desc, inv_desc_rect)
            
            # Rocket Boost (3)
            rocket_text = self.font.render("3. Rocket Boost", True, RED)
            rocket_desc = self.small_font.render("Shoot rockets with SPACE", True, WHITE)
            rocket_rect = rocket_text.get_rect(center=(WINDOW_WIDTH//2, y_start + spacing * 2))
            rocket_desc_rect = rocket_desc.get_rect(center=(WINDOW_WIDTH//2, y_start + spacing * 2 + 25))
            self.screen.blit(rocket_text, rocket_rect)
            self.screen.blit(rocket_desc, rocket_desc_rect)
            
            # Slow Boost (4)
            slow_text = self.font.render("4. Slow Boost", True, PURPLE)
            slow_desc = self.small_font.render("Slows down enemies", True, WHITE)
            slow_rect = slow_text.get_rect(center=(WINDOW_WIDTH//2, y_start + spacing * 3))
            slow_desc_rect = slow_desc.get_rect(center=(WINDOW_WIDTH//2, y_start + spacing * 3 + 25))
            self.screen.blit(slow_text, slow_rect)
            self.screen.blit(slow_desc, slow_desc_rect)
            
            # Laser Boost (5)
            laser_text = self.font.render("5. Laser Boost", True, (0, 255, 127))
            laser_desc = self.small_font.render("Destructive laser for 11 seconds", True, WHITE)
            laser_rect = laser_text.get_rect(center=(WINDOW_WIDTH//2, y_start + spacing * 4))
            laser_desc_rect = laser_desc.get_rect(center=(WINDOW_WIDTH//2, y_start + spacing * 4 + 25))
            self.screen.blit(laser_text, laser_rect)
            self.screen.blit(laser_desc, laser_desc_rect)
            
            # Agile Boost (6)
            agile_text = self.font.render("6. Agile Boost", True, (255, 100, 255))
            agile_desc = self.small_font.render("Thin car, move along dividers", True, WHITE)
            agile_rect = agile_text.get_rect(center=(WINDOW_WIDTH//2, y_start + spacing * 5))
            agile_desc_rect = agile_desc.get_rect(center=(WINDOW_WIDTH//2, y_start + spacing * 5 + 25))
            self.screen.blit(agile_text, agile_rect)
            self.screen.blit(agile_desc, agile_desc_rect)
            
            # Instructions
            instruction_text = self.small_font.render("Press 1, 2, 3, 4, 5, or 6 to select", True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 50))
            self.screen.blit(instruction_text, instruction_rect)
            
            # Game controls info
            controls_text = self.small_font.render("In game: P to pause, ESC to quit", True, GRAY)
            controls_rect = controls_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 20))
            self.screen.blit(controls_text, controls_rect)
            
            pygame.display.flip()
            return
        
        # Draw road
        self.draw_road()
        
        # Draw lasers (behind cars for visual effect)
        for laser in self.lasers:
            laser.draw(self.screen)
        
        # Draw cars
        self.player.draw(self.screen)
        for car in self.enemy_cars:
            car.draw(self.screen)
        
        # Draw boosts
        for boost in self.boosts:
            boost.draw(self.screen)
        
        # Draw rockets
        for rocket in self.rockets:
            rocket.draw(self.screen)
        
        # Draw explosions
        for explosion in self.explosions:
            explosion.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw high score
        best_score = max(self.high_scores) if any(self.high_scores) else 0
        high_score_text = self.small_font.render(f"Best: {best_score}", True, YELLOW)
        self.screen.blit(high_score_text, (10, 45))
        
        # Draw speed indicator
        speed_text = self.font.render(f"Speed: {ENEMY_SPEED:.1f}", True, WHITE)
        self.screen.blit(speed_text, (10, 75))
        
        # Draw boost status
        y_offset = 115
        if self.player.speed_boost:
            boost_text = self.font.render(f"Line Boost: {self.player.speed_boost_timer//60 + 1}s", True, ORANGE)
            self.screen.blit(boost_text, (10, y_offset))
            y_offset += 30
        
        if self.player.invincible:
            invincible_text = self.font.render(f"Invincible: {self.player.invincible_timer//60 + 1}s", True, CYAN)
            self.screen.blit(invincible_text, (10, y_offset))
            y_offset += 30
        
        if self.player.rocket_boost:
            rocket_text = self.font.render(f"Rocket Boost: {self.player.rocket_boost_timer//60 + 1}s", True, RED)
            self.screen.blit(rocket_text, (10, y_offset))
            y_offset += 30
        
        if self.player.slow_boost:
            slow_text = self.font.render(f"Slow Boost: {self.player.slow_boost_timer//60 + 1}s", True, PURPLE)
            self.screen.blit(slow_text, (10, y_offset))
            y_offset += 30
        
        if self.player.laser_boost:
            laser_text = self.font.render(f"Laser Boost: {self.player.laser_boost_timer//60 + 1}s", True, (0, 255, 127))
            self.screen.blit(laser_text, (10, y_offset))
            y_offset += 30
        
        if self.player.agile_boost:
            agile_text = self.font.render(f"Agile Boost: {self.player.agile_boost_timer//60 + 1}s", True, (255, 100, 255))
            self.screen.blit(agile_text, (10, y_offset))
        
        # Draw pause screen
        if self.paused:
            # Semi-transparent overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Pause text
            pause_text = self.big_font.render("PAUSED", True, WHITE)
            pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 40))
            self.screen.blit(pause_text, pause_rect)
            
            # Instructions
            resume_text = self.font.render("Press P to resume", True, WHITE)
            quit_text = self.font.render("Press ESC to quit", True, WHITE)
            
            resume_rect = resume_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 20))
            quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
            
            self.screen.blit(resume_text, resume_rect)
            self.screen.blit(quit_text, quit_rect)
        
        # Draw game over screen
        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Game over text
            if self.new_high_score:
                game_over_text = self.big_font.render("NEW HIGH SCORE!", True, YELLOW)
            else:
                game_over_text = self.big_font.render("CRASH!", True, RED)
            
            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            
            # High scores list
            high_scores_title = self.font.render("High Scores:", True, WHITE)
            
            # Center the text
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 120))
            final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 80))
            high_scores_title_rect = high_scores_title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 40))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(final_score_text, final_score_rect)
            self.screen.blit(high_scores_title, high_scores_title_rect)
            
            # Draw high scores list
            for i, score in enumerate(self.high_scores):
                color = YELLOW if score == self.score and self.new_high_score else WHITE
                score_text = self.small_font.render(f"{i+1}. {score}", True, color)
                score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 10 + i * 20))
                self.screen.blit(score_text, score_rect)
            
            # Control instructions
            restart_text = self.font.render("Press SPACE to restart", True, WHITE)
            quit_text = self.font.render("Press ESC to quit", True, WHITE)
            
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 100))
            quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 130))
            
            self.screen.blit(restart_text, restart_rect)
            self.screen.blit(quit_text, quit_rect)
        
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
    game = CarDodgeGame()
    game.run()

if __name__ == "__main__":
    main()