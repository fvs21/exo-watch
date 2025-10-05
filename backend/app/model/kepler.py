import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, precision_recall_curve, auc
import matplotlib.pyplot as plt
import joblib
from typing import Tuple
import sys
import xgboost as xgb
import os

KOI_FEATURES = [
    'koi_period',       # Período Orbital
    'koi_time0bk',      # Época del Tránsito
    'koi_impact',       # Parámetro de Impacto
    'koi_duration',     # Duración del Tránsito
    'koi_depth',        # Profundidad del Tránsito
    'koi_prad',         # Radio Planetario
    'koi_teq',          # Temperatura de Equilibrio
    'koi_insol',        # Flujo de Insolación
    'koi_model_snr',    # Relación Señal a Ruido del Tránsito
    'koi_steff',        # Temperatura Estelar Efectiva
    'koi_srad',         # Radio Estelar
]

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data", "raw")
OUTPUTS_PATH = os.path.join(BASE_PATH, "model", "outputs")

def load_kepler_data() -> Tuple[pd.DataFrame, pd.Series]:
    filepath = os.path.join(DATA_PATH, 'koi.csv')  # Asegúrate que la ruta es correcta
    target_column = 'koi_disposition'

    df_raw = pd.read_csv(filepath, skiprows=53)
    # 1. Separa los datos por su disposición original.
    confirmed_and_candidates = df_raw[df_raw[target_column].isin(['CONFIRMED', 'CANDIDATE'])]
    false_positives = df_raw[df_raw[target_column] == 'FALSE POSITIVE']

    # 2. Aplica tu condición de filtrado SOLO al DataFrame de Falsos Positivos.
    # Nos quedamos con los FP donde la flag 'nt' O la flag 'ss' es 1.
    condition = (false_positives['koi_fpflag_nt'] == 1) | (false_positives['koi_fpflag_ss'] == 1)
    filtered_false_positives = false_positives[condition]

    # 3. Vuelve a unir los DataFrames: los confirmados/candidatos + los FP filtrados.
    df_filtered = pd.concat([confirmed_and_candidates, filtered_false_positives])
    '''
    df_filtered = df_raw[df_raw[target_column].isin(['CONFIRMED', 'FALSE POSITIVE', 'CANDIDATE'])]


    print(df_filtered.head())
'''
    df_clean = df_filtered[KOI_FEATURES + [target_column]].copy()

    for col in KOI_FEATURES:
        df_clean[col].fillna(df_clean[col].median(), inplace=True)

    X = df_clean[KOI_FEATURES]

    y = df_clean[target_column].apply(lambda x: 1 if x in ['CONFIRMED', 'CANDIDATE'] else 0)
    
    return X, y

def use_light_gbm_model(X: pd.DataFrame, y: pd.Series, model_params: dict = None) -> Tuple[str, float, float, float]:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    model = lgb.LGBMClassifier(**model_params)

    model.fit(X_train, y_train)
    print("¡Entrenamiento completo!")
    
    # 3. Hacer predicciones y evaluar
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nPrecisión del modelo: {accuracy * 100:.2f}%")
    print("\nReporte de Clasificación:")
    print(classification_report(y_test, y_pred, target_names=['FALSE POSITIVE', 'CANDIDATE']))

    y_pred_proba = model.predict_proba(X_test)
    y_proba = y_pred_proba[:, 1]

    roc_auc = roc_auc_score(y_test, y_proba)
    precision, recall, _ = precision_recall_curve(y_test, y_proba)
    pr_auc = auc(recall, precision)

    print(f"ROC-AUC: {roc_auc:.3f}")
    print(f"PR-AUC: {pr_auc:.3f}")
    
    # 4. Guardar el modelo entrenado para uso futuro

    outputs = os.listdir(OUTPUTS_PATH)

    if len(outputs) == 0:
        model_filename = 'exoplanet_kepler_model.joblib'
    else:
        model_filename = f"exoplanet_kepler_model_v{len(outputs)+1}.joblib"

    model_path = os.path.join(OUTPUTS_PATH, model_filename)
    joblib.dump(model, model_path)
    print(f"\nModelo guardado exitosamente como '{model_filename}'")
    
    '''# 5. Visualizar la importancia de las características
    lgb.plot_importance(model, max_num_features=11, figsize=(10, 8), 
                        title='Importancia de las Características (LightGBM)')
    plt.tight_layout()
    plt.savefig('feature_importance_kepler.png')
    print("Gráfico de importancia de características guardado como 'feature_importance_kepler.png'")'''

    return model_filename, accuracy, roc_auc, pr_auc

def use_xg_boost_model(X: pd.DataFrame, y: pd.Series, model_params: dict = None) -> Tuple[str, float, float, float]:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = xgb.XGBClassifier(**model_params)

    model.fit(X_train, y_train, eval_set=[(X_test, y_test)])

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:,1]

    accuracy = accuracy_score(y_test, y_pred)

    roc_auc = roc_auc_score(y_test, y_proba)
    precision, recall, _ = precision_recall_curve(y_test, y_proba)
    pr_auc = auc(recall, precision)

    print("ROC-AUC:", roc_auc_score(y_test, y_proba))
    print("\nReporte de clasificación:\n", classification_report(y_test, y_pred))

    # 5. Visualizar la importancia de las características
    outputs = os.listdir(OUTPUTS_PATH)

    if len(outputs) == 0:
        model_filename = 'exoplanet_kepler_model_xgb.joblib'
    else:
        model_filename = f"exoplanet_kepler_model_v{len(outputs)+1}.joblib"

    model_path = os.path.join(OUTPUTS_PATH, model_filename)
    joblib.dump(model, model_path)
    print(f"\nModelo guardado exitosamente como '{model_filename}'")

    return model_filename, accuracy, roc_auc, pr_auc 

def use_randomforest_model(X: pd.DataFrame, y: pd.Series, model_params: dict = None) -> Tuple[str, float, float, float]:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    # n_jobs=-1 usa todos los núcleos de tu CPU para acelerar el entrenamiento
    model = RandomForestClassifier(**model_params)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print(f"Precisión de Random Forest: {accuracy * 100:.2f}%")

    print(classification_report(y_test, y_pred, target_names=['FALSE POSITIVE', 'CANDIDATE'])) 
    y_pred_proba = model.predict_proba(X_test)

    y_proba = y_pred_proba[:, 1]

    roc_auc = roc_auc_score(y_test, y_proba)
    precision, recall, _ = precision_recall_curve(y_test, y_proba)
    pr_auc = auc(recall, precision)

    print(f"ROC-AUC: {roc_auc:.3f}")
    print(f"PR-AUC: {pr_auc:.3f}") 

    outputs = os.listdir(OUTPUTS_PATH)

    if len(outputs) == 0:
        model_filename = 'exoplanet_kepler_model_randomforest.joblib'
    else:
        model_filename = f"exoplanet_kepler_model_v{len(outputs)+1}.joblib"

    model_path = os.path.join(OUTPUTS_PATH, model_filename)

    joblib.dump(model, model_path)

    print(f"\nModelo guardado exitosamente como '{model_filename}'") 

    return model_filename, accuracy, roc_auc, pr_auc

def train_and_evaluate_model(model_type: str = "light_gbm", params: dict = None):
    X, y = load_kepler_data()

    params = {k: v for k, v in params.items() if v is not None}
    
    if model_type == "light_gbm":
        return use_light_gbm_model(X, y, model_params=params)
    elif model_type == "xgboost":
        return use_xg_boost_model(X, y, model_params=params)
    elif model_type == "random_forest":
        return use_randomforest_model(X, y, model_params = params)
    else:
        raise ValueError("Modelo no soportado. Usa 'light_gbm', 'xgboost' o 'random_forest'.")


def main():
    """Función principal para entrenar y evaluar el modelo.""" 
    if len(sys.argv) == 1:
        model_to_use = "light_gbm"
    else:
        model_to_use = sys.argv[1]

    params = None
    if model_to_use == "light_gbm":
        params = dict(
            random_state=42,
            learning_rate=0.05,
            n_estimators=1000, # Reducido para un entrenamiento más rápido
            num_leaves=40,
            feature_fraction=0.8,
            lambda_l1=0.1,
            lambda_l2=0.1,
            n_jobs=-1
        )
    elif model_to_use == "xgboost":
        params = dict(
            objective="binary:logistic",
            eval_metric="auc",
            n_estimators=1000, # Reducido para un entrenamiento más rápido
            learning_rate=0.02,
            max_depth=8,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_lambda=1.0,
            reg_alpha=0.1,
            random_state=42,
            n_jobs=-1
        )
    elif model_to_use == "random_forest":
        params = dict(
            n_estimators=300, # Un buen punto de partida
            max_depth=15,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1
        )

    train_and_evaluate_model(model_type=model_to_use, params=params)

if __name__ == '__main__':
    main()
