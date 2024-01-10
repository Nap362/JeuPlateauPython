import random
import datetime
##initialisation grille et variables
j="\033[0;33mo\033[0m"
b="\033[0;36m+\033[0m"
r="\033[0;31mx\033[0m"
v=" "

def valeur_pion(chaine) :
    if (chaine=="j"):
        return j
    elif (chaine=="b") :
        return b
    elif (chaine=="r") :
        return r
    else :
        return v

def init_grille() :
    fichier = open("Grilles.txt", "r")
    grilles = fichier.readlines()
    fichier.close()
    grille_chaine = grilles[random.randint(0, len(grilles) - 1)]
    lignes_grille = grille_chaine.split(';')
    grille_temp = []
    grille = []
    for elem in lignes_grille :
        grille_temp.append(elem.split(","))
    for lig in grille_temp :
        ligne = []
        for case in lig :
            ligne.append(valeur_pion(case))
        grille.append(ligne)
    grille.pop(-1)
    return grille

def ecrire_historique(joueur1, joueur2, score_j1, score_j2, niveau) :
    if (niveau==0) :
        partie = "Mode 2 joueurs"
    elif (niveau==1) :
        partie = "Mode Facile"
    elif (niveau==2) :
        partie = "Mode Moyen"
    else :
        partie = "Mode Difficile"
    fichier = open("Historique.txt", "a")
    if (score_j1 > score_j2) :
        result = "Vainqueur : " + joueur1
    elif (score_j2 > score_j1) :
        result = "Vainqueur : " + joueur2
    else :
        result = "Egalité"
    resume_partie = "{0} - {1} - {2} : {3} | {4} : {5} - {6}".format(datetime.date.today(), partie, joueur1, score_j1, joueur2, score_j2, result)
    fichier.write("\n" + resume_partie)
    fichier.close()

##affichage
def affichage_grille(grille) :
    lignes=["A","B","C","D","E","F","G","H"]
    print("   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |")
    print("---+---+---+---+---+---+---+---+---+---")
    i=0
    for ligne in grille :
        print("",lignes[i],"|", end="")
        for case in ligne:
            print("",case,"|", end="")
        print("", lignes[i])
        print("---+---+---+---+---+---+---+---+---+---")
        i+=1
    print("   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |")

def affichage_score(butin_j1, butin_j2, joueur1, joueur2) :
    print("\n  Butin de", joueur1, ":")
    print("     +--------+--------+--------+")
    print('     | {0} : {3:2d} | {1} : {4:2d} | {2} : {5:2d} |    Malus : {6:2d}'.format(j, r, b, butin_j1[0], butin_j1[1], butin_j1[2],  butin_j1[3]))
    print("     +--------+--------+--------+")
    print("  Butin de", joueur2, ":")
    print("     +--------+--------+--------+")
    print('     | {0} : {3:2d} | {1} : {4:2d} | {2} : {5:2d} |    Malus : {6:2d}'.format(j, r, b, butin_j2[0], butin_j2[1], butin_j2[2],  butin_j2[3]))
    print("     +--------+--------+--------+\n")

def afficher_coup_ordi(depart, arrivee) :
    lettres = ["A","B","C","D","E","F","G","H"]
    chaine_depart = lettres[depart[0]] + str(depart[1] + 1)
    chaine_arrivee = lettres[arrivee[0]] + str(arrivee[1] + 1)
    print("Case de départ :", chaine_depart)
    print("Case d'arrivée :",chaine_arrivee)

def affichage_vainqueur(butin_j1, butin_j2, joueur1, joueur2, niveau) :
    score_j1 = butin_j1[0] + (butin_j1[1] * 2) + (butin_j1[2] * 3) - ((butin_j1[2] - butin_j1[3]%2) // 2)
    score_j2 = butin_j2[0] + (butin_j2[1] * 2) + (butin_j2[2] * 3) - ((butin_j2[2] - butin_j2[3]%2) // 2)
    print("\n\tFin de partie\n\t  ---------\n")
    print("Score de", joueur1, ":", score_j1)
    print("Score de", joueur2, ":", score_j2, "\n")
    if (score_j1 > score_j2) :
        print("\tFélicitation", joueur1, "!")
    elif (score_j2 > score_j1) :
        print("\tFélicitation", joueur2, "!")
    else :
        print("\tFélicitions", joueur1, "et", joueur2, "!")
    ecrire_historique(joueur1, joueur2, score_j1, score_j2, niveau)


##vérifications coordonnées
#ord(A)=65, ord(Z)=91
def est_une_lettre(caractere):
    return 65 <= ord(caractere) <= 91
#ord(0)=48, ord(9)=57
def est_un_chiffre(caractere):
    return 48 <= ord(caractere) <= 57

#ord(A)=65, ord(H)=72
def est_dans_grille(coordonnee) :
    if len(coordonnee)==2:
        return 65<=ord(coordonnee[0])<=72 and 1<=int(coordonnee[1])<=8
    else :
        return False

def est_au_bon_format(coordonnee):
    if len(coordonnee) > 1 and est_une_lettre(coordonnee[0]):
        i = 1
        while i < len(coordonnee):
            if not est_un_chiffre(coordonnee[i]):
                return False
            i = i + 1
        return True
    else:
        return False

##vérification déplacements
def indices_valides(lig, col) :
    return 0 <= lig <= 7 and 0 <= col <= 7

def conversion_coordonnee(coordonnee):
    lig = ord(coordonnee[0])-65
    col = int(coordonnee[1]) - 1
    return (lig,col)

def bonne_distance_deplacement(lig_dep, col_dep, lig_arr, col_arr):
    diff_lig = lig_arr - lig_dep
    diff_col = col_arr - col_dep
    return (diff_lig == 0 or diff_lig == 2 or diff_lig == -2) and (diff_col == 0 or diff_col == 2 or diff_col == -2) and (diff_lig != 0 or diff_col != 0)

def case_intermediaire(lig_dep, col_dep, lig_arr, col_arr):
    lig_inter = lig_dep + (lig_arr - lig_dep) // 2
    col_inter = col_dep + (col_arr - col_dep) // 2
    return (lig_inter,col_inter)

def deplacement_valide(lig_dep, col_dep, lig_arr, col_arr, grille):
    lig_inter, col_inter = case_intermediaire(lig_dep, col_dep, lig_arr, col_arr)
    if grille[lig_dep][col_dep] == j and grille[lig_arr][col_arr] == v and grille[lig_inter][col_inter] != v:
        return bonne_distance_deplacement(lig_dep, col_dep, lig_arr, col_arr)
    else :
        return False

def cases_arrivee_possibles(grille, lig_dep, col_dep) :
    dir = [(-2,-2), (-2,0), (-2,2), (0,-2), (0, 2), (2,-2), (2,0), (2,2)]
    cases_arr = []
    for elem in dir :
        lig_arr, col_arr = lig_dep + elem[0], col_dep + elem[1]
        if indices_valides(lig_arr, col_arr) and deplacement_valide(lig_dep, col_dep, lig_arr, col_arr, grille) :
            cases_arr.append((lig_arr, col_arr))
    return cases_arr


## fonctions de choix
def demande_selection(options, texte) :
    val = input(texte)
    while (not val in options) :
        print("Commande inconnue.")
        val = input(texte)
    return val

def choix_noms_joueurs(nb_joueurs) :
    changement = demande_selection(["O", "N"],"Personnaliser les noms des joueurs ? O/N\n")
    if (nb_joueurs==1) :
        if (changement == "O") :
            joueur1 = input("Nom du Joueur 1 : ")
        else :
            joueur1 = "Joueur 1"
        joueur2 = "Ordinateur"
    else :
        if (changement == "O") :
            joueur1 = input("Nom du Joueur 1 : ")
            joueur2 = input("Nom du Joueur 2 : ")
        else :
            joueur1, joueur2 = "Joueur 1", "Joueur 2"
    return joueur1, joueur2

def demande_coordonnees(texte):
    coordonnee=input(texte)
    valide = False
    while (not valide) :
        if not est_au_bon_format(coordonnee) :
            print("Format invalide, veuillez recommencer. [Format = A1]")
            coordonnee=input(texte)
        elif not est_dans_grille(coordonnee) :
            print("Coordonnées hors de la grille, veuillez recommencer. [Grille = A1 - H8]")
            coordonnee=input(texte)
        else :
            valide = True
    return conversion_coordonnee(coordonnee)

def case_depart(grille) :
    lig_dep, col_dep = demande_coordonnees("Case de départ : ")
    cases_arr = cases_arrivee_possibles(grille, lig_dep, col_dep)
    while (cases_arr == []) :
        print("Pion non jouable. Veuillez recommencer.\n")
        lig_dep, col_dep = demande_coordonnees("Case de départ : ")
        cases_arr = cases_arrivee_possibles(grille, lig_dep, col_dep)
    return lig_dep, col_dep, cases_arr

def case_arrivee(grille, cases_arr) :
    lig_arr, col_arr = demande_coordonnees("Case d'arrivée : ")
    while not ((lig_arr, col_arr) in cases_arr) :
        print("Déplacement invalide. Veuillez recommencer.\n")
        lig_arr, col_arr = demande_coordonnees("Case d'arrivée : ")
    return lig_arr, col_arr


##modification éléments du jeu
def modif_grille(grille, lig_dep, col_dep, lig_arr, col_arr):
    lig_inter, col_inter = case_intermediaire(lig_dep, col_dep, lig_arr, col_arr)
    grille[lig_dep][col_dep] = v
    pion_capture = grille[lig_inter][col_inter]
    grille[lig_inter][col_inter] = v
    grille[lig_arr][col_arr] = j
    return pion_capture

def modif_butin(butin_joueur_courant, pion_capture) :
    if (pion_capture == j) :
        butin_joueur_courant[0] += 1
    elif (pion_capture == r) :
        butin_joueur_courant[1] += 1
    else :
        butin_joueur_courant[2] += 1


##deroulement de la partie
def prochain_joueur(joueur_courant) :
    return (joueur_courant + 1) % 2

def points_pion(pion) :
    if (pion==j) :
        return 1
    elif (pion==r) :
        return 2
    else :
        return 3

def liste_pions_deplacables(grille) :
    liste = []
    for lig in range (len(grille)) :
        ligne = grille[lig]
        for col in range (len(ligne)) :
            if (cases_arrivee_possibles(grille, lig, col) != []) :
                liste.append((lig, col))
    return liste

def enchainement(grille, lig_dep, col_dep, butin_joueur_courant) :
    choix = demande_selection(["O", "N"], "Voulez-vous continuer ? O/N\n")
    if (choix=="O") :
        if (cases_arrivee_possibles(grille, lig_dep, col_dep) == []) :
            print("Pas d'enchainement possible.")
            butin_joueur_courant[3] += 1
            return False
        return True
    else :
        return False

def jouer_coup(grille, butin_joueur_courant):
    lig_dep, col_dep, cases_arr = case_depart(grille)
    lig_arr, col_arr = case_arrivee(grille, cases_arr)
    pion_capture = modif_grille(grille, lig_dep, col_dep, lig_arr, col_arr)
    modif_butin(butin_joueur_courant, pion_capture)
    lig_dep, col_dep = lig_arr, col_arr
    while enchainement(grille, lig_dep, col_dep, butin_joueur_courant) :
        affichage_grille(grille)
        cases_arr = cases_arrivee_possibles(grille, lig_dep, col_dep)
        lig_arr, col_arr = case_arrivee(grille, cases_arr)
        pion_capture = modif_grille(grille, lig_dep, col_dep, lig_arr, col_arr)
        modif_butin(butin_joueur_courant, pion_capture)
        lig_dep, col_dep = lig_arr, col_arr
    return grille, butin_joueur_courant

##coup ordinateur
def liste_coups_simples_possibles(g, liste_cases_departs) :
    liste = []
    for depart in liste_cases_departs :
        liste_cases_arrivees = cases_arrivee_possibles(g, depart[0], depart[1])
        for arrivee in liste_cases_arrivees :
            lig_inter, col_inter = case_intermediaire(depart[0], depart[1], arrivee[0], arrivee[1])
            points = points_pion(g[lig_inter][col_inter])
            liste.append([depart, arrivee, points])
    return liste

def copie_grille(grille1) :
    grille2 = []
    for elem in grille1 :
        grille2.append(list(elem))
    return grille2

def liste_enchainements(grille, lig_dep, col_dep) :
    grille_temp = copie_grille(grille)
    liste_cases_arrivees = cases_arrivee_possibles(grille_temp, lig_dep, col_dep)
    liste_ench = []
    for arrivee in liste_cases_arrivees :
        pion_capture = modif_grille(grille_temp, lig_dep, col_dep, arrivee[0], arrivee[1])
        points = points_pion(pion_capture)
        liste_suite_ench = liste_enchainements(grille_temp, arrivee[0], arrivee[1])
        if (liste_suite_ench == []) :
            liste_ench.append([arrivee, points])
        else :
            for elem in liste_suite_ench :
                elem.insert(0, arrivee)
                elem[-1] += points
            liste_ench.append(elem)
        grille_temp = copie_grille(grille)
    return liste_ench

def liste_coups_enchainements_possibles(grille, liste_cases_departs) :
    grille_temp = copie_grille(grille)
    liste = []
    for depart in liste_cases_departs :
        liste_ench = liste_enchainements(grille_temp, depart[0], depart[1])
        for elem in liste_ench :
            elem.insert(0,depart)
            liste.append(elem)
    return liste

def meilleur_coup(liste) :
    max = 0
    coup = []
    for elem in liste :
        if (max < elem[-1]) :
            max = elem[-1]
            coup = elem
    return coup

def coup_ordi(grille, butin_joueur_courant, niveau):
    liste_cases_departs = liste_pions_deplacables(grille)
    if (niveau ==1) :
        liste_coups_possibles = liste_coups_simples_possibles(grille, liste_cases_departs)
        coup = liste_coups_possibles[random.randint(0, len(liste_coups_possibles) - 1)]
        coup.pop(-1)
    elif (niveau == 2) :
        liste_coups_possibles = liste_coups_simples_possibles(grille, liste_cases_departs)
        coup = meilleur_coup(liste_coups_possibles)
        coup.pop(-1)
    else :
        ##niveau==3
        liste_coups_possibles = liste_coups_enchainements_possibles(grille, liste_cases_departs)
        coup = meilleur_coup(liste_coups_possibles)
        coup.pop(-1)
    afficher_coup_ordi(coup[0], coup[1])
    pion_capture = modif_grille(grille, coup[0][0], coup[0][1], coup[1][0], coup[1][1])
    modif_butin(butin_joueur_courant, pion_capture)
    if (niveau==3) :
        coup.pop(0)
        depart = coup.pop(0)
        while (coup != []) :
            print("Enchainement")
            affichage_grille(grille)
            arrivee = coup.pop(0)
            afficher_coup_ordi(depart, arrivee)
            pion_capture = modif_grille(grille, depart[0], depart[1], arrivee[0], arrivee[1])
            modif_butin(butin_joueur_courant, pion_capture)
            depart = arrivee
        return grille, butin_joueur_courant
    else :
        coup.pop(0)
        depart = coup[0]
        liste_coups_possibles = liste_coups_simples_possibles(grille, coup)
        while (liste_coups_possibles != []) :
            ## choisir de faire un enchainement ou non pour l'IA de niveau 1
            suite = random.randint(0, 1)
            if (niveau==1 and suite==1) :
                print("Enchainement")
                affichage_grille(grille)
                coup = liste_coups_possibles[random.randint(0, len(liste_coups_possibles) - 1)]
                coup.pop(-1)
                afficher_coup_ordi(coup[0], coup[1])
                pion_capture = modif_grille(grille, coup[0][0], coup[0][1], coup[1][0], coup[1][1])
                modif_butin(butin_joueur_courant, pion_capture)
            elif (niveau==2) :
                print("Enchainement")
                affichage_grille(grille)
                coup = meilleur_coup(liste_coups_possibles)
                coup.pop(-1)
                afficher_coup_ordi(coup[0], coup[1])
                pion_capture = modif_grille(grille, coup[0][0], coup[0][1], coup[1][0], coup[1][1])
                modif_butin(butin_joueur_courant, pion_capture)
            else :
                ##niveau==1 et suite==1 -> fin du coup
                return grille, butin_joueur_courant
            coup.pop(0)
            depart = coup[0]
            liste_coups_possibles = liste_coups_simples_possibles(grille, coup)
        return grille, butin_joueur_courant

def partie(grille, joueur1, joueur2, niveau) :
    print("   ------------------------------")
    print("\tDébut de la partie\n")
    joueur_courant = 0
    butins = [[0, 0, 0, 0], [0, 0, 0, 0]]
    joueurs = [joueur1, joueur2]
    while (liste_pions_deplacables(grille) != []) :
        affichage_grille(grille)
        affichage_score(butins[0], butins[1], joueurs[0], joueurs[1])
        print("\tTour de", joueurs[joueur_courant])
        if(joueur_courant==1 and niveau != 0) :
            ##au tour de l'Ordinateur
            grille, butins[joueur_courant] = coup_ordi(grille, butins[joueur_courant], niveau)
        else :
            grille, butins[joueur_courant] = jouer_coup(grille, butins[joueur_courant])
        joueur_courant = prochain_joueur(joueur_courant)
        liste_cases_departs = liste_pions_deplacables(grille)
    affichage_grille(grille)
    affichage_score(butins[0], butins[1], joueurs[0], joueurs[1])
    affichage_vainqueur(butins[0], butins[1], joueurs[0], joueurs[1], niveau)

##menu
def menu() :
    print("                            Bienvenue !\n")
    print("        Jouer        |    Règles du jeu    | Historique parties")
    print("          1          |          2          |          3\n")
    choix = int(demande_selection(["1", "2", "3"], "Sélection :"))
    if (choix == 1):
        grille = init_grille()
        print("                   Type de partie")
        print("     Joueur VS Joueur     |   Joueur VS Ordinateur")
        print("            1             |            2\n")
        choix = int(demande_selection(["1", "2"], "Sélection :"))
        if (choix == 1) :
            joueur1, joueur2 = choix_noms_joueurs(2)
            partie(grille, joueur1, joueur2, 0)
        else :
            print("                     Niveau")
            print("     Facile     |     Moyen     |     Difficile")
            print("       1        |       2       |         3\n")
            choix = int(demande_selection(["1", "2", "3"], "Sélection :"))
            joueur1, joueur2 = choix_noms_joueurs(1)
            partie(grille, joueur1, joueur2, choix)
    elif (choix == 2):
        print("\n--------------\n")
        fichier = open("ReglesDuJeu.txt", "r")
        for line in fichier:
            print(line, end='')
        fichier.close()
        print("")
        menu()
    else :
        print("\n--------------\n")
        fichier = open("Historique.txt", "r")
        for line in fichier:
            print(line, end='')
        fichier.close()
        print("")
        menu()

###Code principal
menu()


##Tests
def test_est_au_bon_format():
    assert est_au_bon_format("A1"), "Format valide doit être vrai"
    assert not est_au_bon_format("3B"), "Inversion caractère doit être faux"
    assert not est_au_bon_format("BA"), "Format deux lettres doit être faux"
    assert not est_au_bon_format("22"), "Format 2 chiffres doit être faux"
    assert not est_au_bon_format("Z"), "Format un caractère doit être faux"
    assert est_au_bon_format("M777"), "Format une lettre plusieurs chiffres doit être vrai"


def test_est_dans_grille():
    assert est_dans_grille("A1"), "Coordonnee grille doit être vrai"
    assert not est_dans_grille("B11"), "Colonne hors grille doit être faux"
    assert not est_dans_grille("X1"), "Ligne hors grille doit être faux"
    assert est_dans_grille("Z9"), "Lign et colonne hors grille doit être faux"
