import sys
sys.path.insert(0, '/home/eliel/tekoaly')

import pygame
pygame.init()

from tower_defense_supreme import Game, Tower, LEVELS
import math

def find_tower_spots(path, num_spots=25):
    spots = []
    
    def is_valid(tx, ty):
        if tx < 25 or tx > 975 or ty < 25 or ty > 545:
            return False
        for ppx, ppy in path:
            if math.sqrt((tx-ppx)**2 + (ty-ppy)**2) < 30:
                return False
        for sx, sy in spots:
            if math.sqrt((tx-sx)**2 + (ty-sy)**2) < 35:
                return False
        return True
    
    path_length = 0
    segments = []
    for i in range(len(path) - 1):
        dx = path[i+1][0] - path[i][0]
        dy = path[i+1][1] - path[i][1]
        seg_len = math.sqrt(dx*dx + dy*dy)
        segments.append((path[i], path[i+1], seg_len))
        path_length += seg_len
    
    spacing = path_length / (num_spots + 1)
    next_spot_dist = spacing
    seg_idx = 0
    seg_dist = 0
    
    for _ in range(num_spots):
        while seg_idx < len(segments) and seg_dist + segments[seg_idx][2] < next_spot_dist:
            seg_dist += segments[seg_idx][2]
            seg_idx += 1
        if seg_idx >= len(segments):
            break
        
        remaining = next_spot_dist - seg_dist
        seg_len = segments[seg_idx][2]
        t = remaining / seg_len if seg_len > 0 else 0
        t = min(1.0, max(0.0, t))
        px = segments[seg_idx][0][0] + t * (segments[seg_idx][1][0] - segments[seg_idx][0][0])
        py = segments[seg_idx][0][1] + t * (segments[seg_idx][1][1] - segments[seg_idx][0][1])
        
        offsets = [(45, 0), (-45, 0), (0, 45), (0, -45), (45, 45), (-45, -45),
                   (50, 0), (-50, 0), (0, 50), (0, -50), (55, 0), (-55, 0),
                   (0, 55), (0, -55), (45, 30), (-45, 30), (45, -30), (-45, -30),
                   (30, 45), (-30, 45), (30, -45), (-30, -45)]
        for ox, oy in offsets:
            tx, ty = px + ox, py + oy
            if is_valid(tx, ty):
                spots.append((tx, ty))
                break
        
        next_spot_dist += spacing
    
    if len(spots) < 15:
        for gy in range(50, 550, 25):
            for gx in range(50, 970, 25):
                if is_valid(gx, gy):
                    spots.append((gx, gy))
                    if len(spots) >= 25:
                        break
            if len(spots) >= 25:
                break
    
    return spots

def simulate_level(level_idx, verbose=False):
    game = Game()
    game.load_level(level_idx)
    
    spots = find_tower_spots(game.path, num_spots=20)
    
    spot_idx = 0
    placed = 0
    max_frames = 60 * 60 * 30
    
    while game.state == "playing" and game.frame_count < max_frames:
        game.frame_count += 1
        
        if game.wave_enemies_spawned < game.enemies_in_wave:
            game.spawn_timer += 1
            if game.spawn_timer >= game.spawn_delay:
                game.spawn_enemy()
                game.spawn_timer = 0
        
        for tower in game.towers:
            tower.update(game.enemies, game.projectiles, game.frame_count)
        
        game.projectiles = [p for p in game.projectiles if p.update()]
        
        for projectile in game.projectiles[:]:
            for enemy in game.enemies:
                if enemy.health > 0 and projectile.check_collision(enemy):
                    particles = enemy.take_damage(projectile.damage)
                    game.particles.extend(particles)
                    if enemy.health <= 0:
                        game.money += enemy.reward
                        game.score += enemy.reward * 10
                        game.wave_enemies_killed += 1
                    if projectile in game.projectiles:
                        game.projectiles.remove(projectile)
                    break
        
        for enemy in game.enemies[:]:
            if enemy.health <= 0:
                if enemy in game.enemies:
                    game.enemies.remove(enemy)
            elif not enemy.update():
                game.lives -= 1
                if enemy in game.enemies:
                    game.enemies.remove(enemy)
                if game.lives <= 0:
                    game.state = "game_over"
        
        game.particles = [p for p in game.particles if p.life > 0]
        for p in game.particles:
            p.update()
        
        if (game.wave_enemies_spawned >= game.enemies_in_wave and
            len([e for e in game.enemies if e.health > 0]) == 0):
            if game.wave >= game.total_waves:
                game.state = "victory"
            else:
                game.next_wave()
        
        cost_map = {"basic": 50, "rapid": 70, "heavy": 120, "laser": 150}
        while spot_idx < len(spots):
            if game.money >= 120 and len(game.towers) >= 4 and len([t for t in game.towers if t.tower_type == "heavy"]) < 3:
                ttype = "heavy"
            elif game.money >= 50:
                ttype = "basic"
            else:
                break
            cost = cost_map[ttype]
            if game.money < cost:
                break
            tx, ty = spots[spot_idx]
            can_place = True
            for ppx, ppy in game.path:
                if math.sqrt((tx-ppx)**2 + (ty-ppy)**2) < 30:
                    can_place = False
                    break
            for t in game.towers:
                if math.sqrt((t.x-tx)**2 + (t.y-ty)**2) < 35:
                    can_place = False
                    break
            if can_place:
                game.towers.append(Tower(tx, ty, ttype))
                game.money -= cost
                spot_idx += 1
                placed += 1
            else:
                spot_idx += 1
        
        if len(game.towers) >= 5 and game.money >= 50:
            for tower in game.towers:
                if tower.level < 3 and game.money >= tower.upgrade_cost:
                    tower.upgrade()
                    game.money -= tower.upgrade_cost
                    break
    
    return game.state, game.wave, game.lives, game.money, placed, len(game.towers)

print(f"{'#':>3} {'Name':20s} {'Tier':>4} {'Waves':>5} {'Result':10s} {'Lives':>5} {'Towers':>6} {'Money':>6}")
print("-" * 75)

results = {"victory": 0, "game_over": 0}
impossible_levels = []

for i in range(len(LEVELS)):
    level = LEVELS[i]
    state, wave, lives, money, placed, ntowers = simulate_level(i)
    results[state] += 1
    status = "WIN" if state == "victory" else f"FAIL w{wave}"
    if state != "victory":
        impossible_levels.append(i+1)
    tier_names = {1:"Easy",2:"Med",3:"Hard",4:"VHard",5:"Insane",6:"Legend",7:"Mythic",8:"Impos"}
    tn = tier_names.get(level["tier"], "?")
    print(f"{i+1:3d} {level['name']:20s} {tn:>7s} {level['waves']:5d} {status:10s} {lives:5d} {ntowers:6d} {money:6d}")

print("-" * 75)
print(f"Victory: {results['victory']}/{len(LEVELS)}, Failed: {results['game_over']}/{len(LEVELS)}")
if impossible_levels:
    print(f"Impossible levels: {impossible_levels}")
