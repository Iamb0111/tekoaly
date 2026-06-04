import pygame
import random
import math
import sys

pygame.init()

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PINK = (255, 20, 147)
NEON_GREEN = (57, 255, 20)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

class Player:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT - 100
        self.size = 12
        self.speed = 6
        self.focus_speed = 3
        self.health = 100
        self.max_health = 100
        self.power = 1
        self.max_power = 5
        self.score = 0
        self.lives = 3
        self.invincible = 0
        self.shoot_cooldown = 0
        self.bomb_count = 3
        self.hitbox_size = 3
        self.auto_aim = True  # Auto-aim enabled by default
        
        # Hacker abilities
        self.hacker_mode = True
        self.hack_energy = 100
        self.max_hack_energy = 100
        self.rapid_fire = False
        self.rapid_fire_timer = 0
        self.shield_active = False
        self.shield_timer = 0
        self.time_slow = False
        self.time_slow_timer = 0
        self.glitch_particles = []
        
    def update(self, keys):
        # Focus mode for precise movement
        speed = self.focus_speed if keys[pygame.K_LSHIFT] else self.speed
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += speed
        
        # Keep in bounds
        self.x = max(self.size, min(WINDOW_WIDTH - self.size, self.x))
        self.y = max(self.size, min(WINDOW_HEIGHT - self.size, self.y))
        
        # Update timers
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.invincible > 0:
            self.invincible -= 1
        
        # Hacker ability timers
        if self.rapid_fire_timer > 0:
            self.rapid_fire_timer -= 1
            self.rapid_fire = True
        else:
            self.rapid_fire = False
        
        if self.shield_timer > 0:
            self.shield_timer -= 1
            self.shield_active = True
        else:
            self.shield_active = False
        
        if self.time_slow_timer > 0:
            self.time_slow_timer -= 1
            self.time_slow = True
        else:
            self.time_slow = False
        
        # Regenerate hack energy
        if self.hack_energy < self.max_hack_energy:
            self.hack_energy += 0.2
        
        # Update glitch particles
        for particle in self.glitch_particles[:]:
            particle['lifetime'] -= 1
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            if particle['lifetime'] <= 0:
                self.glitch_particles.remove(particle)
    
    def shoot(self):
        cooldown = 2 if self.rapid_fire else 5
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = cooldown
            return True
        return False
    
    def activate_rapid_fire(self):
        if self.hack_energy >= 30:
            self.hack_energy -= 30
            self.rapid_fire_timer = 180  # 3 seconds
            return True
        return False
    
    def activate_shield(self):
        if self.hack_energy >= 40:
            self.hack_energy -= 40
            self.shield_timer = 240  # 4 seconds
            return True
        return False
    
    def activate_time_slow(self):
        if self.hack_energy >= 50:
            self.hack_energy -= 50
            self.time_slow_timer = 300  # 5 seconds
            return True
        return False
    
    def add_glitch_particles(self):
        for _ in range(5):
            self.glitch_particles.append({
                'x': self.x,
                'y': self.y,
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'lifetime': random.randint(10, 20),
                'color': random.choice([NEON_GREEN, CYAN, PURPLE])
            })
    
    def use_bomb(self):
        if self.bomb_count > 0:
            # Infinity bombs - no decrease
            self.invincible = 120  # 2 seconds
            return True
        return False
    
    def take_damage(self):
        if self.shield_active:
            return False  # Shield blocks damage
        if self.invincible <= 0:
            self.lives -= 1
            self.invincible = 180  # 3 seconds
            self.power = max(1, self.power - 1)
            return True
        return False
    
    def draw(self, screen, focus_mode):
        # Draw glitch particles
        for particle in self.glitch_particles:
            size = int(particle['lifetime'] / 4)
            if size > 0:
                pygame.draw.circle(screen, particle['color'], (int(particle['x']), int(particle['y'])), size)
        
        # Draw shield
        if self.shield_active:
            shield_radius = self.size + 10
            for i in range(3):
                alpha_size = shield_radius + i * 3
                pygame.draw.circle(screen, CYAN, (int(self.x), int(self.y)), alpha_size, 2)
        
        # Draw hitbox when focusing
        if focus_mode:
            pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.hitbox_size, 2)
        
        # Draw auto-aim indicator
        if self.auto_aim:
            # Draw small crosshair above player
            crosshair_y = self.y - 25
            pygame.draw.line(screen, YELLOW, (self.x - 5, crosshair_y), (self.x + 5, crosshair_y), 2)
            pygame.draw.line(screen, YELLOW, (self.x, crosshair_y - 5), (self.x, crosshair_y + 5), 2)
        
        # Draw hacker player (digital/glitch style)
        color = NEON_GREEN if self.rapid_fire else (CYAN if self.invincible > 0 else PURPLE)
        
        # Main body - diamond shape for hacker look
        points = [
            (self.x, self.y - self.size),
            (self.x + self.size, self.y),
            (self.x, self.y + self.size),
            (self.x - self.size, self.y)
        ]
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, WHITE, points, 2)
        
        # Digital overlay lines
        pygame.draw.line(screen, NEON_GREEN, (self.x - self.size//2, self.y), (self.x + self.size//2, self.y), 1)
        pygame.draw.line(screen, NEON_GREEN, (self.x, self.y - self.size//2), (self.x, self.y + self.size//2), 1)
        
        # Hacker eye
        pygame.draw.circle(screen, NEON_GREEN, (int(self.x), int(self.y)), 3)

class PlayerBullet:
    def __init__(self, x, y, angle=0, power=1):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 15
        self.damage = 10 * power
        self.size = 4 + power
        self.color = NEON_GREEN
        self.active = True
        
    def update(self):
        self.y -= self.speed
        self.x += math.sin(self.angle) * 2
        
        if self.y < -10 or self.x < 0 or self.x > WINDOW_WIDTH:
            self.active = False
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class Enemy:
    def __init__(self, x, y, enemy_type="basic"):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.health = 50
        self.max_health = 50
        self.size = 20
        self.speed = 2
        self.shoot_timer = 0
        self.movement_timer = 0
        self.active = True
        
        if enemy_type == "fast":
            self.speed = 4
            self.health = 30
            self.max_health = 30
            self.size = 15
            self.color = RED
        elif enemy_type == "tank":
            self.speed = 1
            self.health = 150
            self.max_health = 150
            self.size = 30
            self.color = PURPLE
        elif enemy_type == "shooter":
            self.speed = 1.5
            self.health = 40
            self.max_health = 40
            self.size = 18
            self.color = ORANGE
        else:
            self.color = GREEN
    
    def update(self, player):
        self.movement_timer += 1
        
        # Movement patterns
        if self.type == "fast":
            # Dive at player
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0:
                self.x += (dx/dist) * self.speed
                self.y += (dy/dist) * self.speed
        elif self.type == "tank":
            # Slow straight movement
            self.y += self.speed
        elif self.type == "shooter":
            # Sine wave movement
            self.y += self.speed
            self.x += math.sin(self.movement_timer * 0.05) * 3
        else:
            # Basic zigzag
            self.y += self.speed
            if self.movement_timer % 60 < 30:
                self.x += 1
            else:
                self.x -= 1
        
        # Shooting
        self.shoot_timer += 1
        
        # Remove if off screen
        if self.y > WINDOW_HEIGHT + 50 or self.health <= 0:
            self.active = False
    
    def can_shoot(self):
        if self.type == "shooter":
            return self.shoot_timer >= 60
        elif self.type == "tank":
            return self.shoot_timer >= 90
        else:
            return self.shoot_timer >= 120
    
    def shoot(self, player):
        if self.can_shoot():
            self.shoot_timer = 0
            bullets = []
            
            if self.type == "shooter":
                # Aimed bullet
                dx = player.x - self.x
                dy = player.y - self.y
                angle = math.atan2(dy, dx)
                bullets.append(EnemyBullet(self.x, self.y, angle))
            elif self.type == "tank":
                # Spread shot
                for i in range(5):
                    angle = math.pi/2 + (i - 2) * 0.3
                    bullets.append(EnemyBullet(self.x, self.y, angle))
            else:
                # Single down bullet
                bullets.append(EnemyBullet(self.x, self.y, math.pi/2))
            
            return bullets
        return []
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size, 2)
        
        # Health bar
        if self.health < self.max_health:
            bar_width = 40
            bar_height = 4
            health_ratio = self.health / self.max_health
            pygame.draw.rect(screen, RED, (self.x - bar_width//2, self.y - self.size - 10, bar_width, bar_height))
            pygame.draw.rect(screen, GREEN, (self.x - bar_width//2, self.y - self.size - 10, bar_width * health_ratio, bar_height))

class EnemyBullet:
    def __init__(self, x, y, angle, speed=5, bullet_type="normal"):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.type = bullet_type
        self.size = 6
        self.color = RED
        self.active = True
        self.lifetime = 300
        
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.lifetime -= 1
        
        if (self.x < -20 or self.x > WINDOW_WIDTH + 20 or 
            self.y < -20 or self.y > WINDOW_HEIGHT + 20 or
            self.lifetime <= 0):
            self.active = False
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size, 1)

class Boss:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = 100
        self.size = 60
        self.health = 1000
        self.max_health = 1000
        self.speed = 3
        self.phase = 1
        self.attack_timer = 0
        self.movement_timer = 0
        self.active = True
        self.color = PURPLE
        
    def update(self, player):
        self.movement_timer += 1
        self.attack_timer += 1
        
        # Movement
        self.x += math.sin(self.movement_timer * 0.02) * 4
        self.x = max(self.size, min(WINDOW_WIDTH - self.size, self.x))
        
        # Phase changes
        if self.health < self.max_health * 0.5 and self.phase == 1:
            self.phase = 2
            self.color = RED
        
        if self.health <= 0:
            self.active = False
    
    def shoot(self, player):
        bullets = []
        
        if self.phase == 1:
            # Circle pattern
            if self.attack_timer >= 30:
                self.attack_timer = 0
                for i in range(12):
                    angle = (i / 12) * math.pi * 2
                    bullets.append(EnemyBullet(self.x, self.y, angle, 4))
        else:
            # Spiral + aimed
            if self.attack_timer >= 20:
                self.attack_timer = 0
                # Spiral
                for i in range(8):
                    angle = (i / 8) * math.pi * 2 + self.movement_timer * 0.1
                    bullets.append(EnemyBullet(self.x, self.y, angle, 5))
                # Aimed shots
                dx = player.x - self.x
                dy = player.y - self.y
                angle = math.atan2(dy, dx)
                for offset in [-0.3, 0, 0.3]:
                    bullets.append(EnemyBullet(self.x, self.y, angle + offset, 7))
        
        return bullets
    
    def draw(self, screen):
        # Boss body
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size, 3)
        
        # Boss eyes
        eye_offset = 15
        pygame.draw.circle(screen, YELLOW, (int(self.x - eye_offset), int(self.y - 10)), 8)
        pygame.draw.circle(screen, YELLOW, (int(self.x + eye_offset), int(self.y - 10)), 8)
        pygame.draw.circle(screen, BLACK, (int(self.x - eye_offset), int(self.y - 10)), 4)
        pygame.draw.circle(screen, BLACK, (int(self.x + eye_offset), int(self.y - 10)), 4)
        
        # Health bar
        bar_width = 200
        bar_height = 10
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, RED, (WINDOW_WIDTH//2 - bar_width//2, 20, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (WINDOW_WIDTH//2 - bar_width//2, 20, bar_width * health_ratio, bar_height))
        pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH//2 - bar_width//2, 20, bar_width, bar_height), 2)

class Powerup:
    def __init__(self, x, y, powerup_type):
        self.x = x
        self.y = y
        self.type = powerup_type
        self.size = 10
        self.speed = 2
        self.bounce = 0
        self.active = True
        
        if powerup_type == "power":
            self.color = YELLOW
        elif powerup_type == "health":
            self.color = GREEN
        elif powerup_type == "bomb":
            self.color = CYAN
        else:
            self.color = WHITE
    
    def update(self):
        self.y += self.speed
        self.bounce += 0.2
        
        if self.y > WINDOW_HEIGHT + 20:
            self.active = False
    
    def draw(self, screen):
        bounce_offset = math.sin(self.bounce) * 3
        draw_y = self.y + bounce_offset
        pygame.draw.circle(screen, self.color, (int(self.x), int(draw_y)), self.size)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(draw_y)), self.size, 2)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.color = color
        self.lifetime = random.randint(20, 40)
        self.size = random.randint(2, 5)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.95
        self.vy *= 0.95
        self.lifetime -= 1
    
    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class BulletStormGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Cosmic Bullet Storm")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 64)
        
        # Game state
        self.running = True
        self.game_over = False
        self.victory = False
        self.wave = 1
        self.enemy_spawn_timer = 0
        self.boss_spawned = False
        
        # Game objects
        self.player = Player()
        self.player_bullets = []
        self.enemies = []
        self.enemy_bullets = []
        self.boss = None
        self.powerups = []
        self.particles = []
        
        # Background stars
        self.stars = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) 
                      for _ in range(100)]
    
    def spawn_enemy(self):
        x = random.randint(50, WINDOW_WIDTH - 50)
        y = -30
        enemy_types = ["basic", "fast", "shooter", "tank"]
        weights = [40, 30, 20, 10]
        enemy_type = random.choices(enemy_types, weights=weights)[0]
        self.enemies.append(Enemy(x, y, enemy_type))
    
    def spawn_boss(self):
        if not self.boss_spawned:
            self.boss = Boss()
            self.boss_spawned = True
    
    def create_explosion(self, x, y, color, count=15):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    if self.player.use_bomb():
                        # Clear all enemy bullets
                        self.enemy_bullets.clear()
                        # Damage all enemies and give 1000 points per enemy
                        for enemy in self.enemies:
                            enemy.health -= 50
                            if enemy.health <= 0:
                                self.player.score += 1000
                        if self.boss and self.boss.active:
                            self.boss.health -= 100
                        self.create_explosion(self.player.x, self.player.y, CYAN, 30)
                elif event.key == pygame.K_c:
                    # Toggle auto-aim
                    self.player.auto_aim = not self.player.auto_aim
                elif event.key == pygame.K_1:
                    # Rapid fire hack
                    self.player.activate_rapid_fire()
                elif event.key == pygame.K_2:
                    # Shield hack
                    self.player.activate_shield()
                elif event.key == pygame.K_3:
                    # Time slow hack
                    self.player.activate_time_slow()
                elif event.key == pygame.K_r and (self.game_over or self.victory):
                    self.restart_game()
    
    def restart_game(self):
        self.player = Player()
        self.player_bullets.clear()
        self.enemies.clear()
        self.enemy_bullets.clear()
        self.boss = None
        self.powerups.clear()
        self.particles.clear()
        self.wave = 1
        self.boss_spawned = False
        self.game_over = False
        self.victory = False
    
    def update(self):
        if self.game_over or self.victory:
            return
        
        keys = pygame.key.get_pressed()
        focus_mode = keys[pygame.K_LSHIFT]
        
        # Update player
        self.player.update(keys)
        
        # Player shooting
        if keys[pygame.K_z] or keys[pygame.K_SPACE]:
            if self.player.shoot():
                if self.player.auto_aim:
                    # Find nearest enemy for auto-aim
                    nearest_target = None
                    min_dist = float('inf')
                    
                    # Check enemies
                    for enemy in self.enemies:
                        dx = enemy.x - self.player.x
                        dy = enemy.y - self.player.y
                        dist = math.sqrt(dx*dx + dy*dy)
                        if dist < min_dist and dy < 0:  # Only aim at enemies above player
                            min_dist = dist
                            nearest_target = (enemy.x, enemy.y)
                    
                    # Check boss
                    if self.boss and self.boss.active:
                        dx = self.boss.x - self.player.x
                        dy = self.boss.y - self.player.y
                        dist = math.sqrt(dx*dx + dy*dy)
                        if dist < min_dist and dy < 0:
                            min_dist = dist
                            nearest_target = (self.boss.x, self.boss.y)
                    
                    # Shoot towards target or straight up if no target
                    if nearest_target:
                        target_angle = math.atan2(nearest_target[1] - self.player.y, 
                                                  nearest_target[0] - self.player.x)
                        for i in range(self.player.power):
                            angle_offset = (i - (self.player.power - 1) / 2) * 0.15
                            bullet_angle = target_angle + angle_offset - math.pi/2  # Adjust for bullet direction
                            self.player_bullets.append(PlayerBullet(self.player.x, self.player.y, 
                                                                    bullet_angle, self.player.power))
                    else:
                        # No target, shoot straight up
                        for i in range(self.player.power):
                            angle = (i - (self.player.power - 1) / 2) * 0.2
                            self.player_bullets.append(PlayerBullet(self.player.x, self.player.y, 
                                                                    angle, self.player.power))
                else:
                    # Normal shooting (straight up)
                    for i in range(self.player.power):
                        angle = (i - (self.player.power - 1) / 2) * 0.2
                        self.player_bullets.append(PlayerBullet(self.player.x, self.player.y, 
                                                                angle, self.player.power))
        
        # Spawn enemies
        if self.wave < 5:
            self.enemy_spawn_timer += 1
            spawn_rate = max(30, 90 - self.wave * 10)
            if self.enemy_spawn_timer >= spawn_rate:
                self.spawn_enemy()
                self.enemy_spawn_timer = 0
        elif self.wave == 5 and not self.boss_spawned:
            self.spawn_boss()
        
        # Add glitch particles to player
        if random.random() < 0.1:
            self.player.add_glitch_particles()
        
        # Update player bullets (affected by time slow)
        bullet_updates = 2 if self.player.time_slow else 1
        for _ in range(bullet_updates):
            for bullet in self.player_bullets[:]:
                bullet.update()
                if not bullet.active:
                    self.player_bullets.remove(bullet)
                    continue
                
                # Check collision with enemies
                for enemy in self.enemies[:]:
                    dx = bullet.x - enemy.x
                    dy = bullet.y - enemy.y
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist < bullet.size + enemy.size:
                        enemy.health -= bullet.damage
                        if bullet in self.player_bullets:
                            self.player_bullets.remove(bullet)
                        if enemy.health <= 0:
                            self.player.score += 100
                            self.create_explosion(enemy.x, enemy.y, enemy.color)
                            # Drop powerup chance
                            if random.random() < 0.3:
                                powerup_type = random.choice(["power", "health", "bomb"])
                                self.powerups.append(Powerup(enemy.x, enemy.y, powerup_type))
                            if enemy in self.enemies:
                                self.enemies.remove(enemy)
                        break
                
                # Check collision with boss
                if self.boss and self.boss.active:
                    dx = bullet.x - self.boss.x
                    dy = bullet.y - self.boss.y
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist < bullet.size + self.boss.size:
                        self.boss.health -= bullet.damage
                        if bullet in self.player_bullets:
                            self.player_bullets.remove(bullet)
                        if self.boss.health <= 0:
                            self.player.score += 5000
                            self.create_explosion(self.boss.x, self.boss.y, PURPLE, 50)
                            self.victory = True
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(self.player)
            if not enemy.active:
                self.enemies.remove(enemy)
                continue
            
            # Enemy shooting
            bullets = enemy.shoot(self.player)
            self.enemy_bullets.extend(bullets)
            
            # Check collision with player
            dx = enemy.x - self.player.x
            dy = enemy.y - self.player.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < enemy.size + self.player.hitbox_size:
                if self.player.take_damage():
                    self.create_explosion(self.player.x, self.player.y, RED)
                    if self.player.lives <= 0:
                        self.game_over = True
                enemy.health = 0
        
        # Update boss
        if self.boss and self.boss.active:
            self.boss.update(self.player)
            bullets = self.boss.shoot(self.player)
            self.enemy_bullets.extend(bullets)
            
            # Check collision with player
            dx = self.boss.x - self.player.x
            dy = self.boss.y - self.player.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < self.boss.size + self.player.hitbox_size:
                if self.player.take_damage():
                    self.create_explosion(self.player.x, self.player.y, RED)
                    if self.player.lives <= 0:
                        self.game_over = True
        
        # Update enemy bullets (slower when time slow is active)
        if not self.player.time_slow:
            for bullet in self.enemy_bullets[:]:
                bullet.update()
                if not bullet.active:
                    self.enemy_bullets.remove(bullet)
                    continue
                
                # Check collision with player hitbox
                dx = bullet.x - self.player.x
                dy = bullet.y - self.player.y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < bullet.size + self.player.hitbox_size:
                    if self.player.take_damage():
                        self.create_explosion(self.player.x, self.player.y, RED)
                        if self.player.lives <= 0:
                            self.game_over = True
                    if bullet in self.enemy_bullets:
                        self.enemy_bullets.remove(bullet)
        else:
            # Slow down enemy bullets
            if self.enemy_spawn_timer % 2 == 0:  # Update every other frame
                for bullet in self.enemy_bullets[:]:
                    bullet.update()
                    if not bullet.active:
                        self.enemy_bullets.remove(bullet)
                        continue
                    
                    # Check collision with player hitbox
                    dx = bullet.x - self.player.x
                    dy = bullet.y - self.player.y
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist < bullet.size + self.player.hitbox_size:
                        if self.player.take_damage():
                            self.create_explosion(self.player.x, self.player.y, RED)
                            if self.player.lives <= 0:
                                self.game_over = True
                        if bullet in self.enemy_bullets:
                            self.enemy_bullets.remove(bullet)
        
        # Update powerups
        for powerup in self.powerups[:]:
            powerup.update()
            if not powerup.active:
                self.powerups.remove(powerup)
                continue
            
            # Check collision with player
            dx = powerup.x - self.player.x
            dy = powerup.y - self.player.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < powerup.size + self.player.size:
                if powerup.type == "power":
                    self.player.power = min(self.player.max_power, self.player.power + 1)
                elif powerup.type == "health":
                    self.player.lives = min(5, self.player.lives + 1)
                elif powerup.type == "bomb":
                    self.player.bomb_count = min(9, self.player.bomb_count + 1)
                self.create_explosion(powerup.x, powerup.y, powerup.color)
                self.powerups.remove(powerup)
        
        # Update particles
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)
        
        # Wave progression
        if len(self.enemies) == 0 and self.enemy_spawn_timer > 60 and self.wave < 5:
            self.wave += 1
    
    def draw(self):
        # Draw background
        self.screen.fill(BLACK)
        
        # Draw stars
        for x, y in self.stars:
            pygame.draw.circle(self.screen, WHITE, (x, y), 1)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw powerups
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw boss
        if self.boss and self.boss.active:
            self.boss.draw(self.screen)
        
        # Draw bullets
        for bullet in self.player_bullets:
            bullet.draw(self.screen)
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)
        
        # Draw player
        keys = pygame.key.get_pressed()
        self.player.draw(self.screen, keys[pygame.K_LSHIFT])
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.player.score}", True, WHITE)
        wave_text = self.font.render(f"Wave: {self.wave}", True, WHITE)
        power_text = self.font.render(f"Power: {self.player.power}/{self.player.max_power}", True, YELLOW)
        bombs_text = self.font.render(f"Bombs: ∞", True, CYAN)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(wave_text, (10, 45))
        self.screen.blit(power_text, (10, 80))
        self.screen.blit(bombs_text, (10, 115))
        
        # Auto-aim status
        aim_status = "ON" if self.player.auto_aim else "OFF"
        aim_color = YELLOW if self.player.auto_aim else GRAY
        aim_text = self.font.render(f"Auto-Aim: {aim_status}", True, aim_color)
        self.screen.blit(aim_text, (10, 150))
        
        # Hack energy bar
        energy_bar_width = 150
        energy_bar_height = 12
        energy_ratio = self.player.hack_energy / self.player.max_hack_energy
        pygame.draw.rect(self.screen, DARK_GRAY, (10, 185, energy_bar_width, energy_bar_height))
        pygame.draw.rect(self.screen, NEON_GREEN, (10, 185, energy_bar_width * energy_ratio, energy_bar_height))
        pygame.draw.rect(self.screen, WHITE, (10, 185, energy_bar_width, energy_bar_height), 2)
        
        energy_text = pygame.font.Font(None, 24).render(f"Hack Energy: {int(self.player.hack_energy)}", True, NEON_GREEN)
        self.screen.blit(energy_text, (165, 186))
        
        # Lives
        for i in range(self.player.lives):
            life_x = 10 + i * 25
            life_y = 210
            # Hacker diamond shape for lives
            points = [(life_x + 10, life_y), (life_x + 18, life_y + 8), (life_x + 10, life_y + 16), (life_x + 2, life_y + 8)]
            pygame.draw.polygon(self.screen, PURPLE, points)
        
        # Hack ability status
        hack_abilities = []
        if self.player.rapid_fire:
            hack_abilities.append("RAPID FIRE")
        if self.player.shield_active:
            hack_abilities.append("SHIELD")
        if self.player.time_slow:
            hack_abilities.append("TIME SLOW")
        
        for i, ability in enumerate(hack_abilities):
            text = pygame.font.Font(None, 28).render(ability, True, NEON_GREEN)
            self.screen.blit(text, (10, 240 + i * 25))
        
        # Controls
        controls = [
            "WASD/Arrows - Move",
            "SHIFT - Focus (slow)",
            "Z/Space - Shoot",
            "X - Bomb",
            "C - Toggle Auto-Aim",
            "",
            "HACKER ABILITIES:",
            "1 - Rapid Fire (30E)",
            "2 - Shield (40E)",
            "3 - Time Slow (50E)"
        ]
        
        y_offset = 0
        for i, control in enumerate(controls):
            if control == "":
                y_offset -= 20
            else:
                color = NEON_GREEN if "HACKER" in control or control.startswith(("1", "2", "3")) else WHITE
                text = pygame.font.Font(None, 20).render(control, True, color)
                self.screen.blit(text, (WINDOW_WIDTH - 200, 10 + i * 20 + y_offset))
        
        # Game over / Victory
        if self.game_over:
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            restart_text = self.font.render("Press R to Restart", True, WHITE)
            score_text = self.font.render(f"Final Score: {self.player.score}", True, WHITE)
            
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 20))
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 60))
            
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)
            self.screen.blit(score_text, score_rect)
        
        if self.victory:
            victory_text = self.big_font.render("VICTORY!", True, YELLOW)
            restart_text = self.font.render("Press R to Play Again", True, WHITE)
            score_text = self.font.render(f"Final Score: {self.player.score}", True, WHITE)
            
            text_rect = victory_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 20))
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 60))
            
            self.screen.blit(victory_text, text_rect)
            self.screen.blit(restart_text, restart_rect)
            self.screen.blit(score_text, score_rect)
        
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
    game = BulletStormGame()
    game.run()

if __name__ == "__main__":
    main()
