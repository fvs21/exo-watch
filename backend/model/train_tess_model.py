import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import joblib


TESS_FEATURES = [
    'pl_orbper',
    'pl_tranmid',
    'pl_trandurh',
    'pl_trandep',
    'pl_rade',
    'pl_eqt',
    'pl_insol',
    'st_teff',
    'st_rad'
]

def load_tess_data():
    filepath = './data/raw/toi.csv'
    target_column = 'tfopwg_disp'

    df_raw = pd.read_csv(filepath, skiprows=69)

    df_filtered = df_raw[df_raw[target_column].isin(['CP', 'FP'])]

    df_clean = df_filtered[TESS_FEATURES + [target_column]].copy()

    for col in TESS_FEATURES:
        df_clean[col].fillna(df_clean[col].median(), inplace=True)

    X = df_clean[TESS_FEATURES]

    y = df_clean[target_column].apply(lambda a : 1 if a == 'CP' else 0)


    return X, y

def main():
    """Función principal para entrenar y evaluar el modelo."""
    

    X, y = load_tess_data()

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
    model_filename = 'exoplanet_tess_model.joblib'
    joblib.dump(model, model_filename)
    print(f"\nModelo guardado exitosamente como '{model_filename}'")
    
    # 5. Visualizar la importancia de las características
    lgb.plot_importance(model, max_num_features=12, figsize=(10, 8), 
                        title='Importancia de las Características (LightGBM)')
    plt.tight_layout()
    plt.savefig('feature_importance_tess.png')
    print("Gráfico de importancia de características guardado como 'feature_importance_tess.png'")

if __name__ == '__main__':
    main()