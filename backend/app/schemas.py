from pydantic import BaseModel, Field
from typing import List, Optional

class CandidateFeatures(BaseModel):
    koi_period: float        # Período Orbital
    koi_time0bk: float      # Época del Tránsito
    koi_impact: float       # Parámetro de Impacto
    koi_duration: float     # Duración del Tránsito
    koi_depth: float        # Profundidad del Tránsito
    koi_prad: float         # Radio Planetario
    koi_teq: float          # Temperatura de Equilibrio
    koi_insol: float        # Flujo de Insolación
    koi_model_snr: float    # Relación Señal a Ruido del Tránsito
    koi_steff: float        # Temperatura Estelar Efectiva
    koi_srad: float         # Radio Estelar

class PredictRequest(BaseModel):
    model: Optional[int] = Field(None, description="Identificador del modelo (opcional). Vacío significa usar el modelo base.")
    features: CandidateFeatures

class CreateModelRequest(BaseModel):
    learning_rate: Optional[float] = None
    n_estimators: Optional[int] = None
    num_leaves: Optional[int] = None
    max_depth: Optional[int] = None
    feature_fraction: Optional[float] = None
    lambda_l1: Optional[float] = None
    lambda_l2: Optional[float] = None

class Model(BaseModel):
    id: int
    name: str
    path: str

    learning_rate: Optional[float] = None
    n_estimators: Optional[int] = None
    num_leaves: Optional[int] = None
    max_depth: Optional[int] = None
    accuracy: Optional[float] = None