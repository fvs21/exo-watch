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

    name, accuracy, roc_auc, pr_auc = train_and_evaluate_model(params=params)

    cursor.execute("""
        INSERT INTO model (name, path, learning_rate, n_estimators, num_leaves, max_depth, lambda_l1, lambda_l2, feature_fraction, random_state, accuracy, roc_auc, pr_auc)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        os.path.join(MODELOS, name),
        data.learning_rate,
        data.n_estimators,
        data.num_leaves,
        data.max_depth,
        data.lambda_l1,
        data.lambda_l2,
        data.feature_fraction,
        data.random_state,
        accuracy,
        roc_auc,
        pr_auc
    ))

    conn.commit()
    model_id = cursor.lastrowid
    conn.close()

    return model_id

def list_models():
    conn = sqlite3.connect(os.path.join(BASE_DIR, "app", "db.sqlite3"))
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, path, learning_rate, n_estimators, num_leaves, max_depth, lambda_l1, lambda_l2, feature_fraction, random_state, accuracy, roc_auc, pr_auc FROM model")
    rows = cursor.fetchall()
    conn.close()

    models = []
    for row in rows:
        models.append({
            "id": row[0],
            "name": row[1], 
            "learning_rate": row[3],
            "n_estimators": row[4],
            "num_leaves": row[5],
            "max_depth": row[6],
            "lambda_l1": row[7],
            "lambda_l2": row[8],
            "feature_fraction": row[9],
            "random_state": row[10],
            "accuracy": row[11],
            "roc_auc": row[12],
            "pr_auc": row[13]
        })
    return models