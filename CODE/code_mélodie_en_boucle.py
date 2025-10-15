from machine import Pin, PWM, ADC
from time import sleep

buzzer = PWM(Pin(20))
ROTARY_ANGLE_SENSOR = ADC(1)

# Notes
C = 262
D = 294
E = 330
F = 349
G = 392
A = 440
B = 494

melodie_1= [(C, 0.4), (C, 0.4), (G, 0.4), (G, 0.4),
           (A, 0.4), (A, 0.4), (G, 0.8),
           (F, 0.4), (F, 0.4), (E, 0.4), (E, 0.4),
           (D, 0.4), (D, 0.4), (C, 0.8)]

def jouer_note(freq, duree):
    buzzer.freq(freq)
    steps = int(duree / 0.01)
    for _ in range(steps):
        pot_value = ROTARY_ANGLE_SENSOR.read_u16()
        angle = (pot_value / 65535) * 300
        # Volume proportionnel à l'angle (0° → 300° → 0 → 65000)
        volume = int((angle / 300) * 65000)
        buzzer.duty_u16(volume)
        sleep(0.01)
    buzzer.duty_u16(0)
    sleep(0.02)
while True:
    for freq, duree in melodie_1:
        jouer_note(freq, duree)
        
