import pygame
import random
import math
import sys
from collections import defaultdict

pygame.init()

W, H = 1280, 800
FPS = 60

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Maailman Valloitus - Risk")
clock = pygame.time.Clock()

FONT_SM = pygame.font.SysFont("arial", 14)
FONT_MD = pygame.font.SysFont("arial", 18, bold=True)
FONT_LG = pygame.font.SysFont("arial", 28, bold=True)
FONT_XL = pygame.font.SysFont("arial", 42, bold=True)
FONT_TINY = pygame.font.SysFont("arial", 11)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (200, 200, 200)
BG_COLOR = (20, 25, 40)
MAP_BG = (30, 40, 60)
PANEL_BG = (25, 30, 50)
PANEL_BORDER = (60, 70, 100)

PLAYER_COLORS = [
    (50, 120, 255),
    (220, 50, 50),
    (50, 200, 50),
    (255, 180, 30),
    (180, 50, 220),
    (50, 220, 220),
]

PLAYER_COLORS_LIGHT = [
    (100, 160, 255),
    (255, 100, 100),
    (100, 240, 100),
    (255, 220, 80),
    (220, 100, 255),
    (100, 255, 255),
]

PLAYER_NAMES = ["Sinä", "Bot Aggressiivinen", "Bot Varovainen", "Bot Tasapainoinen"]

CONTINENT_BONUS = {
    "Pohjois-Amerikka": 5,
    "Etelä-Amerikka": 2,
    "Eurooppa": 5,
    "Afrikka": 3,
    "Aasia": 7,
    "Oseania": 2,
}

CONTINENT_COLORS = {
    "Pohjois-Amerikka": (60, 80, 50),
    "Etelä-Amerikka": (50, 80, 60),
    "Eurooppa": (70, 60, 80),
    "Afrikka": (80, 70, 50),
    "Aasia": (60, 60, 80),
    "Oseania": (50, 70, 70),
}

TERRITORIES = {
    "Alaska": {"continent": "Pohjois-Amerikka", "pos": (105, 135), "neighbors": ["Luoteis-Kanada", "Kamchatka"]},
    "Luoteis-Kanada": {"continent": "Pohjois-Amerikka", "pos": (170, 140), "neighbors": ["Alaska", "Alberta", "Keski-Kanada", "Grönlanti"]},
    "Alberta": {"continent": "Pohjois-Amerikka", "pos": (155, 195), "neighbors": ["Luoteis-Kanada", "Keski-Kanada", "Länsi-USA"]},
    "Keski-Kanada": {"continent": "Pohjois-Amerikka", "pos": (230, 175), "neighbors": ["Luoteis-Kanada", "Alberta", "Ontario", "Länsi-USA"]},
    "Ontario": {"continent": "Pohjois-Amerikka", "pos": (240, 215), "neighbors": ["Keski-Kanada", "Länsi-USA", "Itä-USA", "Quebec"]},
    "Quebec": {"continent": "Pohjois-Amerikka", "pos": (290, 195), "neighbors": ["Ontario", "Itä-USA", "Grönlanti"]},
    "Länsi-USA": {"continent": "Pohjois-Amerikka", "pos": (170, 255), "neighbors": ["Alberta", "Keski-Kanada", "Ontario", "Itä-USA", "Keski-Amerikka"]},
    "Itä-USA": {"continent": "Pohjois-Amerikka", "pos": (240, 255), "neighbors": ["Ontario", "Quebec", "Länsi-USA", "Keski-Amerikka"]},
    "Keski-Amerikka": {"continent": "Pohjois-Amerikka", "pos": (165, 310), "neighbors": ["Länsi-USA", "Itä-USA", "Kolumbia"]},
    "Grönlanti": {"continent": "Pohjois-Amerikka", "pos": (340, 110), "neighbors": ["Luoteis-Kanada", "Quebec", "Islanti"]},
    "Kolumbia": {"continent": "Etelä-Amerikka", "pos": (210, 370), "neighbors": ["Keski-Amerikka", "Venezuela", "Peru", "Brasilia"]},
    "Venezuela": {"continent": "Etelä-Amerikka", "pos": (260, 345), "neighbors": ["Kolumbia", "Brasilia"]},
    "Peru": {"continent": "Etelä-Amerikka", "pos": (195, 420), "neighbors": ["Kolumbia", "Brasilia", "Argentiina"]},
    "Brasilia": {"continent": "Etelä-Amerikka", "pos": (260, 410), "neighbors": ["Kolumbia", "Venezuela", "Peru", "Argentiina"]},
    "Argentiina": {"continent": "Etelä-Amerikka", "pos": (210, 480), "neighbors": ["Peru", "Brasilia"]},
    "Islanti": {"continent": "Eurooppa", "pos": (410, 130), "neighbors": ["Grönlanti", "Skandinavia", "Britannia"]},
    "Skandinavia": {"continent": "Eurooppa", "pos": (470, 130), "neighbors": ["Islanti", "Britannia", "Pohjois-Eurooppa", "Ukraina"]},
    "Britannia": {"continent": "Eurooppa", "pos": (420, 195), "neighbors": ["Islanti", "Skandinavia", "Pohjois-Eurooppa", "Länsi-Eurooppa"]},
    "Pohjois-Eurooppa": {"continent": "Eurooppa", "pos": (490, 185), "neighbors": ["Skandinavia", "Britannia", "Länsi-Eurooppa", "Etelä-Eurooppa", "Ukraina"]},
    "Länsi-Eurooppa": {"continent": "Eurooppa", "pos": (430, 255), "neighbors": ["Britannia", "Pohjois-Eurooppa", "Etelä-Eurooppa", "Pohjois-Afrikka"]},
    "Etelä-Eurooppa": {"continent": "Eurooppa", "pos": (490, 250), "neighbors": ["Pohjois-Eurooppa", "Länsi-Eurooppa", "Ukraina", "Lähi-itä", "Pohjois-Afrikka", "Egypti"]},
    "Ukraina": {"continent": "Eurooppa", "pos": (550, 165), "neighbors": ["Skandinavia", "Pohjois-Eurooppa", "Etelä-Eurooppa", "Lähi-itä", "Afganistan", "Ural"]},
    "Pohjois-Afrikka": {"continent": "Afrikka", "pos": (420, 320), "neighbors": ["Länsi-Eurooppa", "Etelä-Eurooppa", "Egypti", "Itä-Afrikka", "Kongo"]},
    "Egypti": {"continent": "Afrikka", "pos": (490, 300), "neighbors": ["Etelä-Eurooppa", "Pohjois-Afrikka", "Itä-Afrikka", "Lähi-itä"]},
    "Itä-Afrikka": {"continent": "Afrikka", "pos": (510, 370), "neighbors": ["Pohjois-Afrikka", "Egypti", "Kongo", "Etelä-Afrikka", "Madagaskar", "Lähi-itä"]},
    "Kongo": {"continent": "Afrikka", "pos": (470, 400), "neighbors": ["Pohjois-Afrikka", "Itä-Afrikka", "Etelä-Afrikka"]},
    "Etelä-Afrikka": {"continent": "Afrikka", "pos": (480, 470), "neighbors": ["Kongo", "Itä-Afrikka", "Madagaskar"]},
    "Madagaskar": {"continent": "Afrikka", "pos": (540, 480), "neighbors": ["Itä-Afrikka", "Etelä-Afrikka"]},
    "Lähi-itä": {"continent": "Aasia", "pos": (560, 270), "neighbors": ["Etelä-Eurooppa", "Egypti", "Itä-Afrikka", "Afganistan", "Intia", "Ukraina"]},
    "Afganistan": {"continent": "Aasia", "pos": (620, 210), "neighbors": ["Ukraina", "Ural", "Lähi-itä", "Intia", "Kiina"]},
    "Ural": {"continent": "Aasia", "pos": (640, 130), "neighbors": ["Ukraina", "Afganistan", "Siperia", "Jakutia"]},
    "Siperia": {"continent": "Aasia", "pos": (720, 130), "neighbors": ["Ural", "Jakutia", "Mongolia", "Irkutsk"]},
    "Jakutia": {"continent": "Aasia", "pos": (770, 90), "neighbors": ["Ural", "Siperia", "Irkutsk", "Kamchatka"]},
    "Irkutsk": {"continent": "Aasia", "pos": (770, 170), "neighbors": ["Siperia", "Jakutia", "Mongolia", "Kamchatka"]},
    "Kamchatka": {"continent": "Aasia", "pos": (830, 110), "neighbors": ["Alaska", "Jakutia", "Irkutsk", "Mongolia", "Japani"]},
    "Mongolia": {"continent": "Aasia", "pos": (740, 220), "neighbors": ["Siperia", "Irkutsk", "Kamchatka", "Japani", "Kiina"]},
    "Japani": {"continent": "Aasia", "pos": (830, 210), "neighbors": ["Kamchatka", "Mongolia", "Kiina"]},
    "Kiina": {"continent": "Aasia", "pos": (700, 280), "neighbors": ["Afganistan", "Mongolia", "Japani", "Intia", "Kaakkois-Aasia"]},
    "Intia": {"continent": "Aasia", "pos": (630, 310), "neighbors": ["Lähi-itä", "Afganistan", "Kiina", "Kaakkois-Aasia"]},
    "Kaakkois-Aasia": {"continent": "Aasia", "pos": (730, 340), "neighbors": ["Kiina", "Intia", "Indonesia"]},
    "Indonesia": {"continent": "Oseania", "pos": (770, 400), "neighbors": ["Kaakkois-Aasia", "Länsi-Australia", "Uusi-Guinea"]},
    "Länsi-Australia": {"continent": "Oseania", "pos": (800, 470), "neighbors": ["Indonesia", "Itä-Australia"]},
    "Itä-Australia": {"continent": "Oseania", "pos": (850, 460), "neighbors": ["Länsi-Australia", "Uusi-Guinea"]},
    "Uusi-Guinea": {"continent": "Oseania", "pos": (830, 380), "neighbors": ["Indonesia", "Itä-Australia"]},
}

PHASE_REINFORCE = 0
PHASE_ATTACK = 1
PHASE_FORTIFY = 2
PHASE_AI = 3
PHASE_GAME_OVER = 4

PHASE_NAMES = {0: "VAHVISTUS", 1: "HYÖKKÄYS", 2: "LINNOITUS", 3: "BOTIT...", 4: "PELI OHI"}


class Territory:
    def __init__(self, name, data):
        self.name = name
        self.continent = data["continent"]
        self.pos = data["pos"]
        self.neighbors = data["neighbors"]
        self.owner = -1
        self.armies = 0
        self.poly = self._make_poly()

    def _make_poly(self):
        x, y = self.pos
        pts = []
        for i in range(6):
            angle = math.pi / 3 * i - math.pi / 6
            pts.append((x + 32 * math.cos(angle), y + 28 * math.sin(angle)))
        return pts

    def contains(self, mx, my):
        return math.hypot(mx - self.pos[0], my - self.pos[1]) < 30


class Game:
    def __init__(self):
        self.territories = {n: Territory(n, d) for n, d in TERRITORIES.items()}
        self.num_players = 4
        self.current_player = 0
        self.phase = PHASE_REINFORCE
        self.reinforcements_left = 0
        self.selected = None
        self.target = None
        self.dice_results = []
        self.attack_log = []
        self.fortify_from = None
        self.game_over = False
        self.winner = -1
        self.turn_number = 1
        self.conquered_this_turn = False
        self.ai_timer = 0
        self.ai_actions = []
        self.ai_log = []
        self.scroll_y = 0
        self.hover_terr = None
        self.cards = [{} for _ in range(self.num_players)]
        self.card_bonus_used = [False] * self.num_players
        self._distribute()

    def _distribute(self):
        names = list(self.territories.keys())
        random.shuffle(names)
        for i, name in enumerate(names):
            t = self.territories[name]
            t.owner = i % self.num_players
            t.armies = random.randint(1, 3)
        self._calc_reinforcements()

    def _calc_reinforcements(self):
        p = self.current_player
        owned = [t for t in self.territories.values() if t.owner == p]
        if not owned:
            self.reinforcements_left = 0
            return
        base = max(3, len(owned) // 3)
        bonus = 0
        cont_owned = defaultdict(list)
        for t in owned:
            cont_owned[t.continent].append(t)
        for cont, terrs in cont_owned.items():
            all_cont = [t for t in self.territories.values() if t.continent == cont]
            if len(terrs) == len(all_cont):
                bonus += CONTINENT_BONUS[cont]
        self.reinforcements_left = base + bonus

    def _is_adjacent(self, n1, n2):
        return n2 in self.territories[n1].neighbors

    def _roll_dice(self, n):
        return sorted([random.randint(1, 6) for _ in range(n)], reverse=True)

    def _do_attack(self, attacker_name, defender_name, num_atk_dice):
        atk = self.territories[attacker_name]
        dfd = self.territories[defender_name]
        num_def_dice = min(2, dfd.armies)
        atk_rolls = self._roll_dice(min(num_atk_dice, atk.armies - 1))
        def_rolls = self._roll_dice(num_def_dice)
        self.dice_results = (atk_rolls, def_rolls)
        atk_loss = 0
        def_loss = 0
        for a, d in zip(atk_rolls, def_rolls):
            if a > d:
                def_loss += 1
            else:
                atk_loss += 1
        atk.armies -= atk_loss
        dfd.armies -= def_loss
        msg = f"{PLAYER_NAMES[atk.owner]} hyökkää {attacker_name} -> {defender_name}: "
        if def_loss > 0:
            msg += f"Puollustaja menettää {def_loss} "
        if atk_loss > 0:
            msg += f"Hyökkääjä menettää {atk_loss} "
        conquered = False
        if dfd.armies <= 0:
            conquered = True
            old_owner = dfd.owner
            dfd.owner = atk.owner
            move_in = atk.armies - 1
            if num_atk_dice <= atk.armies - 1:
                move_in = max(num_atk_dice, atk.armies - 1)
            move_in = min(move_in, atk.armies - 1)
            dfd.armies = max(1, move_in)
            atk.armies -= dfd.armies
            msg += f"| {defender_name} vallattu! ({dfd.armies} siirretty)"
            if not any(t.owner == old_owner for t in self.territories.values()):
                msg += f" | {PLAYER_NAMES[old_owner]} eliminointu!"
            self.conquered_this_turn = True
        self.attack_log.append(msg)
        if len(self.attack_log) > 50:
            self.attack_log = self.attack_log[-50:]
        return conquered

    def _check_winner(self):
        for p in range(self.num_players):
            if all(t.owner == p for t in self.territories.values()):
                self.game_over = True
                self.winner = p
                self.phase = PHASE_GAME_OVER
                return True
        alive = set(t.owner for t in self.territories.values())
        if len(alive) == 1:
            w = alive.pop()
            self.game_over = True
            self.winner = w
            self.phase = PHASE_GAME_OVER
            return True
        return False

    def end_turn(self):
        self.selected = None
        self.target = None
        self.fortify_from = None
        self.conquered_this_turn = False
        p = self.current_player
        alive = set(t.owner for t in self.territories.values())
        if p not in alive:
            pass
        next_p = (p + 1) % self.num_players
        while next_p not in alive:
            next_p = (next_p + 1) % self.num_players
            if next_p == p:
                break
        self.current_player = next_p
        if next_p == 0:
            self.turn_number += 1
        if next_p == 0:
            self.phase = PHASE_REINFORCE
            self._calc_reinforcements()
        else:
            self.phase = PHASE_AI
            self.ai_timer = 0
            self.ai_actions = []
            self.ai_log = []
            self._start_ai_turn()

    def _start_ai_turn(self):
        p = self.current_player
        self._calc_reinforcements()
        self._ai_reinforce()
        self._ai_attack()
        self._ai_fortify()
        self.ai_timer = pygame.time.get_ticks()

    def _ai_reinforce(self):
        p = self.current_player
        owned = [n for n, t in self.territories.items() if t.owner == p]
        borders = [n for n in owned if any(self.territories[nb].owner != p for nb in self.territories[n].neighbors)]
        if not borders:
            borders = owned
        while self.reinforcements_left > 0:
            if self.current_player == 1:
                terr = self._ai_aggro_pick(borders)
            elif self.current_player == 2:
                terr = self._ai_defensive_pick(borders)
            else:
                terr = self._ai_balanced_pick(borders)
            if terr:
                self.territories[terr].armies += 1
                self.reinforcements_left -= 1
            else:
                t = random.choice(borders)
                self.territories[t].armies += 1
                self.reinforcements_left -= 1

    def _ai_aggro_pick(self, borders):
        best = None
        best_score = -999
        for n in borders:
            t = self.territories[n]
            enemy_nb = [nb for nb in t.neighbors if self.territories[nb].owner != t.owner]
            if not enemy_nb:
                continue
            weakest = min(enemy_nb, key=lambda nb: self.territories[nb].armies)
            score = self.territories[weakest].armies - t.armies + len(enemy_nb) * 2
            if score > best_score:
                best_score = score
                best = n
        return best

    def _ai_defensive_pick(self, borders):
        best = None
        best_threat = 0
        for n in borders:
            t = self.territories[n]
            threat = sum(self.territories[nb].armies for nb in t.neighbors if self.territories[nb].owner != t.owner)
            need = threat - t.armies
            if need > best_threat:
                best_threat = need
                best = n
        return best

    def _ai_balanced_pick(self, borders):
        best = None
        best_score = -999
        for n in borders:
            t = self.territories[n]
            enemy_nb = [nb for nb in t.neighbors if self.territories[nb].owner != t.owner]
            if not enemy_nb:
                continue
            threat = sum(self.territories[nb].armies for nb in enemy_nb)
            score = len(enemy_nb) * 3 - t.armies + (threat > t.armies * 2) * 5
            if score > best_score:
                best_score = score
                best = n
        return best

    def _ai_attack(self):
        p = self.current_player
        for _ in range(50):
            owned = [n for n, t in self.territories.items() if t.owner == p]
            attackable = []
            for n in owned:
                t = self.territories[n]
                if t.armies <= 1:
                    continue
                for nb in t.neighbors:
                    if self.territories[nb].owner != p:
                        attackable.append((n, nb))
            if not attackable:
                break
            if self.current_player == 1:
                scored = [(n, nb, self.territories[n].armies - self.territories[nb].armies) for n, nb in attackable]
                scored.sort(key=lambda x: -x[2])
                if scored[0][2] < 1:
                    if random.random() > 0.3:
                        break
                attacker, defender, _ = scored[0]
            elif self.current_player == 2:
                scored = [(n, nb, self.territories[n].armies - self.territories[nb].armies) for n, nb in attackable]
                scored.sort(key=lambda x: -x[2])
                if scored[0][2] < 2:
                    break
                attacker, defender, _ = scored[0]
            else:
                scored = [(n, nb, self.territories[n].armies - self.territories[nb].armies) for n, nb in attackable]
                scored.sort(key=lambda x: -x[2])
                if scored[0][2] < 0:
                    if random.random() > 0.4:
                        break
                attacker, defender, _ = scored[0]
            num_dice = min(3, self.territories[attacker].armies - 1)
            if num_dice < 1:
                continue
            self._do_attack(attacker, defender, num_dice)
            self.ai_log.append(f"{PLAYER_NAMES[p]}: {attacker} -> {defender}")
            if self._check_winner():
                return

    def _ai_fortify(self):
        p = self.current_player
        owned = [n for n, t in self.territories.items() if t.owner == p]
        for n in owned:
            t = self.territories[n]
            if t.armies <= 1:
                continue
            enemy_nb = [nb for nb in t.neighbors if self.territories[nb].owner != p]
            if enemy_nb:
                continue
            for nb in t.neighbors:
                nb_t = self.territories[nb]
                if nb_t.owner == p:
                    has_enemy = any(self.territories[nnb].owner != p for nnb in nb_t.neighbors)
                    if has_enemy:
                        move = t.armies - 1
                        nb_t.armies += move
                        t.armies = 1
                        break


def draw_game(game):
    screen.fill(BG_COLOR)
    map_surf = pygame.Surface((900, H))
    map_surf.fill(MAP_BG)
    pygame.draw.rect(map_surf, PANEL_BORDER, (0, 0, 900, H), 1)

    continents = defaultdict(list)
    for n, t in game.territories.items():
        continents[t.continent].append(n)

    for cont_name, terr_names in continents.items():
        color = CONTINENT_COLORS.get(cont_name, (50, 50, 50))
        for n in terr_names:
            t = game.territories[n]
            pts = [(x + random.random() * 0.01, y + random.random() * 0.01) for x, y in t.poly]
            pygame.draw.polygon(map_surf, color, pts)
            pygame.draw.polygon(map_surf, (color[0] + 20, color[1] + 20, color[2] + 20), pts, 1)

    for n, t in game.territories.items():
        for nb in t.neighbors:
            nt = game.territories[nb]
            x1, y1 = t.pos
            x2, y2 = nt.pos
            if t.continent == nt.continent:
                col = (60, 70, 90)
            else:
                col = (45, 55, 75)
            pygame.draw.line(map_surf, col, (x1, y1), (x2, y2), 1)

    for n, t in game.territories.items():
        if t.owner >= 0:
            col = PLAYER_COLORS[t.owner]
            pts = t.poly
            pygame.draw.polygon(map_surf, col, pts)
            light = PLAYER_COLORS_LIGHT[t.owner]
            pygame.draw.polygon(map_surf, light, pts, 2)
            if game.selected == n:
                pygame.draw.polygon(map_surf, WHITE, pts, 3)
            elif game.target == n:
                pygame.draw.polygon(map_surf, YELLOW, pts, 3)
            elif game.hover_terr == n:
                pygame.draw.polygon(map_surf, (255, 255, 255), pts, 2)

    for n, t in game.territories.items():
        x, y = t.pos
        army_text = FONT_MD.render(str(t.armies), True, WHITE)
        tr = army_text.get_rect(center=(x, y))
        shadow = FONT_MD.render(str(t.armies), True, BLACK)
        sr = shadow.get_rect(center=(x + 1, y + 1))
        map_surf.blit(shadow, sr)
        map_surf.blit(army_text, tr)
        name_text = FONT_TINY.render(n, True, (200, 200, 210))
        nr = name_text.get_rect(center=(x, y - 22))
        map_surf.blit(name_text, nr)

    screen.blit(map_surf, (0, 0))

    panel_x = 900
    panel_w = W - panel_x
    pygame.draw.rect(screen, PANEL_BG, (panel_x, 0, panel_w, H))
    pygame.draw.line(screen, PANEL_BORDER, (panel_x, 0), (panel_x, H), 2)

    py = 10
    turn_text = FONT_LG.render(f"Vuoro {game.turn_number}", True, GOLD)
    screen.blit(turn_text, (panel_x + 15, py))
    py += 40

    p = game.current_player
    p_col = PLAYER_COLORS[p]
    phase_text = FONT_MD.render(PHASE_NAMES[game.phase], True, p_col)
    screen.blit(phase_text, (panel_x + 15, py))
    py += 28

    player_text = FONT_MD.render(PLAYER_NAMES[p], True, p_col)
    screen.blit(player_text, (panel_x + 15, py))
    py += 30

    if game.phase == PHASE_REINFORCE:
        ri_text = FONT_MD.render(f"Vahvistuksia: {game.reinforcements_left}", True, YELLOW)
        screen.blit(ri_text, (panel_x + 15, py))
        py += 25
        hint = FONT_SM.render("Klikkaa aluetta vahvistukseen", True, LIGHT_GRAY)
        screen.blit(hint, (panel_x + 15, py))
        py += 20
    elif game.phase == PHASE_ATTACK:
        hint = FONT_SM.render("Valitse hyökkäävä alue", True, LIGHT_GRAY)
        screen.blit(hint, (panel_x + 15, py))
        py += 18
        hint2 = FONT_SM.render("sitten kohde (tai oikea = peru)", True, LIGHT_GRAY)
        screen.blit(hint2, (panel_x + 15, py))
        py += 22
    elif game.phase == PHASE_FORTIFY:
        hint = FONT_SM.render("Valitse lähdealue, sitten kohde", True, LIGHT_GRAY)
        screen.blit(hint, (panel_x + 15, py))
        py += 22
    elif game.phase == PHASE_AI:
        hint = FONT_SM.render("Botti pelaa...", True, LIGHT_GRAY)
        screen.blit(hint, (panel_x + 15, py))
        py += 22

    py += 10
    pygame.draw.line(screen, PANEL_BORDER, (panel_x + 10, py), (W - 10, py), 1)
    py += 10

    stats_title = FONT_MD.render("Pelaajat:", True, WHITE)
    screen.blit(stats_title, (panel_x + 15, py))
    py += 25

    for i in range(game.num_players):
        owned = sum(1 for t in game.territories.values() if t.owner == i)
        total_armies = sum(t.armies for t in game.territories.values() if t.owner == i)
        alive = owned > 0
        col = PLAYER_COLORS[i] if alive else GRAY
        marker = "●" if alive else "✕"
        text = FONT_SM.render(f"{marker} {PLAYER_NAMES[i]}: {owned} aluetta, {total_armies} armeijaa", True, col)
        screen.blit(text, (panel_x + 15, py))
        py += 18
    py += 10

    pygame.draw.line(screen, PANEL_BORDER, (panel_x + 10, py), (W - 10, py), 1)
    py += 10

    cont_title = FONT_MD.render("Mantereet:", True, WHITE)
    screen.blit(cont_title, (panel_x + 15, py))
    py += 22

    for cn, bonus in CONTINENT_BONUS.items():
        cont_terr = [t for t in game.territories.values() if t.continent == cn]
        owners = set(t.owner for t in cont_terr)
        if len(owners) == 1:
            owner = owners.pop()
            col = PLAYER_COLORS[owner]
            status = f"✓ {PLAYER_NAMES[owner]} (+{bonus})"
        else:
            col = GRAY
            max_o = max(set(t.owner for t in cont_terr), key=lambda o: sum(1 for t in cont_terr if t.owner == o))
            max_count = sum(1 for t in cont_terr if t.owner == max_o)
            status = f"{max_count}/{len(cont_terr)}"
        text = FONT_SM.render(f"{cn}: {status}", True, col)
        screen.blit(text, (panel_x + 15, py))
        py += 17
    py += 10

    pygame.draw.line(screen, PANEL_BORDER, (panel_x + 10, py), (W - 10, py), 1)
    py += 10

    log_title = FONT_MD.render("Taistelulogi:", True, WHITE)
    screen.blit(log_title, (panel_x + 15, py))
    py += 22

    log_area_top = py
    log_area_h = H - log_area_top - 80
    pygame.draw.rect(screen, (15, 18, 30), (panel_x + 10, log_area_top, panel_w - 20, log_area_h))
    pygame.draw.rect(screen, PANEL_BORDER, (panel_x + 10, log_area_top, panel_w - 20, log_area_h), 1)

    visible_logs = game.attack_log[-(log_area_h // 16):]
    for i, log in enumerate(visible_logs):
        text = FONT_TINY.render(log[:50], True, (180, 180, 190))
        screen.blit(text, (panel_x + 15, log_area_top + 3 + i * 15))

    btn_y = H - 65
    buttons = []

    if game.phase == PHASE_REINFORCE:
        if game.reinforcements_left == 0:
            btn = pygame.Rect(panel_x + 15, btn_y, 170, 35)
            pygame.draw.rect(screen, (50, 130, 50), btn, border_radius=5)
            pygame.draw.rect(screen, (80, 180, 80), btn, 2, border_radius=5)
            t = FONT_MD.render("Hyökkäys vaihe ▶", True, WHITE)
            screen.blit(t, t.get_rect(center=btn.center))
            buttons.append(("attack_phase", btn))
    elif game.phase == PHASE_ATTACK:
        btn = pygame.Rect(panel_x + 15, btn_y, 170, 35)
        pygame.draw.rect(screen, (50, 80, 130), btn, border_radius=5)
        pygame.draw.rect(screen, (80, 120, 180), btn, 2, border_radius=5)
        t = FONT_MD.render("Linnoitus vaihe ▶", True, WHITE)
        screen.blit(t, t.get_rect(center=btn.center))
        buttons.append(("fortify_phase", btn))
    elif game.phase == PHASE_FORTIFY:
        btn = pygame.Rect(panel_x + 15, btn_y, 170, 35)
        pygame.draw.rect(screen, (130, 80, 50), btn, border_radius=5)
        pygame.draw.rect(screen, (180, 120, 80), btn, 2, border_radius=5)
        t = FONT_MD.render("Lopeta vuoro ▶", True, WHITE)
        screen.blit(t, t.get_rect(center=btn.center))
        buttons.append(("end_turn", btn))

    if game.phase == PHASE_ATTACK and game.selected:
        btn2 = pygame.Rect(panel_x + 200, btn_y, 60, 35)
        pygame.draw.rect(screen, (150, 50, 50), btn2, border_radius=5)
        pygame.draw.rect(screen, (200, 80, 80), btn2, 2, border_radius=5)
        t = FONT_SM.render("1 noppa", True, WHITE)
        screen.blit(t, t.get_rect(center=btn2.center))
        buttons.append(("dice_1", btn2))

        if game.territories[game.selected].armies > 2:
            btn3 = pygame.Rect(panel_x + 270, btn_y, 60, 35)
            pygame.draw.rect(screen, (180, 60, 60), btn3, border_radius=5)
            pygame.draw.rect(screen, (220, 100, 100), btn3, 2, border_radius=5)
            t = FONT_SM.render("2 noppaa", True, WHITE)
            screen.blit(t, t.get_rect(center=btn3.center))
            buttons.append(("dice_2", btn3))

        if game.territories[game.selected].armies > 3:
            btn4 = pygame.Rect(panel_x + 340, btn_y, 60, 35)
            pygame.draw.rect(screen, (200, 70, 70), btn4, border_radius=5)
            pygame.draw.rect(screen, (240, 120, 120), btn4, 2, border_radius=5)
            t = FONT_SM.render("3 noppaa", True, WHITE)
            screen.blit(t, t.get_rect(center=btn4.center))
            buttons.append(("dice_3", btn4))

    if game.phase in (PHASE_REINFORCE, PHASE_ATTACK, PHASE_FORTIFY):
        btn_skip = pygame.Rect(panel_x + 200 if game.phase != PHASE_ATTACK else panel_x + 15, btn_y - 40, 130, 30)
        pygame.draw.rect(screen, DARK_GRAY, btn_skip, border_radius=4)
        t = FONT_SM.render("Seuraava vaihe ▶▶", True, LIGHT_GRAY)
        screen.blit(t, t.get_rect(center=btn_skip.center))
        if game.phase == PHASE_REINFORCE:
            buttons.append(("skip_to_attack", btn_skip))
        elif game.phase == PHASE_ATTACK:
            buttons.append(("skip_to_fortify", btn_skip))
        elif game.phase == PHASE_FORTIFY:
            buttons.append(("end_turn", btn_skip))

    if game.game_over:
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        winner_text = FONT_XL.render(f"{PLAYER_NAMES[game.winner]} voittaa!", True, PLAYER_COLORS[game.winner])
        wr = winner_text.get_rect(center=(W // 2, H // 2 - 30))
        screen.blit(winner_text, wr)
        sub = FONT_LG.render("Maailma on vallattu!", True, GOLD)
        sr = sub.get_rect(center=(W // 2, H // 2 + 30))
        screen.blit(sub, sr)
        restart = FONT_MD.render("Paina R uudelleen aloitukseen", True, WHITE)
        rr = restart.get_rect(center=(W // 2, H // 2 + 70))
        screen.blit(restart, rr)

    return buttons


def get_terr_at(game, mx, my):
    for n, t in game.territories.items():
        if t.contains(mx, my):
            return n
    return None


def main():
    game = Game()
    running = True

    while running:
        mx, my = pygame.mouse.get_pos()
        game.hover_terr = get_terr_at(game, mx, my) if mx < 900 else None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    game = Game()
                elif event.key == pygame.K_SPACE:
                    if game.phase == PHASE_REINFORCE and game.reinforcements_left == 0:
                        game.phase = PHASE_ATTACK
                        game.selected = None
                        game.target = None
                    elif game.phase == PHASE_ATTACK:
                        game.phase = PHASE_FORTIFY
                        game.selected = None
                        game.target = None
                        game.fortify_from = None
                    elif game.phase == PHASE_FORTIFY:
                        game.end_turn()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    game.selected = None
                    game.target = None
                    game.fortify_from = None
                    continue

                buttons = draw_game(game)
                clicked_btn = None
                for bname, brect in buttons:
                    if brect.collidepoint(mx, my):
                        clicked_btn = bname
                        break

                if clicked_btn:
                    if clicked_btn == "attack_phase":
                        game.phase = PHASE_ATTACK
                        game.selected = None
                        game.target = None
                    elif clicked_btn == "fortify_phase":
                        game.phase = PHASE_FORTIFY
                        game.selected = None
                        game.target = None
                        game.fortify_from = None
                    elif clicked_btn == "end_turn":
                        game.end_turn()
                    elif clicked_btn == "skip_to_attack":
                        game.reinforcements_left = 0
                        game.phase = PHASE_ATTACK
                        game.selected = None
                    elif clicked_btn == "skip_to_fortify":
                        game.phase = PHASE_FORTIFY
                        game.selected = None
                        game.target = None
                        game.fortify_from = None
                    elif clicked_btn.startswith("dice_"):
                        num_dice = int(clicked_btn.split("_")[1])
                        if game.selected and game.target:
                            game._do_attack(game.selected, game.target, num_dice)
                            game._check_winner()
                            if game.territories[game.selected].owner != game.current_player:
                                game.selected = None
                                game.target = None
                            elif game.territories[game.selected].armies <= 1:
                                game.selected = None
                                game.target = None
                            else:
                                game.target = None
                    continue

                if mx < 900 and game.current_player == 0:
                    clicked = get_terr_at(game, mx, my)
                    if clicked:
                        t = game.territories[clicked]
                        if game.phase == PHASE_REINFORCE:
                            if t.owner == 0 and game.reinforcements_left > 0:
                                t.armies += 1
                                game.reinforcements_left -= 1
                        elif game.phase == PHASE_ATTACK:
                            if game.selected is None:
                                if t.owner == 0 and t.armies > 1:
                                    game.selected = clicked
                            elif game.target is None:
                                if clicked == game.selected:
                                    game.selected = None
                                elif t.owner != 0 and game._is_adjacent(game.selected, clicked):
                                    game.target = clicked
                                    max_dice = min(3, game.territories[game.selected].armies - 1)
                                    game._do_attack(game.selected, game.target, max_dice)
                                    game._check_winner()
                                    if game.territories.get(game.selected) and game.territories[game.selected].owner != 0:
                                        game.selected = None
                                    elif game.territories.get(game.selected) and game.territories[game.selected].armies <= 1:
                                        game.selected = None
                                    game.target = None
                                elif t.owner == 0 and t.armies > 1:
                                    game.selected = clicked
                                else:
                                    game.selected = None
                            else:
                                game.selected = None
                                game.target = None
                        elif game.phase == PHASE_FORTIFY:
                            if game.fortify_from is None:
                                if t.owner == 0 and t.armies > 1:
                                    game.fortify_from = clicked
                            else:
                                if clicked == game.fortify_from:
                                    game.fortify_from = None
                                elif t.owner == 0 and game._is_adjacent(game.fortify_from, clicked):
                                    src = game.territories[game.fortify_from]
                                    dst = game.territories[clicked]
                                    move = src.armies - 1
                                    dst.armies += move
                                    src.armies = 1
                                    game.fortify_from = None
                                    game.end_turn()
                                else:
                                    game.fortify_from = None

        if game.phase == PHASE_AI:
            elapsed = pygame.time.get_ticks() - game.ai_timer
            if elapsed > 600:
                game.end_turn()

        buttons = draw_game(game)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
