import pandas as pd
import joblib
import sys
import csv

KOI_FEATURES = [
    ('koi_period', 'tce_period'),       # Período Orbital
    ('koi_time0bk', 'tce_time0bk'),      # Época del Tránsito
    ('koi_impact', 'tce_impact'),       # Parámetro de Impacto
    ('koi_duration', 'tce_duration'),     # Duración del Tránsito
    ('koi_depth', 'tce_depth'),        # Profundidad del Tránsito
    ('koi_prad', 'tce_prad'),         # Radio Planetario
    ('koi_teq', 'tce_eqt'),          # Temperatura de Equilibrio
    ('koi_insol', 'tce_insol'),        # Flujo de Insolación
    ('koi_model_snr', 'tce_model_snr'),    # Relación Señal a Ruido del Tránsito
    ('koi_steff', 'tce_steff'),        # Temperatura Estelar Efectiva
    ('koi_srad', 'tce_sradius'),         # Radio Estelar
]

def predict_candidate(model_path, candidate_features):
    """Carga un modelo entrenado y predice la clasificación de un nuevo candidato."""
    
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo del modelo en '{model_path}'")
        print("Asegúrate de ejecutar 'train_model.py' primero.")
        return
    
    # Convierte los valores numéricos que vengan como string
    for k, v in candidate_features.items():
        try:
            candidate_features[k] = float(v)
        except (ValueError, TypeError):
            pass  # deja el valor tal cual si no puede convertirse

    candidate_df = pd.DataFrame([candidate_features])

    # Convierte las características del candidato en un DataFrame de Pandas
    # Es crucial que los nombres de las columnas coincidan con los del entrenamiento
    candidate_df = pd.DataFrame([candidate_features])
    
    # Realiza la predicción
    prediction_code = model.predict(candidate_df)[0]
    prediction_proba = model.predict_proba(candidate_df)[0]
    
    # Interpreta los resultados
    verdict = 'CANDIDATE' if prediction_code == 1 else 'FALSE POSITIVE'
    confidence = prediction_proba[1] if verdict == 'CANDIDATE' else prediction_proba[0]
    
    print("\n--- Veredicto del Modelo ---")
    print(f"Clasificación: {verdict}")
    print(f"Confianza: {confidence * 100:.2f}%")

    return verdict, confidence

def main():
    """Función principal para probar la predicción con un candidato de ejemplo."""

    raw = pd.read_csv("./data/raw/events.csv", skiprows=32)
    MODEL_FILE = 'exoplanet_kepler_model.joblib'
    csvfile = open('predictions.csv', 'w', newline='')
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['kepid', 'verdict', 'confidence'])

    if len(sys.argv) < 2:
        for row in raw.iterrows():
            first = row[1].to_dict()
            nuevo_candidato = { k1: first[k2] for k1, k2 in KOI_FEATURES }
            print(f"\nProbando candidato con kepid={first['kepid']}")
            verdict, confidence = predict_candidate(MODEL_FILE, nuevo_candidato)
            csvwriter.writerow([first['kepid'], verdict, f"{confidence * 100:.2f}%"])
            print("-" * 30)

        csvfile.close()

    else:
        kepid = int(sys.argv[1])

        signal = raw[raw['kepid'] == kepid]
        first = signal.iloc[0].to_dict()

        nuevo_candidato = { k1: first[k2] for k1, k2 in KOI_FEATURES }
        
        predict_candidate(MODEL_FILE, nuevo_candidato)


if __name__ == '__main__':
    # Define las características de un candidato hipotético para probar
    # Estos son los datos de un planeta CONFIRMADO real (Kepler-186 f)

    main()