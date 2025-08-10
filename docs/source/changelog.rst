.. _changelog:

Changelog
=========

Tutte le modifiche rilevanti apportate a RasPY Utility saranno documentate in questo file.

Il formato è basato su `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
e questo progetto aderisce a `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

.. _unreleased:

[1.2.0] - 2025-06-13
-------------------

### Aggiunto
- Interfaccia grafica moderna con supporto temi scuro/chiaro
- Server web integrato per accesso remoto
- Visualizzazione in tempo reale dello stato dei pin GPIO
- Integrazione con la system tray per accesso rapido
- Supporto per controllo GPIO remoto
- Interfaccia web responsive per dispositivi mobili/desktop
- Migliorato il sistema di gestione degli errori
- Sistema di logging avanzato con aggiornamenti in tempo reale
- Supporto per più finestre nell'interfaccia grafica
- Supporto per lingue con scrittura da destra a sinistra (RTL)

### Modificato
- Aggiornato il supporto a Python 3.8+
- Rifattorizzato il sistema di controllo GPIO per migliori prestazioni
- Migliorato il sistema dei menu con una migliore organizzazione
- Documentazione e commenti al codice aggiornati
- Dipendenze aggiornate alle ultime versioni stabili
- Migliorata la compatibilità cross-piattaforma

### Corretto
- Risolti problemi di rilevamento e inizializzazione del simulatore GPIO
- Corretti problemi di integrazione dei menu
- Risolte perdite di memoria nei componenti dell'interfaccia grafica
- Migliorata la gestione degli errori nelle operazioni GPIO
- Corretta la funzionalità di cambio lingua
- Risolti problemi di threading nel server web

[1.1.0] - 2025-06-03
-------------------

### Aggiunto
- Interfaccia di controllo GPIO per Raspberry Pi
- Simulatore GPIO per sviluppo su sistemi non Raspberry Pi
- Endpoint REST API per il controllo GPIO
- Interfaccia Tkinter per la gestione GPIO
- Supporto multilingua per l'interfaccia GPIO
- Rilevamento e configurazione automatica del simulatore GPIO
- Client HTTP per la comunicazione con l'API

### Modificato
- Aggiornato il supporto a Python 3.8+
- Migliorata la gestione degli errori e il feedback all'utente
- Migliorato il logging per le operazioni GPIO
- Migliorata la gestione dei processi per il simulatore GPIO

### Corretto
- Risolti problemi di integrazione del menu
- Corretti bug nella gestione dei processi
- Migliorata la compatibilità cross-piattaforma

[1.0.0] - 2025-05-20
-------------------
- Versione stabile iniziale
- Sistema di logging centralizzato
- Supporto multilingua
- Visualizzatore log con filtri
- Framework di base dell'applicazione

.. _GitHub Releases: https://github.com/Nsfr750/raspy-utility/releases

Per un elenco dettagliato di tutte le modifiche, consulta le `GitHub Releases`_.
