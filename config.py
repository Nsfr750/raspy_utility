import os

class Config:
    # Configurazione di base
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    
    # Configurazione del server
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True
    
    # Configurazione GPIO
    GPIO_MODE = 'BCM'  # BCM o BOARD
    
    # Configurazione PIN di default
    DEFAULT_PINS = {
        'LED': 17,
        'BUTTON': 27
    }
    
    # Configurazione connessione di rete
    REMOTE_GPIO_ENABLED = False  # Impostare su True per abilitare il controllo remoto
    REMOTE_GPIO_HOST = 'http://raspberrypi:8000'  # URL del server GPIO remoto
    REMOTE_GPIO_API_KEY = None  # Chiave API opzionale per l'autenticazione
    
    # Timeout per le richieste di rete (in secondi)
    NETWORK_TIMEOUT = 5.0
