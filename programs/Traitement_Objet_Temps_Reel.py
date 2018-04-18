# def ( tableau d'objet du joueur i, nom de l'objet précédent, compteur d'Objet de joueur i, compteur de None de joueur i, i : numero du joueur )
def complement_Objet_Direct(tableau,reference,compteur_Objet_J,compteur_None_J,i):
    if tableau is None :
        return reference, compteur_Objet_J, compteur_None_J

    #CAS None-None
    if ( ( tableau[len(tableau)-1] == None ) & ( reference == None ) ):
        compteur_None_J +=1
        reference = None
    else :
        #CAS Objet-Objet
        #objets differents
        if ( ( tableau[len(tableau)-1] != None ) & ( reference != tableau[len(tableau)-1] ) )  :
            reference = tableau[len(tableau)-1]
            compteur_Objet_J = 0
            compteur_None_J = 0
        #objets identiques
        else :
            if ( (reference == tableau[len(tableau)-1] ) & (compteur_Objet_J == 5) ):
                print('l objet du joueur ',i+1, ' est ', (tableau[len(tableau)-1]))
                compteur_Objet_J +=1
                #compteur_None_J = 0
            else :
                    if ( (reference == tableau[len(tableau)-1] ) &  (compteur_Objet_J != 5) ):
                        compteur_Objet_J += 1
                    else :
                        # CAS None-Objet
                        # + de 25 None
                        if ( ( tableau[len(tableau)-1] != None ) & ( reference == None ) & ( compteur_None_J > 25 ) ) :
                            reference = tableau[len(tableau) - 1]
                            compteur_None_J = 0
                            compteur_Objet_J = 0
                        # - de 15 None
                        else :
                            if( ( tableau[len(tableau)-1] != None ) & ( reference == None ) & (compteur_None_J < 25) ):
                                reference = tableau[len(tableau) - 1]
                                compteur_Objet_J += 1
                                compteur_None_J = 0
                            else :
                                # CAS Objet-None
                                if ( ( tableau[len(tableau)-1] == None ) & ( reference != None ) ) :
                                    compteur_None_J +=1



    return reference,compteur_Objet_J,compteur_None_J

# A METTRE DANS LE CODE PRINCIPAL
if __name__ == '__main__':
    # apres le code de reconnaissance d'objet on obtient un tableau contenant le nom des objets et des None
    # exemple de tableau : tableau = [['cv'],[None],['cr'],['cv']]
    tableau = [['cv'], [None], ['cr'], ['cv']]
    # variables a creer :
    reference_Statu = ['cv',None,None,None]
    compteur_Objet = [1,0,0,0]
    compteur_None = [0,0,20,0]
    # on regarde le dernier element des 4 liste

    #print(reference_Statu,compteur_Objet,compteur_None)


def affiche_objet(tableau, reference_statu, compteur_objet, compteur_none):
    for i in range(0, len(tableau)):
        J = tableau[i]
        reference_statu[i],compteur_objet[i],compteur_none[i] = complement_Objet_Direct(J,reference_statu[i], compteur_objet[i], compteur_none[i], i)

