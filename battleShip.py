#jeu de le nuit du code
import pyxel
import random

class App:
    gamestate : int = 0 # 0 = main menu ; 1 = principal ; 2 = shop ; 3 = FIN
    
    def __init__(self):
        pyxel.init(256,256,title="Nuit du code", fps=60)
        pyxel.load('assets/battleShip.pyxres')

        self.upgrades = [("+1 HITPOINT",15),("+3 HITPOINTS",40),("-RELOADTIME",17),("+3 MONEY @ END", 9)]
        self.winner : Player|None = None
        self.shoplist = []
        self.arrived_shop = True
        self.arrived_game = 60
        self.players : list[Player] = []
        self.add_player(Player(self, 0, (0,0), (3,11), 3, name="player 1"))
        self.add_player(Player(self, 1, (128,128), (4,9), 9, name="player 2"))
        self.playersAlive : list[Player] = [player for player in self.players]
        self.tutorial = False
        self.shopgrid = Grille(width=4,height=2,rendertype=1)
        

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
            self.arrived_shop = True
            self.arrived_game = 60
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
                    self.playersAlive = [player for player in self.players]
                    for player in self.players:
                        player.place_set()
                if pyxel.btnp(pyxel.KEY_T) :
                    self.tutorial = not self.tutorial                
                    # logique pour le main menu



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
                            if player in self.playersAlive:
                                self.playersAlive.remove(player)
                match len(self.playersAlive):
                    case 1: # victoire d'un des deux joueur
                        self.playersAlive[0].roundpoint = True
                        self.winner = self.playersAlive[0]
                        App.gamestate = 3
                    case 0: # égalié
                        self.winner = None
                        App.gamestate = 3
                
                
            
            case 2: #shop
                if self.arrived_shop:
                    self.arrived_shop = False
                    self.shoplist = []
                    self.players[0].menucursor = Cursor(self.players[0],self.shopgrid,position=[0,0])
                    self.players[1].menucursor = Cursor(self.players[1],self.shopgrid,position=[0,0])
                    for i in range(4) :
                        self.shoplist.append(self.upgrades[random.randint(0,3)])
                    print(self.shoplist)

                for player in self.players:
                        if pyxel.btnp(player.keys_dict[player.id]["key up"]):
                            player.move_cursor(0,-1,"shop",self.shopgrid)
                            print(player.menucursor.pos)
                        if pyxel.btnp(player.keys_dict[player.id]["key down"]):
                            player.move_cursor(0,1,"shop",self.shopgrid)
                        if pyxel.btnp(player.keys_dict[player.id]["key left"]):
                            player.move_cursor(-1,0,"shop",self.shopgrid)
                        if pyxel.btnp(player.keys_dict[player.id]["key right"]):
                            player.move_cursor(1,0,"shop",self.shopgrid)

                
                

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
                    self.players[0].frames_between_shoot = [self.players[0].frames_between_shoot[0] -1, self.players[0].frames_between_shoot[1] -1]
                if pyxel.btnp(pyxel.KEY_KP_2) :
                    self.players[1].frames_between_shoot = [self.players[1].frames_between_shoot[0] -1, self.players[1].frames_between_shoot[1] -1]


                        
            case 3:
                
                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.playersAlive = [player for player in self.players]
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
                    pyxel.text(50,26,"ceci est un jeu de bataille navale different",7)
                    pyxel.text(20,32,"chaque joueur doit eliminer les bateau de l'autre",7)
                    pyxel.text(20,38,"le plus rapidement possible",7)
                    pyxel.text(20,52, "controles :", 7)
                    for i in range(len(self.players)):
                        x = 20
                        y = 60+68*i
                        player = self.players[i]
                        color = player.cursorColor
                        pyxel.rectb(x,y,220,60,color)
                        pyxel.text(x+4, y+4, str(player), color)

                        pyxel.text(x+4, y+12, 'bouger :', color)
                        pyxel.blt(x+24, y+20, img=2,**player.keys_texture_dict[player.id]['key up'])
                        pyxel.blt(x+4, y+40, img=2,**player.keys_texture_dict[player.id]['key left'])
                        pyxel.blt(x+24, y+40, img=2,**player.keys_texture_dict[player.id]['key down'])
                        pyxel.blt(x+44, y+40, img=2,**player.keys_texture_dict[player.id]['key right'])

                        pyxel.text(x+84, y+12, 'tirer :', color)
                        pyxel.blt(x+84, y+20, img=2,**player.keys_texture_dict[player.id]['key shoot'])
                else :
                    pyxel.cls(1)
                    pyxel.text(100,70,"Mashbattleship",7)
                    pyxel.text(118,135,"press",7)
                    pyxel.blt(104,150, 2, 0, 32, 48, 16, 0)
                    pyxel.text(112, 170, 'to start', 7)

                    pyxel.text(128-44,200,"press  t  for tutorial",7)
                    pyxel.blt(128-44+22, 195, 2, 48, 32, 16, 16, 0, scale=0.8)



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
                        player.draw_cursors(1)

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
                    match self.shoplist[i][0]:
                        case "+1 HITPOINT":
                            pyxel.text(28 + 50*i,81,"+1HP",7)
                        case "+3 HITPOINTS":
                            pyxel.text(28 + 50*i,81,"+3HP",7)
                        case "-RELOADTIME":
                            pyxel.text(28 + 50*i,81,"-RELOAD",7)
                        case "+3 MONEY @ END":
                            pyxel.text(28 + 50*i,81,"+3  @END",7)
                            pyxel.blt(36 + 50*i,81,1,0,16,8,8,0)
                
                for player in self.players:
                        player.menucursor.drawcursor(2)

                    

            case 3:
                if self.winner:
                    pyxel.cls(self.winner.cursorColor)
                    text = f'{str(self.winner)} wins"'
                    pyxel.text(128-(len(text)*pyxel.FONT_WIDTH)/2,128,text,7)
                else:
                    pyxel.cls(13)
                    pyxel.text(122,128,'tie',7)

                pyxel.text(70,137,"press spacebar to start again",7)
                pyxel.circ(70,100,20,0)
                pyxel.circ(186,100,20,0)



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
    keys_texture_dict : dict[int,dict[str, dict[str, int]]] = {
        0 : {
            "key up" : {'u' : 0, 'v' : 0, 'w' : 16, 'h' : 16, 'colkey' : 0},
            "key down" : {'u' : 16, 'v' : 0, 'w' : 16, 'h' : 16, 'colkey' : 0},
            "key left" : {'u' : 32, 'v' : 0, 'w' : 16, 'h' : 16, 'colkey' : 0},
            "key right" : {'u' : 48, 'v' : 0, 'w' : 16, 'h' : 16, 'colkey' : 0},
            "key shoot" : {'u' : 64, 'v' : 0, 'w' : 16, 'h' : 16, 'colkey' : 0}
        },
        1 : {
            "key up" : {'u' : 0, 'v' : 16, 'w' : 16, 'h' : 16, 'colkey' : 0},
            "key down" : {'u' : 16, 'v' : 16, 'w' : 16, 'h' : 16, 'colkey' : 0},
            "key left" : {'u' : 32, 'v' : 16, 'w' : 16, 'h' : 16, 'colkey' : 0},
            "key right" : {'u' : 48, 'v' : 16, 'w' : 16, 'h' : 16, 'colkey' : 0},
            "key shoot" : {'u' : 64, 'v' : 16, 'w' : 16, 'h' : 16, 'colkey' : 0}
        }
    }


    def __init__(self, app : App, id, grid_offset : tuple[int,int], grid_colors : tuple[int,int], cursor_color : int, name : str|None = None):
        self.id = id if (id in Player.keys_dict) and (id in Player.keys_texture_dict) else 0
        self.grid = Grille(self,8,8, grid_colors, grid_offset[0], grid_offset[1])
        self.cursorColor = cursor_color
        self.roundpoint = False

        self.name : str = name
        if not name:
            self.name = f'player {self.id}'


        self.opponents : list[Player] = []
        self.opponentsGrid : list[Grille] = []
        self.opponentGridCusor : dict[Grille, Cursor] = {}
        self.menucursor : Cursor
        self.cooldown = 0
        self.hp = 9
        self.hp_left = 9
        self.set : list[DaddyBoat] = [Boat1,Boat3x,Boat2x,BoatLtl] #liste de 4 bateaux
        self.money = 0
        self.frames_between_shoot = [20,40] #(tir réussi, tir raté)
        self.bonus_money =  0 # argent en + par round
        self.items = []
        self.debuffs = [] #[(debuff,frames_restantes)]

    def __str__(self) -> str:
        return self.name
    
    def change_name(self, name) -> None:
        self.name = name



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
            elif boat in [Boat3x,Boat3y,BoatLtl,BoatLtr,BoatLbr,BoatLbl]:
                n = 3
            if n <= hp:
                hp -= n
                finalSet.append(boat)

        self.grid.generate_boat(finalSet)

    def move_cursor(self, x, y,type = "game", shopgrid = None):
        match type :
            case "game":
                for cursor in self.opponentGridCusor.values():
                    x1, y1 = cursor.pos[0]+x, cursor.pos[1]+y
                    if self.grid.on_grid((x1,y1)):
                        cursor.pos = [x1,y1]
            
            case "shop":
                x1, y1 = self.menucursor.pos[0]+x, self.menucursor.pos[1]+y
                if shopgrid.on_grid((x1,y1)):
                    self.menucursor.pos = [x1,y1]

    def shoot(self):
        for cursor in self.opponentGridCusor.values():
            cursor.shoot(self)

    def update_cursors_color(self, color : int|None = None):
        color = color if color else self.cursorColor
        for cursor in self.opponentGridCusor.values():
            cursor.col = color
    
    def draw_cursors(self,gamestate):
        for cursor in self.opponentGridCusor.values():
            cursor.drawcursor(gamestate)

    def enter_shop(self,shopgrid) :
        self.cursor = Cursor(self,shopgrid)


class SpriteGroup:
    def __init__(self, *sprite : 'Sprite') -> None:
        self.sprites : list[Sprite] = [*sprite]
        for sprites in self.sprites:
            sprites.set_group(self)

    def add_sprite(self, *sprites : 'Sprite') -> None:
        for sprite in sprites:
            sprite.set_group(self)
            self.sprites.append(sprite)

    def remove_sprite(self, *sprites : 'Sprite') -> None:
        for sprite in sprites:
            if sprite in self.sprites:
                self.sprites.remove(sprite)

    def clear(self):
        self.sprites.clear()

    def get_sprites(self) -> list['Sprite']:
        return self.sprites

class Sprite: # classe qui gere les images (en prevision de futures ajouts)
    group : SpriteGroup|None = None
    def __init__(self, img : int|pyxel.Image, u : float, v : float, w : float, h : float, colkey : int|None = None, *, offset : tuple[int,int]|None = None, scale : float|None = None, rotate : float|None = None):
        self.img = img
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.colkey = colkey
        self.offsetx, self.offsety = offset if offset else (0,0)
        self.rotate = rotate
        self.scale = scale

    def kill(self) -> None:
        if self.group:
            self.group.remove_sprite(self)

    def in_group(self):
        if self.group:
            return True
        return False

    def set_group(self, group : 'SpriteGroup') -> None:
        if group == self.group:
            return
        if self.group:
            self.group.remove_sprite(self)
        self.group = group
        if self.group:
            self.group.add_sprite(self)

    def draw(self, x, y, *, scale : float|None = None, rotate : float|None = None) -> None:
        if self.scale: scale = scale*self.scale if scale else self.scale
        if self.rotate: rotate = rotate+self.rotate if rotate else self.rotate
        pyxel.blt(x+self.offsetx, y+self.offsety, self.img, self.u, self.v, self.w, self.h, self.colkey, rotate=rotate, scale=scale)

class SpriteAnimated(Sprite):
    def __init__(self, delay, *sprite : Sprite, loop : bool = False):
        self.delay = delay
        self.sprites = sprite

        self.loop = loop
        self.delay = delay+1
        self.frameCount = 0
        self.maxIndex = len(self.sprites)-1
        self.index = 0
        self.finished = False


    def draw(self, x, y, *, scale = None, rotate = None):
        self.frameCount += 1
        if self.frameCount > self.delay:
            self.frameCount = 0
            self.index += 1
        if self.index > self.maxIndex:
            if not self.loop:
                self.finished = True
                self.kill()
                return
            self.index = 0
        self.sprites[self.index].draw(x, y, scale=scale, rotate=rotate)
    
    def copy(self) -> 'SpriteAnimated':
        return SpriteAnimated(self.delay, *self.sprites, loop=self.loop)




class DaddyBoat:
    name : str = "DaddyBoat" #nom du bateau (utile pour les textures)
    #coordonnées relative au type du bateau
    relativeCoordinates : dict[tuple[int,int], dict[str, 'Sprite']] = {} #{coordonnées relatifs a ceux données lors de l'initialisation  : {'alive' (et 'dead') : {kwargs pour l'image ('u','v','w' et 'h' sont obligatoire sinon la texture ne seras pas rendue)}}}
    
    def __init__(self, grid : "Grille", coord : tuple[int,int], *, is_fake : bool = False):
        self.grid = grid
        self.size = grid.tileSize
        self.coordinates : dict[tuple[int,int], dict[str, bool|dict[str, Sprite]]] = {} #{coordonnées : alive? , {'alive' (et/ou 'dead') : {kwargs pour l'image ('u','v','w' et 'h' sont obligatoire sinon la texture ne seras pas rendue)}}}}
        for key, value in self.relativeCoordinates.items():
            self.coordinates[(coord[0]+key[0],coord[1]+key[1])] = {'alive' : True, 'is_trap' : False, 'sprites' : value}

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

            # renvoie le tire si la portion du bateau est un piege
            if self.coordinates[coord]['is_trap']:
                for grid in self.grid.player.opponentsGrid:
                    grid.shoot_boat(coord)

            #verifie si le bateau est un faux
            if self.is_fake:
                return False
            return True
        
        return False

        
    
    def draw(self):
        for key, state in self.coordinates.items():
            if state['alive']:
                if 'alive' in state['sprites']:
                    state['sprites']['alive'].draw(key[0]*self.size+self.grid.offsetx, key[1]*self.size+self.grid.offsety)
                else:
                    pyxel.rect(self.grid.offsetx+2+key[0]*self.size,
                            self.grid.offsetx+2+key[1]*self.size,
                            self.size-4,
                            self.size-4,
                            7)
            else:
                if 'dead' in state['sprites']:
                    state['sprites']['dead'].draw(key[0]*self.size+self.grid.offsetx, key[1]*self.size+self.grid.offsety)

    def __str__(self):
        return f'{self.coordinates.keys()}'



class Boat1(DaddyBoat):
    name = "Boat1"
    relativeCoordinates = {
        (0,0) :{'alive' : Sprite(0, 0, 0, 16, 16, colkey=0), 
                'dead' : Sprite(0, 0, 16, 16, 16, colkey=1)}
    }

class Boat2x(DaddyBoat):
    name = "Boat2x"
    relativeCoordinates = {
        (0, 0): {
            "alive": Sprite(0, 16, 0, 16, 16, colkey=0),
            "dead": Sprite(0, 16, 16, 16, 16, colkey=1)
        },
        (1, 0): {
            "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=180),
            "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=180)
        }
    }

class Boat2y(DaddyBoat):
    name = "Boat2y"
    relativeCoordinates = {
        (0, 0): {
            "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=90),
            "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=90)
        },
        (0, 1): {
            "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=-90),
            "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=-90)
        }
    }

class Boat3x(DaddyBoat):
    name = "Boat3x"
    relativeCoordinates = {
        (0, 0): {
            "alive": Sprite(0, 16, 0, 16, 16, colkey=0),
            "dead": Sprite(0, 16, 16, 16, 16, colkey=1)
        },
        (1, 0): {
            "alive": Sprite(0, 32, 0, 16, 16, colkey=0),
            "dead": Sprite(0, 32, 16, 16, 16, colkey=1)
        },
        (2, 0): {
            "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=180),
            "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=180)
        }
    }

class Boat3y(DaddyBoat):
    name = "Boat3y"
    relativeCoordinates = {
        (0, 0): {
            "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=90),
            "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=90)
        },
        (0, 1): {
            "alive": Sprite(0, 32, 0, 16, 16, colkey=0, rotate=90),
            "dead": Sprite(0, 32, 16, 16, 16, colkey=1, rotate=90)
        },
        (0, 2): {
            "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=-90),
            "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=-90)
        }
    }

class BoatLtl(DaddyBoat):
    name = "BoatLtl"
    relativeCoordinates = {
        (0, 0): {
            "alive": Sprite(0, 48, 0, 16, 16, colkey=0, rotate=-90),
            "dead": Sprite(0, 48, 16, 16, 16, colkey=1, rotate=-90)
        },
        (1, 0): {
            "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=180),
            "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=180)
        },
        (0, 1): {
            "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=-90),
            "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=-90)
        }
    }

class BoatLtr(DaddyBoat):
    name = "BoatLtr"
    relativeCoordinates = {
        (0, 0): {
            "alive": Sprite(0, 48, 0, 16, 16, colkey=0, rotate=0),
            "dead": Sprite(0, 48, 16, 16, 16, colkey=1, rotate=0)
        },
        (-1, 0): {
            "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=0),
            "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=0)
        },
        (0, 1): {
            "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=90),
            "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=90)
        }
    }

class BoatLbl(DaddyBoat):
    name = "BoatLbl"
    relativeCoordinates = {
        (0, 0): {
            "alive": Sprite(0, 48, 0, 16, 16, colkey=0, rotate=180),
            "dead": Sprite(0, 48, 16, 16, 16, colkey=1, rotate=180)
        },
        (1, 0): {
            "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=180),
            "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=180)
        },
        (0, -1): {
            "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=-90),
            "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=-90)
        }
    }

class BoatLbr(DaddyBoat):
    name = "BoatLbr"
    relativeCoordinates = {
        (0, 0): {
            "alive": Sprite(0, 48, 0, 16, 16, colkey=0, rotate=180),
            "dead": Sprite(0, 48, 16, 16, 16, colkey=1, rotate=180)
        },
        (-1, 0): {
            "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=0),
            "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=0)
        },
        (0, -1): {
            "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=-90),
            "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=-90)
        }
    }




class Cursor :
    def __init__(self, player : Player, grid : 'Grille', position = [0,0]):
        self.pos = position
        self.player = player
        self.grid = grid

        self.offsetx = self.grid.offsetx
        self.offsety = self.grid.offsety
        self.col = self.player.cursorColor
    
    def drawcursor(self,gamestate) :
        match gamestate:
            case 1:
                pyxel.rectb(self.offsetx + 16*self.pos[0], self.offsety + 16*self.pos[1],16,16,self.col)
                pyxel.rectb(self.offsetx-1 + 16*self.pos[0], self.offsety-1 + 16*self.pos[1],18,18,self.col)
            case 2:
                
                if self.pos[1] == 1:
                    

                    pyxel.rectb(27 + 50*self.pos[0],80,45,130,self.col)
                else : pyxel.rectb(27 + 50*self.pos[0],15,45,43,self.col)

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
    def __init__(self, player = None ,width : int = 0, height : int = 0, colors = [0,2], offsetx : int = 0, offsety : int = 0,rendertype : int = 0):
        if player != None:
            self.player = player
        if width != 0:
            self.width : int = width
        if height != 0:
            self.height : int = height
        self.tileSize = 16
        
        self.offsetx = offsetx
        self.offsety = offsety
        if colors != None:
            self.col1 = colors[0]
            self.col2 = colors[1]

        self.rendertype = rendertype #si le rendertype != 0 , la grille est invisible, le curseur render tout
        if rendertype == 0:
            self.boats : list[DaddyBoat] = []
            self.coordinatesBoat : dict[tuple[int,int], DaddyBoat] = {} #{coordonnée : bateau a ces coordonnées}

        self.explosions : SpriteGroup = SpriteGroup()

        
        
    def on_grid(self, coord : tuple[int,int]):
        # verifie que les coordonnées soient bien sur la grille
        if 0 <= coord[0] < self.width and 0 <= coord[1] < self.height:
            
            return True
        return False
    
    def shoot_boat(self, coord : tuple[int,int]) -> bool:
        # retour demande au bateau si il a été touché si il est sur cette case sinon retourne False
        if coord in self.coordinatesBoat:
            self.explosions.add_sprite(Explosion((self.offsetx+coord[0]*self.tileSize, self.offsety+coord[1]*self.tileSize), False))
            print(self.explosions.get_sprites())
            return self.coordinatesBoat[coord].get_shot(coord)
        
        self.explosions.add_sprite(Explosion((self.offsetx+coord[0]*self.tileSize, self.offsety+coord[1]*self.tileSize)))
        print(self.explosions.get_sprites())
        return False
    
    def draw(self):
        match self.rendertype:
            case 0:
                for i in range(8):
                    for j in range(8):
                        if (i+j)%2:
                            pyxel.rect(16*i +self.offsetx,16*j + self.offsety ,16,16,self.col1)
                        else:
                            pyxel.rect(16*i +self.offsetx,16*j + self.offsety ,16,16,self.col2)

                for boat in self.boats:
                    boat.draw()
                for explosion in self.explosions.get_sprites():
                    explosion.draw()
                
        
    def generate_boat(self, boats_list : list[DaddyBoat]):
        # reiniitalise la grille
        self.explosions.clear()
        self.boats = []
        self.coordinatesBoat = {}
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
                    elif boat in [Boat3x,Boat3y,BoatLtl,BoatLtr,BoatLbr,BoatLbl]:
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


class Explosion(Sprite):
    textures : dict[bool, SpriteAnimated] = {
        True : SpriteAnimated(
            20,
            Sprite(0, 0, 32, 16, 16, colkey=0),
            Sprite(0, 16, 32, 16, 16, colkey=0),
            Sprite(0, 32, 32, 16, 16, colkey=0),
            Sprite(0, 48, 32, 16, 16, colkey=0),
            Sprite(0, 64, 32, 16, 16, colkey=0)
        ),
        False : SpriteAnimated(
            20,
            Sprite(0, 0, 48, 16, 16, colkey=0),
            Sprite(0, 16, 48, 16, 16, colkey=0),
            Sprite(0, 32, 48, 16, 16, colkey=0)
        )
    }
    def __init__(self, coordinates : tuple[int,int], in_water : bool = True):
        """doit etre placé dans une variable 'self.explosions'"""
        self.in_water = in_water
        self.coordinates : tuple[int,int] = coordinates
        self.animation = self.textures[self.in_water].copy()

    def draw(self):
        self.animation.draw(*self.coordinates)
        if self.animation.finished:
            self.kill()





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