API Reference
************

Panoramica
=========

L'API REST di RasPY 4 Utility permette di controllare i pin GPIO tramite richieste HTTP. 
Tutte le risposte sono in formato JSON.

Endpoint disponibili
==================

.. http:get:: /api/gpio

   Restituisce lo stato di tutti i pin GPIO configurati.

   **Risposta di esempio**:

   .. code-block:: json

      {
        "17": {"state": 0, "mode": "out", "description": "LED Rosso"},
        "18": {"state": 1, "mode": "in", "description": "Pulsante"}
      }

.. http:get:: /api/gpio/<int:pin>

   Restituisce lo stato di un pin specifico.

   :param pin: Numero del pin GPIO
   :status 200: Operazione riuscita
   :status 404: Pin non trovato
   
   **Risposta di esempio**:

   .. code-block:: json

      {
        "state": 0,
        "mode": "out",
        "description": "LED Rosso"
      }

.. http:post:: /api/gpio/<int:pin>/on

   Accende il pin specificato.
   
   :param pin: Numero del pin GPIO
   :status 200: Operazione riuscita
   :status 400: Pin non valido o non scrivibile

.. http:post:: /api/gpio/<int:pin>/off

   Spegne il pin specificato.
   
   :param pin: Numero del pin GPIO
   :status 200: Operazione riuscita
   :status 400: Pin non valido o non scrivibile

Esempi di utilizzo
=================

Utilizzo con cURL:

.. code-block:: bash

   # Accendi il pin 17
   curl -X POST http://localhost:5000/api/gpio/17/on
   
   # Leggi lo stato del pin 17
   curl http://localhost:5000/api/gpio/17
   
   # Spegni il pin 17
   curl -X POST http://localhost:5000/api/gpio/17/off

Utilizzo con Python:

.. code-block:: python

   import requests
   
   BASE_URL = "http://localhost:5000/api/gpio"
   
   # Accendi un pin
   response = requests.post(f"{BASE_URL}/17/on")
   print(response.json())
   
   # Leggi lo stato
   response = requests.get(f"{BASE_URL}/17")
   print(response.json())
