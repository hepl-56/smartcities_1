from machine import Pin, PWM, ADC
import time

# Configuration des broches
buzzer = PWM(Pin(20))  # Buzzer 
potentiometre = ADC(1)  # Potentiomètre 
led = Pin(18, Pin.OUT)  # LED 
bouton = Pin(16, Pin.IN, Pin.PULL_DOWN)  # Bouton 

# Variables globales
melodie_actuelle = 0
bouton_precedent = 0
debounce_time = 0

# Définition des mélodies (fréquences en Hz et durées en ms)
# Mélodie 1: "Joyeux Anniversaire"
melodie1 = [
    (262, 400), (262, 400), (294, 800), (262, 800),  # Do Do Ré Do
    (349, 800), (330, 1600),                          # Fa Mi
    (262, 400), (262, 400), (294, 800), (262, 800),  # Do Do Ré Do
    (392, 800), (349, 1600),                          # Sol Fa
]

# Mélodie 2: "Frère Jacques"
melodie2 = [
    (262, 500), (294, 500), (330, 500), (262, 500),  # Do Ré Mi Do
    (262, 500), (294, 500), (330, 500), (262, 500),  # Do Ré Mi Do
    (330, 500), (349, 500), (392, 1000),             # Mi Fa Sol
    (330, 500), (349, 500), (392, 1000),             # Mi Fa Sol
]

# Mélodie 3: "Mario Bros"
melodie3 = [
    (659, 150), (659, 150), (0, 150), (659, 150),    # Mi Mi _ Mi
    (0, 150), (523, 150), (659, 300),                # _ Do Mi
    (784, 300), (0, 300),                            # Sol _
    (392, 300), (0, 300),                            # Sol grave _
]

melodies = [melodie1, melodie2, melodie3]
noms_melodies = ["Joyeux Anniversaire", "Frère Jacques", "Mario Bros"]

def lire_volume():
    """Lit la valeur du potentiomètre et retourne le duty cycle (0-65535)"""
    valeur = potentiometre.read_u16()  # Valeur de 0 à 65535
    # Mapping: 0-65535 -> 0-32768 (volume max à 50% pour protéger le buzzer)
    return valeur // 2

def gerer_bouton():
    """Change de mélodie à chaque pression du bouton"""
    global melodie_actuelle, bouton_precedent, debounce_time
    
    bouton_actuel = bouton.value()
    temps_actuel = time.ticks_ms()
    
    if bouton_actuel == 1 and bouton_precedent == 0:
        if time.ticks_diff(temps_actuel, debounce_time) > 300:
            melodie_actuelle = (melodie_actuelle + 1) % len(melodies)
            print(f"Mélodie: {noms_melodies[melodie_actuelle]}")
            debounce_time = temps_actuel
    
    bouton_precedent = bouton_actuel

def jouer_note(frequence, duree, volume):
    """Joue une note avec le volume spécifié"""
    if frequence > 0:
        buzzer.freq(frequence)
        buzzer.duty_u16(volume)
        led.value(1)  # Allume la LED pendant la note
    else:
        buzzer.duty_u16(0)  # Silence
        led.value(0)  # Éteint la LED pendant le silence
    
    time.sleep_ms(duree)
    
    # Petite pause entre les notes (10% de la durée)
    buzzer.duty_u16(0)
    led.value(0)
    time.sleep_ms(duree // 10)

def jouer_melodie():
    """Joue la mélodie sélectionnée avec le volume du potentiomètre"""
    melodie = melodies[melodie_actuelle]
    
    for frequence, duree in melodie:
        # Lire le volume à chaque note pour un contrôle en temps réel
        volume = lire_volume()
        jouer_note(frequence, duree, volume)
        
        # Vérifier le bouton pendant la mélodie
        gerer_bouton()

# Programme principal

print("=" * 50)
print("\nCommandes:")
print("- Tournez le potentiomètre pour ajuster le volume")
print("- Appuyez sur le bouton pour changer de mélodie")
print(f"\nMélodie actuelle: {noms_melodies[melodie_actuelle]}")
print("\nDémarrage...\n")

try:
    while True:
        jouer_melodie()
        time.sleep_ms(500)  # Pause entre les répétitions
        gerer_bouton()  # Vérifier le bouton pendant la pause
        
except KeyboardInterrupt:
    print("\n\nProgramme arrêté")
    buzzer.duty_u16(0)
    buzzer.deini