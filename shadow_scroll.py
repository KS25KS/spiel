"""
SHADOW SCROLL  —  A Ninja Quest
================================
Install:  pip install pygame
Run:      python shadow_scroll.py

Controls:
  Arrow keys / WASD  — move / navigate
  SPACE              — jump (platformer) / confirm
  Z                  — attack
  S                  — open shop (anywhere except boss fight)
  ESC                — pause / quit confirm
"""

import pygame
import random
import sys
import math

pygame.init()

# ─── constants ────────────────────────────────────────────────────────────────
W, H = 800, 520
FPS  = 60
TILE = 32

# colour palette  (eerie blue / ghostly green / black theme)
BLACK   = (  5,  8, 18)
DKBLUE  = (  8, 20, 45)
BLUE1   = ( 20, 80,150)
BLUE2   = ( 40,160,220)
BLUE3   = ( 90,210,255)
GREEN1  = ( 10, 60, 35)
GHOSTG  = ( 60,255,160)
GHOSTG2 = ( 20,180,100)
STONE   = ( 18, 32, 50)
STONELT = ( 28, 50, 75)
GOLD    = (232,194, 70)
GOLDDARK= (160,130, 30)
RED     = (220, 50, 50)
REDDARK = (120, 15, 15)
PURPLE  = (140, 60,210)
PURPLT  = (200,130,255)
WHITE   = (220,230,255)
GREY    = ( 80, 90,110)
ORANGE  = (230,120, 30)

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Shadow Scroll")
clock  = pygame.time.Clock()

# ─── fonts ────────────────────────────────────────────────────────────────────
try:
    FONT_SM  = pygame.font.SysFont("Courier New", 13, bold=True)
    FONT_MD  = pygame.font.SysFont("Courier New", 18, bold=True)
    FONT_LG  = pygame.font.SysFont("Courier New", 28, bold=True)
    FONT_XL  = pygame.font.SysFont("Courier New", 40, bold=True)
except:
    FONT_SM  = pygame.font.SysFont(None, 14)
    FONT_MD  = pygame.font.SysFont(None, 20)
    FONT_LG  = pygame.font.SysFont(None, 30)
    FONT_XL  = pygame.font.SysFont(None, 44)


# ══════════════════════════════════════════════════════════════════════════════
#  PIXEL ART DRAWING HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def px(surf, col, rect):
    pygame.draw.rect(surf, col, rect)

def draw_ninja(surf, x, y, facing, anim_t, attacking, invincible):
    """Blue-black ninja with scarf. facing: 1=right, -1=left."""
    if invincible and (pygame.time.get_ticks() // 80) % 2 == 0:
        return
    flip = facing < 0
    # leg bob
    lb = int(math.sin(anim_t) * 3)

    def r(rx, ry, rw, rh):
        fx = x + (W_NINJA - rx - rw if flip else rx)
        surf.fill(col, (fx, y + ry, rw, rh))

    W_NINJA = 20
    col = BLUE1
    # torso
    surf.fill(BLUE1,   (x+(W_NINJA//2-5 if not flip else W_NINJA//2-5), y+8, 10, 12))
    # head
    surf.fill(BLACK,   (x+(W_NINJA//2-5 if not flip else W_NINJA//2-5), y, 10, 9))
    # headband
    surf.fill(BLUE2,   (x+(W_NINJA//2-5 if not flip else W_NINJA//2-5), y+1, 10, 3))
    # eyes
    surf.fill(BLUE3,   (x+(W_NINJA//2-2 if not flip else W_NINJA//2+1), y+3, 3, 2))
    # scarf
    surf.fill(BLUE3,   (x+(W_NINJA//2-6 if not flip else W_NINJA//2-4), y+5, 12, 3))
    surf.fill(BLUE2,   (x+(W_NINJA//2-7 if not flip else W_NINJA//2-3), y+8, 4, 6))
    # legs
    surf.fill(DKBLUE,  (x+(W_NINJA//2-5 if not flip else W_NINJA//2-1), y+20, 4, 6+lb))
    surf.fill(DKBLUE,  (x+(W_NINJA//2+1 if not flip else W_NINJA//2-5), y+20, 4, 9-lb))
    # arms
    surf.fill(BLUE1,   (x+(W_NINJA//2-7 if not flip else W_NINJA//2+3), y+9, 3, 8))
    surf.fill(BLUE1,   (x+(W_NINJA//2+4 if not flip else W_NINJA//2-7), y+9, 3, 8))
    # sword attack
    if attacking:
        sx = x + (W_NINJA+2 if not flip else -14)
        surf.fill(WHITE,  (sx, y+6, 14, 3))
        surf.fill(GOLD,   (sx, y+5, 4, 5))


def draw_small_dragon(surf, x, y, anim_t, hp, max_hp):
    """Aggressive small dragon enemy."""
    bob = int(math.sin(anim_t) * 2)
    y += bob
    # body
    surf.fill((100, 20, 20), (x+2, y+6, 14, 10))
    # head
    surf.fill((140, 30, 30), (x+8, y, 10, 8))
    # horns
    surf.fill((80, 10, 10),  (x+9, y-4, 3, 5))
    surf.fill((80, 10, 10),  (x+14, y-3, 3, 4))
    # eyes
    surf.fill((255,200, 0),  (x+10, y+2, 3, 2))
    surf.fill((200, 0,  0),  (x+11, y+2, 2, 2))
    # wings
    surf.fill((60, 10, 10),  (x-4, y+3, 6, 7))
    surf.fill((60, 10, 10),  (x+16, y+3, 6, 7))
    # tail
    surf.fill((100, 20, 20), (x-2, y+12, 4, 4))
    # hp bar
    if hp < max_hp:
        pygame.draw.rect(surf, REDDARK, (x, y-8, 18, 4))
        pygame.draw.rect(surf, RED,     (x, y-8, int(18*hp/max_hp), 4))


def draw_boss_dragon(surf, x, y, anim_t, hp, max_hp):
    """Big black-and-red boss dragon."""
    bob = int(math.sin(anim_t * 0.5) * 4)
    y += bob
    S = 3  # scale multiplier via rects

    def b(rx, ry, rw, rh, c):
        surf.fill(c, (x + rx*S, y + ry*S, rw*S, rh*S))

    # body
    b(2, 8, 18, 14, (15,  5,  5))
    b(3, 9, 16, 12, (30, 10, 10))
    # belly
    b(5,11,  10, 8, (60, 20, 20))
    # head
    b(8, 0, 14, 10, (25,  5,  5))
    b(9, 1, 12,  8, (40, 10, 10))
    # snout / jaw
    b(15, 6, 7,  5, (30,  8,  8))
    b(15, 9, 7,  3, (20,  5,  5))
    # teeth
    b(16,11, 2,  3, WHITE)
    b(19,11, 2,  3, WHITE)
    # eyes  — glowing red
    b(10, 2, 4,  3, (255, 30, 30))
    b(11, 3, 2,  2, (255,200,  0))
    # horns
    b( 9,-5, 3,  6, (10,  3,  3))
    b(12,-7, 3,  8, (10,  3,  3))
    b(17,-4, 3,  5, (10,  3,  3))
    # wings (large)
    b(-8, 4, 10, 14, (12,  4,  4))
    b(-12,2,  5, 10, (20,  6,  6))
    b(22, 4, 10, 14, (12,  4,  4))
    b(27, 2,  5, 10, (20,  6,  6))
    # legs
    b( 4,20,  5,  8, (20,  6,  6))
    b(13,20,  5,  8, (20,  6,  6))
    # claws
    b( 3,27,  3,  3, (60, 20, 20))
    b( 6,27,  3,  3, (60, 20, 20))
    b(12,27,  3,  3, (60, 20, 20))
    b(15,27,  3,  3, (60, 20, 20))
    # tail
    b( 0,18,  4,  6, (20,  6,  6))
    b(-3,22,  4,  5, (15,  4,  4))
    # fire breath (animated)
    if int(anim_t * 2) % 3 == 0:
        b(22, 5,  8,  4, (255,120,  0))
        b(28, 4, 10,  6, (255, 60,  0))
        b(36, 5,  6,  4, (200, 30,  0))

    # HP bar
    bar_w = 22 * S
    pygame.draw.rect(surf, REDDARK, (x, y - 20, bar_w, 8))
    pygame.draw.rect(surf, RED,     (x, y - 20, int(bar_w * hp / max_hp), 8))
    pygame.draw.rect(surf, WHITE,   (x, y - 20, bar_w, 8), 1)
    lbl = FONT_SM.render("BOSS", True, WHITE)
    surf.blit(lbl, (x + bar_w // 2 - lbl.get_width() // 2, y - 32))


def draw_wise_dragon(surf, x, y):
    """White dragon sensei with long beard and Wu hat."""
    # body
    surf.fill((180,180,220), (x-16, y-28, 32, 40))
    surf.fill((210,210,240), (x-12, y-40, 24, 20))
    # beard
    surf.fill(WHITE, (x-10, y-10, 6, 30))
    surf.fill(WHITE, (x-6,  y-10, 4, 35))
    surf.fill(WHITE, (x-2,  y-10, 4, 32))
    surf.fill(WHITE, (x+2,  y-10, 4, 28))
    # eyes
    surf.fill((100,120,200), (x-8, y-34, 5, 4))
    surf.fill((100,120,200), (x+3, y-34, 5, 4))
    surf.fill(BLACK,         (x-7, y-33, 3, 3))
    surf.fill(BLACK,         (x+4, y-33, 3, 3))
    # sensei hat (conical)
    pts = [(x, y-56), (x-18, y-40), (x+18, y-40)]
    pygame.draw.polygon(surf, GOLDDARK, pts)
    pygame.draw.polygon(surf, GOLD,     pts, 2)
    surf.fill(GOLD, (x-18, y-42, 36, 5))
    # wings folded
    surf.fill((160,160,200), (x-28, y-20, 14, 24))
    surf.fill((160,160,200), (x+14, y-20, 14, 24))
    # staff
    surf.fill((120, 90, 40), (x+22, y-50, 5, 70))
    surf.fill(GHOSTG,        (x+21, y-56, 7, 10))


# ══════════════════════════════════════════════════════════════════════════════
#  PARTICLE SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

class Particle:
    def __init__(self, x, y, col):
        self.x, self.y  = float(x), float(y)
        self.vx = random.uniform(-2.5, 2.5)
        self.vy = random.uniform(-3.5, 0.5)
        self.col  = col
        self.life = random.randint(18, 35)
        self.max_life = self.life

    def update(self):
        self.x  += self.vx
        self.y  += self.vy
        self.vy += 0.15
        self.life -= 1

    def draw(self, surf, cam_x=0):
        alpha = int(255 * self.life / self.max_life)
        s = pygame.Surface((4, 4), pygame.SRCALPHA)
        s.fill((*self.col[:3], alpha))
        surf.blit(s, (int(self.x) - cam_x, int(self.y)))


# ══════════════════════════════════════════════════════════════════════════════
#  GAME STATE
# ══════════════════════════════════════════════════════════════════════════════

class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.mode      = "intro"    # intro | platformer | dungeon | shop | win | dead | pause
        self.prev_mode = "platformer"
        self.level     = 1          # 1..5
        self.lives     = 3
        self.coins     = 0
        self.weapon    = "sword"    # sword | bow | staff
        self.hp        = 6
        self.max_hp    = 6
        self.intro_step = 0
        self.frame     = 0
        self.particles : list[Particle] = []
        self.message   = ""
        self.msg_timer = 0
        self.scroll_found = False

    def add_particles(self, x, y, col, n=8):
        for _ in range(n):
            self.particles.append(Particle(x, y, col))

    def set_msg(self, txt, duration=240):
        self.message   = txt
        self.msg_timer = duration

    def weapon_dmg(self):
        return {"sword": 1, "bow": 2, "staff": 3}[self.weapon]


GS = GameState()


# ══════════════════════════════════════════════════════════════════════════════
#  INTRO SCENE
# ══════════════════════════════════════════════════════════════════════════════

INTRO_LINES = [
    ("SHEN-LONG", BLUE3,
     "Young ninja... I have watched you from the mists of a thousand years."),
    ("SHEN-LONG", BLUE3,
     "Five tombs lie ahead — each darker than the last."),
    ("SHEN-LONG", BLUE3,
     "The Sacred Scroll of Eternity was stolen by the Ghost Dragons."),
    ("SHEN-LONG", BLUE3,
     "It rests in the deepest tomb, guarded by Vorthar — the Black Dragon."),
    ("SHEN-LONG", BLUE3,
     "Cross the haunted overworld between each tomb. Collect coins. Grow stronger."),
    ("SHEN-LONG", BLUE3,
     "But remember: three lives are all you carry. Spend them wisely."),
    ("[ PRESS SPACE ]", GHOSTG,
     "Arrow keys / WASD — move.   SPACE — jump.   Z — attack.   S — shop."),
]


def draw_intro():
    # sky (daytime for the intro)
    screen.fill((100, 170, 220))
    # clouds
    t = GS.frame
    for i in range(5):
        cx = (i * 200 + t // 3) % (W + 100) - 50
        cy = 60 + i * 18
        pygame.draw.ellipse(screen, WHITE, (cx, cy, 100, 30))
        pygame.draw.ellipse(screen, WHITE, (cx+20, cy-12, 70, 28))
    # ground
    pygame.draw.rect(screen, (40, 90, 30), (0, H-80, W, 80))
    for i in range(0, W, 16):
        c = (50,110,35) if (i//16)%2==0 else (40,90,30)
        pygame.draw.rect(screen, c, (i, H-84, 16, 10))

    # wise dragon (left side)
    draw_wise_dragon(screen, 130, H-100)
    # ninja (right side)
    draw_ninja(screen, W-140, H-120, -1, 0, False, False)

    # dialogue box
    box = pygame.Rect(30, H-180, W-60, 120)
    pygame.draw.rect(screen, (0, 10, 25, 200), box)
    pygame.draw.rect(screen, BLUE2, box, 2)

    step = min(GS.intro_step, len(INTRO_LINES)-1)
    spk, col, text = INTRO_LINES[step]
    lbl = FONT_MD.render(spk + ":", True, col)
    screen.blit(lbl, (box.x+14, box.y+12))

    # word-wrap text
    words = text.split()
    line, lines_out, lx, ly = "", [], box.x+14, box.y+36
    for w in words:
        test = line + w + " "
        if FONT_SM.size(test)[0] > box.w - 28:
            lines_out.append(line); line = w + " "
        else:
            line = test
    lines_out.append(line)
    for l in lines_out:
        screen.blit(FONT_SM.render(l, True, (200,230,255)), (lx, ly)); ly += 18

    hint = FONT_SM.render("SPACE to continue", True, GREY)
    screen.blit(hint, (box.right - hint.get_width() - 12, box.bottom - 18))


# ══════════════════════════════════════════════════════════════════════════════
#  PLATFORMER
# ══════════════════════════════════════════════════════════════════════════════

class PlatformPlayer:
    W, H_P = 20, 24
    SPEED   = 3.2
    JUMP    = -10.5
    GRAV    = 0.45

    def __init__(self):
        self.x = 60.0; self.y = 200.0
        self.vx = 0.0; self.vy = 0.0
        self.on_ground = False
        self.facing    = 1
        self.anim      = 0.0
        self.attacking = False
        self.atk_timer = 0
        self.invincible = 0
        self.hp = GS.hp

    def respawn(self):
        self.x = 60; self.y = 200
        self.vx = self.vy = 0
        self.hp = GS.hp = GS.max_hp

    def update(self, keys, platforms):
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: self.vx = -self.SPEED; self.facing = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.vx =  self.SPEED; self.facing =  1
        else: self.vx *= 0.65

        self.vy += self.GRAV
        self.x  += self.vx
        self.y  += self.vy
        self.on_ground = False

        for pl in platforms:
            if (self.x + self.W > pl.x and self.x < pl.x + pl.w and
                    self.y + self.H_P > pl.y and self.y + self.H_P < pl.y + pl.h + 12 and self.vy >= 0):
                self.y = pl.y - self.H_P
                self.vy = 0; self.on_ground = True

        if self.vx != 0 and self.on_ground:
            self.anim += 0.18
        if self.attacking:
            self.atk_timer -= 1
            if self.atk_timer <= 0: self.attacking = False
        if self.invincible > 0: self.invincible -= 1

    def draw(self, cam_x):
        draw_ninja(screen, int(self.x) - cam_x, int(self.y), self.facing, self.anim, self.attacking, self.invincible)


class PlatEnemy:
    def __init__(self, platform):
        self.pl = platform
        self.x  = float(platform.x + random.randint(10, max(11, platform.w - 30)))
        self.y  = float(platform.y - 20)
        self.vx = random.choice([-1, 1]) * 0.9
        self.vy = 0.0
        self.on_ground = False
        self.hp  = 1
        self.max_hp = 1
        self.anim = random.uniform(0, math.pi * 2)

    def update(self, platforms):
        self.anim += 0.1
        self.x += self.vx
        self.vy += 0.45
        self.y  += self.vy
        self.on_ground = False
        for pl in platforms:
            if (self.x+18 > pl.x and self.x < pl.x+pl.w and
                    self.y+20 > pl.y and self.y+20 < pl.y+pl.h+12 and self.vy >= 0):
                self.y = pl.y - 20; self.vy = 0; self.on_ground = True
        if self.x < self.pl.x or self.x > self.pl.x + self.pl.w - 18:
            self.vx *= -1

    def draw(self, cam_x):
        draw_small_dragon(screen, int(self.x)-cam_x, int(self.y), self.anim, self.hp, self.max_hp)


class PlatCoin:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.collected = False
        self.t = random.uniform(0, math.pi*2)

    def draw(self, cam_x):
        if self.collected: return
        self.t += 0.08
        bob = int(math.sin(self.t) * 3)
        cx = int(self.x) - cam_x
        pygame.draw.rect(screen, GOLD,     (cx-5, self.y-5+bob, 10, 10))
        pygame.draw.rect(screen, GOLDDARK, (cx-3, self.y-3+bob,  6,  6))


class Door:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.w, self.h = 36, 52
        self.t = 0

    def update(self): self.t += 0.05

    def draw(self, cam_x):
        dx = self.x - cam_x
        pygame.draw.rect(screen, (50, 22,  8),  (dx,      self.y,      self.w, self.h))
        pygame.draw.rect(screen, (90, 45, 18),  (dx+3,    self.y+3,    self.w-6, self.h-6))
        for i in range(4):
            pygame.draw.rect(screen, (30, 10, 3), (dx+5, self.y+5+i*12, self.w-10, 8))
        pygame.draw.rect(screen, GOLD, (dx+self.w//2-3, self.y+self.h//2-3, 6, 6))
        glow = int(abs(math.sin(self.t)) * 8)
        pygame.draw.rect(screen, PURPLE, (dx+self.w//2-2, self.y-8-glow, 4, 8))
        pygame.draw.rect(screen, PURPLT, (dx+self.w//2-1, self.y-12-glow, 2, 5))


def build_platformer(level):
    # Max safe horizontal gap = ~110px  (physics: jump covers ~149px max)
    # Max safe vertical drop  = ~80px   (player can't jump UP more than ~110px)
    # All gaps here stay within those limits so every jump is possible.

    # Each entry: (x, y, width, height)
    # Y increases downward. Ground level is ~360. Higher Y = lower on screen.
    layout = [
        # starting ground — nice and wide so player has room to get moving
        (0,    360, 380, 60),
        # first few easy hops, gentle steps up
        (430,  320, 120, 22),
        (590,  290, 100, 22),
        (730,  310, 110, 22),
        (880,  270, 100, 22),
        # mid section — slight up/down rhythm
        (1020, 300, 120, 22),
        (1170, 260, 100, 22),
        (1310, 290, 110, 22),
        (1450, 250, 100, 22),
        # harder section — gaps get a bit wider on higher levels
        (1590, 280, 100, 22),
        (1730, 240, 90,  22),
        (1860, 270, 110, 22),
        (1990, 300, 100, 22),
        (2110, 260, 100, 22),
        # final approach — wide safe platform with the door on it
        (2160, 300, 300, 70),
    ]

    # On higher levels, shrink some platform widths and add small extra hops
    if level >= 2:
        layout[6]  = (1170, 250, 80, 22)   # a bit trickier
        layout[10] = (1730, 230, 75, 22)
    if level >= 3:
        layout[8]  = (1590, 270, 70, 22)
        layout[12] = (2110, 245, 75, 22)
    if level >= 4:
        layout.insert(13, (2180, 220, 60, 22))  # extra hop before final
    if level >= 5:
        layout.insert(14, (2260, 250, 60, 22))  # one more tricky hop

    base_plats = [pygame.Rect(x, y, w, h) for x, y, w, h in layout]

    # Door sits on top of the final wide platform
    final = base_plats[-1]
    door_x = final.x + final.w // 2 - 18   # centred on final platform
    door_y = final.y - 52                   # sitting ON the platform surface
    door   = Door(door_x, door_y)

    world_w = final.x + final.w + 60       # world ends just past the door

    # Enemies — only on platforms wide enough to pace on
    enemies = []
    usable  = [p for p in base_plats if p.w >= 70]
    for i in range(4 + level * 2):
        pl = random.choice(usable)
        enemies.append(PlatEnemy(pl))

    # Coins scattered across all platforms
    coins = []
    for i in range(8 + level * 3):
        pl  = random.choice(base_plats)
        cx  = pl.x + random.randint(8, max(9, pl.w - 16))
        coins.append(PlatCoin(cx, pl.y - 18))

    return base_plats, door, enemies, coins, world_w


class PlatformerScene:
    def __init__(self, level):
        self.level = level
        self.platforms, self.door, self.enemies, self.coins, self.world_w = build_platformer(level)
        self.player = PlatformPlayer()
        self.camera_x = 0.0

    def update(self, keys, events):
        self.player.update(keys, self.platforms)
        self.door.update()
        for e in self.enemies: e.update(self.platforms)

        p = self.player
        # fall into void
        if p.y > H + 60:
            GS.lives -= 1
            GS.add_particles(p.x, H-40, RED, 14)
            if GS.lives <= 0:
                GS.mode = "dead"
                GS.set_msg("You fell into the void. The scroll is lost...")
            else:
                p.respawn()
                GS.set_msg(f"Fell! Lives left: {GS.lives}")
            return

        # attack
        if p.attacking:
            ax = p.x + (p.W + 4 if p.facing > 0 else -18)
            for e in self.enemies:
                if e.hp > 0 and abs(e.x - ax) < 24 and abs(e.y - p.y) < 28:
                    e.hp -= GS.weapon_dmg()
                    GS.add_particles(e.x, e.y, RED, 6)
                    if e.hp <= 0: GS.coins += 3

        self.enemies = [e for e in self.enemies if e.hp > 0]

        # enemy collision
        if p.invincible <= 0:
            for e in self.enemies:
                if abs(e.x - p.x) < 22 and abs(e.y - p.y) < 26:
                    p.hp -= 1; p.invincible = 60; GS.hp = p.hp
                    GS.add_particles(p.x, p.y, RED, 10)
                    if p.hp <= 0:
                        GS.lives -= 1
                        if GS.lives <= 0:
                            GS.mode = "dead"
                            GS.set_msg("Slain on the overworld. The darkness wins...")
                        else:
                            p.respawn()
                            GS.set_msg(f"Defeated! Lives: {GS.lives}")
                    break

        # collect coins
        for c in self.coins:
            if not c.collected and abs(c.x - p.x) < 18 and abs(c.y - p.y) < 22:
                c.collected = True; GS.coins += 1

        # enter door
        if (p.x + p.W > self.door.x and p.x < self.door.x + self.door.w and
                p.y + p.H_P > self.door.y and p.y < self.door.y + self.door.h):
            GS.mode = "dungeon"
            GS.set_msg(f"Entering Tomb {self.level}...")
            return

        # camera
        target = p.x - W // 2
        self.camera_x += (target - self.camera_x) * 0.1
        self.camera_x = max(0, min(self.world_w - W, self.camera_x))

    def draw(self):
        cam = int(self.camera_x)

        # background
        screen.fill(DKBLUE)
        # stars
        for i in range(80):
            sx = (i * 173 - cam // 4) % W
            sy = (i * 97) % (H - 80)
            c = BLUE2 if i % 4 == 0 else STONE
            screen.fill(c, (sx, sy, 2, 2))
        # ghostly mist bands
        for i in range(3):
            s = pygame.Surface((W, 30), pygame.SRCALPHA)
            alpha = int(20 + math.sin(GS.frame * 0.02 + i) * 8)
            s.fill((*GHOSTG, alpha))
            screen.blit(s, (0, 100 + i * 90))

        # platforms
        for pl in self.platforms:
            px = pl.x - cam
            if -pl.w < px < W + pl.w:
                pygame.draw.rect(screen, GREEN1,  (px, pl.y, pl.w, pl.h))
                for i in range(0, pl.w, 12):
                    c = (35, 90, 30) if (i//12)%2==0 else GREEN1
                    pygame.draw.rect(screen, c, (px+i, pl.y, 12, 6))
                pygame.draw.rect(screen, (8, 28, 8), (px, pl.y, pl.w, 2))

        self.door.draw(cam)
        for c in self.coins: c.draw(cam)
        for e in self.enemies: e.draw(cam)
        self.player.draw(cam)

        # particles
        for pt in GS.particles: pt.draw(screen, cam)

        # hp bar
        hp_pct = max(0, self.player.hp / GS.max_hp)
        pygame.draw.rect(screen, REDDARK, (12, 12, 100, 10))
        bar_col = (70,220,70) if hp_pct > 0.5 else ORANGE if hp_pct > 0.25 else RED
        pygame.draw.rect(screen, bar_col, (12, 12, int(100*hp_pct), 10))
        pygame.draw.rect(screen, WHITE,   (12, 12, 100, 10), 1)
        screen.blit(FONT_SM.render("HP", True, WHITE), (14, 10))


# ══════════════════════════════════════════════════════════════════════════════
#  DUNGEON
# ══════════════════════════════════════════════════════════════════════════════

COLS_D, ROWS_D = 22, 15
TILE_D = 32

class DungeonPlayer:
    def __init__(self):
        self.r = 1; self.c = 1
        self.hp = GS.hp; self.max_hp = GS.max_hp
        self.facing = 1
        self.invincible = 0
        self.atk_flash  = 0
        self.move_timer = 0

    def try_move(self, dr, dc, dungeon):
        nr, nc = self.r + dr, self.c + dc
        if not dungeon.is_wall(nr, nc):
            self.r, self.c = nr, nc
            self.facing = dc if dc != 0 else self.facing
            return True
        return False


class DungeonEnemy:
    def __init__(self, r, c, level, is_boss=False):
        self.r, self.c = r, c
        self.is_boss   = is_boss
        self.hp   = (20 if is_boss else 1 + level // 2)
        self.max_hp = self.hp
        self.dr, self.dc = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        self.timer = 0
        self.speed = max(4, 14 - level * 2) if not is_boss else 8
        self.anim  = 0.0
        self.phase = 0  # boss phases

    def update(self, dungeon, player):
        self.timer += 1
        self.anim  += 0.05
        if self.timer < self.speed: return
        self.timer = 0

        # boss tracks player more aggressively
        if self.is_boss and self.hp < self.max_hp // 2:
            self.speed = max(3, self.speed - 1)  # speeds up at half hp
            dr = 1 if player.r > self.r else -1 if player.r < self.r else 0
            dc = 1 if player.c > self.c else -1 if player.c < self.c else 0
            if abs(player.r - self.r) > abs(player.c - self.c): dc = 0
            else: dr = 0
            self.dr, self.dc = dr, dc

        nr, nc = self.r + self.dr, self.c + self.dc
        if dungeon.is_wall(nr, nc):
            dirs = [(1,0),(-1,0),(0,1),(0,-1)]
            random.shuffle(dirs)
            for d in dirs:
                tnr, tnc = self.r + d[0], self.c + d[1]
                if not dungeon.is_wall(tnr, tnc):
                    self.dr, self.dc = d
                    nr, nc = tnr, tnc
                    break
        if not dungeon.is_wall(nr, nc):
            self.r, self.c = nr, nc


class Dungeon:
    def __init__(self, level):
        self.level  = level
        self.is_boss_level = (level == 5)
        self.map    = self._gen_map(level)
        self.coins  = []
        self.exit   = None
        self.scroll_pos = None
        self.enemies: list[DungeonEnemy] = []
        self._place_objects()
        self.player = DungeonPlayer()
        self.move_cd = 0
        self.off_x = (W - COLS_D * TILE_D) // 2
        self.off_y = (H - ROWS_D * TILE_D) // 2 - 16

    def _gen_map(self, level):
        m = [[1]*COLS_D for _ in range(ROWS_D)]
        for r in range(1, ROWS_D-1):
            for c in range(1, COLS_D-1):
                m[r][c] = 0
        walls = 24 + level * 5
        for _ in range(walls):
            r = random.randint(2, ROWS_D-3)
            c = random.randint(2, COLS_D-3)
            if r > 2 or c > 2: m[r][c] = 1
        return m

    def is_wall(self, r, c):
        return r < 0 or r >= ROWS_D or c < 0 or c >= COLS_D or self.map[r][c] == 1

    def _occ(self):
        taken = [(1,1)]
        taken += [(e.r, e.c) for e in self.enemies]
        taken += [(coin[0], coin[1]) for coin in self.coins]
        if self.exit: taken.append(self.exit)
        return taken

    def _empty_cell(self):
        occ = self._occ()
        for _ in range(500):
            r = random.randint(1, ROWS_D-2)
            c = random.randint(1, COLS_D-2)
            if not self.is_wall(r, c) and (r,c) not in occ:
                return (r, c)
        return (2, 2)

    def _place_objects(self):
        # coins
        for _ in range(5 + self.level):
            p = self._empty_cell()
            self.coins.append([p[0], p[1], False])  # r, c, collected

        # exit or scroll
        if self.is_boss_level:
            self.scroll_pos = self._empty_cell()
        else:
            self.exit = self._empty_cell()

        # enemies
        n = 3 + self.level * 2
        for i in range(n):
            p = self._empty_cell()
            is_boss = self.is_boss_level and i == 0
            self.enemies.append(DungeonEnemy(p[0], p[1], self.level, is_boss=is_boss))

    def update(self, keys, events):
        p = self.player
        self.move_cd = max(0, self.move_cd - 1)

        if self.move_cd == 0:
            dr = dc = 0
            if keys[pygame.K_UP]    or keys[pygame.K_w]: dr = -1
            elif keys[pygame.K_DOWN]  or keys[pygame.K_s]: dr =  1
            elif keys[pygame.K_LEFT]  or keys[pygame.K_a]: dc = -1
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]: dc =  1
            if dr or dc:
                p.try_move(dr, dc, self)
                self.move_cd = 9

        # attack with Z
        for ev in events:
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_z:
                p.atk_flash = 12
                for e in self.enemies:
                    if abs(e.r - p.r) + abs(e.c - p.c) == 1:
                        e.hp -= GS.weapon_dmg()
                        GS.add_particles(
                            self.off_x + e.c*TILE_D + TILE_D//2,
                            self.off_y + e.r*TILE_D + TILE_D//2, RED, 8)
                self.enemies = [e for e in self.enemies if e.hp > 0]

        if p.atk_flash > 0: p.atk_flash -= 1

        # enemy movement + collision
        for e in self.enemies:
            e.update(self, p)
            if p.invincible <= 0 and e.r == p.r and e.c == p.c:
                dmg = 2 if e.is_boss else 1
                p.hp -= dmg; p.invincible = 40; GS.hp = p.hp
                GS.add_particles(
                    self.off_x + p.c*TILE_D + TILE_D//2,
                    self.off_y + p.r*TILE_D + TILE_D//2, RED, 10)
                if p.hp <= 0:
                    GS.lives -= 1
                    if GS.lives <= 0:
                        GS.mode = "dead"
                        GS.set_msg("The darkness consumes you. The scroll is lost...")
                    else:
                        p.r, p.c = 1, 1
                        p.hp = GS.max_hp; GS.hp = GS.max_hp
                        GS.set_msg(f"Slain! Lives: {GS.lives}")

        if p.invincible > 0: p.invincible -= 1

        # collect coins
        for coin in self.coins:
            if not coin[2] and coin[0] == p.r and coin[1] == p.c:
                coin[2] = True; GS.coins += 1

        # scroll pickup (boss level — need all enemies dead)
        if self.scroll_pos and not GS.scroll_found:
            if p.r == self.scroll_pos[0] and p.c == self.scroll_pos[1]:
                if len(self.enemies) == 0:
                    GS.scroll_found = True
                    GS.mode = "win"
                else:
                    GS.set_msg("Defeat Vorthar first!", 90)

        # exit (non-boss)
        if self.exit and p.r == self.exit[0] and p.c == self.exit[1]:
            if len(self.enemies) == 0:
                GS.level += 1
                GS.hp = p.hp
                GS.mode = "platformer"
                GS.set_msg(f"Tomb {self.level} cleared! Ascending...")
            else:
                GS.set_msg("Defeat all enemies first!", 90)

    def draw(self):
        screen.fill((4, 6, 14))
        ox, oy = self.off_x, self.off_y

        for r in range(ROWS_D):
            for c in range(COLS_D):
                tx, ty = ox + c*TILE_D, oy + r*TILE_D
                if self.map[r][c]:
                    pygame.draw.rect(screen, STONE,   (tx, ty, TILE_D, TILE_D))
                    pygame.draw.rect(screen, STONELT, (tx+1, ty+1, TILE_D-2, 5))
                    pygame.draw.rect(screen, STONELT, (tx+1, ty+1, 5, TILE_D-2))
                else:
                    c2 = (12, 22, 36) if (r+c)%2==0 else (10, 18, 30)
                    pygame.draw.rect(screen, c2, (tx, ty, TILE_D, TILE_D))
                    # ghostly green shimmer
                    alpha = int(12 + math.sin(GS.frame*0.03+r*0.3+c*0.4)*6)
                    s = pygame.Surface((TILE_D, TILE_D), pygame.SRCALPHA)
                    s.fill((*GHOSTG2, alpha))
                    screen.blit(s, (tx, ty))

        # coins
        t = GS.frame * 0.08
        for coin in self.coins:
            if coin[2]: continue
            cx = ox + coin[1]*TILE_D + TILE_D//2
            cy = oy + coin[0]*TILE_D + TILE_D//2 + int(math.sin(t + coin[1])*3)
            pygame.draw.rect(screen, GOLD,     (cx-5, cy-5, 10, 10))
            pygame.draw.rect(screen, GOLDDARK, (cx-3, cy-3,  6,  6))

        # scroll
        if self.scroll_pos and not GS.scroll_found:
            sr, sc = self.scroll_pos
            sx = ox + sc*TILE_D + TILE_D//2
            sy = oy + sr*TILE_D + TILE_D//2
            g = int(abs(math.sin(GS.frame*0.05))*30)
            s = pygame.Surface((28, 28), pygame.SRCALPHA)
            s.fill((255, 220, 80, 40 + g))
            screen.blit(s, (sx-14, sy-14))
            pygame.draw.rect(screen, GOLD, (sx-6, sy-8, 12, 16))
            pygame.draw.rect(screen, GOLDDARK, (sx-6, sy-8, 12, 3))
            pygame.draw.rect(screen, GOLDDARK, (sx-6, sy+5, 12, 3))
            screen.blit(FONT_SM.render("S", True, BLACK), (sx-4, sy-5))

        # exit door
        if self.exit:
            er, ec = self.exit
            ex = ox + ec*TILE_D + TILE_D//2 - 14
            ey = oy + er*TILE_D + TILE_D//2 - 20
            if len(self.enemies) == 0:
                pygame.draw.rect(screen, (50,22,8), (ex, ey, 28, 40))
                pygame.draw.rect(screen, (90,45,18),(ex+3,ey+3,22,34))
                glow = int(abs(math.sin(GS.frame*0.06))*6)
                pygame.draw.rect(screen, PURPLE, (ex+11, ey-8-glow, 6, 10))
                pygame.draw.rect(screen, GOLD, (ex+11,ey+16,6,6))
            else:
                pygame.draw.rect(screen, (28,14,5), (ex, ey, 28, 40))
                pygame.draw.rect(screen, (50,25,10),(ex+3,ey+3,22,34))

        # enemies
        p = self.player
        for e in self.enemies:
            ex2 = ox + e.c*TILE_D + TILE_D//2 - 9
            ey2 = oy + e.r*TILE_D + TILE_D//2 - 10
            if e.is_boss:
                draw_boss_dragon(screen, ox + e.c*TILE_D - 20, oy + e.r*TILE_D - 30, e.anim, e.hp, e.max_hp)
            else:
                draw_small_dragon(screen, ex2, ey2, e.anim, e.hp, e.max_hp)

        # player
        px2 = ox + p.c*TILE_D + TILE_D//2 - 10
        py2 = oy + p.r*TILE_D + TILE_D//2 - 12
        draw_ninja(screen, px2, py2, p.facing, 0, p.atk_flash > 0, p.invincible)

        # particles
        for pt in GS.particles: pt.draw(screen)

        # hp bar
        hp_pct = max(0, p.hp / p.max_hp)
        pygame.draw.rect(screen, REDDARK, (12, 12, 100, 10))
        bar_col = (70,220,70) if hp_pct > 0.5 else ORANGE if hp_pct > 0.25 else RED
        pygame.draw.rect(screen, bar_col, (12, 12, int(100*hp_pct), 10))
        pygame.draw.rect(screen, WHITE,   (12, 12, 100, 10), 1)
        screen.blit(FONT_SM.render("HP", True, WHITE), (14, 10))

        # enemy count
        alive = len(self.enemies)
        ec_col = GHOSTG if alive == 0 else RED
        screen.blit(FONT_SM.render(f"enemies: {alive}", True, ec_col), (W-110, 12))

        # boss level tip
        if self.is_boss_level and self.scroll_pos and not GS.scroll_found:
            if alive > 0:
                lbl = FONT_MD.render("DEFEAT VORTHAR TO CLAIM THE SCROLL!", True, RED)
            else:
                lbl = FONT_MD.render("TAKE THE SACRED SCROLL!", True, GOLD)
            screen.blit(lbl, (W//2 - lbl.get_width()//2, H-34))


# ══════════════════════════════════════════════════════════════════════════════
#  SHOP
# ══════════════════════════════════════════════════════════════════════════════

SHOP_ITEMS = [
    {"key": pygame.K_1, "label": "1", "name": "Ghostwood Bow",  "cost":  5, "weapon": "bow",   "desc": "+2 attack  |  ranged shots"},
    {"key": pygame.K_2, "label": "2", "name": "Shadow Staff",   "cost": 14, "weapon": "staff", "desc": "+3 attack  |  arcane power"},
    {"key": pygame.K_3, "label": "3", "name": "Dragon Herb x2", "cost":  4, "weapon": None,    "desc": "Restore +2 HP instantly"},
    {"key": pygame.K_4, "label": "4", "name": "Ninja Scroll",   "cost":  8, "weapon": None,    "desc": "+1 max HP permanently"},
]

def draw_shop():
    screen.fill((3, 8, 20))
    # border box
    box = pygame.Rect(W//2-240, 30, 480, H-60)
    pygame.draw.rect(screen, (8, 22, 40),  box)
    pygame.draw.rect(screen, BLUE2,        box, 2)

    title = FONT_LG.render("~ SHADOW MARKET ~", True, BLUE3)
    screen.blit(title, (W//2 - title.get_width()//2, 48))

    coins_lbl = FONT_MD.render(f"Your coins:  {GS.coins}    Weapon: {GS.weapon.upper()}", True, GOLD)
    screen.blit(coins_lbl, (W//2 - coins_lbl.get_width()//2, 88))

    for i, item in enumerate(SHOP_ITEMS):
        iy   = 130 + i * 82
        owned = (item["weapon"] and GS.weapon == item["weapon"])
        bg   = (10, 35, 20) if owned else (8, 18, 34)
        bd   = GHOSTG if owned else BLUE1
        pygame.draw.rect(screen, bg, (box.x+16, iy, box.w-32, 70))
        pygame.draw.rect(screen, bd, (box.x+16, iy, box.w-32, 70), 1)

        name_col = GHOSTG if owned else WHITE
        screen.blit(FONT_MD.render(f"[{item['label']}]  {item['name']}", True, name_col), (box.x+30, iy+10))
        screen.blit(FONT_SM.render(item["desc"], True, BLUE2), (box.x+30, iy+34))
        cost_str = "OWNED" if owned else f"Cost: {item['cost']} coins"
        cost_col = GHOSTG if owned else GOLD
        cost_lbl = FONT_SM.render(cost_str, True, cost_col)
        screen.blit(cost_lbl, (box.right - cost_lbl.get_width() - 30, iy+22))

    hint = FONT_SM.render("Press S or ESC to close shop", True, GREY)
    screen.blit(hint, (W//2 - hint.get_width()//2, box.bottom - 26))

def handle_shop_input(ev):
    for item in SHOP_ITEMS:
        if ev.key == item["key"]:
            if item["weapon"] and GS.weapon == item["weapon"]:
                GS.set_msg("Already owned!"); return
            if GS.coins < item["cost"]:
                GS.set_msg("Not enough coins!"); return
            GS.coins -= item["cost"]
            if item["weapon"]:
                GS.weapon = item["weapon"]
                GS.set_msg(f"{item['name']} equipped!")
            elif item["name"].startswith("Dragon"):
                heal = min(2, GS.max_hp - GS.hp)
                GS.hp = min(GS.hp + 2, GS.max_hp)
                GS.set_msg(f"+{heal} HP restored!")
            elif "Scroll" in item["name"]:
                GS.max_hp += 1; GS.hp = min(GS.hp+1, GS.max_hp)
                GS.set_msg("Max HP increased!")


# ══════════════════════════════════════════════════════════════════════════════
#  WIN / DEAD SCREENS
# ══════════════════════════════════════════════════════════════════════════════

def draw_win():
    screen.fill(BLACK)
    t = GS.frame
    for i in range(100):
        x = (i*177 + t) % W
        y = (i*113 + t//2) % H
        c = [BLUE3, GHOSTG, PURPLE][i%3]
        screen.fill(c, (x, y, 3, 3))
    draw_ninja(screen, W//2-10, H//2-80, 1, t*0.1, False, False)
    # scroll in hand
    pygame.draw.rect(screen, GOLD, (W//2+14, H//2-84, 18, 28))
    pygame.draw.rect(screen, GOLDDARK, (W//2+14, H//2-84, 18, 5))
    pygame.draw.rect(screen, GOLDDARK, (W//2+14, H//2-61, 18, 5))

    for i, (txt, col, size) in enumerate([
        ("THE SACRED SCROLL IS YOURS!", BLUE3, FONT_LG),
        ("The ghost dragons are banished. Peace returns.", GHOSTG, FONT_MD),
        (f"Coins collected: {GS.coins}   Lives remaining: {GS.lives}", GOLD, FONT_SM),
        ("PRESS R TO PLAY AGAIN", GREY, FONT_SM),
    ]):
        lbl = size.render(txt, True, col)
        screen.blit(lbl, (W//2-lbl.get_width()//2, H//2+30+i*34))

def draw_dead():
    screen.fill((6, 0, 2))
    t = GS.frame
    for i in range(40):
        x = (i*193 + t//2) % W
        y = (i*137) % H
        a = int(160 + math.sin(t*0.05+i)*60)
        s = pygame.Surface((4,4), pygame.SRCALPHA)
        s.fill((180, 20, 40, a))
        screen.blit(s, (x, y))

    for i, (txt, col, size) in enumerate([
        ("YOUR QUEST HAS ENDED", RED,  FONT_XL),
        ("The scroll remains in darkness...", (180,80,80), FONT_MD),
        (f"You reached Tomb {GS.level}  |  Coins: {GS.coins}", GREY, FONT_SM),
        ("PRESS R TO TRY AGAIN", GREY, FONT_SM),
    ]):
        lbl = size.render(txt, True, col)
        screen.blit(lbl, (W//2-lbl.get_width()//2, H//2-60+i*56))


# ══════════════════════════════════════════════════════════════════════════════
#  HUD
# ══════════════════════════════════════════════════════════════════════════════

def draw_hud():
    # lives
    lives_str = "♥" * GS.lives + "♡" * max(0, 3-GS.lives)
    screen.blit(FONT_SM.render(lives_str, True, (220, 60, 90)), (W//2-28, 6))
    # coins
    screen.blit(FONT_SM.render(f"✦ {GS.coins}", True, GOLD), (W-80, 6))
    # level
    lbl = f"LVL {GS.level}  |  {'TOMB' if GS.mode=='dungeon' else 'OVERWORLD'}"
    screen.blit(FONT_SM.render(lbl, True, BLUE2), (W//2-50, H-20))
    # weapon
    screen.blit(FONT_SM.render(GS.weapon.upper(), True, GHOSTG), (6, H-20))
    # shop hint
    screen.blit(FONT_SM.render("S=shop", True, GREY), (W-56, H-20))
    # message
    if GS.msg_timer > 0:
        alpha = min(255, GS.msg_timer * 4)
        msg_s = pygame.Surface((W, 22), pygame.SRCALPHA)
        msg_s.fill((0, 0, 0, 120))
        screen.blit(msg_s, (0, H//2 - 11))
        lbl = FONT_MD.render(GS.message, True, WHITE)
        screen.blit(lbl, (W//2-lbl.get_width()//2, H//2-10))
        GS.msg_timer -= 1


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN LOOP
# ══════════════════════════════════════════════════════════════════════════════

def main():
    GS.reset()

    plat_scene  : PlatformerScene | None = None
    dungeon_scene: Dungeon        | None = None

    def enter_platformer():
        nonlocal plat_scene
        plat_scene = PlatformerScene(GS.level)
        GS.mode = "platformer"
        GS.set_msg(f"Level {GS.level} — reach the ancient door!")

    def enter_dungeon():
        nonlocal dungeon_scene
        dungeon_scene = Dungeon(GS.level)
        GS.mode = "dungeon"
        if GS.level == 5:
            GS.set_msg("TOMB OF VOID — Vorthar awaits. Find the Sacred Scroll!")
        else:
            GS.set_msg(f"Tomb {GS.level} — defeat all enemies then find the exit.")

    while True:
        keys   = pygame.key.get_pressed()
        events = pygame.event.get()

        for ev in events:
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                # global restart
                if ev.key == pygame.K_r:
                    GS.reset()
                    plat_scene = dungeon_scene = None
                    continue

                # intro advance
                if GS.mode == "intro":
                    if ev.key in (pygame.K_SPACE, pygame.K_z):
                        GS.intro_step += 1
                        if GS.intro_step >= len(INTRO_LINES):
                            enter_platformer()

                # shop toggle
                elif ev.key == pygame.K_s:
                    if GS.mode in ("platformer", "dungeon"):
                        GS.prev_mode = GS.mode
                        GS.mode = "shop"
                    elif GS.mode == "shop":
                        GS.mode = GS.prev_mode
                elif GS.mode == "shop":
                    if ev.key == pygame.K_ESCAPE:
                        GS.mode = GS.prev_mode
                    else:
                        handle_shop_input(ev)

                # jump
                elif GS.mode == "platformer" and plat_scene:
                    if ev.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                        p = plat_scene.player
                        if p.on_ground:
                            p.vy = p.JUMP; p.on_ground = False
                    if ev.key == pygame.K_z and plat_scene:
                        p = plat_scene.player
                        p.attacking = True; p.atk_timer = 14

                elif GS.mode in ("win", "dead"):
                    if ev.key == pygame.K_r:
                        GS.reset()
                        plat_scene = dungeon_scene = None

        # ── update ────────────────────────────────────────────────────────────
        GS.frame += 1
        GS.particles = [p for p in GS.particles if p.life > 0]
        for pt in GS.particles: pt.update()

        if GS.mode == "intro":
            pass

        elif GS.mode == "platformer":
            if plat_scene is None: enter_platformer()
            if GS.mode == "platformer":
                plat_scene.update(keys, events)
            if GS.mode == "dungeon":
                enter_dungeon()

        elif GS.mode == "dungeon":
            if dungeon_scene is None or dungeon_scene.level != GS.level:
                enter_dungeon()
            if GS.mode == "dungeon":
                dungeon_scene.update(keys, events)
            if GS.mode == "platformer":
                enter_platformer()

        # ── draw ──────────────────────────────────────────────────────────────
        screen.fill(BLACK)

        if GS.mode == "intro":
            draw_intro()
        elif GS.mode == "platformer" and plat_scene:
            plat_scene.draw()
            draw_hud()
        elif GS.mode == "dungeon" and dungeon_scene:
            dungeon_scene.draw()
            draw_hud()
        elif GS.mode == "shop":
            draw_shop()
        elif GS.mode == "win":
            draw_win()
        elif GS.mode == "dead":
            draw_dead()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()