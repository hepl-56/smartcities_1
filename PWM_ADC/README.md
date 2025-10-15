#  Exercice 2 — Volume d'une mélodie

##  Objectif
Créer un programme MicroPython permettant de gérer le volume d'une mélodie jouée sur un buzzer. Le volume est contrôlé par un potentiomètre.

---

##  Matériel requis
- Microcontrôleur compatible MicroPython (**Raspberry Pi Pico**)
- Module potentiomètre
- Buzzer
- LED 
- Bouton poussoir 
- Câbles de connexion

---

##  Consigne de travail

### Version de base
1. Branchez le buzzer et le potentiomètre au microcontrôleur
2. Écrivez un programme MicroPython qui répond aux exigences suivantes :
   - Une mélodie (au choix, soyez créatif) est jouée en boucle
   - Le fait de changer le potentiomètre modifie directement le volume de la mélodie
3. Testez votre programme et vérifiez qu'il fonctionne correctement

### Bonus
- **Bonus 1** : Ajoutez un bouton poussoir qui permet de changer de mélodie
- **Bonus 2** : Ajoutez une LED qui clignote au rythme de la mélodie

---

##  Montage

### Schéma de câblage - Version de base

```
Raspberry Pi Pico
┌─────────────────────┐
│                     │
│  I2C0 ──── Potentiomètre (Signal)
│
│                     │
│  D20(VCC) ──── Buzzer (+)
│  GND ───────────── Buzzer (-)
│                     │
└─────────────────────┘
```

### Schéma complet avec Bonus

```
Raspberry Pi Pico
┌─────────────────────┐
│                     │
│I2C0 ──── Potentiomètre (Signal)
│                     │
│  D20 ──── Buzzer (+)
│  GND ───────────── Buzzer (-)
│                     │
│  D18 ────────── LED 
│                     │
│  D16 ──── Bouton ── GND (Bonus 1)
│                     │
└─────────────────────┘
```


**📸 Insérer une image du montage physique ici**
<img width="444" height="640" alt="image" src="https://github.com/user-attachments/assets/a31e29de-a4f1-4cae-b148-be367c10dd3b" />

---

##  Code

Les codes sont disponibles dans le dossier **`CODE`** de ce dépôt :


```

### 🔗 Liens directs vers les codes

- **[Version de base](code_python/exercice2_base.py)** - Contrôle du volume avec potentiomètre
- **[Bonus 1 : Changement de mélodie](code_python/exercice2_bonus1.py)** - Ajout du bouton pour changer de mélodie
- **[Bonus 2 : LED rythmique](code_python/exercice2_bonus2.py)** - LED qui clignote au rythme de la musique

---

## ⚙️ Fonctionnement du programme

### Version de base
En faisant varier l'angle de rotation du potentiomètre, le volume de la note musicale varie également. La valeur du volume de la mélodie est fonction de la valeur de l'angle de rotation du potentiomètre.

**Mélodie jouée :** "Joyeux Anniversaire"

**Caractéristiques techniques :**
- Lecture du potentiomètre : `ROTARY_ANGLE_SENSOR.read_u16()` (valeurs 0-65535)
- Volume : Limité à 50% du maximum pour protéger le buzzer
- Contrôle en temps réel : Le volume est lu à chaque note

### Bonus 1 - Changement de mélodie
**Même fonctionnement que la version de base** +

Appuyez sur le bouton poussoir pour cycler entre **3 mélodies** :
1. **Joyeux Anniversaire** - Classique festif
2. **Frère Jacques** - Comptine française
3. **Mario Bros** - Thème du jeu vidéo emblématique

**Fonctionnalités supplémentaires :**
- Système anti-rebond (debouncing) de 300ms pour éviter les pressions multiples
- Détection de front montant : réagit uniquement lors de l'appui
- Affichage du nom de la mélodie dans la console
- Le bouton est vérifié pendant la lecture de la mélodie

### Bonus 2 - LED rythmique
**Même fonctionnement que la version de base** +

La LED s'allume et s'éteint au rythme de la musique :
- **LED allumée** : Pendant chaque note jouée
- **LED éteinte** : Pendant les silences et pauses
- **Effet de démarrage** : 3 clignotements rapides au lancement
- **Effet de transition** : 3 clignotements entre chaque répétition de la mélodie

---

## Tests et validation

###  Test de base
**Test du potentiomètre** :
- **Tourner le potentiomètre dans le sens des aiguilles d'une montre** : le volume de la mélodie augmente
- **Tourner le potentiomètre dans le sens contraire des aiguilles d'une montre** : le volume diminue
- À volume minimum : la mélodie est à peine audible ou silencieuse
- À volume maximum : la mélodie est clairement audible (50% du duty cycle)

###  Tests Bonus 1
**Test du changement de mélodie** :
- **Premier appui** sur le bouton : passage à "Frère Jacques"
- **Deuxième appui** : passage à "Mario Bros"
- **Troisième appui** : retour à "Joyeux Anniversaire"
- Le volume reste contrôlable pendant tous les changements
- Message affiché dans la console à chaque changement

### Tests Bonus 2
**Test de la LED** :
- La LED clignote en **synchronisation parfaite** avec chaque note
- La LED reste **éteinte** pendant les silences
- Les **effets visuels** (démarrage et transitions) fonctionnent correctement
- Le volume reste contrôlable pendant le clignotement de la LED

---

##  Concepts MicroPython utilisés

### Version de base
- **PWM (Pulse Width Modulation)** : Pour générer les fréquences sonores du buzzer
- **ADC (Analog to Digital Converter)** : Pour lire la valeur analogique du potentiomètre
- **Gestion du temps** : `time.sleep_ms()` pour contrôler la durée des notes
- **Boucles infinies** : `while True` pour jouer la mélodie en continu
- **Listes de tuples** : Pour stocker les notes (fréquence, durée)

- **GPIO Digital Output** : Pour contrôler la LED
- **Synchronisation** : Coordination entre le buzzer et la LED
- **Effets visuels** : Boucles pour créer des patterns de clignotement

---

### Fréquences des notes (en Hz)

| Note | Octave 3 | Octave 4 | Octave 5 |
|------|----------|----------|----------|
| Do (C) | 131 | 262 | 523 |
| Ré (D) | 147 | 294 | 587 |
| Mi (E) | 165 | 330 | 659 |
| Fa (F) | 175 | 349 | 698 |
| Sol (G) | 196 | 392 | 784 |
| La (A) | 220 | 440 | 880 |
| Si (B) | 247 | 494 | 988 |

### Format des mélodies

```python
# Format: (fréquence_Hz, durée_ms)
melodie = [
    (262, 500),  # Do pendant 500ms
    (294, 500),  # Ré pendant 500ms
    (330, 500),  # Mi pendant 500ms
    (0, 200),    # Silence de 200ms
]
```



## 👨‍💻 Auteur

Projet réalisé par **Elvira Nganne**  
Dans le cadre du cours de **MicroPython / Raspberry Pi Pico**

