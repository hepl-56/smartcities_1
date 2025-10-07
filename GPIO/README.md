#  Exercice 1 – Clignotement de LED avec bouton poussoir

##  Objectif:
Créer un programme **MicroPython** qui permet de faire clignoter une LED à différentes vitesses en fonction du **nombre de pressions sur un bouton poussoir**.
---

##  Matériel nécessaire
-  Microcontrôleur  compatible avec Microphython: **Raspberry Pi Pico**
-  Module LED
- Bouton poussoir
- Câbles
- Logiciel Thonny pour la programmation

---

## Schéma de branchement (exemple)

| Composant | Broche Pico | Type de broche |
|------------|--------------|----------------|
| LED        | D16          | Entrée/Sortie (OUT)   |
| Bouton     |  D20         | Entrée (IN) avec `Pin.PULL_DOWN` |

---

## Code source

Le programme est disponible dans le document code sur la page d'accueil.

Ce programme  permet :
- de **faire clignoter la LED à 0,5 Hz** après un premier appui,  
- de **faire clignoter plus rapidement** après un deuxième appui,  
- et **d’éteindre la LED** après un troisième appui.

Le cycle recommence automatiquement ensuite.

---

##  Fonctionnement
1. Appuie **une fois** → LED clignote lentement.  
2. Appuie **deux fois** → LED clignote rapidement.  
3. Appuie **trois fois** → LED s’éteint.  
4. Appuie **encore une fois** → retour au premier mode.  

---

##  Auteur
Projet réalisé dans le cadre de l’**Exercice 1 – MicroPython**  
HEPL — Projet Smartcitie 
*[hepl56]*  
