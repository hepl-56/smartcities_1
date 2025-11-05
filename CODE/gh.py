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

# ==================== VALEURS PAR DEFAUT SIMULEES ====================
valeurs_brutes = [0, 16384, 32768, 49152, 65535]  # simuler potentiomètre
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
        led.value((t // 1000) % 2)
    else:
        led.value((t // 250) % 2)

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

        # Mettre à jour LCD si temp ou consigne change
        if temp != temp_precedente or consigne != consigne_precedente:
            temp_precedente = temp
            consigne_precedente = consigne

            if diff >= 3:
                # Température trop élevée → alarme
                buzzer.freq(1000)
                buzzer.duty_u16(30000)

                # Faire clignoter "ALARM" pendant 3 secondes
                fin_alarme = ticks_ms() + 3000  # durée 3 sec
                afficher = True
                while ticks_ms() < fin_alarme:
                    lcd.clear()
                    if afficher:
                        lcd.setCursor(0, 0)
                        lcd.print("ALARM")
                        lcd.setCursor(0, 1)
                        lcd.print(f"Ambient:{temp:.1f}C")
                    # alterner l'affichage toutes les 0,5 s
                    afficher = not afficher
                    clignoter_led(diff)
                    sleep(0.5)

                buzzer.duty_u16(0)  # éteindre buzzer après alarme

            else:
                # Température normale
                lcd.clear()
                lcd.setCursor(0, 0)
                lcd.print(f"Set:{consigne:.1f}C")
                lcd.setCursor(0, 1)
                lcd.print(f"Ambient:{temp:.1f}C")
                buzzer.duty_u16(0)

        # LED clignotante hors alarme
        clignoter_led(diff)

        sleep(1)

    except Exception as e:
        lcd.clear()
        lcd.print("Erreur capteur")
        print("Erreur :", e)
        sleep(2)
