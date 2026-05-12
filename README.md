# Yams Tournament : La Quete de la "Chance du Debutant"

Bienvenue dans ce laboratoire d'experimentation probabiliste. Ce projet est ne 
d'une frustration universelle : pourquoi les gens qui ne comprennent rien aux 
regles gagnent-ils toujours au Yams ?

Ici, on ne se contente pas de rager, on simule. Ce logiciel est un moteur de 
jeu complet en Python, dote d'une interface graphique "Industrial Dark" et 
d'un framework de tournoi permettant d'opposer des humains, des algorithmes 
gloutons et des IA locales.

## La Problematique
Est-ce que la "chance du debutant" existe ? Pour le savoir, j'ai cree plusieurs 
profils de joueurs (Agents) respectant une interface commune et je les ai fait 
s'affronter sur des milliers de parties.

### Les Combattants :
* L'Expert : Analyse les opportunites de suites et de combinaisons rares.
* Le Glouton (Greedy) : Maximise le score immediat et regroupe les des par 
  valeur majoritaire.
* Le Debutant : Strategie polyvalente simulant un comportement moins cible.
* Le Hasard (Random) : Effectue des choix purement aleatoires pour les des et 
  les categories.
* L'IA (Phi-3-Mini via Ollama) : Decisions deleguees a un modele de langage 
  local via des prompts.

## Les Resultats (Le Verdict de la Data)
Apres des tournois massifs orchestres par le Tournament Manager, 
les chiffres sont tombes :

+-----------------------+-----------------------+-----------------------------+
| Confrontation         | Resultat              | Explication                 |
+-----------------------+-----------------------+-----------------------------+
| Expert vs Debutant    | Victoire Debutant     | L'Expert sacrifie trop de   |
|                       | (56.4%)               | points de suites en visant  |
|                       |                       | uniquement le Yams.         |
+-----------------------+-----------------------+-----------------------------+
| IA (Phi-3) vs Debutant| Defaite Totale        | L'IA gere mal les regles de |
|                       | (0% de win)           | calcul et                   |
|                       |                       | hallucine parfois ses des.  |
+-----------------------+-----------------------+-----------------------------+

Note sur les LLM : L'agent LLM utilise subprocess pour communiquer avec 
Ollama. Pour des resultats probants, des modeles plus massifs seraient 
necessaires.

## Stack Technique
* Coeur : Gestion des 5 des et des 3 lancers (game.py).
* Scoring : Calcul des 13 categories standard (scoring.py).
* GUI : PySide/PyQt avec scoreboard et panneau de probabilites.
* Data : Persistance via SQLite et export CSV (storage/ scripts/).

## Installation & Test
1. Installez les dependances : pip install -r requirements.txt
2. Lancez l'interface : python app.py
3. Admirez vos statistiques s'effondrer.

-------------------------------------------------------------------------------
Projet realise pour l'exercice, le plaisir, et pour enfin avoir une preuve 
mathematique a montrer a tous ceuxx qui gagnent ...
===============================================================================