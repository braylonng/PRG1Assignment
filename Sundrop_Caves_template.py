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
    
    # TODO: Add your map loading code here
    
    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)

    map_file.close()

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    return

def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)

    # TODO: initialize fog
    
    # TODO: initialize player
    #   You will probably add other entries into the player dictionary
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
    return

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
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
    print(f"Warehouse: {player['warehouse']}")
    print("------------------------------\n")
    return

# This function saves the game
def save_game(game_map, fog, player):
    # save map
    # save fog
    # save player
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
    # TODO: Show Day
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")
            

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
day=0
while True:
    if game_state=='main':
        show_main_menu()
        option=input('Your Choice? ').strip()
        if option.upper()=='Q':
            print('Thanks for playing!')
            break
        elif option.upper()=='N':
            name=input('Greetings, miner! What is your name? ')
            print('Pleased to meet you, {}. Welcome to Sundrop Town!'.format(name))
            game_state='town'
            
        elif option.upper()=='L':
            load_game(game_map, fog, player)
            print("Game loaded.")
            game_state = 'town'
        else:
            print('Invalid Option. Please try again.')
            continue

    elif game_state=='town':
        day+=1
        print(f'DAY {day}')
        show_town_menu()
        choice=input('Your choice? ').strip()
        if choice.upper()=='Q':
             break
        elif choice.upper()=='B':  
            while True:
                print('----------------------- Shop Menu -------------------------')
                if player['pickaxe']== 1:
                    print('(P)ickaxe upgrade to Level 2 to mine silver ore for 50 GP')
                elif player['pickaxe']==2:
                    print('(P)ickaxe upgrade to Level 3 to mine silver ore for 150 GP')
                #make torch option here
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
                elif shop_choice.upper()=='L':
                    break
                else:
                    print('Invalid option. Please try again')
        elif choice.upper() =='I':
            show_information(player)


                            
