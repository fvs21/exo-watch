import pandas as pd
import joblib

def predict_candidate(model_path, candidate_features):
    """Carga un modelo entrenado y predice la clasificación de un nuevo candidato."""
    
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo del modelo en '{model_path}'")
        print("Asegúrate de ejecutar 'train_model.py' primero.")
        return

    # Convierte las características del candidato en un DataFrame de Pandas
    # Es crucial que los nombres de las columnas coincidan con los del entrenamiento
    candidate_df = pd.DataFrame([candidate_features])
    
    # Realiza la predicción
    prediction_code = model.predict(candidate_df)[0]
    prediction_proba = model.predict_proba(candidate_df)[0]
    
    # Interpreta los resultados
    verdict = 'CONFIRMED' if prediction_code == 1 else 'FALSE POSITIVE'
    confidence = prediction_proba[1] if verdict == 'CONFIRMED' else prediction_proba[0]
    
    print("\n--- Veredicto del Modelo ---")
    print(f"Clasificación: {verdict}")
    print(f"Confianza: {confidence * 100:.2f}%")

if __name__ == '__main__':
    # Define las características de un candidato hipotético para probar
    # Estos son los datos de un planeta CONFIRMADO real (Kepler-186 f)
    nuevo_candidato = {
        'koi_period': 129.944,
        'koi_time0bk': 170.536,
        'koi_impact': 0.721,
        'koi_duration': 5.89,
        'koi_depth': 434.0,
        'koi_prad': 1.17,
        'koi_teq': 188,
        'koi_insol': 0.29,
        'koi_model_snr': 16.2,
        'koi_steff': 3788,
        'koi_srad': 0.52
    }
    
    # Ruta al modelo guardado
    MODEL_FILE = 'exoplanet_kepler_model.joblib'
    
    predict_candidate(MODEL_FILE, nuevo_candidato)