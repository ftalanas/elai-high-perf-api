import pickle
from pathlib import Path


# Caricamento e deserializzazione modello
def load_model(path: str):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Model not found at: {p.resolve()}")
    with p.open("rb") as f:
        return pickle.load(f)
