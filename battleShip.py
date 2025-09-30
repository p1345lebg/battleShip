#jeu de le nuit du code
import pyxel
import random
import os
import json
import ast

class App:
    gamestate : int = 0 # 0 = main menu ; 1 = principal ; 2 = shop ; 3 = FIN ; 4 = choix ressourcepack
    ressourcePack = None
    
    def __init__(self):
        pyxel.init(256,256,title="Nuit du code", fps=60)
        App.ressourcePack = RessourcePack()
        self.ressourcePack = App.ressourcePack

        self.upgrades = [("+1 HITPOINT",15),("+3 HITPOINTS",40),("-RELOADTIME",17),("+3 MONEY @ END", 9)]
        self.winner : Player|None = None
        self.shoplist = []
        self.arrived_shop = True
        self.arrived_game = 60
        self.players : list[Player] = []
        self.add_player(Player(self, 0, (0,0), (3,11), 3, 0, name="player 1"))
        self.add_player(Player(self, 1, (128,128), (4,9), 9, 1, name="player 2"))
        self.playersAlive : list[Player] = [player for player in self.players]
        self.tutorial = False
        self.shopgrid = ShopGrid(self.players[0])
        self.ressourcePackGrid = RessourcePackGrid(self.players[0])
        

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
        elif pyxel.btnp(pyxel.KEY_R):
            App.gamestate = 4

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
                        for player in self.players:
                            player.money+=player.bonus_money
                        self.playersAlive[0].roundpoint = True
                        self.winner = self.playersAlive[0]
                        App.gamestate = 3
                    case 0: # égalié
                        for player in self.players:
                            player.money+=player.bonus_money
                        self.winner = None
                        App.gamestate = 3
                
                
            
            case 2: #shop
                if self.arrived_shop:
                    self.arrived_shop = False
                    self.shopgrid.generate_shop()
                    self.shopgrid.player = self.winner if self.winner else self.players[0]

                self.shopgrid.update()


                
                

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

            case 4:
                self.ressourcePackGrid.update()
                

    

    def draw(self):
        match App.gamestate:
            case 0:
                #graphismes pour le main menu
                if self.tutorial :
                    textColor = App.ressourcePack.ui["tutorial"]["text"]
                    background = App.ressourcePack.ui["tutorial"]["background"]
                    pyxel.cls(background)
                    pyxel.text(50,26,"ceci est un jeu de bataille navale different",textColor)
                    pyxel.text(20,32,"chaque joueur doit eliminer les bateau de l'autre",textColor)
                    pyxel.text(20,38,"le plus rapidement possible",textColor)
                    pyxel.text(20,52, "controles :", textColor)
                    for i in range(len(self.players)):
                        x = 20
                        y = 60+68*i
                        player = self.players[i]
                        color = App.ressourcePack.players[str(player.color)]["tutorial color"]
                        pyxel.rectb(x,y,220,60,color)
                        pyxel.text(x+4, y+4, str(player), color)

                        pyxel.text(x+4, y+12, 'bouger :', color)
                        if player.keys_dict[player.id]['key up'] in App.ressourcePack.keys:
                            App.ressourcePack.keys[player.keys_dict[player.id]['key up']].draw(x+24, y+20)
                        if player.keys_dict[player.id]['key left'] in App.ressourcePack.keys:
                            App.ressourcePack.keys[player.keys_dict[player.id]['key left']].draw(x+4, y+40)
                        if player.keys_dict[player.id]['key down'] in App.ressourcePack.keys:
                            App.ressourcePack.keys[player.keys_dict[player.id]['key down']].draw(x+24, y+40)
                        if player.keys_dict[player.id]['key right'] in App.ressourcePack.keys:
                            App.ressourcePack.keys[player.keys_dict[player.id]['key right']].draw(x+44, y+40)

                        pyxel.text(x+84, y+12, 'tirer :', color)
                        if player.keys_dict[player.id]['key shoot'] in App.ressourcePack.keys:
                            App.ressourcePack.keys[player.keys_dict[player.id]['key shoot']].draw(x+84, y+20)
                else :
                    textColor = App.ressourcePack.ui["main menu"]["text"]
                    background = App.ressourcePack.ui["main menu"]["background"]
                    pyxel.cls(background)
                    pyxel.text(100,70,"Mashbattleship",textColor)
                    pyxel.text(118,135,"press",textColor)
                    pyxel.blt(104,150, 2, 0, 32, 48, 16, 0)
                    pyxel.text(112, 170, 'to start', textColor)

                    pyxel.text(128-44,200,"press     for tutorial",textColor)
                    pyxel.blt(128-44+22, 195, 2, 48, 32, 16, 16, 0, scale=0.8)



            case 1:
                #graphismes jeu principal
                if self.arrived_game > 0:
                    pyxel.cls(App.ressourcePack.ui["game counter"]["background"])
                    textColor = App.ressourcePack.ui["game counter"]["text"]
                    if self.arrived_game > 40 :
                        pyxel.text(128,128,"3",textColor)
                    elif self.arrived_game > 20 :
                        pyxel.text(128,128,"2",textColor)
                    else : pyxel.text(128,128,"1",textColor)

                else:
                    pyxel.cls(13)

                    #--------UI joueur 1-----------
                    player = self.players[0]
                    background = App.ressourcePack.players[str(player.color)]["stat window"]["background"]
                    textColor = App.ressourcePack.players[str(player.color)]["stat window"]["text"]
                    hpBarColor = App.ressourcePack.players[str(player.color)]["stat window"]["hp bar"]
                    pyxel.rect(128,0,128,128,background)
                    pyxel.rect(140,115,110,10,0)
                    pyxel.rect(142,117, (106* player.hp_left) / player.hp ,6,hpBarColor)

                    pyxel.text(147,101,str(player.money),textColor)
                    pyxel.blt(140,100,1,0,16,8,8,0)
                    #--------UI joueur 2-----------
                    player = self.players[1]
                    background = App.ressourcePack.players[str(player.color)]["stat window"]["background"]
                    textColor = App.ressourcePack.players[str(player.color)]["stat window"]["text"]
                    hpBarColor = App.ressourcePack.players[str(player.color)]["stat window"]["hp bar"]
                    pyxel.rect(0,128,128,128,background)
                    pyxel.rect(5,133,110,10,0)
                    pyxel.rect(7,135, (106* player.hp_left) / player.hp ,6,hpBarColor)

                    pyxel.text(10,146,str(player.money),textColor)
                    pyxel.blt(3,145,1,0,16,8,8,0)

                    for player in self.players:
                        player.grid.draw()

                    #dessiner les curseurs
                    for player in self.players:
                        player.draw_cursors(1)



            case 2:
                #shop
                background = App.ressourcePack.ui["shop"]["background"]
                onBackgound = App.ressourcePack.ui["shop"]["on background"]
                textColor = App.ressourcePack.ui["shop"]["text"]
                pyxel.cls(background)
                pyxel.text(5,5,"SHOP",textColor)
                pyxel.rect(20,10,210,50,onBackgound)
                pyxel.rect(20,70,210,150,onBackgound)
                self.shopgrid.draw()

            case 3:
                if self.winner:
                    background = App.ressourcePack.players[str(self.winner.color)]["win"]["background"]
                    textColor = App.ressourcePack.players[str(self.winner.color)]["win"]["text"]
                    pyxel.cls(background)
                    text = f'{str(self.winner)} wins'
                    pyxel.text(128-(len(text)*pyxel.FONT_WIDTH)/2,128,text,textColor)
                else:
                    background = App.ressourcePack.ui["game draw"]["background"]
                    textColor = App.ressourcePack.ui["game draw"]["text"]
                    pyxel.cls(13)
                    pyxel.text(122,128,'tie',textColor)

                pyxel.text(70,137,"press spacebar to start again",textColor)
                pyxel.circ(70,100,20,0)
                pyxel.circ(186,100,20,0)

            case 4: # page de choix du pack de texture
                background = App.ressourcePack.ui["ressourcepack menu"]["background"]
                pyxel.cls(background)
                self.ressourcePackGrid.draw()



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


    def __init__(self, app : App, id, grid_offset : tuple[int,int], grid_colors : tuple[int,int], cursor_color : int, color : str, name : str|None = None):
        self.id = id if (id in Player.keys_dict) else 0
        self.color = str(color)
        self.grid = GameGrid(self,grid_offset, *grid_colors)
        self.cursorColor = App.ressourcePack.players[self.color]["cursor color"]
        self.roundpoint = False

        self.name : str = name
        if not name:
            self.name = f'player {self.id}'


        self.opponents : list[Player] = []
        self.opponentsGrid : list[GameGrid] = []
        self.opponentGridCusor : dict[GameGrid, Cursor] = {}
        self.menucursor : Cursor
        self.cooldown = 0
        self.hp = 9
        self.hp_left = 9
        self.set : list[DaddyBoat] = ShopGrid.boatSets['default']
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
                    if self.grid.on_grid(x1,y1):
                        cursor.pos = [x1,y1]
            
            case "shop":
                x1, y1 = self.menucursor.pos[0]+x, self.menucursor.pos[1]+y
                if shopgrid.on_grid(x1,y1):
                    self.menucursor.pos = [x1,y1]

    def shoot(self):
        for cursor in self.opponentGridCusor.values():
            cursor.shoot(self)

    def update_cursors_color(self, color : int|None = None):
        color = color if color else self.cursorColor
        for cursor in self.opponentGridCusor.values():
            cursor.col = color
    
    def draw_cursors(self,gamestate):
        self.cursorColor = App.ressourcePack.players[self.color]["cursor color"]
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


    def draw(self, x, y, *, scale : float|None = None, rotate : float|None = None):
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


class RessourcePack:
    ui : dict[str, dict[str, int]] = {
        "main menu" : {
            "background" : 1,
            "text" : 7
        },
        "tutorial" : {
            "background" : 1,
            "text" : 7
        },
        "ressourcepack menu" : {
            "background" : 1,
            "primary" : 13,
            "text" : 7
        },
        "shop" : {
            "background" : 1,
            "on background" : 5,
            "primary" : 13,
            "text" : 7
        },
        "game counter" : {
            "background" : 13,
            "text" : 7
        },
        "game draw" : {
            "background" : 13,
            "text" : 7
        }
    }

    players : dict[int,dict[str, int|list[int]|dict[str, int]]] = {
        "0" : {
            "cursor color" : 3,
            "grid colors" : [3,11],
            "tutorial color" : 3,
            "win" : {
                "background" : 9,
                "text" : 7
            },
            "stat window" : {
                "background" : 5,
                "text" : 7,
                "hp bar" : 5
            }
        },
        "1" : {
            "cursor color" : 9,
            "grid colors" : [4,9],
            "tutorial color" : 9,
            "win" : {
                "background" : 9,
                "text" : 7
            },
            "stat window" : {
                "background" : 14,
                "text" : 7,
                "hp bar" : 14
            }
        }
    }

    boats : dict[str, dict[tuple[int,int], Sprite]] = {
        "boat1" : {
            (0,0) : {
                'alive' : Sprite(0, 0, 0, 16, 16, colkey=0), 
                'dead' : Sprite(0, 0, 16, 16, 16, colkey=1)
            }
        },
        "boat2x" : {
            (0, 0): {
                "alive": Sprite(0, 16, 0, 16, 16, colkey=0),
                "dead": Sprite(0, 16, 16, 16, 16, colkey=1)
            },
            (1, 0): {
                "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=180),
                "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=180)
            }
        },
        "boat2y" : {
            (0, 0): {
                "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=90),
                "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=90)
            },
            (0, 1): {
                "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=-90),
                "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=-90)
            }
        },
        "boat3x" : {
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
        },
        "boat3y" : {
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
        },
        "boatLtl" : {
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
        },
        "boatLtr" : {
            (0, 0): {
                "alive": Sprite(0, 48, 0, 16, 16, colkey=0, rotate=0),
                "dead": Sprite(0, 48, 16, 16, 16, colkey=1, rotate=0)
            },
            (-1, 0): {
                "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=0),
                "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=0)
            },
            (0, 1): {
                "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=-90),
                "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=-90)
            }
        },
        "boatLbl" : {
            (0, 0): {
                "alive": Sprite(0, 48, 0, 16, 16, colkey=0, rotate=180),
                "dead": Sprite(0, 48, 16, 16, 16, colkey=1, rotate=180)
            },
            (1, 0): {
                "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=180),
                "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=180)
            },
            (0, -1): {
                "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=90),
                "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=90)
            }
        },
        "boatLbr" : {
            (0, 0): {
                "alive": Sprite(0, 48, 0, 16, 16, colkey=0, rotate=90),
                "dead": Sprite(0, 48, 16, 16, 16, colkey=1, rotate=90)
            },
            (-1, 0): {
                "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=0),
                "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=0)
            },
            (0, -1): {
                "alive": Sprite(0, 16, 0, 16, 16, colkey=0, rotate=90),
                "dead": Sprite(0, 16, 16, 16, 16, colkey=1, rotate=90)
            }
        }
    }

    keys : dict[str, Sprite] = {
        pyxel.KEY_UP : Sprite(2, 0,0,16,16,colkey=0),
        pyxel.KEY_DOWN : Sprite(2, 16,0,16,16,colkey=0),
        pyxel.KEY_LEFT : Sprite(2, 32,0,16,16,colkey=0),
        pyxel.KEY_RIGHT : Sprite(2, 48,0,16,16,colkey=0),
        pyxel.KEY_M : Sprite(2, 64,0,16,16,colkey=0),
        pyxel.KEY_Z : Sprite(2, 0,16,16,16,colkey=0),
        pyxel.KEY_S : Sprite(2, 16,16,16,16,colkey=0),
        pyxel.KEY_Q : Sprite(2, 32,16,16,16,colkey=0),
        pyxel.KEY_D : Sprite(2, 48,16,16,16,colkey=0),
        pyxel.KEY_V : Sprite(2, 64,16,16,16,colkey=0)
    }
    
    sets : dict[str, Sprite] = {
        "default" : Sprite(0, 0, 64, 32, 32, 10),
        "one" : Sprite(0,32,64, 32,32, 10),
        "all" : Sprite(0,64,64, 32,32, 10)
    }
    
    def __init__(self):
        """n'est valide que pour les bateaux pour l'instant"""
        pyxel.load('assets/battleShip.pyxres')
        RessourcePack.colorPalette = pyxel.colors.to_list()
    
    def get_available_ressourcepack(self) -> list[str]:
        undisponible_packs = ['default', 'theme sombre']
        return ['default'] + [directory for directory in os.listdir('assets') if (directory not in undisponible_packs) and (os.path.isdir(f'assets/{directory}') and 'ressources.json' in os.listdir(f'assets/{directory}'))]
    
    def change_ressourcepack(self, ressourcepack_name : str) -> None:
        if not ressourcepack_name in self.get_available_ressourcepack():
            return
        
        if ressourcepack_name == 'default':
            pyxel.load('assets/battleShip.pyxres')
            self.boats = RessourcePack.boats
            self.keys = RessourcePack.keys
            self.sets = RessourcePack.sets
            self.ui = RessourcePack.ui
            self.players = RessourcePack.players
            return
        
        pyxel.load(f'assets/{ressourcepack_name}/ressources.pyxres')
        with open(os.sep.join(['assets',ressourcepack_name,'ressources.json'])) as file:
            file : dict[str, dict[str, int|str|dict[str, dict[str, dict[str, int]]]]]= json.load(file)

        self.boats = {}
        if 'boats' in file:
            for key, value in file['boats'].items():
                self.boats[key] = {}
                for coord, state in value.items():
                    coord = ast.literal_eval(coord)
                    self.boats[key][coord] = {}
                    for name, texture in state.items():
                        self.boats[key][coord][name] = Sprite(**texture) if any(kwarg in texture for kwarg in ['img', 'u', 'v', 'w', 'h']) else None

        if 'ui' in file:
            self.ui = file['ui']

        if "players" in file:
            self.players = file["players"]

        if "keys" in file:
            for key, value in file.items():
                if not hasattr(pyxel, key):
                    continue
                key = getattr(pyxel, key)
                if not key in RessourcePack.sets:
                    continue
                self.keys[key] = Sprite(**value)

        if "sets" in file:
            self.sets = {}
            for key in RessourcePack.sets.keys():
                if key in file["sets"]:
                    self.sets[key] = Sprite(**file["sets"][key])
                else:
                    self.sets[key] = Sprite(0, 0, 0, 16, 16)


class Grid:
    def __init__(self, offset : tuple[int,int],
                    size : tuple[int,int],
                    tile_size : tuple[int,int],
                    *color : int,
                    gap : None|tuple[int,int] = None,
                    special_tile_size : None|dict[str, dict[int, int]] = None):
        """
        
        """
        self.coord : tuple[int,int] = offset
        self.offsetx = offset[0]
        self.offsety = offset[1]
        self.width : int
        self.height : int
        self.width, self.height = size

        self.tileSize : tuple[int, int] = tile_size
        self.colors : list[int] = list(color) if color else [0]
        self.gap : int = gap if gap else (0,0)
        self.specialTileSize : dict[str, dict[int, int]] = {
            "x" : special_tile_size["x"] if "x" in special_tile_size else {},
            "y" : special_tile_size["y"] if "y" in special_tile_size else {}
        } if special_tile_size else {"x" : {}, "y" : {}}

    def draw(self):
        x, y = self.coord
        maxindex = len(self.colors)
        pw, ph = 0,0
        for i in range(self.width):
            w = self.tileSize[0] if i not in self.specialTileSize['x'] else self.specialTileSize['x'][i]
            for j in range(self.height):
                h = self.tileSize[1] if j not in self.specialTileSize['y'] else self.specialTileSize['y'][j]
                pyxel.rect(x, y, w, h, self.colors[(i+j)%maxindex])
                y+=h+self.gap[1]
            y = self.coord[1]
            x+=w+self.gap[0]

    def on_grid(self, x,y):
        return 0 <= x < self.width and 0 <= y < self.height

    def select(self, x,y):
        if not self.on_grid(x,y):
            raise IndexError


class RessourcePackGrid(Grid):
    def __init__(self, player : Player):
        self.player = player
        self.ressourcePacks = App.ressourcePack.get_available_ressourcepack()
        super().__init__((16,16), (1,len(self.ressourcePacks)), (224,32), 13, gap=(8, 8))
        self.cursor = Cursor(player, self)

    def draw(self):
        super().draw()
        self.colors = [App.ressourcePack.ui["ressourcepack menu"]["primary"]]
        textColor = App.ressourcePack.ui["ressourcepack menu"]["text"]
        for i in range(len(self.ressourcePacks)):
            x = 20
            y = 20+(self.tileSize[1]+self.gap[1])*i
            pyxel.text(x,y, self.ressourcePacks[i], textColor)
        self.cursor.draw()

    def update(self):
        if pyxel.btnp(self.player.keys_dict[self.player.id]["key up"]):
            self.cursor.move(0, -1)
        if pyxel.btnp(self.player.keys_dict[self.player.id]["key down"]):
            self.cursor.move(0, 1)
        if pyxel.btnp(self.player.keys_dict[self.player.id]["key left"]):
            self.cursor.move(-1, 0)
        if pyxel.btnp(self.player.keys_dict[self.player.id]["key right"]):
            self.cursor.move(1, 0)

        if pyxel.btnp(self.player.keys_dict[self.player.id]["key shoot"]):
            App.ressourcePack.change_ressourcepack(self.ressourcePacks[self.cursor.pos[1]])




class DaddyBoat:
    name : str = "DaddyBoat" #nom du bateau (utile pour les textures)
    relativeCoordinates : list[tuple[int,int]] = [] # liste des coordonnées relative du batteau
    
    def __init__(self, grid : "GameGrid", coord : tuple[int,int], *, is_fake : bool = False):
        self.grid = grid
        self.size = grid.tileSize[0]
        self.coordinates : dict[tuple[int,int], dict[str, bool|dict[str, Sprite]]] = {} #{coordonnées : alive? , {'alive' (et/ou 'dead') : {kwargs pour l'image ('u','v','w' et 'h' sont obligatoire sinon la texture ne seras pas rendue)}}}}
        for x,y in self.relativeCoordinates:
            self.coordinates[(coord[0]+x,coord[1]+y)] = {'alive' : True, 'is_trap' : False, 'sprites' : App.ressourcePack.boats[self.name][(x,y)] if (self.name in App.ressourcePack.boats and (x,y) in App.ressourcePack.boats[self.name]) else {}}

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
    name = "boat1"
    relativeCoordinates = [
        (0,0)
    ]

class Boat2x(DaddyBoat):
    name = "boat2x"
    relativeCoordinates = [
        (0, 0),
        (1, 0)
    ]

class Boat2y(DaddyBoat):
    name = "boat2y"
    relativeCoordinates = [
        (0, 0),
        (0, 1)
    ]

class Boat3x(DaddyBoat):
    name = "boat3x"
    relativeCoordinates = [
        (0, 0),
        (1, 0),
        (2, 0)
    ]

class Boat3y(DaddyBoat):
    name = "boat3y"
    relativeCoordinates = [
        (0, 0),
        (0, 1),
        (0, 2)
    ]

class BoatLtl(DaddyBoat):
    name = "boatLtl"
    relativeCoordinates = [
        (0, 0),
        (1, 0),
        (0, 1)
    ]

class BoatLtr(DaddyBoat):
    name = "boatLtr"
    relativeCoordinates = [
        (0, 0),
        (-1, 0),
        (0, 1)
    ]

class BoatLbl(DaddyBoat):
    name = "boatLbl"
    relativeCoordinates = [
        (0, 0),
        (1, 0),
        (0, -1)
    ]

class BoatLbr(DaddyBoat):
    name = "boatLbr"
    relativeCoordinates = [
        (0, 0),
        (-1, 0),
        (0, -1)
    ]




class Cursor :
    def __init__(self, player : Player, grid : Grid, position = [0,0]):
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

    def draw(self):
        x = self.grid.coord[0]+(self.grid.tileSize[0]+self.grid.gap[0])*self.pos[0]
        y = self.grid.coord[1]+(self.grid.tileSize[1]+self.grid.gap[1])*self.pos[1]
        w = self.grid.tileSize[0] if self.pos[0] not in self.grid.specialTileSize["x"] else self.grid.specialTileSize["x"][self.pos[0]]
        h = self.grid.tileSize[1] if self.pos[1] not in self.grid.specialTileSize["y"] else self.grid.specialTileSize["y"][self.pos[1]]

        pyxel.rectb(x,y,w,h,self.player.cursorColor)
        pyxel.rectb(x-1, y-1, w+2, h+2, self.player.cursorColor)

    def shoot(self, attacker : Player|None = None) -> bool:
        if self.grid.shoot_boat((self.pos[0], self.pos[1])):
            self.grid.player.hp_left -= 1
            if attacker:
                attacker.cooldown = self.player.frames_between_shoot[0]
                attacker.money += 1
        else:
            if attacker:
                attacker.cooldown = self.player.frames_between_shoot[1]
    
    def select(self):
        self.grid.select(*self.pos)

    def move(self, x,y):
        x += self.pos[0]
        y += self.pos[1]
        if self.grid.on_grid(x,y):
            self.pos = [x,y]


class GameGrid(Grid):
    def __init__(self, player, coord, *color):
        super().__init__(coord, (8,8), (16,16), *color)
        self.player : Player = player
        self.colors = App.ressourcePack.players[self.player.color]["grid colors"]
        self.boats : list[DaddyBoat] = []
        self.coordinatesBoat : dict[tuple[int,int], DaddyBoat] # coordonnées ou sont les bateaux suivit du bateau a ces coordonnées
        self.explosions : SpriteGroup = SpriteGroup()

    def shoot_boat(self, coord : tuple[int,int]):
        # retour demande au bateau si il a été touché si il est sur cette case sinon retourne False
        if coord in self.coordinatesBoat:
            self.explosions.add_sprite(Explosion((self.offsetx+coord[0]*self.tileSize[0], self.offsety+coord[1]*self.tileSize[1]), False))
            return self.coordinatesBoat[coord].get_shot(coord)
        
        self.explosions.add_sprite(Explosion((self.offsetx+coord[0]*self.tileSize[0], self.offsety+coord[1]*self.tileSize[1])))
        return False
    
    def draw(self):
        self.colors = App.ressourcePack.players[self.player.color]["grid colors"]
        super().draw()
        for boat in self.boats:
            boat.draw()
        for explosion in self.explosions.get_sprites():
            explosion.draw()

    def generate_boat(self, boats_list : list[DaddyBoat]):
        self.player.hp_left = self.player.hp
        # reinitalise la grille
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
                    if coord in coords or not (self.on_grid(*coord)):
                        ok = False
                        break
                # ajoute le bateau si les conditions précédantes sont respectées
                if ok:
                    coords += temp.get_coordinates()
                    self.boats.append(temp)
                stop -= 1
            else:
                if not ok: # retire la vie correcsondant au bateau si celui-ci n'est pas placé
                    if boat in [Boat1]:
                        n = 1
                    elif boat in [Boat2x,Boat2y]:
                        n = 2
                    elif boat in [Boat3x,Boat3y,BoatLtl,BoatLtr,BoatLbr,BoatLbl]:
                        n = 3
                    self.player.hp_left -= n
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




class Upgrade:
    price : int = 0
    description : str = "aucune description"
    def buy(self, player : Player) -> bool:
        """ajoute l'amelioration au joueur
        
        return:
            True si l'amelioration est achetée
            False si l'achat échoue
        """
        if player.money < self.price:
            return False
        player.money -= self.price
        return True

    def render(self, x, y, textColor : int):
        """rendu dans le shop"""

    def activate(self, player : Player):
        """
        active son action

            player : joueur qui subit les effets
        """


class Upgrade1Hitpoint(Upgrade):
    price = 15
    description = "augmente de 1 les HPs du joueur"
    def buy(self, player : Player):
        if not super().buy(player):
            return False
        
        player.hp += 1
        return True

    def render(self, x, y, textColor : int):
        pyxel.text(x+4, y+4, f"prix : {self.price}", textColor)
        pyxel.text(x+4, y+12, '+1 HITPOINT', textColor)

class Upgrade3Hitpoint(Upgrade):
    price = 40
    description = "augmente de 3 les HPs du joueur"
    def buy(self, player : Player):
        if not super().buy(player):
            return False
        
        player.hp += 3
        return True

    def render(self, x, y, textColor : int):
        pyxel.text(x+4, y+4, f"prix : {self.price}", textColor)
        pyxel.text(x+4, y+12, '+3 HITPOINT', textColor)

class UpgradeReloadtime(Upgrade):
    price = 17
    description = "diminue le temps avant de pouvoir tirer a nouveau"
    def buy(self, player):
        if not super().buy(player):
            return False
        
        player.frames_between_shoot[0] -= 1 if player.frames_between_shoot[0] > 0 else 0
        player.frames_between_shoot[1] -= 1 if player.frames_between_shoot[1] > 0 else 0
        return True

    def render(self, x, y, textColor : int):
        pyxel.text(x+4, y+4, f"prix : {self.price}", textColor)
        pyxel.text(x+4, y+12, "- RELOAD TIME", textColor)

class UpgradeMoneyAtEnd3(Upgrade):
    price = 9
    description = "monaie gagnee en fin de manche"
    def buy(self, player):
        if not super().buy(player):
            return False
        
        player.bonus_money += 3
        return True

    def render(self, x, y, textColor : int):
        pyxel.text(x+4, y+4, f"prix : {self.price}", textColor)
        pyxel.text(x+4, y+12, "+3 MONEY @ END", textColor)


class ShopGrid(Grid):
    boatSets : dict[str, list[DaddyBoat]] = { # nom du set (utile pour generer la texture du set dans le shop) : set(liste des classes de bateau)
        "default" : [Boat1,Boat3x,Boat2x,BoatLtl],
        "one" : [Boat1],
        "all" : [Boat1,Boat2x,Boat3x,Boat2y,Boat3y,BoatLbl,BoatLtl,BoatLbr,BoatLtr]
    }
    upgrades : list[Upgrade] = [
        Upgrade1Hitpoint(),
        Upgrade3Hitpoint(),
        UpgradeReloadtime(),
        UpgradeMoneyAtEnd3()
    ]

    def __init__(self, player : Player):
        super().__init__((27, 15), (4,2), (45, 43), App.ressourcePack.ui["shop"]["primary"], gap=(5,22), special_tile_size={"y" : {1 : 130}})
        self.__player = player
        self.cursor = Cursor(player, self)
        self.setsInShop : list[list[DaddyBoat]] = []
        self.upgradesInShop : list[Upgrade] = []
        self.generate_shop()

    @property
    def player(self):
        return self.__player
    
    @player.setter
    def player(self, player : Player):
        self.__player = player
        self.cursor = Cursor(self.player, self)

    def generate_shop(self):
        self.setsInShop = random.choices(list(self.boatSets.keys()), k=4)
        self.upgradesInShop = random.choices(self.upgrades, k=4)

    def draw(self):
        self.colors = [App.ressourcePack.ui["shop"]["primary"]]
        super().draw()
        textColor = App.ressourcePack.ui["shop"]["text"]
        pyxel.text(self.coord[0], self.coord[1]-8, str(self.player.money), textColor)

        self.cursor.draw()

        for i in range(4):
            x = self.coord[0]+(self.tileSize[0]+self.gap[0])*i
            y = self.coord[1]+self.tileSize[1]+self.gap[1]
            self.upgradesInShop[i].render(x, y, App.ressourcePack.ui["shop"]["text"])

        for i in range(4):
            x = self.coord[0]+(self.tileSize[0]+self.gap[0])*i
            y = self.coord[1]
            pyxel.text(x+4 ,y+4, self.setsInShop[i], textColor)
            App.ressourcePack.sets[self.setsInShop[i]].draw(x+4,y+10)

    def update(self):
        if pyxel.btnp(self.player.keys_dict[self.player.id]["key up"]):
            self.cursor.move(0, -1)
        if pyxel.btnp(self.player.keys_dict[self.player.id]["key down"]):
            self.cursor.move(0, 1)
        if pyxel.btnp(self.player.keys_dict[self.player.id]["key left"]):
            self.cursor.move(-1, 0)
        if pyxel.btnp(self.player.keys_dict[self.player.id]["key right"]):
            self.cursor.move(1, 0)

        if pyxel.btnp(self.player.keys_dict[self.player.id]["key shoot"]):
            match self.cursor.pos[1]:
                case 0:
                    self.player.set = self.boatSets[self.setsInShop[self.cursor.pos[0]]]
                case 1:
                    self.upgradesInShop[self.cursor.pos[0]].buy(self.player)



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
        """doit etre placé dans un groupe de sprite"""
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