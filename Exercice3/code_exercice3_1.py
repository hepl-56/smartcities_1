from machine import Pin, PWM, I2C
from utime import sleep, ticks_ms
import dht
from lcd1602 import LCD1602

# ==================== CONFIGURATION DU MATERIEL ====================
# Capteur DHT11 pour mesurer la température ambiante
capteur = dht.DHT11(Pin(18))

# LED pour indication
led = Pin(20, Pin.OUT)

# Buzzer pour alarme
buzzer = PWM(Pin(16))
buzzer.duty_u16(0)  # buzzer éteint au départ

# LCD I2C 16x2
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)
lcd = LCD1602(i2c, 2, 16)  # 2 lignes, 16 colonnes
lcd.display()
lcd.clear()

# ==================== VALEURS PAR DEFAUT SIMULEES ====================
# Valeurs brutes simulant le potentiomètre (0 → 65535)
valeurs_brutes = [0, 16384, 32768, 49152, 65535]  # de 0% à 100% de la plage
index = 0  # index pour parcourir la liste

# Fonction pour convertir valeur brute en température 15-35°C
def consigne_depuis_valeur_brute(val):
    """Convertit la valeur brute (0-65535) en température de consigne (15-35°C)"""
    consigne = 15 + (val / 65535) * (35 - 15)
    return round(consigne, 1)

# ==================== FONCTION DE CLIGNOTEMENT DE LED ====================
def clignoter_led(diff):
    """
    Clignote la LED selon la différence entre la température ambiante et la consigne
    - diff <= 0 : LED éteinte
    - 0 < diff < 3 : clignotement lent 0,5 Hz
    - diff >= 3 : clignotement rapide 2 Hz
    """
    t = ticks_ms()
    if diff <= 0:
        led.off()
    elif 0 < diff < 3:
        led.value((t // 1000) % 2)  # 0,5 Hz
    else:
        led.value((t // 250) % 2)   # 2 Hz

# ==================== AFFICHAGE INITIAL ====================
# Lire la première valeur simulée et convertir en consigne
valeur_brute = valeurs_brutes[index % len(valeurs_brutes)]
consigne = consigne_depuis_valeur_brute(valeur_brute)

# Lire la température ambiante initiale
capteur.measure()
temp = capteur.temperature()

# Afficher la consigne et la température sur le LCD
lcd.clear()
lcd.setCursor(0, 0)
lcd.print(f"Set:{consigne:.1f}C")
lcd.setCursor(0, 1)
lcd.print(f"Ambient:{temp:.1f}C")
sleep(3)  # pause pour visualiser la consigne et la température

# ==================== BOUCLE PRINCIPALE ====================
temp_precedente = temp
consigne_precedente = consigne

while True:
    try:
        # Passer à la prochaine valeur simulée dans la liste
        index += 1
        valeur_brute = valeurs_brutes[index % len(valeurs_brutes)]
        consigne = consigne_depuis_valeur_brute(valeur_brute)

        # Mesurer la température ambiante avec le DHT11
        capteur.measure()
        temp = capteur.temperature()

        # Calculer la différence entre température et consigne
        diff = temp - consigne

        # Mise à jour du LCD si la température ou la consigne change
        if temp != temp_precedente or consigne != consigne_precedente:
            lcd.clear()
            temp_precedente = temp
            consigne_precedente = consigne

            if diff >= 3:
                # Température trop élevée → alarme
                lcd.setCursor(0, 0)
                lcd.print("ALARM")
                lcd.setCursor(0, 1)
                lcd.print(f"Ambient:{temp:.1f}C")
                buzzer.freq(1000)         # fréquence du buzzer
                buzzer.duty_u16(30000)    # activer le buzzer
            else:
                # Température normale
                lcd.setCursor(0, 0)
                lcd.print(f"Set:{consigne:.1f}C")
                lcd.setCursor(0, 1)
                lcd.print(f"Ambient:{temp:.1f}C")
                buzzer.duty_u16(0)        # buzzer éteint

        # Contrôle de la LED selon la différence
        clignoter_led(diff)

        # Attendre 3 secondes avant de passer à la prochaine valeur simulée
        sleep(3)

    except Exception as e:
        # Gestion des erreurs du capteur
        lcd.clear()
        lcd.print("Erreur capteur")
        print("Erreur :", e)
        sleep(2)
