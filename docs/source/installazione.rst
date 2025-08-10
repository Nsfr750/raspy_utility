Installazione
************

Requisiti di sistema
===================

- Python 3.8 o superiore
- Raspberry Pi (opzionale, è disponibile un simulatore)
- Connessione Internet (per l'installazione dei pacchetti)

Installazione
============

1. Clona il repository:

   .. code-block:: bash

      git clone https://github.com/Nsfr750/raspy-utility.git
      cd raspy-utility

2. Crea e attiva un ambiente virtuale (consigliato):

   .. code-block:: bash

      python -m venv venv
      .\venv\Scripts\activate  # Su Windows
      source venv/bin/activate  # Su Linux/Mac

3. Installa le dipendenze:

   .. code-block:: bash

      pip install -r requirements.txt

4. Su Raspberry Pi, installa le dipendenze aggiuntive:

   .. code-block:: bash

      sudo apt-get update
      sudo apt-get install python3-rpi.gpio

Avvio dell'applicazione
======================

.. code-block:: bash

   python main.py

Per il server API:

.. code-block:: bash

   python run.py

Configurazione
=============

Modifica il file ``config.py`` per personalizzare le impostazioni:

- Porta del server
- Configurazione dei pin GPIO
- Impostazioni di lingua
- Opzioni di logging
