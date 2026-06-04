import pygame
import sys
import random
import math
import json
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1000
FPS = 60

# Colors - Ultimate Color Palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)
NEON_GREEN = (57, 255, 20)
NEON_BLUE = (77, 77, 255)
NEON_PINK = (255, 20, 147)
NEON_PURPLE = (191, 0, 255)
NEON_ORANGE = (255, 95, 31)
DARK_RED = (139, 0, 0)
DARK_GREEN = (0, 100, 0)
DARK_BLUE = (0, 0, 139)
ROYAL_BLUE = (65, 105, 225)
FOREST_GREEN = (34, 139, 34)
FIRE_RED = (255, 69, 0)
ICE_BLUE = (176, 224, 230)
LIGHTNING_YELLOW = (255, 255, 224)
SHADOW_PURPLE = (72, 61, 139)
LAVA_ORANGE = (255, 140, 0)
COSMIC_VIOLET = (138, 43, 226)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
BROWN = (139, 69, 19)
LIGHT_BROWN = (205, 133, 63)

# Element Colors
FIRE_COLORS = [(255, 0, 0), (255, 69, 0), (255, 140, 0), (255, 215, 0)]
ICE_COLORS = [(176, 224, 230), (173, 216, 230), (135, 206, 235), (70, 130, 180)]
LIGHTNING_COLORS = [(255, 255, 0), (255, 255, 224), (255, 215, 0), (255, 165, 0)]
NATURE_COLORS = [(34, 139, 34), (0, 128, 0), (154, 205, 50), (124, 252, 0)]
SHADOW_COLORS = [(72, 61, 139), (75, 0, 130), (138, 43, 226), (148, 0, 211)]

class GameMode(Enum):
    ADVENTURE = "adventure"
    BATTLE_ROYALE = "battle_royale"
    TOWER_DEFENSE = "tower_defense"
    RACING = "racing"
    PUZZLE = "puzzle"
    SURVIVAL = "survival"
    BUILDING = "building"
    RPG = "rpg"
    SUPER_SHADOW = "super_shadow"

class Element(Enum):
    FIRE = "fire"
    ICE = "ice"
    LIGHTNING = "lightning"
    NATURE = "nature"
    SHADOW = "shadow"
    LIGHT = "light"
    NEUTRAL = "neutral"

class Particle:
    def __init__(self, x, y, vx, vy, color, size=3, life=60, gravity=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life
        self.gravity = gravity
        self.alpha = 255
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.vx *= 0.99
        self.vy *= 0.99
        self.life -= 1
        self.alpha = int(255 * (self.life / self.max_life))
        return self.life > 0
    
    def draw(self, screen):
        if self.life > 0:
            color_with_alpha = (*self.color[:3], self.alpha)
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

class FloatingText:
    def __init__(self, x, y, text, color, font_size=24):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, font_size)
        self.life = 60  # 1 second at 60 FPS
        self.max_life = 60
        self.vy = -2  # Float upward
        self.alpha = 255
    
    def update(self):
        self.y += self.vy
        self.life -= 1
        self.alpha = int(255 * (self.life / self.max_life))
        return self.life > 0
    
    def draw(self, screen):
        if self.life > 0:
            # Create surface with alpha
            text_surface = self.font.render(self.text, True, self.color)
            text_surface.set_alpha(self.alpha)
            screen.blit(text_surface, (int(self.x), int(self.y)))

class Player:
    def __init__(self, x, y, player_class="mage"):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 50
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 4  # REDUCED from 6 for difficulty
        self.on_ground = False
        self.facing_right = True
        
        # RPG Stats
        self.level = 1
        self.experience = 0
        self.experience_to_next = 100
        self.skill_points = 5
        
        # Core Stats - REDUCED for difficulty
        self.health = 60  # Reduced from 100
        self.max_health = 60  # Reduced from 100
        self.stamina = 100
        self.max_stamina = 100
        self.shield = 0
        self.max_shield = 0
        
        # Attributes
        self.strength = 10
        self.intelligence = 10
        self.agility = 10
        self.vitality = 10
        self.luck = 10
        
        # Class System
        self.player_class = player_class
        self.class_level = 1
        self.primary_element = Element.NEUTRAL
        self.secondary_element = None
        
        # Equipment
        self.weapon = None
        self.armor = None
        self.accessories = []
        
        # Inventory and Economy
        self.inventory = {}
        self.gold = 1000
        self.gems = {}  # Different types of magical gems
        
        # Combat - REDUCED for difficulty
        self.attack_power = 30  # Reduced from 50
        self.magic_power = 35   # Reduced from 50
        self.defense = 10       # Reduced from 20
        self.magic_resistance = 10  # Reduced from 20
        self.critical_chance = 0.03  # Reduced from 0.05
        self.dodge_chance = 0.05     # Reduced from 0.1
        self.attack_range = 60
        self.attack_cooldown = 0
        self.is_attacking = False
        self.attack_animation = 0
        
        # Movement Abilities
        self.can_double_jump = True
        self.double_jumped = False
        self.dash_cooldown = 0
        self.wall_jump_available = True
        self.jump_pressed = False
        
        # Visual Effects
        self.trail = []
        self.aura_color = NEON_BLUE
        self.animation_frame = 0
        self.hit_flash = 0
        
        # Initialize based on class
        self.setup_class()
    
    def setup_class(self):
        """Initialize player based on chosen class"""
        if self.player_class == "mage":
            self.primary_element = Element.FIRE
            self.intelligence += 5
            self.aura_color = NEON_PURPLE
            
        elif self.player_class == "warrior":
            self.primary_element = Element.NEUTRAL
            self.strength += 5
            self.vitality += 3
            self.max_health += 50
            self.health = self.max_health
            self.attack_power += 30
            self.defense += 15
            self.aura_color = NEON_ORANGE
            
        elif self.player_class == "archer":
            self.primary_element = Element.NATURE
            self.agility += 5
            self.luck += 3
            self.critical_chance += 0.1
            self.speed += 2
            self.aura_color = NEON_GREEN
            
        elif self.player_class == "assassin":
            self.primary_element = Element.SHADOW
            self.agility += 7
            self.dodge_chance += 0.15
            self.critical_chance += 0.2
            self.speed += 3
            self.aura_color = SHADOW_PURPLE
    
    def jump(self):
        """Handle jumping with double jump support"""
        if self.on_ground:
            self.vel_y = -15
            self.on_ground = False
            self.double_jumped = False
            return True
        elif self.can_double_jump and not self.double_jumped:
            self.vel_y = -12  # Slightly weaker second jump
            self.double_jumped = True
            # Create particle effect for double jump
            self.create_jump_particles()
            return True
        return False
    
    def create_jump_particles(self):
        """Create visual effect for double jump"""
        particles = []
        for _ in range(15):
            angle = random.uniform(math.pi/4, 3*math.pi/4)  # Particles shoot downward
            speed = random.uniform(3, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            color = random.choice([NEON_BLUE, CYAN, WHITE, self.aura_color])
            particles.append(Particle(
                self.x + self.width//2 + random.randint(-10, 10),
                self.y + self.height,
                vx, vy, color, random.randint(2, 4), 25, 0
            ))
        return particles
    
    def attack(self, enemies):
        """Perform melee attack on nearby enemies"""
        if self.attack_cooldown > 0:
            return []
        
        self.is_attacking = True
        self.attack_animation = 15  # Attack animation duration
        self.attack_cooldown = 60  # INCREASED attack cooldown for difficulty
        
        particles = []
        damaged_enemies = []
        
        # Calculate attack area
        attack_x = self.x + self.width if self.facing_right else self.x - self.attack_range
        attack_y = self.y
        attack_width = self.attack_range
        attack_height = self.height
        
        # Check for enemies in attack range
        for enemy in enemies:
            if (enemy.x < attack_x + attack_width and
                enemy.x + enemy.width > attack_x and
                enemy.y < attack_y + attack_height and
                enemy.y + enemy.height > attack_y):
                
                # Calculate damage
                base_damage = self.attack_power
                if random.random() < self.critical_chance:
                    base_damage *= 2  # Critical hit
                    
                # Apply damage
                enemy.health -= base_damage
                damaged_enemies.append(enemy)
                
                # Create hit particles
                for _ in range(10):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(2, 6)
                    vx = math.cos(angle) * speed
                    vy = math.sin(angle) * speed
                    color = random.choice([RED, ORANGE, YELLOW])
                    particles.append(Particle(
                        enemy.x + enemy.width//2,
                        enemy.y + enemy.height//2,
                        vx, vy, color, random.randint(2, 5), 20, 0
                    ))
        
        # Create attack effect particles
        for _ in range(8):
            effect_x = self.x + self.width//2 + (self.attack_range//2 if self.facing_right else -self.attack_range//2)
            effect_y = self.y + self.height//2
            angle = random.uniform(-math.pi/4, math.pi/4) + (0 if self.facing_right else math.pi)
            speed = random.uniform(5, 10)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            color = self.aura_color
            particles.append(Particle(
                effect_x, effect_y, vx, vy, color, random.randint(3, 6), 15, 0
            ))
        
        return particles
    
    def update(self, platforms):
        # Handle input
        keys = pygame.key.get_pressed()
        
        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = max(self.vel_x - 1, -self.speed)
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = min(self.vel_x + 1, self.speed)
            self.facing_right = True
        else:
            self.vel_x *= 0.8
        
        # Apply gravity
        self.vel_y += 0.8
        if self.vel_y > 15:
            self.vel_y = 15
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Platform collision
        self.on_ground = False
        for platform in platforms:
            if (self.x < platform.x + platform.width and
                self.x + self.width > platform.x and
                self.y < platform.y + platform.height and
                self.y + self.height > platform.y):
                
                if self.vel_y > 0 and self.y < platform.y:
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    self.double_jumped = False
        
        # Screen boundaries
        if self.x < 0:
            self.x = 0
        elif self.x > WINDOW_WIDTH - self.width:
            self.x = WINDOW_WIDTH - self.width
        
        if self.y > WINDOW_HEIGHT:
            self.take_damage(40)  # INCREASED fall damage for difficulty
            self.x = 100
            self.y = 100
        
        # Regeneration
        if self.stamina < self.max_stamina:
            self.stamina += 1
        
        # Update cooldowns
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        if self.attack_animation > 0:
            self.attack_animation -= 1
        else:
            self.is_attacking = False
        
        if self.hit_flash > 0:
            self.hit_flash -= 1
        
        # Update trail
        self.trail.append((self.x + self.width//2, self.y + self.height//2))
        if len(self.trail) > 20:
            self.trail.pop(0)
        
        self.animation_frame += 1
    
    def take_damage(self, damage):
        """Take damage with defense calculations"""
        actual_damage = max(1, damage - self.defense)
        
        if self.shield > 0:
            self.shield -= actual_damage
            if self.shield < 0:
                self.health += self.shield
                self.shield = 0
        else:
            self.health -= actual_damage
        
        self.hit_flash = 20
        
        if self.health <= 0:
            self.health = 0
            return True
        return False
    
    def add_experience(self, amount):
        """Add experience and handle level ups"""
        self.experience += amount
        leveled_up = False
        
        while self.experience >= self.experience_to_next:
            self.experience -= self.experience_to_next
            self.level += 1
            self.experience_to_next = int(self.experience_to_next * 1.2)
            self.skill_points += 3
            
            # Stat increases on level up - REDUCED for difficulty
            self.max_health += random.randint(4, 8)  # Reduced from 8-15
            self.max_stamina += random.randint(2, 4)  # Reduced from 3-8
            
            # Level up bonus - REDUCED heal for difficulty
            level_up_heal = self.max_health // 4  # Only heal 25% instead of 50%
            self.health = min(self.health + level_up_heal, self.max_health)
            self.stamina = self.max_stamina
            
            leveled_up = True
        
        return leveled_up
    
    def draw(self, screen):
        # Draw trail
        for i, pos in enumerate(self.trail):
            if i > 0:
                alpha = int(255 * (i / len(self.trail)))
                trail_color = (*self.aura_color[:3], alpha // 4)
                size = max(1, int(6 * (i / len(self.trail))))
                pygame.draw.circle(screen, self.aura_color, pos, size)
        
        # Draw aura
        aura_intensity = 50 + math.sin(self.animation_frame * 0.1) * 20
        aura_surface = pygame.Surface((self.width + 20, self.height + 20))
        aura_surface.set_alpha(int(aura_intensity))
        pygame.draw.ellipse(aura_surface, self.aura_color, (0, 0, self.width + 20, self.height + 20))
        screen.blit(aura_surface, (self.x - 10, self.y - 10))
        
        # Draw player
        color = WHITE
        if self.hit_flash > 0 and self.hit_flash % 10 < 5:
            color = RED
        
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.aura_color, (self.x, self.y, self.width, self.height), 3)
        
        # Class indicator
        if self.player_class == "mage":
            # Staff
            staff_x = self.x + self.width + 5 if self.facing_right else self.x - 15
            pygame.draw.line(screen, BROWN, (staff_x, self.y + 10), (staff_x, self.y + 40), 3)
            pygame.draw.circle(screen, self.aura_color, (staff_x, self.y + 10), 5)
        
        elif self.player_class == "warrior":
            # Sword
            sword_x = self.x + self.width + 5 if self.facing_right else self.x - 20
            pygame.draw.rect(screen, SILVER, (sword_x, self.y + 15, 15, 25))
            pygame.draw.polygon(screen, SILVER, [(sword_x + 7, self.y + 15), (sword_x + 3, self.y + 5), (sword_x + 11, self.y + 5)])
        
        elif self.player_class == "archer":
            # Bow
            bow_x = self.x + self.width + 5 if self.facing_right else self.x - 15
            pygame.draw.arc(screen, BROWN, (bow_x - 5, self.y + 10, 10, 30), 0, math.pi, 2)
        
        elif self.player_class == "assassin":
            # Daggers
            dagger_x = self.x + self.width + 3 if self.facing_right else self.x - 12
            pygame.draw.line(screen, SILVER, (dagger_x, self.y + 20), (dagger_x + 8, self.y + 15), 2)
            pygame.draw.line(screen, SILVER, (dagger_x, self.y + 25), (dagger_x + 8, self.y + 30), 2)
        
        # Double jump indicator
        if not self.on_ground and self.can_double_jump and not self.double_jumped:
            # Draw wings to indicate double jump is available
            wing_color = NEON_BLUE if self.player_class == "mage" else self.aura_color
            wing_alpha = 150 + int(50 * math.sin(self.animation_frame * 0.3))
            
            # Create wing surface with alpha
            wing_surface = pygame.Surface((30, 15))
            wing_surface.set_alpha(wing_alpha)
            wing_surface.fill(wing_color)
            
            # Draw left wing
            pygame.draw.ellipse(wing_surface, wing_color, (0, 0, 15, 15))
            screen.blit(wing_surface, (self.x - 15, self.y + 15))
            
            # Draw right wing
            pygame.draw.ellipse(wing_surface, wing_color, (0, 0, 15, 15))
            screen.blit(wing_surface, (self.x + self.width, self.y + 15))
        
        # Attack animation
        if self.is_attacking and self.attack_animation > 0:
            # Draw attack area
            attack_alpha = int(255 * (self.attack_animation / 15))
            attack_surface = pygame.Surface((self.attack_range, self.height))
            attack_surface.set_alpha(attack_alpha // 3)
            
            if self.facing_right:
                attack_color = RED
                pygame.draw.rect(attack_surface, attack_color, (0, 0, self.attack_range, self.height))
                screen.blit(attack_surface, (self.x + self.width, self.y))
                
                # Draw slash effect
                slash_length = self.attack_range * 0.8
                start_pos = (self.x + self.width, self.y + self.height // 2)
                end_pos = (self.x + self.width + slash_length, self.y + self.height // 2)
                pygame.draw.line(screen, WHITE, start_pos, end_pos, 4)
            else:
                attack_color = RED
                pygame.draw.rect(attack_surface, attack_color, (0, 0, self.attack_range, self.height))
                screen.blit(attack_surface, (self.x - self.attack_range, self.y))
                
                # Draw slash effect
                slash_length = self.attack_range * 0.8
                start_pos = (self.x, self.y + self.height // 2)
                end_pos = (self.x - slash_length, self.y + self.height // 2)
                pygame.draw.line(screen, WHITE, start_pos, end_pos, 4)

class Enemy:
    def __init__(self, x, y, enemy_type="goblin"):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.enemy_type = enemy_type
        self.health = 90  # Increased from 50
        self.max_health = 90  # Increased from 50
        self.speed = 3  # Increased from 2
        self.damage = 25  # Increased from 15
        self.element = Element.NEUTRAL
        self.ai_state = "patrol"
        self.target = None
        self.detection_range = 200  # Increased from 150
        self.attack_range = 60  # Increased from 50
        self.attack_cooldown = 0
        self.patrol_center = x
        self.patrol_range = 100
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.animation_frame = 0
        self.experience_value = 25
        self.gold_value = 10
        
        # Setup based on type
        self.setup_enemy_type()
    
    def setup_enemy_type(self):
        """Configure enemy based on type"""
        if self.enemy_type == "fire_elemental":
            self.health = 150  # Increased from 80
            self.max_health = 150
            self.damage = 40  # Increased from 25
            self.element = Element.FIRE
            self.color = FIRE_RED
            self.experience_value = 50
            self.gold_value = 25
            
        elif self.enemy_type == "ice_golem":
            self.health = 200  # Increased from 120
            self.max_health = 200
            self.damage = 50  # Increased from 30
            self.speed = 2  # Increased from 1
            self.element = Element.ICE
            self.color = ICE_BLUE
            self.width = 40
            self.height = 50
            self.experience_value = 75
            self.gold_value = 40
            
        elif self.enemy_type == "lightning_sprite":
            self.health = 80  # Increased from 40
            self.max_health = 80
            self.damage = 35  # Increased from 20
            self.speed = 7  # Increased from 5
            self.element = Element.LIGHTNING
            self.color = LIGHTNING_YELLOW
            self.width = 25
            self.height = 30
            self.experience_value = 40
            self.gold_value = 20
            
        elif self.enemy_type == "shadow_assassin":
            self.health = 120  # Increased from 60
            self.max_health = 120
            self.damage = 60  # Increased from 35
            self.speed = 6  # Increased from 4
            self.element = Element.SHADOW
            self.color = SHADOW_PURPLE
            self.experience_value = 60
            self.gold_value = 30
            
        elif self.enemy_type == "nature_guardian":
            self.health = 250  # Increased from 100
            self.max_health = 250
            self.damage = 45  # Increased from 20
            self.speed = 3  # Increased from 2
            self.element = Element.NATURE
            self.color = FOREST_GREEN
            self.width = 35
            self.height = 45
            self.experience_value = 65
            self.gold_value = 35
            
        elif self.enemy_type == "boss_demon":
            self.health = 500  # Massive boss health
            self.max_health = 500
            self.damage = 80   # Devastating damage
            self.speed = 2     # Slow but deadly
            self.element = Element.SHADOW
            self.color = DARK_RED
            self.width = 60    # Larger boss
            self.height = 80
            self.experience_value = 300
            self.gold_value = 200
            self.detection_range = 300  # Sees very far
            self.attack_range = 100     # Long reach
            
        else:  # goblin
            self.color = GREEN
    
    def update(self, player, platforms):
        # AI State Machine
        player_distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        
        if player_distance <= self.detection_range:
            if player_distance <= self.attack_range:
                self.ai_state = "attack"
            else:
                self.ai_state = "chase"
        else:
            self.ai_state = "patrol"
        
        # AI Behavior
        if self.ai_state == "patrol":
            # Patrol around spawn point
            if abs(self.x - self.patrol_center) > self.patrol_range:
                if self.x > self.patrol_center:
                    self.vel_x = -self.speed * 0.5
                    self.facing_right = False
                else:
                    self.vel_x = self.speed * 0.5
                    self.facing_right = True
            else:
                if random.random() < 0.02:
                    self.vel_x = random.uniform(-self.speed * 0.5, self.speed * 0.5)
                    self.facing_right = self.vel_x > 0
        
        elif self.ai_state == "chase":
            # Chase player
            if self.x < player.x:
                self.vel_x = min(self.vel_x + 0.5, self.speed)
                self.facing_right = True
            elif self.x > player.x:
                self.vel_x = max(self.vel_x - 0.5, -self.speed)
                self.facing_right = False
        
        elif self.ai_state == "attack":
            # Attack player
            if self.attack_cooldown <= 0:
                if player.take_damage(self.damage):
                    pass  # Player died
                self.attack_cooldown = 120
                return self.create_attack_effects()
        
        # Apply gravity
        self.vel_y += 0.8
        if self.vel_y > 15:
            self.vel_y = 15
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Platform collision
        self.on_ground = False
        for platform in platforms:
            if (self.x < platform.x + platform.width and
                self.x + self.width > platform.x and
                self.y < platform.y + platform.height and
                self.y + self.height > platform.y):
                
                if self.vel_y > 0 and self.y < platform.y:
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    self.on_ground = True
        
        # Screen boundaries
        if self.x < 0 or self.x > WINDOW_WIDTH - self.width:
            self.vel_x *= -1
            self.facing_right = not self.facing_right
        
        if self.y > WINDOW_HEIGHT:
            self.y = 100
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        self.animation_frame += 1
        return []
    
    def create_attack_effects(self):
        """Create attack effect particles based on element"""
        effects = []
        
        if self.element == Element.FIRE:
            colors = FIRE_COLORS
        elif self.element == Element.ICE:
            colors = ICE_COLORS
        elif self.element == Element.LIGHTNING:
            colors = LIGHTNING_COLORS
        elif self.element == Element.NATURE:
            colors = NATURE_COLORS
        elif self.element == Element.SHADOW:
            colors = SHADOW_COLORS
        else:
            colors = [WHITE, SILVER]
        
        for _ in range(10):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            color = random.choice(colors)
            effects.append(Particle(
                self.x + self.width//2, self.y + self.height//2,
                vx, vy, color, random.randint(2, 5), 30, 0.1
            ))
        
        return effects
    
    def take_damage(self, damage, element=Element.NEUTRAL):
        """Take damage with elemental considerations"""
        actual_damage = damage
        
        # Elemental weaknesses and resistances
        if element == Element.FIRE and self.element == Element.ICE:
            actual_damage *= 1.5  # Fire vs Ice
        elif element == Element.ICE and self.element == Element.FIRE:
            actual_damage *= 1.5  # Ice vs Fire
        elif element == Element.LIGHTNING and self.element == Element.NATURE:
            actual_damage *= 1.5  # Lightning vs Nature
        elif element == self.element:
            actual_damage *= 0.5  # Same element resistance
        
        self.health -= int(actual_damage)
        return self.health <= 0
    
    def draw(self, screen):
        # Draw enemy with elemental effects
        base_color = self.color
        
        # Elemental aura
        if self.element != Element.NEUTRAL:
            aura_intensity = 30 + math.sin(self.animation_frame * 0.15) * 15
            aura_surface = pygame.Surface((self.width + 15, self.height + 15))
            aura_surface.set_alpha(int(aura_intensity))
            
            if self.element == Element.FIRE:
                aura_color = random.choice(FIRE_COLORS)
            elif self.element == Element.ICE:
                aura_color = random.choice(ICE_COLORS)
            elif self.element == Element.LIGHTNING:
                aura_color = random.choice(LIGHTNING_COLORS)
            elif self.element == Element.NATURE:
                aura_color = random.choice(NATURE_COLORS)
            elif self.element == Element.SHADOW:
                aura_color = random.choice(SHADOW_COLORS)
            else:
                aura_color = WHITE
            
            pygame.draw.ellipse(aura_surface, aura_color, (0, 0, self.width + 15, self.height + 15))
            screen.blit(aura_surface, (self.x - 7, self.y - 7))
        
        # Draw enemy body
        pygame.draw.rect(screen, base_color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
        
        # Health bar
        if self.health < self.max_health:
            bar_width = self.width
            bar_height = 4
            pygame.draw.rect(screen, RED, (self.x, self.y - 8, bar_width, bar_height))
            health_width = int(bar_width * (self.health / self.max_health))
            pygame.draw.rect(screen, GREEN, (self.x, self.y - 8, health_width, bar_height))

class Platform:
    def __init__(self, x, y, width, height, platform_type="stone"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.platform_type = platform_type
        
        if platform_type == "stone":
            self.color = GRAY
        elif platform_type == "wood":
            self.color = BRONZE
        elif platform_type == "metal":
            self.color = SILVER
        elif platform_type == "crystal":
            self.color = NEON_PURPLE
        elif platform_type == "lava":
            self.color = LAVA_ORANGE
        elif platform_type == "ice":
            self.color = ICE_BLUE
        else:
            self.color = GRAY
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)

class Collectible:
    def __init__(self, x, y, item_type="coin"):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.item_type = item_type
        self.animation_frame = 0
        self.collected = False
        
        if item_type == "coin":
            self.color = GOLD
            self.value = 10
        elif item_type == "gem":
            self.color = NEON_PURPLE
            self.value = 50
        elif item_type == "health_potion":
            self.color = RED
            self.value = 50
        elif item_type == "experience_orb":
            self.color = NEON_GREEN
            self.value = 100
        elif item_type == "skill_tome":
            self.color = COSMIC_VIOLET
            self.value = 1
        else:
            self.color = WHITE
    
    def update(self, player):
        if self.collected:
            return False
        
        # Check collection
        collision = (self.x < player.x + player.width and
                    self.x + self.width > player.x and
                    self.y < player.y + player.height and
                    self.y + self.height > player.y)
        
        if collision:
            self.collected = True
            
            if self.item_type == "coin":
                player.gold += self.value
            elif self.item_type == "gem":
                player.gold += self.value
            elif self.item_type == "health_potion":
                player.health = min(player.max_health, player.health + self.value)
            elif self.item_type == "experience_orb":
                player.add_experience(self.value)
            elif self.item_type == "skill_tome":
                player.skill_points += self.value
            
            return True
        
        self.animation_frame += 1
        return False
    
    def draw(self, screen):
        if not self.collected:
            y_offset = math.sin(self.animation_frame * 0.1) * 5
            
            # Glow effect
            glow_size = 30 + math.sin(self.animation_frame * 0.2) * 8
            glow_surface = pygame.Surface((glow_size, glow_size))
            glow_surface.set_alpha(100)
            pygame.draw.circle(glow_surface, self.color, (glow_size//2, glow_size//2), glow_size//2)
            screen.blit(glow_surface, (self.x - glow_size//2 + self.width//2, 
                                     self.y - glow_size//2 + self.height//2 + y_offset))
            
            # Item
            if self.item_type == "skill_tome":
                # Book shape
                pygame.draw.rect(screen, self.color, (self.x, self.y + y_offset, self.width, self.height))
                pygame.draw.rect(screen, WHITE, (self.x + 2, self.y + 2 + y_offset, self.width - 4, self.height - 4))
            else:
                pygame.draw.circle(screen, self.color, 
                                 (int(self.x + self.width//2), int(self.y + self.height//2 + y_offset)), 
                                 self.width//2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("ULTIMATE FANTASY ADVENTURE - The Greatest Game Ever!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        self.huge_font = pygame.font.Font(None, 72)
        
        # Game state
        self.running = True
        self.game_state = "class_selection"  # class_selection, playing, paused, game_over, victory
        self.selected_class = 0
        self.class_names = ["Mage", "Warrior", "Archer", "Assassin"]
        self.class_descriptions = [
            "Master of elemental power with enhanced magical abilities",
            "Mighty fighter with incredible strength and defense", 
            "Swift ranged attacker with nature abilities",
            "Stealthy assassin with shadow powers and critical strikes"
        ]
        
        # Game objects
        self.player = None
        self.enemies = []
        self.platforms = []
        self.collectibles = []
        self.particles = []
        self.floating_texts = []
        
        # Level progression
        self.current_level = 1
        self.max_level = 10
        self.level_complete = False
        
        # Timers
        self.enemy_spawn_timer = 0
        self.collectible_spawn_timer = 0
        
        # Camera
        self.camera_x = 0
        self.camera_y = 0
        self.screen_shake = 0
        self.screen_shake_intensity = 0
        
        # Background
        self.background_stars = []
        for _ in range(200):
            self.background_stars.append({
                'x': random.randint(0, WINDOW_WIDTH),
                'y': random.randint(0, WINDOW_HEIGHT),
                'size': random.randint(1, 4),
                'color': random.choice([WHITE, NEON_BLUE, NEON_PURPLE, GOLD]),
                'twinkle': random.randint(0, 100)
            })
    
    def add_screen_shake(self, intensity, duration):
        """Add screen shake effect"""
        self.screen_shake = duration
        self.screen_shake_intensity = intensity
    
    def create_level(self, level_num):
        """Create level geometry and enemies"""
        self.platforms.clear()
        self.enemies.clear()
        self.collectibles.clear()
        
        # Ground
        self.platforms.append(Platform(0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, 50, "stone"))
        
        if level_num == 1:
            # Tutorial level
            self.platforms.extend([
                Platform(200, 800, 200, 20, "wood"),
                Platform(500, 700, 150, 20, "stone"),
                Platform(800, 600, 200, 20, "wood"),
                Platform(1100, 500, 150, 20, "stone"),
                Platform(300, 400, 100, 20, "crystal"),
                Platform(700, 300, 150, 20, "metal"),
            ])
            
            # Basic enemies
            self.enemies.extend([
                Enemy(300, 750, "goblin"),
                Enemy(600, 650, "goblin"),
                Enemy(900, 550, "fire_elemental"),
                Enemy(1200, 450, "goblin"),
            ])
            
            # Collectibles
            self.collectibles.extend([
                Collectible(250, 780, "coin"),
                Collectible(550, 680, "health_potion"),
                Collectible(850, 580, "health_potion"),
                Collectible(350, 380, "experience_orb"),
                Collectible(750, 280, "skill_tome"),
            ])
        
        elif level_num >= 2:
            # Procedural level generation - INCREASED DIFFICULTY
            platform_count = 8 + level_num * 2
            enemy_count = 6 + level_num * 2  # Increased from 3 + level_num
            collectible_count = 3 + level_num  # Reduced from 5 + level_num
            
            # Generate platforms
            for i in range(platform_count):
                x = random.randint(100, WINDOW_WIDTH - 200)
                y = random.randint(200, WINDOW_HEIGHT - 100)
                width = random.randint(100, 300)
                height = random.randint(15, 30)
                
                platform_types = ["stone", "wood", "metal", "crystal"]
                if level_num >= 5:
                    platform_types.extend(["lava", "ice"])
                
                platform_type = random.choice(platform_types)
                self.platforms.append(Platform(x, y, width, height, platform_type))
            
            # Generate enemies - INCREASED DIFFICULTY
            enemy_types = ["goblin", "fire_elemental", "ice_golem"]
            if level_num >= 3:
                enemy_types.extend(["lightning_sprite", "shadow_assassin"])
            if level_num >= 5:
                enemy_types.append("nature_guardian")
            if level_num >= 7:  # Add bosses on high levels
                enemy_types.append("boss_demon")
            
            for i in range(enemy_count):
                if self.platforms:
                    platform = random.choice(self.platforms[1:])  # Skip ground
                    enemy_x = platform.x + random.randint(0, max(1, platform.width - 50))
                    enemy_y = platform.y - 50
                    enemy_type = random.choice(enemy_types)
                    
                    # Force spawn a boss every 3 levels after level 6
                    if level_num >= 7 and level_num % 3 == 0 and i == 0:
                        enemy_type = "boss_demon"
                    
                    self.enemies.append(Enemy(enemy_x, enemy_y, enemy_type))
            
            # Generate collectibles
            collectible_types = ["coin", "gem", "health_potion", "experience_orb"]
            if level_num >= 3:
                collectible_types.append("skill_tome")
            
            for i in range(collectible_count):
                if self.platforms:
                    platform = random.choice(self.platforms[1:])
                    collectible_x = platform.x + random.randint(20, max(21, platform.width - 20))
                    collectible_y = platform.y - 25
                    collectible_type = random.choice(collectible_types)
                    self.collectibles.append(Collectible(collectible_x, collectible_y, collectible_type))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "class_selection":
                    if event.key == pygame.K_UP:
                        self.selected_class = (self.selected_class - 1) % len(self.class_names)
                    elif event.key == pygame.K_DOWN:
                        self.selected_class = (self.selected_class + 1) % len(self.class_names)
                    elif event.key == pygame.K_RETURN:
                        self.start_game()
                
                elif self.game_state == "playing":
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "paused"
                    elif event.key == pygame.K_SPACE:
                        # Handle attack
                        particles = self.player.attack(self.enemies)
                        if particles:
                            self.particles.extend(particles)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        # Handle jumping with double jump
                        if self.player.jump():
                            # Add particles if it was a double jump
                            if self.player.double_jumped:
                                particles = self.player.create_jump_particles()
                                self.particles.extend(particles)
                
                elif self.game_state == "paused":
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "playing"
                
                elif self.game_state in ["game_over", "victory"]:
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_q:
                        self.running = False
    
    def start_game(self):
        """Initialize game with selected class"""
        class_name = self.class_names[self.selected_class].lower()
        self.player = Player(100, 400, class_name)
        self.game_state = "playing"
        self.current_level = 1
        self.create_level(self.current_level)
    
    def restart_game(self):
        """Restart the game"""
        self.game_state = "class_selection"
        self.selected_class = 0
        self.current_level = 1
        self.level_complete = False
        self.player = None
        self.enemies.clear()
        self.platforms.clear()
        self.collectibles.clear()
        self.particles.clear()
    
    def update(self):
        if self.game_state != "playing":
            return
        
        # Update screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1
        
        # Update player
        self.player.update(self.platforms)
        
        # Update particles
        for particle in self.particles[:]:
            if not particle.update():
                self.particles.remove(particle)
        
        # Update floating texts
        for text in self.floating_texts[:]:
            if not text.update():
                self.floating_texts.remove(text)
        
        # Update enemies
        for enemy in self.enemies[:]:
            effects = enemy.update(self.player, self.platforms)
            if effects:
                self.particles.extend(effects)
            
            if enemy.health <= 0:
                # Enemy died
                self.player.add_experience(enemy.experience_value)
                self.player.gold += enemy.gold_value
                
                # Large health gain for killing enemy
                health_gain = 70  # Increased health gain
                self.player.health = min(self.player.max_health, self.player.health + health_gain)
                
                # Add floating text for health gain
                health_text = FloatingText(
                    self.player.x + self.player.width//2 - 15,
                    self.player.y - 20,
                    f"+{health_gain} HP",
                    NEON_GREEN,
                    30
                )
                self.floating_texts.append(health_text)
                
                # Death effects
                death_effects = []
                for _ in range(20):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(3, 10)
                    vx = math.cos(angle) * speed
                    vy = math.sin(angle) * speed
                    color = enemy.color
                    death_effects.append(Particle(
                        enemy.x + enemy.width//2, enemy.y + enemy.height//2,
                        vx, vy, color, random.randint(3, 8), 40, 0.2
                    ))
                self.particles.extend(death_effects)
                
                self.enemies.remove(enemy)
        
        # Update collectibles
        for collectible in self.collectibles[:]:
            if collectible.update(self.player):
                # Collection effects
                collection_effects = []
                for _ in range(15):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(2, 6)
                    vx = math.cos(angle) * speed
                    vy = math.sin(angle) * speed
                    collection_effects.append(Particle(
                        collectible.x + collectible.width//2, collectible.y + collectible.height//2,
                        vx, vy, collectible.color, random.randint(2, 5), 30, 0
                    ))
                self.particles.extend(collection_effects)
                self.collectibles.remove(collectible)
        
        # Level progression
        if len(self.enemies) == 0 and not self.level_complete:
            if self.current_level >= self.max_level:
                self.game_state = "victory"
            else:
                self.current_level += 1
                self.create_level(self.current_level)
                
                # Small health bonus for completing level (REDUCED for difficulty)
                level_health_bonus = 10  # Reduced from 20
                self.player.health = min(self.player.health + level_health_bonus, self.player.max_health)
                
                # Add floating text for level completion bonus
                level_text = FloatingText(
                    self.player.x + self.player.width//2 - 30,
                    self.player.y - 30,
                    f"Level Complete! +{level_health_bonus} HP",
                    GOLD,
                    32
                )
                self.floating_texts.append(level_text)
                
                # Create level completion visual effect
                for _ in range(30):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(3, 8)
                    vx = math.cos(angle) * speed
                    vy = math.sin(angle) * speed
                    color = random.choice([GOLD, NEON_GREEN, CYAN])
                    completion_particle = Particle(
                        self.player.x + self.player.width//2,
                        self.player.y + self.player.height//2,
                        vx, vy, color, random.randint(4, 8), 50, 0
                    )
                    self.particles.append(completion_particle)
        
        # Game over check
        if self.player.health <= 0:
            self.game_state = "game_over"
        
        # Update background
        for star in self.background_stars:
            star['twinkle'] = (star['twinkle'] + 1) % 200
    
    def draw_background(self):
        """Draw animated background"""
        # Gradient background
        for y in range(0, WINDOW_HEIGHT, 5):
            color_ratio = y / WINDOW_HEIGHT
            r = int(25 * (1 - color_ratio) + 10 * color_ratio)
            g = int(25 * (1 - color_ratio) + 0 * color_ratio)
            b = int( 112 * (1 - color_ratio) + 50 * color_ratio)
            pygame.draw.rect(self.screen, (r, g, b), (0, y, WINDOW_WIDTH, 5))
        
        # Twinkling stars
        for star in self.background_stars:
            if star['twinkle'] < 150:
                alpha = 100 + (star['twinkle'] % 50) * 2
                star_surface = pygame.Surface((star['size'] * 2, star['size'] * 2))
                star_surface.set_alpha(alpha)
                pygame.draw.circle(star_surface, star['color'], (star['size'], star['size']), star['size'])
                self.screen.blit(star_surface, (star['x'] - star['size'], star['y'] - star['size']))
    
    def draw_ui(self):
        """Draw game UI"""
        if self.game_state == "playing":
            # Player stats
            # Health bar
            health_width = 300
            health_height = 25
            pygame.draw.rect(self.screen, DARK_RED, (20, 20, health_width, health_height))
            health_fill = int(health_width * (self.player.health / self.player.max_health))
            pygame.draw.rect(self.screen, RED, (20, 20, health_fill, health_height))
            pygame.draw.rect(self.screen, WHITE, (20, 20, health_width, health_height), 2)
            
            health_text = self.font.render(f"Health: {self.player.health}/{self.player.max_health}", True, WHITE)
            self.screen.blit(health_text, (330, 25))
            
            # Experience bar
            exp_width = 200
            exp_height = 15
            pygame.draw.rect(self.screen, DARK_GREEN, (20, 55, exp_width, exp_height))
            exp_fill = int(exp_width * (self.player.experience / self.player.experience_to_next))
            pygame.draw.rect(self.screen, NEON_GREEN, (20, 55, exp_fill, exp_height))
            pygame.draw.rect(self.screen, WHITE, (20, 55, exp_width, exp_height), 2)
            
            exp_text = self.small_font.render(f"EXP: {self.player.experience}/{self.player.experience_to_next}", True, WHITE)
            self.screen.blit(exp_text, (230, 57))
            
            # Player info
            level_text = self.font.render(f"Level: {self.player.level}", True, GOLD)
            class_text = self.font.render(f"Class: {self.player.player_class.title()}", True, self.player.aura_color)
            gold_text = self.font.render(f"Gold: {self.player.gold}", True, GOLD)
            skill_text = self.font.render(f"Skill Points: {self.player.skill_points}", True, NEON_PURPLE)
            
            self.screen.blit(level_text, (20, 90))
            self.screen.blit(class_text, (150, 90))
            self.screen.blit(gold_text, (20, 120))
            self.screen.blit(skill_text, (20, 150))
            
            # Level info
            level_info_text = self.large_font.render(f"Level {self.current_level}/{self.max_level}", True, WHITE)
            enemies_text = self.font.render(f"Enemies: {len(self.enemies)}", True, RED)
            
            self.screen.blit(level_info_text, (WINDOW_WIDTH - 300, 20))
            self.screen.blit(enemies_text, (WINDOW_WIDTH - 200, 60))
            
            # Attack cooldown indicator
            attack_y = 190
            attack_title = self.font.render("Attack:", True, WHITE)
            self.screen.blit(attack_title, (20, attack_y))
            
            if self.player.attack_cooldown > 0:
                attack_text = f"Space: Attack - {(self.player.attack_cooldown // 60) + 1}s"
                attack_color = GRAY
            else:
                attack_text = "Space: Attack - Ready!"
                attack_color = NEON_GREEN
            
            attack_render = self.small_font.render(attack_text, True, attack_color)
            self.screen.blit(attack_render, (20, attack_y + 25))
            
            # Controls
            controls_y = WINDOW_HEIGHT - 100
            controls = [
                "AD: Move | W/Up: Jump | Space: Attack | ESC: Pause"
            ]
            
            for i, control in enumerate(controls):
                control_text = self.small_font.render(control, True, WHITE)
                self.screen.blit(control_text, (20, controls_y + i * 25))
    
    def draw_class_selection(self):
        """Draw class selection screen"""
        # Title
        title_text = self.huge_font.render("ULTIMATE FANTASY ADVENTURE", True, GOLD)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, 100))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.large_font.render("Choose Your Class", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH//2, 180))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Class options
        for i, (class_name, description) in enumerate(zip(self.class_names, self.class_descriptions)):
            y = 300 + i * 120
            
            if i == self.selected_class:
                # Highlight selected class
                highlight_rect = pygame.Rect(100, y - 20, WINDOW_WIDTH - 200, 100)
                pygame.draw.rect(self.screen, NEON_BLUE, highlight_rect, 3)
                
                # Class preview
                preview_colors = [NEON_PURPLE, NEON_ORANGE, NEON_GREEN, SHADOW_PURPLE]
                preview_color = preview_colors[i]
                
                pygame.draw.rect(self.screen, preview_color, (150, y + 10, 40, 50))
                pygame.draw.rect(self.screen, WHITE, (150, y + 10, 40, 50), 2)
            
            class_text = self.large_font.render(class_name, True, GOLD if i == self.selected_class else WHITE)
            desc_text = self.font.render(description, True, WHITE)
            
            self.screen.blit(class_text, (220, y))
            self.screen.blit(desc_text, (220, y + 40))
        
        # Instructions
        instruction_text = self.font.render("Use UP/DOWN arrows to select, ENTER to confirm", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 50))
        self.screen.blit(instruction_text, instruction_rect)
    
    def draw_overlays(self):
        """Draw game state overlays"""
        if self.game_state == "paused":
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            pause_text = self.huge_font.render("PAUSED", True, WHITE)
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(pause_text, text_rect)
        
        elif self.game_state == "game_over":
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(DARK_RED)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.huge_font.render("GAME OVER", True, RED)
            final_level_text = self.large_font.render(f"Reached Level: {self.current_level}", True, WHITE)
            final_stats_text = self.font.render(f"Player Level: {self.player.level} | Gold: {self.player.gold}", True, GOLD)
            restart_text = self.font.render("Press R to restart or Q to quit", True, WHITE)
            
            texts = [game_over_text, final_level_text, final_stats_text, restart_text]
            for i, text in enumerate(texts):
                text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100 + i * 60))
                self.screen.blit(text, text_rect)
        
        elif self.game_state == "victory":
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(DARK_GREEN)
            self.screen.blit(overlay, (0, 0))
            
            victory_text = self.huge_font.render("VICTORY!", True, GOLD)
            complete_text = self.large_font.render("All Levels Completed!", True, NEON_GREEN)
            final_stats_text = self.font.render(f"Final Level: {self.player.level} | Gold: {self.player.gold}", True, GOLD)
            restart_text = self.font.render("Press R to play again or Q to quit", True, WHITE)
            
            texts = [victory_text, complete_text, final_stats_text, restart_text]
            for i, text in enumerate(texts):
                text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100 + i * 60))
                self.screen.blit(text, text_rect)
    
    def draw(self):
        # Draw background
        self.draw_background()
        
        if self.game_state == "class_selection":
            self.draw_class_selection()
        
        else:
            # Draw platforms
            for platform in self.platforms:
                platform.draw(self.screen)
            
            # Draw collectibles
            for collectible in self.collectibles:
                collectible.draw(self.screen)
            
            # Draw particles
            for particle in self.particles:
                particle.draw(self.screen)
            
            # Draw floating texts
            for text in self.floating_texts:
                text.draw(self.screen)
            
            # Draw enemies
            for enemy in self.enemies:
                enemy.draw(self.screen)
            
            # Draw player
            if self.player:
                self.player.draw(self.screen)
            
            # Draw UI
            self.draw_ui()
            
            # Draw overlays
            self.draw_overlays()
        
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
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
