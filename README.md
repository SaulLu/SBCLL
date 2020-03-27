# Vampires vs Loups Garous - Groupe 1

Ce projet consiste en l'implémentation d'une IA pouvant jouer au jeu "Vampires vs Loups Garous" en utilisant plusieurs stratégies différentes.

## Mode d'emploi de l'IA

Pour jouer : 
1. Lancer le serveur du jeu.
2. Exécuter le fichier "player.py" (au niveau de la racine du projet) avec les paramètres suivants : 
    * -n : le nom du joueur (par défaut, pioche le nom du joueur dans le fichier de config du jeu) ;
    * -s : la stratégie utilisée - toutes les stratégie décrite en partie 3 sont disponibles (par défaut, utilise la stratégie "random") ;
    * -he : l'heuristique utilisée - toutes les heuristiques décrites en partie 3 sont disponibles (par défaut, utilise l'heuristique "naive").
3. Les étapes importantes sont décrites dans la console et un fichier de log est créé.

## Structure du code

--- **connector** : *le code relatif au serveur client*
    |   --- **client.py** : *le client et ses fonctions d'interaction* 
    |   --- **config.json** : *la config client*
    |   --- **connect.py** : *les fonctions pour encrypter / décrypter les commandes à envoyer / reçues par le client* 
--- **cpp \ target_module** : *module de calcul pour les stratégies de target en C++*
    |   --- **target_module_v1**
    |   --- **target_module.sln**
--- **models** : *les classes du jeu et les machines de calcul*
    |   --- **battle_engine.py** : *fonctions de calculs des issues (espérances) des batailles aléatoires*
    |   --- **board.py** : *classe pour décrire le plateau de jeu*
    |   --- **cell.py** : *classe pour décrire une case du plateau de jeu*
    |   --- **check_engine.py** : *fonctions de vérifications intermédiaires*
    |   --- **engine.py** : *fonctions de calcul de base sur le plateau de jeu*
    |   --- **mov.py** : *classe pour décrire un mouvement dans le jeu, tel qu'attendu par la commande MOV*
    |   --- **target_engine.py** : *fonctions de calcul pour les stratégies de target*
--- **strategies** : *les stratégies et heuristiques*
    |   --- **abstract_strategy.py** *classe abstraite pour décrire une stratégie*
    |   --- **alpha_beta.py** : *classe pour calculer le meilleur prochain coup selon alpha-beta* 
    |   --- **heuristics.py** : *les heuristiques pour calculer le score d'un plateau*
    |   --- **next_best_strategy.py** : *l'une des classes implémentant une stratégie*
    |   --- **random_strategy.py** : *l'une des classes implémentant une stratégie*
    |   --- **random_target_strategy.py** : *l'une des classes implémentant une stratégie* 
    |   --- **random_walk_strategy.py** : *l'une des classes implémentant une stratégie*
    |   --- **target_strategy_v2.py** : *l'une des classes implémentant une stratégie*
    |   --- **target_strategy.py** : *l'une des classes implémentant une stratégie*
    |   --- **target_walk_strategy.py** : *l'une des classes implémentant une stratégie* ???????
--- **.gitignore**
--- **config.json** : *la config du jeu*
--- **heuristics_tests.py** : *l'un des fichiers de tests*
--- **module_tests.py** : *l'un des fichiers de tests*
--- **parameters.py** : *les paramètres du jeu*
--- **player.py** : *le code relatif au joueur, gère l'interaction client et utilise une stratégie donnée* 
--- **README.md**
--- **speed_test.py** : *l'un des fichiers de tests*
--- **tests.py** : *l'un des fichiers de tests*

## Algorithmes, stratégies et heuristiques

### Heuristiques
Toutes les heuristiques sont présentées dans le fichier `heuristics.py`.

#### naive
Calcule la différence entre le nombre de nos créatures et le nombre de créatures adverses (ne prend pas en compte les humains).
#### target_diff
Calcule ???

### Alpha-bêta
Nous proposons notre propre implémentation du principe alpha-bêta dans le fichier `alpha_beta.py`, sous forme d'une classe. Cette classe a pour attributs :
* la profondeur maximale que nous souhaitons atteindre ;
* la méthode permettant de calculer à partir d'un plateau ses noeuds fils ;
* l'heuristique permettant d'attribuer un score à chaque plateau ;
* des attributs permettant de calculer si l'on effectue un time-out avant d'atteindre la profondeur souhaitée pour chaque branche ; 
Parmi ces derniers attributs, `timed_out` peut être utilisé au sein d'une stratégie pour adapter la profondeur maximale entre chaque tour. Il est intéressant d'adapter cette profondeur maximale car en cas de time-out, certaines branches ne sont pas du tout explorées à la même profondeur que celles pour lesquelles on avait encore le temps ; éviter le timeout permet une exploration équilibrée et donc plus juste.
Notons que chaque fils d'un plateau est un noeud obtenu à partir d'une liste d'objets "mov", qui mène à plusieurs plateaux possibles associés à des probabilités (en fonction des batailles aléatoires). Le score d'un tel noeud est la somme des multiplications du score de chaque plateau fils et de la probabilité d'apparition dudit plateau.

En plus de l'élagage inhérent au principe d'alpha-bêta, et de celui éventuellement présent dans le calcul des noeuds fils (dépendant de la stratégie), nous avons rajouté un troisième moment d'élagage, à l'aide de la méthode `nodes_pruning`. Cette méthode prend place juste après le calcul des noeuds fils, et supprime les noeuds dont l'heuristique est trop éloignée du meilleur noeud fils.

### Stratégies
Toutes les stratégies découlent de la classe abstraite `Strategy`. Cette classe abstraite contient une méthode permettant de mettre le plateau à jour déjà implémentée, et une méthode `next_moves` décidant du prochain coup du joueur selon le plateau actuel à overrider.

#### random
Cette stratégie choisit pour chaque cellule un coup aléatoire parmi tous les coups légaux ; elle prend bien garde à bouger au moins une créature.
#### random_walk
Cette stratégie calcule tous les coups (liste de "mov") possibles à partir du plateau actuel. Elle calcule ensuite des marches aléatoires de profondeur 5 pour chacun de ces coups tant qu'elle a du temps. Enfin, elle choisit le coup menant le plus probablement à des plateaux ayant une bonne heuristique.
#### next_best
Cette stratégie calcule tous les coups possibles à partir du plateau actuel et les plateaux résultants. Elle calcule l'heuristique de chaque plateau et choisit le coup menant au meilleur plateau.
#### target
Cette stratégie utilise un arbre de décision alpha-bêta. Les fils d'un plateau donné sont calculés à l'aide de fonctions calculant :
* Pour chacune de nos cases, les cases adverses (humaines ou de l'autre type de créature) pouvant être attaquées sans risques. Ces cases adverses sont les targets potentielles de chacune de nos cases.
* Pour le plateau, toutes les combinaisons possibles d'attributions de nos cases vers des targets potentielles (en prenant en compte le fait qu'une case puisse se diviser en plusieurs, ou que deux cases peuvent fusionner si aucune target adverse n'est possible).
* Pour chaque combinaison nos  cases / targets potentielles, la prochaine listes de "mov" que nous devons faire pour avancer vers les-dites targets. 
Ce calcul de fils élague donc tous les coups ne nous dirigeant pas vers des targets potentielles.
#### target2
Cette stratégie agit selon les mêmes principes que la précédentes. Seulement, les fonctions de calcul des target, de leurs attributions et des "mov" correspondant se fait grâce à un module en C++ que nous avons créé, afin de gagner du temps.

