from machine import Pin, ADC
import neopixel
import utime
import random

# --- Initialisation du matériel ---
MIC_PIN = 1          #  ADC=1
LED_PIN = 18          # GP18 = signal de données NeoPixel
N_LEDS = 1            # nombre de LED NeoPixel (1 si module unique)

mic = ADC(MIC_PIN)
led = neopixel.NeoPixel(Pin(LED_PIN), N_LEDS)

# --- Paramètres de détection ---
SEUIL = 20000         # seuil de déclenchement
TEMPS_MIN = 150       # délai minimal entre deux battements (ms)
dernier_temps = utime.ticks_ms()

# --- Fonction : couleur aléatoire ---
def couleur_aleatoire():
    
    return (
        random.randint(0, 255),  # rouge
        random.randint(0, 255),  # vert
        random.randint(0, 255)   # bleu
    )

# --- Boucle principale ---

print("🎶 Démarrage du programme de détection musicale avec NeoPixel 🎶")

while True:
    val = mic.read_u16()  # lecture du signal sonore

    # Détection de pic sonore (battement)
    
    if val > SEUIL and utime.ticks_diff(utime.ticks_ms(), dernier_temps) > TEMPS_MIN:
        dernier_temps = utime.ticks_ms()

        # Choisir une couleur aléatoire
        
        color = couleur_aleatoire()
        led[0] = color
        led.write()

        print(f"🎵 Battement détecté → Couleur : {color}")

    else:
        
        # LED légèrement allumée entre deux battements
        
        led[0] = (5, 5, 5)
        led.write()

    utime.sleep(0.01)
