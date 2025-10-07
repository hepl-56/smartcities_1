from machine import Pin
from time import sleep

led = Pin(16, Pin.OUT)      
bouton = Pin(20, Pin.IN, Pin.PULL_DOWN)  

etat_précedent_bouton  = 0
nb_pression = 0

while True:
    etat_bouton = bouton.value()

    # Détection d'un appui (front montant)
    if etat_bouton == 1 and etat_précedent_bouton  == 0:
        nb_pression += 1
        print("Bouton pressé :", nb_pression)
        sleep(0.2) 
        
        if nb_pression > 3:
            nb_pression = 1

    if nb_pression == 1:
        led.toggle()
        sleep(1)  
    elif nb_pression == 2:
        led.toggle()
        sleep(0.2)  
    elif nb_pression == 3:
        led.value(0) 

    etat_précedent_bouton = etat_bouton
