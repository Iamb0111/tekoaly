import pygame
import math
import random
import sys
from pygame import gfxdraw

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
BROWN = (139, 69, 19)
DARK_GREEN = (0, 128, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)

class Vector3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector3D(0, 0, 0)
        return Vector3D(self.x/mag, self.y/mag, self.z/mag)
    
    def cross(self, other):
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

class Camera3D:
    def __init__(self):
        self.position = Vector3D(0, 5, 10)
        self.target = Vector3D(0, 0, 0)
        self.up = Vector3D(0, 1, 0)
        self.fov = 60
        self.near = 0.1
        self.far = 1000
        
        # Mouse look
        self.yaw = 0
        self.pitch = 0
        self.sensitivity = 0.002
        
    def update_look(self, mouse_dx, mouse_dy):
        self.yaw += mouse_dx * self.sensitivity
        self.pitch -= mouse_dy * self.sensitivity
        self.pitch = max(-math.pi/2 + 0.1, min(math.pi/2 - 0.1, self.pitch))
        
        # Update target based on yaw and pitch
        self.target.x = self.position.x + math.cos(self.pitch) * math.sin(self.yaw)
        self.target.y = self.position.y + math.sin(self.pitch)
        self.target.z = self.position.z + math.cos(self.pitch) * math.cos(self.yaw)
    
    def move_forward(self, distance):
        direction = (self.target - self.position).normalize()
        self.position = self.position + direction * distance
        self.target = self.target + direction * distance
    
    def move_right(self, distance):
        forward = (self.target - self.position).normalize()
        right = forward.cross(self.up).normalize()
        self.position = self.position + right * distance
        self.target = self.target + right * distance
    
    def move_up(self, distance):
        self.position.y += distance
        self.target.y += distance

class Object3D:
    def __init__(self, position=Vector3D(0, 0, 0)):
        self.position = position
        self.rotation = Vector3D(0, 0, 0)
        self.scale = Vector3D(1, 1, 1)
        self.vertices = []
        self.faces = []
        self.color = WHITE
        self.velocity = Vector3D(0, 0, 0)
        self.angular_velocity = Vector3D(0, 0, 0)
        
    def add_vertex(self, x, y, z):
        self.vertices.append(Vector3D(x, y, z))
    
    def add_face(self, *vertex_indices):
        self.faces.append(list(vertex_indices))
    
    def transform_vertex(self, vertex):
        # Apply scaling
        v = Vector3D(
            vertex.x * self.scale.x,
            vertex.y * self.scale.y,
            vertex.z * self.scale.z
        )
        
        # Apply rotation
        # Rotate around Y axis
        cos_y = math.cos(self.rotation.y)
        sin_y = math.sin(self.rotation.y)
        x = v.x * cos_y - v.z * sin_y
        z = v.x * sin_y + v.z * cos_y
        v.x, v.z = x, z
        
        # Rotate around X axis
        cos_x = math.cos(self.rotation.x)
        sin_x = math.sin(self.rotation.x)
        y = v.y * cos_x - v.z * sin_x
        z = v.y * sin_x + v.z * cos_x
        v.y, v.z = y, z
        
        # Rotate around Z axis
        cos_z = math.cos(self.rotation.z)
        sin_z = math.sin(self.rotation.z)
        x = v.x * cos_z - v.y * sin_z
        y = v.x * sin_z + v.y * cos_z
        v.x, v.y = x, y
        
        # Apply translation
        v.x += self.position.x
        v.y += self.position.y
        v.z += self.position.z
        
        return v
    
    def update(self, dt):
        # Update position
        self.position = self.position + self.velocity * dt
        
        # Update rotation
        self.rotation = self.rotation + self.angular_velocity * dt

class Cube(Object3D):
    def __init__(self, position=Vector3D(0, 0, 0), size=1, color=WHITE):
        super().__init__(position)
        self.color = color
        s = size / 2
        
        # Define cube vertices
        self.add_vertex(-s, -s, -s)  # 0
        self.add_vertex(s, -s, -s)   # 1
        self.add_vertex(s, s, -s)    # 2
        self.add_vertex(-s, s, -s)   # 3
        self.add_vertex(-s, -s, s)   # 4
        self.add_vertex(s, -s, s)    # 5
        self.add_vertex(s, s, s)     # 6
        self.add_vertex(-s, s, s)    # 7
        
        # Define faces
        self.add_face(0, 1, 2, 3)  # Front
        self.add_face(5, 4, 7, 6)  # Back
        self.add_face(4, 0, 3, 7)  # Left
        self.add_face(1, 5, 6, 2)  # Right
        self.add_face(3, 2, 6, 7)  # Top
        self.add_face(4, 5, 1, 0)  # Bottom

class Pyramid(Object3D):
    def __init__(self, position=Vector3D(0, 0, 0), size=1, color=YELLOW):
        super().__init__(position)
        self.color = color
        s = size / 2
        h = size
        
        # Define pyramid vertices
        self.add_vertex(-s, 0, -s)   # 0 - Base
        self.add_vertex(s, 0, -s)    # 1 - Base
        self.add_vertex(s, 0, s)     # 2 - Base
        self.add_vertex(-s, 0, s)    # 3 - Base
        self.add_vertex(0, h, 0)     # 4 - Apex
        
        # Define faces
        self.add_face(0, 1, 2, 3)    # Base
        self.add_face(0, 4, 1)       # Side 1
        self.add_face(1, 4, 2)       # Side 2
        self.add_face(2, 4, 3)       # Side 3
        self.add_face(3, 4, 0)       # Side 4

class Sphere(Object3D):
    def __init__(self, position=Vector3D(0, 0, 0), radius=1, color=BLUE, detail=8):
        super().__init__(position)
        self.color = color
        self.radius = radius
        
        # Generate sphere vertices
        for i in range(detail + 1):
            lat = math.pi * i / detail - math.pi/2
            for j in range(detail * 2 + 1):
                lon = 2 * math.pi * j / (detail * 2)
                
                x = radius * math.cos(lat) * math.cos(lon)
                y = radius * math.sin(lat)
                z = radius * math.cos(lat) * math.sin(lon)
                
                self.add_vertex(x, y, z)
        
        # Generate faces
        for i in range(detail):
            for j in range(detail * 2):
                p1 = i * (detail * 2 + 1) + j
                p2 = p1 + detail * 2 + 1
                p3 = p1 + 1
                p4 = p2 + 1
                
                if i < detail and j < detail * 2:
                    if p1 < len(self.vertices) and p2 < len(self.vertices) and \
                       p3 < len(self.vertices) and p4 < len(self.vertices):
                        self.add_face(p1, p2, p4, p3)

class Player:
    def __init__(self):
        self.position = Vector3D(0, 1, 0)
        self.velocity = Vector3D(0, 0, 0)
        self.health = 100
        self.max_health = 100
        self.speed = 8
        self.jump_power = 12
        self.on_ground = False
        self.score = 0
        self.level = 1
        self.experience = 0
        self.energy = 100
        self.max_energy = 100
        self.weapons = ['Sword', 'Bow', 'Magic Staff']
        self.current_weapon = 0
        self.abilities = ['Dash', 'Shield', 'Fireball']
        self.inventory = {'Gold': 0, 'Gems': 0, 'Potions': 3}
        
    def move(self, direction, dt):
        if self.energy > 0:
            self.velocity = self.velocity + direction * self.speed * dt
            self.energy = max(0, self.energy - 10 * dt)
    
    def jump(self):
        if self.on_ground and self.energy > 20:
            self.velocity.y = self.jump_power
            self.on_ground = False
            self.energy -= 20
    
    def dash(self, direction):
        if self.energy > 30:
            self.velocity = self.velocity + direction * 15
            self.energy -= 30
    
    def use_ability(self, ability_index):
        if ability_index < len(self.abilities) and self.energy > 40:
            self.energy -= 40
            return self.abilities[ability_index]
        return None
    
    def update(self, dt):
        # Apply gravity
        self.velocity.y -= 30 * dt
        
        # Update position
        self.position = self.position + self.velocity * dt
        
        # Ground collision
        if self.position.y <= 1:
            self.position.y = 1
            self.velocity.y = 0
            self.on_ground = True
        
        # Friction
        self.velocity.x *= 0.85
        self.velocity.z *= 0.85
        
        # Regenerate energy
        self.energy = min(self.max_energy, self.energy + 25 * dt)
        
        # Regenerate health slowly
        if self.health < self.max_health:
            self.health = min(self.max_health, self.health + 5 * dt)

class Enemy(Object3D):
    def __init__(self, position, enemy_type="basic"):
        super().__init__(position)
        self.enemy_type = enemy_type
        self.health = 50
        self.max_health = 50
        self.speed = 3
        self.attack_damage = 10
        self.attack_cooldown = 0
        self.target = None
        self.ai_state = "patrol"
        self.patrol_center = position
        self.patrol_radius = 10
        self.patrol_angle = 0
        
        if enemy_type == "fast":
            self.color = RED
            self.speed = 6
            self.health = 30
            self.attack_damage = 8
        elif enemy_type == "strong":
            self.color = PURPLE
            self.speed = 1.5
            self.health = 100
            self.attack_damage = 20
        elif enemy_type == "flying":
            self.color = CYAN
            self.speed = 4
            self.health = 40
            self.attack_damage = 12
        else:
            self.color = ORANGE
    
    def update(self, dt, player_pos):
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        
        # AI behavior
        distance_to_player = (player_pos - self.position).magnitude()
        
        if distance_to_player < 15:  # Detection range
            self.ai_state = "chase"
            direction = (player_pos - self.position).normalize()
            self.velocity = direction * self.speed
            
            if distance_to_player < 2 and self.attack_cooldown <= 0:
                self.attack_cooldown = 1.0
                return True  # Attack player
        else:
            # Patrol behavior
            self.ai_state = "patrol"
            self.patrol_angle += dt
            target_x = self.patrol_center.x + math.cos(self.patrol_angle) * self.patrol_radius
            target_z = self.patrol_center.z + math.sin(self.patrol_angle) * self.patrol_radius
            
            direction = Vector3D(target_x - self.position.x, 0, target_z - self.position.z).normalize()
            self.velocity = direction * (self.speed * 0.5)
        
        # Update position
        super().update(dt)
        
        # Keep enemies on ground
        if self.enemy_type != "flying":
            self.position.y = max(0.5, self.position.y)
        
        return False

class Collectible(Object3D):
    def __init__(self, position, item_type="coin"):
        super().__init__(position)
        self.item_type = item_type
        self.value = 10
        self.collected = False
        self.float_offset = 0
        self.rotation_speed = 2
        
        if item_type == "coin":
            self.color = GOLD
            self.value = 10
        elif item_type == "gem":
            self.color = PURPLE
            self.value = 50
        elif item_type == "health_potion":
            self.color = RED
            self.value = 30
        elif item_type == "energy_potion":
            self.color = BLUE
            self.value = 40
        elif item_type == "power_orb":
            self.color = WHITE
            self.value = 100
    
    def update(self, dt):
        # Floating animation
        self.float_offset += dt * 3
        self.position.y += math.sin(self.float_offset) * 0.02
        
        # Rotation animation
        self.rotation.y += self.rotation_speed * dt
        
        super().update(dt)

class Projectile(Object3D):
    def __init__(self, position, direction, projectile_type="fireball"):
        super().__init__(position)
        self.direction = direction.normalize()
        self.speed = 20
        self.damage = 25
        self.lifetime = 3.0
        self.age = 0
        self.projectile_type = projectile_type
        
        if projectile_type == "fireball":
            self.color = ORANGE
            self.scale = Vector3D(0.3, 0.3, 0.3)
        elif projectile_type == "ice_shard":
            self.color = CYAN
            self.damage = 20
            self.scale = Vector3D(0.2, 0.4, 0.2)
        elif projectile_type == "lightning":
            self.color = YELLOW
            self.damage = 35
            self.speed = 30
            self.scale = Vector3D(0.1, 0.1, 0.1)
        
        self.velocity = self.direction * self.speed
    
    def update(self, dt):
        self.age += dt
        super().update(dt)
        return self.age < self.lifetime

class Renderer3D:
    def __init__(self, screen, camera):
        self.screen = screen
        self.camera = camera
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        
    def project_point(self, point_3d):
        # Transform point relative to camera
        cam_pos = self.camera.position
        cam_target = self.camera.target
        cam_up = self.camera.up
        
        # Calculate view matrix
        forward = (cam_target - cam_pos).normalize()
        right = forward.cross(cam_up).normalize()
        up = right.cross(forward)
        
        # Transform to camera space
        rel_pos = point_3d - cam_pos
        cam_x = rel_pos.dot(right)
        cam_y = rel_pos.dot(up)
        cam_z = rel_pos.dot(forward)
        
        # Perspective projection
        if cam_z <= 0.1:
            return None
        
        fov_rad = math.radians(self.camera.fov)
        aspect = self.width / self.height
        
        # Project to screen coordinates
        screen_x = (cam_x / cam_z) / math.tan(fov_rad / 2) / aspect
        screen_y = (cam_y / cam_z) / math.tan(fov_rad / 2)
        
        # Convert to pixel coordinates
        pixel_x = (screen_x + 1) * self.width / 2
        pixel_y = (1 - screen_y) * self.height / 2
        
        return (int(pixel_x), int(pixel_y), cam_z)
    
    def draw_object(self, obj):
        # Transform vertices
        transformed_vertices = []
        for vertex in obj.vertices:
            world_vertex = obj.transform_vertex(vertex)
            projected = self.project_point(world_vertex)
            if projected:
                transformed_vertices.append(projected)
            else:
                transformed_vertices.append(None)
        
        # Draw faces
        for face in obj.faces:
            face_vertices = []
            valid_face = True
            avg_z = 0
            
            for vertex_index in face:
                if vertex_index < len(transformed_vertices) and transformed_vertices[vertex_index]:
                    face_vertices.append(transformed_vertices[vertex_index][:2])
                    avg_z += transformed_vertices[vertex_index][2]
                else:
                    valid_face = False
                    break
            
            if valid_face and len(face_vertices) >= 3:
                avg_z /= len(face_vertices)
                
                # Calculate shading based on distance
                brightness = max(0.2, min(1.0, 50 / avg_z))
                shaded_color = tuple(int(c * brightness) for c in obj.color)
                
                # Draw filled polygon
                try:
                    pygame.draw.polygon(self.screen, shaded_color, face_vertices)
                    pygame.draw.polygon(self.screen, BLACK, face_vertices, 1)
                except:
                    pass
    
    def draw_line_3d(self, start, end, color=WHITE):
        start_proj = self.project_point(start)
        end_proj = self.project_point(end)
        
        if start_proj and end_proj:
            pygame.draw.line(self.screen, color, start_proj[:2], end_proj[:2], 2)
    
    def draw_particle_effect(self, position, color, size=5):
        projected = self.project_point(position)
        if projected:
            pygame.draw.circle(self.screen, color, projected[:2], size)

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def add_explosion(self, position, color=ORANGE, count=20):
        for _ in range(count):
            velocity = Vector3D(
                random.uniform(-5, 5),
                random.uniform(0, 8),
                random.uniform(-5, 5)
            )
            self.particles.append({
                'position': Vector3D(position.x, position.y, position.z),
                'velocity': velocity,
                'color': color,
                'life': 1.0,
                'max_life': 1.0
            })
    
    def add_magic_effect(self, position, color=PURPLE, count=15):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            velocity = Vector3D(
                math.cos(angle) * speed,
                random.uniform(0, 4),
                math.sin(angle) * speed
            )
            self.particles.append({
                'position': Vector3D(position.x, position.y, position.z),
                'velocity': velocity,
                'color': color,
                'life': 1.5,
                'max_life': 1.5
            })
    
    def update(self, dt):
        for particle in self.particles[:]:
            particle['life'] -= dt
            if particle['life'] <= 0:
                self.particles.remove(particle)
                continue
            
            # Update position
            particle['position'] = particle['position'] + particle['velocity'] * dt
            
            # Apply gravity
            particle['velocity'].y -= 10 * dt
            
            # Fade color
            alpha = particle['life'] / particle['max_life']
            particle['alpha'] = alpha
    
    def draw(self, renderer):
        for particle in self.particles:
            alpha = particle.get('alpha', 1.0)
            color = tuple(int(c * alpha) for c in particle['color'])
            size = max(1, int(5 * alpha))
            renderer.draw_particle_effect(particle['position'], color, size)

class Game3D:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Epic 3D Adventure - Ultimate Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 48)
        
        # Game state
        self.running = True
        self.paused = False
        self.game_state = "menu"  # menu, playing, game_over, victory
        self.level = 1
        self.wave = 1
        self.enemies_remaining = 0
        
        # 3D System
        self.camera = Camera3D()
        self.renderer = Renderer3D(self.screen, self.camera)
        self.particle_system = ParticleSystem()
        
        # Game objects
        self.player = Player()
        self.objects = []
        self.enemies = []
        self.collectibles = []
        self.projectiles = []
        
        # Input
        self.keys_pressed = set()
        self.mouse_locked = False
        self.last_mouse_pos = (0, 0)
        
        # UI
        self.menu_selection = 0
        self.menu_options = ["Start Game", "Instructions", "Quit"]
        
        # Initialize world
        self.create_world()
        self.spawn_wave()
        
    def create_world(self):
        """Create the 3D world with platforms, obstacles, and decorations"""
        # Ground platforms
        for x in range(-50, 51, 10):
            for z in range(-50, 51, 10):
                if random.random() < 0.3:  # 30% chance for platform
                    height = random.uniform(0.2, 2.0)
                    platform = Cube(Vector3D(x, height/2, z), height, GRAY)
                    self.objects.append(platform)
        
        # Decorative objects
        for _ in range(20):
            x = random.uniform(-40, 40)
            z = random.uniform(-40, 40)
            y = random.uniform(2, 8)
            
            obj_type = random.choice(['cube', 'pyramid', 'sphere'])
            color = random.choice([RED, GREEN, BLUE, YELLOW, PURPLE, CYAN])
            
            if obj_type == 'cube':
                obj = Cube(Vector3D(x, y, z), random.uniform(1, 3), color)
            elif obj_type == 'pyramid':
                obj = Pyramid(Vector3D(x, y, z), random.uniform(1, 3), color)
            else:
                obj = Sphere(Vector3D(x, y, z), random.uniform(0.5, 2), color)
            
            # Add some rotation
            obj.angular_velocity = Vector3D(
                random.uniform(-1, 1),
                random.uniform(-1, 1),
                random.uniform(-1, 1)
            )
            
            self.objects.append(obj)
        
        # Add collectibles
        for _ in range(30):
            x = random.uniform(-35, 35)
            z = random.uniform(-35, 35)
            y = random.uniform(1, 3)
            
            item_type = random.choice(['coin', 'gem', 'health_potion', 'energy_potion'])
            collectible = Collectible(Vector3D(x, y, z), item_type)
            
            # Make collectibles small cubes for simplicity
            collectible.vertices = []
            collectible.faces = []
            s = 0.3
            collectible.add_vertex(-s, -s, -s)
            collectible.add_vertex(s, -s, -s)
            collectible.add_vertex(s, s, -s)
            collectible.add_vertex(-s, s, -s)
            collectible.add_vertex(-s, -s, s)
            collectible.add_vertex(s, -s, s)
            collectible.add_vertex(s, s, s)
            collectible.add_vertex(-s, s, s)
            collectible.add_face(0, 1, 2, 3)
            collectible.add_face(5, 4, 7, 6)
            collectible.add_face(4, 0, 3, 7)
            collectible.add_face(1, 5, 6, 2)
            collectible.add_face(3, 2, 6, 7)
            collectible.add_face(4, 5, 1, 0)
            
            self.collectibles.append(collectible)
    
    def spawn_wave(self):
        """Spawn a new wave of enemies"""
        enemy_count = 5 + self.wave * 2
        self.enemies_remaining = enemy_count
        
        for _ in range(enemy_count):
            # Spawn enemies away from player
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(20, 40)
            x = math.cos(angle) * distance
            z = math.sin(angle) * distance
            
            enemy_types = ['basic', 'fast', 'strong']
            if self.wave > 3:
                enemy_types.append('flying')
            
            enemy_type = random.choice(enemy_types)
            enemy = Enemy(Vector3D(x, 1, z), enemy_type)
            
            # Create enemy as a cube
            enemy.vertices = []
            enemy.faces = []
            s = 0.8
            enemy.add_vertex(-s, 0, -s)
            enemy.add_vertex(s, 0, -s)
            enemy.add_vertex(s, 2*s, -s)
            enemy.add_vertex(-s, 2*s, -s)
            enemy.add_vertex(-s, 0, s)
            enemy.add_vertex(s, 0, s)
            enemy.add_vertex(s, 2*s, s)
            enemy.add_vertex(-s, 2*s, s)
            enemy.add_face(0, 1, 2, 3)
            enemy.add_face(5, 4, 7, 6)
            enemy.add_face(4, 0, 3, 7)
            enemy.add_face(1, 5, 6, 2)
            enemy.add_face(3, 2, 6, 7)
            enemy.add_face(4, 5, 1, 0)
            
            self.enemies.append(enemy)
    
    def handle_input(self):
        """Handle all input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                
                if self.game_state == "menu":
                    if event.key == pygame.K_UP:
                        self.menu_selection = (self.menu_selection - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.menu_selection = (self.menu_selection + 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        if self.menu_selection == 0:  # Start Game
                            self.game_state = "playing"
                            self.mouse_locked = True
                            pygame.mouse.set_visible(False)
                        elif self.menu_selection == 1:  # Instructions
                            pass  # Could add instructions screen
                        elif self.menu_selection == 2:  # Quit
                            self.running = False
                
                elif self.game_state == "playing":
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "menu"
                        self.mouse_locked = False
                        pygame.mouse.set_visible(True)
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_SPACE:
                        self.player.jump()
                    elif event.key == pygame.K_1:
                        self.player.current_weapon = 0
                    elif event.key == pygame.K_2:
                        self.player.current_weapon = 1
                    elif event.key == pygame.K_3:
                        self.player.current_weapon = 2
                    elif event.key == pygame.K_q:
                        # Use ability
                        ability = self.player.use_ability(0)
                        if ability == "Fireball":
                            self.cast_fireball()
                        elif ability == "Shield":
                            self.player.health = min(self.player.max_health, self.player.health + 20)
                        elif ability == "Dash":
                            forward = (self.camera.target - self.camera.position).normalize()
                            self.player.dash(forward)
                    elif event.key == pygame.K_e:
                        # Use ability 2
                        ability = self.player.use_ability(1)
                        if ability:
                            self.particle_system.add_magic_effect(self.player.position)
                    elif event.key == pygame.K_r:
                        # Use ability 3
                        ability = self.player.use_ability(2)
                        if ability:
                            self.cast_area_spell()
            
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
            
            elif event.type == pygame.MOUSEMOTION and self.mouse_locked:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
                
                dx = mouse_x - center_x
                dy = mouse_y - center_y
                
                if dx != 0 or dy != 0:
                    self.camera.update_look(dx, dy)
                    pygame.mouse.set_pos(center_x, center_y)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and self.game_state == "playing":
                if event.button == 1:  # Left click - attack
                    self.player_attack()
                elif event.button == 3:  # Right click - special attack
                    self.cast_fireball()
    
    def cast_fireball(self):
        """Cast a fireball projectile"""
        if self.player.energy >= 30:
            direction = (self.camera.target - self.camera.position).normalize()
            fireball = Projectile(
                Vector3D(self.player.position.x, self.player.position.y + 1, self.player.position.z),
                direction,
                "fireball"
            )
            
            # Create fireball as sphere
            fireball.vertices = []
            fireball.faces = []
            detail = 6
            radius = 0.3
            
            for i in range(detail + 1):
                lat = math.pi * i / detail - math.pi/2
                for j in range(detail * 2 + 1):
                    lon = 2 * math.pi * j / (detail * 2)
                    x = radius * math.cos(lat) * math.cos(lon)
                    y = radius * math.sin(lat)
                    z = radius * math.cos(lat) * math.sin(lon)
                    fireball.add_vertex(x, y, z)
            
            # Simple faces for fireball
            for i in range(detail):
                for j in range(detail * 2):
                    p1 = i * (detail * 2 + 1) + j
                    p2 = p1 + detail * 2 + 1
                    p3 = p1 + 1
                    p4 = p2 + 1
                    
                    if p1 < len(fireball.vertices) and p2 < len(fireball.vertices) and \
                       p3 < len(fireball.vertices) and p4 < len(fireball.vertices):
                        fireball.add_face(p1, p2, p4, p3)
            
            self.projectiles.append(fireball)
            self.player.energy -= 30
            
            # Add particle effect
            self.particle_system.add_magic_effect(fireball.position, ORANGE, 10)
    
    def cast_area_spell(self):
        """Cast an area of effect spell"""
        for enemy in self.enemies[:]:
            distance = (enemy.position - self.player.position).magnitude()
            if distance < 10:
                enemy.health -= 40
                self.particle_system.add_explosion(enemy.position, PURPLE, 15)
                if enemy.health <= 0:
                    self.enemies.remove(enemy)
                    self.enemies_remaining -= 1
                    self.player.score += 50
    
    def player_attack(self):
        """Player melee attack"""
        weapon = self.player.weapons[self.player.current_weapon]
        attack_range = 3
        damage = 25
        
        if weapon == "Sword":
            damage = 30
        elif weapon == "Bow":
            damage = 20
            attack_range = 15
        elif weapon == "Magic Staff":
            damage = 35
            self.player.energy -= 10
        
        # Find enemies in range
        for enemy in self.enemies[:]:
            distance = (enemy.position - self.player.position).magnitude()
            if distance < attack_range:
                enemy.health -= damage
                self.particle_system.add_explosion(enemy.position, RED, 8)
                
                if enemy.health <= 0:
                    self.enemies.remove(enemy)
                    self.enemies_remaining -= 1
                    self.player.score += 25
                    
                    # Drop collectible
                    if random.random() < 0.3:
                        item_type = random.choice(['coin', 'gem', 'health_potion'])
                        collectible = Collectible(enemy.position, item_type)
                        self.setup_collectible_geometry(collectible)
                        self.collectibles.append(collectible)
    
    def setup_collectible_geometry(self, collectible):
        """Setup geometry for collectible"""
        collectible.vertices = []
        collectible.faces = []
        s = 0.3
        collectible.add_vertex(-s, -s, -s)
        collectible.add_vertex(s, -s, -s)
        collectible.add_vertex(s, s, -s)
        collectible.add_vertex(-s, s, -s)
        collectible.add_vertex(-s, -s, s)
        collectible.add_vertex(s, -s, s)
        collectible.add_vertex(s, s, s)
        collectible.add_vertex(-s, s, s)
        collectible.add_face(0, 1, 2, 3)
        collectible.add_face(5, 4, 7, 6)
        collectible.add_face(4, 0, 3, 7)
        collectible.add_face(1, 5, 6, 2)
        collectible.add_face(3, 2, 6, 7)
        collectible.add_face(4, 5, 1, 0)
    
    def update_player_movement(self, dt):
        """Update player movement based on input"""
        if self.paused:
            return
        
        movement_speed = self.player.speed * dt
        
        # Calculate camera direction vectors
        forward = (self.camera.target - self.camera.position).normalize()
        right = forward.cross(Vector3D(0, 1, 0)).normalize()
        
        # Movement
        movement = Vector3D(0, 0, 0)
        
        if pygame.K_w in self.keys_pressed:
            movement = movement + forward * movement_speed
        if pygame.K_s in self.keys_pressed:
            movement = movement - forward * movement_speed
        if pygame.K_a in self.keys_pressed:
            movement = movement - right * movement_speed
        if pygame.K_d in self.keys_pressed:
            movement = movement + right * movement_speed
        
        # Apply movement
        if movement.magnitude() > 0:
            self.player.move(movement, dt)
        
        # Update camera to follow player
        self.camera.position.x = self.player.position.x
        self.camera.position.z = self.player.position.z
        self.camera.position.y = self.player.position.y + 2
    
    def update_game_logic(self, dt):
        """Update main game logic"""
        if self.paused or self.game_state != "playing":
            return
        
        # Update player
        self.player.update(dt)
        
        # Update objects
        for obj in self.objects:
            obj.update(dt)
        
        # Update enemies
        for enemy in self.enemies[:]:
            attacked = enemy.update(dt, self.player.position)
            if attacked:
                self.player.health -= enemy.attack_damage
                self.particle_system.add_explosion(self.player.position, RED, 5)
                
                if self.player.health <= 0:
                    self.game_state = "game_over"
        
        # Update collectibles
        for collectible in self.collectibles[:]:
            collectible.update(dt)
            
            # Check collection
            distance = (collectible.position - self.player.position).magnitude()
            if distance < 2:
                self.collect_item(collectible)
                self.collectibles.remove(collectible)
        
        # Update projectiles
        for projectile in self.projectiles[:]:
            if not projectile.update(dt):
                self.projectiles.remove(projectile)
                continue
            
            # Check projectile hits
            for enemy in self.enemies[:]:
                distance = (projectile.position - enemy.position).magnitude()
                if distance < 1.5:
                    enemy.health -= projectile.damage
                    self.particle_system.add_explosion(enemy.position, projectile.color, 10)
                    self.projectiles.remove(projectile)
                    
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.enemies_remaining -= 1
                        self.player.score += 35
                    break
        
        # Update particle system
        self.particle_system.update(dt)
        
        # Check wave completion
        if self.enemies_remaining <= 0:
            self.wave += 1
            self.spawn_wave()
            self.player.experience += 100
            self.player.score += 200
            
            # Level up check
            if self.player.experience >= self.player.level * 100:
                self.player.level += 1
                self.player.max_health += 20
                self.player.health = self.player.max_health
                self.player.max_energy += 20
                self.player.energy = self.player.max_energy
                self.particle_system.add_magic_effect(self.player.position, GOLD, 25)
    
    def collect_item(self, item):
        """Handle item collection"""
        if item.item_type == "coin":
            self.player.inventory['Gold'] += item.value
            self.player.score += item.value
        elif item.item_type == "gem":
            self.player.inventory['Gems'] += 1
            self.player.score += item.value
        elif item.item_type == "health_potion":
            self.player.health = min(self.player.max_health, self.player.health + item.value)
        elif item.item_type == "energy_potion":
            self.player.energy = min(self.player.max_energy, self.player.energy + item.value)
        elif item.item_type == "power_orb":
            self.player.score += item.value
            self.player.experience += 50
        
        # Particle effect
        self.particle_system.add_magic_effect(item.position, item.color, 8)
    
    def draw_menu(self):
        """Draw the main menu"""
        self.screen.fill(BLACK)
        
        # Title
        title = self.big_font.render("EPIC 3D ADVENTURE", True, GOLD)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 150))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font.render("Ultimate Edition", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH//2, 200))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Menu options
        for i, option in enumerate(self.menu_options):
            color = YELLOW if i == self.menu_selection else WHITE
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, 300 + i * 60))
            self.screen.blit(text, text_rect)
        
        # Instructions
        instructions = [
            "WASD - Move",
            "Mouse - Look around",
            "Space - Jump",
            "Q/E/R - Use abilities",
            "1/2/3 - Switch weapons",
            "Left Click - Attack",
            "Right Click - Fireball",
            "P - Pause"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, GRAY)
            self.screen.blit(text, (50, 400 + i * 25))
    
    def draw_hud(self):
        """Draw the heads-up display"""
        # Health bar
        health_ratio = self.player.health / self.player.max_health
        health_width = 200
        health_height = 20
        
        pygame.draw.rect(self.screen, DARK_GRAY, (20, 20, health_width, health_height))
        pygame.draw.rect(self.screen, RED, (20, 20, health_width * health_ratio, health_height))
        pygame.draw.rect(self.screen, WHITE, (20, 20, health_width, health_height), 2)
        
        health_text = self.small_font.render(f"Health: {int(self.player.health)}/{self.player.max_health}", True, WHITE)
        self.screen.blit(health_text, (25, 25))
        
        # Energy bar
        energy_ratio = self.player.energy / self.player.max_energy
        pygame.draw.rect(self.screen, DARK_GRAY, (20, 50, health_width, health_height))
        pygame.draw.rect(self.screen, BLUE, (20, 50, health_width * energy_ratio, health_height))
        pygame.draw.rect(self.screen, WHITE, (20, 50, health_width, health_height), 2)
        
        energy_text = self.small_font.render(f"Energy: {int(self.player.energy)}/{self.player.max_energy}", True, WHITE)
        self.screen.blit(energy_text, (25, 55))
        
        # Score and level
        score_text = self.font.render(f"Score: {self.player.score}", True, GOLD)
        self.screen.blit(score_text, (20, 90))
        
        level_text = self.font.render(f"Level: {self.player.level}", True, GOLD)
        self.screen.blit(level_text, (20, 120))
        
        wave_text = self.font.render(f"Wave: {self.wave}", True, YELLOW)
        self.screen.blit(wave_text, (20, 150))
        
        enemies_text = self.font.render(f"Enemies: {self.enemies_remaining}", True, RED)
        self.screen.blit(enemies_text, (20, 180))
        
        # Current weapon
        weapon_text = self.font.render(f"Weapon: {self.player.weapons[self.player.current_weapon]}", True, WHITE)
        self.screen.blit(weapon_text, (WINDOW_WIDTH - 250, 20))
        
        # Inventory
        inventory_y = 50
        for item, count in self.player.inventory.items():
            inv_text = self.small_font.render(f"{item}: {count}", True, WHITE)
            self.screen.blit(inv_text, (WINDOW_WIDTH - 150, inventory_y))
            inventory_y += 25
        
        # Abilities cooldown indicators
        abilities_y = 140
        for i, ability in enumerate(self.player.abilities):
            color = GREEN if self.player.energy >= 40 else RED
            ability_text = self.small_font.render(f"{ability} ({['Q','E','R'][i]})", True, color)
            self.screen.blit(ability_text, (WINDOW_WIDTH - 200, abilities_y + i * 25))
        
        # Crosshair
        center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        pygame.draw.line(self.screen, WHITE, (center_x - 10, center_y), (center_x + 10, center_y), 2)
        pygame.draw.line(self.screen, WHITE, (center_x, center_y - 10), (center_x, center_y + 10), 2)
    
    def draw_game_over(self):
        """Draw game over screen"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.big_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.font.render(f"Final Score: {self.player.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.screen.blit(score_text, score_rect)
        
        restart_text = self.font.render("Press ESC to return to menu", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_3d_scene(self):
        """Draw the main 3D scene"""
        # Sort objects by distance for proper rendering
        all_objects = []
        
        # Add world objects
        for obj in self.objects:
            distance = (obj.position - self.camera.position).magnitude()
            all_objects.append((distance, obj))
        
        # Add enemies
        for enemy in self.enemies:
            distance = (enemy.position - self.camera.position).magnitude()
            all_objects.append((distance, enemy))
        
        # Add collectibles
        for collectible in self.collectibles:
            distance = (collectible.position - self.camera.position).magnitude()
            all_objects.append((distance, collectible))
        
        # Add projectiles
        for projectile in self.projectiles:
            distance = (projectile.position - self.camera.position).magnitude()
            all_objects.append((distance, projectile))
        
        # Sort by distance (farthest first)
        all_objects.sort(key=lambda x: x[0], reverse=True)
        
        # Draw all objects
        for distance, obj in all_objects:
            self.renderer.draw_object(obj)
        
        # Draw particle effects
        self.particle_system.draw(self.renderer)
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            self.handle_input()
            
            if self.game_state == "playing":
                self.update_player_movement(dt)
                self.update_game_logic(dt)
                
                # Draw 3D scene
                self.screen.fill(BLACK)
                self.draw_3d_scene()
                self.draw_hud()
                
                if self.paused:
                    pause_text = self.big_font.render("PAUSED", True, YELLOW)
                    pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
                    self.screen.blit(pause_text, pause_rect)
                
                if self.game_state == "game_over":
                    self.draw_game_over()
            
            elif self.game_state == "menu":
                self.draw_menu()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game3D()
    game.run()
