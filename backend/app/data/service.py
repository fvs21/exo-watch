import os
from pydantic import BaseModel


BASE_DIR=os.path.dirname(os.path.dirname(__file__))
MODELOS=os.path.join(BASE_DIR, "..", "model")

_modelo_activo = str(os.path.join(MODELOS, "exoplanet_kepler_model.joblib"))

class ChangeModel(BaseModel):
    model_path: str

def get_modelo_activo() -> str:
    return _modelo_activo

def cambiar_modelo(req: ChangeModel) -> dict:
    global _modelo_activo
    _modelo_activo = os.path.join(MODELOS, req.model_path)
    return {"Nuevo modelo": req.model_path}

