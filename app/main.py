import os
from fastapi import FastAPI, HTTPException
from typing import List, Union
import numpy as np

from .schemas import PredictItem, PredictOut, PredictBody
from .preprocessing import make_features
from .model_loader import load_model
from .db import save_prediction
from motor.core import AgnosticCollection

MODEL_PATH = os.getenv("MODEL_PATH", "models/Model.pkl")
THRESHOLD = float(os.getenv("THRESHOLD", "0.10"))

app = FastAPI(title="ELAI High-Perf Predict API")


# Carico modello all'avvio
@app.on_event("startup")
def startup():
    # carica modello una sola volta
    app.state.model = load_model(MODEL_PATH)


# Definizione GET
@app.get("/health")
def health():
    return {"status": "ok"}


# Definizione POST
@app.post("/predict")
async def predict(body: PredictBody):
    try:
        # Normalizza input a lista
        if isinstance(body, list):
            items = body
            mode = "batch"
        else:
            items = [body]
            mode = "single"

        if len(items) == 0:
            raise HTTPException(status_code=400, detail="Empty batch not allowed")
        if len(items) > 1000:
            raise HTTPException(status_code=400, detail="Batch size > 1000 not allowed")
        # Preprocessing dei dati
        X = make_features(items)

        model = app.state.model
        # RandomForestClassifier supporta predict_proba (da report)
        proba = model.predict_proba(X)[:, 1]  # classe positiva=1

        outputs: List[dict] = []
        for p in proba.tolist():
            label = "OK" if p >= THRESHOLD else "NO_ACQUISTO"
            outputs.append({"probability": float(p), "label": label})

        # risposta single o batch (come richiesto)
        response = outputs[0] if mode == "single" else outputs

        # salvataggio 1-write per chiamata
        if mode == "single":
            input_data = items[0].model_dump()
        else:
            input_data = [it.model_dump() for it in items]

        output_data = response  # già dict o list[dict]

        try:
            await save_prediction(
                input_data=input_data,
                output_data=output_data,
                n_records=len(items),
                mode=mode,
            )
        except Exception as e:
            # Temporaneo: stampa errore per debug
            print(f"[mongo] save failed: {e}")

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
