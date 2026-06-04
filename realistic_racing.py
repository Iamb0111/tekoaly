import pygame
import math
import random
import sys
import time

# Initialize pygame and mixer for sounds
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
LIGHT_GRAY = (200, 200, 200)
DARK_GREEN = (0, 100, 0)
PURPLE = (128, 0, 128)

class SoundManager:
    def __init__(self):
        self.engine_sound = None
        self.tire_screech = None
        self.crash_sound = None
        self.engine_volume = 0.3
        self.engine_pitch = 1.0
        self.create_sounds()
    
    def create_sounds(self):
        """Create procedural sounds using pygame"""
        try:
            # Create engine sound (low frequency rumble)
            self.create_engine_sound()
            # Create tire screech sound
            self.create_tire_sound()
            # Create crash sound
            self.create_crash_sound()
        except:
            print("Sound creation failed, continuing without audio")
    
    def create_engine_sound(self):
        """Create engine rumble sound"""
        duration = 1.0
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = []
        for i in range(frames):
            time_point = float(i) / sample_rate
            # Mix multiple frequencies for realistic engine sound
            wave = 0
            wave += 0.3 * math.sin(2 * math.pi * 80 * time_point)  # Base frequency
            wave += 0.2 * math.sin(2 * math.pi * 160 * time_point) # Harmonic
            wave += 0.1 * math.sin(2 * math.pi * 240 * time_point) # Higher harmonic
            wave += 0.05 * random.uniform(-1, 1)  # Engine noise
            arr.append([int(wave * 32767), int(wave * 32767)])
        
        sound_array = pygame.sndarray.make_sound(arr)
        self.engine_sound = sound_array
    
    def create_tire_sound(self):
        """Create tire screech sound"""
        duration = 0.5
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = []
        for i in range(frames):
            time_point = float(i) / sample_rate
            # High frequency noise for tire screech
            wave = 0.5 * random.uniform(-1, 1)
            wave += 0.3 * math.sin(2 * math.pi * 1000 * time_point)
            # Fade out
            fade = 1.0 - (time_point / duration)
            wave *= fade
            arr.append([int(wave * 16383), int(wave * 16383)])
        
        sound_array = pygame.sndarray.make_sound(arr)
        self.tire_screech = sound_array
    
    def create_crash_sound(self):
        """Create crash sound"""
        duration = 0.8
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = []
        for i in range(frames):
            time_point = float(i) / sample_rate
            # Noise burst with decay
            wave = random.uniform(-1, 1) * 0.8
            # Add some metallic resonance
            wave += 0.2 * math.sin(2 * math.pi * 300 * time_point)
            # Exponential decay
            decay = math.exp(-time_point * 3)
            wave *= decay
            arr.append([int(wave * 32767), int(wave * 32767)])
        
        sound_array = pygame.sndarray.make_sound(arr)
        self.crash_sound = sound_array
    
    def play_engine(self, throttle, rpm):
        """Play engine sound with dynamic pitch based on RPM"""
        if self.engine_sound:
            try:
                # Adjust pitch based on RPM
                pitch = 1.0 + (rpm - 1000) / 4000  # Base pitch adjustment
                volume = 0.1 + throttle * 0.4
                
                # Simple pitch simulation by playing at different volumes/frequencies
                if hasattr(pygame.mixer, 'Channel'):
                    channel = pygame.mixer.Channel(0)
                    if not channel.get_busy():
                        channel.play(self.engine_sound, loops=-1)
                    channel.set_volume(volume)
            except:
                pass
    
    def play_tire_screech(self):
        """Play tire screech sound"""
        if self.tire_screech:
            try:
                pygame.mixer.Channel(1).play(self.tire_screech)
            except:
                pass
    
    def play_crash(self):
        """Play crash sound"""
        if self.crash_sound:
            try:
                pygame.mixer.Channel(2).play(self.crash_sound)
            except:
                pass

class Particle:
    def __init__(self, x, y, vx, vy, color, life):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.life = life
        self.max_life = life
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # Gravity
        self.vx *= 0.98  # Air resistance
        self.vy *= 0.98
        self.life -= 1
    
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            color = (*self.color[:3], alpha)
            size = max(1, int(3 * (self.life / self.max_life)))
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0  # Car direction in radians
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 0
        self.max_speed = 12
        self.acceleration = 0.3
        self.deceleration = 0.15
        self.turn_speed = 0.08
        self.friction = 0.95
        
        # Car dimensions
        self.width = 30
        self.height = 15
        
        # Engine simulation
        self.throttle = 0
        self.rpm = 1000
        self.gear = 1
        
        # Physics
        self.mass = 1000  # kg
        self.drag_coefficient = 0.001
        
        # Damage system
        self.health = 100
        self.max_health = 100
        
        # Tire marks
        self.tire_marks = []
        self.last_positions = []
        
        # Particles for effects
        self.particles = []
    
    def update(self, keys, dt):
        # Input handling
        throttle = 0
        steering = 0
        braking = False
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            throttle = 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            braking = True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            steering = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            steering = 1
        
        self.throttle = throttle
        
        # Engine simulation
        if throttle > 0:
            self.rpm = min(6000, self.rpm + 50 * throttle)
            # Apply acceleration
            force_x = math.cos(self.angle) * self.acceleration * throttle
            force_y = math.sin(self.angle) * self.acceleration * throttle
            self.velocity_x += force_x
            self.velocity_y += force_y
        else:
            self.rpm = max(1000, self.rpm - 30)
        
        # Braking
        if braking:
            self.velocity_x *= 0.9
            self.velocity_y *= 0.9
            # Add brake particles
            if self.speed > 1:
                self.add_brake_particles()
        
        # Steering (only works when moving)
        if abs(self.speed) > 0.5 and steering != 0:
            # Realistic steering - less effective at high speeds
            turn_factor = max(0.3, 1.0 - abs(self.speed) / self.max_speed)
            self.angle += steering * self.turn_speed * turn_factor * (abs(self.speed) / 5)
        
        # Physics simulation
        self.apply_physics(dt)
        
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Calculate speed
        self.speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        
        # Speed limit
        if self.speed > self.max_speed:
            self.velocity_x = (self.velocity_x / self.speed) * self.max_speed
            self.velocity_y = (self.velocity_y / self.speed) * self.max_speed
            self.speed = self.max_speed
        
        # Add tire marks when turning/sliding
        if abs(steering) > 0.1 and self.speed > 2:
            self.add_tire_mark()
        
        # Update particles
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()
        
        # Keep track of recent positions for skid marks
        self.last_positions.append((self.x, self.y))
        if len(self.last_positions) > 10:
            self.last_positions.pop(0)
    
    def apply_physics(self, dt):
        """Apply realistic physics"""
        # Air resistance
        drag_force_x = -self.drag_coefficient * self.velocity_x * abs(self.velocity_x)
        drag_force_y = -self.drag_coefficient * self.velocity_y * abs(self.velocity_y)
        
        self.velocity_x += drag_force_x
        self.velocity_y += drag_force_y
        
        # Ground friction
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction
        
        # Tire friction (lateral forces)
        # Calculate car's forward direction
        forward_x = math.cos(self.angle)
        forward_y = math.sin(self.angle)
        
        # Project velocity onto car's forward direction
        forward_velocity = self.velocity_x * forward_x + self.velocity_y * forward_y
        
        # Calculate lateral velocity (sideways sliding)
        lateral_velocity_x = self.velocity_x - forward_velocity * forward_x
        lateral_velocity_y = self.velocity_y - forward_velocity * forward_y
        
        # Apply lateral friction (resist sliding)
        lateral_friction = 0.85
        self.velocity_x -= lateral_velocity_x * (1 - lateral_friction)
        self.velocity_y -= lateral_velocity_y * (1 - lateral_friction)
    
    def add_tire_mark(self):
        """Add tire mark at current position"""
        # Calculate tire positions
        tire_offset = 8
        left_tire_x = self.x - math.sin(self.angle) * tire_offset
        left_tire_y = self.y + math.cos(self.angle) * tire_offset
        right_tire_x = self.x + math.sin(self.angle) * tire_offset
        right_tire_y = self.y - math.cos(self.angle) * tire_offset
        
        self.tire_marks.append({
            'left': (left_tire_x, left_tire_y),
            'right': (right_tire_x, right_tire_y),
            'life': 300
        })
        
        # Limit tire marks
        if len(self.tire_marks) > 100:
            self.tire_marks.pop(0)
    
    def add_brake_particles(self):
        """Add brake dust particles"""
        for _ in range(3):
            particle_x = self.x + random.uniform(-10, 10)
            particle_y = self.y + random.uniform(-10, 10)
            vx = random.uniform(-2, 2)
            vy = random.uniform(-2, 2)
            self.particles.append(Particle(particle_x, particle_y, vx, vy, GRAY, 30))
    
    def add_crash_particles(self):
        """Add crash particles"""
        for _ in range(20):
            particle_x = self.x + random.uniform(-15, 15)
            particle_y = self.y + random.uniform(-15, 15)
            vx = random.uniform(-8, 8)
            vy = random.uniform(-8, 8)
            color = random.choice([RED, ORANGE, YELLOW, DARK_GRAY])
            self.particles.append(Particle(particle_x, particle_y, vx, vy, color, 60))
    
    def take_damage(self, amount):
        """Take damage from collision"""
        self.health -= amount
        self.add_crash_particles()
        if self.health <= 0:
            self.health = 0
    
    def draw(self, screen):
        # Draw tire marks first (behind car)
        for mark in self.tire_marks:
            if mark['life'] > 0:
                alpha = int(100 * (mark['life'] / 300))
                if alpha > 0:
                    pygame.draw.circle(screen, DARK_GRAY, (int(mark['left'][0]), int(mark['left'][1])), 2)
                    pygame.draw.circle(screen, DARK_GRAY, (int(mark['right'][0]), int(mark['right'][1])), 2)
                mark['life'] -= 1
        
        # Draw car body with 3D effect
        car_points = self.get_car_points()
        
        # Draw shadow
        shadow_points = [(p[0] + 2, p[1] + 2) for p in car_points]
        pygame.draw.polygon(screen, DARK_GRAY, shadow_points)
        
        # Main car body
        car_color = RED
        if self.health < 30:
            car_color = DARK_GRAY  # Damaged car
        elif self.health < 60:
            car_color = (200, 100, 100)  # Slightly damaged
        
        pygame.draw.polygon(screen, car_color, car_points)
        pygame.draw.polygon(screen, BLACK, car_points, 2)
        
        # Draw windows
        window_points = self.get_window_points()
        pygame.draw.polygon(screen, LIGHT_GRAY, window_points)
        pygame.draw.polygon(screen, BLACK, window_points, 1)
        
        # Draw headlights
        headlight_points = self.get_headlight_points()
        for point in headlight_points:
            pygame.draw.circle(screen, YELLOW, (int(point[0]), int(point[1])), 3)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(screen)
        
        # Draw health bar
        bar_width = 40
        bar_height = 6
        bar_x = self.x - bar_width // 2
        bar_y = self.y - 25
        
        # Background
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        # Health
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height), 1)
    
    def get_car_points(self):
        """Get car outline points for drawing"""
        # Car dimensions
        half_width = self.width // 2
        half_height = self.height // 2
        
        # Local coordinates
        points = [
            (-half_width, -half_height),
            (half_width, -half_height),
            (half_width, half_height),
            (-half_width, half_height)
        ]
        
        # Rotate and translate
        rotated_points = []
        for px, py in points:
            # Rotate
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            # Translate
            rotated_points.append((self.x + rx, self.y + ry))
        
        return rotated_points
    
    def get_window_points(self):
        """Get window points for drawing"""
        # Smaller rectangle for windows
        half_width = (self.width // 2) - 4
        half_height = (self.height // 2) - 2
        
        points = [
            (-half_width, -half_height),
            (half_width, -half_height),
            (half_width, half_height),
            (-half_width, half_height)
        ]
        
        rotated_points = []
        for px, py in points:
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            rotated_points.append((self.x + rx, self.y + ry))
        
        return rotated_points
    
    def get_headlight_points(self):
        """Get headlight positions"""
        # Front of car
        front_x = self.x + math.cos(self.angle) * (self.width // 2)
        front_y = self.y + math.sin(self.angle) * (self.width // 2)
        
        # Offset for left and right headlights
        offset = 6
        left_x = front_x - math.sin(self.angle) * offset
        left_y = front_y + math.cos(self.angle) * offset
        right_x = front_x + math.sin(self.angle) * offset
        right_y = front_y - math.cos(self.angle) * offset
        
        return [(left_x, left_y), (right_x, right_y)]

class Track:
    def __init__(self):
        self.barriers = []
        self.checkpoints = []
        self.start_line = None
        self.create_track()
    
    def create_track(self):
        """Create a realistic racing track"""
        # Track boundaries (outer walls)
        margin = 50
        
        # Outer boundary
        self.barriers.extend([
            # Top wall
            {'start': (margin, margin), 'end': (WINDOW_WIDTH - margin, margin)},
            # Right wall
            {'start': (WINDOW_WIDTH - margin, margin), 'end': (WINDOW_WIDTH - margin, WINDOW_HEIGHT - margin)},
            # Bottom wall
            {'start': (WINDOW_WIDTH - margin, WINDOW_HEIGHT - margin), 'end': (margin, WINDOW_HEIGHT - margin)},
            # Left wall
            {'start': (margin, WINDOW_HEIGHT - margin), 'end': (margin, margin)}
        ])
        
        # Inner track obstacles/barriers
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        
        # Central island
        island_size = 100
        self.barriers.extend([
            {'start': (center_x - island_size, center_y - island_size), 
             'end': (center_x + island_size, center_y - island_size)},
            {'start': (center_x + island_size, center_y - island_size), 
             'end': (center_x + island_size, center_y + island_size)},
            {'start': (center_x + island_size, center_y + island_size), 
             'end': (center_x - island_size, center_y + island_size)},
            {'start': (center_x - island_size, center_y + island_size), 
             'end': (center_x - island_size, center_y - island_size)}
        ])
        
        # Additional barriers for realism
        self.barriers.extend([
            # Chicane elements
            {'start': (200, 200), 'end': (300, 180)},
            {'start': (400, 220), 'end': (500, 200)},
            {'start': (800, 300), 'end': (900, 320)},
            {'start': (700, 500), 'end': (800, 480)},
        ])
        
        # Start line
        self.start_line = {'start': (100, WINDOW_HEIGHT - 200), 'end': (100, WINDOW_HEIGHT - 150)}
        
        # Checkpoints for lap counting
        self.checkpoints = [
            {'pos': (WINDOW_WIDTH - 100, center_y), 'passed': False},
            {'pos': (center_x, 100), 'passed': False},
            {'pos': (100, center_y), 'passed': False}
        ]
    
    def check_collision(self, car):
        """Check if car collides with track barriers"""
        car_points = car.get_car_points()
        
        for barrier in self.barriers:
            if self.line_polygon_collision(barrier['start'], barrier['end'], car_points):
                return True
        return False
    
    def line_polygon_collision(self, line_start, line_end, polygon):
        """Check if line segment intersects with polygon"""
        # Simplified collision detection
        for i in range(len(polygon)):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % len(polygon)]
            
            if self.lines_intersect(line_start, line_end, p1, p2):
                return True
        return False
    
    def lines_intersect(self, line1_start, line1_end, line2_start, line2_end):
        """Check if two line segments intersect"""
        x1, y1 = line1_start
        x2, y2 = line1_end
        x3, y3 = line2_start
        x4, y4 = line2_end
        
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 0.001:
            return False
        
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
        
        return 0 <= t <= 1 and 0 <= u <= 1
    
    def draw(self, screen):
        # Draw track surface
        track_color = DARK_GRAY
        pygame.draw.rect(screen, track_color, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Draw grass/background
        grass_color = DARK_GREEN
        pygame.draw.rect(screen, grass_color, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Draw track area
        track_margin = 50
        pygame.draw.rect(screen, DARK_GRAY, 
                        (track_margin, track_margin, 
                         WINDOW_WIDTH - 2*track_margin, WINDOW_HEIGHT - 2*track_margin))
        
        # Draw barriers
        for barrier in self.barriers:
            pygame.draw.line(screen, WHITE, barrier['start'], barrier['end'], 4)
            # Add 3D effect
            start_x, start_y = barrier['start']
            end_x, end_y = barrier['end']
            pygame.draw.line(screen, LIGHT_GRAY, 
                           (start_x + 1, start_y + 1), (end_x + 1, end_y + 1), 2)
        
        # Draw start line
        if self.start_line:
            pygame.draw.line(screen, YELLOW, self.start_line['start'], self.start_line['end'], 6)
            # Checkered pattern
            for i in range(0, 50, 10):
                if i % 20 == 0:
                    y_pos = self.start_line['start'][1] + i
                    pygame.draw.line(screen, BLACK, (95, y_pos), (105, y_pos), 3)
        
        # Draw checkpoints
        for checkpoint in self.checkpoints:
            color = GREEN if checkpoint['passed'] else RED
            pygame.draw.circle(screen, color, (int(checkpoint['pos'][0]), int(checkpoint['pos'][1])), 8)
            pygame.draw.circle(screen, WHITE, (int(checkpoint['pos'][0]), int(checkpoint['pos'][1])), 8, 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Realistic Racing Simulator")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game objects
        self.car = Car(120, WINDOW_HEIGHT - 175)
        self.track = Track()
        self.sound_manager = SoundManager()
        
        # Game state
        self.running = True
        self.lap_time = 0
        self.best_lap_time = float('inf')
        self.current_lap = 1
        self.total_laps = 3
        self.race_finished = False
        self.start_time = time.time()
        
        # Camera
        self.camera_x = 0
        self.camera_y = 0
        
        # Performance monitoring
        self.fps_counter = 0
        self.fps_timer = 0
        self.current_fps = 60
    
    def update_camera(self):
        """Update camera to follow car"""
        target_x = self.car.x - WINDOW_WIDTH // 2
        target_y = self.car.y - WINDOW_HEIGHT // 2
        
        # Smooth camera movement
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_y += (target_y - self.camera_y) * 0.1
        
        # Keep camera in bounds
        self.camera_x = max(0, min(self.camera_x, WINDOW_WIDTH))
        self.camera_y = max(0, min(self.camera_y, WINDOW_HEIGHT))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.restart_race()
    
    def restart_race(self):
        """Restart the race"""
        self.car = Car(120, WINDOW_HEIGHT - 175)
        self.lap_time = 0
        self.current_lap = 1
        self.race_finished = False
        self.start_time = time.time()
        for checkpoint in self.track.checkpoints:
            checkpoint['passed'] = False
    
    def update(self, dt):
        if not self.race_finished:
            keys = pygame.key.get_pressed()
            self.car.update(keys, dt)
            
            # Update camera
            self.update_camera()
            
            # Check collisions
            if self.track.check_collision(self.car):
                self.car.take_damage(20)
                self.sound_manager.play_crash()
                # Bounce back
                self.car.velocity_x *= -0.5
                self.car.velocity_y *= -0.5
            
            # Update lap time
            self.lap_time = time.time() - self.start_time
            
            # Play engine sound
            self.sound_manager.play_engine(self.car.throttle, self.car.rpm)
            
            # Check if car is sliding (for tire screech)
            if self.car.speed > 5 and abs(self.car.velocity_x) > 2:
                self.sound_manager.play_tire_screech()
        
        # Update FPS counter
        self.fps_counter += 1
        self.fps_timer += dt
        if self.fps_timer >= 1.0:
            self.current_fps = self.fps_counter
            self.fps_counter = 0
            self.fps_timer = 0
    
    def draw_hud(self):
        """Draw heads-up display"""
        # Speed
        speed_kmh = int(self.car.speed * 10)  # Convert to km/h scale
        speed_text = self.font.render(f"Speed: {speed_kmh} km/h", True, WHITE)
        self.screen.blit(speed_text, (10, 10))
        
        # RPM
        rpm_text = self.font.render(f"RPM: {int(self.car.rpm)}", True, WHITE)
        self.screen.blit(rpm_text, (10, 50))
        
        # Gear (simplified)
        gear = min(6, max(1, int(self.car.rpm / 1200)))
        gear_text = self.font.render(f"Gear: {gear}", True, WHITE)
        self.screen.blit(gear_text, (10, 90))
        
        # Health
        health_text = self.font.render(f"Health: {int(self.car.health)}%", True, WHITE)
        self.screen.blit(health_text, (10, 130))
        
        # Lap info
        lap_text = self.font.render(f"Lap: {self.current_lap}/{self.total_laps}", True, WHITE)
        self.screen.blit(lap_text, (WINDOW_WIDTH - 200, 10))
        
        # Time
        time_text = self.font.render(f"Time: {self.lap_time:.1f}s", True, WHITE)
        self.screen.blit(time_text, (WINDOW_WIDTH - 200, 50))
        
        # Best lap
        if self.best_lap_time < float('inf'):
            best_text = self.font.render(f"Best: {self.best_lap_time:.1f}s", True, YELLOW)
            self.screen.blit(best_text, (WINDOW_WIDTH - 200, 90))
        
        # FPS
        fps_text = self.small_font.render(f"FPS: {self.current_fps}", True, WHITE)
        self.screen.blit(fps_text, (WINDOW_WIDTH - 80, WINDOW_HEIGHT - 30))
        
        # Controls
        controls = [
            "WASD/Arrows - Drive",
            "R - Restart Race",
            "ESC - Exit"
        ]
        for i, control in enumerate(controls):
            text = self.small_font.render(control, True, WHITE)
            self.screen.blit(text, (10, WINDOW_HEIGHT - 80 + i * 20))
        
        # Race status
        if self.race_finished:
            finish_text = self.font.render("RACE FINISHED!", True, YELLOW)
            text_rect = finish_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            # Background
            pygame.draw.rect(self.screen, BLACK, text_rect.inflate(20, 10))
            self.screen.blit(finish_text, text_rect)
        
        # Damage warning
        if self.car.health < 30:
            warning_text = self.font.render("CRITICAL DAMAGE!", True, RED)
            text_rect = warning_text.get_rect(center=(WINDOW_WIDTH//2, 50))
            self.screen.blit(warning_text, text_rect)
    
    def draw(self):
        # Clear screen
        self.screen.fill(DARK_GREEN)
        
        # Draw track
        self.track.draw(self.screen)
        
        # Draw car
        self.car.draw(self.screen)
        
        # Draw HUD
        self.draw_hud()
        
        pygame.display.flip()
    
    def run(self):
        last_time = time.time()
        
        while self.running:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            self.handle_events()
            self.update(dt)
            self.draw()
            
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
