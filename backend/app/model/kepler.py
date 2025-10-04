import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, precision_recall_curve, auc
import matplotlib.pyplot as plt
import joblib
from typing import Tuple
import sys
import xgboost as xgb

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

def load_kepler_data() -> Tuple[pd.DataFrame, pd.Series]:
    filepath = './data/raw/koi.csv' # Asegúrate que la ruta es correcta
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

def use_light_gbm_model(X: pd.DataFrame, y: pd.Series, model_params: dict = None):
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
    model_filename = 'outputs/exoplanet_kepler_model.joblib'
    joblib.dump(model, model_filename)
    print(f"\nModelo guardado exitosamente como '{model_filename}'")
    
    # 5. Visualizar la importancia de las características
    lgb.plot_importance(model, max_num_features=11, figsize=(10, 8), 
                        title='Importancia de las Características (LightGBM)')
    plt.tight_layout()
    plt.savefig('feature_importance_kepler.png')
    print("Gráfico de importancia de características guardado como 'feature_importance_kepler.png'")

def use_xg_boost_model(X: pd.DataFrame, y: pd.Series):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = xgb.XGBClassifier(
        objective="binary:logistic",
        eval_metric="auc",
        n_estimators=2000,
        learning_rate=0.02,
        max_depth=8,           # deeper trees
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=(y_train.value_counts()[0] / y_train.value_counts()[1]),
        reg_lambda=1.0,        # L2 regularization
        reg_alpha=0.1,         # L1 regularization
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train, eval_set=[(X_test, y_test)])

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:,1]

    print("ROC-AUC:", roc_auc_score(y_test, y_proba))
    print("\nReporte de clasificación:\n", classification_report(y_test, y_pred))

    # 5. Visualizar la importancia de las características
    xgb.plot_importance(model)
    plt.title("XGBoost Feature Importance")
    plt.tight_layout()
    plt.savefig('feature_importance_kepler_xgb.png')
    print("Gráfico de importancia de características guardado como 'feature_importance_kepler_xgb.png'")

def train_and_evaluate_model(model_type: str = "light_gbm", params: dict = None):
    X, y = load_kepler_data()
    
    if model_type == "light_gbm":
        use_light_gbm_model(X, y, model_params=params)
    elif model_type == "xgboost":
        use_xg_boost_model(X, y, model_params=params)
    else:
        raise ValueError("Modelo no soportado. Usa 'light_gbm' o 'xgboost'.")


def main():
    """Función principal para entrenar y evaluar el modelo.""" 
    if len(sys.argv) == 1:
        model_to_use = "light_gbm"
    else:
        model_to_use = sys.argv[1]

    params = dict(
        random_state=42,
        learning_rate=0.05,
        n_estimators=2000,
        num_leaves=40,
        feature_fraction=0.8,
        lambda_l1=0.1,
        lambda_l2=0.1,
    ) if model_to_use == "light_gbm" else None

    train_and_evaluate_model(model_type=model_to_use, params=params)

if __name__ == '__main__':
    main()
