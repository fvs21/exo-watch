import os
import sqlite3
from typing import Optional, Union
from .schemas import CreateModelRequest, LightGBMParams, XGBoostParams, RandomForestParams
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

def create_model(data: Union[LightGBMParams, XGBoostParams, RandomForestParams]) -> int:
    conn = sqlite3.connect(os.path.join(BASE_DIR, "app", "db.sqlite3"))
    cursor = conn.cursor()

    params = data.model_dump()
    model_type = data.model_type

    # Train the model
    name, accuracy, roc_auc, pr_auc = train_and_evaluate_model(model_type=model_type, params=params)

    # Insert parameters into the appropriate table
    params_id = None
    
    if isinstance(data, LightGBMParams):
        cursor.execute("""
            INSERT INTO lightgbm_params (
                learning_rate, n_estimators, num_leaves, max_depth,
                lambda_l1, lambda_l2, feature_fraction, random_state
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.learning_rate,
            data.n_estimators,
            data.num_leaves,
            data.max_depth,
            data.lambda_l1,
            data.lambda_l2,
            data.feature_fraction,
            data.random_state
        ))
        params_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO model (
                name, path, model_type, accuracy, roc_auc, pr_auc, lightgbm_params_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            os.path.join(MODELOS, name),
            model_type,
            accuracy,
            roc_auc,
            pr_auc,
            params_id
        ))
        
    elif isinstance(data, XGBoostParams):
        cursor.execute("""
            INSERT INTO xgboost_params (
                learning_rate, n_estimators, max_depth, subsample,
                colsample_bytree, reg_lambda, reg_alpha, random_state
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.learning_rate,
            data.n_estimators,
            data.max_depth,
            data.subsample,
            data.colsample_bytree,
            data.reg_lambda,
            data.reg_alpha,
            data.random_state
        ))
        params_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO model (
                name, path, model_type, accuracy, roc_auc, pr_auc, xgboost_params_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            os.path.join(MODELOS, name),
            model_type,
            accuracy,
            roc_auc,
            pr_auc,
            params_id
        ))
        
    elif isinstance(data, RandomForestParams):
        cursor.execute("""
            INSERT INTO randomforest_params (
                n_estimators, max_depth, min_samples_leaf, 
                min_samples_split, random_state
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            data.n_estimators,
            data.max_depth,
            data.min_samples_leaf,
            data.min_samples_split,
            data.random_state
        ))
        params_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO model (
                name, path, model_type, accuracy, roc_auc, pr_auc, randomforest_params_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            os.path.join(MODELOS, name),
            model_type,
            accuracy,
            roc_auc,
            pr_auc,
            params_id
        ))

    conn.commit()
    model_id = cursor.lastrowid
    conn.close()

    return model_id

def list_models():
    conn = sqlite3.connect(os.path.join(BASE_DIR, "app", "db.sqlite3"))
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, name, path, model_type, accuracy, roc_auc, pr_auc,
               lightgbm_params_id, xgboost_params_id, randomforest_params_id
        FROM model
    """)
    rows = cursor.fetchall()
    
    models = []
    for row in rows:
        model_id, name, path, model_type, accuracy, roc_auc, pr_auc, lgbm_id, xgb_id, rf_id = row
        
        params = None
        
        # Fetch the appropriate params based on model_type
        if model_type == "light_gbm" and lgbm_id:
            cursor.execute("""
                SELECT id, learning_rate, n_estimators, num_leaves, max_depth,
                       lambda_l1, lambda_l2, feature_fraction, random_state
                FROM lightgbm_params WHERE id = ?
            """, (lgbm_id,))
            param_row = cursor.fetchone()
            if param_row:
                params = {
                    "id": param_row[0],
                    "model_type": "light_gbm",
                    "learning_rate": param_row[1],
                    "n_estimators": param_row[2],
                    "num_leaves": param_row[3],
                    "max_depth": param_row[4],
                    "lambda_l1": param_row[5],
                    "lambda_l2": param_row[6],
                    "feature_fraction": param_row[7],
                    "random_state": param_row[8]
                }
                
        elif model_type == "xgboost" and xgb_id:
            cursor.execute("""
                SELECT id, learning_rate, n_estimators, max_depth, subsample,
                       colsample_bytree, reg_lambda, reg_alpha, random_state
                FROM xgboost_params WHERE id = ?
            """, (xgb_id,))
            param_row = cursor.fetchone()
            if param_row:
                params = {
                    "id": param_row[0],
                    "model_type": "xgboost",
                    "learning_rate": param_row[1],
                    "n_estimators": param_row[2],
                    "max_depth": param_row[3],
                    "subsample": param_row[4],
                    "colsample_bytree": param_row[5],
                    "reg_lambda": param_row[6],
                    "reg_alpha": param_row[7],
                    "random_state": param_row[8]
                }
                
        elif model_type == "random_forest" and rf_id:
            cursor.execute("""
                SELECT id, n_estimators, max_depth, min_samples_leaf, 
                       min_samples_split, random_state
                FROM randomforest_params WHERE id = ?
            """, (rf_id,))
            param_row = cursor.fetchone()
            if param_row:
                params = {
                    "id": param_row[0],
                    "model_type": "random_forest",
                    "n_estimators": param_row[1],
                    "max_depth": param_row[2],
                    "min_samples_leaf": param_row[3],
                    "min_samples_split": param_row[4],
                    "random_state": param_row[5]
                }
        
        models.append({
            "id": model_id,
            "name": name,
            "model_type": model_type,
            "accuracy": accuracy,
            "roc_auc": roc_auc,
            "pr_auc": pr_auc,
            "params": params
        })
    
    conn.close()
    return models