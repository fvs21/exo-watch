import os
import sqlite3
from typing import Optional
from .schemas import CreateModelRequest
from .model.kepler import train_and_evaluate_model

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODELOS = os.path.join(BASE_DIR, "app", "model", "outputs")

BASE_ML_MODEL = str(os.path.join(MODELOS, "exoplanet_kepler_model.joblib"))

def get_model(id: Optional[int]) -> str:
    if id is None:
        return BASE_ML_MODEL

    conn = sqlite3.connect(os.path.join(BASE_DIR, "app", "db.sqlite3"))
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM model WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    return row[0] if row else BASE_ML_MODEL

def create_model(data: CreateModelRequest) -> int:
    conn = sqlite3.connect(os.path.join(BASE_DIR, "app", "db.sqlite3"))
    cursor = conn.cursor()

    params = data.model_dump()

    name = train_and_evaluate_model(params=params)

    cursor.execute("""
        INSERT INTO model (name, path, learning_rate, n_estimators, num_leaves, max_depth)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        os.path.join(MODELOS, f"{name}.joblib"),
        data.learning_rate,
        data.n_estimators,
        data.num_leaves,
        data.max_depth
    ))

    conn.commit()
    model_id = cursor.lastrowid
    conn.close()

    return model_id