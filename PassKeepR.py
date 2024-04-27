from rich.console import Console
from rich.table import Table
from colorama import Fore, Back, Style, init
import secrets
import string
import subprocess
import platform
import sqlite3

def clear_terminal():
  if platform.system() == 'Windows':
    subprocess.call('cls', shell=True)
  else:
    subprocess.call('clear', shell=True)
  ascii_prompt = str("""
   ▄▄▄· ▄▄▄· .▄▄ · .▄▄ · ▄ •▄ ▄▄▄ .▄▄▄ . ▄▄▄·▄▄▄  
  ▐█ ▄█▐█ ▀█ ▐█ ▀. ▐█ ▀. █▌▄▌▪▀▄.▀·▀▄.▀·▐█ ▄█▀▄ █·
   ██▀·▄█▀▀█ ▄▀▀▀█▄▄▀▀▀█▄▐▀▀▄·▐▀▀▪▄▐▀▀▪▄ ██▀·▐▀▀▄ 
  ▐█▪·•▐█ ▪▐▌▐█▄▪▐█▐█▄▪▐█▐█.█▌▐█▄▄▌▐█▄▄▌▐█▪·•▐█•█▌
  .▀    ▀  ▀  ▀▀▀▀  ▀▀▀▀ ·▀  ▀ ▀▀▀  ▀▀▀ .▀   .▀  ▀
  """)
  print(Fore.GREEN + ascii_prompt + Fore.RESET)
def dropDB():
  conn = sqlite3.connect('PassDB.db')

  cursor = conn.cursor()
  cursor.execute("""
    DROP TABLE users_BDD
    """)
  conn.commit()
  conn.close()
def passgen():

  lettres = string.ascii_letters
  nombres = string.digits
  special_car = string.punctuation

  password = str("")
  pwd_length = int(input("Combien de caractère voulez-vous pour votre mot de passe ?\n"))
  content = str(input("\nQuels types de caractères voulez-vous pour votre mot de passe ?\nChoix possible : \n\t1 - Lettres + Nombres\n\t2 - Lettres + Caractère spéciaux\n\t3 - Nombres + Caratères spéciaux\n\t4 - Lettres + Nombres + Cractères spéciaux\n"))

  if content == "1":
    content = lettres + nombres
    for i in range(pwd_length):
      password += "".join(secrets.choice(content))

  elif content == "2":
    content = lettres + special_car
    for i in range(pwd_length):
      password += "".join(secrets.choice(content))

  elif content == "3":
    content = nombres + special_car
    for i in range(pwd_length):
      password += "".join(secrets.choice(content))

  elif content == "4":
    content = lettres + nombres + special_car
    for i in range(pwd_length):
      password += "".join(secrets.choice(content))

  else:
    print("Il n'y a que 4 choix possible")
    passgen()

  return password
def createDB():
  site = str(input("Entrez l'URL complète du site : "))
  user = str(input("Entrez votre nom d'utilisateur : "))
  passw = str(input("Avez-vous deja un mot de passe ?\n\t1 - Oui\n\t2 - Non\n"))

  if passw == "1":
    passw = str(input("Entrez votre mot de passe : "))
  elif passw == "2":
    passw = passgen()
  else:
    print("Que deux choix de disponible")

  conn = sqlite3.connect('PassDB.db')

  cursor = conn.cursor()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS users_BDD(
       id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
       site TEXT,
       user TEXT,
       password TEXT
    )
    """)

  cursor.execute("""INSERT INTO users_BDD(site,user,password) VALUES(?,?,?)""", (site, user, passw))

  cursor.execute("""
    SELECT site, user, password FROM users_BDD
    """)
  new_line = cursor.fetchall()

  table = Table(title="Mon Gestionnaire de Mot de Passe")

  table.add_column("Site", justify="center", style="cyan")
  table.add_column("Username", justify="center", style="magenta")
  table.add_column("Password", justify="center", style="red")

  for item in new_line:
    table.add_row(item[0], item[1], item[2])

  console = Console()
  console.print(table)

  conn.commit()
  conn.close()
def printDB():
  conn = sqlite3.connect('PassDB.db')

  cursor = conn.cursor()
  cursor.execute("""
  SELECT site, user, password FROM users_BDD
  """)

  ret_BDD = cursor.fetchall()

  table = Table(title="Mon Gestionnaire de Mot de Passe")

  table.add_column("Site", justify="center", style="cyan")
  table.add_column("Username", justify="center", style="magenta")
  table.add_column("Password", justify="center", style="red")

  for item in ret_BDD:
    table.add_row(item[0], item[1], item[2])

  console = Console()
  console.print(table)

clear_terminal()
Choix = str(input("Que voulez-vous faire ? \n\t1 - Ajouter un compte\n\t2 - Supprimer la base de donner\n\t3 - Afficher la Base De Donnée\n"))

if Choix == "1":
  createDB()
elif Choix == "2":
  dropDB()
elif Choix == "3":
  printDB()
else:
  print("Que trois choix de disponible")


