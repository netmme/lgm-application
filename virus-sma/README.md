# virus-sma

## Concept

Faire un programme à cheval entre un jeu de la vie et une simulation de virus.

## Observations

Il y avait BEAUCOUP de choses dans la classe World et le fichier est bien trop
long et pas du tout atomique. La gestion de la grille est mauvaise puisqu'elle
demande d'être éditée deux fois (une fois avec map et une fois avec
agents_position). Les constantes ne sont pas forcément à leur place. Bref,
vraiment pas agréable à prendre en main mais le résultat reste amusant.

### Changments effectués

* Plutôt que de logger comme une brute, j'ai utilisé la bibliothèque logging.
* Utilisation de argparse pour donner les paramètres de la simulation plutôt
que d'éditer le main à chaque fois.
* Séparation des classe : le monde, le logger et le statter
* Les humains soignés restent dans la simulation. C'est un facteur très
important car les immunisés gênent les déplacements de malade mais ne
transmettent pas la maladie.

### Chantier abandonné

* Tout le monde se déplace aléatoirement, les malades ne vont pas vers les
hopitaux.

## Référence

GLM N°236 Avril 2020

Auteur de l'article: Tristan Colombo
