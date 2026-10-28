"""Dice Dungeon: a tiny terminal RPG.

Run with:  python dungeon.py
Requires Python 3.7+ (standard library only).
"""

import json
import random
from dataclasses import dataclass, asdict
from pathlib import Path

# Where progress is saved (created next to wherever you run the script)
SAVE_FILE = Path("save.json")


# ---------------------------------------------------------------------------
# Part 1: The player
# ---------------------------------------------------------------------------
@dataclass
class Player:
    name: str
    hp: int = 30
    gold: int = 0
    level: int = 1

    def is_alive(self):
        return self.hp > 0

    def attack(self):
        # Roll 2-6, plus your level as a bonus
        return random.randint(2, 6) + self.level


# ---------------------------------------------------------------------------
# Part 2: Monsters and saving
# ---------------------------------------------------------------------------
MONSTERS = {
    "Slime": {"hp": 8, "damage": (1, 3), "gold": (1, 5)},
    "Goblin": {"hp": 12, "damage": (2, 4), "gold": (3, 8)},
    "Skeleton": {"hp": 16, "damage": (3, 5), "gold": (5, 12)},
}


def save_game(player):
    SAVE_FILE.write_text(json.dumps(asdict(player)))


def load_game():
    if SAVE_FILE.exists():
        data = json.loads(SAVE_FILE.read_text())
        return Player(**data)
    return None


# ---------------------------------------------------------------------------
# Part 3: The fight
# ---------------------------------------------------------------------------
def fight(player):
    name = random.choice(list(MONSTERS))
    stats = MONSTERS[name]
    monster_hp = stats["hp"]
    print(f"\nA wild {name} appears!")

    while monster_hp > 0 and player.is_alive():
        choice = input("[a]ttack or [r]un? ").strip().lower()

        if choice == "r":
            if random.random() < 0.5:
                print("You escaped!")
                return
            print("Couldn't escape!")
        elif choice == "a":
            dmg = player.attack()
            monster_hp -= dmg
            print(f"You hit the {name} for {dmg}.")
        else:
            print("Type 'a' or 'r'.")
            continue

        # The monster strikes back only if it's still standing
        if monster_hp > 0:
            hit = random.randint(*stats["damage"])
            player.hp -= hit
            print(f"The {name} hits you for {hit}. HP: {max(player.hp, 0)}")

    if player.is_alive():
        loot = random.randint(*stats["gold"])
        player.gold += loot
        print(f"You win! +{loot} gold.")
        if player.gold >= player.level * 15:
            player.level += 1
            player.hp += 10
            print(f"Level up! You are now level {player.level}.")


# ---------------------------------------------------------------------------
# Part 4: The main loop
# ---------------------------------------------------------------------------
def main():
    player = load_game()
    if player:
        print(f"Welcome back, {player.name}!")
    else:
        player = Player(name=input("Name your hero: ").strip())

    playing = True
    while playing and player.is_alive():
        print(f"\n{player.name} | HP {player.hp} | Gold {player.gold} | Lv {player.level}")
        action = input("[f]ight, [s]ave, [q]uit? ").strip().lower()

        if action == "f":
            fight(player)
        elif action == "s":
            save_game(player)
            print("Game saved.")
        elif action == "q":
            playing = False

    if not player.is_alive():
        print("You have fallen. Game over.")
        SAVE_FILE.unlink(missing_ok=True)  # permadeath: delete the save


if __name__ == "__main__":
    main()
