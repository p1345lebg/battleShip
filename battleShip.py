#jeu de le nuit du code
import pyxel
import random

class App:
    gamestate : int = 0 # 0 = main menu ; 1 = principal ; 2 = shop ; 3 = FIN
    

    def __init__(self):
        pyxel.init(256,256,title="Nuit du code", fps=60)
        pyxel.load('assets/battleShip.pyxres')

        self.upgrades = [("+1 HITPOINT",15),("+3 HITPOINTS",40),("-RELOADTIME",17),("+3 MONEY @ END", 9)]
        self.grillep1 = Grille()
        self.grillep2 = Grille(128,128)
        self.winner = "player 1"
        self.shoplist = []
        self.arrived_shop = True
        self.arrived_game = 60
        self.player0 = Player(0, self.grillep1)
        self.player1 = Player(1, self.grillep2)
        #on est obligé de faire ça pour avoir l'autre joueur dans les 2
        self.player0.set_opponent(self.player1)
        self.player1.set_opponent(self.player0)

        self.tutorial = False

        pyxel.run(self.update,self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_I):
            App.gamestate = 1
            self.player0.place_set()
            self.player1.place_set()
        elif pyxel.btnp(pyxel.KEY_O):
            App.gamestate = 2
        elif pyxel.btnp(pyxel.KEY_P):
            App.gamestate = 3
        elif pyxel.btnp(pyxel.KEY_U):
            App.gamestate = 0

        match App.gamestate:
            case 0:
                if pyxel.btnp(pyxel.KEY_SPACE):
                    App.gamestate = 1
                    self.player0.place_set()
                    self.player1.place_set()
                if pyxel.btnp(pyxel.KEY_T) :
                    self.tutorial = not self.tutorial                # logique pour le maineenu
            case 1:
                for i in self.player1.debuffs :
                    match i[0]:
                        case _ : pass
                if self.arrived_game > 0 :
                    self.arrived_game-=1
                else:
                    #mouvement joueur 1
                    if pyxel.btnp(self.player0.keys_dict[0]["key up"]):
                        if self.player0.cursor.pos[1] > 0 :
                            self.player0.cursor.pos[1] -=1
                    if pyxel.btnp(self.player0.keys_dict[0]["key down"]):
                        if self.player0.cursor.pos[1] < 7 :
                            self.player0.cursor.pos[1] += 1
                    if pyxel.btnp(self.player0.keys_dict[0]["key left"]):
                        if self.player0.cursor.pos[0] > 0 :
                            self.player0.cursor.pos[0] -= 1
                    if pyxel.btnp(self.player0.keys_dict[0]["key right"]):
                        if self.player0.cursor.pos[0] < 7 :
                            self.player0.cursor.pos[0] += 1
                    if pyxel.btnp(self.player0.keys_dict[0]["key shoot"]):
                        if self.player0.cooldown == 0 :
                            self.player0.cursor.shoot()
                            self.player0.cursor.col = 13
                    #mouvement joueur 1
                    if pyxel.btnp(self.player1.keys_dict[1]["key up"]):
                        if self.player1.cursor.pos[1] > 0 :
                            self.player1.cursor.pos[1] -=1
                    if pyxel.btnp(self.player1.keys_dict[1]["key down"]):
                        if self.player1.cursor.pos[1] < 7 :
                            self.player1.cursor.pos[1] += 1
                    if pyxel.btnp(self.player1.keys_dict[1]["key left"]):
                        if self.player1.cursor.pos[0] > 0 :
                            self.player1.cursor.pos[0] -= 1
                    if pyxel.btnp(self.player1.keys_dict[1]["key right"]):
                        if self.player1.cursor.pos[0] < 7 :
                            self.player1.cursor.pos[0] += 1
                    if pyxel.btnp(self.player1.keys_dict[1]["key shoot"]):
                        if self.player1.cooldown == 0:
                            self.player1.cursor.shoot()
                            self.player1.cursor.col = 13
                            
                    

                    if self.player0.cooldown > 0 :
                        self.player0.cooldown -= 1
                    else : self.player0.cursor.col = 3
                    if self.player1.cooldown > 0 :
                        self.player1.cooldown -= 1
                    else : self.player1.cursor.col = 9

                    if self.player0.hp_left == 0 :
                        self.winner = "player 2"
                        App.gamestate = 3
                    if self.player1.hp_left == 0 :
                        self.winner = "player 1"
                        App.gamestate = 3
                
                
            
            case 2: #shop
                if self.arrived_shop:
                    self.arrived_shop = False
                    self.shoplist = []
                    for i in range(4) :
                        self.shoplist.append(self.upgrades[random.randint(0,3)])
                for i in range(len(self.shoplist)):
                    pyxel.text(50 + 40*i,50,self.shoplist[i][0] + " : " + str(self.shoplist[i][1]),7)  
                 
                if pyxel.btnp(pyxel.KEY_KP_1) :
                    self.player0.hp += 1 
                #Cheats pour la démonstration
                
                if pyxel.btnp(pyxel.KEY_KP_1) :
                    self.player0.hp -= 1 
                if pyxel.btnp(pyxel.KEY_KP_4) :
                    self.player0.hp += 1  

                if pyxel.btnp(pyxel.KEY_KP_3) :
                    self.player1.hp -= 1 
                if pyxel.btnp(pyxel.KEY_KP_6) :
                    self.player1.hp += 1  

                if pyxel.btnp(pyxel.KEY_KP_7) :
                    self.player0.frames_between_shoot = [self.player0.frames_between_shoot[0] -1, self.player0.frames_between_shoot[1] -1]
                if pyxel.btnp(pyxel.KEY_KP_2) :
                    self.player1.frames_between_shoot = [self.player1.frames_between_shoot[0] -1, self.player1.frames_between_shoot[1] -1]
                    
                        
            case 3:
                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.player0.hp_left = self.player0.hp
                    self.player1.hp_left = self.player1.hp
                    self.player0.place_set()
                    self.player1.place_set()
                    self.arrived_game = 60
                    App.gamestate = 1
                

    
    def draw(self):
        match App.gamestate:
            case 0:
                if self.tutorial :
                    pyxel.cls(1)
                    pyxel.text(50,26,"ceci est un jeu de bataille navale différent",7)
                    pyxel.text(20,32,"chaque joueur doit éliminer les bateau de l'autre",7)
                    pyxel.text(20,38,"le plus rapidement possible",7)
                    pyxel.text(20,44,"joueur 1 :  curseur bleu ; joueur 2 : curseur rouge",7)
                    pyxel.text(20,50,"mouvement : ",7)
                    pyxel.text(20,56,"joueur 1 : ZQSD  ;  joueur 2 : les fleches",7)
                    pyxel.text(20,62, "TIR :",7)
                    pyxel.text(20,68,"joueur 1 : V  ;  joueur 2 : \" ; \" ",7)
                else :
                    pyxel.cls(1)
                    pyxel.text(110,128,"Mashbattleship",7)
                    pyxel.text(100,135,"press spacebar to start",7)
                    pyxel.text(100,140,"press t for tutorial",7)

                #graphismes pour le main menu

            case 1:
                #graphismes jeu principal
                if self.arrived_game > 0:
                    pyxel.cls(13)
                    if self.arrived_game > 40 :
                        pyxel.text(128,128,"3",7)
                    elif self.arrived_game > 20 :
                        pyxel.text(128,128,"2",7)
                    else : pyxel.text(128,128,"1",7)
                else:
                    pyxel.cls(13)
                    pyxel.rect(0,0,127,127,11)
                    pyxel.rect(128,128,127,127,11)
                    self.grillep1.draw(3,11)
                    self.grillep2.draw(4,9)
                    #dessiner les curseurs
                    self.player0.cursor.drawcursor()
                    self.player1.cursor.drawcursor()
                    #UI joueur 1
                    pyxel.text(140,20,"money : " + str(self.player0.money),7)
                    pyxel.text(140,25,"hp : " + str(self.player0.hp_left),7)
                    #UI joueur 2
                    
                    pyxel.text(20,140,"money : " + str(self.player1.money),7)
                    pyxel.text(20,145,"hp : " + str(self.player1.hp_left),7)

                
            
            case 2:
                #shop
                pyxel.cls(1)
                pyxel.text(5,5,"SHOP",7)
                pyxel.rect(20,10,210,50,5)
                pyxel.rect(20,70,210,150,5)
                shop_populate()
                for i in range(4):
                    pyxel.rect(27 + 50*i,15,45,43,13)
                    pyxel.rect(27 + 50*i,80,45,130,13)
            
            case 3:
                pyxel.cls(1)
                pyxel.text(110,128,self.winner + " wins",7)
                pyxel.text(100,137,"press spacebar to start again",7)



#---------------------------------------
#-------------Classes-------------------
#---------------------------------------
class Player:
    keys_dict : dict[int, dict[str, int]] = {
        0 : {
            "key up" : pyxel.KEY_Z ,
            "key down" : pyxel.KEY_S,
            "key left" : pyxel.KEY_Q,
            "key right" : pyxel.KEY_D,
            "key shoot" : pyxel.KEY_V
        },
        1 : {
            "key up" : pyxel.KEY_UP ,
            "key down" : pyxel.KEY_DOWN,
            "key left" : pyxel.KEY_LEFT,
            "key right" : pyxel.KEY_RIGHT,
            "key shoot" : pyxel.KEY_SEMICOLON
        }
    }


    def __init__(self, id, grid : 'Grille', opponent = None):
        self.id = id
        self.grid = grid
        
        self.opponent = opponent
        if opponent != None :
            self.set_opponent(opponent)
            self.opponentGrid = opponent.grid
        self.cooldown = 0
        self.hp = 9
        self.hp_left = 9
        self.set : list[DaddyBoat] = [Boat1,Boat3x,Boat2x,Boat3y] #liste de 4 bateaux
        self.money = 0
        self.frames_between_shoot = [20,40] #(tir réussi, tir raté)
        self.bonus_money =  0 # argent en + par round
        self.items = []
        self.debuffs = [] #[(debuff,frames_restantes)]

    def set_opponent(self, opponent : 'Player'):
        self.opponent = opponent
        self.opponentGrid = opponent.grid
        self.cursor = Cursor(self, self.opponentGrid)

    def place_set(self):
        finalSet : list[DaddyBoat] = []
        hp = self.hp
        while hp > 0:
            n = 0
            temp = random.choice(self.set)
            if temp == Boat1:
                n = 1
            elif temp == Boat2x or temp == Boat2y:
                n = 2
            else:
                n = 3
            if n <= hp:
                hp -= n
                finalSet.append(temp)

        self.grid.generate_boat(finalSet)



class DaddyBoat:

    relativeCoordinates : dict[tuple[int,int], dict[str, int]] = {}
    
    def __init__(self, grid : "Grille", coord : tuple[int,int], is_trap : bool = False):
        self.grid = grid
        self.size = grid.tileSize
        self.coordinates : dict[tuple[int,int], dict[str, bool|dict[str, int]]] = {}
        for key, value in self.relativeCoordinates.items():
            self.coordinates[(coord[0]+key[0],coord[1]+key[1])] = {'alive' : True, 'textureKwargs' : value}

        self.alive : bool = True if self.coordinates else False

        self.is_trap = is_trap
        

    def get_coordinates(self) -> list[tuple[int,int]]:
        return self.coordinates.keys()
        
    def get_shot(self, coord : tuple[int,int]) -> bool:
        if coord in self.coordinates and self.coordinates[coord]['alive']:
            self.coordinates[coord]['alive'] = False
            if all(boat['alive'] == False for boat in self.coordinates.values()):
                self.alive = False
            return True
        
        return False

        
    
    def draw(self):
        for key, value in self.coordinates.items():
            if value['alive']:
                if value['textureKwargs'] and all(i in value['textureKwargs'] for i in ['u','v','w','h']):
                    pyxel.blt(
                        x=self.grid.offsetx+key[0]*self.size,
                        y=self.grid.offsety+key[1]*self.size,
                        img=0,
                        colkey=0,
                        **value['textureKwargs']
                    )
                else:
                    pyxel.rect(self.grid.offsetx+2+key[0]*self.size,
                            self.grid.offsetx+2+key[1]*self.size,
                            self.size-4,
                            self.size-4,
                            7)
    
class Boat1(DaddyBoat):
    relativeCoordinates = {(0,0) : {'u' : 0, 'v' : 0, 'w' : 16, 'h' : 16}}

class Boat2x(DaddyBoat):
    relativeCoordinates = {(0,0) : {}, 
                           (1,0) : {}}

class Boat2y(DaddyBoat):
    relativeCoordinates = {(0,0) : {}, 
                           (0,1) : {}}

class Boat3x(DaddyBoat):
    relativeCoordinates = {(0,0) : {}, 
                           (1,0) : {}, 
                           (2,0) : {}}

class Boat3y(DaddyBoat):
    relativeCoordinates = {(0,0) : {}, 
                           (0,1) : {}, 
                           (0,2) : {}}

class BoalLtl(DaddyBoat):
    relativeCoordinates = {(0,0) : {},
                           (1,0) : {},
                           (0,1) : {}}

class BoatLtr(DaddyBoat):
    relativeCoordinates = {(0,0) : {},
                           (-1,0): {}, 
                           (0,1) : {}}

class BoatLbl(DaddyBoat):
    relativeCoordinates = {(0,0) : {}, 
                           (1,0) : {}, 
                           (0,-1): {}}

class BoatLbr(DaddyBoat):
    relativeCoordinates = {(0,0) : {},
                           (-1,0): {}, 
                           (0,-1): {}}


class Cursor :
    def __init__(self, player : Player, opponentGrid : 'Grille'):
        self.pos = [0,0]
        self.player = player
        self.id = player.id
        if self.id == 0 : 
            self.offsetx = 128
            self.offsety = 128
            self.col = 3
        else :
            self.offsetx = 0
            self.offsety = 0 
            self.col = 9
        self.opponentGrid = opponentGrid
    
    def drawcursor(self) :
        pyxel.rectb(self.offsetx + 16*self.pos[0], self.offsety + 16*self.pos[1],16,16,self.col)
        pyxel.rectb(self.offsetx-1 + 16*self.pos[0], self.offsety-1 + 16*self.pos[1],18,18,self.col)

    def shoot(self) -> bool:
        if self.opponentGrid.shoot_boat((self.pos[0], self.pos[1])):
            self.player.cooldown = self.player.frames_between_shoot[0]
            self.player.opponent.hp_left -= 1
        else:
            self.player.cooldown = self.player.frames_between_shoot[1]
    



class Grille :
    def __init__(self, offsetx : int = 0, offsety : int = 0):
        self.width : int = 8
        self.height : int = 8
        self.tileSize = 16
        
        self.offsetx = offsetx
        self.offsety = offsety

        self.boats : list[DaddyBoat] = []
        self.coordinatesBoat : dict[tuple[int,int], DaddyBoat] = {}

        
        
    def on_grid(self, coord : tuple[int,int]):
        if 0 <= coord[0] < self.width and 0 <= coord[1] < self.height:
            return True
        return False
    
    def shoot_boat(self, coord : tuple[int,int]) -> bool:
        if coord in self.coordinatesBoat:
            return self.coordinatesBoat[coord].get_shot(coord)
        return False
    
    def draw(self,col1,col2):
        col = col1
        for i in range(8):
            for j in range(8):
                pyxel.rect(16*i +self.offsetx,16*j + self.offsety ,16,16,col)
                if col == col1: col = col2
                else : col = col1
            if col == col1: col = col2
            else : col = col1

        for boat in self.boats:
            boat.draw()
    
    def generate_boat(self, boats_list : list[DaddyBoat]):
        self.boats = []
        coords : list[tuple[int,int]] = []
        for boat in boats_list:
            stop = 10
            ok = False
            while not (ok or stop <= 0):
                ok = True
                x = random.randrange(self.width)
                y = random.randrange(self.height)
                temp = boat(self, (x,y))
                for coord in temp.get_coordinates():
                    if coord in coords or not (self.on_grid(coord)):
                        ok = False
                        break
                if ok:
                    coords += temp.get_coordinates()
                    self.boats.append(temp)
                stop -= 1
        for boat in self.boats:
            for coord in boat.coordinates:
                self.coordinatesBoat[coord] = boat
    
    def add_fake_boat(self, boat):
        coords = []
        ok = False
        while not ok:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            temp = boat(self, (x,y))
            for coord in temp.get_coordinates():
                if coord in coords or not (self.on_grid(coord)):
                    ok = False
                    break
            if ok:
                coords += temp.get_coordinates()
                self.boats.append(temp)
            
#--------------------------------
#----------FUNC LOGIC------------
#--------------------------------
shopsets = [[(1),(2,"hor"),(3,"vert"),(3,"L normal")], [(1),(1),(1),(1)], [(1),(3,"L normal"),(3,"L symmétrie horizontale"),(3,"L double symmétrie")],]  

#remplace shopsets par les classes de bateau correspondantes + leur prix(adt)
shopitems = [[]] 
#name, price, function,
def shop_populate():
    #render
    for i in range(4):
        pyxel.text(29 + 50*i, 17,"price:",7)
        pyxel.text(29 + 50*i, 85,"price:",7)
    pass
        

def debuff_invert(player : Player,debuff_index):
    player.keys_dict[player.id]["key up"] = Player.keys_dict[player.id]["key down"]
    player.keys_dict[player.id]["key down"] = Player.keys_dict[player.id]["key up"]
    player.keys_dict[player.id]["key left"] = Player.keys_dict[player.id]["key right"]
    player.keys_dict[player.id]["key right"] = Player.keys_dict[player.id]["key left"]
    
    player.debuffs[debuff_index][1] -= 1
    #fin
    if player.debuffs[debuff_index][1] == 0 :
        player.keys_dict[player.id]["key up"] = Player.keys_dict[player.id]["key up"]
        player.keys_dict[player.id]["key down"] = Player.keys_dict[player.id]["key down"]
        player.keys_dict[player.id]["key left"] = Player.keys_dict[player.id]["key left"]
        player.keys_dict[player.id]["key right"] = Player.keys_dict[player.id]["key right"]
    
def debuff_snare(player : Player,debuff_index):
    player.frames_between_shoot = 40

    player.debuffs[debuff_index][1] -= 1
    #fin 
    if player.debuffs[debuff_index][1] == 0 :
        player.frames_between_shoot = 0
        
    
#--------------------------------
#----------FUNC DRAWS------------
#--------------------------------




if __name__ == "__main__":
    App()