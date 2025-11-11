import network
import ntptime
import utime

# === PARAMÈTRES WI-FI ===
SSID = "iP"           # ← à remplacer
PASSWORD = "Ton_MotDePasse"     # ← à remplacer

# --- Connexion Wi-Fi ---
wlan = network.WLAN(network.STA_IF)  # mode station (client)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connexion au Wi-Fi...")

# Attente de la connexion
while not wlan.isconnected():
    print("⏳ Connexion en cours...")
    utime.sleep(1)

print("✅ Connecté au réseau Wi-Fi !")
print("Adresse IP :", wlan.ifconfig()[0])

# --- Synchronisation de l'heure via Internet (serveur NTP) ---
print("\nSynchronisation de l'heure...")

try:
    ntptime.settime()  # met à jour l'heure interne du Pico W (en UTC)
    print("✅ Heure synchronisée avec le serveur NTP.")
except Exception as e:
    print("⚠️ Échec de la synchronisation :", e)

# --- Affichage de l'heure actuelle ---
while True:
    t = utime.localtime()  # renvoie (année, mois, jour, heure, minute, seconde, ...)
    heure = (t[3] + 1) % 24  # UTC+1 → Belgique/France (ajuster si besoin)
    minute = t[4]
    seconde = t[5]

    print(f"🕒 Heure actuelle : {heure:02d}:{minute:02d}:{seconde:02d}")
    utime.sleep(1)
