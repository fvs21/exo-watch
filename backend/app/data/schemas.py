from pydantic import BaseModel, Field
from typing import List, Optional

class CandidateFeatures(BaseModel):
    model: None | int = Field(None, description="Identificador del modelo (opcional). Vacío significa usar el modelo base.")
    orbital_period: float      # Período Orbital
    transit_epoch: float      # Época del Tránsito
    transit_duration: float     # Duración del Tránsito
    transit_depth: float        # Profundidad del Tránsito
    planet_radius: float         # Radio Planetario
    eq_temp: float               # Temperatura de Equilibrio
    insol: float                 # Flujo de Insolación
    snr: float                   # Relación Señal a Ruido
    steff: float                 # Temperatura Estelar Efectiva
    srad: float                  # Radio Estelar

class Model(BaseModel):
    id: int
    name: str
    path: str

    learning_rate: Optional[float] = None
    n_estimators: Optional[int] = None
    num_leaves: Optional[int] = None
    max_depth: Optional[int] = None
    accuracy: Optional[float] = None