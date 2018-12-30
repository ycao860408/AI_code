import collections
import queue

"""The following is the goal test shown as a constant integer"""

GOAL_STATE = 4321

"""
This is a action list. 0 is to start from the bottom, 1 is starting above the first pancake, 2 is starting
abovethe second pancake. It is nonsense to start above the third, only resulting a flip of the top pancake
without changing the configuration of the all pancakes.
"""

ACTION = list(range(3))

"""
The following is the data structure to store the node. It can carry the information like
    
state: the current state
parent: the parent of the current state
paction: what action did its parent do to get the current state
pcost: the past cost to get the current state from the beginning
hcost: the heuristic cost at this moment.
"""

Node = collections.namedtuple("Node","state parent paction pcost hcost")

"""
This is used to test whether the current state is the goal test. Because python has trouble to compare
string. I just convert it to an integer first and then compare them
"""
def goal_test(node):
    return int(node.state)==GOAL_STATE

"""
This is used to find the heuristic cost at current state. Find the largest ID which is not equal to the right
ID at that place. The right ID is given by 4-index of the array where the real ID stays in.
"""

def get_hcost(state):
    temp = list(map(int,list(state)))
    max=0
    for i in range(4):
        if(temp[i]+i-4!=0 and temp[i]>max):
            max=temp[i]
    return max

"""
For the following xkey functions are used to defined the StupidPriorityQueue, which is a min-pq maintaining the
order based on different standard. And this xkey functions are used to regulate the standard. For example, if it 
is based on the akey, then it maintain its order based on the sum of the real cost and heristic cost. and also 
notice that each key function returns a tuple whose second element is the absolute value of the state. This is 
used to break the tire in the case that two states have the equal first element.
"""

def akey(item):
    return item.pcost+item.hcost, -int(item.state)
def ukey(item):
    return item.pcost, -int(item.state)
def gkey(item):
    return item.hcost, -int(item.state)

"""
As discribed as above, this is a self-defined min-pq. And its constructor enable it to define different objects
based on different sorting standard. And its default sorting is based on the one required by uniform cost search.
"""


class StupidPriorityQueue:
    def __init__(self,choice='u'):
        self.__list = []
        self.__choice = choice
    
    def add(self,item):
        self.__list.append(item)
        if self.__choice =="a":
            self.__list.sort(key=akey)
        elif self.__choice =="u":
            self.__list.sort(key =ukey)
        elif self.__choice =="g":
            self.__list.sort(key = gkey)
    
    def get(self):
        if len(self.__list):
            return self.__list.pop(0)
        else:
            return None
    
    def empty(self):
        return len(self.__list)==0

"""The following is just output the instruction when the program begins to run."""

def printstart():
    print("""\nThis program is designed to apply different searching methods. You are required to type in a string in the form of '####X'. Each '#' represents a digit among 1, 2, 3, 4 and 'X' is used to indicate the methods you are going to use. For example, you may type in "1324a".\n
    d: \t Depth First Search \n
    b: \t Breadth First Search \n
    u: \t Uniform-Cost Search \n
    g: \t Greedy Search \n
    a: \t A* Search \n""")    

"""
The following is to generate a new state based on the current state, the method and the action it is going to use.
The result is achieved by spliting the string of the current state with considering the action. And the past cost 
is updated by the next action 4-{0,1,2}. And the heuristic cost is either 0 or calculated by the former function.
Then the result is returned within the data structure mentioned previously.
"""


def generate_child(action,node,method):
    state = node.state[::-1] if action==0 else node.state[:action]+node.state[:action-1:-1]
    parent = node.state
    paction = action
    pcost = node.pcost +(4-action)
    hcost = 0 if method in {"b","d","u"} else get_hcost(state)
    return Node(state,parent,paction,pcost,hcost)

"""
BFS method based on the graph search version. 
the frontier is the fringe discussed in the class. It is a FIFO queue here and the the fontier_set is a set used 
to check the membership in the queue. It is fast to carry an in operation because of its hash property. And all 
the explored one is stored in a dictionary called explored. I use this data structure because it is easy to 
retrive its elements and also its build-in function explored_dict.keys() is a view that can dynamically reflect 
the membership. So the finally all the explored nodes are stored in the dictionary. The result is None or an
unempty dictioinary.
"""


def BFS(problem):
    root = Node(problem,None,None,0,0)
    explored_dict=dict()
    frontier_set= set()
    frontier = queue.Queue()
    if goal_test(root): 
        explored_dict[root.state]=root
        return explored_dict
    frontier.put(root)
    frontier_set.add(root.state)
    while True:
        if frontier.empty(): return None
        node = frontier.get()
        frontier_set.remove(node.state)
        explored_dict[node.state]=node
        for action in ACTION:
            child = generate_child(action,node,"b")
            if (child.state not in explored_dict.keys()) and (child.state not in frontier_set):
                if goal_test(child):
                    explored_dict[child.state] = child
                    return explored_dict
                frontier.put(child)
                frontier_set.add(child.state)

"""
The code for DFS is almost the same as the BFS except for here the fringe is realized by a LIFO queue.
"""

def DFS(problem):
    root = Node(problem,None,None,0,0)
    explored_dict=dict()
    frontier_set= set()
    frontier = queue.LifoQueue()
    if goal_test(root): 
        explored_dict[root.state]=root
        return explored_dict
    frontier.put(root)
    frontier_set.add(root.state)
    while True:
        if frontier.empty(): return None
        node = frontier.get()
        frontier_set.remove(node.state)
        explored_dict[node.state]=node
        for action in ACTION:
            child = generate_child(action,node,"d")
            if (child.state not in explored_dict.keys()) and (child.state not in frontier_set):
                if goal_test(child):
                    explored_dict[child.state] = child
                    return explored_dict
                frontier.put(child)
                frontier_set.add(child.state)

"""
The code for the UCS is almost the same as the BFS and DFS, except for the fringe here is realized by 
the StupidPriorityQueue with the default standard to sort. that is, sorting based on the past cost to get the
current state.
"""

def UCS(problem):
    root = Node(problem,None,None,0,0)
    explored_dict=dict()
    frontier_set= set()
    frontier = StupidPriorityQueue()
    if goal_test(root): 
        explored_dict[root.state]=root
        return explored_dict
    frontier.add(root)
    frontier_set.add(root.state)
    while True:
        if frontier.empty(): return None
        node = frontier.get()
        frontier_set.remove(node.state)
        explored_dict[node.state]=node
        for action in ACTION:
            child = generate_child(action,node,"u")
            if (child.state not in explored_dict.keys()) and (child.state not in frontier_set):
                if goal_test(child):
                    explored_dict[child.state] = child
                    return explored_dict
                frontier.add(child)
                frontier_set.add(child.state)

"""
The code for the GRE is almost the same as the UCS, except for the fringe here is realized by
the StupidPriorityQueue with the greedy standard to sort, that is, sorting based on the heuristic cost.
"""
                
def GRE(problem):
    root = Node(problem,None,None,0,get_hcost(problem))
    explored_dict=dict()
    frontier_set= set()
    frontier = StupidPriorityQueue("g")
    if goal_test(root): 
        explored_dict[root.state]=root
        return explored_dict
    frontier.add(root)
    frontier_set.add(root.state)
    while True:
        if frontier.empty(): return None
        node = frontier.get()
        frontier_set.remove(node.state)
        explored_dict[node.state]=node
        for action in ACTION:
            child = generate_child(action,node,"g")
            if (child.state not in explored_dict.keys()) and (child.state not in frontier_set):
                if goal_test(child):
                    explored_dict[child.state] = child
                    return explored_dict
                frontier.add(child)
                frontier_set.add(child.state)

"""
The code for the GRE is almost the same as the UCS and GRE, except for the fringe here is realized by
the StupidPriorityQueue with the A* standard to sort, that is, sorting based on the sum of  heuristic cost and
past cost to get the current state.
"""

def ASTAR(problem):
    root = Node(problem,None,None,0,get_hcost(problem))
    explored_dict=dict()
    frontier_set= set()
    frontier = StupidPriorityQueue("a")
    if goal_test(root): 
        explored_dict[root.state]=root
        return explored_dict
    frontier.add(root)
    frontier_set.add(root.state)
    while True:
        if frontier.empty(): return None
        node = frontier.get()
        frontier_set.remove(node.state)
        explored_dict[node.state]=node
        for action in ACTION:
            child = generate_child(action,node,"a")
            if (child.state not in explored_dict.keys()) and (child.state not in frontier_set):
                if goal_test(child):
                    explored_dict[child.state] = child
                    return explored_dict
                frontier.add(child)
                frontier_set.add(child.state)

"""
The following function is to print the result satisfying the requirement. 
"""
                


def printAns(ans,method):
    if ans is None:
        print("There is no solution for this input!")
    else:
        pathQueue = queue.LifoQueue()
        state = "4321"
        if method in {"b","d","u"}:
            pathQueue.put("{state}  g={pcost:<3}".format(**ans[state]._asdict()))
        else:
            pathQueue.put("{state}  g={pcost:<3} h={hcost:<3}".format(**ans[state]._asdict()))

        while ans[state].parent is not None:
            action = ans[state].paction
            state = ans[state].parent
            stateAction = "|"+state if action == 0 else state[:action] + "|" +state[action:]
            g = ans[state].pcost
            h = ans[state].hcost
            if method in {"b","d","u"}:
                output = "{stateAction} g={g:<3}".format(**locals())
            else:
                output = "{stateAction} g={g:<3} h={h:<3}".format(**locals())
            pathQueue.put(output)

        while not pathQueue.empty():
            print(pathQueue.get())

def checkDigit(strDigit,scope):
    return all(map(lambda x: int(x) in scope,list(strDigit)))


def getResult(problem, method):
    if method =="a":
        return ASTAR(problem)
    elif method =="b":
        return BFS(problem)
    elif method =="d":
        return DFS(problem)
    elif method =="g":
        return GRE(problem)
    else:
        return UCS(problem)

def main():
    printstart()
    while True:
        signal = input("Enter a string with example format and type q to quit!\n")
        if signal == "":
            print("The input should not be empty. Enter again, please.")
            continue
        elif signal =='q':
            break
        elif len(signal) != 5:
            print("Invalid Input! Only require 5 characters! Enter again, please.")
            continue
        else:
            try:
                problem = signal[:4]
                method = signal[4]
                if method not in {"a","d","b","g","u"}:
                    print("Invalid method character! Enter again, please.")
                    continue
                elif not checkDigit(problem,{1,2,3,4}):
                    print("ID character should be among 1,2,3,4! Enter again, please.")
                    continue
                else:
                    ans = getResult(problem,method)
                    print("\n")
                    printAns(ans,method)
            except ValueError:
                print("Non-digit is found in ID part! Enter again, please.")
main()