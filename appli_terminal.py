import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/submit", methods=['POST'])
def contenuSite():
    choice=request.form['choice']

    if choice == '1':

        groupes=name_grp()
        return render_template('nameGrp.html', groupes = groupes)

    elif choice == '2' :

        albums = albums_YGrp()
        return render_template('albums.html', albums = albums)

    elif choice == '3' :

        return render_template('albumsBygrpSearch.html')

    elif choice == '4' :

        return render_template('albumsByYSearch.html')

    return "<p>{}</p>".format(choice)

@app.route("/albums", methods=['POST'])
def contenuAlbums():
    nom_grp = request.form['nameGrp']

    albumsBygrp = albums_by_grp()

    return render_template('albumsBygrp.html', albumsBygrp = albumsBygrp, nom_grp = nom_grp)

@app.route("/albumsByYear", methods = ['POST'])
def contenuAlbumsByYear() :

    year = request.form['year']

    albumsByYear = albums_by_year()

    return render_template('albumsByY.html', year = year, albumsByYear = albumsByYear)

def name_grp(): # affiche le nom des groupes

    #connexion à la bdd
    connexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='record_company'
    )

    # curseur qui va récup les infos dans bdd avec les requetes
    curseur = connexion.cursor()

    curseur.execute("select name from bands;")

    resultat = curseur.fetchall()

    # bonne pratique, toujours fermer les curseurs et connexion pour libérer le serveur
    curseur.close()
    connexion.close()

    return resultat
    

def albums_YGrp() : # affiche les albums crées, avec l'anne et le groupe
    
    #connexion à la bdd

    connexion = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='record_company'
    )

    # curseur qui va récup les infos dans bdd avec les requetes
    curseur = connexion.cursor()

    curseur.execute("SELECT albums.name, albums.release_year, bands.name FROM albums JOIN bands ON albums.band_id = bands.id;")

    resultat = curseur.fetchall()

    for ligne in resultat :
        print(f"{ligne[0]} sorti en {ligne[1]} par {ligne[2]}.")

    # bonne pratique, toujours fermer les curseurs et connexion pour libérer le serveur
    curseur.close()
    connexion.close()

    return resultat

def albums_by_grp() : # affiche les albums d'un groupe par recherche du nom du groupe
    
    #connexion à la bdd
    connexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='record_company'
    )

    # curseur qui va récup les infos dans bdd avec les requetes
    curseur = connexion.cursor()
    
    nom_grp = request.form['nameGrp']

    curseur.execute(f"SELECT albums.name FROM albums JOIN bands ON albums.band_id = bands.id WHERE bands.name = '{nom_grp}';")

    resultat = curseur.fetchall()

    # bonne pratique, toujours fermer les curseurs et connexion pour libérer le serveur
    curseur.close()
    connexion.close()

    return resultat

def albums_by_year():

    #connexion à la bdd
    connexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='record_company'
    )

    # curseur qui va récup les infos dans bdd avec les requetes
    curseur = connexion.cursor()
    
    annee = request.form['year']

    curseur.execute(f"SELECT name FROM albums WHERE release_year = {annee};")

    resultat = curseur.fetchall()

    # bonne pratique, toujours fermer les curseurs et connexion pour libérer le serveur
    curseur.close()
    connexion.close()

    return resultat
# # authentification :

# # pour demain, implémenter md5, sql enregistre que md5 avec scell et la requete compare md5 + scell (expl : secret) que j'ajoute dans la requete de recherche dans 
# # la bdd à la suite du mdp (expl : 123secret)



# sel = "secret"

# def authentification(login, password, sel):

#     #connexion à la bdd
#     connexion = mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='root',
#         database='record_company'
#     )

#     # curseur qui va récup les infos dans bdd avec les requetes
#     curseur = connexion.cursor()

#     curseur.execute(f"SELECT login password FROM users WHERE login='{login}' and password=md5('{password + sel}');")

#     resultat = curseur.fetchall()

#     if len(resultat)> 0:
#         return True
#     else:
#         return False

#     # bonne pratique, toujours fermer les curseurs et connexion pour libérer le serveur
#     curseur.close()
#     connexion.close()

# # modification de mot de passe une fois connecté

# def modif_mdp(login, password, sel) :
#     #connexion à la bdd
#     connexion = mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='root',
#         database='record_company'
#     )
#     password = input("Saisissez votre nouveau mot de passe : ")
    
#     # curseur qui va récup les infos dans bdd avec les requetes
#     curseur = connexion.cursor()    
#     curseur.execute(f"UPDATE users SET password = md5('{password + sel}') WHERE login = '{login}'; COMMIT;")


#     print(f"Lignes modifiées : {curseur.rowcount}")
    
    
#     # bonne pratique, toujours fermer les curseurs et connexion pour libérer le serveur
#     curseur.close()
#     connexion.close()

#     return True

# is_auth = False

# while is_auth == False :
#     login = input("Saisissez le login : ")

#     password = input("Saisissez le password : ")

#     if (authentification(login, password, sel)) :
#         is_auth = True
#         print("Authentification réussie !!")
#     else :
#         print("Echec d'authentification :(")



# # menu d'interface après login

# want_quit = False

# print("Bonjour et bienvenu dans cette application conçue pour modifier notre base de données.")

# while want_quit == False:

#     print("1. Afficher les noms de groupes présents dans la BDD")
#     print("2. Afficher la liste des albums avec leur année de publication et le groupe qui les a enregistrés")
#     print("3. Afficher les albums d'un groupe (avec une recherche par nom du groupe)")
#     print("4. Afficher les albums sortis pour une année (avec une recherche par année)")
#     print("5. Modifier mon mot de passe")
#     print("6. Me reconnecter")
#     print("7. Quitter")


#     choice = input("Entrez le chiffre correspondant à l'action que vous souhaitez effectuer : ")

#     if choice == '1' :
#         name_grp()
#     elif choice == '2' :
#         albums_YGrp()
#     elif choice == '3':
#         albums_by_grp()
#     elif choice == '4':
#         albums_by_year()
#     elif choice== '5' :
#         print(modif_mdp(login, password, sel))
#     elif choice == '6' : 
#         is_auth = False

#         while is_auth == False :
#             login = input("Saisissez le login : ")

#             password = input("Saisissez le password : ")

#             if (authentification(login, password, sel)) :
#                 is_auth = True
#                 print("Authentification réussie !!")
#             else :
#                 print("Echec d'authentification :(")

        
#     elif choice == '7':
#         print("Au revoir.")
#         want_quit = True
        
#     else:
#         print("Choix invalide, veuillez entrer un chiffre valide.")
        