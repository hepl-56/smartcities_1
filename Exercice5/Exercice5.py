import network
import time
import ntptime
from machine import Pin, PWM

# --- Connexion à internet ---
SSID = "nom_du_WIFI"
PASSWORD = "mot de passe"


wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(1)
wlan.active(True)

print(f"Connexion à: {SSID}")
wlan.connect(SSID, PASSWORD)

# Attente de la connexion
for i in range(20):
    status = wlan.status()
    if status == 3:
        print("✓ CONNECTÉ!")
        print("IP:", wlan.ifconfig()[0])
        break
    elif status < 0:
        print(f"✗ Échec - Statut: {status}")
        print("→ Vérifie ton mot de passe Wi-Fi")
        break
    elif status == 1:
        print(".", end="")
    time.sleep(0.5)

# --- Récupération de l'heure actuelle sur internet ---
# --- Récupération de l'heure actuelle sur internet ---
try:
    print("\nSynchronisation avec le serveur NTP...")
    ntptime.host = "pool.ntp.org"
    ntptime.settime()  # Met à jour l'heure interne du Pico (UTC)
    print("Heure synchronisée avec Internet !")

except Exception as e:
    print("Erreur NTP :", e)

# --- Fonction pour fuseau horaire (doit être en dehors du try/except) ---
TZ_OFFSET = 1  # Fuseau horaire (Belgique)
def heure_locale(offset):
    t = time.time() + offset * 3600
    return time.localtime(t)

# Récupération et affichage unique
t = heure_locale(TZ_OFFSET)
print("Heure locale actuelle : %02d:%02d:%02d" % (t[3], t[4], t[5]))
print("Date locale actuelle  : %02d/%02d/%04d" % (t[2], t[1], t[0]))

## calcule de l'angle du servo Moteur
def calcul_angle(heure):
    """Retourne l'angle correspondant à une heure sur 12h (0° à 180°)."""
    angle = (heure % 12) * 15  # 180° / 12 = 15° par heure
    return angle

print("Heure   Angle (°)")
print("------------------")

for h in range(1, 13):
    print(f"{h:>2} h   =  {calcul_angle(h):.0f}°")
# --- ⚙️ Configuration du servo ---
SERVO_PIN = 18      # Broche signal du servo (GP15)
PWM_FREQ = 50       # Fréquence standard servo = 50 Hz
SERVO_MIN = 500     # Durée impulsion pour 0° (µs)
SERVO_MAX = 2500    # Durée impulsion pour 180° (µs)



# Fonctionnement du servo Moteur en fonction des angles calculés

def write_servo(angle_deg):
    # Clamp (sécurité)
    if angle_deg < 0: angle_deg = 0
    if angle_deg > 180: angle_deg = 180
    
    # Conversion angle → microsecondes
    pulse_us = SERVO_MIN + (SERVO_MAX - SERVO_MIN) * (angle_deg / 180)
    duty = int(pulse_us * 65535 / 20000)  # période = 20ms à 50Hz
    pwm.duty_u16(duty)
    print("→ Servo à %.1f° " % (angle_deg))

#  Initialisation du PWM 
pwm = PWM(Pin(SERVO_PIN))
pwm.freq(PWM_FREQ)

# Test sur tout le cadran 
print("Test de position des heures (0° → 180°)...")

for heure in range(0, 13):  # 0 à 12
    angle = heure * 15  # 12h = 180°
    print("Heure:", (heure if heure != 0 else 12), "h  →  angle =", angle, "°")
    write_servo(angle)
    time.sleep(1.5)  # petite pause entre chaque position

print(" Fin du Test.")

# Retour automatique du servo à 0° avant l'horloge ---
print("\nRetour du servo à 0° (position 12h)...")
write_servo(0)
time.sleep(2)
print("Servo prêt pour l'heure actuelle !")


## Controle du servo moteur



print("\n--- Contrôle du servo selon l'heure Internet ---")

def calcul_angle(heure, minute=0, seconde=0):
    """Calcule l'angle exact du servo (12h → 180°)."""
    angle = ((heure % 12) + minute / 60 + seconde / 3600) * 15
    return angle

def set_servo(angle_deg):
    """Envoie au servo un angle (0°–180°)."""
    # Sécurité pour éviter les valeurs hors limites
    if angle_deg < 0:
        angle_deg = 0
    if angle_deg > 180:
        angle_deg = 180

    # Conversion angle → largeur d’impulsion (µs)
    pulse_us = SERVO_MIN + (SERVO_MAX - SERVO_MIN) * (angle_deg / 180)
    duty = int(pulse_us * 65535 / 20000)  # Période = 20 ms à 50 Hz
    pwm.duty_u16(duty)
    print(f"→ Servo positionné à {angle_deg:.1f}° (pulse = {pulse_us:.0f} µs)")

# --- Positionnement du servo selon l’heure actuelle ---
print("\n--- Positionnement du servo selon l'heure ---")

t = heure_locale(TZ_OFFSET)
heure, minute, seconde = t[3], t[4], t[5]

angle = calcul_angle(heure, minute, seconde)
print("Heure locale actuelle : %02d:%02d:%02d" % (heure, minute, seconde))
print("Angle calculé :", round(angle, 2), "°")

# Envoi de la position au servo
set_servo(angle)
print("Le servo est maintenant positionné selon l’heure actuelle !")
