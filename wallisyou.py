HAUT = 0
DROITE = 1
BAS = 2
GAUCHE = 3 

def connecte(donjon, position1, position2):
    '''
    fonction qui regarde si les position de position2 sont connecte à ceux du position1
    paramètre :
        donjon
        un tuple position1
        un tuple position2
    retournes :
        True si position2 est adjacent est connecte avec position1
        que les positions sont les mêmes si position1 et position2 sont similaire
        que les positions ne sont pas adjacentes si position1 n'est pas adjacents a position2
    '''
    #variable ligne et colonne qui prend les valeurs des positions
    ligne1,colonne1 = position1
    ligne2,colonne2 = position2
    
    #Vérifie si les deux positions sont dans donjon
    if (ligne1 < 0 or ligne1 >= len(donjon)) or (colonne1 < 0 or colonne1 >= len(donjon[0])):
        return "La position 1 est hors de la grille"
    if (ligne2 < 0 or ligne2 >= len(donjon)) or (colonne2 < 0 or colonne2 >= len(donjon[0])):
        return "La position 2 est hors de la grille"
    #porte qui prend comme valeurs les tuples dans les listes de listes de donjon
    porte1 = donjon[ligne1][colonne1]
    porte2 = donjon[ligne2][colonne2]
    
     
    #regarde si les positions sont adjacents ou sont similaire 
    if  ligne1 == ligne2 and colonne1 == colonne2 :
        return "les positions sont les même"
    if  ligne1 != ligne2 and colonne1 != colonne2 :
       return "les positions ne sont pas adjacents" 
    if ligne1 < ligne2 - 1 or colonne1 < colonne2 - 1 or ligne1 > ligne2 + 1 or colonne1 > colonne2 + 1:
        return "les postions ne sont pas adjacents"
    #regarde si les positions sont connéctées ou pas
       
    if ligne1 < ligne2 and (porte1[BAS] == True and porte2[HAUT] == True)   :
            return True
    if ligne1 > ligne2 and (porte1[HAUT] == True and porte2[BAS] == True) :
            return True
    if colonne1 < colonne2 and (porte1[DROITE] == True and porte2[GAUCHE] == True) :
            return True
    if colonne1 > colonne2 and (porte1[GAUCHE] == True and porte2[DROITE] == True) :
            return True
        
    return False



def pivot(donjon,position):
    '''
    fonction qui pivote à 90 degrès dans le sens horraire une salle de position en position dans le donjon
    
    paramètre :
        le donjon choisit
        une position d'une salle dans le donjon
    return rien
    '''
    (ligne,colonne) = position
    (haut,droite,bas,gauche) = donjon[ligne][colonne]
    #pivote une case du donjon dans le sens horraire
    donjon[ligne][colonne] = (gauche,haut,droite,bas)
    


#fonction pour créer une liste avec au moins 4 positions possible
def position_dans_donjon(donjon,position):
    '''
    fonction qui créer une liste avec tout les positions adjacents à position du paramètre
    
    paramètre:
        le donjon choisit
    return lst une liste avec des positions
    '''
    lst = []
    ligne,colonne = position
    #ajoute dans lst les position qui sont adjacents au position en parametre et qui sont inclu dans donjon
    if ligne > 0:
        lst.append((ligne - 1 ,colonne))
    if colonne < len(donjon[0])-1 :
        lst.append((ligne,colonne + 1))
    if ligne < len(donjon) - 1 :
        lst.append((ligne + 1,colonne))
    if colonne > 0 :
        lst.append((ligne,colonne - 1))
    return lst



def chemin_dragon_max(chemin):
    '''
    fonction qui regarde le chemin à parcourir pour atteindre le dragon avec le niveau le plus haut
    
    paramètre:
        le chemin qui est constitué de position
    retourne :
        un tuple avec le chemiin vers le dragons avec le plus haut niveau et son niveau
    '''
    niveau_max = -1
    chemin_niveau_max = None
    for elem in chemin :
        #regarde si niveau est superieur à niveau max 
        route,niveau = elem
        if niveau > niveau_max:
            chemin_niveau_max = route
            niveau_max = niveau
    return (chemin_niveau_max,niveau_max)
            
 
 
def intention(donjon, position, dragons, visite):
    '''
    fonction récurcive qui permet de créer un chemin vers le dragons avec le plus haut niveau et si le chemin n'existe pas
    il créer un chemin vers le 2eme dragon avec le plus haut niveau et rajoute les positions déjà visitées dans un ensemble vide
    
    paramètre:
        le donjon choisit
        la position de l'aventurier
        les dragons
        l'ensemble vide visite
    return:
        si le dragons et l'aventurier sont au même endroit il renvoie la position et le nveau du dragon
        si la position est dans l'ensemble visite il retourne None
        si les positions sont connécte avec celui de l'aventurier il retourne le chemin vers le dragons avec son niveau
    '''
    # Vérifier si la position correspond à un dragon
    for dragon_numero_x in dragons:
        if position == dragon_numero_x['position']:
            niveau = dragon_numero_x['niveau']
            return ([position], niveau)

    # Vérifier si la position a déjà été visitée
    if position in visite:
        return None
    else:
        visite.add(position)

    # Liste des positions adjacentes valides
    position_collé = position_dans_donjon(donjon, position)

    chemins_1 = []
    for cible in position_collé:
        if connecte(donjon, position, cible):
            route = intention(donjon, cible, dragons, visite)
            if route is not None:
                chemins_1.append(route)
                
    if chemins_1 == []:
        return None

    chemin_plus_haut_niveau = chemin_dragon_max(chemins_1)
    return ([position] + chemin_plus_haut_niveau[0], chemin_plus_haut_niveau[1])

   

def rencontre(aventurier, dragons):
    '''
    fonction qui traite la recontre de l'aventurier et des dragons
    en comparant leurs niveau pour voir si l'aventurier meurt ou pas
    
    paramètre :
        l'aventurier
        les dragons
    return rien
    '''
    for dragon_numero_x in dragons :
    #compare les positions du dragon avec celle de l'aventurier 
        if aventurier['position'] == dragon_numero_x['position'] :
            #compare les niveaus de l'aventurier et du dragon
            if dragon_numero_x['niveau'] <= aventurier['niveau'] :
                aventurier['niveau'] += 1
                dragons.remove(dragon_numero_x)
                                        
            else :
                #si l'aventurier est trop bas niveau l'aventurier est mort 
                aventurier['statut'] = 'mort'
        


def appliquer_chemin(aventurier, dragons, chemin) :
    '''
    fonction qui applique le chemin donné par intention et dés que l'aventurier à rejoint un dragon
    il effectue la fonction recontre pour voir si l'aventurier restera vie ou pas
    
    paramètre :
        l'aventurier
        les dragons
        le chemin donné par intention
    return rien
    '''
    for cases in chemin[0] :
    #la position de l'aventurier evolue en fonction de case
       aventurier['position'] = cases
       
    for drake in dragons :
       if cases == drake['position'] :
           #on compare les caractérisitique de l'aventurier avec ceux du dragons 
            rencontre(aventurier, dragons)   
        

        
def fin_partie(aventurier, dragons) :
    '''
    fonction qui regarde dés que la partie se finit c'est à dire que si il n'y a plus de dragons
    ou  bien que l'aventurier est mort pour traiter la fin de la partie pour voir qui gagne et qui perd
    
    paramètre:
        l'aventurier
        les dragons
    retourne:
        1 si il n'y a plus de dragons sdonc que la partie est gagné par l'aventurier
        -1 si l'aventurier est mort donc que la partie est perdu par l'aventurier
        0 la partie continue
    '''
    #si il n'y a plus de dragon la partie est gagné donc on retourne 1
    if dragons == [] :
        return 1
    #si l'aventurier est mort on retourne -1
    elif aventurier['statut'] == 'mort' :
        return -1
    else :
        return 0
    


from string import punctuation
parasite = punctuation
def charger(nom_du_fichier):
    '''
    fonction qui prend en parametre un fichier et transcrire les données du fichier afin d'en récuperer donjon, aventurier, dragons
    
    paramétre:
       map_x.txt
    
    return:
       donjon,aventurier,dragons
    '''
    
    fichier = open(nom_du_fichier, encoding="utf8")
    ligne_du_fichier = fichier.readlines()
    donnée_donjon = []
    donnée_aventurier = []
    donnée_dragons = []    
    for element in ligne_du_fichier:
        if element[0] == 'A':
            donnée_aventurier.append(element[:-1])
        elif element[0] == 'D':
            donnée_dragons.append(element[:-1])
        else:
            donnée_donjon.append(element[:-1])
    
    fichier_entier_separer = donnée_donjon + donnée_aventurier + donnée_dragons
    for donnée_xxxx in fichier_entier_separer:
        for element in donnée_xxxx:
            if element in parasite:
                break
        
    #Construction de l'aventurier
    aventurier = {}
    (ligne_aventurier, colonne_aventurier) = int(donnée_aventurier[0][2]),int(donnée_aventurier[0][4])
    position_aventurier = (ligne_aventurier, colonne_aventurier)
    aventurier['position'] = position_aventurier
    aventurier['niveau'] = 1
    aventurier['statut'] = 'en vie'
    
    #Construction des dragons
    dragons = []   
    for element in donnée_dragons:
        dragon = {}
        (ligne_dragons, colonne_dragons) = int(element[2]),int(element[4])
        position_dragon = (ligne_dragons, colonne_dragons)
        dragon['position'] = position_dragon
        niveau_dragon = int(element[6])
        dragon['niveau'] = niveau_dragon
        dragons.append(dragon)
        
    #Construction du donjon
    donjon = []
    fichier_tiles = open("tiles.txt", encoding="utf8")
    ligne_du_fichier_tiles = fichier_tiles.readlines()
    tiles = {}
    for element in ligne_du_fichier_tiles:
        if 'droits' in element:
            tiles[element[10]] = (False,True,False,True)
            tiles[element[12]] = (True,False,True,False)
        if 'angles' in element:
            tiles[element[10]] = (False,True,True,False)
            tiles[element[12]] = (False,False,True,True)
            tiles[element[14]] = (True,True,False,False)
            tiles[element[16]] = (True,False,False,True)
        if 'triples' in element:
            tiles[element[10]] = (True,True,True,False)
            tiles[element[12]] = (True,False,True,True)
            tiles[element[14]] = (False,True,True,True)
            tiles[element[16]] = (True,True,False,True)
        if 'bouts' in element:
            tiles[element[10]] = (True,False,False,False)
            tiles[element[12]] = (False,False,False,True)
            tiles[element[14]] = (False,False,True,False)
            tiles[element[16]] = (False,True,False,False)
        if 'quatre' in element:
            tiles[element[10]] = (True,True,True,True)
            
    #Separer les salles (qui sont sous forme str)      
    liste_donjon_separer = []  
    for ligne in donnée_donjon:
        lst = []
        for colonne in ligne:
            lst.append(colonne)
        liste_donjon_separer.append(lst)
        
    #Transformer les salles en bool
    i = 0
    while i < len(liste_donjon_separer[0]):
        lst1 = []
        for element_lst in liste_donjon_separer[i]:
                lst1.append(tiles[element_lst])
        donjon.append(lst1)
        i += 1
        
    return (donjon, aventurier, dragons)

'''PARTIE GRAPHIQUE'''

from fltk import*
import time

def choix_donjon(nombre_de_niveau):
    '''
    fonction qui créer des rectangle et un texte avec les different donjon disponible
    
    paramètre :
        le nombre de niveau disponible
    
    return :
        un tuples avec des coordonnées x1,x2 qui correspond aux coordonnées en abcsisse du rectangle
    '''
    rectangle(0,0,x,y,remplissage = "grey")
    espace = 100
    numero_du_niveau = 1 
    x1 = espace
    x2 = x-espace
    y1 = y/nombre_de_niveau
    y2 = y1+30
    #créer le texte sur le haut de la page 
    texte(x1,y1-y1/2,"CHOISIT TON DONJON !",couleur = "black",ancrage= 'w')
    while numero_du_niveau <= nombre_de_niveau :
        #créer les cases avec comme texte donjon i
        num_donjon = "DONJON "+str(numero_du_niveau)
        rectangle(x1,y1,x2,y2,remplissage = "white")
        texte(x2/2+25,y1+15,num_donjon,couleur = "black",ancrage='center')
        y1 += espace
        y2 += espace
        numero_du_niveau += 1
    return (x1,x2,nombre_de_niveau,espace)
 
 
 
def choix_nom_donjon(x1,x2,nombre_de_niveau,espace) :
    '''
    fonction qui créer des zones dans les rectangle pour pouvoir cliquer dessus pour les selectionner
    
    paramètre :
        les cordonnées x1 et x2 qui correspond au fonction choix_donjon
        le nombre de niveau disponible
    
    retourne :
        le nom du fichier qui correspond au donjon qu'on a choisit
    '''
    while True:
        y1 = y/nombre_de_niveau
        y2 = y1+30
        ev= donne_ev()
        tev = type_ev(ev)

        if tev == "ClicGauche" :
            arrondie_x,arrondie_y =abscisse(ev), ordonnee(ev)
            #permet de cliquer sur un des case pour choisir son donjon
            i = 0
            while i <= nombre_de_niveau-1:
                if arrondie_x >= x1 and arrondie_x <= x2 :
                    if arrondie_y >= y1 + espace*i and arrondie_y <= y2 + espace*i:
                        nom = "map"+str(i+1)+".txt"
                        efface_tout()
                        return nom
                i+=1
        mise_a_jour()



def structure_donjon(taille_fenêtre_x ,taille_fenêtre_y) :
    '''
    fonction qui créer la structure de base du donjon celle ci restera intact jusqu'à la fin,
    on créer d'abord les bordure extrême du donjon puis les bordures des salle sur les extremité du donjon
    et enfin les bordures des salles du donjons
    
    parametre :
        les taille de la fenêtre en x et en y
    
    return rien
    '''
    taille = 10
    taile_de_q = 20
    x = taille_fenêtre_x
    y = taille_fenêtre_y
    x_base = x/len(donjon)
    y_base = y/len(donjon[0])
    couleur_donjon = "black"
    
    #dessine l'arrière plan du donjon
    
    
    #dessine les bordure du donjon
    rectangle(0,0,taille,y, remplissage = couleur_donjon)
    rectangle(x,0,x-taille,y,remplissage = couleur_donjon)
    rectangle(0,0,x,taille ,remplissage = couleur_donjon)
    rectangle(0,y-taille,x,y ,remplissage = couleur_donjon)
    
    for i in range(0,len(donjon[0]*2)-1,2) :
        y1 = x_base - x_base/2 +taille + x_base/8
        y2 = x_base - x_base/2 -taille - x_base/8
        x1 = y_base - y_base/2 +taille + y_base/8
        x2 = y_base - y_base/2 -taille - y_base/8
        #dessine bordure sur les extreme des salles
        #verticale
        
        rectangle (i*x_base/2-taille, 0 , i*x_base/2+taille, y/taile_de_q,  remplissage = couleur_donjon)
        rectangle (i*x_base/2-taille, y , i*x_base/2+taille , y-(y/taile_de_q), remplissage = couleur_donjon)
            
        #horizontale
        rectangle(0, i*y_base/2-taille, x/taile_de_q, i*y_base/2 +taille, remplissage = couleur_donjon)
        rectangle(x, i*y_base/2-taille, x-(x/taile_de_q), i*y_base/2 +taille,  remplissage = couleur_donjon)
            
        #coins du donjon    
        for j in range(0,len(donjon[0]*2)-2,2) :
            #ligne verticale
            rectangle(i*x_base/2-taille, y_base/2+x1, i*x_base/2+taille, y_base/2 +x2, remplissage = couleur_donjon)
            #ligne horizontale
            rectangle(x_base/2 + y1, i*y_base/2-taille, x_base/2+y2 , i*y_base/2+taille, remplissage = couleur_donjon)
            x1 += y_base
            x2 += y_base
            y1 += x_base 
            y2 += x_base
 
 
 
def une_case_donjon(position) :
    '''
    fonction qui déssine une seule case du donjons, elle regarde côté par côté le donjon pour voir si elle est fermé
    si oui elle créer alors un rectangle qui montre que c'est fermer
    
    paramètre :
        une position dans le donjon choisit
        
    return rien
    '''
    ligne,colonne = position
    case = donjon[ligne][colonne]
    
    couleur_arriere_plan = 'red'
    hauteur_case = x/len(donjon) 
    largeur_case = y/len(donjon[0]) 
    x1 = colonne * hauteur_case
    x2 = x1 + hauteur_case
    y1 = ligne * largeur_case
    y2 = y1 + largeur_case
    
    taille_separe = 5
    #dessine un rectangle pour fermer la case
    if case[HAUT] == False :
        rectangle(x1 ,y1 ,x2 ,y1+taille_separe ,remplissage = couleur_arriere_plan)
    
    if case[DROITE] == False :
        rectangle(x2-taille_separe ,y1 ,x2 ,y2 ,remplissage = couleur_arriere_plan)
    
    if case[BAS] == False :
        rectangle(x1 ,y2-taille_separe ,x2 ,y2 ,remplissage = couleur_arriere_plan)
    
    if case[GAUCHE] == False :
        rectangle(x1 ,y1 ,x1+taille_separe ,y2 ,remplissage = couleur_arriere_plan)



def case_donjon():
    '''
    une fonction qui utlilise la fonction une_case_donjon et regarde pour tout les cases dans donjons
    si elles sont ouvertes ou pas
    
    parametre :
        rien
    
    return rien
    '''
    
    rectangle(0,0,x,y,remplissage = "grey")
    #regarde pour toute les salle disponible pour voir si il faut fermer la salle ou pas
    for i in range(len(donjon[0])):
        for j in range(len(donjon)):
            une_case_donjon((i,j))
    
   
    
def placer_aventurier(aventurier) :
    '''
    fonction qui place l'aventurier et son niveau à la bonne position dans le donjon
    et l'aventurier aura des couleurs différentes en fonction de son niveau
    
    paramètre :
        l'aventurier pour voir sa position et son niveau

    return rien
    '''
    ligne,colonne = aventurier['position']
    niveau_aventurier = aventurier['niveau']
    hauteur_case = x/len(donjon)
    largeur_case = y/len(donjon[0]) 
    x1 = colonne * hauteur_case + hauteur_case/2
    x2 = x1 + hauteur_case/4
    y1 = ligne * largeur_case + largeur_case/2
    y2 = y1 - largeur_case/3
    #place l'aventurier à la bonne position
    if aventurier['niveau'] == 1:
        image(x1,y1,'Knight_s_niveau1.png',largeur=50, hauteur=100,ancrage='center',tag='im')
        texte(x2,y2,str(niveau_aventurier),couleur = "white",taille=20)
    if aventurier['niveau'] == 2:
        image(x1,y1,'Knight_s_niveau2.png',largeur=50, hauteur=100,ancrage='center',tag='im')
        texte(x2,y2,str(niveau_aventurier),couleur = "black",taille=20)
    if aventurier['niveau'] == 3:
        image(x1,y1,'Knight_s_niveau3.png',largeur=50, hauteur=100,ancrage='center',tag='im')
        texte(x2,y2,str(niveau_aventurier),couleur = "yellow",taille=20)



def placer_dragons(dragons):
    '''
    fonction qui place touts les dragons avec leurs niveaux à la bonne position
    et la dragons comme pour l'aventurier auront des couleurs différentes en fonction de leurs niveaux
        
    paramètre :
        les dragons pour voir leurs positions et leurs niveaux
    
    return rien
    '''
    for dragon_numero_x in dragons :
        dragon_position = dragon_numero_x['position']
        dragon_niveau = dragon_numero_x['niveau']
        
        ligne,colonne = dragon_position
        hauteur_case = x/len(donjon)
        largeur_case = y/len(donjon[0]) 
        x1 = colonne * hauteur_case + hauteur_case/2
        x2 = x1 + hauteur_case/4
        y1 = ligne * largeur_case + largeur_case/2
        y2 = y1 - largeur_case/3
        
        #place les dragons à la bonne position
        image(x1,y1,'Dragon_s.png',largeur=100, hauteur=60,ancrage='center',tag='im')
        texte(x2,y2,str(dragon_niveau),couleur = "white",taille=20)
        
        #place les dragons en fonctions de leurs niveau à la bonne position
        if dragon_niveau == 1 :
            image(x1,y1,'Dragon_s_niveau1.png',largeur=100, hauteur=60,ancrage='center',tag='im')
            
        elif dragon_niveau == 2 :
            image(x1,y1,'Dragon_s_niveau2.png',largeur=100, hauteur=60,ancrage='center',tag='im')
            
        elif dragon_niveau == 3 :    
            image(x1,y1,'Dragon_s_niveau3.png',largeur=100, hauteur=60,ancrage='center',tag='im')
        
        texte(x2,y2,str(dragon_niveau),couleur = "yellow",taille=20)
        
        

def cordoone_salle_vers_POSITION_Y(y_clic) :
    '''
    fonction qui convertit les clique de position ordonnes en position
    
    parametre :
        y_clic le clique gauche de la souris
    
    return rien
    '''
    i = 0
    y_base = y/len(donjon[0])
    y_limite = 0
    #regarde les cordonnées y de chaque salle pour les convertir en position
    while i < len(donjon[0]):
        if y_clic <= y_limite + y_base and y_clic >= y_limite:
            y_pos = i
            return y_pos
        y_limite += y_base
        i+=1 
    


def cordoone_salle_vers_POSITION():
    '''
    fonction qui convertit les positions x et y de notre clic gauche en tuple position dans le donjon
    
    parametre:
        rien
    
    return rien
    '''
    x_pos = -1
    y_pos = -1
    while True :
        ev = attend_clic_gauche()
        x_endroit,y_endroit = ev
        i = 0
        x_base = x/len(donjon[0])
        x_limite = 0
        #regarde les cordonnées de chaque salle pour les convertir en position
        while i < len(donjon[0]):
            if x_endroit <= x_limite + x_base and x_endroit >= x_limite:
                x_pos = i
                y_pos = cordoone_salle_vers_POSITION_Y(y_endroit)
                return (y_pos, x_pos)
            x_limite += x_base
            i+=1
        


def coordonne_chemin(chemin):
    '''
    fonction qui convertit les position de chemin créer par la fonction intention en cordonnées et
    l'ajoute dans une liste vide
    
    paramètre :
        le chemin créer par la donction intention
        
    return :
        la lsite avec les postion convertit en coordonnées
    '''
    liste_position_chemin = []
    for position in chemin[0] :
        x_co = -1
        y_co = -1
        x_position,y_position = position
            
        i = 0
        while i < len(donjon[0]):
            if x_position == i:
                x_co = y+y/len(donjon)/2
            x_co -= y/len(donjon)    
            i+=1
                
        j = 0
        while j < len(donjon[0]):
            if y_position == j:
                y_co = x+x/len(donjon[0])/2
            y_co -= x/len(donjon[0])
            j+=1

        liste_position_chemin.append((y_co,x_co))
        
    return liste_position_chemin



def chemin_fleche(x_coor,y_coor,x_coor_sui,y_coor_sui):
    '''fonction qui créer des recrangles qui représente le chemin posiible pour l'aventurier
    
    paramètre:
        x_coor et y_coor qui sont les cordonnées qui servent pour la création des rectangle
        de même pour x_coor_sui et y_coor_sui
    return rien

    '''
    
    chemin_couleur = 'blue'
    x_base = x/len(donjon)
    y_base = y/len(donjon[0])
    x1 = x_coor*y_base + y_base/2
    y1 = y_coor*x_base + x_base/2

    #Haut
    if x_coor > x_coor_sui and y_coor == y_coor_sui:
        rectangle(y1,x1-y_base,y1,x1, chemin_couleur)    
    #Bas
    if x_coor < x_coor_sui and y_coor == y_coor_sui:
        rectangle(y1,x1+y_base,y1,x1 , chemin_couleur)
    #Droite
    if x_coor == x_coor_sui and y_coor > y_coor_sui:
        rectangle(y1,x1,y1-x_base,x1, chemin_couleur)
    #Gauche
    if x_coor == x_coor_sui and y_coor < y_coor_sui:
        rectangle(y1,x1,y1+x_base,x1, chemin_couleur)


def afficher_chemin(chemin_intention):
    '''fonction qui affiche le chemin créer par intention sous forme de rectangle bleu
    
    paramètre :
        chemin créer par la fonction intention
    
    return rien
    '''
    chemin = chemin_intention[0]
    i = 0
    while i < len(chemin)-1:
        x_coor = chemin[i][0]
        y_coor = chemin[i][1]
        x_coor_sui = chemin[i+1][0]
        y_coor_sui = chemin[i+1][1]
        chemin_fleche(x_coor,y_coor,x_coor_sui,y_coor_sui)
        i += 1



def maj_chemin_aventurier(chemin) :
    '''met à jour toute les 1seconde la postions de l'aventurier grâce à ses cordonnées depuis la fonction coordonne_chemin

    paramètre :
        aventurier_position qui est la position de l'aventurier
        chemin créer par la fonction intention
    
    retourne rien
    '''
    liste_position_chemin = coordonne_chemin(chemin)
    aventurier_skin = None
    if liste_position_chemin != [] :
        images_aventurier = []
        for coordonne in liste_position_chemin :
            x_maj_a,y_maj_a = coordonne
            if aventurier_skin is not None:
                efface(aventurier_skin)
            #met a jour l'image de l'aventurier pour faire une animation des ses mouvement
            if aventurier['niveau'] == 1:
                aventurier_skin = image(x_maj_a, y_maj_a, 'Knight_s_niveau1.png', largeur=100, hauteur=60, ancrage='center', tag='skin aventurier')
                mise_a_jour()
                attente(1)
            if aventurier['niveau'] == 2:
                aventurier_skin = image(x_maj_a, y_maj_a, 'Knight_s_niveau2.png', largeur=100, hauteur=60, ancrage='center', tag='skin aventurier')
                mise_a_jour()
                attente(1)
            if aventurier['niveau'] == 3:
                aventurier_skin = image(x_maj_a, y_maj_a, 'Knight_s_niveau3.png', largeur=100, hauteur=60, ancrage='center', tag='skin aventurier')
                mise_a_jour()
                attente(1)
        

        
def inisialiser_donjon(donjon,aventurier,dragons,x,y):
    '''
    fonction qui affiche la structure initialle du donjon avec les dragons et l'aventurier

    paramètre :
        le donjon
        l'aventurier,les dragons
        la taille de la fenêtre x et y
    return rien
    '''
    #créer la structure de base du donjon
    case_donjon()
    structure_donjon(x,y)
    placer_dragons(dragons)
    placer_aventurier(aventurier)



def fin_partie_graphique(aventurier, dragons) :
    '''fonction qui affiche des rectangle des images et de textes quand on finit la parie
       c'est à dire que soit l'aventurier et mort qu coup on affiche game over
        si tout les dragons on été tué on affiche victoire
    
    paramètre :
        l'aventurier
        les dragons
    return rien
    '''
    end = fin_partie(aventurier,dragons)
    #si on gagne affiche qu'on a gagné
    if end == 1 :
        rectangle(0,0,x,y,remplissage = 'gray')
        image(x/2,y/4,'Knight_s.png',largeur = 400 , hauteur = 500 , tag ='im')
        rectangle(x/2-x/4,y/4-y/8,x/2+x/4,y/4+y/8,remplissage = "green")
        
        rectangle(0,y,x/2,y/2+y/4,remplissage = 'blue')
        texte(0,y,'OUI appuyer sur "o"',couleur = 'black',ancrage = 'sw')
        rectangle(x,y,x/2,y/2+y/4,remplissage = 'orange')
        texte(x,y,'NON appuyer sur "n"',couleur = 'black',ancrage = 'se')
        texte(x/2,y/2,'Voulez vous rejouer ?',couleur = 'white',ancrage = 'center')
        
        texte(x/2,y/4,'VICTORY !',couleur = "yellow",ancrage = 'n')
        image(150,350,'Dragon_s_mort.png',largeur=50, hauteur=100,tag='im')
    #si on perd affiche qu'on a perdu
    elif end == -1 :
        rectangle(0,0,x,y,remplissage = 'gray')
        image(x/2,y/4,'Dragon_s.png',largeur = 400 , hauteur = 500 , tag ='im')
        rectangle(x/2-x/4,y/4-y/8,x/2+x/4,y/4+y/8,remplissage = "red")
        
        rectangle(0,y,x/2,y/2+y/4,remplissage = 'blue')
        texte(0,y-y/16,'OUI appuyer sur "o"',couleur = 'black',ancrage = 'sw')
        rectangle(x,y,x/2,y/2+y/4,remplissage = 'orange')
        texte(x,y-y/16,'NON appuyer sur "n"',couleur = 'black',ancrage = 'se')
        texte(x/2,y/2,'VOULEZ-VOUS REJOUER ?',couleur = 'white',ancrage = 'center')
        
        texte(x/2,y/4,'Game Over !',couleur = "black",ancrage = 'n')
        image(150,350,'Knight_s_mort.png',largeur=50, hauteur=100,tag='skin_aventurier')
        


'''Programme principale'''

x = 800
y = 800
cree_fenetre(x,y)
nombre_de_niveau = 4
#permet de choisir son donjon en cliquant dessus

#inisialiser les valeurs de base pour pouvoir afficher le bon donjon la bonne position pour l'aventurier et les bonnes position pour le dragons
x1_choix, x2_choix, nombre_de_niveau,espace = choix_donjon(nombre_de_niveau)
nom = choix_nom_donjon(x1_choix,x2_choix,nombre_de_niveau,espace)


donjon = charger(nom)[0]
aventurier = charger(nom)[1]
dragons = charger(nom)[2]
inisialiser_donjon(donjon,aventurier,dragons,x,y)

while True:
    #pivote le donjon lorsqu'on sur une des salles du donjons
    position_a_pivoter = cordoone_salle_vers_POSITION()
    pivot(donjon, position_a_pivoter)
    inisialiser_donjon(donjon, aventurier, dragons, x, y)
    
    chemin = intention(donjon, aventurier['position'], dragons, set())
    if chemin is not None:
        afficher_chemin(chemin)
        ev = attend_ev()
        tev = type_ev(ev)
        if tev == 'Touche':
            
            if touche(ev) == 'space':
                maj_chemin_aventurier(chemin)
                appliquer_chemin(aventurier, dragons, chemin)
                efface_tout()
                inisialiser_donjon(donjon, aventurier, dragons, x, y)
                fin_partie_graphique(aventurier, dragons)
                if fin_partie(aventurier, dragons) == 1 or fin_partie(aventurier, dragons) == -1:
                    ev_rejouer = attend_ev()
                    tev_rejouer = type_ev(ev_rejouer)
                    if tev_rejouer == 'Touche':
                        if touche(ev_rejouer) == 'n':
                            ferme_fenetre()
                            break
                            
                        elif touche(ev_rejouer) == 'o':
                            efface_tout()
                            x1_choix, x2_choix, nombre_de_niveau,espace = choix_donjon(nombre_de_niveau)
                            nom = choix_nom_donjon(x1_choix,x2_choix,nombre_de_niveau,espace)
                            donjon = charger(nom)[0]
                            aventurier = charger(nom)[1]
                            dragons = charger(nom)[2]
                            inisialiser_donjon(donjon,aventurier,dragons,x,y)
                            mise_a_jour() 