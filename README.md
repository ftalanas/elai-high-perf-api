ELAI High-Performance Predict API

PANORAMICA
Questo progetto implementa una API di inferenza ad alte prestazioni basata su FastAPI, progettata per esporre in produzione un modello di machine learning tramite endpoint HTTP.

Lo stack principale include:
- FastAPI: Gestione asincrona delle richieste
- MongoDB: Database documentale
- RandomForestClassifier (scikit-learn): Modello predittivo
- NumPy: Gestione delle feature numeriche

ARCHITETTURA APPLICATIVA
L’applicazione è strutturata come una inference pipeline asincrona:
1) Caricamento del modello a startup:
Il modello viene deserializzato una sola volta all’avvio dell’API per ridurre latenza e overhead computazionale.

2) Validazione input tramite Pydantic
Gli oggetti in ingresso vengono validati prima dell’esecuzione della logica di inferenza (es. controllo su età ≥ 0).

3) Preprocessing deterministico
- binarizzazione della variabile categorica cliente_attivo
- costruzione della matrice numerica delle feature (make_features)

4) Inferenza con probabilità (predict_proba)
Data la forte sbilanciatura del dataset (conversion rate ≈ 10%),
la decision boundary è impostata THRESHOLD = 0.10 invece della soglia standard 0.5.

5) Post-processing e risposta JSON
La probabilità della classe positiva viene trasformata in:
- OK → cliente potenzialmente acquirente
- NO_ACQUISTO → cliente non target

6) Persistenza asincrona su MongoDB
Le predizioni vengono salvate tramite Motor (AsyncIOMotorClient)
con strategia best-effort logging:
- eventuali errori del database non bloccano la risposta API
Ogni documento contiene:
- timestamp UTC
- modalità (single/batch)
- numero record
- input e output della predizione

AVVIO DELL'APPLICAZIONE
1. Clonare il repository
git clone https://github.com/ftalanas/elai-high-perf-api
cd elai-high-perf-api
2. Creare e attivare un virtual environment
python -m venv .venv
source .venv/bin/activate -> Linux/Mac
source .venv\Scripts\activate -> Windows
3. Installare le dipendenze
pip install -r requirements.txt
4. Avviare servizi (API + MongoDB)
docker compose up --build
5. Avviare l’API manualmente
uvicorn app.main:app --reload --port 8000
L’API sarà disponibile su -> http://127.0.0.1:8000
6. Accedere alla shell MongoDB
docker exec -it elai_mongo mongosh
7. Verifica documenti salvati
use elai
db.predictions.find().sort({ timestamp: -1 }).limit(5)

NOTE DI SVILUPPO
Durante lo sviluppo, le porte standard risultavano già occupate.
L’applicazione è quindi stata eseguita su porte alternative locali senza impatti sulla logica applicativa.
In un ambiente di deployment reale, le porte verrebbero configurate tramite:
- variabili d’ambiente
- configurazione Docker / orchestrazione
garantendo portabilità tra ambienti (dev, staging, production).
