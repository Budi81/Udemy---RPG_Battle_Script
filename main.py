from classes.game import Person, Bcolors
from classes.magic import Spell
from classes.inventory import Item


# Create Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black") 
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")


# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 1000)
elixier = Item("Elixier", "elixier", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

granade = Item("Granade", "attack", "Deals 500 damage", 500)


player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5}, 
                {"item": superpotion, "quantity": 5}, {"item": elixier, "quantity": 5}, 
                {"item": hielixer, "quantity": 2}, {"item": granade, "quantity": 5}]


# Instantiate People
player1 = Person("Valos:", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Nick :", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("Robot:", 3089, 174, 288, 34, player_spells, player_items)
enemy = Person("Magus", 11200, 221, 525, 25, [], [])

players = [player1, player2, player3]

running = True

print(Bcolors.FAIL + Bcolors.BOLD + "An ENEMY ATTACKS!" + Bcolors.ENDC)

while running:
    print("========================")
    print("\n")
    print("NAME                   HP                                 MP")
    for player in players:
        player.get_stats()


    for player in players:
        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            print("You have attacked for", dmg, "points od damage.")

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose spell: ")) - 1
            
            if magic_choice == -1: continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(Bcolors.FAIL + "\nNot enough MP\n" + Bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(Bcolors.OKBLUE + "\n" + spell.name + "heals for", str(magic_dmg), "HP." + Bcolors.ENDC)
            elif spell.type == "black":
                enemy.take_damage(magic_dmg)
                print(Bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage." + Bcolors.ENDC)

        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1: continue

            item = player.items[item_choice]["item"]
            
            if player.items[item_choice]["quantity"] == 0:
                print(Bcolors.FAIL + "\n" + "None left.." + Bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1 

            if item.type == "potion":
                player.heal(item.prop)
                print(Bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" +Bcolors.ENDC)

            elif item.type == "elixier":
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(Bcolors.OKGREEN + "\n" + item.name + " fully restored HP/MP" + Bcolors.ENDC)
            
            elif item.type == "attack":
                enemy.take_damage(item.prop)
                print(Bcolors.OKGREEN + item.name, "deals", str(item.prop), "points of damage" + Bcolors.ENDC)

    enemy_choice = 1

    enemy_damage = enemy.generate_damage()
    player1.take_damage(enemy_damage)
    print("Enemy attacks for:", enemy_damage, "points od damage.")

    print("=========================")
    print("Enemy HP:", Bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + Bcolors.ENDC +"\n")


    if enemy.get_hp() == 0:
        print(Bcolors.OKGREEN + "You win!" + Bcolors.ENDC)
        running = False

    elif player.get_hp() == 0:
        print(Bcolors.FAIL + "Your enemy has defeated you!" + Bcolors.ENDC)
        running = False