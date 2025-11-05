from machine import Pin, ADC
import neopixel
import utime
import random

# --- Initialisation du matériel ---
MIC_PIN = 1       # Entrée analogique du micro
LED_PIN = 18       # Broche NeoPixel
N_LEDS = 1         # Nombre de LED NeoPixel (1 dans ton cas)

mic = ADC(MIC_PIN)
led = neopixel.NeoPixel(Pin(LED_PIN), N_LEDS)

# --- Paramètres de détection ---
SEUIL = 20000       # sensibilité du micro
TEMPS_MIN = 150     # ms entre deux battements
dernier_temps = utime.ticks_ms()

# --- Variables BPM ---
battements = []            # liste d'instants (ms)
bpm_moyenne = []           # moyenne par minute
temps_debut_minute = utime.ticks_ms()

# --- Couleurs ---
def couleur_aleatoire():
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )

# --- Calcul BPM instantané ---
def calcul_bpm(battements):
    if len(battements) < 2:
        return 0
    deltas = [battements[i+1] - battements[i] for i in range(len(battements)-1)]
    moyenne = sum(deltas) / len(deltas)  # moyenne des intervalles (ms)
    bpm = 60000 / moyenne  # conversion en battements par minute
    return round(bpm, 1)

# --- Écriture du BPM moyen dans un fichier ---
def ecrire_bpm_moyen(bpm_moyen):
    try:
        with open("bpm_log.txt", "a") as f:
            t = utime.localtime()
            horodatage = f"{t[3]:02d}:{t[4]:02d}:{t[5]:02d}"
            f.write(f"{horodatage} - BPM moyen : {bpm_moyen}\n")
        print(f"📝 Fichier mis à jour : {bpm_moyen} BPM à {horodatage}")
    except Exception as e:
        print("⚠️ Erreur d’écriture :", e)

# --- Boucle principale ---
print("🎶 Démarrage : détection musicale et calcul BPM 🎶")

while True:
    val = mic.read_u16()

    # Détection d’un battement
    if val > SEUIL and utime.ticks_diff(utime.ticks_ms(), dernier_temps) > TEMPS_MIN:
        maintenant = utime.ticks_ms()
        battements.append(maintenant)
        dernier_temps = maintenant

        # Couleur aléatoire
        color = couleur_aleatoire()
        led[0] = color
        led.write()

        # Calcul BPM instantané
        bpm_instant = calcul_bpm(battements)
        print(f"🎵 Battement détecté | Couleur: {color} | BPM ≈ {bpm_instant}")

    else:
        led[0] = (5, 5, 5)
        led.write()

    # Chaque minute, calcul moyenne et écriture
    if utime.ticks_diff(utime.ticks_ms(), temps_debut_minute) > 60000:
        bpm_moyen = calcul_bpm(battements)
        bpm_moyenne.append(bpm_moyen)
        ecrire_bpm_moyen(bpm_moyen)
        battements.clear()  # réinitialise pour la minute suivante
        temps_debut_minute = utime.ticks_ms()

    utime.sleep(0.01)
