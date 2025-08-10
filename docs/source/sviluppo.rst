Guida allo sviluppo
****************

Struttura del progetto
=====================

::

    raspy-utility/
    ├── app/                    # Codice sorgente principale
    │   ├── __init__.py
    │   ├── routes.py          # Endpoint API
    │   └── gpio_simulator.py  # Simulatore GPIO
    ├── gui/                   # Interfaccia utente
    │   ├── main_window.py
    │   └── gpio_window.py
    ├── struttura/             # Moduli di supporto
    │   ├── __init__.py
    │   ├── menu.py
    │   └── lang.py
    ├── tests/                 # Test automatici
    ├── docs/                  # Documentazione
    ├── main.py                # Punto di ingresso
    └── requirements.txt       # Dipendenze

Configurazione dell'ambiente
===========================

1. Clona il repository:

   .. code-block:: bash

      git clone https://github.com/Nsfr750/raspy-utility.git
      cd raspy-utility

2. Crea un ambiente virtuale:

   .. code-block:: bash

      python -m venv venv
      .\venv\Scripts\activate  # Windows
      source venv/bin/activate  # Linux/Mac

3. Installa le dipendenze di sviluppo:

   .. code-block:: bash

      pip install -r requirements-dev.txt

Linee guida di codifica
======================

- Segui PEP 8 per lo stile del codice
- Usa docstring in formato Google per la documentazione
- Scrivi test per ogni nuova funzionalità
- Commenta il codice in inglese
- Usa nomi descrittivi per variabili e funzioni

Esecuzione dei test
==================

.. code-block:: bash

   # Esegui tutti i test
   pytest
   
   # Esegui i test con report di copertura
   pytest --cov=app tests/
   
   # Genera report HTML della copertura
   pytest --cov=app --cov-report=html tests/

Documentazione
=============

Per generare la documentazione:

.. code-block:: bash

   # Installa le dipendenze per la documentazione
   pip install -r docs/requirements-docs.txt
   
   # Genera la documentazione HTML
   cd docs
   make html
   
   # Apri la documentazione nel browser
   start _build/html/index.html  # Windows
   xdg-open _build/html/index.html  # Linux
   open _build/html/index.html  # Mac

Processo di commit
================

1. Crea un branch per la nuova funzionalità:
   .. code-block:: bash

      git checkout -b feature/nuova-funzionalita

2. Fai commit delle modifiche:
   .. code-block:: bash

      git add .
      git commit -m "Aggiungi nuova funzionalità"

3. Invia le modifiche al repository remoto:
   .. code-block:: bash

      git push origin feature/nuova-funzionalita

4. Crea una Pull Request su GitHub
