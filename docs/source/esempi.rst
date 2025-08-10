Esempi
******

In questa sezione troverai esempi pratici per utilizzare RasPY 4 Utility.

Controllo di un LED
==================

Questo esempio mostra come controllare un LED collegato al pin GPIO 17.

.. code-block:: python

   import requests
   import time
   
   BASE_URL = "http://localhost:5000/api/gpio"
   LED_PIN = 17
   
   def lampeggia_led(volte=5, intervallo=0.5):
       """Fa lampeggiare un LED."""
       for _ in range(volte):
           # Accendi il LED
           requests.post(f"{BASE_URL}/{LED_PIN}/on")
           time.sleep(intervallo)
           # Spegni il LED
           requests.post(f"{BASE_URL}/{LED_PIN}/off")
           time.sleep(intervallo)
   
   if __name__ == "__main__":
       lampeggia_led(10)  # Lampeggia 10 volte

Lettura di un pulsante
=====================

Questo esempio mostra come leggere lo stato di un pulsante collegato al pin GPIO 18.

.. code-block:: python

   import requests
   import time
   
   BASE_URL = "http://localhost:5000/api/gpio"
   PULSANTE_PIN = 18
   
   def leggi_pulsante():
       """Legge lo stato di un pulsante."""
       try:
           response = requests.get(f"{BASE_URL}/{PULSANTE_PIN}")
           stato = response.json().get("state", 0)
           return stato == 1
       except Exception as e:
           print(f"Errore durante la lettura del pin: {e}")
           return False
   
   if __name__ == "__main__":
       print("Premi Ctrl+C per uscire")
       try:
           while True:
               if leggi_pulsante():
                   print("Pulsante premuto!")
               time.sleep(0.1)
       except KeyboardInterrupt:
           print("\nProgramma terminato")

Controllo di più dispositivi
===========================

Questo esempio mostra come controllare più dispositivi contemporaneamente.

.. code-block:: python

   import requests
   import time
   
   class DispositivoGPIO:
       """Classe per gestire un dispositivo GPIO."""
       
       def __init__(self, pin, nome):
           self.pin = pin
           self.nome = nome
           self.base_url = f"http://localhost:5000/api/gpio/{pin}"
       
       def accendi(self):
           """Accende il dispositivo."""
           requests.post(f"{self.base_url}/on")
           print(f"{self.nome} acceso")
       
       def spegni(self):
           """Spegne il dispositivo."""
           requests.post(f"{self.base_url}/off")
           print(f"{self.nome} spento")
       
       def stato(self):
           """Restituisce lo stato del dispositivo."""
           response = requests.get(self.base_url)
           return response.json().get("state", 0) == 1
   
   if __name__ == "__main__":
       # Crea istanze dei dispositivi
       led_rosso = DispositivoGPIO(17, "LED Rosso")
       led_verde = DispositivoGPIO(18, "LED Verde")
       pulsante = DispositivoGPIO(19, "Pulsante")
       
       try:
           print("Premi Ctrl+C per uscire")
           while True:
               if pulsante.stato():
                   led_rosso.accendi()
                   led_verde.spegni()
               else:
                   led_rosso.spegni()
                   led_verde.accendi()
               time.sleep(0.1)
       except KeyboardInterrupt:
           # Spegni tutto all'uscita
           led_rosso.spegni()
           led_verde.spegni()
           print("\nProgramma terminato")
