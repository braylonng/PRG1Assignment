from random import randint

player = {}
game_map = []
fog = []

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    map_file = open(filename, 'r')
    global MAP_WIDTH
    global MAP_HEIGHT
    
    map_struct.clear()
    
    with open('level1.txt','r') as map:
        for line in map:
            map_struct.append(list(line.strip()))
    MAP_HEIGHT = len(map_struct)
    MAP_WIDTH = len(map_struct[0]) if MAP_HEIGHT >0 else 0
    
    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)

    map_file.close()

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    radius = 1 if not player.get('torch') else 2
    for dy in range(-radius, radius+1):
        for dx in range(-radius, radius+1):
            x = player['x'] + dx
            y = player['y'] + dy
            if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                fog[y][x] = False
    return

def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)
    fog.clear()
    for _ in range(MAP_HEIGHT):
    # TODO: initialize fog
        fog.append([True] * MAP_WIDTH)
    # TODO: initialize player
    player.clear()
    #   You will probably add other entries into the player dictionary
    player['torch'] = False
    player['portal'] = (0,0)
    player['pickaxe']=1
    player['load']= 0
    player['max_load']=10
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY


    clear_fog(fog, player)
    
# This function draws the entire map, covered by the fof
def draw_map(game_map, fog, player):
    print("+" + ("-" * MAP_WIDTH) + "+")
    for y in range(MAP_HEIGHT):
        row = "|"
        for x in range(MAP_WIDTH):
            if x == player['x'] and y == player['y']:
                row += 'M'
            elif (x, y) == player['portal']:
                row += 'P'
            elif fog[y][x]:
                row += '?'
            else:
                row += game_map[y][x]
        row += "|"
        print(row)
    print("+" + ("-" * MAP_WIDTH) + "+")
    

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    radius = 1 if not player.get('torch') else 2
    for dy in range(-radius, radius + 1):
        row = "|"
        for dx in range(-radius, radius + 1):
            x = player['x'] + dx
            y = player['y'] + dy
            if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                if x == player['x'] and y == player['y']:
                    row += 'M'
                elif fog[y][x]:
                    row += '?'
                else:
                    row += game_map[y][x]
            else:
                row += '#'
        row += "|"
        print(row)
    return

# This function shows the information for the player
def show_information(player):
    print('\n----- Player Information -----')
    print(f'Name: {player.get('name','Unknown')}')
    print(f"Current position: ({player['x']}, {player['y']})")
    print(f'Pickaxe level: {player['pickaxe']}')
    for ore in minerals:
        print(f'{ore.capitalize()}: {player[ore]}')
        print("------------------------------")
    print(f"Load: {player['load']} / {player['max_load']}")
    print(f"GP: {player['GP']}")
    print(f"Steps taken: {player['steps']}")
    #print(f"Warehouse: {player['warehouse']}")
    print("------------------------------\n")
    return

# This function saves the game
def save_game(game_map, fog, player):
    with open('savegame.txt','w') as save:
    # save map
        save.write(str(game_map))+ '\n'
    # save fog
        save.write(str(fog)+'\n')
    # save player
        save.write(str(player) + "\n")
    return
        
# This function loads the game
def load_game(game_map, fog, player):
    # load map
    with open('save_game.txt','r') as savefile:
        game_map_data= eval(savefile.readline())
        fog_data = eval(savefile.readline())
        player_data=eval(savefile.readline())
    game_map.clear()
    game_map.extend(game_map_data)
    # load fog
    fog.clear()
    fog.extend(game_map_data)
    # load player
    player.clear()
    player.update(player_data)
    return

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
#    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")
def show_town_menu():
    print()
    
    print(f'DAY {int(player['day'])+1}')
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")
def sell_ore():
    total =0 
    for ore in minerals:
        if player[ore]>0:
            price = randint(*prices[ore])
            gp = player[ore]*price
            print(f'You sold {player[ore]} {ore} for {gp} GP.')
            player ['GP'] += gp 
            player[ore] =0
            player['load']=0
            total +=gp
    if player['GP']>= WIN_GP:
        print(f'\nWoo-hoo! Well done, {player['name']}, you have {player['GP']} GP!\nYou now have enough to retire and play video games every day.\nAnd it only took you {player['day']} days and {player['steps']} steps! You win!')
def replenish_nodes():
    ores=['C','S','G']
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if game_map[y][x] == ' ' and randint(1,100)<=20:
                game_map[y][x] = ores[randint(0,2)]
            

#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

# TODO: The game!
while True:
    if game_state=='main':
        show_main_menu()
        option=input('Your Choice? ').strip()
        if option.upper()=='Q':
            print('Thanks for playing!')
            break
        elif option.upper()=='N':
            name=input('Greetings, miner! What is your name? ')
            player['name'] = name
            print('Pleased to meet you, {}. Welcome to Sundrop Town!'.format(name))
            initialize_game(game_map, fog, player)
            game_state='town'
            
        elif option.upper()=='L':
            load_game(game_map, fog, player)
            print("Game loaded.")
            game_state = 'town'
        else:
            print('Invalid Option. Please try again.')
            continue

    elif game_state=='town':
        show_town_menu()
        choice=input('Your choice? ').strip()
        if choice.upper()=='Q':
             game_state='main'
        elif choice.upper()=='B':  
            while True:
                print('----------------------- Shop Menu -------------------------')
                if player['pickaxe'] == 1:
                    print('(P)ickaxe upgrade to Level 2 to mine silver ore for 50 GP')
                elif player['pickaxe']==2:
                    print('(P)ickaxe upgrade to Level 3 to mine silver ore for 150 GP')
                if not player['torch']:
                    print("(T)orch (Magic) upgrade for 50 GP")
                print('(B)ackpack upgrade to carry 12 items for 20 GP')
                print('(L)eave shop')
                print('-----------------------------------------------------------')
                print(f'GP: {player['GP']}')
                print('-----------------------------------------------------------')
                shop_choice=input('Your choice? ').strip()
                if  shop_choice.upper()=='P':
                    if player['pickaxe']==1:
                        if player['GP']>=50:
                            player['GP']-=50
                            player['pickaxe']=2
                            print('Congratulations! You can now mine silver!')
                        else:
                            print("Not enough GP.")
                    elif player['pickaxe']==2:
                        if player['GP']>=150:
                            player['GP'] -= 150
                            player['pickaxe'] = 3
                        print("Congratulations! You can now mine gold!")
                    elif player['pickaxe']==3:
                        print('Your Pickaxe is already maxed out!')
                elif shop_choice.upper() == 'B':
                    price= player['max_load']*2
                    if player['GP']>=price:
                        player['GP']-=price
                        player['max_load'] +=2
                        print(f'Congratulations! You can now carry {player['max_load']} items!')
                elif shop_choice.upper() == 'T' and not player['torch']:
                    if player['GP'] >= 50:
                        player['GP'] -= 50
                        player['torch'] = True
                        print("Magic torch activated! You can now see a 5x5 area.")
                    else:
                        print("Not enough GP.")
                elif shop_choice.upper()=='L':
                    break
                else:
                    print('Invalid option. Please try again')
        elif choice.upper() =='I':
            show_information(player)
        elif choice.upper()== 'M':
            draw_map(game_map, fog, player)
        elif choice.upper() == 'E':
            game_state = 'mine'
        elif choice.upper()=='V':
            save_game(game_map,fog, player)
            print('Game saved')
        else:
            print('Invalid option. Please try again.')
    elif game_state=='mine':
        clear_fog(fog,player)
        draw_view(game_map, fog, player)
        print(f'Turns left: {player['turns']}    Load: {player['load']}    Steps: {player['steps']}') 
        move = input("(WASD) to move | (M)ap | (I)nfo | (P)ortal | (Q)uit: ").strip().lower()
        if move in ['w','a','s','d']:
            dx, dy = 0,0
            if move == 'w': dy=-1
            elif move == 's': dy = 1
            elif move == 'a': dx =-1
            elif move == 'd': dx=1
            new_x = player['x']+ dx
            new_y = player['y']+ dy

            if not (0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT):
                print("Invalid move. You cant't move ourside the cave.")
            else:
                pickaxe_levels = {'C': 1, 'S': 2, 'G': 3}
                tile = game_map[new_y][new_x]
                can_mine = tile in mineral_names and player ['load'] < player['max_load']
                if tile in mineral_names[tile]:
                    mineral = mineral_names[tile]
                    if player['pickaxe'] < pickaxe_levels[minerals]:
                        print(f"Your pickaxe isn't strong enough to mine {mineral}")
                        continue
                    if not can_mine:
                        print("You're carrying too much!")
                        continue
                    if mineral == 'copper':
                        amount = randint(1,5)
                    elif mineral == 'silver':
                        amount = randint(1,3)
                    elif mineral == 'gold':
                        amount = randint(1,2)
                    space = player['max_load'] - player['load']
                    picked = min(space,amount)
                    player[mineral]+= picked
                    print(f'You mined {picked} piece(s) of {mineral}.')
                player['x']=new_x
                player['y']=new_y
                player['turns'] -= 1
                player['steps'] +=1
                clear_fog(fog, player)

                if player['turns']==0:
                    print('You are exhausted.\nYou place your portal stone here and zap back to town.')
                    game_state = 'town'
                    player['portal'] = (player['x'], player['y'])
                    player['x'], player ['y']=0,0
                    sell_ore()
                    player['day'] +=1
                    player['turns'] = TURNS_PER_DAY
                    replenish_nodes()
        elif move == 'p':
            draw_map(game_map,fog,player)
        elif move == 'i':
            show_information(player)
        elif move =='p':
            print('You place your portal stone here and zap back to town.')
            player['portal'] = (player['x'], player['y'])
            player['x'] = 0
            player['y']=0
            game_state='town'
            sell_ore()
            player['day'] +=1
            player['turns']=TURNS_PER_DAY
            replenish_nodes()

        elif move == 'q':
            game_state= 'main'
        else:
            print('Invalid option. Please try again')         



                        