#jeu de le nuit du code
import pyxel
import random

class App:
    gamestate : int = 0 # 0 = main menu ; 1 = principal ; 2 = shop ; 3 = FIN
    
    def __init__(self):
        pyxel.init(256,256,title="Nuit du code", fps=60)
        pyxel.load('assets/battleShip.pyxres')

        self.upgrades = [("+1 HITPOINT",15),("+3 HITPOINTS",40),("-RELOADTIME",17),("+3 MONEY @ END", 9)]
        self.winner = "player 1"
        self.shoplist = []
        self.arrived_shop = True
        self.arrived_game = 60
        self.players : list[Player] = []
        self.add_player(Player(self, 0, (0,0), (3,11), 3))
        self.add_player(Player(self, 1, (128,128), (4,9), 9))
        self.tutorial = False

        pyxel.run(self.update,self.draw)

    def add_player(self, player : 'Player'):
        # ajoute le joueur a la liste d'ennemies des autres joueurs, de même dans l'autre sens
        for p in self.players:
            player.add_opponent(p)
            p.add_opponent(player)
        # ajoute le joueur a la liste des joueurs
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)
        # retire le joueur de la liste d'ennemie des autres joueurs
        for p in self.players:
            p.remove_opponent(player)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_I):
            App.gamestate = 1
            for player in self.players:
                player.place_set()
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
                    for player in self.players:
                        player.place_set()
                if pyxel.btnp(pyxel.KEY_T) :
                    self.tutorial = not self.tutorial                # logique pour le main menu



            case 1:
                for player in self.players:
                    for i in player.debuffs :
                        match i[0]:
                            case _ : print("non")
                if self.arrived_game > 0 :
                    self.arrived_game-=1
                else:
                    #mouvement joueurs
                    for player in self.players:
                        if pyxel.btnp(player.keys_dict[player.id]["key up"]):
                            player.move_cursor(0,-1)
                        if pyxel.btnp(player.keys_dict[player.id]["key down"]):
                            player.move_cursor(0,1)
                        if pyxel.btnp(player.keys_dict[player.id]["key left"]):
                            player.move_cursor(-1,0)
                        if pyxel.btnp(player.keys_dict[player.id]["key right"]):
                            player.move_cursor(1,0)
                        if pyxel.btnp(player.keys_dict[player.id]["key shoot"]):
                            if player.cooldown <= 0 :
                                player.shoot()
                                player.update_cursors_color(13)

                        if player.cooldown > 0 :
                            player.cooldown -= 1
                        else : player.update_cursors_color()

                        if player.hp_left == 0 :
                            self.winner = f"player {player.id+1}"
                            App.gamestate = 3
                
                
            
            case 2: #shop
                if self.arrived_shop:
                    self.arrived_shop = False
                    self.shoplist = []
                    for i in range(4) :
                        self.shoplist.append(self.upgrades[random.randint(0,3)])
                for i in range(len(self.shoplist)):
                    pyxel.text(50 + 40*i,50,self.shoplist[i][0] + " : " + str(self.shoplist[i][1]),7)  
                

                #Cheats pour la démonstration
                
                if pyxel.btnp(pyxel.KEY_KP_1) :
                    self.players[0].hp -= 1 
                if pyxel.btnp(pyxel.KEY_KP_4) :
                    self.players[0].hp += 1  

                if pyxel.btnp(pyxel.KEY_KP_3) :
                    self.players[1].hp -= 1 
                if pyxel.btnp(pyxel.KEY_KP_6) :
                    self.players[1].hp += 1  

                if pyxel.btnp(pyxel.KEY_KP_7) :
                    self.players[0].frames_between_shoot = [self.player0.frames_between_shoot[0] -1, self.player0.frames_between_shoot[1] -1]
                if pyxel.btnp(pyxel.KEY_KP_2) :
                    self.players[1].frames_between_shoot = [self.player1.frames_between_shoot[0] -1, self.player1.frames_between_shoot[1] -1]


                        
            case 3:
                if pyxel.btnp(pyxel.KEY_SPACE):
                    for player in self.players:
                        player.hp_left = player.hp
                        player.place_set()
                    self.arrived_game = 60
                    App.gamestate = 1
                

    

    def draw(self):
        match App.gamestate:
            case 0:
                #graphismes pour le main menu
                if self.tutorial :
                    pyxel.cls(1)
                    pyxel.text(50,26,"ceci est un jeu de bataille navale différent",7)
                    pyxel.text(20,32,"chaque joueur doit éliminer les bateau de l'autre",7)
                    pyxel.text(20,38,"le plus rapidement possible",7)
                    pyxel.text(20,44,"joueur 1 :  curseur bleu ; joueur 2 : curseur rouge",7)
                    pyxel.text(20,50,"mouvement : ",7)
                    pyxel.text(20,56,"joueur 1 : les fleches ;  joueur 2 : ZQSD ",7)
                    pyxel.text(20,62, "TIR :",7)
                    pyxel.text(20,68,"joueur 1 :  \" m \"  ; joueur 2 : \" v \" ",7)
                else :
                    pyxel.cls(1)
                    pyxel.text(110,70,"Mashbattleship",7)
                    pyxel.text(100,135,"press spacebar to start",7)
                    pyxel.text(100,140,"press t for tutorial",7)



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
                    pyxel.rect(128,0,128,128,5)
                    pyxel.rect(0,128,128,128,14)

                    for player in self.players:
                        player.grid.draw()

                    #dessiner les curseurs
                    for player in self.players:
                        player.draw_cursors()

                    #--------UI joueur 1-----------
                    pyxel.rect(140,115,110,10,0)
                    pyxel.rect(142,117, (106* self.players[0].hp_left) / self.players[0].hp ,6,3)

                    pyxel.text(147,101,str(self.players[0].money),7)
                    pyxel.blt(140,100,1,0,16,8,8,0)
                    #--------UI joueur 2-----------
                    pyxel.rect(5,133,110,10,0)
                    pyxel.rect(7,135, (106* self.players[1].hp_left) / self.players[1].hp ,6,4)

                    pyxel.text(10,146,str(self.players[1].money),7)
                    pyxel.blt(3,145,1,0,16,8,8,0)



            case 2:
                #shop
                pyxel.cls(1)
                pyxel.text(5,5,"SHOP",7)
                pyxel.rect(20,10,210,50,5)
                pyxel.rect(20,70,210,150,5)
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
            "key up" : pyxel.KEY_UP ,
            "key down" : pyxel.KEY_DOWN,
            "key left" : pyxel.KEY_LEFT,
            "key right" : pyxel.KEY_RIGHT,
            "key shoot" : pyxel.KEY_M
        },
        1 : {
            "key up" : pyxel.KEY_Z ,
            "key down" : pyxel.KEY_S,
            "key left" : pyxel.KEY_Q,
            "key right" : pyxel.KEY_D,
            "key shoot" : pyxel.KEY_V
        }
    }


    def __init__(self, app : App, id, grid_offset : tuple[int,int], grid_colors : tuple[int,int], cursor_color : int, opponent = None):
        self.id = id
        self.grid = Grille(self, grid_colors, grid_offset[0], grid_offset[1])
        self.cursorColor = cursor_color

        self.opponents : list[Player] = []
        self.opponentsGrid : list[Grille] = []
        self.opponentGridCusor : dict[Grille, Cursor] = {}
        
        self.cooldown = 0
        self.hp = 9
        self.hp_left = 9
        self.set : list[DaddyBoat] = [Boat1,Boat3x,Boat2x,BoalLtl] #liste de 4 bateaux
        self.money = 0
        self.frames_between_shoot = [20,40] #(tir réussi, tir raté)
        self.bonus_money =  0 # argent en + par round
        self.items = []
        self.debuffs = [] #[(debuff,frames_restantes)]

    def set_opponent(self, opponent : 'Player'):
        self.opponent = opponent
        self.opponentGrid = opponent.grid
        self.cursor = Cursor(self, self.opponentGrid)

    def add_opponent(self, player : 'Player'):
        self.opponents.append(player)
        self.opponentsGrid.append(player.grid)
        self.opponentGridCusor[player.grid] = Cursor(self, player.grid)

    def remove_opponent(self, player : 'Player'):
        self.opponents.remove(player)
        self.opponentsGrid.remove(player.grid)
        self.opponentGridCusor.pop(player.grid)

    def place_set(self):
        finalSet : list[DaddyBoat] = []
        hp = self.hp
        while hp > 0:
            n = 0
            boat = random.choice(self.set)
            if boat in [Boat1]:
                n = 1
            elif boat in [Boat2x,Boat2y]:
                n = 2
            elif boat in [Boat3x,Boat3y,BoalLtl,BoatLtr,BoatLbr,BoatLbl]:
                n = 3
            if n <= hp:
                hp -= n
                finalSet.append(boat)

        self.grid.generate_boat(finalSet)

    def move_cursor(self, x, y):
        for cursor in self.opponentGridCusor.values():
            x1, y1 = cursor.pos[0]+x, cursor.pos[1]+y
            if self.grid.on_grid((x1,y1)):
                cursor.pos = [x1,y1]

    def shoot(self):
        for cursor in self.opponentGridCusor.values():
            cursor.shoot(self)

    def update_cursors_color(self, color : int|None = None):
        color = color if color else self.cursorColor
        for cursor in self.opponentGridCusor.values():
            cursor.col = color
    
    def draw_cursors(self):
        for cursor in self.opponentGridCusor.values():
            cursor.drawcursor()



class DaddyBoat:
    #coordonnées relative au type du bateau
    relativeCoordinates : dict[tuple[int,int], dict[str, int]] = {} #{coordonnées relatifs a ceux données lors de l'initialisation  : {kwargs pour l'image ('u','v','w' et 'h' sont obligatoire sinon la texture ne seras pas rendue)}}
    
    def __init__(self, grid : "Grille", coord : tuple[int,int], *, is_fake : bool = False):
        self.grid = grid
        self.size = grid.tileSize
        self.coordinates : dict[tuple[int,int], dict[str, bool|dict[str, int]]] = {} #{coordonnées : {'alive' (et 'dead'){kwargs pour l'image ('u','v','w' et 'h' sont obligatoire sinon la texture ne seras pas rendue)}}}
        for key, value in self.relativeCoordinates.items():
            self.coordinates[(coord[0]+key[0],coord[1]+key[1])] = {'alive' : True, 'is_trap' : False, 'textureKwargs' : value}

        self.alive : bool = True if self.coordinates else False

        self.is_fake = is_fake
        

    def get_coordinates(self) -> list[tuple[int,int]]:
        return self.coordinates.keys()
        
    def get_shot(self, coord : tuple[int,int]) -> bool:
        # verifie que les bateau soit bien a ces coordonnées et qu'il soit bien en vie
        if coord in self.coordinates and self.coordinates[coord]['alive']:
            self.coordinates[coord]['alive'] = False
            # verifie que le bateau soit entierement mort
            if all(boat['alive'] == False for boat in self.coordinates.values()):
                self.alive = False

            #verifie si le bateau est un faux
            if self.is_fake:
                return False
            return True
        
        return False

        
    
    def draw(self):
        for key, value in self.coordinates.items():
            if value['alive']:
                if 'alive' in value['textureKwargs'] and all(i in value['textureKwargs']['alive'] for i in ['u','v','w','h']): #verifie que toutes les données necessaire a l'image sont présente
                    pyxel.blt(
                        x=self.grid.offsetx+key[0]*self.size,
                        y=self.grid.offsety+key[1]*self.size,
                        img=0,
                        colkey=0,
                        **value['textureKwargs']['alive']
                    )
                else: #dessine la texture par défaut (carré blanc)
                    pyxel.rect(self.grid.offsetx+2+key[0]*self.size,
                            self.grid.offsetx+2+key[1]*self.size,
                            self.size-4,
                            self.size-4,
                            7)
            else:
                if 'dead' in value['textureKwargs'] and all(i in value['textureKwargs']['dead'] for i in ['u','v','w','h']): #verifie que toutes les données necessaire a l'image sont présente
                    pyxel.blt(
                        x=self.grid.offsetx+key[0]*self.size,
                        y=self.grid.offsety+key[1]*self.size,
                        img=0,
                        colkey=1,
                        **value['textureKwargs']['dead']
                    )
class Boat1(DaddyBoat):
    relativeCoordinates = {(0,0) : {'alive' : {'u' : 0, 'v' : 0, 'w' : 16, 'h' : 16},
                                    'dead' : {'u' : 0, 'v' : 16, 'w' : 16, 'h' : 16}}}

class Boat2x(DaddyBoat):
    relativeCoordinates = {(0,0) : {'alive' : {'u' : 16, 'v' : 0, 'w' : 16, 'h' : 16},
                                    'dead' : {'u' : 16, 'v' : 16, 'w' : 16, 'h' : 16}}, 
                           (1,0) : {'alive' : {'u' : 16, 'v' : 0, 'w' : 16, 'h' : 16, 'rotate' : 180},
                                    'dead' : {'u' : 16, 'v' : 16, 'w' : 16, 'h' : 16, 'rotate' : 180}}}

class Boat2y(DaddyBoat):
    relativeCoordinates = {(0,0) : {'alive' : {'u' : 16, 'v' : 0, 'w' : 16, 'h' : 16, 'rotate' : 90},
                                    'dead' : {'u' : 16, 'v' : 16, 'w' : 16, 'h' : 16, 'rotate' : 90}}, 
                           (0,1) : {'alive' : {'u' : 16, 'v' : 0, 'w' : 16, 'h' : 16, 'rotate' : -90},
                                    'dead' : {'u' : 16, 'v' : 16, 'w' : 16, 'h' : 16, 'rotate' : -90}}}

class Boat3x(DaddyBoat):
    relativeCoordinates = {(0,0) : {'alive' : {'u' : 16, 'v' : 0, 'w' : 16, 'h' : 16},
                                    'dead' : {'u' : 16, 'v' : 16, 'w' : 16, 'h' : 16}}, 
                           (1,0) : {'alive' : {'u' : 32, 'v' : 0, 'w' : 16, 'h' : 16},
                                    'dead' : {'u' : 32, 'v' : 16, 'w' : 16, 'h' : 16}}, 
                           (2,0) : {'alive' : {'u' : 16, 'v' : 0, 'w' : 16, 'h' : 16, 'rotate' : 180},
                                    'dead' : {'u' : 16, 'v' : 16, 'w' : 16, 'h' : 16, 'rotate' : 180}}}

class Boat3y(DaddyBoat):
    relativeCoordinates = {(0,0) : {'alive' : {'u' : 16, 'v' : 0, 'w' : 16, 'h' : 16, 'rotate' : 90},
                                    'dead' : {'u' : 16, 'v' : 16, 'w' : 16, 'h' : 16, 'rotate' : 90}}, 
                           (0,1) : {'alive' : {'u' : 32, 'v' : 0, 'w' : 16, 'h' : 16, 'rotate' : 90},
                                    'dead' : {'u' : 32, 'v' : 16, 'w' : 16, 'h' : 16, 'rotate' : 90}}, 
                           (0,2) : {'alive' : {'u' : 16, 'v' : 0, 'w' : 16, 'h' : 16, 'rotate' : -90},
                                    'dead' : {'u' : 16, 'v' : 16, 'w' : 16, 'h' : 16, 'rotate' : -90}}}

class BoalLtl(DaddyBoat):
    relativeCoordinates = {(0,0) : {'alive' : {'u' : 48, 'v' : 0, 'w' : 16, 'h' : 16, 'rotate' : -90},
                                    'dead' : {'u' : 48, 'v' : 16, 'w' : 16, 'h' : 16, 'rotate' : -90}},
                           (1,0) : {'alive' : {'u' : 16, 'v' : 0, 'w' : 16, 'h' : 16, 'rotate' : 180},
                                    'dead' : {'u' : 16, 'v' : 16, 'w' : 16, 'h' : 16, 'rotate' : 180}},
                           (0,1) : {'alive' : {'u' : 16, 'v' : 0, 'w' : 16, 'h' : 16, 'rotate' : -90}, 
                                    'dead' : {'u' : 16, 'v' : 16, 'w' : 16, 'h' : 16, 'rotate' : -90}}}

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
    def __init__(self, player : Player, grid : 'Grille', position = [0,0]):
        self.pos = position
        self.player = player
        self.grid = grid

        self.offsetx = self.grid.offsetx
        self.offsety = self.grid.offsety
        self.col = self.player.cursorColor
    
    def drawcursor(self) :
        pyxel.rectb(self.offsetx + 16*self.pos[0], self.offsety + 16*self.pos[1],16,16,self.col)
        pyxel.rectb(self.offsetx-1 + 16*self.pos[0], self.offsety-1 + 16*self.pos[1],18,18,self.col)

    def shoot(self, attacker : Player|None = None) -> bool:
        if self.grid.shoot_boat((self.pos[0], self.pos[1])):
            self.grid.player.hp_left -= 1
            if attacker:
                attacker.cooldown = self.player.frames_between_shoot[0]
                attacker.money += 1
        else:
            if attacker:
                attacker.cooldown = self.player.frames_between_shoot[1]
    



class Grille :
    def __init__(self, player : Player, colors : tuple[int,int], offsetx : int = 0, offsety : int = 0):
        self.player = player
        self.width : int = 8
        self.height : int = 8
        self.tileSize = 16
        
        self.offsetx = offsetx
        self.offsety = offsety
        self.col1 = colors[0]
        self.col2 = colors[1]

        self.boats : list[DaddyBoat] = []
        self.coordinatesBoat : dict[tuple[int,int], DaddyBoat] = {} #{coordonnée : bateau a ces coordonnées}

        
        
    def on_grid(self, coord : tuple[int,int]):
        # verifie que les coordonnées soient bien sur la grille
        if 0 <= coord[0] < self.width and 0 <= coord[1] < self.height:
            return True
        return False
    
    def shoot_boat(self, coord : tuple[int,int]) -> bool:
        # retour demande au bateau si il a été touché si il est sur cette case sinon retourne False
        if coord in self.coordinatesBoat:
            return self.coordinatesBoat[coord].get_shot(coord)
        return False
    
    def draw(self):
        for i in range(8):
            for j in range(8):
                if (i+j)%2:
                    pyxel.rect(16*i +self.offsetx,16*j + self.offsety ,16,16,self.col1)
                else:
                    pyxel.rect(16*i +self.offsetx,16*j + self.offsety ,16,16,self.col2)

        for boat in self.boats:
            boat.draw()
    
    def generate_boat(self, boats_list : list[DaddyBoat]):
        # reiniitalise la grille
        self.boats = []
        coords : list[tuple[int,int]] = []
        # parcours tout les bateaux qu'on souhaite placer
        for boat in boats_list:
            stop = 10
            ok = False
            # essaye de placer les bateaux
            while not (ok or stop <= 0):
                ok = True
                x = random.randrange(self.width)
                y = random.randrange(self.height)
                temp = boat(self, (x,y))
                # verifie que le batteau de touche aucun autre batteau deja placé
                for coord in temp.get_coordinates():
                    if coord in coords or not (self.on_grid(coord)):
                        ok = False
                        break
                # ajoute le bateau si les conditions précédantes sont respectées
                if ok:
                    coords += temp.get_coordinates()
                    self.boats.append(temp)
                # sinon retire la vie associées au joueur (en développement)
                else:
                    if boat in [Boat1]:
                        n = 1
                    elif boat in [Boat2x,Boat2y]:
                        n = 2
                    elif boat in [Boat3x,Boat3y,BoalLtl,BoatLtr,BoatLbr,BoatLbl]:
                        n = 3
                stop -= 1
        for boat in self.boats:
            for coord in boat.coordinates:
                self.coordinatesBoat[coord] = boat
    
    def add_fake_boat(self, boat : DaddyBoat):
        coords = []
        stop = 10
        ok = False
        # essaye de placer les bateaux
        while not ok or stop > 0:
            stop -= 1
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            temp = boat(self, (x,y), is_fake=True)
            # verifie que le batteau de touche aucun autre batteau deja placé
            for coord in temp.get_coordinates():
                if coord in coords or not (self.on_grid(coord)):
                    ok = False
                    break
            # ajoute le bateau si les conditions précédantes sont respectées
            if ok:
                coords += temp.get_coordinates()
                self.boats.append(temp)

    def add_trap_to_boat(self, trap_amount):
        #selectionne une coordonnée aléatoire possedant un ou plisieurs bateaux puis défini cette case come piégée
        boats = random.choices(self.coordinatesBoat.items(), k=trap_amount)
        for coordinates, boat in boats:
            boat : DaddyBoat
            boat.coordinates[coordinates]['is_trap'] = True
            
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