import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, precision_recall_curve, auc
import matplotlib.pyplot as plt
import joblib


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

def load_kepler_data():
    filepath = './data/raw/koi.csv' # Asegúrate que la ruta es correcta
    target_column = 'koi_disposition'

    df_raw = pd.read_csv(filepath, skiprows=53)
    
    df_filtered = df_raw[df_raw[target_column].isin(['CONFIRMED', 'FALSE POSITIVE', 'CANDIDATE'])]
    
    df_clean = df_filtered[KOI_FEATURES + [target_column]].copy()
    
    for col in KOI_FEATURES:
        df_clean[col].fillna(df_clean[col].median(), inplace=True)

    X = df_clean[KOI_FEATURES]

    y = df_clean[target_column].apply(lambda x: 1 if x in ['CONFIRMED', 'CANDIDATE'] else 0)
    
    return X, y

def main():
    """Función principal para entrenar y evaluar el modelo.""" 
    X, y = load_kepler_data()

    # 1. Dividir los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    # 2. Crear y entrenar el modelo LightGBM
    print("\nEntrenando el modelo LightGBM...")
    model = lgb.LGBMClassifier(
        random_state=42
    )

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
    model_filename = 'exoplanet_kepler_model.joblib'
    joblib.dump(model, model_filename)
    print(f"\nModelo guardado exitosamente como '{model_filename}'")
    
    # 5. Visualizar la importancia de las características
    lgb.plot_importance(model, max_num_features=11, figsize=(10, 8), 
                        title='Importancia de las Características (LightGBM)')
    plt.tight_layout()
    plt.savefig('feature_importance_kepler.png')
    print("Gráfico de importancia de características guardado como 'feature_importance_kepler.png'")

if __name__ == '__main__':
    main()