from classes.game import Person, Bcolors
from classes.magic import Spell
from classes.inventory import Item


# Create Black Magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black") 
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")


# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixier = Item("Elixier", "elixier", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

granade = Item("Granade", "attack", "Deals 500 damage", 500)


player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5}, 
                {"item": superpotion, "quantity": 5}, {"item": elixier, "quantity": 5}, 
                {"item": hielixer, "quantity": 2}, {"item": granade, "quantity": 5}]


# Instantiate People
player = Person(460, 65, 60, 34, player_spells, player_items)
enemy = Person(1200, 65, 45, 25, [], [])

running = True

print(Bcolors.FAIL + Bcolors.BOLD + "An ENEMY ATTACKS!" + Bcolors.ENDC)

while running:
    print("========================")
    player.choose_action()
    choice = input("Choose action: ")
    index = int(choice) - 1

    if index == 0:
        dmg = player.generate_damage()
        enemy.take_damage(dmg)
        print("You have attacked for", dmg, "points od damage.") 
    
    elif index == 1:    
        player.choose_magic()
        magic_choice = int(input("Choose spell: ")) - 1
        
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
        item_choice = int(input("Choose item: ")) - 1

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
            print(Bcolors.FAIL + item.name, "deals", str(item.prop), "points of damage" + Bcolors.ENDC)

    enemy_choice = 1

    enemy_damage = enemy.generate_damage()
    player.take_damage(enemy_damage)
    print("Enemy attacks for:", enemy_damage, "points od damage.")

    print("=========================")
    print("Enemy HP:", Bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + Bcolors.ENDC +"\n")

    print("Your HP:" + Bcolors.OKGREEN + str(player.get_hp()) + "/" + str(player.get_max_hp()) + Bcolors.ENDC)
    print("Your MP:" + Bcolors.OKBLUE + str(player.get_mp()) + "/" + str(player.get_max_mp()) + Bcolors.ENDC + "\n")

    if enemy.get_hp() == 0:
        print(Bcolors.OKGREEN + "You win!" + Bcolors.ENDC)
        running = False

    elif player.get_hp() == 0:
        print(Bcolors.FAIL + "Your enemy has defeated you!" + Bcolors.ENDC)
        running = False