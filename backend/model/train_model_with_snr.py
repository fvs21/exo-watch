import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import joblib


FEATURES = [
    'orbital_period',       # Período Orbital
    'transit_epoch',      # Época del Tránsito
    'transit_duration',     # Duración del Tránsito
    'transit_depth',        # Profundidad del Tránsito
    'planet_radius',         # Radio Planetario
    'eq_temp',           # Temperatura de Equilibrio
    'insol',
    'snr',
    'steff',         # Temperatura Estelar Efectiva
    'srad',          # Radio Estelar
]

KOI_FEATURES = [
    'koi_period',       # Período Orbital
    'koi_time0bk',      # Época del Tránsito
    #'koi_impact',       # Parámetro de Impacto
    'koi_duration',     # Duración del Tránsito
    'koi_depth',        # Profundidad del Tránsito
    'koi_prad',         # Radio Planetario
    'koi_teq',          # Temperatura de Equilibrio
    'koi_insol',        # Flujo de Insolación
    'koi_model_snr',    # Relación Señal a Ruido del Tránsito
    'koi_steff',        # Temperatura Estelar Efectiva
    'koi_srad',         # Radio Estelar
]

TESS_FEATURES = [
    'pl_orbper',
    'pl_tranmid',
    'pl_trandurh',
    'pl_trandep',
    'pl_rade',
    'pl_eqt',
    'pl_insol',
    'snr_calculated',
    'st_teff',
    'st_rad'
]

def load_tess_data():
    filepath = './data/raw/toi_with_snr.csv' # Asegúrate que la ruta es correcta
    target_column = 'tfopwg_disp'

    # Lee el archivo CSV, usando 'comment=#' para ignorar las líneas de encabezado
    df_raw = pd.read_csv(filepath, comment='#')

    df_filtered = df_raw[df_raw[target_column].isin(['CP', 'FP'])]

    df_clean = df_filtered[TESS_FEATURES + [target_column]].copy()

    for col in TESS_FEATURES:
        df_clean[col].fillna(df_clean[col].median(), inplace=True)

    # --- CORRECCIÓN AQUÍ ---
    # 1. Renombra las columnas en df_clean PRIMERO
    new_col_names = {toi: general for toi, general in zip(TESS_FEATURES, FEATURES)}
    df_clean.rename(columns=new_col_names, inplace=True)

    # 2. Ahora, crea X usando los NUEVOS nombres de columnas (de la lista FEATURES)
    X = df_clean[FEATURES]
    # -----------------------

    y = df_clean[target_column].apply(lambda a : 1 if a == 'CP' else 0)

    return X, y

def load_kepler_data():
    filepath = './data/raw/koi.csv' # Asegúrate que la ruta es correcta
    target_column = 'koi_disposition'

    df_raw = pd.read_csv(filepath, skiprows=53)
    
    df_filtered = df_raw[df_raw[target_column].isin(['CONFIRMED', 'FALSE POSITIVE'])]
    
    df_clean = df_filtered[KOI_FEATURES + [target_column]].copy()
    
    for col in KOI_FEATURES:
        df_clean[col].fillna(df_clean[col].median(), inplace=True)
    
    # --- CORRECCIÓN AQUÍ ---
    # 1. Renombra las columnas en df_clean PRIMERO
    new_col_names = {koi: general for koi, general in zip(KOI_FEATURES, FEATURES)}
    df_clean.rename(columns=new_col_names, inplace=True)

    # 2. Ahora, crea X usando los NUEVOS nombres de columnas (de la lista FEATURES)
    X = df_clean[FEATURES]
    # -----------------------
    
    y = df_clean[target_column].apply(lambda x: 1 if x == 'CONFIRMED' else 0)
    
    return X, y

def main():
    """Función principal para entrenar y evaluar el modelo."""
    
    X_koi, y_koi = load_kepler_data()
    X_toi, y_toi = load_tess_data()

    X = pd.concat([X_koi, X_toi], ignore_index=True)
    y = pd.concat([y_koi, y_toi], ignore_index=True)

    # 1. Dividir los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    # 2. Crear y entrenar el modelo LightGBM
    print("\nEntrenando el modelo LightGBM...")
    model = lgb.LGBMClassifier(random_state=42)
    model.fit(X_train, y_train)
    print("¡Entrenamiento completo!")
    
    # 3. Hacer predicciones y evaluar
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nPrecisión del modelo: {accuracy * 100:.2f}%")
    print("\nReporte de Clasificación:")
    print(classification_report(y_test, y_pred, target_names=['FALSE POSITIVE', 'CONFIRMED']))
    
    # 4. Guardar el modelo entrenado para uso futuro
    model_filename = 'exoplanet_lgbm_model.joblib'
    joblib.dump(model, model_filename)
    print(f"\nModelo guardado exitosamente como '{model_filename}'")
    
    # 5. Visualizar la importancia de las características
    lgb.plot_importance(model, max_num_features=12, figsize=(10, 8), 
                        title='Importancia de las Características (LightGBM)')
    plt.tight_layout()
    plt.savefig('feature_importance_snr.png')
    print("Gráfico de importancia de características guardado como 'feature_importance_snr.png'")

if __name__ == '__main__':
    main()