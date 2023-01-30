import tkinter as tk
import random
import numpy as np
import copy 

#################################################################################
#
#   Données de partie
dx = np.array([0, -1, 0, 1, 0], dtype=np.int32)
dy = np.array([0, 0, 1, 0, -1], dtype=np.int32)

# scores associés à chaque déplacement
ds = np.array([0, 1, 1, 1, 1], dtype=np.int32)


Data = [   [1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1] ]

GInit  = np.array(Data,dtype=np.int8)
GInit  = np.flip(GInit,0).transpose()

LARGEUR = 13
HAUTEUR = 17

# container pour passer efficacement toutes les données de la partie

class Game:
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.Score   = Score
        self.Grille  = Grille
    
    def copy(self): 
        return copy.deepcopy(self)

# initialisation de la partie
GameInit = Game(GInit,3,5)

##############################################################
#
#   création de la fenetre principale  - NE PAS TOUCHER

L = 20  # largeur d'une case du jeu en pixel    
largeurPix = LARGEUR * L
hauteurPix = HAUTEUR * L


Window = tk.Tk()
Window.geometry(str(largeurPix)+"x"+str(hauteurPix))   # taille de la fenetre
Window.title("TRON")


# création de la frame principale stockant toutes les pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
Frame0 = CreerUnePage(0)

canvas = tk.Canvas(Frame0,width = largeurPix, height = hauteurPix, bg ="black" )
canvas.place(x=0,y=0)

#   Dessine la grille de jeu - ne pas toucher

def Affiche(Game):
    canvas.delete("all")
    H = canvas.winfo_height()
    
    def DrawCase(x,y,coul):
        x *= L
        y *= L
        canvas.create_rectangle(x,H-y,x+L,H-y-L,fill=coul)
    
    # dessin des murs 
   
    for x in range (LARGEUR):
       for y in range (HAUTEUR):
           if Game.Grille[x,y] == 1  : DrawCase(x,y,"gray" )
           if Game.Grille[x,y] == 2  : DrawCase(x,y,"cyan" )

    # dessin de la moto
    DrawCase(Game.PlayerX,Game.PlayerY,"red" )

def AfficheScore(Game):
   info = "SCORE : " + str(Game.Score)
   canvas.create_text(80, 13,   font='Helvetica 12 bold', fill="yellow", text=info)


###########################################################
#
# gestion du joueur IA

# VOTRE CODE ICI 

# Retourne la liste des déplacements possibles du joueur
def GetPossibleMoves(Game):
    # liste des déplacements possibles
    L = []
    # coordonnées courantes du joueur
    x,y = Game.PlayerX, Game.PlayerY
    # droite
    if (Game.Grille[x+1][y] == 0):
        L.append((1,0))
    # gauche
    if (Game.Grille[x-1][y] == 0):
        L.append((-1,0))
    # haut
    if (Game.Grille[x][y+1] == 0):
        L.append((0,1))
    # bas
    if (Game.Grille[x][y-1] == 0):
        L.append((0,-1))
    return L

# retourne un déplacement aléatoire parmi ceux possibles
def GetRandomMove(Game):
    L = GetPossibleMoves(Game)
    if L == []:
        L = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    return L[random.randrange(len(L))]

repeat = 10000

# Jeu aléatoire pour simuler les parties
def SimulationPartie(Game):
    
    # on copie les données de départ afin de créer plusieurs parties
    G = np.tile(Game.Grille,(repeat,1,1))
    X = np.tile(Game.PlayerX, repeat)
    Y = np.tile(Game.PlayerY, repeat)
    S = np.tile(Game.Score, repeat)
    I = np.arange(repeat) 
    
    loop = True
    while(loop):
        # créé le mur
        G[I, X, Y] = 2
        
        # initialisation des directions possibles, 
        # avec une taille pour chacun des vecteurs associés
        L = np.zeros((repeat,4), dtype = np.int32)
        sizes = np.zeros(repeat, dtype = np.int32)
        
        # Liste les directions
        
        # Gauche
        Left = (G[I, X-1,Y] == 0) *1
        L[I, sizes] = Left 
        sizes += Left
        
        # Haut
        Up = (G[I,X,Y+1] == 0) *1
        L[I,sizes] = Up*2
        sizes += Up
        
        # Droite
        Right = (G[I,X+1,Y] == 0)*1
        L[I,sizes] = Right*3
        sizes =+ Right
        
        # Down
        Down = (G[I, X, Y - 1] == 0)*1
        L[I,sizes] = Down * 4
        sizes += Down
        
        # on passe les tailles à 0 à 1 afin de ne pas bouger
        sizes[sizes == 0] = 1
        
        # On récupère une direction aléatoire parmi celles disponibles
        r_dir = np.random.randint(sizes)
        
        Choix = L[I,r_dir]
        
        
        # DEPLACEMENT
        DX = dx[Choix]
        DY = dy[Choix]
        DS = ds[Choix]
        
        # end game
        loop = not(np.sum(DS) == 0)
        X += DX
        Y += DY
        S += DS
        
    return np.sum(S)

def Action(Game,Direction):
    x, y = Game.PlayerX, Game.PlayerY

    Game.Grille[x, y] = 2

    x += Direction[0]
    y += Direction[1]

    if Game.Grille[x, y] > 0:
        return True
    else:
        Game.PlayerX = x
        Game.PlayerY = y
        Game.Score += 1
        return False

# algorithme de Monte-Carlo
def MonteCarlo(Game, Direction):
    # on crée une copie du jeu
    GameCopy = Game.copy()
    # on joue la partie
    Action(GameCopy, Direction)
    # on retourne le total de la partie
    return SimulationPartie(GameCopy)

def Play(Game):   
    L = GetPossibleMoves(Game)
    average = []
    # position aléatoire si absence dde direction
    if L == []:
        return(1,1)
    
    for dir in L:
        average.append(MonteCarlo(Game, dir))
    dir = L[average.index(max(average))]
    
    return Action(Game,dir)
     

################################################################################
     
CurrentGame = GameInit.copy()
 

def Partie():

    PartieTermine = Play(CurrentGame)
    
    if not PartieTermine :
        Affiche(CurrentGame)
        # rappelle la fonction Partie() dans 30ms
        # entre temps laisse l'OS réafficher l'interface
        Window.after(100,Partie) 
    else :
        AfficheScore(CurrentGame)


#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Window.after(100,Partie)
Window.mainloop()
      

    
        

      
 

