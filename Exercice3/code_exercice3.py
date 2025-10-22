from machine import Pin, ADC, PWM, I2C
from utime import sleep, ticks_ms
import dht
from lcd1602 import LCD1602

# ==================== CONFIGURATION ====================
capteur = dht.DHT11(Pin(18))
pot = ADC(0)

led = Pin(20, Pin.OUT)
buzzer = PWM(Pin(16))
buzzer.duty_u16(0)  # buzzer éteint au départ

i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)
lcd = LCD1602(i2c, 2, 16)
lcd.display()
lcd.clear()

# ==================== FONCTIONS ====================
def lire_consigne():
    """Lit le potentiomètre et convertit en température 15-35°C"""
    val = pot.read_u16()
    return round(15 + (val / 65535) * (35 - 15), 1)

def clignoter_led(diff):
    """LED clignotante selon la différence de température"""
    t = ticks_ms()
    if diff <= 0:
        led.off()
    elif 0 < diff < 3:
        led.value((t // 1000) % 2)  # clignotement lent 0,5 Hz
    else:
        led.value((t // 250) % 2)   # clignotement rapide 2 Hz

# ==================== AFFICHAGE INITIAL ====================
# Lire les valeurs initiales
capteur.measure()
temp = capteur.temperature()
consigne = lire_consigne()

lcd.clear()
lcd.setCursor(0, 0)
lcd.print(f"Set:{consigne:.1f}C")
lcd.setCursor(0, 1)
lcd.print(f"Ambient:{temp:.1f}C")

sleep(3)  # attendre 3 secondes pour visualiser les valeurs initiales

# ==================== BOUCLE PRINCIPALE ====================
temp_precedente = temp
consigne_precedente = consigne

while True:
    try:
        # Lecture de la température et de la consigne
        capteur.measure()
        temp = capteur.temperature()
        consigne = lire_consigne()
        diff = temp - consigne

        # Mise à jour du LCD uniquement si la valeur change
        if temp != temp_precedente or consigne != consigne_precedente:
            lcd.clear()
            temp_precedente = temp
            consigne_precedente = consigne

            if diff >= 3:
                lcd.setCursor(0, 0)
                lcd.print("ALARM")
                lcd.setCursor(0, 1)
                lcd.print(f"Ambient:{temp:.1f}C")
                buzzer.freq(1000)
                buzzer.duty_u16(30000)
            else:
                lcd.setCursor(0, 0)
                lcd.print(f"Set:{consigne:.1f}C")
                lcd.setCursor(0, 1)
                lcd.print(f"Ambient:{temp:.1f}C")
                buzzer.duty_u16(0)

        # LED clignotante selon la différence
        clignoter_led(diff)

        # Attendre 1 seconde avant prochaine mesure
        sleep(1)

    except Exception as e:
        lcd.clear()
        lcd.print("Erreur capteur")
        print("Erreur :", e)
        sleep(2)
