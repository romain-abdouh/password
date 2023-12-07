import json
import hashlib
import getpass
import random
import string


# l’algorithme de hachage SHA-256 seul donnera toujours le même hashage pour le même mot de passe entrée.

# Generation mot de passes aléatoires
characters = string.ascii_letters + string.digits + string.punctuation
password_length = 12 
password = ""
for _ in range(password_length):
   password += random.choice(characters)

print("Mot de passe généré : {}".format(password))


# Enregistrement d'un utilisateur avec nom + mot de passe correspondant au criteres
def enregistrement():
    while True:
        nom = input("Entrez votre nom: ")
        password = getpass.getpass("Entrez votre mot de passe : ")
        liste_caractere = ('!', '@', '#', '$', '%', '^', '&')

        if len(password) < 8:
            print('Il doit y avoir au moins 8 caractères')
        elif not any(char.isdigit() for char in password):
            print('Il faut au moins un chiffre')
        elif not any(char.isupper() for char in password):
            print('Il faut au moins une lettre majuscule')
        elif not any(char.islower() for char in password):
            print('Il faut au moins une lettre minuscule')
        elif not any(char in password for char in liste_caractere):
            print('Mettez au moins un symbole spécial : !, @, #, $, %, ^, &')
        else:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()           
            try:
                with open('utilisateur.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = {}
            if nom in data and hashed_password in data[nom]['hashed_password']:
                print("Le mot de passe est déjà enregistré.")
            else: 
                if nom in data:
                    data[nom]['hashed_password'].append(hashed_password) # j'ai ajouté cette ligne pour permettre à utilisateur d'avoir plusieurs mots de passe 
                else:
                    data[nom] = {'hashed_password': [hashed_password]}
                print("Utilisateur créé !")    
            # écrit nouveaux données dans le fichier
            with open('utilisateur.json', 'w') as f:
                json.dump(data, f)
        return nom

# Connexion de l'utilisateur
def login():
    nom = input("Entrez votre nom: ")
    password = getpass.getpass("Entrez votre mot de passe : ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # recuperation données 
    with open('utilisateur.json', 'r') as f:
        data = json.load(f)

    if nom in data and hashed_password in data[nom]['hashed_password']:
        print("Connection réussi")
        return True
    else:
        print("Mauvais nom ou mot de passe.")
        return False

# Menu
def menu():
    nom = None
    while True:
        print("1. Enregistrer")
        print("2. Connecter")
        print("3. Quitter")
        choice = input("Entrez votre choix : ")

        if choice == '1':
            nom = enregistrement()

        elif choice == '2':
            if login():
                gerer_passwords(nom)

        elif choice == '3':
            break

# Gerer les mots de passes
def gerer_passwords(nom):
    while True:
        print("1. Voir mot de passe")
        print("2. Ajouter mot de passe")
        print("3. Quitter")
        password_choice = input("Entrez votre choix : ")

        if password_choice == '1':
            with open('utilisateur.json', 'r') as f:
               data = json.load(f)
            # Permet d'afficher les mots de passes que de l'utilisateur connecté
            user_data = {key: value for key, value in data.items() if key == nom}
            if nom is not None and nom in user_data:
                print(f"Vos mots de passe sont : {user_data[nom]['hashed_password']}")
            else:
               print("Aucun mot de passe enregistré pour ce nom.")

        elif password_choice == '2':
            while True:
                nouveau_password = getpass.getpass("Entrez votre nouveau mot de passe : ")
                liste_caractere = ('!', '@', '#', '$', '%', '^', '&')
                if len(nouveau_password) < 8:
                    print('Il doit y avoir au moins 8 caractères')
                elif not any(char.isdigit() for char in nouveau_password):
                    print('Il faut au moins un chiffre')
                elif not any(char.isupper() for char in nouveau_password):
                    print('Il faut au moins une lettre majuscule')
                elif not any(char.islower() for char in nouveau_password):
                    print('Il faut au moins une lettre minuscule')
                elif not any(char in nouveau_password for char in liste_caractere):
                    print('Mettez au moins un symbole spécial : !, @, #, $, %, ^, &')
                else:
                    new_hashed_password = hashlib.sha256(nouveau_password.encode()).hexdigest()
                    # recuperation données
                    try:
                        with open('utilisateur.json', 'r') as f:
                            data = json.load(f)
                    except FileNotFoundError:
                        data = {}

                    if nom in data and new_hashed_password in data[nom]['hashed_password']:
                        print("Le mot de passe est déjà enregistré.")
                    else: 
                        if nom in data:
                            data[nom]['hashed_password'].append(new_hashed_password)
                        else:
                            data[nom] = {'hashed_password': [new_hashed_password]}

                    # écrit nouveaux données dans le fichier
                        with open('utilisateur.json', 'w') as f:
                            json.dump(data, f)
                        print("Nouveau mot de passe enregistré !")

                return nom

        elif password_choice == '3':
           break

menu()