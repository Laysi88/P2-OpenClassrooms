# Bêta scrapping Book to Scrape

## Prérequis:
- IDE (exemple:VSCODE ou Pycharm ou tout autre IDE de votre choix)
- Python: disponible sur https://www.python.org/

**Marche à suivre sous Windows**

## Etape 1: Initialisation de votre envirronement virtuel

Ouvrir le dossier "Projet N°2" sur votre IDE
Créé votre envirronement virtuel dans le terminal powershell avec la commande : 

`python -m venv env`

Une fois votre environement virtuel créé, lancer la commande:

`.\env\Scripts\Activate.ps1 dans votre terminal`

Vous vous retrouverez alors sur votre environement virtuel.

## Etape 2: Installer les Prérequis

Dans votre terminal entrer la commande:

`pip install -r requirements.txt`

## Etape 3:Lancer le programme de scrapping

Dans votre terminal entrer la commande:

`python main.py`

### Phase 1
 - Choississez si vous voulez scrapper un livre en indiquand la lettre "l"
 - Entrez l'url de la page du livre

### Phase 2 
 - Choississez si vous voulez scrapper un livre en indiquand la lettre "l" ou une categorie avec "c"
 - Entrez l'url de la page du livre pour "l" ou l'url de la page de la catégorie pour "c".Attention certaines catégories peuvent contenir plusieurs page: toujours prendre l'url de la première page. 

 ### Phase 3 
 - Choississez si vous voulez scrapper un livre en indiquand la lettre "l", une categorie avec "c" ou le site avec la lettre "s"

 ### Phase 4 
 - Les images sont enregistrées dans un dossier "Pictures" à la racine du projet
