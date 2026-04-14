# Shadow Scroll – Game Design Document

## 🎮 Overview

Shadow Scroll is a 2D pixel game developed in Python using the Pygame library.  
It combines a side-scrolling platformer with a top-down dungeon crawler.

The game is single-player and level-based, featuring combat, exploration, and progression through multiple interconnected gameplay styles.

---

## 🧩 Technology

- Language: Python 3
- Library: Pygame
- No additional external frameworks planned (optional future expansion possible)

---

## 🎯 Core Gameplay

The game is structured around levels that alternate between:

### 🏃 Platformer Mode
- Side-scrolling gameplay
- Player moves through linear levels
- Enemies patrol platforms
- End of level leads to dungeon entrance (door system)

### 🏰 Dungeon Mode
- Top-down exploration
- Rooms connected through doors
- Combat with enemies and bosses
- Collect coins and items
- Find progression items and collectibles

---

## 🧑 Player System

The player controls a pixel ninja character.

### Attributes:
- Health system
- Main melee weapon (sword)
- Upgradable weapons system

### Weapons:
- Sword (default weapon)
- Staff (shop upgrade)
- Bow (shop upgrade)
- Additional weapons planned

---

## 👾 Enemies

### Platformer Enemies:
- Small red dragon enemies
- Patrol back and forth on platforms
- Damage player on contact

### Dungeon Enemies:
- Red dragon henchmen
- Patrol dungeon rooms
- Chase the player when detected

### Bosses:
- Strong enemies at key progression points
- Block advancement until defeated

---

## 🛒 Shop System

- Located in dungeon areas
- Uses collected coins as currency
- Allows weapon upgrades and item purchases
- Not accessible during boss fights

---

## 🧭 Progression System

- Game is divided into multiple levels (5+ planned)
- Each level contains both platformer and dungeon sections
- Progress is unlocked through doors between modes

### Checkpoints:
- Platformer checkpoints for respawning
- Dungeon checkpoints at room entrances

### Save System (planned):
- Account-based progression system
- Level selection menu after unlocking stages

---

## 🗺️ Game Structure

- Linear level progression with increasing difficulty
- Mix of exploration and platforming
- Reward-based progression system (coins + upgrades)

---

## 🎵 Audio & Visuals (Optional / Planned)

- Pixel art visual style
- Dark fantasy aesthetic
- Possible future additions:
  - Sound effects
  - Background music
  - Animation improvements

---

## 🚀 Future Ideas

- Multiplayer mode (optional future feature)
- Expanded weapon system
- More enemy types
- More complex dungeon layouts
- Story expansion

---

## ⚙️ Summary

Shadow Scroll is designed as a hybrid action-adventure game combining platforming and dungeon exploration into a single continuous experience, with progression, upgrades, and increasing difficulty over multiple levels.