from pydantic import BaseModel, Field
from typing import List, Union, Literal, Optional


class PredictItem(BaseModel):
    nome: Optional[str] = None
    eta: int = Field(..., ge=0)
    cliente_attivo: Optional[str] = None  # "SI"/"NO"/None/altro


class PredictOut(BaseModel):
    probability: float
    label: Literal["OK", "NO_ACQUISTO"]


# Body può essere singolo oggetto o lista (batch)
PredictBody = Union[PredictItem, List[PredictItem]]
