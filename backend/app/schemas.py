from pydantic import BaseModel, Field
from typing import List, Optional, Union, Literal, Annotated

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

# LightGBM Parameters
class LightGBMParams(BaseModel):
    model_type: Literal["light_gbm"] = "light_gbm"
    learning_rate: Optional[float] = None
    n_estimators: Optional[int] = None
    num_leaves: Optional[int] = None
    max_depth: Optional[int] = None
    lambda_l1: Optional[float] = None
    lambda_l2: Optional[float] = None
    feature_fraction: Optional[float] = None
    random_state: Optional[int] = None

# XGBoost Parameters
class XGBoostParams(BaseModel):
    model_type: Literal["xgboost"] = "xgboost"
    learning_rate: Optional[float] = None
    n_estimators: Optional[int] = None
    max_depth: Optional[int] = None
    subsample: Optional[float] = None
    colsample_bytree: Optional[float] = None
    reg_lambda: Optional[float] = None
    reg_alpha: Optional[float] = None
    random_state: Optional[int] = None

# Random Forest Parameters
class RandomForestParams(BaseModel):
    model_type: Literal["random_forest"] = "random_forest"
    n_estimators: Optional[int] = None
    max_depth: Optional[int] = None
    min_samples_leaf: Optional[int] = None
    min_samples_split: Optional[int] = None
    random_state: Optional[int] = None

# Discriminated Union for Create Model Request
CreateModelRequest = Annotated[
    Union[LightGBMParams, XGBoostParams, RandomForestParams],
    Field(discriminator='model_type')
]

# Response Models
class LightGBMParamsResponse(LightGBMParams):
    id: int

class XGBoostParamsResponse(XGBoostParams):
    id: int

class RandomForestParamsResponse(RandomForestParams):
    id: int

class Model(BaseModel):
    id: int
    name: str
    path: str
    model_type: str
    accuracy: Optional[float] = None
    roc_auc: Optional[float] = None
    pr_auc: Optional[float] = None
    params: Optional[Union[LightGBMParamsResponse, XGBoostParamsResponse, RandomForestParamsResponse]] = None