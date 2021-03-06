import socket
import sys
import json
import time
import cherrypy
import webbrowser
from random import *
from sys import maxsize
from math import inf as infinity
from os import system
import msgpack
"""
all variables :
    t0 for the time processing
    human for human turn(used in minimax) and comp for the ai
    temp_board is used to deepcopy the actual board without changing it
    board is the board we'll take from the json
    counter for the possibilities
    depth is the depth we want to check in advance = the numbers of moves checked in advance
"""
HEADER = 4096
PORT = 3001
FORMAT = 'utf-8'
SERVER = "localhost"
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
t0=time.time()
human = -1
computer = +1
name = "Jack Uzi"
board = []
counter = 0
choosing_depth=4
points = 0
randomtext = ["C'est moi le plus fort dans ma forme","J'vais au casino en claquettes","02 880","C'est Jack, Jack Uzi",
            "Tu vas moins faire le malin","T'es dans ta jalousie","Nous on joue pas de la flute","Les oreilles ont des murs",
            "Ici c'est nous les meilleurs","Au jour d'aujourd'hui","Ils voyent bien qu'on va tout péter",
            "Persone ne gagne ici","Moi j'ai peur de personne","J'me lève à 14h du matin","On fait du vélo sans les mains",
            "Maintenant tu fais moins le malin", "Nous on fait pas de calin","Pan Pan!","Y'en a qu'ont le mental et y'en a qu'on que l'emmental",
            "Jack septe pas le pardon","Jack septe les chèques","Jack célère"]
def game_over(state):
    if len(all_moves(state))== 0:
        return True
    else:
        return False


    
def all_moves(state):
    """
    param: state, it takes the actual board and will check all possible moves
    return : case, returns a lsit of dicts with all the possible moves
    """
    case = []
    cells = set()
    # cells = []
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if 0 < len(cell) < 5:
                cells.add((x, y))
    for x,y in cells:
        for a,b in cells:   
            if x-1 <= a <= x+1 and y-1 <= b <= y+1:
                if a == x and b == y:
                    pass
                else :
                    if len(state[a][b]) <= 5- len(state[x][y]):
                        case.append({"from":(x,y), "to":(a,b),"tscore": int})
    return case

def set_move(x,y,a,b,state):
    """
    set the move on board if coordinates are valid
    param : player is the current playing (not sure if needed)
    parm x and y : row and col from
    param a and b : row and col to
    """
    global board
    state[a][b].extend(state[x][y])
    state[x][y].clear()


def eval(state):
    """
    param: state is the catual board that will be evaluated
    here it's for the leaves
    for the moment 0 is for comp and 1 for human
    """
    points = 0
    for row in state: 
        for col in row:
            length = len(col)
            # if 0 is the color of computer and 1 for the human
            if length == 0:
                pass
            elif 0<length<5:
                if col[-1]==1:
                    points -= 1
                elif col[-1]==0:
                    points +=1
            elif length == 5:
                if col[-1]==1:
                    points -= 5
                    # for a in range(len(col)-1):
                    #     if a == 0:
                    #         points-=1
                elif col[-1]==0:
                    points +=5
                    # for a in range(len(col)-1):
                    #     if a == 1:
                    #         points+=1
    
    # I should put a max and min that a and b shouldn't pass
                
    return points
def choose_depth(state):
    """
    param: state, checking all the movements we can still do
    and setting the max depth in the minimax
    """
    global choosing_depth
    pile_count = 0
    # if len(all_moves(state)) ==0:
    #     choosing_depth = 0
    for x in state:
        for y in x:
            if len(y) ==1:
                pile_count +=1
    # print("pile count :",pile_count)
    if pile_count >= 16:
        choosing_depth = 3
    elif 10<= pile_count<16:
        choosing_depth = 4
    elif pile_count ==1:
        choosing_depth = 1
    else:
        choosing_depth =2
def minimax(state,depth,alpha,beta,player):
    """
    param: state, the board, that changes further when we iterate it in the loop
    param: depth, it's the depth we chose outside the function and will decrease for each iteration we do
        the starting depth is for ex 4, it's the root, and 1 is the leaves. It can't go under 1
    param: alpha and beta for pruning useless branches and optimizing
    param: player stands for human or computer turn, as it will maximize at comp turn and minimize at human turn
    return : returns the best move of its children
    """
    
    global counter
    global points
    global choosing_depth
    
    temp_board = msgpack.packb(state)
    # new_state = msgpack.unpackb(temp_board)
    if player == computer:
        best = {"from":list,"to":list,"tscore":-infinity}        # - inf because we want the algo to maximize for the computer
    else :
        best = {"from":list,"to":list,"tscore":+infinity}

    if depth == 0 or game_over(state):          #when we're at the level under the leaves, leaves depth = 1

        return best

    for move in all_moves(state):      #the loop that iterates itself when going inside it's children
        # x= move["from"][0]
        # y = move["from"][1]
        x, y = move["from"]
        # a = move["to"][0]
        # b = move["to"][1]
        a,b = move["to"]
        
        
        # temp_board = msgpack.packb(state)   # using this copy of board to re iterate itself and making a new board for each child
        new_state = msgpack.unpackb(temp_board)
        # new_state = state[:]        
        set_move(x,y,a,b,new_state) 
        
        if depth == 1: # if leaf
            counter +=1
            move["tscore"] = eval(new_state) #it calls the evaluate to put score on the leaves

        else:       #we iterate the function minimax by taking the best score the children returned
            move["tscore"] = minimax(new_state,depth-1,alpha,beta,-player)["tscore"] # = the best score from children
                
        
        # compare score with adjacent nodes
        if player == computer:  #maximize
            
            if best["tscore"]< move["tscore"]:
                best = move     #max value
            alpha = max(alpha,best["tscore"])
            
            
        else :
            if best["tscore"]> move["tscore"]:
                best = move     #min value
            beta = min(beta,best["tscore"])
            
        if beta <= alpha:
            # print("break")
            break
        
    return best #returns only the best score of the children
def send ():
    
    with open("matricules.json") as file:
        msg = json.loads(file.read())
    print(msg)
    msg = json.dumps(msg)
    # message = pickle.dumps(msg)
    # print(message)
    message = msg.encode(FORMAT)
    print(message)
    
    
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    # client.send(send_length)
    client.send(message)
    print(msg_length)
    

class Server:
    
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    # @cherrypy.expose
    
        
    @cherrypy.expose
    def default(self,atr= "abc"):
        return "<h1 >404 </h1 ><p> Page not found ! Fin du monde !</p>"

    @cherrypy.expose
    def move(self):
        # Deal with CORS
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        if cherrypy.request.method == "OPTIONS":
            return ''
        
        body = cherrypy.request.json
        board = body["game"]
        player = body["players"]
        choose_depth(board)

        if player == name:
            best_move = minimax(board,choosing_depth,-infinity,infinity,computer)
        else :
            best_move = minimax(board,choosing_depth,-infinity,infinity,human)
        x,y = best_move["from"]
        a,b = best_move["to"]
        print(body)
        return {
                "move": {
                    "from": [x, y],
                    "to": [a, b]
                },
                "message": choice(randomtext)
            }

    @cherrypy.expose
    def ping(self):
        send()
        return "pong"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080
    

    webbrowser.open('http://localhost:8080/ping')
    print('browser started !')
    
    # send()
    
    
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())