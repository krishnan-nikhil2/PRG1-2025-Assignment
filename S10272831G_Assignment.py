# Krishnan Nikhil CSF03 P08 10272831G

#VARIABLES

import random
day = 1
GP = 0
pick_level = 1
capacity = 10
current_load = 0
steps = 0
turns = 20
pos = [0,0]
portal = 1
lett_to_word = {"C":"copper","S":"silver","G":"gold"}
random_drop = {"copper":(1,5),"silver":(1,3),"gold":(1,2)}
storage = {"copper":0,"silver":0,"gold":0}
random_calculate = {"copper":(1,3),"silver":(5,8),"gold":(10,18)}
in_mine = 0
c = 0
pick_level_capability = {1:"copper",2:"silver",3:"gold"}
whether_can_mine = {1:"C",2:"CS",3:"CSG"}
mined_nodes = []
all_known_coords = []
torch = 0
#FUNCTIONS

def actual_map():   # Load the level1 map from file.
    file = open("level1.txt","r")
    full_map = [] # nested list of the map data from the file which will be modified
    row = [] # used to get list of one line from text file
    for i in file: # i is the lines of the file
        i = i.replace("\n","")
        for j in i: # j is the individual elements of each line of the map the elements are either ores ore empty spaces
            row.append(j)
        full_map.append(row)
        row = []
    
    file.close()

    return full_map
    
def town_menu(day): # display the town menu along with the choice
    displayed_town_menu = """DAY {}
----- Sundrop Town -----
(B)uy stuff
See Player (I)nformation
See Mine (M)ap
(E)nter mine
Sa(V)e game
(Q)uit to main menu
------------------------
""".format(day)
    print(displayed_town_menu)
    choice = input("Your choice? ")

    return choice

def town_menu_buy(GP,capacity,pick_level,torch): # display shop info and does calculation for each purchase
    pick_price = {2:50,3:150}
    can_buy_pick = True # variable to check whether you are able to upgrade pickaxe


    while True: # this loop is to correctly print the right buy menu  when faced with several edge cases
                # like when you have max pick level but you can still ugrade to level 4 but it would be useless as there is only 3 ores.
                # there is also another edge cases of the increases viewport additional feature where you can only buy it once
        if pick_level <= 2:
            if pick_level == 1:
                ore = "silver"
            else:
                ore = "gold"
            if torch: # if increased view port is bought
                buy_menu = """----------------------- Shop Menu -------------------------
(P)ickaxe upgrade to Level {} to mine {} ore for {} GP
(B)ackpack upgrade to carry {} items for {} GP
(L)eave shop
-----------------------------------------------------------
GP: {}
-----------------------------------------------------------
""".format(pick_level+1,ore,pick_price[pick_level+1],capacity+2,capacity*2,GP)
            else:
                buy_menu = """----------------------- Shop Menu -------------------------
(P)ickaxe upgrade to Level {} to mine {} ore for {} GP
(B)ackpack upgrade to carry {} items for {} GP
(V)iewport upgrade to 5X5 for 50 GP
(L)eave shop
-----------------------------------------------------------
GP: {}
-----------------------------------------------------------
""".format(pick_level+1,ore,pick_price[pick_level+1],capacity+2,capacity*2,GP)
    
        else:
            can_buy_pick = False # you have have max level pickaxe already
            if torch: #  if increased view port is bought
                buy_menu = """----------------------- Shop Menu -------------------------
(B)ackpack upgrade to carry {} items for {} GP
(L)eave shop
-----------------------------------------------------------
GP: {}
-----------------------------------------------------------
""".format(capacity+2,capacity*2,GP)
            else:
                buy_menu = """----------------------- Shop Menu -------------------------
(B)ackpack upgrade to carry {} items for {} GP
(V)iewport upgrade to 5X5 for 50 GP
(L)eave shop
-----------------------------------------------------------
GP: {}
-----------------------------------------------------------
""".format(capacity+2,capacity*2,GP)
        
        
        print(buy_menu)
        choice = input("Your choice? ")
        if choice.upper() == "B" and GP >= capacity*2:
            GP -= capacity*2
            capacity += 2
            print("Congratulations! you can now carry {} items".format(capacity))
        elif choice.upper() == "B" and GP < capacity*2:
            print("Not enough GP")
        elif choice.upper() == "P" and can_buy_pick:
            if pick_level == 1 and GP >= 50:
                GP -= 50
                pick_level += 1
                print("Congratulations! You can now mine silver!")
            elif pick_level == 2 and GP >= 150:
                GP -= 150
                pick_level += 1
                print("Congratulations! You can now mine gold!")
            elif pick_level <= 2 and GP < 150:
                print("Not enough GP")
        elif choice.upper() == "V":
            if GP >= 50:
                print("Congratulations! you now have a bigger viewport")
                GP -= 50
                torch = 1
            else:
                print("Not enough GP")
        elif choice.upper() == "L":
            return GP, capacity,pick_level,torch
        
        else:
            print("Please enter a valid choice") 

def town_menu_player_info(name,position,current_load,GP,steps,portal,in_mine,storage,): # display player info for both in twon and mine menu
    if portal == 1: # if you are at town that is what the varibale means if it is 1
        word = "Portal Position"
    else:
        word = "Current position"
    if in_mine == 0:
        info = """\n----- Player Information -----
Name: {}
{}: ({}, {})
Pickaxe level: {} ({})
------------------------------
Load: {} / {}
------------------------------
GP: {}
Steps taken: {}
------------------------------
""".format(name,word,position[0],position[1],pick_level,pick_level_capability[pick_level],current_load,capacity,GP,steps)
    else:
        info = """\n----- Player Information -----
Name: {}
{}: ({}, {})
Pickaxe level: {} ({})
Gold: {}
Silver: {}
Copper: {}
------------------------------
Load: {} / {}
------------------------------
GP: {}
Steps taken: {}
------------------------------
""".format(name,word,position[0],position[1],pick_level,pick_level_capability[pick_level],storage["gold"],storage["silver"],storage["copper"],current_load,capacity,GP,steps)
    
    return info
    
def mine_map_info(map,day): # the data of the map shown to the user with fog that will gradually disappear
    fog = [] # this is the map data that is going to be showed to player when he calls the map option
    length = len(map[0])
    width = len(map)

    for i in range(width): # initialises the full fog of the map at the start of the game
        row = ["?"]*length
        fog.append(row)

    return fog

def draw_mine_map_info(fog,map): # displays the fog map in appropriate format
    length = len(map[0])
    print("\n+"+("-"*length)+"+")
    for k in fog: # k is the list of the nested list of fog
        k = "".join(k)
        print("|"+k+"|")
    print("+"+("-"*length)+"+")

def mine_menu_info(pos,map,mined_nodes,torch,mutate = True): # computes the viewport
    # ok so for the additional of feature of the 5 by 5 viewport the idea is that when player is at the edge of map
    # the view port displays the player right beside the barrier instead of the middle where it is one unit away from barrier

    check = [pos[0],pos[1]] # check is the testing coords that allows to check various testcases before drawing of the mine menu
    if not(torch): # if 5by5 viewport is not bought
        check[0] -= 1
        check[1] -= 1
    else:
        check[0] -= 2
        check[1] -= 2
    threebythree = [] # threebyethree is a nested list of the coords to display for the viewport. pls ignore the name it is meant for both sizes of the viewport
    number_col = 0
    num_rows = 0
    x,y = 0,0 # the final coords to be used when calculating the coords to be displayed
    unfogcoords = [] # these are the coords that is found by moving and hence you know the surround coords around player which will be used when unfogging the map
    middle = "" # this is the element of what the player has stepped into. elemnt is whether it is empty space or ore. pls ignore the name of it being called middle

    if not(torch): # this nested if else statement is to figure out the number of rows to display when the player is close to the edge of the map
        if check[1] < 0 or check[1]+2 > len(map)-1: # whether at top or bottom of map
            threebythree.append(["#","#","#"])
            num_rows = 2
            if check[1] < 0:
                y = check[1] +1
            else:
                y = check[1]
        else:
            num_rows = 3
            y = check[1]
    
    else: # this is basicaly the same code as above but changed for the 5by5 view port
        if check[1] < 0 or check[1]+3 >= len(map)-1:
            threebythree.append(["#","#","#","#","#"])
            num_rows = 4
            if check[1] < 0:
                if pos[1] == 0:
                    y = check[1] +2
                elif pos[1] == 1:
                    y = check[1] + 1
            else:
                # this part of code is not in the above code as this tests for special test cases at the edges of map
                # the edge cases are the stuff i said at the top of the function comment of how 5 by 5 viewport works
                if pos[1] == len(map)-1:
                    y = check[1] -1
                else:
                    y = check[1]
        else:
            num_rows = 5
            y = check[1]

    
    for i in range(num_rows):
        if not(torch): # this long nested if else statment is the same as above but now for checking horizontally
            if check[0] < 0 or check[0]+2 > len(map[0])-1:
                row = ["#"]
                number_col = 2
                if check[0] < 0:
                    x = check[0] + 1
                else:
                    x = check[0]
                
            else:
                row = []
                number_col = 3
                x = check[0]

        else: # if torch is bought
            if check[0] < 0 or check[0]+3 >= len(map[0])-1:
                row = ["#"]
                number_col = 4
                
                if check[0] < 0:
                    if pos[0] == 0:
                        x = check[0] + 2
                    elif pos[0] == 1:
                        x = check[0] + 1
                    
                else:
                    if pos[0] == len(map[0])-1:
                        x = check[0] - 1
                    else:
                        x = check[0]
                    
                
            else:
                row = []
                number_col = 5
                x = check[0]



        for j in range(number_col):
            
            row.append(map[y+i][x+j]) # this gets the acutal map info that is not shown player but only the surrounding info which is the viewport size
            unfogcoords.append([x+j,y+i])

        if not(torch): # this is to correctly display the barrier if the player is all the way right instead of the barrier on the left
            if check[0]+2 > len(map[0])-1:
                row.pop(0)
                row.append("#")
        else:
            if check[0]+3 >= len(map[0])-1:
                row.pop(0)
                row.append("#")

        threebythree.append(row)
    if not(torch): # this is the same as above but for vertical display
        if check[1]+2 > len(map)-1:
            first = threebythree.pop(0)
            threebythree.append(first)
    else:
        if check[1]+3 >= len(map)-1:
            first = threebythree.pop(0)
            threebythree.append(first)
        
    if not(torch): # this long if else is to correctly display where the M location should be in the mine menu
        threebythree[1].insert(1,"M")
        middle = threebythree[1].pop(2)
    else:
        if pos[0] == 0 and pos[1] == 0:
            threebythree[1].insert(1,"M")
            middle = threebythree[1].pop(2)
        elif pos[0] == len(map[0])-1 and pos[1] == 0:
            threebythree[1].insert(3,"M")
            middle = threebythree[1].pop(4)
        elif pos[0] == 0 and pos[1] == len(map)-1:
            threebythree[3].insert(1,"M")
            middle = threebythree[3].pop(2)
        elif pos[0] == len(map[0])-1 and pos[1] == len(map)-1:
            threebythree[3].insert(3,"M")
            middle = threebythree[3].pop(4)
        elif pos[1] == 0 and pos[0] != 0: 
            threebythree[1].insert(2,"M")
            middle = threebythree[1].pop(3)
        elif pos[1] == len(map)-1 and pos[0] != 0:
            threebythree[3].insert(2,"M")
            middle = threebythree[3].pop(3)
        elif pos[0] == 0 and pos[1] != len(map)-1:
            threebythree[2].insert(1,"M")
            middle = threebythree[2].pop(2)
        elif pos[0] == len(map[0])-1 and pos[1] != len(map)-1:
            threebythree[2].insert(3,"M")
            middle = threebythree[2].pop(4)
        else:
            threebythree[2].insert(2,"M")
            middle = threebythree[2].pop(3)


    if middle in "CSG" and mutate: # mutate is a vriable to correctly mine the ore and it is important for the ore replenishing  feature
        mined_nodes.append([pos[0],pos[1],middle])
        map[pos[1]].insert(pos[0]," ")
        map[pos[1]].pop(pos[0]+1)

    return threebythree,middle,unfogcoords,mined_nodes
    
def draw_mine_menu(day,turns,capacity,steps,threebythree,current_load,torch): # display mine menu to user
    print("DAY {}".format(day))
    if not(torch):
        print("+---+")
    else:
        print("+-----+")
    for line in threebythree:
        line = "".join(line)
        print("|"+line+"|")
    if not(torch):
        print("+---+")
    else:
        print("+-----+")

    print("Turns left: {:<6} Load: {} / {:<6} Steps: {}".format(turns,current_load,capacity,steps))
    print("(WASD) to move")
    print("(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu")

    action = input("Action? ")

    return action

def move_mine(pos,choice,map,capacity,current_load,whether_can_mine,pick_level): # handles movement of player
    town = True # a variable to check if a player has moved into 0,0 which is the town and then go back into town menu
    if choice == "W" and pos[1] > 0:
        if map[pos[1]-1][pos[0]] in "CSG" and current_load >= capacity:
            print("You can't carry any more, so you can't go that way.")
        elif map[pos[1]-1][pos[0]] in "CSG" and map[pos[1]-1][pos[0]] not in whether_can_mine[pick_level]:
            print("Your pickaxe is not good enough to mine {}".format(lett_to_word[map[pos[1]-1][pos[0]]]))
        else:
            if [pos[1]-1,pos[0]] == [0,0]:
                town = False
            pos[1] -= 1
        
    elif choice == "S" and pos[1] < len(map)-1:
        if map[pos[1]+1][pos[0]] in "CSG" and current_load >= capacity:
            print("You can't carry any more, so you can't go that way.")
        elif map[pos[1]+1][pos[0]] in "CSG" and map[pos[1]+1][pos[0]] not in whether_can_mine[pick_level]:
            print("Your pickaxe is not good enough to mine {}".format(lett_to_word[map[pos[1]+1][pos[0]]]))
        else:
            if [pos[1]+1,pos[0]] == [0,0]:
                town = False
            pos[1] += 1
    elif choice == "A" and pos[0] > 0:
        if map[pos[1]][pos[0]-1] in "CSG" and current_load >= capacity:
            print("You can't carry any more, so you can't go that way.")
        elif map[pos[1]][pos[0]-1] in "CSG" and map[pos[1]][pos[0]-1] not in whether_can_mine[pick_level]:
            print("Your pickaxe is not good enough to mine {}".format(lett_to_word[map[pos[1]][pos[0]-1]]))
        else:
            if [pos[1],pos[0]-1] == [0,0]:
                town = False
            pos[0] -= 1
    elif choice == "D" and pos[0] < len(map[0])-1:
        if map[pos[1]][pos[0]+1] in "CSG" and current_load >= capacity:
            print("You can't carry any more, so you can't go that way.")
        elif map[pos[1]][pos[0]+1] in "CSG" and map[pos[1]][pos[0]+1] not in whether_can_mine[pick_level]:
            print("Your pickaxe is not good enough to mine {}".format(lett_to_word[map[pos[1]][pos[0]+1]]))
        else:
            if [pos[1],pos[0]+1] == [0,0]:
                town = False
            pos[0] += 1

    return pos,town

def ore_storage(middle,lett_to_word,storage,random_drop): # ore storage
    amount = 0
    amount = random.randint((random_drop[lett_to_word[middle]])[0],(random_drop[lett_to_word[middle]])[1])
    storage[lett_to_word[middle]] += amount

    return storage,amount,lett_to_word[middle]

def calculate_gp(ore,random_calculate): # calculates gp for each ore obtained
    total = 0
    total = storage[ore]*random.randint(random_calculate[ore][0],random_calculate[ore][1])

    return total
     
def unfog(coords,map,fog,pos,all_known_coords): # changes the fog map using the known coords
    for i in all_known_coords:
        fog[i[1]].insert(i[0],map[i[1]][i[0]])
        fog[i[1]].pop(i[0]+1)
    fog[pos[1]][pos[0]] = "M" # replaces current postion with M to show where the player is on map
    
def portal_stone(GP,storage,c,turns): # handling of using the portal stone feature
    if turns == 1:
        print("You are exhausted.")
    if storage["copper"] > 0 or storage["silver"] > 0 or storage["gold"] > 0:
        print("You place your portal stone here and zap back to town.")
    else:
        print("You place your portal stone here and zap back to town.\n")
    for i in storage:
        if storage[i] > 0:
            c += 1
            total = calculate_gp(i,random_calculate)
            print("You sell {} {} ore for {} GP.".format(storage[i],i,total))
            GP += total
    if c > 0:
        print("You now have {} GP!\n".format(GP))

    return GP

def save_game(pos,GP,day,steps,turns,pick_level,capacity,map,fog,name,torch): # save game
    file = open("saved_game.txt","w")
    file.close()
    file = open("saved_game.txt","a")
    file.write("{};{};{};{};{};{};{};{};{}".format(pos,GP,day,steps,turns,pick_level,capacity,name,torch))
    for i in map: # i is each line of actual map not shown to player
        file.write("\n;{}".format("".join(i)))
    for j in fog: # j is each line of map shown to player
        file.write("\n;{}".format("".join(j)))
    file.close()
    print("Game saved.\n")

def load_game(pos,GP,day,steps,turns,pick_level,capacity,map,fog,name,torch): # load game
    
    file = open("saved_game.txt","r")
    data = file.read()
    data = data.replace("\n","")
    data = data.split(";")
    first = data[0]
    first = first[1:len(first)-1]
    first = first.split(",")
    first[0] = int(first[0])
    first[1] = int(first[1])
    pos = first
    GP = int(data[1])
    day = int(data[2])
    steps = int(data[3])
    turns = int(data[4])
    pick_level = int(data[5])
    capacity = int(data[6])
    name = data[7]
    torch = int(data[8])
    map = []
    current = 9
    for i in range(10): # i is the line of the actaul map that is converted to suitable format 
        row = data[current+i]
        row = list(row)
        map.append(row)
    current += 10
    fog  = []
    for j in range(10): # j is the line of the fog map that is converted to suitable format 
        row = data[current+j]
        row = list(row)
        fog.append(row)
        

    file.close()
    print("Game loaded.\n")

    return pos,GP,day,steps,turns,pick_level,capacity,map,fog,name,torch
    
def top_scores(): # display the top scores
    try:
        file = open("scores.txt","r")
        score = []
        for i in file:
            i = i.replace("\n","")
            i = i.split(",")
            score.append([int(i[1]),int(i[2]),(int(i[3]))*-1,i[0]])

        if not(score):
            print("no scores recorded yet!")
        
        score.sort()
        


        print("\n--- Top 5 Sundrop Mountain Scores ---")
        print("{:<5}{:<15}{:<6}{:<8}{}".format("Rank","Name","Days","Steps","GP"))
        for rank in range(1,len(score)+1):
            if rank == 6:
                break
            print("{:<5}{:<15}{:<6}{:<8}{}".format(rank,score[rank-1][3],score[rank-1][0],score[rank-1][1],abs(score[rank-1][2])))
        print("--------------------------------------\n")
            
        file.close()
    except FileNotFoundError:
        print("no scores has been recorded\n")

def winning_data(name,day,steps,GP): # extract the relvant data after winning
    file = open("scores.txt","a")
    file.write("{},{},{},{}\n".format(name,day,steps,GP))
    file.close()

def find_saved_game(): # checks whether there is a saved game file
    try:
        file = open("saved_game.txt","r")
        file.close()
        return True
    
    except FileNotFoundError:
        print("No saved game found\n")
        return False

def replenish_nodes(mined_nodes,map,lett_to_word,pos): # additonal feature of replenishing ore
    if len(mined_nodes) > 0:
        random_node = random.randint(0,len(mined_nodes)-1)
        chance = random.randint(1,5)
        if chance == 1:
            print("{} node replenished at ({},{})".format(lett_to_word[mined_nodes[random_node][2]],mined_nodes[random_node][0],mined_nodes[random_node][1]))
            if pos == [mined_nodes[random_node][0],mined_nodes[random_node][1]]:
                print("Your portal location is currently on it")
            map[mined_nodes[random_node][1]][mined_nodes[random_node][0]] = mined_nodes[random_node][2]
            mined_nodes.pop(random_node)



print("""---------------- Welcome to Sundrop Caves! ----------------
You spent all your money to get the deed to a mine, a small
backpack, a simple pickaxe and a magical portal stone.
      
How quickly can you get the 500 GP you need to retire
and live happily ever after?
-----------------------------------------------------------
      """)


main_menu = """--- Main Menu ----
(N)ew game
(L)oad saved game
(Q)uit
(V)iew top scores
------------------
"""

# MAIN GAME CODE


while True: # main menu loop
    if GP >= 500:
        print("""-------------------------------------------------------------
Woo-hoo! Well done, {}, you have {} GP!
You now have enough to retire and play video games every day.
And it only took you {} days and {} steps! You win!
-------------------------------------------------------------\n""".format(name,GP,day,steps))
        final_score = winning_data(name,day,steps,GP)
        GP = 0
        
    print(main_menu)
    main_menu_choice = input("Your choice? ")
    map = actual_map()
    fog = mine_map_info(map,day)
    name = "" # initialised so that when loading it does not have error
    if main_menu_choice.upper() == "Q":
        break
    elif main_menu_choice.upper() == "L":
        if find_saved_game() == True: # checks if there is a saved game file
            pos,GP,day,steps,turns,pick_level,capacity,map,fog,name,torch = load_game(pos,GP,day,steps,turns,pick_level,capacity,map,fog,name,torch)
        else:
            continue 
    elif main_menu_choice.upper() == "V":
        TOP_scores = top_scores()
        continue

    elif main_menu_choice.upper() == "N":
        day = 1
        GP = 100
        pick_level = 3
        capacity = 100
        current_load = 0
        steps = 0
        turns = 20
        pos = [0,0]
        portal = 1 # portal variable is to determine whether the player is outside or inside mine to correctly display the sutiable of whether player psotion or portal position 
        lett_to_word = {"C":"copper","S":"silver","G":"gold"}
        random_drop = {"copper":(1,5),"silver":(1,3),"gold":(1,2)}
        storage = {"copper":0,"silver":0,"gold":0}
        random_calculate = {"copper":(1,3),"silver":(5,8),"gold":(10,18)}
        in_mine = 0 # this is used to check if the player is in the mine to dispaly the second info menu which includes how much ore the player ahs mined
        c = 0 # a variable to count and check if the player has even mined any ores when using portal stone
        pick_level_capability = {1:"copper",2:"silver",3:"gold"}
        whether_can_mine = {1:"C",2:"CS",3:"CSG"}
        mined_nodes = [] # it is all the coords of the ores that have been mined
        all_known_coords = [] # it is all the known coords by moving and beiing revealed by mine menu which will be used to update fog map
        torch = 0 # variable to see if upgraded viewport is bought
        while True: # loop to prevent semicolon from being in name as that is a delimeter i am using for game sav and load function
            name = input("Greetings, miner! What is your name? ")
            if ";" in name: 
                print("name should not contain ';' please try again")
            else:
                break
        print("Pleased to meet you, {}. Welcome to Sundrop Town!\n".format(name))
        
    else:
        print("Please enter a valid choice")
        continue
        
    


    while GP < 500: # town menu loop 
        choice = town_menu(day).upper()
        mine_menu = mine_menu_info(pos,map,mined_nodes,torch,mutate=False)
        # mine menu is called here  to get the current coords and it helps solve problem of not showing the correct map
        # as for example if you immediately call the map on day 1 without entering the mine, if mine menu is not called, the fog map will show everything as fog instead of the intial 3 spaces that is known 
        threebythree = mine_menu[0]
        middle = mine_menu[1]
        coords = mine_menu[2]
        for i in coords:
            if i not in all_known_coords:
                all_known_coords.append(i)
        if choice == "B":
            output = town_menu_buy(GP,capacity,pick_level,torch)
            GP,capacity,pick_level,torch = output[0],output[1],output[2],output[3] # assign back to output so that the changes are saved
        elif choice == "Q":
            break 
        elif choice == "I":
            portal = 1 
            print(town_menu_player_info(name,pos,current_load,GP,steps,portal,in_mine,storage))
        elif choice == "M":
            unfog(coords,map,fog,pos,all_known_coords)
            if pos != [0,0]: # to display where portal location is
                fog[0][0] = "M"
                fog[pos[1]][pos[0]] = "P"
            mine_map = draw_mine_map_info(fog,map)
            print()
        elif choice == "E":
            print("""\n---------------------------------------------------
{:>28}
---------------------------------------------------

""".format("DAY"+" "+str(day)),end="")
            in_mine = 1
            turns = 20
            c = 0
            while True: # mine menu loop 
                # mutate is false as the player has not moved and if there is a ore restored on the player locatioon
                # it does not automatically mine it and result in not getting the ore(you can only get ore when pressing wasd)
                mine_menu = mine_menu_info(pos,map,mined_nodes,torch,mutate=False) 

                threebythree = mine_menu[0] # data to display for view port
                middle = mine_menu[1] # middle of viewport/players current position
                coords = mine_menu[2] # coords for the viewport
                for i in coords: # i is the known coord
                    if i not in all_known_coords:
                        all_known_coords.append(i)
                mine_menu_choice = draw_mine_menu(day,turns,capacity,steps,threebythree,current_load,torch)
                if mine_menu_choice.upper() in ["W","A","S","D"]: 
                    print("\n---------------------------------------------------")
                    movement = move_mine(pos,mine_menu_choice.upper(),map,capacity,current_load,whether_can_mine,pick_level)
                    mine_menu = mine_menu_info(pos,map,mined_nodes,torch,mutate=True)
                    middle = mine_menu[1]
                    if middle in "CSG": 
                        
                        amount = ore_storage(middle,lett_to_word,storage,random_drop)[1]
                        print("You mined {} piece(s) of {}".format(amount,lett_to_word[middle]))
                        if current_load + amount > capacity:
                            print("...but you can only carry {} more piece(s)!".format(capacity-current_load))
                            remaining = capacity-current_load
                            current_load += remaining
                            storage[lett_to_word[middle]] -= amount
                            storage[lett_to_word[middle]] += remaining
                            
                        else:
                            current_load += amount
                        
                        

                    unfog(coords,map,fog,pos,all_known_coords)
                    steps += 1
                    if turns == 1 or not(movement[1]): # to use portal when runnig out of turns
                        new_nodes = replenish_nodes(mined_nodes,map,lett_to_word,pos)
                        portal_info = portal_stone(GP,storage,c,turns)
                        storage = {"copper":0,"silver":0,"gold":0}
                        day += 1
                        current_load = 0
                        GP = portal_info
                        break
                        
                    turns -= 1
                    
                    
                    
                
                elif mine_menu_choice.upper() == "Q":
                    choice = "Q"
                    break
                elif mine_menu_choice.upper() == "M":
                    unfog(coords,map,fog,pos,all_known_coords) 
                    fog[0][0] = "T"
                    mine_map = draw_mine_map_info(fog,map)
                elif mine_menu_choice.upper() == "I":
                    portal = 0
                    print(town_menu_player_info(name,pos,current_load,GP,steps,portal,in_mine,storage),end = "")
                elif mine_menu_choice.upper() == "P":
                    new_nodes = replenish_nodes(mined_nodes,map,lett_to_word,pos)
                    print("---------------------------------------------------")
                    portal_info = portal_stone(GP,storage,c,turns)
                    storage = {"copper":0,"silver":0,"gold":0}
                    day += 1
                    current_load = 0
                    GP = portal_info
                    break
                else:
                    print("Please enter a valid action")

                
        
        elif choice == "V":
            game_save = save_game(pos,GP,day,steps,turns,pick_level,capacity,map,fog,name,torch)

        if choice == "Q":
            break
        in_mine = 0


        if choice not  in ["V","Q","B","E","M","I"]:
            print("Please enter a valid choice")


