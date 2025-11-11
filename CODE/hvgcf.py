from machine import Pin, PWM
import time

# --- ⚙️ Configuration du servo ---
SERVO_PIN = 18      # Broche signal du servo (GP15)
PWM_FREQ = 50       # Fréquence standard servo = 50 Hz
SERVO_MIN = 500     # Durée impulsion pour 0° (µs)
SERVO_MAX = 2500    # Durée impulsion pour 180° (µs)

# --- Fonction pour convertir un angle en impulsion PWM ---
def write_servo(angle_deg):
    # Clamp (sécurité)
    if angle_deg < 0: angle_deg = 0
    if angle_deg > 180: angle_deg = 180
    
    # Conversion angle → microsecondes
    pulse_us = SERVO_MIN + (SERVO_MAX - SERVO_MIN) * (angle_deg / 180)
    duty = int(pulse_us * 65535 / 20000)  # période = 20ms à 50Hz
    pwm.duty_u16(duty)
    print("→ Servo à %.1f° " % (angle_deg))

# --- Initialisation du PWM ---
pwm = PWM(Pin(SERVO_PIN))
pwm.freq(PWM_FREQ)

# --- Test progressif sur tout le cadran ---
print("Test de position des heures (0° → 180°)...")

for heure in range(0, 13):  # 0 à 12
    angle = heure * 15  # 12h = 180°
    print("Heure:", (heure if heure != 0 else 12), "h  →  angle =", angle, "°")
    write_servo(angle)
    time.sleep(1.5)  # petite pause entre chaque position

print("✅ Test terminé. Ajuste ton cadran selon les positions observées.")
