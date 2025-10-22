from machine import Pin, PWM, I2C
from utime import sleep, ticks_ms
import dht
from lcd1602 import LCD1602

# ==================== CONFIGURATION ====================
capteur = dht.DHT11(Pin(18))

led = Pin(20, Pin.OUT)
buzzer = PWM(Pin(16))
buzzer.duty_u16(0)

i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)
lcd = LCD1602(i2c, 2, 16)
lcd.display()
lcd.clear()

# ==================== VALEURS SIMULEES ====================
valeurs_brutes = [0, 16384, 32768, 49152, 65535]  # simulation potentiomètre
index = 0

def consigne_depuis_valeur_brute(val):
    """Convertit valeur brute 0-65535 en température 15-35°C"""
    return round(15 + (val / 65535) * (35 - 15), 1)

def clignoter_led(diff):
    """Clignotement LED selon la différence température-consigne"""
    t = ticks_ms()
    if diff <= 0:
        led.off()
    elif 0 < diff < 3:
        led.value((t // 1000) % 2)  # clignotement lent 0,5 Hz
    else:
        led.value((t // 250) % 2)   # clignotement rapide 2 Hz

def defiler_alarm_droite():
    """Défilement du mot ALARM de gauche vers la droite sur 16 colonnes"""
    texte = "!!! ALARM !!!   "  # espaces pour sortir du LCD
    longueur = len(texte)
    # Boucle pour déplacer le texte vers la droite
    for i in range(longueur - 15, -1, -1):  # commence à droite et va vers gauche
        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.print(texte[i:i+16])
        sleep(0.3)
        # LED clignotante rapide pendant le défilement
        led.value((ticks_ms() // 250) % 2)

# ==================== BOUCLE PRINCIPALE ====================
temp_precedente = None
consigne_precedente = None

while True:
    try:
        # Lire consigne simulée
        index += 1
        valeur_brute = valeurs_brutes[index % len(valeurs_brutes)]
        consigne = consigne_depuis_valeur_brute(valeur_brute)

        # Lire température ambiante
        capteur.measure()
        temp = capteur.temperature()
        diff = temp - consigne

        # Si température dépasse consigne +3°C → ALARM
        if diff >= 3:
            buzzer.freq(1000)
            buzzer.duty_u16(30000)

            # Faire défiler ALARM de gauche vers la droite
            defiler_alarm_droite()

            buzzer.duty_u16(0)  # arrêter buzzer après défilement

        # Sinon affichage normal
        else:
            if temp != temp_precedente or consigne != consigne_precedente:
                lcd.clear()
                lcd.setCursor(0, 0)
                lcd.print(f"Set:{consigne:.1f}C")
                lcd.setCursor(0, 1)
                lcd.print(f"Ambient:{temp:.1f}C")
                temp_precedente = temp
                consigne_precedente = consigne

            # LED clignotante selon différence
            clignoter_led(diff)

        sleep(1)

    except Exception as e:
        lcd.clear()
        lcd.print("Erreur capteur")
        print("Erreur :", e)
        sleep(2)
