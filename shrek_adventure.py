import pygame
import random
import math
import sys

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 69, 19)
BLUE = (30, 144, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_BLUE = (173, 216, 230)
SWAMP_GREEN = (107, 142, 35)
GOLD = (255, 215, 0)
NEON_GREEN = (57, 255, 20)
RAINBOW = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]

class Particle:
    def __init__(self, x, y, color, vx=0, vy=0, life=60):
        self.x = x
        self.y = y
        self.vx = vx + random.uniform(-3, 3)
        self.vy = vy + random.uniform(-4, 2)
        self.color = color
        self.life = life
        self.max_life = life
        self.size = random.uniform(2, 6)
        self.gravity = 0.2
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.vx *= 0.98
        self.life -= 1
    
    def draw(self, screen):
        if self.life > 0:
            alpha = self.life / self.max_life
            size = max(1, int(self.size * alpha))
            color = (*self.color, int(255 * alpha))
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

class Shrek:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = 15
        self.on_ground = False
        self.health = 100
        self.max_health = 100
        self.facing_right = True
        self.animation_frame = 0
        self.roar_cooldown = 0
        self.invulnerable = 0
        
        # Shrek abilities
        self.onions = 3
        self.mud_balls = 5
        
        # CHEAT/HACK FEATURES
        self.god_mode = False
        self.super_speed = False
        self.infinite_ammo = False
        self.rainbow_mode = False
        self.giant_mode = False
        self.noclip = False
        self.auto_heal = False
        self.super_jump = False
        self.rapid_fire = False
        
        # Cheat counters
        self.cheat_timer = 0
        self.rainbow_frame = 0
        
    def update(self, platforms):
        # Handle input
        keys = pygame.key.get_pressed()
        
        # CHEAT FEATURES
        current_speed = self.speed * 3 if self.super_speed else self.speed
        current_jump = self.jump_power * 2 if self.super_jump else self.jump_power
        
        # Auto-heal cheat
        if self.auto_heal and self.cheat_timer % 60 == 0:
            self.health = min(self.max_health, self.health + 1)
        
        # Rainbow mode frame counter
        if self.rainbow_mode:
            self.rainbow_frame += 1
        
        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -current_speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = current_speed
            self.facing_right = True
        else:
            self.vel_x *= 0.8  # Friction
        
        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = -current_jump
            self.on_ground = False
        
        # Flying with noclip
        if self.noclip:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.vel_y = -current_speed
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.vel_y = current_speed
            else:
                self.vel_y *= 0.8
        else:
            # Apply gravity
            self.vel_y += 0.8
            if self.vel_y > 15:
                self.vel_y = 15
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Platform collision (skip if noclip)
        if not self.noclip:
            self.on_ground = False
            for platform in platforms:
                if (self.x < platform.x + platform.width and
                    self.x + self.width > platform.x and
                    self.y < platform.y + platform.height and
                    self.y + self.height > platform.y):
                    
                    # Landing on top
                    if self.vel_y > 0 and self.y < platform.y:
                        self.y = platform.y - self.height
                        self.vel_y = 0
                        self.on_ground = True
                    # Hitting from below
                    elif self.vel_y < 0 and self.y > platform.y:
                        self.y = platform.y + platform.height
                        self.vel_y = 0
                    # Side collision
                    else:
                        if self.vel_x > 0:
                            self.x = platform.x - self.width
                        else:
                            self.x = platform.x + platform.width
                        self.vel_x = 0
        
        # Screen boundaries
        if self.x < 0:
            self.x = 0
        elif self.x > WINDOW_WIDTH - self.width:
            self.x = WINDOW_WIDTH - self.width
        
        if self.y > WINDOW_HEIGHT and not self.noclip:
            if not self.god_mode:
                self.health -= 20
            self.y = 100
            self.x = 100
        
        # Update counters
        self.animation_frame += 1
        self.cheat_timer += 1
        if self.roar_cooldown > 0:
            self.roar_cooldown -= 1
        if self.invulnerable > 0:
            self.invulnerable -= 1
    
    def take_damage(self, damage):
        if self.god_mode:
            return False  # No damage in god mode
        if self.invulnerable <= 0:
            self.health -= damage
            self.invulnerable = 60  # 1 second of invulnerability
            return True
        return False
    
    def roar(self, enemies):
        """Shrek's special roar attack"""
        roar_cooldown_time = 30 if self.rapid_fire else 180
        if self.roar_cooldown <= 0:
            self.roar_cooldown = roar_cooldown_time
            particles = []
            
            # Create roar particles
            particle_count = 40 if self.rapid_fire else 20
            for _ in range(particle_count):
                angle = random.uniform(-math.pi/4, math.pi/4)
                if not self.facing_right:
                    angle = math.pi - angle
                
                speed = random.uniform(8, 15)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
                
                # Rainbow particles in rainbow mode
                color = RAINBOW[self.rainbow_frame % len(RAINBOW)] if self.rainbow_mode else GREEN
                
                particles.append(Particle(
                    self.x + self.width//2, self.y + self.height//2,
                    color, vx, vy, 30
                ))
            
            # Damage nearby enemies
            roar_range = 250 if self.rapid_fire else 150
            roar_damage = 50 if self.rapid_fire else 30
            for enemy in enemies:
                dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
                if dist < roar_range:
                    enemy.take_damage(roar_damage)
            
            return particles
        return []
    
    def throw_mud(self, mouse_x, mouse_y):
        """Throw mud ball"""
        if self.mud_balls > 0 or self.infinite_ammo:
            if not self.infinite_ammo:
                self.mud_balls -= 1
            
            # Calculate direction
            dx = mouse_x - (self.x + self.width//2)
            dy = mouse_y - (self.y + self.height//2)
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist > 0:
                dx /= dist
                dy /= dist
            
            speed = 20 if self.rapid_fire else 12
            return MudBall(self.x + self.width//2, self.y + self.height//2, dx * speed, dy * speed, self.rainbow_mode)
        return None
    
    def draw(self, screen):
        # Shrek body (green ogre)
        base_color = GREEN
        
        # Cheat mode colors
        if self.rainbow_mode:
            base_color = RAINBOW[self.rainbow_frame // 10 % len(RAINBOW)]
        elif self.god_mode:
            base_color = NEON_GREEN
        
        color = base_color
        if self.invulnerable > 0 and self.invulnerable % 10 < 5:
            color = (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50))
        
        # Size modifiers for giant mode
        width_mod = self.width * 1.5 if self.giant_mode else self.width
        height_mod = self.height * 1.5 if self.giant_mode else self.height
        
        # Body
        pygame.draw.ellipse(screen, color, (self.x, self.y + 20, width_mod, height_mod - 20))
        
        # Head
        head_size = 30 if self.giant_mode else 20
        pygame.draw.circle(screen, color, (int(self.x + width_mod//2), int(self.y + 15)), head_size)
        
        # Eyes
        eye_offset = 5 if self.facing_right else -5
        eye_size = 6 if self.giant_mode else 4
        pupil_size = 3 if self.giant_mode else 2
        
        pygame.draw.circle(screen, WHITE, (int(self.x + width_mod//2 - 8 + eye_offset), int(self.y + 10)), eye_size)
        pygame.draw.circle(screen, WHITE, (int(self.x + width_mod//2 + 8 + eye_offset), int(self.y + 10)), eye_size)
        pygame.draw.circle(screen, BLACK, (int(self.x + width_mod//2 - 6 + eye_offset), int(self.y + 10)), pupil_size)
        pygame.draw.circle(screen, BLACK, (int(self.x + width_mod//2 + 6 + eye_offset), int(self.y + 10)), pupil_size)
        
        # Ears
        ear_size = 9 if self.giant_mode else 6
        pygame.draw.circle(screen, DARK_GREEN, (int(self.x + width_mod//2 - 15), int(self.y + 5)), ear_size)
        pygame.draw.circle(screen, DARK_GREEN, (int(self.x + width_mod//2 + 15), int(self.y + 5)), ear_size)
        
        # Arms
        if self.animation_frame % 40 < 20:
            arm_y = self.y + 25
        else:
            arm_y = self.y + 30
        
        arm_size = 12 if self.giant_mode else 8
        pygame.draw.circle(screen, color, (int(self.x - 5), int(arm_y)), arm_size)
        pygame.draw.circle(screen, color, (int(self.x + width_mod + 5), int(arm_y)), arm_size)
        
        # Legs
        leg_offset = 2 if self.animation_frame % 20 < 10 else -2
        leg_width = 12 if self.giant_mode else 8
        leg_height = 22 if self.giant_mode else 15
        
        pygame.draw.ellipse(screen, color, (self.x + 8 + leg_offset, self.y + height_mod - 10, leg_width, leg_height))
        pygame.draw.ellipse(screen, color, (self.x + width_mod - 16 - leg_offset, self.y + height_mod - 10, leg_width, leg_height))
        
        # Special effects
        if self.noclip:
            # Ghost effect
            overlay = pygame.Surface((width_mod, height_mod))
            overlay.set_alpha(100)
            overlay.fill(WHITE)
            screen.blit(overlay, (self.x, self.y))
        
        if self.super_speed:
            # Speed lines
            for i in range(5):
                line_x = self.x - i * 10
                pygame.draw.line(screen, YELLOW, (line_x, self.y + height_mod//2), 
                               (line_x - 15, self.y + height_mod//2), 2)
        
        # Health bar
        bar_width = 60
        bar_height = 6
        bar_x = self.x - 10
        bar_y = self.y - 15
        
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        health_width = int(bar_width * (self.health / self.max_health))
        health_color = NEON_GREEN if self.god_mode else GREEN
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))

class Enemy:
    def __init__(self, x, y, enemy_type="knight"):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.enemy_type = enemy_type
        self.health = 50
        self.max_health = 50
        self.speed = 1
        self.damage = 10
        self.attack_cooldown = 0
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.animation_frame = 0
        
        # Set properties based on type
        if enemy_type == "knight":
            self.color = GRAY
            self.health = 60
            self.speed = 1.5
            self.damage = 15
        elif enemy_type == "dragon":
            self.color = RED
            self.health = 120
            self.speed = 2
            self.damage = 25
            self.width = 50
            self.height = 50
        elif enemy_type == "fairy":
            self.color = PINK
            self.health = 30
            self.speed = 3
            self.damage = 8
            self.width = 20
            self.height = 25
        
        # NEW INFINITE LEVEL ENEMIES!
        elif enemy_type == "boss_knight":
            self.color = DARK_GRAY
            self.health = 150
            self.speed = 2
            self.damage = 30
            self.width = 60
            self.height = 70
        elif enemy_type == "mega_dragon":
            self.color = (200, 0, 0)  # Dark red
            self.health = 250
            self.speed = 2.5
            self.damage = 40
            self.width = 80
            self.height = 80
        elif enemy_type == "shadow_fairy":
            self.color = (50, 0, 100)  # Dark purple
            self.health = 80
            self.speed = 4
            self.damage = 20
            self.width = 25
            self.height = 30
        elif enemy_type == "giant_knight":
            self.color = (100, 100, 100)
            self.health = 400
            self.speed = 1
            self.damage = 60
            self.width = 100
            self.height = 120
        elif enemy_type == "shadow_boss":
            self.color = (20, 20, 20)
            self.health = 500
            self.speed = 3
            self.damage = 50
            self.width = 90
            self.height = 100
        elif enemy_type == "ice_dragon":
            self.color = (150, 200, 255)
            self.health = 300
            self.speed = 2
            self.damage = 35
            self.width = 70
            self.height = 70
        elif enemy_type == "fire_demon":
            self.color = (255, 100, 0)
            self.health = 350
            self.speed = 2.5
            self.damage = 45
            self.width = 75
            self.height = 85
        
        # PAHEMMAT VIHOLLISET! (WORSE ENEMIES!)
        elif enemy_type == "nightmare_lord":
            self.color = (0, 0, 0)  # Pure black
            self.health = 1000
            self.speed = 4
            self.damage = 100
            self.width = 120
            self.height = 150
        elif enemy_type == "chaos_beast":
            self.color = (255, 0, 255)  # Magenta
            self.health = 800
            self.speed = 5
            self.damage = 80
            self.width = 100
            self.height = 120
        elif enemy_type == "void_stalker":
            self.color = (30, 0, 50)  # Very dark purple
            self.health = 600
            self.speed = 6
            self.damage = 70
            self.width = 80
            self.height = 100
        elif enemy_type == "death_knight":
            self.color = (50, 0, 0)  # Dark red
            self.health = 1200
            self.speed = 3
            self.damage = 150
            self.width = 140
            self.height = 160
        elif enemy_type == "plague_dragon":
            self.color = (100, 150, 0)  # Sickly green
            self.health = 1500
            self.speed = 3.5
            self.damage = 120
            self.width = 160
            self.height = 140
        elif enemy_type == "soul_reaper":
            self.color = (200, 200, 200)  # Ghostly gray
            self.health = 500
            self.speed = 7
            self.damage = 90
            self.width = 70
            self.height = 90
        elif enemy_type == "demon_overlord":
            self.color = (150, 0, 0)  # Blood red
            self.health = 2000
            self.speed = 2
            self.damage = 200
            self.width = 200
            self.height = 220
        elif enemy_type == "shadow_titan":
            self.color = (10, 10, 10)  # Almost black
            self.health = 2500
            self.speed = 1.5
            self.damage = 250
            self.width = 250
            self.height = 280
        elif enemy_type == "cosmic_horror":
            self.color = (100, 0, 200)  # Dark purple
            self.health = 3000
            self.speed = 2.5
            self.damage = 300
            self.width = 300
            self.height = 320
        elif enemy_type == "apocalypse_bringer":
            self.color = (255, 50, 0)  # Bright red-orange
            self.health = 5000
            self.speed = 3
            self.damage = 500
            self.width = 400
            self.height = 450
        
        self.max_health = self.health
    
    def update(self, shrek, platforms):
        # AI: Move towards Shrek
        if self.x < shrek.x:
            self.vel_x = self.speed
            self.facing_right = True
        elif self.x > shrek.x:
            self.vel_x = -self.speed
            self.facing_right = False
        else:
            self.vel_x = 0
        
        # SPECIAL ABILITIES FOR PAHEMMAT VIHOLLISET!
        if self.enemy_type == "nightmare_lord":
            # Teleport occasionally
            if self.animation_frame % 200 == 0:
                self.x = shrek.x + random.randint(-100, 100)
                self.y = shrek.y + random.randint(-50, 50)
        
        elif self.enemy_type == "chaos_beast":
            # Chaotic movement
            if self.animation_frame % 60 == 0:
                self.vel_x = random.uniform(-self.speed * 2, self.speed * 2)
        
        elif self.enemy_type == "void_stalker":
            # Phase through platforms occasionally
            if self.animation_frame % 120 < 30:
                pass  # Skip platform collision during this phase
        
        elif self.enemy_type == "death_knight":
            # Charge attack
            if abs(self.x - shrek.x) > 200 and self.animation_frame % 180 == 0:
                charge_speed = 8 if self.x < shrek.x else -8
                self.vel_x = charge_speed
        
        elif self.enemy_type == "plague_dragon":
            # Poison clouds
            if self.animation_frame % 90 == 0:
                # Create poison effect near Shrek
                if abs(self.x - shrek.x) < 200:
                    if not shrek.god_mode:
                        shrek.take_damage(5)  # Poison damage
        
        elif self.enemy_type == "soul_reaper":
            # Super fast movement towards Shrek
            if abs(self.x - shrek.x) < 300:
                self.speed = 7
            else:
                self.speed = 3
        
        elif self.enemy_type in ["demon_overlord", "shadow_titan", "cosmic_horror", "apocalypse_bringer"]:
            # Ultimate bosses have multiple abilities
            if self.animation_frame % 120 == 0:
                # Area damage attack
                if abs(self.x - shrek.x) < 150 and abs(self.y - shrek.y) < 100:
                    if not shrek.god_mode:
                        shrek.take_damage(50)
            
            # Screen effects for apocalypse bringer
            if self.enemy_type == "apocalypse_bringer" and self.animation_frame % 300 == 0:
                # Massive area attack
                if abs(self.x - shrek.x) < 400:
                    if not shrek.god_mode:
                        shrek.take_damage(100)
        
        # Jump if Shrek is above
        if abs(self.x - shrek.x) < 100 and shrek.y < self.y - 50 and self.on_ground:
            jump_power = 20 if self.enemy_type in ["nightmare_lord", "soul_reaper"] else 12
            self.vel_y = -jump_power
            self.on_ground = False
        
        # Apply gravity (except for some flying enemies)
        if self.enemy_type not in ["void_stalker", "soul_reaper", "cosmic_horror"]:
            self.vel_y += 0.8
            if self.vel_y > 15:
                self.vel_y = 15
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Platform collision (skip for certain enemies during special phases)
        skip_collision = (self.enemy_type == "void_stalker" and self.animation_frame % 120 < 30)
        
        if not skip_collision:
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
            if self.enemy_type != "nightmare_lord":  # Nightmare lord can teleport
                self.vel_x *= -1
        
        if self.y > WINDOW_HEIGHT:
            if self.enemy_type == "nightmare_lord":
                # Teleport back up
                self.y = 100
                self.x = random.randint(100, WINDOW_WIDTH - 100)
            else:
                self.y = 100
        
        # Attack Shrek if close
        if self.attack_cooldown <= 0:
            dist = math.sqrt((self.x - shrek.x)**2 + (self.y - shrek.y)**2)
            attack_range = 100 if self.enemy_type in ["demon_overlord", "shadow_titan", "cosmic_horror", "apocalypse_bringer"] else 50
            
            if dist < attack_range:
                if shrek.take_damage(self.damage):
                    # Longer cooldown for more powerful enemies
                    base_cooldown = 120
                    if self.enemy_type in ["nightmare_lord", "death_knight", "plague_dragon"]:
                        base_cooldown = 150
                    elif self.enemy_type in ["demon_overlord", "shadow_titan"]:
                        base_cooldown = 180
                    elif self.enemy_type in ["cosmic_horror", "apocalypse_bringer"]:
                        base_cooldown = 200
                    
                    self.attack_cooldown = base_cooldown
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        self.animation_frame += 1
    
    def take_damage(self, damage):
        self.health -= damage
        particles = []
        
        if self.health <= 0:
            # Death particles
            for _ in range(15):
                particles.append(Particle(
                    self.x + self.width//2, self.y + self.height//2,
                    self.color, random.uniform(-5, 5), random.uniform(-8, 2), 60
                ))
        
        return particles
    
    def draw(self, screen):
        if self.health <= 0:
            return
        
        # Draw based on enemy type
        if self.enemy_type == "knight":
            # Knight body
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            # Helmet
            pygame.draw.circle(screen, self.color, (int(self.x + self.width//2), int(self.y + 10)), 12)
            # Sword
            sword_x = self.x + (self.width + 5) if self.facing_right else self.x - 10
            pygame.draw.rect(screen, GOLD, (sword_x, self.y + 5, 5, 20))
        
        elif self.enemy_type == "dragon":
            # Dragon body
            pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))
            # Wings
            wing_y = self.y + 10 + math.sin(self.animation_frame * 0.3) * 3
            pygame.draw.ellipse(screen, ORANGE, (self.x - 10, wing_y, 15, 25))
            pygame.draw.ellipse(screen, ORANGE, (self.x + self.width - 5, wing_y, 15, 25))
            # Head
            pygame.draw.circle(screen, self.color, (int(self.x + self.width//2), int(self.y + 10)), 15)
        
        elif self.enemy_type == "fairy":
            # Fairy body
            pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))
            # Wings
            wing_y = self.y + 5 + math.sin(self.animation_frame * 0.5) * 2
            pygame.draw.ellipse(screen, WHITE, (self.x - 5, wing_y, 8, 12))
            pygame.draw.ellipse(screen, WHITE, (self.x + self.width - 3, wing_y, 8, 12))
            # Wand
            wand_x = self.x + (self.width + 5) if self.facing_right else self.x - 8
            pygame.draw.line(screen, BROWN, (wand_x, self.y + 10), (wand_x, self.y + 25), 2)
            pygame.draw.circle(screen, YELLOW, (wand_x, self.y + 10), 3)
        
        # NEW BOSS ENEMIES
        elif self.enemy_type == "boss_knight":
            # Bigger armored knight
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.circle(screen, self.color, (int(self.x + self.width//2), int(self.y + 15)), 20)
            # Giant sword
            sword_x = self.x + (self.width + 8) if self.facing_right else self.x - 15
            pygame.draw.rect(screen, GOLD, (sword_x, self.y, 8, 40))
            # Spikes on armor
            for i in range(3):
                spike_y = self.y + 20 + i * 15
                pygame.draw.polygon(screen, WHITE, [(self.x + self.width//2 - 5, spike_y), 
                                                  (self.x + self.width//2 + 5, spike_y),
                                                  (self.x + self.width//2, spike_y - 10)])
        
        elif self.enemy_type == "mega_dragon":
            # Huge dragon
            pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))
            # Bigger wings
            wing_y = self.y + 15 + math.sin(self.animation_frame * 0.2) * 5
            pygame.draw.ellipse(screen, (255, 150, 0), (self.x - 20, wing_y, 25, 40))
            pygame.draw.ellipse(screen, (255, 150, 0), (self.x + self.width - 5, wing_y, 25, 40))
            # Massive head
            pygame.draw.circle(screen, self.color, (int(self.x + self.width//2), int(self.y + 15)), 25)
            # Fire breath effect
            if self.animation_frame % 60 < 20:
                fire_x = self.x + (self.width + 30) if self.facing_right else self.x - 30
                for i in range(5):
                    fire_color = (255, random.randint(100, 255), 0)
                    pygame.draw.circle(screen, fire_color, (fire_x + i * 10, self.y + 20), 8)
        
        elif self.enemy_type == "shadow_fairy":
            # Dark fairy with shadow trail
            pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))
            # Dark wings
            wing_y = self.y + 5 + math.sin(self.animation_frame * 0.7) * 3
            pygame.draw.ellipse(screen, (100, 0, 150), (self.x - 8, wing_y, 12, 18))
            pygame.draw.ellipse(screen, (100, 0, 150), (self.x + self.width - 4, wing_y, 12, 18))
            # Shadow trail
            for i in range(3):
                trail_x = self.x - i * 15
                trail_alpha = 100 - i * 30
                pygame.draw.circle(screen, (50, 0, 100), (trail_x, self.y + self.height//2), 8 - i * 2)
        
        elif self.enemy_type in ["giant_knight", "shadow_boss", "ice_dragon", "fire_demon"]:
            # Boss enemies - special effects
            pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))
            
            # Boss glow effect
            glow_color = self.color
            for i in range(3):
                glow_size = (self.width + i * 10, self.height + i * 10)
                glow_pos = (self.x - i * 5, self.y - i * 5)
                pygame.draw.ellipse(screen, (*glow_color, 50 - i * 15), (*glow_pos, *glow_size))
            
            # Boss crown/horns
            crown_x = self.x + self.width//2
            crown_y = self.y - 10
            pygame.draw.polygon(screen, GOLD, [(crown_x - 15, crown_y), (crown_x, crown_y - 20), (crown_x + 15, crown_y)])
            
            # Health indicator for bosses
            if self.health < self.max_health * 0.3:
                # Red danger glow when low health
                danger_glow = pygame.Surface((self.width + 20, self.height + 20))
                danger_glow.set_alpha(100)
                danger_glow.fill(RED)
                screen.blit(danger_glow, (self.x - 10, self.y - 10))
        
        # PAHEMMAT VIHOLLISET PIIRTÄMINEN!
        elif self.enemy_type == "nightmare_lord":
            # Nightmare Lord - constantly shifting darkness
            base_color = (self.animation_frame % 50, 0, 0)
            pygame.draw.ellipse(screen, base_color, (self.x, self.y, self.width, self.height))
            
            # Nightmare aura - expanding darkness
            for i in range(5):
                aura_size = (self.width + i * 30, self.height + i * 30)
                aura_pos = (self.x - i * 15, self.y - i * 15)
                darkness = 100 - i * 20
                pygame.draw.ellipse(screen, (darkness, 0, darkness), (*aura_pos, *aura_size))
            
            # Glowing red eyes
            eye_glow = 50 + math.sin(self.animation_frame * 0.3) * 50
            pygame.draw.circle(screen, (255, int(eye_glow), 0), (self.x + 30, self.y + 40), 15)
            pygame.draw.circle(screen, (255, int(eye_glow), 0), (self.x + 90, self.y + 40), 15)
            
            # Crown of darkness
            for i in range(7):
                spike_x = self.x + 20 + i * 15
                spike_y = self.y - 30
                pygame.draw.polygon(screen, BLACK, [(spike_x - 5, spike_y), (spike_x + 5, spike_y), (spike_x, spike_y - 40)])
        
        elif self.enemy_type == "chaos_beast":
            # Chaos Beast - constantly changing colors
            chaos_colors = [(255, 0, 255), (255, 255, 0), (0, 255, 255), (255, 128, 0)]
            chaos_color = chaos_colors[self.animation_frame // 15 % len(chaos_colors)]
            pygame.draw.ellipse(screen, chaos_color, (self.x, self.y, self.width, self.height))
            
            # Chaotic spikes everywhere
            for i in range(12):
                angle = (self.animation_frame + i * 30) * 0.1
                spike_x = self.x + self.width//2 + math.cos(angle) * 60
                spike_y = self.y + self.height//2 + math.sin(angle) * 60
                pygame.draw.circle(screen, chaos_color, (int(spike_x), int(spike_y)), 8)
            
            # Multiple eyes
            for i in range(6):
                eye_x = self.x + 20 + (i % 3) * 30
                eye_y = self.y + 30 + (i // 3) * 40
                pygame.draw.circle(screen, WHITE, (eye_x, eye_y), 8)
                pygame.draw.circle(screen, RED, (eye_x, eye_y), 4)
        
        elif self.enemy_type == "void_stalker":
            # Void Stalker - semi-transparent with void effect
            void_surface = pygame.Surface((self.width, self.height))
            void_surface.set_alpha(150)
            void_surface.fill(self.color)
            screen.blit(void_surface, (self.x, self.y))
            
            # Void tendrils
            for i in range(8):
                tendril_x = self.x + self.width//2 + math.cos(self.animation_frame * 0.1 + i) * 40
                tendril_y = self.y + self.height//2 + math.sin(self.animation_frame * 0.1 + i) * 40
                pygame.draw.line(screen, (100, 0, 150), (self.x + self.width//2, self.y + self.height//2),
                               (int(tendril_x), int(tendril_y)), 3)
            
            # Void core
            pygame.draw.circle(screen, (200, 0, 255), (self.x + self.width//2, self.y + self.height//2), 20)
        
        elif self.enemy_type == "death_knight":
            # Death Knight - massive armored figure
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            
            # Skull helmet
            pygame.draw.circle(screen, WHITE, (self.x + self.width//2, self.y + 30), 25)
            # Eye sockets
            pygame.draw.circle(screen, BLACK, (self.x + self.width//2 - 10, self.y + 25), 8)
            pygame.draw.circle(screen, BLACK, (self.x + self.width//2 + 10, self.y + 25), 8)
            # Glowing eyes
            pygame.draw.circle(screen, RED, (self.x + self.width//2 - 10, self.y + 25), 4)
            pygame.draw.circle(screen, RED, (self.x + self.width//2 + 10, self.y + 25), 4)
            
            # Massive sword
            sword_x = self.x + (self.width + 20) if self.facing_right else self.x - 30
            pygame.draw.rect(screen, GRAY, (sword_x, self.y - 20, 15, 100))
            pygame.draw.polygon(screen, GRAY, [(sword_x + 7, self.y - 20), (sword_x, self.y - 40), (sword_x + 15, self.y - 40)])
            
            # Death aura
            death_glow = pygame.Surface((self.width + 40, self.height + 40))
            death_glow.set_alpha(80)
            death_glow.fill((100, 0, 0))
            screen.blit(death_glow, (self.x - 20, self.y - 20))
        
        elif self.enemy_type == "plague_dragon":
            # Plague Dragon - sickly and toxic
            pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))
            
            # Toxic wings
            wing_y = self.y + 20 + math.sin(self.animation_frame * 0.15) * 8
            pygame.draw.ellipse(screen, (150, 200, 0), (self.x - 30, wing_y, 40, 60))
            pygame.draw.ellipse(screen, (150, 200, 0), (self.x + self.width - 10, wing_y, 40, 60))
            
            # Plague head with multiple eyes
            pygame.draw.circle(screen, self.color, (self.x + self.width//2, self.y + 25), 30)
            for i in range(4):
                eye_x = self.x + self.width//2 + (i - 2) * 15
                eye_y = self.y + 20 + (i % 2) * 10
                pygame.draw.circle(screen, YELLOW, (eye_x, eye_y), 6)
                pygame.draw.circle(screen, BLACK, (eye_x, eye_y), 3)
            
            # Toxic breath
            if self.animation_frame % 80 < 30:
                breath_x = self.x + (self.width + 40) if self.facing_right else self.x - 40
                for i in range(8):
                    toxic_x = breath_x + i * 15
                    toxic_y = self.y + 30 + random.randint(-10, 10)
                    pygame.draw.circle(screen, (200, 255, 0), (toxic_x, toxic_y), 6)
        
        elif self.enemy_type == "soul_reaper":
            # Soul Reaper - ghostly and fast
            ghost_surface = pygame.Surface((self.width, self.height))
            ghost_surface.set_alpha(180)
            ghost_surface.fill(self.color)
            screen.blit(ghost_surface, (self.x, self.y))
            
            # Scythe
            scythe_x = self.x + (self.width + 15) if self.facing_right else self.x - 25
            pygame.draw.line(screen, BLACK, (scythe_x, self.y), (scythe_x, self.y + 80), 5)
            pygame.draw.arc(screen, BLACK, (scythe_x - 15, self.y - 10, 30, 30), 0, 3.14, 3)
            
            # Soul trail
            for i in range(5):
                trail_x = self.x - i * 20
                trail_alpha = 200 - i * 40
                trail_surface = pygame.Surface((20, 20))
                trail_surface.set_alpha(trail_alpha)
                trail_surface.fill(WHITE)
                screen.blit(trail_surface, (trail_x, self.y + self.height//2))
        
        elif self.enemy_type in ["demon_overlord", "shadow_titan", "cosmic_horror", "apocalypse_bringer"]:
            # ULTIMATE BOSSES
            pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))
            
            # Massive aura effects
            for i in range(8):
                aura_size = (self.width + i * 20, self.height + i * 20)
                aura_pos = (self.x - i * 10, self.y - i * 10)
                if self.enemy_type == "demon_overlord":
                    aura_color = (255 - i * 30, 0, 0)
                elif self.enemy_type == "shadow_titan":
                    aura_color = (i * 10, i * 10, i * 10)
                elif self.enemy_type == "cosmic_horror":
                    aura_color = RAINBOW[i % len(RAINBOW)]
                else:  # apocalypse_bringer
                    aura_color = (255, 255 - i * 30, 0)
                
                aura_surface = pygame.Surface(aura_size)
                aura_surface.set_alpha(30 - i * 3)
                aura_surface.fill(aura_color)
                screen.blit(aura_surface, aura_pos)
            
            # Multiple crowns/horns for ultimate bosses
            for crown_layer in range(3):
                crown_x = self.x + self.width//2
                crown_y = self.y - 30 - crown_layer * 20
                crown_size = 30 + crown_layer * 10
                for spike in range(9):
                    spike_angle = spike * 0.7
                    spike_x = crown_x + math.cos(spike_angle) * crown_size
                    spike_y = crown_y + math.sin(spike_angle) * crown_size
                    pygame.draw.polygon(screen, GOLD, [
                        (crown_x, crown_y),
                        (spike_x - 5, spike_y),
                        (spike_x + 5, spike_y)
                    ])
            
            # Screen shake effect for apocalypse bringer
            if self.enemy_type == "apocalypse_bringer" and self.animation_frame % 30 < 5:
                shake_offset = random.randint(-5, 5)
                screen_shake = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                screen_shake.set_alpha(100)
                screen_shake.fill((255, 0, 0))
                screen.blit(screen_shake, (shake_offset, shake_offset))
            
            # Boss health bar - extra large for ultimate bosses
            bar_width = self.width + 40
            bar_height = 8
            bar_x = self.x - 20
            bar_y = self.y - 25
            
            pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
            health_width = int(bar_width * (self.health / self.max_health))
            
            if self.enemy_type == "apocalypse_bringer":
                health_color = RAINBOW[self.animation_frame // 5 % len(RAINBOW)]
            else:
                health_color = GREEN
            
            pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
            
            # Boss name display
            boss_name = self.enemy_type.replace("_", " ").title()
            name_surface = pygame.font.Font(None, 32).render(boss_name, True, WHITE)
            name_rect = name_surface.get_rect(center=(self.x + self.width//2, self.y - 50))
            screen.blit(name_surface, name_rect)
        
        # Health bar
        if self.health < self.max_health:
            bar_width = self.width
            bar_height = 4
            bar_x = self.x
            bar_y = self.y - 10
            
            pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
            health_width = int(bar_width * (self.health / self.max_health))
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))

class MudBall:
    def __init__(self, x, y, vx, vy, rainbow_mode=False):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = 8
        self.life = 180
        self.damage = 25
        self.rainbow_mode = rainbow_mode
        self.rainbow_frame = 0
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3  # Gravity
        self.life -= 1
        self.rainbow_frame += 1
        
        return self.life > 0 and 0 <= self.x <= WINDOW_WIDTH and 0 <= self.y <= WINDOW_HEIGHT
    
    def check_collision(self, enemy):
        dist = math.sqrt((self.x - (enemy.x + enemy.width//2))**2 + 
                        (self.y - (enemy.y + enemy.height//2))**2)
        return dist < self.size + 15
    
    def draw(self, screen):
        if self.rainbow_mode:
            color = RAINBOW[self.rainbow_frame // 5 % len(RAINBOW)]
            inner_color = RAINBOW[(self.rainbow_frame // 5 + 1) % len(RAINBOW)]
        else:
            color = BROWN
            inner_color = DARK_GREEN
        
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, inner_color, (int(self.x), int(self.y)), self.size - 2)

class Platform:
    def __init__(self, x, y, width, height, platform_type="ground"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.platform_type = platform_type
        
        if platform_type == "ground":
            self.color = BROWN
        elif platform_type == "swamp":
            self.color = SWAMP_GREEN
        elif platform_type == "castle":
            self.color = GRAY
        else:
            self.color = BROWN
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)

class Collectible:
    def __init__(self, x, y, item_type="onion"):
        self.x = x
        self.y = y
        self.item_type = item_type
        self.collected = False
        self.animation_frame = 0
        self.size = 15
    
    def update(self, shrek):
        self.animation_frame += 1
        
        # Check collection
        if not self.collected:
            dist = math.sqrt((self.x - (shrek.x + shrek.width//2))**2 + 
                           (self.y - (shrek.y + shrek.height//2))**2)
            if dist < 25:
                self.collected = True
                
                if self.item_type == "onion":
                    shrek.onions += 1
                elif self.item_type == "health":
                    shrek.health = min(shrek.max_health, shrek.health + 25)
                elif self.item_type == "mud":
                    shrek.mud_balls += 3
                
                # NEW INFINITE LEVEL COLLECTIBLES!
                elif self.item_type == "super_onion":
                    shrek.onions += 5
                    shrek.health = min(shrek.max_health, shrek.health + 10)
                elif self.item_type == "mega_health":
                    shrek.health = shrek.max_health  # Full heal!
                elif self.item_type == "explosive_mud":
                    shrek.mud_balls += 10
                elif self.item_type == "power_crystal":
                    # Temporary super powers
                    shrek.super_speed = True
                    shrek.super_jump = True
                elif self.item_type == "rainbow_gem":
                    shrek.rainbow_mode = True
                elif self.item_type == "giant_mushroom":
                    shrek.giant_mode = True
                
                return True
        return False
    
    def draw(self, screen):
        if self.collected:
            return
        
        y_offset = math.sin(self.animation_frame * 0.1) * 3
        
        if self.item_type == "onion":
            # Onion
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y + y_offset)), self.size)
            pygame.draw.circle(screen, BROWN, (int(self.x), int(self.y + y_offset)), self.size - 3)
        elif self.item_type == "health":
            # Health potion
            pygame.draw.rect(screen, RED, (self.x - 8, self.y + y_offset - 10, 16, 20))
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y + y_offset - 5)), 3)
        elif self.item_type == "mud":
            # Mud pile
            pygame.draw.circle(screen, BROWN, (int(self.x), int(self.y + y_offset)), self.size)
            pygame.draw.circle(screen, DARK_GREEN, (int(self.x), int(self.y + y_offset)), self.size - 3)
        
        # NEW SPECIAL COLLECTIBLES!
        elif self.item_type == "super_onion":
            # Golden onion
            pygame.draw.circle(screen, GOLD, (int(self.x), int(self.y + y_offset)), self.size + 3)
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y + y_offset)), self.size)
            # Sparkle effect
            for i in range(4):
                sparkle_x = self.x + math.cos(self.animation_frame * 0.1 + i) * 20
                sparkle_y = self.y + y_offset + math.sin(self.animation_frame * 0.1 + i) * 20
                pygame.draw.circle(screen, WHITE, (int(sparkle_x), int(sparkle_y)), 2)
        
        elif self.item_type == "mega_health":
            # Mega health potion with glow
            glow_size = self.size + 5 + math.sin(self.animation_frame * 0.2) * 3
            pygame.draw.circle(screen, (255, 100, 100), (int(self.x), int(self.y + y_offset)), int(glow_size))
            pygame.draw.rect(screen, (255, 0, 0), (self.x - 10, self.y + y_offset - 12, 20, 24))
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y + y_offset - 3)), 5)
            # Plus sign
            pygame.draw.line(screen, WHITE, (self.x - 6, self.y + y_offset), (self.x + 6, self.y + y_offset), 3)
            pygame.draw.line(screen, WHITE, (self.x, self.y + y_offset - 6), (self.x, self.y + y_offset + 6), 3)
        
        elif self.item_type == "explosive_mud":
            # Explosive mud with sparks
            pygame.draw.circle(screen, (150, 75, 0), (int(self.x), int(self.y + y_offset)), self.size + 2)
            pygame.draw.circle(screen, BROWN, (int(self.x), int(self.y + y_offset)), self.size)
            # Sparks
            for i in range(6):
                spark_x = self.x + math.cos(self.animation_frame * 0.3 + i) * 15
                spark_y = self.y + y_offset + math.sin(self.animation_frame * 0.3 + i) * 15
                pygame.draw.circle(screen, ORANGE, (int(spark_x), int(spark_y)), 1)
        
        elif self.item_type == "power_crystal":
            # Power crystal
            crystal_color = RAINBOW[self.animation_frame // 10 % len(RAINBOW)]
            pygame.draw.polygon(screen, crystal_color, [
                (self.x, self.y + y_offset + 10),
                (self.x - 10, self.y + y_offset),
                (self.x, self.y + y_offset - 10),
                (self.x + 10, self.y + y_offset)
            ])
            # Inner glow
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y + y_offset)), 5)
        
        elif self.item_type == "rainbow_gem":
            # Rainbow gem
            for i in range(7):
                color = RAINBOW[i]
                size = self.size - i * 2
                if size > 0:
                    pygame.draw.circle(screen, color, (int(self.x), int(self.y + y_offset)), size)
        
        elif self.item_type == "giant_mushroom":
            # Giant mushroom
            # Stem
            pygame.draw.rect(screen, WHITE, (self.x - 4, self.y + y_offset, 8, 15))
            # Cap
            pygame.draw.circle(screen, RED, (int(self.x), int(self.y + y_offset - 5)), 12)
            # Spots
            pygame.draw.circle(screen, WHITE, (int(self.x - 5), int(self.y + y_offset - 3)), 3)
            pygame.draw.circle(screen, WHITE, (int(self.x + 5), int(self.y + y_offset - 7)), 2)
            pygame.draw.circle(screen, WHITE, (int(self.x + 2), int(self.y + y_offset - 10)), 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Shrek's Swamp Adventure")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.running = True
        self.game_state = "playing"  # playing, paused, game_over, victory
        self.level = 1
        self.score = 0
        self.enemies_defeated = 0
        
        # Game objects
        self.shrek = Shrek(100, 100)
        self.enemies = []
        self.platforms = []
        self.collectibles = []
        self.mud_balls = []
        self.particles = []
        
        # Camera
        self.camera_x = 0
        self.camera_y = 0
        
        # Initialize level
        self.create_level()
        
        # Frame counter
        self.frame_count = 0
    
    def create_level(self):
        """Create platforms, enemies, and collectibles for current level"""
        self.platforms.clear()
        self.enemies.clear()
        self.collectibles.clear()
        
        # Ground platforms
        self.platforms.append(Platform(0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, 50, "ground"))
        
        # INFINITE LEVEL GENERATION!
        if self.level == 1:
            # Swamp level
            self.platforms.extend([
                Platform(200, 650, 200, 20, "swamp"),
                Platform(500, 600, 150, 20, "swamp"),
                Platform(750, 550, 200, 20, "swamp"),
                Platform(300, 500, 100, 20, "swamp"),
                Platform(600, 450, 150, 20, "swamp"),
            ])
            
            # Enemies
            self.enemies.extend([
                Enemy(300, 600, "knight"),
                Enemy(600, 550, "knight"),
                Enemy(800, 500, "fairy"),
                Enemy(400, 400, "knight"),
            ])
            
            # Collectibles
            self.collectibles.extend([
                Collectible(250, 620, "onion"),
                Collectible(550, 570, "health"),
                Collectible(800, 520, "mud"),
                Collectible(350, 470, "onion"),
            ])
        
        elif self.level == 2:
            # Castle approach
            self.platforms.extend([
                Platform(150, 650, 150, 20, "castle"),
                Platform(400, 600, 200, 20, "castle"),
                Platform(700, 550, 150, 20, "castle"),
                Platform(900, 500, 200, 20, "castle"),
                Platform(250, 450, 100, 20, "castle"),
                Platform(500, 400, 150, 20, "castle"),
                Platform(750, 350, 200, 20, "castle"),
            ])
            
            # More enemies
            self.enemies.extend([
                Enemy(200, 600, "knight"),
                Enemy(500, 550, "dragon"),
                Enemy(800, 500, "knight"),
                Enemy(300, 400, "fairy"),
                Enemy(600, 350, "knight"),
                Enemy(900, 300, "dragon"),
            ])
            
            # More collectibles
            self.collectibles.extend([
                Collectible(200, 620, "health"),
                Collectible(450, 570, "mud"),
                Collectible(750, 520, "onion"),
                Collectible(300, 420, "health"),
                Collectible(550, 370, "mud"),
                Collectible(800, 320, "onion"),
            ])
        
        else:
            # INFINITE PROCEDURAL GENERATION!
            self.generate_infinite_level()
    
    def generate_infinite_level(self):
        """Generate infinite procedural levels"""
        random.seed(self.level)  # Same seed = same level layout
        
        # Determine level theme based on level number
        themes = ["swamp", "castle", "volcano", "ice", "space", "underground", "cloud", "desert"]
        theme = themes[(self.level - 3) % len(themes)]
        
        # Platform generation
        platform_count = min(20, 5 + self.level)
        
        for i in range(platform_count):
            # Random platform placement with some logic
            x = random.randint(50, WINDOW_WIDTH - 200)
            y = random.randint(200, WINDOW_HEIGHT - 100)
            width = random.randint(80, 250)
            height = random.randint(15, 30)
            
            # Ensure platforms aren't too close to each other
            valid_position = True
            for platform in self.platforms:
                if (abs(platform.x - x) < 100 and abs(platform.y - y) < 50):
                    valid_position = False
                    break
            
            if valid_position:
                platform_type = theme if theme in ["swamp", "castle"] else "ground"
                self.platforms.append(Platform(x, y, width, height, platform_type))
        
        # Enemy generation - scales with level
        enemy_types = ["knight", "fairy", "dragon"]
        enemy_count = min(15, 3 + self.level // 2)
        
        # Add new enemy types for higher levels
        if self.level >= 5:
            enemy_types.append("boss_knight")
        if self.level >= 8:
            enemy_types.append("mega_dragon")
        if self.level >= 12:
            enemy_types.append("shadow_fairy")
        
        # PAHEMMAT VIHOLLISET KORKEAMMILLA TASOILLA!
        if self.level >= 15:
            enemy_types.extend(["nightmare_lord", "chaos_beast"])
        if self.level >= 20:
            enemy_types.extend(["void_stalker", "death_knight"])
        if self.level >= 25:
            enemy_types.extend(["plague_dragon", "soul_reaper"])
        if self.level >= 30:
            enemy_types.append("demon_overlord")
        if self.level >= 40:
            enemy_types.append("shadow_titan")
        if self.level >= 50:
            enemy_types.append("cosmic_horror")
        if self.level >= 100:
            enemy_types.append("apocalypse_bringer")
        
        for i in range(enemy_count):
            # Place enemies on or near platforms
            if self.platforms:
                platform = random.choice(self.platforms[1:])  # Skip ground platform
                enemy_x = platform.x + random.randint(0, max(1, platform.width - 50))
                enemy_y = platform.y - 50
                enemy_type = random.choice(enemy_types)
                
                self.enemies.append(Enemy(enemy_x, enemy_y, enemy_type))
        
        # Special boss enemies every 5 levels
        if self.level % 5 == 0:
            self.add_boss_enemy()
        
        # Collectible generation
        collectible_types = ["onion", "health", "mud"]
        collectible_count = min(12, 3 + self.level // 3)
        
        # Add special collectibles for higher levels
        if self.level >= 10:
            collectible_types.extend(["super_onion", "mega_health", "explosive_mud"])
        
        for i in range(collectible_count):
            if self.platforms:
                platform = random.choice(self.platforms[1:])
                collectible_x = platform.x + random.randint(20, max(21, platform.width - 20))
                collectible_y = platform.y - 25
                collectible_type = random.choice(collectible_types)
                
                self.collectibles.append(Collectible(collectible_x, collectible_y, collectible_type))
        
        # Add special level features
        self.add_level_features(theme)
    
    def add_boss_enemy(self):
        """Add special boss enemy every 5 levels"""
        if self.level < 15:
            boss_types = ["mega_dragon", "giant_knight", "shadow_boss", "ice_dragon", "fire_demon"]
        elif self.level < 30:
            boss_types = ["nightmare_lord", "chaos_beast", "void_stalker", "death_knight"]
        elif self.level < 50:
            boss_types = ["plague_dragon", "soul_reaper", "demon_overlord"]
        elif self.level < 100:
            boss_types = ["shadow_titan", "cosmic_horror"]
        else:
            boss_types = ["apocalypse_bringer"]  # Ultimate boss for level 100+
        
        boss_type = boss_types[(self.level // 5 - 1) % len(boss_types)]
        
        # Place boss in center area
        boss_x = WINDOW_WIDTH // 2
        boss_y = 200
        
        self.enemies.append(Enemy(boss_x, boss_y, boss_type))
    
    def add_level_features(self, theme):
        """Add special features based on theme"""
        if theme == "volcano":
            # Add lava pits (dangerous areas)
            for i in range(3):
                x = random.randint(100, WINDOW_WIDTH - 200)
                y = WINDOW_HEIGHT - 100
                self.platforms.append(Platform(x, y, 100, 50, "lava"))
        
        elif theme == "ice":
            # Add slippery ice platforms
            for i in range(2):
                x = random.randint(200, WINDOW_WIDTH - 300)
                y = random.randint(400, 600)
                self.platforms.append(Platform(x, y, 150, 20, "ice"))
        
        elif theme == "space":
            # Add floating platforms
            for i in range(4):
                x = random.randint(100, WINDOW_WIDTH - 150)
                y = random.randint(100, 500)
                self.platforms.append(Platform(x, y, 80, 15, "space"))
        
        elif theme == "cloud":
            # Add bouncy cloud platforms
            for i in range(3):
                x = random.randint(150, WINDOW_WIDTH - 200)
                y = random.randint(300, 600)
                self.platforms.append(Platform(x, y, 120, 25, "cloud"))
    
    def update_camera(self):
        """Update camera to follow Shrek"""
        target_x = self.shrek.x - WINDOW_WIDTH // 2
        target_y = self.shrek.y - WINDOW_HEIGHT // 2
        
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_y += (target_y - self.camera_y) * 0.1
        
        # Keep camera in bounds
        self.camera_x = max(0, min(self.camera_x, 0))  # No horizontal scrolling for now
        self.camera_y = max(-200, min(self.camera_y, 0))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.game_state = "paused" if self.game_state == "playing" else "playing"
                elif event.key == pygame.K_r and self.game_state == "game_over":
                    self.restart_game()
                elif event.key == pygame.K_q and self.game_state == "playing":
                    # Shrek's roar attack
                    particles = self.shrek.roar(self.enemies)
                    self.particles.extend(particles)
                
                # CHEAT CODES!
                elif event.key == pygame.K_F1:
                    # God Mode
                    self.shrek.god_mode = not self.shrek.god_mode
                    if self.shrek.god_mode:
                        self.shrek.health = self.shrek.max_health
                
                elif event.key == pygame.K_F2:
                    # Super Speed
                    self.shrek.super_speed = not self.shrek.super_speed
                
                elif event.key == pygame.K_F3:
                    # Infinite Ammo
                    self.shrek.infinite_ammo = not self.shrek.infinite_ammo
                    if self.shrek.infinite_ammo:
                        self.shrek.mud_balls = 999
                
                elif event.key == pygame.K_F4:
                    # Rainbow Mode
                    self.shrek.rainbow_mode = not self.shrek.rainbow_mode
                
                elif event.key == pygame.K_F5:
                    # Giant Mode
                    self.shrek.giant_mode = not self.shrek.giant_mode
                
                elif event.key == pygame.K_F6:
                    # Noclip Mode
                    self.shrek.noclip = not self.shrek.noclip
                
                elif event.key == pygame.K_F7:
                    # Auto Heal
                    self.shrek.auto_heal = not self.shrek.auto_heal
                
                elif event.key == pygame.K_F8:
                    # Super Jump
                    self.shrek.super_jump = not self.shrek.super_jump
                
                elif event.key == pygame.K_F9:
                    # Rapid Fire
                    self.shrek.rapid_fire = not self.shrek.rapid_fire
                
                elif event.key == pygame.K_F10:
                    # Kill All Enemies
                    for enemy in self.enemies[:]:
                        particles = enemy.take_damage(9999)
                        self.particles.extend(particles)
                
                elif event.key == pygame.K_F11:
                    # Level Skip
                    self.enemies.clear()
                
                elif event.key == pygame.K_F12:
                    # ALL CHEATS ON!
                    self.shrek.god_mode = True
                    self.shrek.super_speed = True
                    self.shrek.infinite_ammo = True
                    self.shrek.rainbow_mode = True
                    self.shrek.giant_mode = True
                    self.shrek.noclip = True
                    self.shrek.auto_heal = True
                    self.shrek.super_jump = True
                    self.shrek.rapid_fire = True
                    self.shrek.health = self.shrek.max_health
                    self.shrek.mud_balls = 999
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.game_state == "playing":  # Left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mud_ball = self.shrek.throw_mud(mouse_x - self.camera_x, mouse_y - self.camera_y)
                    if mud_ball:
                        self.mud_balls.append(mud_ball)
    
    def update(self):
        if self.game_state != "playing":
            return
        
        self.frame_count += 1
        
        # Update Shrek
        self.shrek.update(self.platforms)
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(self.shrek, self.platforms)
            if enemy.health <= 0:
                particles = enemy.take_damage(0)  # Get death particles
                self.particles.extend(particles)
                self.enemies.remove(enemy)
                self.enemies_defeated += 1
                self.score += 100
        
        # Update mud balls
        for mud_ball in self.mud_balls[:]:
            if not mud_ball.update():
                self.mud_balls.remove(mud_ball)
                continue
            
            # Check enemy collisions
            for enemy in self.enemies:
                if mud_ball.check_collision(enemy):
                    particles = enemy.take_damage(mud_ball.damage)
                    self.particles.extend(particles)
                    if mud_ball in self.mud_balls:
                        self.mud_balls.remove(mud_ball)
                    break
        
        # Update collectibles
        for collectible in self.collectibles[:]:
            if collectible.update(self.shrek):
                self.score += 50
        
        # Update particles
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
        
        # Update camera
        self.update_camera()
        
        # Check level completion - INFINITE LEVELS!
        if len(self.enemies) == 0:
            # Never ending game! Always generate next level
            self.level += 1
            self.create_level()
            
            # Rewards for completing levels
            self.shrek.health = min(self.shrek.max_health, self.shrek.health + 25)
            self.shrek.mud_balls += 2
            self.score += self.level * 100  # Bonus score based on level
            
            # Special rewards every 5 levels
            if self.level % 5 == 0:
                self.shrek.health = self.shrek.max_health  # Full heal
                self.shrek.mud_balls += 10
                self.score += 1000
            
            # Epic rewards every 10 levels
            if self.level % 10 == 0:
                self.shrek.max_health += 25  # Increase max health
                self.shrek.health = self.shrek.max_health
                self.score += 5000
        
        # Check game over
        if self.shrek.health <= 0:
            self.game_state = "game_over"
    
    def restart_game(self):
        """Restart the game"""
        self.game_state = "playing"
        self.level = 1
        self.score = 0
        self.enemies_defeated = 0
        self.frame_count = 0
        
        self.shrek = Shrek(100, 100)
        self.mud_balls.clear()
        self.particles.clear()
        
        self.camera_x = 0
        self.camera_y = 0
        
        self.create_level()
    
    def draw_background(self):
        """Draw background based on level"""
        if self.level == 1:
            # Swamp background
            self.screen.fill(SWAMP_GREEN)
            
            # Draw swamp trees
            for i in range(0, WINDOW_WIDTH, 100):
                tree_x = i + int(self.camera_x * 0.3)
                pygame.draw.rect(self.screen, BROWN, (tree_x, 200, 15, 200))
                pygame.draw.circle(self.screen, DARK_GREEN, (tree_x + 7, 180), 30)
        
        elif self.level == 2:
            # Castle approach
            self.screen.fill(LIGHT_BLUE)
            
            # Draw castle in background
            castle_x = WINDOW_WIDTH - 200 + int(self.camera_x * 0.2)
            pygame.draw.rect(self.screen, GRAY, (castle_x, 100, 150, 200))
            pygame.draw.polygon(self.screen, DARK_GRAY, [
                (castle_x + 75, 100), (castle_x + 50, 50), (castle_x + 100, 50)
            ])
        
        else:
            # INFINITE LEVEL THEMES!
            themes = ["swamp", "castle", "volcano", "ice", "space", "underground", "cloud", "desert"]
            theme = themes[(self.level - 3) % len(themes)]
            
            if theme == "volcano":
                self.screen.fill((100, 0, 0))  # Dark red
                # Lava streams
                for i in range(0, WINDOW_WIDTH, 150):
                    lava_x = i + int(self.camera_x * 0.1)
                    pygame.draw.rect(self.screen, (255, 100, 0), (lava_x, 600, 20, 200))
                # Smoke clouds
                for i in range(0, WINDOW_WIDTH, 200):
                    smoke_x = i + int(self.camera_x * 0.2)
                    pygame.draw.circle(self.screen, (80, 80, 80), (smoke_x, 150), 40)
            
            elif theme == "ice":
                self.screen.fill((200, 230, 255))  # Ice blue
                # Ice crystals
                for i in range(0, WINDOW_WIDTH, 120):
                    crystal_x = i + int(self.camera_x * 0.3)
                    pygame.draw.polygon(self.screen, WHITE, [
                        (crystal_x, 300), (crystal_x - 20, 250), (crystal_x + 20, 250)
                    ])
                # Snow particles
                for i in range(20):
                    snow_x = (i * 60 + self.frame_count) % WINDOW_WIDTH
                    snow_y = (i * 100 + self.frame_count * 2) % WINDOW_HEIGHT
                    pygame.draw.circle(self.screen, WHITE, (snow_x, snow_y), 2)
            
            elif theme == "space":
                self.screen.fill((10, 10, 30))  # Dark space
                # Stars
                for i in range(50):
                    star_x = (i * 37) % WINDOW_WIDTH
                    star_y = (i * 73) % WINDOW_HEIGHT
                    pygame.draw.circle(self.screen, WHITE, (star_x, star_y), 1)
                # Planets
                pygame.draw.circle(self.screen, (100, 150, 200), (200, 150), 30)
                pygame.draw.circle(self.screen, (200, 100, 100), (800, 200), 25)
            
            elif theme == "underground":
                self.screen.fill((50, 30, 20))  # Dark brown
                # Cave walls
                for i in range(0, WINDOW_WIDTH, 100):
                    wall_x = i + int(self.camera_x * 0.1)
                    pygame.draw.rect(self.screen, (30, 20, 10), (wall_x, 0, 50, 200))
                # Stalactites
                for i in range(0, WINDOW_WIDTH, 80):
                    stal_x = i + int(self.camera_x * 0.2)
                    pygame.draw.polygon(self.screen, GRAY, [
                        (stal_x, 0), (stal_x - 10, 50), (stal_x + 10, 50)
                    ])
            
            elif theme == "cloud":
                self.screen.fill((150, 200, 255))  # Sky blue
                # Clouds
                for i in range(0, WINDOW_WIDTH, 150):
                    cloud_x = i + int(self.camera_x * 0.4)
                    pygame.draw.circle(self.screen, WHITE, (cloud_x, 100), 40)
                    pygame.draw.circle(self.screen, WHITE, (cloud_x + 30, 100), 35)
                    pygame.draw.circle(self.screen, WHITE, (cloud_x - 30, 100), 30)
                # Rainbows
                if self.level % 20 == 0:  # Special rainbow levels
                    for i, color in enumerate(RAINBOW):
                        pygame.draw.arc(self.screen, color, (400, 200, 400, 200), 0, 3.14, 5 + i)
            
            elif theme == "desert":
                self.screen.fill((255, 200, 100))  # Sandy yellow
                # Sand dunes
                for i in range(0, WINDOW_WIDTH, 200):
                    dune_x = i + int(self.camera_x * 0.2)
                    pygame.draw.ellipse(self.screen, (255, 180, 80), (dune_x, 400, 150, 80))
                # Cacti
                for i in range(0, WINDOW_WIDTH, 300):
                    cactus_x = i + int(self.camera_x * 0.3)
                    pygame.draw.rect(self.screen, GREEN, (cactus_x, 300, 10, 100))
                    pygame.draw.rect(self.screen, GREEN, (cactus_x - 15, 330, 20, 8))
            
            else:  # Default castle theme
                self.screen.fill(PURPLE)
                # Draw castle walls
                for i in range(0, WINDOW_WIDTH, 50):
                    wall_x = i + int(self.camera_x * 0.1)
                    pygame.draw.rect(self.screen, GRAY, (wall_x, 0, 25, 100))
    
    def draw_ui(self):
        """Draw user interface"""
        # Health bar
        health_bar_width = 200
        health_bar_height = 20
        health_x = 20
        health_y = 20
        
        pygame.draw.rect(self.screen, RED, (health_x, health_y, health_bar_width, health_bar_height))
        health_width = int(health_bar_width * (self.shrek.health / self.shrek.max_health))
        health_color = NEON_GREEN if self.shrek.god_mode else GREEN
        pygame.draw.rect(self.screen, health_color, (health_x, health_y, health_width, health_bar_height))
        
        health_text = self.small_font.render(f"Health: {self.shrek.health}/{self.shrek.max_health}", True, WHITE)
        self.screen.blit(health_text, (health_x, health_y + 25))
        
        # Items
        items_y = 70
        onion_text = self.small_font.render(f"Onions: {self.shrek.onions}", True, WHITE)
        mud_display = "∞" if self.shrek.infinite_ammo else str(self.shrek.mud_balls)
        mud_text = self.small_font.render(f"Mud Balls: {mud_display}", True, WHITE)
        
        self.screen.blit(onion_text, (20, items_y))
        self.screen.blit(mud_text, (20, items_y + 25))
        
        # Score and level with theme
        score_text = self.font.render(f"Score: {self.score}", True, GOLD)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        enemies_text = self.small_font.render(f"Enemies: {len(self.enemies)}", True, WHITE)
        
        # Show level theme for infinite levels
        if self.level >= 3:
            themes = ["swamp", "castle", "volcano", "ice", "space", "underground", "cloud", "desert"]
            current_theme = themes[(self.level - 3) % len(themes)]
            theme_text = self.small_font.render(f"Theme: {current_theme.title()}", True, YELLOW)
            self.screen.blit(theme_text, (WINDOW_WIDTH - 200, 130))
        
        self.screen.blit(score_text, (WINDOW_WIDTH - 200, 20))
        self.screen.blit(level_text, (WINDOW_WIDTH - 200, 60))
        self.screen.blit(enemies_text, (WINDOW_WIDTH - 200, 100))
        
        # CHEAT STATUS
        cheat_y = WINDOW_HEIGHT - 200
        active_cheats = []
        
        if self.shrek.god_mode:
            active_cheats.append("GOD MODE")
        if self.shrek.super_speed:
            active_cheats.append("SUPER SPEED")
        if self.shrek.infinite_ammo:
            active_cheats.append("INFINITE AMMO")
        if self.shrek.rainbow_mode:
            active_cheats.append("RAINBOW MODE")
        if self.shrek.giant_mode:
            active_cheats.append("GIANT MODE")
        if self.shrek.noclip:
            active_cheats.append("NOCLIP")
        if self.shrek.auto_heal:
            active_cheats.append("AUTO HEAL")
        if self.shrek.super_jump:
            active_cheats.append("SUPER JUMP")
        if self.shrek.rapid_fire:
            active_cheats.append("RAPID FIRE")
        
        if active_cheats:
            cheat_title = self.small_font.render("ACTIVE CHEATS:", True, NEON_GREEN)
            self.screen.blit(cheat_title, (WINDOW_WIDTH - 250, cheat_y))
            
            for i, cheat in enumerate(active_cheats):
                cheat_text = self.small_font.render(cheat, True, RAINBOW[i % len(RAINBOW)])
                self.screen.blit(cheat_text, (WINDOW_WIDTH - 250, cheat_y + 20 + i * 15))
        
        # Controls
        controls = [
            "WASD/Arrows: Move",
            "Space: Jump", 
            "Click: Throw Mud",
            "Q: Roar Attack",
            "P: Pause",
            "",
            "CHEAT CODES:",
            "F1: God Mode",
            "F2: Super Speed",
            "F3: Infinite Ammo",
            "F4: Rainbow Mode",
            "F5: Giant Mode",
            "F6: Noclip",
            "F7: Auto Heal",
            "F8: Super Jump",
            "F9: Rapid Fire",
            "F10: Kill All",
            "F11: Skip Level",
            "F12: ALL CHEATS!"
        ]
        
        for i, control in enumerate(controls):
            if control == "CHEAT CODES:":
                color = NEON_GREEN
            elif control.startswith("F"):
                color = YELLOW
            else:
                color = WHITE
            
            if control:  # Skip empty lines
                text = self.small_font.render(control, True, color)
                self.screen.blit(text, (20, WINDOW_HEIGHT - 400 + i * 16))
    
    def draw(self):
        # Draw background
        self.draw_background()
        
        # Apply camera offset
        camera_offset_x = int(self.camera_x)
        camera_offset_y = int(self.camera_y)
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen)
        
        # Draw collectibles
        for collectible in self.collectibles:
            collectible.draw(self.screen)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw mud balls
        for mud_ball in self.mud_balls:
            mud_ball.draw(self.screen)
        
        # Draw Shrek
        self.shrek.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Draw game state overlays
        if self.game_state == "paused":
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            pause_text = self.font.render("PAUSED - Press P to continue", True, WHITE)
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(pause_text, text_rect)
        
        elif self.game_state == "game_over":
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(RED)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("GAME OVER - Shrek has fallen!", True, WHITE)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            level_text = self.font.render(f"Reached Level: {self.level}", True, WHITE)
            restart_text = self.font.render("Press R to restart", True, WHITE)
            
            texts = [game_over_text, score_text, level_text, restart_text]
            for i, text in enumerate(texts):
                text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + i * 40))
                self.screen.blit(text, text_rect)
        
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
