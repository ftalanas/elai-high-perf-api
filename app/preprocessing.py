import numpy as np
from typing import List, Tuple
from .schemas import PredictItem


def binarize_cliente_attivo(v: str | None) -> int:
    return 1 if (v is not None and v == "SI") else 0


def make_features(items: List[PredictItem]) -> np.ndarray:
    # Drop "nome"
    # eta pass-through
    # cliente_attivo binarizzato
    X = np.zeros((len(items), 2), dtype=float)
    for i, it in enumerate(items):
        X[i, 0] = float(it.eta)
        X[i, 1] = float(binarize_cliente_attivo(it.cliente_attivo))
    return X
