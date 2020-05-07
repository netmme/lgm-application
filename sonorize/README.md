# sonorize

## Concept

S'amuse avec la lecture de sons et le random en shell.

### Utilisation hors hook

Exempl d'utilisation depuis le dossier ./sonorize:

#### Lister les catégories

`./sonorize .. listCategories`

#### Lister les catgories des sons

`./sonorize .. listTypes <category>`

#### Jouer un son

`./sonorize .. playSound <category> <type>`

Le chemin à indiquer est un peu étrange comme pratique mais c'était
pour me simplifier la tâche lors de l'appel du script par un git hook.

## Remarques

C'était drôle. Totalement inutile mais une fois combiné au git-hook on obtient un
niveau de fun jamais atteint à ce jour.

### Changements effectués

* Les modulos ne sont pas magique et la solution proposée dans l'article
ne donnait pas une distribution uniforme. J'ai préféré utilisé ce cher
urandom à la place.
* Le mp3 est fichier plus courrant et newbie donc j'ai préféré ce format
pour les fichiers audios.
