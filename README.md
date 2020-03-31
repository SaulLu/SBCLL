# Vampires vs Loups Garous - Groupe 1

Ce projet consiste en l'implémentation d'une IA pouvant jouer au jeu "Vampires vs Loups Garous" en utilisant plusieurs stratégies différentes.

## Mode d'emploi de l'IA

Pour installer l'IA
1. Cloner ce repository
2. Dans un terminal, lancer la commande `python setup.py build_ext --inplace` dans le dossier `SBCLL\cpp\target_module\target_module_v1`

Pour jouer : 
1. Lancer le serveur du jeu.
2. Exécuter le fichier "player.py" (au niveau de la racine du projet) avec les paramètres suivants: `python player.py -s target2 -he target_diff`
3. Les étapes importantes sont décrites dans la console.

Bonus, dans le terminal, il est possible de choisir pour "player.py":
```
    -n : le nom du joueur (par défaut, pioche le nom du joueur dans le fichier de config du jeu);
    -s : la stratégie utilisée - toutes les stratégie décrite en partie 3 sont disponibles (par défaut, utilise la stratégie "random");
    -he : l'heuristique utilisée - toutes les heuristiques décrites en partie 3 sont disponibles (par défaut, utilise l'heuristique "naive").
```

## Structure du code

<pre>
│
├── <b>connector</b> : <i>le code relatif au serveur client</i>
│   ├── <b>client.py</b> : <i>le client et ses fonctions d'interaction</i> 
│   ├── <b>config.json</b> : <i>la config client</i>
│   ├── <b>connect.py</b> : <i>les fonctions pour encrypter / décrypter les commandes à envoyer / recevoir par le client</i> 
├──  <b>cpp \ target_module</b> : <i>module de calcul pour les stratégies de target en C++</i>
│   ├── <b>target_module_v1</b>
│   ├── <b>target_module.sln</b>
├──  <b>models</b> : <i>les classes du jeu et les machines de calcul</i>
│   ├── <b>battle_engine.py</b> : <i>fonctions de calculs des issues (espérances) des batailles aléatoires</i>
│   ├── <b>board.py</b> : <i>classe pour décrire le plateau de jeu</i>
│   ├── <b>cell.py</b> : <i>classe pour décrire une case du plateau de jeu</i>
│   ├── <b>check_engine.py</b> : <i>fonctions de vérifications intermédiaires</i>
│   ├── <b>engine.py</b> : <i>fonctions de calcul de base sur le plateau de jeu</i>
│   ├── <b>mov.py</b> : <i>classe pour décrire un mouvement dans le jeu, tel qu'attendu par la commande MOV</i>
│   ├── <b>target_engine.py</b> : <i>fonctions de calcul pour les stratégies de target</i>
├──  <b>strategies</b> : <i>les stratégies et heuristiques</i>
│   ├── <b>abstract_strategy.py</b> : <i>classe abstraite pour décrire une stratégie</i>
│   ├── <b>alpha_beta.py</b> : <i>classe pour calculer le meilleur prochain coup selon alpha-beta</i> 
│   ├── <b>heuristics.py</b> : <i>les heuristiques pour calculer le score d'un plateau</i>
│   ├── <b>next_best_strategy.py</b> : <i>l'une des classes implémentant une stratégie</i>
│   ├── <b>random_strategy.py</b> : <i>l'une des classes implémentant une stratégie</i>
│   ├── <b>random_target_strategy.py</b> : <i>l'une des classes implémentant une stratégie</i> 
│   ├── <b>random_walk_strategy.py</b> : <i>l'une des classes implémentant une stratégie</i>
│   ├── <b>target_strategy_v2.py</b> : <i>l'une des classes implémentant une stratégie</i>
│   ├── <b>target_strategy.py</b> : <i>l'une des classes implémentant une stratégie</i>
│   ├── <b>target_walk_strategy.py</b> : <i>l'une des classes implémentant une stratégie</i>
├── <b>.gitignore</b>
├── <b>config.json</b> : <i>la config du jeu</i>
├── <b>heuristics_tests.py</b> : <i>l'un des fichiers de tests</i>
├── <b>module_tests.py</b> : <i>l'un des fichiers de tests</i>
├── <b>parameters.py</b> : <i>les paramètres du jeu</i>
├── <b>player.py</b> : <i>le code relatif au joueur, gère l'interaction client et utilise une stratégie donnée</i> 
├── <b>README.md</b>
├── <b>speed_test.py</b> : <i>l'un des fichiers de tests</i>
├── <b>stat_test.py</b> : <i>l'un des fichiers de tests</i>
└── <b>tests.py</b> : <i>l'un des fichiers de tests</i>
</pre>

## Algorithmes, stratégies et heuristiques

### Heuristiques
Toutes les heuristiques sont présentées dans le fichier `heuristics.py`.

#### a. naive
Calcule la différence entre le nombre de nos créatures et le nombre de créatures adverses (ne prend pas en compte les humains).
#### b. target_diff
Se base sur sur l'heuristique naive mais ajoute un terme qui prend en compte les potentialités de chaque case de créature. Pour chaque case de créature, on somme toutes les créatures qu'elle peux absorber ou détruire instantanément, pondéré par le carré de l'inverse de la distance qui les sépare. Ce terme est ajouté pour nos créatures et soustrait pour les créatures adverses.

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

#### a. random
Cette stratégie choisit pour chaque cellule un coup aléatoire parmi tous les coups légaux ; elle prend bien garde à bouger au moins une créature.
Attention, cette dernière n'est à utiliser que sur des boards simples.
#### b. random_walk
Cette stratégie calcule tous les coups (liste de "mov") possibles à partir du plateau actuel. Elle calcule ensuite des marches aléatoires de profondeur 5 pour chacun de ces coups tant qu'elle a du temps. Enfin, elle choisit le coup menant le plus probablement à des plateaux ayant une bonne heuristique.
#### c. next_best
Cette stratégie calcule tous les coups possibles à partir du plateau actuel et les plateaux résultants. Elle calcule l'heuristique de chaque plateau et choisit le coup menant au meilleur plateau.
Attention, cette dernière n'est à utiliser que sur des boards simples.
#### d. target
Cette stratégie utilise un arbre de décision alpha-bêta. Les fils d'un plateau donné sont calculés à l'aide de fonctions calculant :
* Pour chacune de nos cases, les cases adverses (humaines ou de l'autre type de créature) pouvant être attaquées sans risques. Ces cases adverses sont les targets potentielles de chacune de nos cases.
* Pour le plateau, toutes les combinaisons possibles d'attributions de nos cases vers des targets potentielles (en prenant en compte le fait qu'une case puisse se diviser en plusieurs, ou que deux cases peuvent fusionner si aucune target adverse n'est possible).
* Pour limiter l'explosion combinatoire, on limite le nombre de targets par angle de vue pour chacune des cases attaquantes. Par exemple pour chaque cône de 30°, l'attaquant retiendra seulement la target la plus proche dans ce cône. Nous partons du principe que pour aller chercher une target ignorée par cette règle, il faut déja avancer vers la target retenue.
* Pour chaque combinaison de nos targets potentielles, la prochaine listes de "mov" que nous devons faire pour avancer vers les-dites targets en essayant d'emprunter le chemin le plus court entre la case initiale et celle de la target et en allant uniquement sur des cases disponibles (ie, la case d'arrivée ne peut pas être une case occupée par notre créature ou par un humain ou l'adversaire si ce n'est pas la target).
Ce calcul de fils élague donc tous les coups ne nous dirigeant pas vers des targets potentielles.
#### e. target2
Cette stratégie agit selon les mêmes principes que la précédentes. Seulement, les fonctions de calcul des target, de leurs attributions se fait grâce à un module en C++ que nous avons créé, afin de gagner du temps.
#### f. target_walk
Cette stratégie est un mélange entre target_walk et target. On utilise un alpha_bêta comme dans target mais les noeuds fils sont tirés aléatoirements. On a alors seulement un échantillon des fils disponibles. Cette stratégie privilégie la profondeur d'exlploration à l'exactitude des scores attribués à chaque noeuds de l'arbre. Elle n'explore aussi qu'une partie des branches, certaines n'étant pas tirées par le hasard

