#In this homework, we must very careful about the reference property of the python language. 
# when I am going to update the value of inner list of the list, I first assign a shallow copy of the innerlist 
# to the original one and based on that shallow copied one, I change the corresponding value. If not doing this, 
# more than one values in those unexpected position are changed 同时。
import sys, random, copy
LIVING_COST = -1
ROW_NUM = 3
COL_NUM = 4
ALPHA = 0.1
GAMMA = 0.5
RESULT = ["\u2191","\u2192","\u2190","\u2193"]

dx = [-1,0,0,1]
dy = [0,1,-1,0]


class WallError(Exception): pass
class OptionError(Exception): pass
class LocError(Exception): pass

def translate_to_index(loc):
    try: 
        if loc > ROW_NUM * COL_NUM or loc < 0:
            raise LocError
        x = (ROW_NUM - 1) - ((loc - 1) // COL_NUM)
        y = (loc - 1) % COL_NUM
        return x, y
    except LocError:
        print("The Location should be within 12.")
    
    
def assign_special(table, loc, name):
    x, y = translate_to_index(loc)
    if name == "donut":
        table[x][y] = [0]
    elif name == "forbidden":
        table[x][y] =[0]
    elif name == "wall":
        table[x][y] =[0]
    return copy.deepcopy(table)

def init_table(donut, forbidden, wall):
    Q_value = [0]*4
    table = [[Q_value for i in range(COL_NUM)] for j in range(ROW_NUM)]
    table = assign_special(table, donut, "donut")
    table = assign_special(table, forbidden,"forbidden")
    table = assign_special(table, wall,"wall")
    return table

def change_location(x,y,action,wall):
    nx = x + dx[action]
    ny = y + dy[action]
    wall_x, wall_y = translate_to_index(wall)
    if (nx < 0 or nx >= ROW_NUM) or (ny < 0 or ny >=COL_NUM) or (nx == wall_x and ny == wall_y) :
        raise WallError
    return nx, ny 


    
        
def Q_learning(table,donut, forbidden, wall, limits):
    EPSILON = 0.1
    x_0, y_0 = translate_to_index(1)
    donut_x, donut_y = translate_to_index(donut)
    forbidden_x, forbidden_y = translate_to_index(forbidden)
    x, y = x_0, y_0;
    time = 0; 
    #print("at the begining")
    #printTable(table)
    random.seed(12345)
    while(True):
        try:
            time += 1
            if time == limits:
                break
            #print(time,"forbidden",table[forbidden_x][forbidden_y])   
            #print("donut",table[donut_x][donut_y])
            if x == forbidden_x and y == forbidden_y:
                table[x][y] = list(table[x][y])
                table[x][y][0] = (1- ALPHA)*table[x][y][0] + ALPHA* (-100)
                x, y = x_0, y_0
                #printTable(table)
                #print("go back to the zero from forbidden")
            elif x == donut_x and y == donut_y:
                table[x][y] = list(table[x][y])
                table[x][y][0] = (1- ALPHA)*table[x][y][0] + ALPHA* (100)
                x, y = x_0, y_0
                #printTable(table)
                #print("go back to zero from donut")
            else:
                if time >= 10000:
                    EPSILON = 0
                flip = random.random()
            
                if flip < EPSILON:
                    action = random.randrange(4)
                else:
                    action = table[x][y].index(max(table[x][y]))
                #print(time,x,y,flip, action,RESULT[action])
                nx, ny = change_location(x,y,action, wall)
                #print("next postion", nx, ny)
                table[x][y] = list(table[x][y])
                table[x][y][action] = (1- ALPHA)*table[x][y][action] + ALPHA* (LIVING_COST + GAMMA * max(table[nx][ny]))
                x, y = nx, ny
                #printTable(table)
            
        except WallError:
            table[x][y] = list(table[x][y])
            table[x][y][action] = (1- ALPHA)*table[x][y][action] + ALPHA* LIVING_COST
            #printTable(table)
            #print("stay at the old state because of the wall")
    return copy.deepcopy(table)

def print_result(table, option, square, forbidden, donut,wall):
    if option =="q":
        if square == wall:
            print("no Q value at the wall")
        else:
            square_x, square_y = translate_to_index(square)
            target = table[square_x][square_y]
            if square == donut or square == forbidden:
                name = "donut" if square == donut else "forbidden"
                print("{0} {1} {2:>6.2f}".format(name,RESULT[1],target[0]))
            else :
                for i in range(4):
                    print("{0} {1:>6.2f}".format(RESULT[i],target[i]))
    else:
        for i in sorted(set(range(1,13)) - {forbidden,donut,wall}):
            x, y = translate_to_index(i)
            print("{0:2} {1}".format(i,RESULT[table[x][y].index(max(table[x][y]))]))

def printTable(table):
    for item in table: 
        for k in item:
            print(k, end = " ")
        print()
    
def usagefunction():
    print(
    '''    This program is used to present a simple Q-learning algorithms. The correct way to use it is  \n
    python3 Qlearning.py location_donut location_forbidden location_wall option_p_or_q [loacation_of_square]\n
    Please retry again with the right format.''')

def main() :
    if len(sys.argv) <=1 or len(sys.argv) > 6 :
        usagefunction()
    else:
        try: 
            if len(sys.argv) in {5,6}:
                donut, forbidden, wall = map(int, sys.argv[1:4])
                option = sys.argv[4]
                if option not in {"p","q"}:
                    raise OptionError
                square = 0 if len(sys.argv) == 5 else int(sys.argv[5])
                table = init_table(donut, forbidden, wall)
                table = Q_learning(table,donut, forbidden, wall, 20000)
                print_result(table,option,square,forbidden, donut,wall)
                #print(RESULT)
                #printTable(table)
                
            else:
                usagefunction()
        except ValueError:
            print("location_donut, location_forbidden, location_wall and location_square should be digits")
        except OptionError:
            print("option_p_or_q should be either p or q.")
            
main()