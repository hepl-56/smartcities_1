from machine import Pin, I2C, ADC, PWM
import time
import dht
from i2c_lcd import I2cLcd  # version PCF8574 compatible LCD1602

# Capteur
capteur = dht.DHT11(Pin(18))

# Potentiomètre
pot = ADC(1)

# LED et buzzer
led = Pin(20, Pin.OUT)
buzzer = PWM(Pin(16))
buzzer.duty_u16(0)

# LCD I2C (adresse détectée 0x3E)
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)
lcd = I2cLcd(i2c, 0x3E, 2, 16)

def lire_consigne():
    val = pot.read_u16()
    consigne = 15 + (val / 65535) * (35 - 15)
    return round(consigne,1)

while True:
    try:
        capteur.measure()
        temp = capteur.temperature()
        consigne = lire_consigne()
        diff = temp - consigne

        lcd.clear()
        if diff >= 3:
            lcd.putstr("!!! ALARM !!!\n")
            lcd.putstr(f"T:{temp:.1f} > S:{consigne:.1f}")
            buzzer.freq(1000)
            buzzer.duty_u16(30000)
            led.value(int(time.ticks_ms()//250 % 2))  # LED clignotante rapide
        elif diff > 0:
            lcd.putstr(f"Set:{consigne:.1f}C\nAmbient:{temp:.1f}C")
            buzzer.duty_u16(0)
            led.value(int(time.ticks_ms()//1000 % 2))  # LED clignotante lente
        else:
            lcd.putstr(f"Set:{consigne:.1f}C\nAmbient:{temp:.1f}C")
            buzzer.duty_u16(0)
            led.off()

        time.sleep(0.2)

    except Exception as e:
        lcd.clear()
        lcd.putstr("Erreur capteur")
        print("Erreur :", e)
        time.sleep(2)
