import os
from pydantic import BaseModel
import sqlite3
from typing import Optional

BASE_DIR=os.path.dirname(os.path.dirname(__file__))
MODELOS=os.path.join(BASE_DIR, "..", "model")

BASE_ML_MODEL = str(os.path.join(MODELOS, "exoplanet_kepler_model.joblib"))

def get_model(id: Optional[int]) -> str:
    if id is None:
        return BASE_ML_MODEL
    
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
    cursor = conn.cursor()
    cursor.execute("SELECT model_path FROM models WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    return row[0] if row else BASE_ML_MODEL

MODEL_MAP={
    "Modelo (TESS)": "exoplanet_tess_model.joblib",
    "Modelo (Kepler)": "exoplanet_kepler_model.joblib",
    "Libre (6 campos)": "exoplanet_lgbm_model.joblib"
}

_modelo_activo = str(os.path.join(MODELOS, "exoplanet_kepler_model.joblib"))

class ChangeModel(BaseModel):
    model_path: str

def get_modelo_activo() -> str: #eliminar en un futuro no es necesario
    return _modelo_activo

def cambiar_modelo(req: ChangeModel) -> dict:
    global _modelo_activo
    _modelo_activo = os.path.join(MODELOS, req.model_path)
    return {"Nuevo modelo": req.model_path}

def get_model_path(model_name: str) -> str:
    file=MODEL_MAP.get(model_name)
    if not file:
        raise ValueError(f"Modelo no encontrado: {model_name}")
    return os.path.join(MODELOS, file)
