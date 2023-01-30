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


# Jeu aléatoire pour simuler les parties
def SimulationPartie(G : Game):
    while(True):
        # on récupère la liste des déplacements possibles
        L = GetPossibleMoves(G)
        if (L == []):
            # retourne le nombre de cases parcourues
            return G.Score
        random_move = GetRandomMove(G)
        # on crée le mur
        G.Grille[G.PlayerX,G.PlayerY] = 2
        # on assigne la prochaine case au joueur
        G.PlayerX += random_move[0]
        G.PlayerY += random_move[1]
        G.Score += 1

# algorithme de Monte-Carlo
def MonteCarlo(G : Game, nbrParties):
    # on initialise le total 
    total = 0
    # on fait le nombre de parties demandées par nbrParties
    for i in range(0,nbrParties):
        # on crée une copie du jeu
        GameCopy = G.copy()
        # on simule une partie
        total += SimulationPartie(GameCopy)
    # on retourne le total de la partie
    return total

# détermine le coup à jouer pour la partie courante à l'aide des fonctions précédentes
def GetBestMove(G : Game, nbrParties):
    # on récupère la liste des déplacements possibles
    L = GetPossibleMoves(G)
    # sans direction, on lui assigne une aléatoire
    if len(L) == 0:
        return GetRandomMove(G)
    # on détermine le potentiel des déplacements possibles
    L2 = []
    for move in L:
        # on simule une partie
        L2.append(MonteCarlo(G, nbrParties))
    print(L2)
    # on retourne le meilleur déplacement
    return L[L2.index(max(L2))]

def Play(G : Game):   
    
    x,y = G.PlayerX, G.PlayerY

    G.Grille[x,y] = 2  # laisse la trace de la moto

    # on récupère le meilleur coup possible
    bestMove = GetBestMove(G,100)
    # on effectue le déplacement
    x += bestMove[0]
    y += bestMove[1]

    v = G.Grille[x,y]
    
    if v > 0 :
        # collision détectée
        return True # partie terminée
    else :
       G.PlayerX = x  # valide le déplacement
       G.PlayerY = y  # valide le déplacement
       G.Score += 1
       return False   # la partie continue
     

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
      

    
        

      
 

