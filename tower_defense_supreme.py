import pygame
import random
import math
import sys

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (200, 200, 200)
DARK_GREEN = (0, 150, 0)
GOLD = (255, 215, 0)
MAGENTA = (255, 0, 255)
PINK = (255, 100, 180)
BROWN = (139, 69, 19)
DARK_RED = (139, 0, 0)

LEVELS = [
    # TIER 1: EASY (levels 1-10)
    {"name": "Green Valley", "tier": 1, "waves": 3, "start_money": 100, "lives": 10, "path": [(50, 100), (200, 100), (200, 300), (400, 300), (400, 100), (600, 100), (600, 300), (800, 300), (800, 100), (950, 100)]},
    {"name": "Zigzag Ridge", "tier": 1, "waves": 3, "start_money": 100, "lives": 10, "path": [(50, 150), (300, 150), (300, 300), (500, 300), (500, 150), (700, 150), (700, 400), (900, 400), (900, 150), (950, 150)]},
    {"name": "Winding Pass", "tier": 1, "waves": 3, "start_money": 100, "lives": 10, "path": [(50, 250), (200, 250), (200, 80), (400, 80), (400, 400), (600, 400), (600, 150), (800, 150), (800, 350), (950, 350)]},
    {"name": "Serpent Tail", "tier": 1, "waves": 3, "start_money": 100, "lives": 10, "path": [(50, 80), (350, 80), (350, 200), (150, 200), (150, 400), (400, 400), (400, 300), (600, 300), (600, 500), (800, 500), (800, 150), (950, 150)]},
    {"name": "The Maze", "tier": 1, "waves": 4, "start_money": 110, "lives": 10, "path": [(50, 80), (200, 80), (200, 200), (400, 200), (400, 80), (600, 80), (600, 350), (400, 350), (400, 500), (600, 500), (600, 350), (800, 350), (800, 200), (950, 200)]},
    {"name": "Shortcut", "tier": 1, "waves": 3, "start_money": 100, "lives": 10, "path": [(50, 200), (250, 200), (250, 80), (450, 80), (450, 350), (650, 350), (650, 100), (850, 100), (850, 400), (950, 400)]},
    {"name": "Easy Street", "tier": 1, "waves": 3, "start_money": 100, "lives": 10, "path": [(50, 100), (150, 100), (150, 300), (350, 300), (350, 100), (550, 100), (550, 400), (750, 400), (750, 200), (950, 200)]},
    {"name": "Gentle Slope", "tier": 1, "waves": 3, "start_money": 100, "lives": 10, "path": [(50, 80), (200, 80), (200, 250), (400, 250), (400, 100), (600, 100), (600, 400), (800, 400), (800, 200), (950, 200)]},
    {"name": "River Run", "tier": 1, "waves": 3, "start_money": 100, "lives": 10, "path": [(50, 300), (200, 300), (200, 100), (400, 100), (400, 400), (600, 400), (600, 150), (800, 150), (800, 350), (950, 350)]},
    {"name": "First Blood", "tier": 1, "waves": 3, "start_money": 100, "lives": 10, "path": [(50, 100), (300, 100), (300, 300), (500, 300), (500, 100), (700, 100), (700, 400), (900, 400), (900, 200), (950, 200)]},

    # TIER 2: MEDIUM (levels 11-20)
    {"name": "Double Back", "tier": 2, "waves": 4, "start_money": 90, "lives": 8, "path": [(50, 80), (500, 80), (500, 300), (200, 300), (200, 500), (500, 500), (500, 300), (800, 300), (800, 100), (950, 100)]},
    {"name": "Crossroads", "tier": 2, "waves": 4, "start_money": 90, "lives": 8, "path": [(50, 250), (250, 250), (250, 80), (500, 80), (500, 400), (700, 400), (700, 100), (950, 100)]},
    {"name": "Spiral", "tier": 2, "waves": 4, "start_money": 100, "lives": 10, "path": [(50, 350), (300, 350), (300, 80), (550, 80), (550, 350), (400, 350), (400, 500), (700, 500), (700, 200), (950, 200)]},
    {"name": "Uphill Battle", "tier": 2, "waves": 4, "start_money": 90, "lives": 8, "path": [(50, 500), (150, 500), (150, 350), (350, 350), (350, 150), (500, 150), (500, 350), (650, 350), (650, 150), (800, 150), (800, 350), (950, 350)]},
    {"name": "Loop de Loop", "tier": 2, "waves": 4, "start_money": 90, "lives": 8, "path": [(50, 80), (400, 80), (400, 250), (150, 250), (150, 400), (400, 400), (400, 250), (650, 250), (650, 400), (900, 400), (900, 200), (950, 200)]},
    {"name": "Detour", "tier": 2, "waves": 4, "start_money": 90, "lives": 8, "path": [(50, 100), (300, 100), (300, 400), (100, 400), (100, 550), (400, 550), (400, 300), (600, 300), (600, 100), (800, 100), (800, 400), (950, 400)]},
    {"name": "Sidetrack", "tier": 2, "waves": 4, "start_money": 90, "lives": 8, "path": [(50, 80), (200, 80), (200, 350), (400, 350), (400, 150), (600, 150), (600, 500), (800, 500), (800, 250), (950, 250)]},
    {"name": "Wavy", "tier": 2, "waves": 4, "start_money": 90, "lives": 8, "path": [(50, 150), (250, 150), (250, 350), (450, 350), (450, 100), (650, 100), (650, 400), (850, 400), (850, 200), (950, 200)]},
    {"name": "Staircase", "tier": 2, "waves": 4, "start_money": 90, "lives": 8, "path": [(50, 100), (200, 100), (200, 300), (350, 300), (350, 100), (500, 100), (500, 350), (650, 350), (650, 100), (800, 100), (800, 400), (950, 400)]},
    {"name": "Labyrinth", "tier": 2, "waves": 4, "start_money": 90, "lives": 8, "path": [(50, 80), (250, 80), (250, 250), (100, 250), (100, 450), (350, 450), (350, 200), (550, 200), (550, 400), (750, 400), (750, 150), (950, 150)]},

    # TIER 3: HARD (levels 21-35)
    {"name": "Lightning", "tier": 3, "waves": 5, "start_money": 150, "lives": 8, "path": [(50, 80), (200, 80), (200, 500), (350, 500), (350, 150), (500, 150), (500, 450), (650, 450), (650, 100), (800, 100), (800, 400), (950, 400)]},
    {"name": "Switchback", "tier": 3, "waves": 5, "start_money": 150, "lives": 8, "path": [(50, 100), (300, 100), (300, 300), (100, 300), (100, 500), (350, 500), (350, 300), (550, 300), (550, 100), (750, 100), (750, 400), (950, 400)]},
    {"name": "The Gauntlet", "tier": 3, "waves": 5, "start_money": 150, "lives": 8, "path": [(50, 250), (200, 250), (200, 80), (400, 80), (400, 250), (250, 250), (250, 450), (450, 450), (450, 250), (600, 250), (600, 450), (800, 450), (800, 200), (950, 200)]},
    {"name": "Narrow Escape", "tier": 3, "waves": 5, "start_money": 150, "lives": 8, "path": [(50, 80), (120, 80), (120, 350), (300, 350), (300, 120), (480, 120), (480, 400), (300, 400), (300, 550), (500, 550), (500, 300), (700, 300), (700, 100), (900, 100), (900, 500), (950, 500)]},
    {"name": "Fortress", "tier": 3, "waves": 5, "start_money": 150, "lives": 8, "path": [(50, 150), (250, 150), (250, 350), (100, 350), (100, 500), (400, 500), (400, 350), (550, 350), (550, 100), (750, 100), (750, 300), (600, 300), (600, 500), (900, 500), (900, 200), (950, 200)]},
    {"name": "Snake Pit", "tier": 3, "waves": 5, "start_money": 150, "lives": 8, "path": [(50, 80), (150, 80), (150, 300), (350, 300), (350, 100), (550, 100), (550, 400), (350, 400), (350, 500), (650, 500), (650, 200), (850, 200), (850, 450), (950, 450)]},
    {"name": "Tricky Path", "tier": 3, "waves": 5, "start_money": 150, "lives": 8, "path": [(50, 100), (200, 100), (200, 400), (400, 400), (400, 150), (300, 150), (300, 300), (550, 300), (550, 100), (750, 100), (750, 400), (950, 400)]},
    {"name": "Twister", "tier": 3, "waves": 5, "start_money": 150, "lives": 8, "path": [(50, 200), (250, 200), (250, 80), (450, 80), (450, 350), (250, 350), (250, 500), (500, 500), (500, 250), (700, 250), (700, 100), (900, 100), (900, 400), (950, 400)]},
    {"name": "Zig Zag Zag", "tier": 3, "waves": 5, "start_money": 150, "lives": 8, "path": [(50, 100), (200, 100), (200, 300), (350, 300), (350, 100), (500, 100), (500, 400), (650, 400), (650, 150), (800, 150), (800, 450), (950, 450)]},
    {"name": "Corkscrew", "tier": 3, "waves": 5, "start_money": 150, "lives": 8, "path": [(50, 150), (250, 150), (250, 300), (100, 300), (100, 450), (350, 450), (350, 200), (550, 200), (550, 400), (750, 400), (750, 100), (950, 100)]},
    {"name": "Backtrack", "tier": 3, "waves": 5, "start_money": 150, "lives": 8, "path": [(50, 80), (300, 80), (300, 250), (150, 250), (150, 400), (400, 400), (400, 250), (600, 250), (600, 450), (800, 450), (800, 150), (950, 150)]},
    {"name": "Harassing", "tier": 3, "waves": 5, "start_money": 150, "lives": 8, "path": [(50, 100), (150, 100), (150, 400), (350, 400), (350, 80), (550, 80), (550, 500), (750, 500), (750, 200), (900, 200), (900, 400), (950, 400)]},
    {"name": "Mindbend", "tier": 3, "waves": 5, "start_money": 150, "lives": 8, "path": [(50, 80), (200, 80), (200, 300), (400, 300), (400, 150), (250, 150), (250, 450), (500, 450), (500, 250), (700, 250), (700, 450), (900, 450), (900, 200), (950, 200)]},
    {"name": "Fracture", "tier": 3, "waves": 5, "start_money": 150, "lives": 8, "path": [(50, 250), (200, 250), (200, 80), (400, 80), (400, 400), (600, 400), (600, 150), (800, 150), (800, 350), (900, 350), (900, 100), (950, 100)]},
    {"name": "Puzzle", "tier": 3, "waves": 6, "start_money": 160, "lives": 8, "path": [(50, 100), (100, 100), (100, 300), (300, 300), (300, 100), (500, 100), (500, 400), (300, 400), (300, 500), (600, 500), (600, 250), (800, 250), (800, 500), (950, 500)]},

    # TIER 4: VERY HARD (levels 36-45)
    {"name": "Warzone", "tier": 4, "waves": 6, "start_money": 180, "lives": 7, "path": [(50, 50), (500, 50), (500, 200), (100, 200), (100, 400), (400, 400), (400, 200), (700, 200), (700, 400), (300, 400), (300, 550), (600, 550), (600, 350), (900, 350), (900, 100), (950, 100)]},
    {"name": "Impossible", "tier": 4, "waves": 6, "start_money": 180, "lives": 7, "path": [(50, 100), (150, 100), (150, 300), (350, 300), (350, 80), (550, 80), (550, 300), (350, 300), (350, 500), (550, 500), (550, 300), (750, 300), (750, 80), (900, 80), (900, 400), (950, 400)]},
    {"name": "Nightmare", "tier": 4, "waves": 6, "start_money": 180, "lives": 7, "path": [(50, 80), (80, 80), (80, 500), (250, 500), (250, 80), (400, 80), (400, 500), (550, 500), (550, 80), (700, 80), (700, 500), (850, 500), (850, 200), (950, 200)]},
    {"name": "Chaos", "tier": 4, "waves": 6, "start_money": 180, "lives": 7, "path": [(50, 400), (200, 400), (200, 100), (350, 100), (350, 300), (150, 300), (150, 500), (450, 500), (450, 300), (650, 300), (650, 100), (800, 100), (800, 400), (950, 400)]},
    {"name": "Apocalypse", "tier": 4, "waves": 6, "start_money": 180, "lives": 7, "path": [(50, 100), (200, 100), (200, 450), (80, 450), (80, 550), (350, 550), (350, 350), (200, 350), (200, 250), (450, 250), (450, 450), (650, 450), (650, 150), (800, 150), (800, 400), (950, 400)]},
    {"name": "Death Wish", "tier": 4, "waves": 6, "start_money": 180, "lives": 7, "path": [(50, 150), (150, 150), (150, 400), (350, 400), (350, 100), (200, 100), (200, 300), (450, 300), (450, 500), (650, 500), (650, 200), (800, 200), (800, 450), (950, 450)]},
    {"name": "Madness", "tier": 4, "waves": 6, "start_money": 180, "lives": 7, "path": [(50, 80), (100, 80), (100, 350), (300, 350), (300, 150), (500, 150), (500, 450), (300, 450), (300, 550), (600, 550), (600, 250), (800, 250), (800, 500), (950, 500)]},
    {"name": "Carnage", "tier": 4, "waves": 6, "start_money": 180, "lives": 7, "path": [(50, 100), (250, 100), (250, 300), (100, 300), (100, 500), (350, 500), (350, 200), (550, 200), (550, 400), (750, 400), (750, 100), (900, 100), (900, 350), (950, 350)]},
    {"name": "Mayhem", "tier": 4, "waves": 6, "start_money": 180, "lives": 7, "path": [(50, 80), (200, 80), (200, 200), (400, 200), (400, 80), (600, 80), (600, 300), (400, 300), (400, 500), (600, 500), (600, 300), (800, 300), (800, 100), (950, 100)]},
    {"name": "Rampage", "tier": 4, "waves": 7, "start_money": 190, "lives": 7, "path": [(50, 250), (200, 250), (200, 80), (350, 80), (350, 400), (150, 400), (150, 550), (400, 550), (400, 300), (600, 300), (600, 100), (800, 100), (800, 400), (950, 400)]},

    # TIER 5: INSANE (levels 46-60)
    {"name": "Hellfire", "tier": 5, "waves": 7, "start_money": 180, "lives": 5, "path": [(50, 80), (120, 80), (120, 400), (280, 400), (280, 100), (440, 100), (440, 500), (280, 500), (280, 300), (440, 300), (440, 100), (600, 100), (600, 500), (800, 500), (800, 200), (950, 200)]},
    {"name": "Doom", "tier": 5, "waves": 7, "start_money": 180, "lives": 5, "path": [(50, 200), (180, 200), (180, 50), (350, 50), (350, 300), (180, 300), (180, 500), (350, 500), (350, 300), (550, 300), (550, 100), (720, 100), (720, 450), (550, 450), (550, 250), (900, 250), (900, 500), (950, 500)]},
    {"name": "Oblivion", "tier": 5, "waves": 7, "start_money": 180, "lives": 5, "path": [(50, 100), (100, 100), (100, 350), (250, 350), (250, 150), (400, 150), (400, 400), (250, 400), (250, 550), (450, 550), (450, 400), (600, 400), (600, 200), (750, 200), (750, 450), (600, 450), (600, 550), (850, 550), (850, 300), (950, 300)]},
    {"name": "Inferno", "tier": 5, "waves": 7, "start_money": 180, "lives": 5, "path": [(50, 80), (100, 80), (100, 500), (250, 500), (250, 100), (400, 100), (400, 350), (250, 350), (250, 200), (400, 200), (400, 500), (550, 500), (550, 100), (700, 100), (700, 400), (550, 400), (550, 550), (850, 550), (850, 200), (950, 200)]},
    {"name": "The End", "tier": 5, "waves": 8, "start_money": 190, "lives": 5, "path": [(50, 80), (80, 80), (80, 300), (250, 300), (250, 100), (400, 100), (400, 350), (250, 350), (250, 500), (400, 500), (400, 350), (550, 350), (550, 150), (700, 150), (700, 450), (550, 450), (550, 550), (750, 550), (750, 250), (900, 250), (900, 500), (950, 500)]},
    {"name": "Torment", "tier": 5, "waves": 7, "start_money": 180, "lives": 5, "path": [(50, 100), (120, 100), (120, 300), (280, 300), (280, 80), (440, 80), (440, 350), (280, 350), (280, 500), (500, 500), (500, 250), (660, 250), (660, 450), (850, 450), (850, 150), (950, 150)]},
    {"name": "Suffering", "tier": 5, "waves": 7, "start_money": 180, "lives": 5, "path": [(50, 80), (200, 80), (200, 350), (80, 350), (80, 550), (300, 550), (300, 300), (500, 300), (500, 80), (700, 80), (700, 400), (500, 400), (500, 550), (750, 550), (750, 200), (950, 200)]},
    {"name": "Despair", "tier": 5, "waves": 7, "start_money": 190, "lives": 5, "path": [(50, 150), (180, 150), (180, 350), (350, 350), (350, 100), (180, 100), (180, 250), (500, 250), (500, 450), (300, 450), (300, 550), (600, 550), (600, 300), (800, 300), (800, 100), (950, 100)]},
    {"name": "Annihilation", "tier": 5, "waves": 8, "start_money": 200, "lives": 5, "path": [(50, 80), (100, 80), (100, 400), (250, 400), (250, 100), (400, 100), (400, 500), (250, 500), (250, 300), (450, 300), (450, 100), (600, 100), (600, 400), (450, 400), (450, 550), (700, 550), (700, 250), (850, 250), (850, 500), (950, 500)]},
    {"name": "Total War", "tier": 5, "waves": 8, "start_money": 210, "lives": 5, "path": [(50, 100), (200, 100), (200, 250), (80, 250), (80, 450), (250, 450), (250, 300), (400, 300), (400, 100), (600, 100), (600, 350), (400, 350), (400, 550), (650, 550), (650, 200), (800, 200), (800, 450), (950, 450)]},

    # TIER 6: LEGENDARY (levels 61-70)
    {"name": "Armageddon", "tier": 6, "waves": 8, "start_money": 300, "lives": 5, "path": [(50, 80), (200, 80), (200, 250), (400, 250), (400, 80), (550, 80), (550, 400), (400, 400), (400, 550), (550, 550), (550, 400), (750, 400), (750, 150), (900, 150), (900, 500), (750, 500), (750, 550), (950, 550)]},
    {"name": "Judgment", "tier": 6, "waves": 8, "start_money": 250, "lives": 5, "path": [(50, 100), (80, 100), (80, 350), (220, 350), (220, 120), (380, 120), (380, 350), (220, 350), (220, 500), (380, 500), (380, 350), (550, 350), (550, 150), (720, 150), (720, 450), (550, 450), (550, 550), (850, 550), (850, 250), (950, 250)]},
    {"name": "Apotheosis", "tier": 6, "waves": 8, "start_money": 260, "lives": 5, "path": [(50, 80), (150, 80), (150, 200), (300, 200), (300, 80), (450, 80), (450, 300), (300, 300), (300, 450), (150, 450), (150, 550), (350, 550), (350, 400), (500, 400), (500, 200), (650, 200), (650, 500), (500, 500), (500, 550), (800, 550), (800, 300), (950, 300)]},
    {"name": "Godslayer", "tier": 6, "waves": 8, "start_money": 260, "lives": 5, "path": [(50, 150), (200, 150), (200, 80), (350, 80), (350, 300), (200, 300), (200, 450), (350, 450), (350, 300), (500, 300), (500, 100), (650, 100), (650, 450), (500, 450), (500, 550), (700, 550), (700, 250), (850, 250), (850, 500), (950, 500)]},
    {"name": "Eternal", "tier": 6, "waves": 9, "start_money": 280, "lives": 5, "path": [(50, 80), (100, 80), (100, 300), (200, 300), (200, 100), (350, 100), (350, 350), (200, 350), (200, 500), (350, 500), (350, 350), (500, 350), (500, 150), (650, 150), (650, 450), (500, 450), (500, 550), (650, 550), (650, 450), (800, 450), (800, 200), (950, 200)]},
    {"name": "Infinity", "tier": 6, "waves": 9, "start_money": 280, "lives": 5, "path": [(50, 100), (120, 100), (120, 350), (250, 350), (250, 150), (400, 150), (400, 400), (250, 400), (250, 550), (400, 550), (400, 400), (550, 400), (550, 200), (700, 200), (700, 500), (550, 500), (550, 550), (800, 550), (800, 300), (950, 300)]},
    {"name": "Beyond", "tier": 6, "waves": 9, "start_money": 300, "lives": 5, "path": [(50, 80), (80, 80), (80, 250), (180, 250), (180, 80), (320, 80), (320, 300), (180, 300), (180, 450), (320, 450), (320, 300), (480, 300), (480, 100), (620, 100), (620, 400), (480, 400), (480, 550), (720, 550), (720, 250), (850, 250), (850, 500), (950, 500)]},
    {"name": "Transcend", "tier": 6, "waves": 9, "start_money": 300, "lives": 5, "path": [(50, 150), (150, 150), (150, 80), (300, 80), (300, 250), (150, 250), (150, 400), (300, 400), (300, 250), (450, 250), (450, 100), (600, 100), (600, 400), (450, 400), (450, 550), (600, 550), (600, 400), (750, 400), (750, 200), (900, 200), (900, 500), (950, 500)]},
    {"name": "Omega", "tier": 6, "waves": 10, "start_money": 320, "lives": 5, "path": [(50, 80), (100, 80), (100, 300), (200, 300), (200, 100), (350, 100), (350, 350), (200, 350), (200, 500), (350, 500), (350, 350), (500, 350), (500, 150), (650, 150), (650, 450), (500, 450), (500, 550), (650, 550), (650, 450), (800, 450), (800, 200), (950, 200)]},
    {"name": "The Final Stand", "tier": 6, "waves": 10, "start_money": 350, "lives": 5, "path": [(50, 80), (80, 80), (80, 300), (200, 300), (200, 100), (350, 100), (350, 350), (200, 350), (200, 500), (350, 500), (350, 350), (500, 350), (500, 150), (650, 150), (650, 450), (500, 450), (500, 550), (650, 550), (650, 450), (800, 450), (800, 200), (950, 200)]},

    # TIER 7: MYTHIC (levels 71-85)
    {"name": "Void Walker", "tier": 7, "waves": 8, "start_money": 500, "lives": 7, "path": [(50, 80), (200, 80), (200, 500), (450, 500), (450, 80), (700, 80), (700, 500), (950, 500)]},
    {"name": "Abyss", "tier": 7, "waves": 8, "start_money": 500, "lives": 7, "path": [(50, 100), (250, 100), (250, 500), (500, 500), (500, 80), (750, 80), (750, 450), (950, 450)]},
    {"name": "Ragnarok", "tier": 7, "waves": 8, "start_money": 400, "lives": 5, "path": [(50, 150), (250, 150), (250, 80), (450, 80), (450, 350), (250, 350), (250, 500), (500, 500), (500, 250), (700, 250), (700, 80), (850, 80), (850, 400), (700, 400), (700, 550), (950, 550)]},
    {"name": "Calamity", "tier": 7, "waves": 9, "start_money": 370, "lives": 5, "path": [(50, 80), (100, 80), (100, 300), (250, 300), (250, 100), (400, 100), (400, 400), (250, 400), (250, 550), (450, 550), (450, 300), (600, 300), (600, 100), (750, 100), (750, 450), (600, 450), (600, 550), (850, 550), (850, 250), (950, 250)]},
    {"name": "Devastation", "tier": 7, "waves": 9, "start_money": 420, "lives": 5, "path": [(50, 100), (200, 100), (200, 350), (400, 350), (400, 80), (600, 80), (600, 450), (400, 450), (400, 550), (600, 550), (600, 250), (800, 250), (800, 80), (950, 80)]},
    {"name": "Cataclysm", "tier": 7, "waves": 9, "start_money": 380, "lives": 5, "path": [(50, 80), (150, 80), (150, 250), (300, 250), (300, 80), (450, 80), (450, 350), (300, 350), (300, 500), (150, 500), (150, 550), (400, 550), (400, 400), (600, 400), (600, 150), (750, 150), (750, 500), (900, 500), (900, 250), (950, 250)]},
    {"name": "Extinction", "tier": 7, "waves": 10, "start_money": 400, "lives": 5, "path": [(50, 80), (80, 80), (80, 250), (200, 250), (200, 80), (350, 80), (350, 400), (200, 400), (200, 550), (400, 550), (400, 300), (550, 300), (550, 80), (700, 80), (700, 450), (550, 450), (550, 550), (800, 550), (800, 200), (950, 200)]},
    {"name": "Reckoning", "tier": 7, "waves": 10, "start_money": 420, "lives": 5, "path": [(50, 150), (150, 150), (150, 80), (300, 80), (300, 350), (150, 350), (150, 500), (350, 500), (350, 250), (500, 250), (500, 80), (650, 80), (650, 400), (500, 400), (500, 550), (700, 550), (700, 300), (850, 300), (850, 500), (950, 500)]},

    # TIER 8: IMPOSSIBLE (levels 86-100)
    {"name": "Nether", "tier": 8, "waves": 9, "start_money": 700, "lives": 8, "path": [(50, 80), (250, 80), (250, 500), (500, 500), (500, 80), (750, 80), (750, 500), (950, 500)]},
    {"name": "Obliteration", "tier": 8, "waves": 9, "start_money": 700, "lives": 8, "path": [(50, 80), (250, 80), (250, 500), (500, 500), (500, 100), (750, 100), (750, 500), (950, 500)]},
    {"name": "Purgatory", "tier": 8, "waves": 9, "start_money": 700, "lives": 8, "path": [(50, 80), (250, 80), (250, 500), (500, 500), (500, 250), (750, 250), (750, 500), (950, 500)]},
    {"name": "Condemnation", "tier": 8, "waves": 10, "start_money": 720, "lives": 8, "path": [(50, 80), (250, 80), (250, 500), (500, 500), (500, 80), (250, 80), (250, 550), (550, 550), (550, 300), (750, 300), (750, 80), (950, 80)]},
    {"name": "Ruination", "tier": 8, "waves": 10, "start_money": 720, "lives": 8, "path": [(50, 100), (300, 100), (300, 450), (550, 450), (550, 80), (800, 80), (800, 500), (950, 500)]},
    {"name": "Abaddon", "tier": 8, "waves": 10, "start_money": 650, "lives": 7, "path": [(50, 200), (250, 200), (250, 80), (500, 80), (500, 400), (250, 400), (250, 550), (550, 550), (550, 250), (750, 250), (750, 80), (950, 80)]},
    {"name": "Behemoth", "tier": 8, "waves": 10, "start_money": 650, "lives": 7, "path": [(50, 80), (250, 80), (250, 350), (500, 350), (500, 80), (750, 80), (750, 400), (500, 400), (500, 550), (750, 550), (750, 250), (950, 250)]},
    {"name": "Leviathan", "tier": 8, "waves": 10, "start_money": 770, "lives": 8, "path": [(50, 100), (250, 100), (250, 400), (500, 400), (500, 80), (750, 80), (750, 500), (950, 500)]},
    {"name": "True End", "tier": 8, "waves": 12, "start_money": 700, "lives": 7, "path": [(50, 80), (250, 80), (250, 350), (500, 350), (500, 80), (750, 80), (750, 400), (500, 400), (500, 550), (750, 550), (750, 250), (950, 250)]},
]

class Particle:
    def __init__(self, x, y, color, vx=0, vy=0, life=60):
        self.x = x
        self.y = y
        self.vx = vx + random.uniform(-2, 2)
        self.vy = vy + random.uniform(-3, 1)
        self.color = color
        self.life = life
        self.max_life = life
        self.size = random.uniform(1, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.15
        self.vx *= 0.98
        self.life -= 1

    def draw(self, screen):
        if self.life > 0:
            alpha = self.life / self.max_life
            size = max(1, int(self.size * alpha))
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

class Tower:
    def __init__(self, x, y, tower_type="basic"):
        self.x = x
        self.y = y
        self.tower_type = tower_type
        self.level = 1
        self.range = 80
        self.damage = 10
        self.fire_rate = 60
        self.last_shot = 0
        self.target = None
        self.cost = 50
        self.upgrade_cost = 30
        self.selected = False

        if tower_type == "basic":
            self.color = BLUE
            self.range = 80
            self.damage = 15
            self.fire_rate = 45
        elif tower_type == "rapid":
            self.color = GREEN
            self.range = 60
            self.damage = 8
            self.fire_rate = 20
            self.cost = 70
        elif tower_type == "heavy":
            self.color = RED
            self.range = 100
            self.damage = 30
            self.fire_rate = 90
            self.cost = 120
        elif tower_type == "laser":
            self.color = PURPLE
            self.range = 120
            self.damage = 25
            self.fire_rate = 30
            self.cost = 150

    def find_target(self, enemies):
        closest = None
        closest_dist = float('inf')
        for enemy in enemies:
            if enemy.health <= 0:
                continue
            dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if dist <= self.range and dist < closest_dist:
                closest = enemy
                closest_dist = dist
        return closest

    def update(self, enemies, projectiles, frame_count):
        self.target = self.find_target(enemies)
        if self.target and frame_count - self.last_shot >= self.fire_rate:
            self.shoot(projectiles)
            self.last_shot = frame_count

    def shoot(self, projectiles):
        if not self.target:
            return
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 0:
            dx /= dist
            dy /= dist
            speed = 8
            projectiles.append(Projectile(self.x, self.y, dx * speed, dy * speed, self.damage, self.tower_type))

    def upgrade(self):
        if self.level < 5:
            self.level += 1
            self.damage += 5
            self.range += 10
            self.fire_rate = max(10, self.fire_rate - 5)
            self.upgrade_cost = int(self.upgrade_cost * 1.5)
            return True
        return False

    def draw(self, screen):
        if self.selected:
            pygame.draw.circle(screen, (255, 255, 255, 50), (int(self.x), int(self.y)), self.range, 1)
        pygame.draw.circle(screen, DARK_GRAY, (int(self.x), int(self.y)), 18)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 15)
        for i in range(self.level):
            angle = i * (2 * math.pi / 5)
            px = self.x + math.cos(angle) * 10
            py = self.y + math.sin(angle) * 10
            pygame.draw.circle(screen, GOLD, (int(px), int(py)), 2)
        if self.target and self.target.health > 0:
            pygame.draw.line(screen, self.color, (self.x, self.y), (self.target.x, self.target.y), 2)

class Projectile:
    def __init__(self, x, y, vx, vy, damage, projectile_type="basic"):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.damage = damage
        self.projectile_type = projectile_type
        self.life = 120
        if projectile_type == "basic":
            self.color = CYAN
            self.size = 3
        elif projectile_type == "rapid":
            self.color = GREEN
            self.size = 2
        elif projectile_type == "heavy":
            self.color = RED
            self.size = 5
        elif projectile_type == "laser":
            self.color = PURPLE
            self.size = 4

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        return self.life > 0 and 0 <= self.x <= WINDOW_WIDTH and 0 <= self.y <= WINDOW_HEIGHT

    def check_collision(self, enemy):
        dist = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
        return dist < 12

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (*self.color, 100), (int(self.x), int(self.y)), self.size + 2)

class Enemy:
    def __init__(self, path, enemy_type="basic", tier=1):
        self.path = path
        self.path_index = 0
        self.x = path[0][0]
        self.y = path[0][1]
        self.enemy_type = enemy_type
        self.speed = 1.5
        self.max_health = 30
        self.health = self.max_health
        self.reward = 10
        self.size = 8
        self.armor = 0
        self.split = False

        tier_mult = 1 + (tier - 1) * 0.25

        if enemy_type == "basic":
            self.color = RED
            self.speed = 2
            self.max_health = int(25 * tier_mult)
            self.reward = 10
        elif enemy_type == "fast":
            self.color = YELLOW
            self.speed = 3.5
            self.max_health = int(15 * tier_mult)
            self.reward = 15
            self.size = 6
        elif enemy_type == "tank":
            self.color = DARK_GRAY
            self.speed = 1
            self.max_health = int(80 * tier_mult)
            self.reward = 25
            self.size = 12
        elif enemy_type == "flying":
            self.color = CYAN
            self.speed = 2.5
            self.max_health = int(20 * tier_mult)
            self.reward = 20
        elif enemy_type == "armored":
            self.color = BROWN
            self.speed = 1.5
            self.max_health = int(40 * tier_mult)
            self.reward = 20
            self.size = 10
            self.armor = 3
        elif enemy_type == "healer":
            self.color = PINK
            self.speed = 2.0
            self.max_health = int(30 * tier_mult)
            self.reward = 25
            self.size = 9
            self.heal_timer = 0
        elif enemy_type == "giant":
            self.color = DARK_RED
            self.speed = 0.8
            self.max_health = int(200 * tier_mult)
            self.reward = 60
            self.size = 18
            self.armor = 2
        elif enemy_type == "splitter":
            self.color = MAGENTA
            self.speed = 2.2
            self.max_health = int(60 * tier_mult)
            self.reward = 30
            self.size = 11
            self.split = True

        self.health = self.max_health

    def update(self):
        if self.path_index >= len(self.path) - 1:
            return False
        current = self.path[self.path_index]
        next_point = self.path[self.path_index + 1]
        dx = next_point[0] - current[0]
        dy = next_point[1] - current[1]
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 0:
            dx = (dx / dist) * self.speed
            dy = (dy / dist) * self.speed
            self.x += dx
            self.y += dy
            if math.sqrt((self.x - next_point[0])**2 + (self.y - next_point[1])**2) < 5:
                self.path_index += 1
        if hasattr(self, 'heal_timer'):
            self.heal_timer += 1
        return True

    def take_damage(self, damage):
        if self.armor > 0:
            damage = max(1, damage - self.armor * 2)
        self.health -= damage
        particles = []
        if self.health <= 0:
            for _ in range(8):
                particles.append(Particle(self.x, self.y, self.color,
                    random.uniform(-3, 3), random.uniform(-4, 2), 45))
        return particles

    def draw(self, screen):
        if self.health <= 0:
            return
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.size + 1)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        bar_width = 20
        bar_height = 4
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.size - 8
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        health_width = int(bar_width * (self.health / self.max_health))
        hp_color = GREEN if self.health > self.max_health * 0.5 else YELLOW if self.health > self.max_health * 0.25 else RED
        pygame.draw.rect(screen, hp_color, (bar_x, bar_y, health_width, bar_height))

        ticks = pygame.time.get_ticks()
        if self.enemy_type == "flying":
            wing_offset = math.sin(ticks * 0.01) * 3
            pygame.draw.circle(screen, WHITE, (int(self.x - 8), int(self.y + wing_offset)), 3)
            pygame.draw.circle(screen, WHITE, (int(self.x + 8), int(self.y + wing_offset)), 3)
        elif self.enemy_type == "armored":
            pygame.draw.circle(screen, GRAY, (int(self.x), int(self.y)), self.size + 1, 2)
        elif self.enemy_type == "healer":
            cs = self.size // 2
            pygame.draw.line(screen, WHITE, (self.x - cs, self.y), (self.x + cs, self.y), 2)
            pygame.draw.line(screen, WHITE, (self.x, self.y - cs), (self.x, self.y + cs), 2)
        elif self.enemy_type == "giant":
            pulse = int(math.sin(ticks * 0.005) * 2)
            pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.size + pulse, 2)
        elif self.enemy_type == "splitter":
            pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.size + 1, 1)
            for i in range(3):
                a = ticks * 0.003 + i * 2.09
                px = self.x + math.cos(a) * 6
                py = self.y + math.sin(a) * 6
                pygame.draw.circle(screen, WHITE, (int(px), int(py)), 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tower Defense Supreme")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.tiny_font = pygame.font.Font(None, 18)

        self.state = "level_select"
        self.money = 100
        self.lives = 10
        self.score = 0
        self.wave = 1
        self.level = 0
        self.total_waves = 3
        self.enemies_in_wave = 5
        self.wave_enemies_spawned = 0
        self.wave_enemies_killed = 0
        self.spawn_timer = 0
        self.spawn_delay = 120

        self.towers = []
        self.enemies = []
        self.projectiles = []
        self.particles = []
        self.path = []

        self.selected_tower = None
        self.placing_tower = None
        self.level_page = 0
        self.running = True
        self.frame_count = 0

    def spawn_enemy(self):
        if self.wave_enemies_spawned >= self.enemies_in_wave:
            return
        tier = LEVELS[self.level]["tier"]
        enemy_types = ["basic"]
        if self.wave >= 2:
            enemy_types.append("fast")
        if self.wave >= 3:
            enemy_types.append("tank")
        if self.wave >= 4:
            enemy_types.append("flying")
        if tier >= 3 and self.wave >= 3:
            enemy_types.append("armored")
        if tier >= 4 and self.wave >= 4:
            enemy_types.append("healer")
        if tier >= 4 and self.wave >= 5:
            enemy_types.append("splitter")
        if tier >= 3 and self.wave >= 6:
            enemy_types.append("giant")
        if tier >= 7:
            enemy_types.extend(["armored", "giant"])
            if self.wave >= 5:
                enemy_types.extend(["splitter", "healer"])
        if tier >= 8:
            enemy_types.extend(["giant", "giant", "splitter"])
            if self.wave >= 3:
                enemy_types.extend(["armored", "healer"])
        enemy_type = random.choice(enemy_types)
        self.enemies.append(Enemy(self.path, enemy_type, tier))
        self.wave_enemies_spawned += 1

    def load_level(self, level_idx):
        self.level = level_idx
        level = LEVELS[level_idx]
        self.path = level["path"]
        self.total_waves = level["waves"]
        self.wave = 1
        self.money = max(50, level["start_money"])
        self.lives = level["lives"]
        self.score = 0
        self.towers.clear()
        self.enemies.clear()
        self.projectiles.clear()
        self.particles.clear()
        self.selected_tower = None
        self.placing_tower = None
        self.enemies_in_wave = 5
        self.wave_enemies_spawned = 0
        self.wave_enemies_killed = 0
        self.spawn_timer = 0
        self.spawn_delay = 120
        self.frame_count = 0
        self.state = "playing"

    def next_wave(self):
        self.wave += 1
        tier = LEVELS[self.level]["tier"]
        self.enemies_in_wave = min(25 + tier * 3, 5 + self.wave * 2 + tier * 2)
        self.wave_enemies_spawned = 0
        self.wave_enemies_killed = 0
        self.spawn_delay = max(15, 110 - self.wave * 4 - tier * 5)
        self.money += 50 + tier * 10

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and self.state == "playing":
                    self.state = "paused"
                elif event.key == pygame.K_SPACE and self.state == "paused":
                    self.state = "playing"
                elif event.key == pygame.K_1:
                    self.placing_tower = "basic"
                elif event.key == pygame.K_2:
                    self.placing_tower = "rapid"
                elif event.key == pygame.K_3:
                    self.placing_tower = "heavy"
                elif event.key == pygame.K_4:
                    self.placing_tower = "laser"
                elif event.key == pygame.K_r:
                    self.state = "level_select"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    self.handle_click(mx, my)
                elif event.button == 3:
                    self.placing_tower = None
                    self.selected_tower = None

    def handle_click(self, x, y):
        if self.state == "level_select":
            page = self.level_page
            lpp = 12
            start = page * lpp
            end = min(start + lpp, len(LEVELS))
            for i in range(start, end):
                li = i - start
                bx = 60 + (li % 4) * WINDOW_WIDTH // 4
                by = 160 + (li // 4) * 110
                if bx <= x <= bx + WINDOW_WIDTH // 4 - 20 and by <= y <= by + 80:
                    self.load_level(i)
                    return
            if page > 0 and 10 <= x <= 110 and WINDOW_HEIGHT - 50 <= y <= WINDOW_HEIGHT - 20:
                self.level_page -= 1
            if end < len(LEVELS) and WINDOW_WIDTH - 120 <= x <= WINDOW_WIDTH - 10 and WINDOW_HEIGHT - 50 <= y <= WINDOW_HEIGHT - 20:
                self.level_page += 1
            return

        clicked_tower = None
        for tower in self.towers:
            if math.sqrt((tower.x - x)**2 + (tower.y - y)**2) < 20:
                clicked_tower = tower
                break
        if clicked_tower:
            self.selected_tower = clicked_tower
            for tower in self.towers:
                tower.selected = False
            clicked_tower.selected = True
            self.placing_tower = None
        elif self.placing_tower:
            if self.can_place_tower(x, y):
                tower_cost = self.get_tower_cost(self.placing_tower)
                if self.money >= tower_cost:
                    self.towers.append(Tower(x, y, self.placing_tower))
                    self.money -= tower_cost
                    self.placing_tower = None
        else:
            for tower in self.towers:
                tower.selected = False
            self.selected_tower = None

    def can_place_tower(self, x, y):
        for px, py in self.path:
            if math.sqrt((x - px)**2 + (y - py)**2) < 30:
                return False
        for tower in self.towers:
            if math.sqrt((tower.x - x)**2 + (tower.y - y)**2) < 35:
                return False
        return 20 < x < WINDOW_WIDTH - 20 and 20 < y < WINDOW_HEIGHT - 150

    def get_tower_cost(self, tower_type):
        costs = {"basic": 50, "rapid": 70, "heavy": 120, "laser": 150}
        return costs.get(tower_type, 50)

    def update(self):
        if self.state != "playing":
            return
        self.frame_count += 1

        if self.wave_enemies_spawned < self.enemies_in_wave:
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay:
                self.spawn_enemy()
                self.spawn_timer = 0

        for tower in self.towers:
            tower.update(self.enemies, self.projectiles, self.frame_count)

        for enemy in self.enemies[:]:
            if enemy.enemy_type == "healer" and enemy.health > 0 and hasattr(enemy, 'heal_timer'):
                if enemy.heal_timer >= 60:
                    enemy.heal_timer = 0
                    for other in self.enemies:
                        if other != enemy and other.health > 0 and other.health < other.max_health:
                            d = math.sqrt((enemy.x - other.x)**2 + (enemy.y - other.y)**2)
                            if d < 100:
                                other.health = min(other.max_health, other.health + 6)
                                for _ in range(3):
                                    self.particles.append(Particle(other.x, other.y, PINK,
                                        random.uniform(-2, 2), random.uniform(-3, 1), 25))

        self.projectiles = [p for p in self.projectiles if p.update()]

        for projectile in self.projectiles[:]:
            for enemy in self.enemies:
                if enemy.health > 0 and projectile.check_collision(enemy):
                    particles = enemy.take_damage(projectile.damage)
                    self.particles.extend(particles)
                    if enemy.health <= 0:
                        if enemy.enemy_type == "splitter":
                            small = Enemy(self.path, "fast", LEVELS[self.level]["tier"])
                            small.x = enemy.x + random.uniform(-10, 10)
                            small.y = enemy.y + random.uniform(-10, 10)
                            small.max_health = int(enemy.max_health * 0.2)
                            small.health = small.max_health
                            small.speed = 1.5
                            small.size = 5
                            small.reward = 5
                            self.enemies.append(small)
                            for _ in range(5):
                                self.particles.append(Particle(small.x, small.y, MAGENTA,
                                    random.uniform(-3, 3), random.uniform(-4, 2), 30))
                        self.money += enemy.reward
                        self.score += enemy.reward * 10
                        self.wave_enemies_killed += 1
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    break

        for enemy in self.enemies[:]:
            if enemy.health <= 0:
                if enemy in self.enemies:
                    self.enemies.remove(enemy)
            elif not enemy.update():
                self.lives -= 1
                self.enemies.remove(enemy)
                if self.lives <= 0:
                    self.state = "game_over"

        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()

        if (self.wave_enemies_spawned >= self.enemies_in_wave and
            len([e for e in self.enemies if e.health > 0]) == 0):
            if self.wave >= self.total_waves:
                self.state = "victory"
            else:
                self.next_wave()

    def draw_path(self):
        if len(self.path) > 1:
            pygame.draw.lines(self.screen, DARK_GRAY, False, self.path, 8)
            pygame.draw.lines(self.screen, LIGHT_GRAY, False, self.path, 4)

    def draw_ui(self):
        ui_rect = pygame.Rect(0, WINDOW_HEIGHT - 150, WINDOW_WIDTH, 150)
        pygame.draw.rect(self.screen, DARK_GRAY, ui_rect)
        pygame.draw.rect(self.screen, WHITE, ui_rect, 2)

        level_data = LEVELS[self.level]
        tier_names = {1: "EASY", 2: "MEDIUM", 3: "HARD", 4: "VERY HARD", 5: "INSANE", 6: "LEGENDARY", 7: "MYTHIC", 8: "IMPOSSIBLE"}
        tier_name = tier_names.get(level_data["tier"], "")

        money_text = self.font.render(f"Money: ${self.money}", True, GOLD)
        lives_text = self.font.render(f"Lives: {self.lives}", True, RED)
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        wave_text = self.font.render(f"Wave: {self.wave}/{self.total_waves}", True, WHITE)
        level_text = self.small_font.render(f"{level_data['name']} [{tier_name}]", True, CYAN)

        self.screen.blit(money_text, (10, WINDOW_HEIGHT - 140))
        self.screen.blit(lives_text, (10, WINDOW_HEIGHT - 110))
        self.screen.blit(score_text, (10, WINDOW_HEIGHT - 80))
        self.screen.blit(wave_text, (10, WINDOW_HEIGHT - 50))
        self.screen.blit(level_text, (10, WINDOW_HEIGHT - 25))

        tower_types = ["basic", "rapid", "heavy", "laser"]
        tower_costs = [50, 70, 120, 150]
        tower_colors = [BLUE, GREEN, RED, PURPLE]

        for i, (tower_type, cost, color) in enumerate(zip(tower_types, tower_costs, tower_colors)):
            x = 250 + i * 80
            y = WINDOW_HEIGHT - 100
            button_rect = pygame.Rect(x, y, 70, 60)
            button_color = color if self.money >= cost else GRAY
            pygame.draw.rect(self.screen, button_color, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 2)
            pygame.draw.circle(self.screen, button_color, (x + 35, y + 20), 8)
            cost_text = self.small_font.render(f"${cost}", True, WHITE)
            key_text = self.small_font.render(f"{i+1}", True, WHITE)
            self.screen.blit(cost_text, (x + 5, y + 35))
            self.screen.blit(key_text, (x + 55, y + 5))

        if self.selected_tower:
            info_x = 650
            info_y = WINDOW_HEIGHT - 140
            tower_info = [
                f"Level: {self.selected_tower.level}",
                f"Damage: {self.selected_tower.damage}",
                f"Range: {self.selected_tower.range}",
                f"Upgrade: ${self.selected_tower.upgrade_cost}"
            ]
            for i, info in enumerate(tower_info):
                text = self.small_font.render(info, True, WHITE)
                self.screen.blit(text, (info_x, info_y + i * 20))
            if self.selected_tower.level < 5 and self.money >= self.selected_tower.upgrade_cost:
                upgrade_text = self.small_font.render("Press U to upgrade", True, GREEN)
                self.screen.blit(upgrade_text, (info_x, info_y + 80))

        instructions = [
            "1-4: Place towers",
            "Click: Select tower",
            "U: Upgrade tower",
            "Space: Pause",
            "R: Level select",
            "ESC: Exit"
        ]
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            self.screen.blit(text, (WINDOW_WIDTH - 150, WINDOW_HEIGHT - 140 + i * 16))

    def draw(self):
        self.screen.fill(BLACK)

        if self.state == "level_select":
            page = self.level_page
            lpp = 12
            start = page * lpp
            end = min(start + lpp, len(LEVELS))
            total_pages = (len(LEVELS) + lpp - 1) // lpp

            title = self.font.render(f"SELECT LEVEL ({page+1}/{total_pages})", True, WHITE)
            title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 50))
            self.screen.blit(title, title_rect)

            tier_colors = {1: GREEN, 2: YELLOW, 3: ORANGE, 4: RED, 5: PURPLE, 6: MAGENTA, 7: CYAN, 8: WHITE}
            tier_names = {1: "EASY", 2: "MEDIUM", 3: "HARD", 4: "VERY HARD", 5: "INSANE", 6: "LEGENDARY", 7: "MYTHIC", 8: "IMPOSSIBLE"}

            for i in range(start, end):
                li = i - start
                level = LEVELS[i]
                bx = 60 + (li % 4) * WINDOW_WIDTH // 4
                by = 160 + (li // 4) * 110
                rect = pygame.Rect(bx, by, WINDOW_WIDTH // 4 - 20, 80)
                tc = tier_colors.get(level["tier"], WHITE)
                pygame.draw.rect(self.screen, DARK_GRAY, rect)
                pygame.draw.rect(self.screen, tc, rect, 2)
                name_text = self.small_font.render(f"{i+1}. {level['name']}", True, WHITE)
                self.screen.blit(name_text, (bx + 8, by + 8))
                info_text = self.tiny_font.render(f"{level['waves']} waves | ${level['start_money']} | ♥{level['lives']}", True, tc)
                self.screen.blit(info_text, (bx + 8, by + 35))
                tier_text = self.tiny_font.render(tier_names[level["tier"]], True, tc)
                self.screen.blit(tier_text, (bx + 8, by + 55))

            if page > 0:
                prev_text = self.small_font.render("< PREV", True, WHITE)
                self.screen.blit(prev_text, (10, WINDOW_HEIGHT - 50))
            if end < len(LEVELS):
                next_text = self.small_font.render("NEXT >", True, WHITE)
                self.screen.blit(next_text, (WINDOW_WIDTH - 80, WINDOW_HEIGHT - 50))

            pygame.display.flip()
            return

        self.draw_path()

        for particle in self.particles:
            particle.draw(self.screen)
        for tower in self.towers:
            tower.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for projectile in self.projectiles:
            projectile.draw(self.screen)

        if self.placing_tower:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.can_place_tower(mouse_x, mouse_y):
                color = (*self.get_tower_color(self.placing_tower), 128)
                pygame.draw.circle(self.screen, color, (mouse_x, mouse_y), 15)
                pygame.draw.circle(self.screen, WHITE, (mouse_x, mouse_y), 80, 1)

        self.draw_ui()

        if self.state == "paused":
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            pause_text = self.font.render("PAUSED - Press SPACE to continue", True, WHITE)
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(pause_text, text_rect)
        elif self.state == "game_over":
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(RED)
            self.screen.blit(overlay, (0, 0))
            texts = [
                self.font.render("GAME OVER", True, WHITE),
                self.font.render(f"Final Score: {self.score}", True, WHITE),
                self.font.render("Press R to go to level select", True, WHITE)
            ]
            for i, text in enumerate(texts):
                text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + i * 40))
                self.screen.blit(text, text_rect)
        elif self.state == "victory":
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(GREEN)
            self.screen.blit(overlay, (0, 0))
            texts = [
                self.font.render("LEVEL COMPLETE!", True, WHITE),
                self.font.render(f"Final Score: {self.score}", True, WHITE),
                self.font.render("Press R to go to level select", True, WHITE)
            ]
            for i, text in enumerate(texts):
                text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + i * 40))
                self.screen.blit(text, text_rect)

        pygame.display.flip()

    def get_tower_color(self, tower_type):
        colors = {"basic": BLUE, "rapid": GREEN, "heavy": RED, "laser": PURPLE}
        return colors.get(tower_type, BLUE)

    def run(self):
        while self.running:
            self.handle_events()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_u] and self.selected_tower and hasattr(self, '_last_upgrade'):
                if pygame.time.get_ticks() - self._last_upgrade > 500:
                    if self.money >= self.selected_tower.upgrade_cost:
                        if self.selected_tower.upgrade():
                            self.money -= self.selected_tower.upgrade_cost
                    self._last_upgrade = pygame.time.get_ticks()
            elif not hasattr(self, '_last_upgrade'):
                self._last_upgrade = 0
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