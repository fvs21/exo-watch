import pandas as pd
import numpy as np

def calculate_snr_from_toi_catalog(input_filepath, output_filepath):
    """
    Carga un catálogo TOI de la NASA, calcula una estimación del SNR para cada
    candidato y guarda el resultado en un nuevo archivo CSV.
    """
    print(f"Cargando datos desde: '{input_filepath}'")
    try:
        # Los archivos del Exoplanet Archive de la NASA usan '#' para comentarios
        df = pd.read_csv(input_filepath, comment='#')
        print("Datos cargados exitosamente.")
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo en la ruta: '{input_filepath}'")
        print("Asegúrate de que el nombre del archivo es correcto y está en la misma carpeta.")
        return

    # --- Cálculo del SNR ---
    required_cols = ['pl_trandep', 'pl_trandeperr1', 'pl_trandeperr2']
    if not all(col in df.columns for col in required_cols):
        missing = [col for col in required_cols if col not in df.columns]
        print(f"Error: Faltan las siguientes columnas en el archivo: {missing}")
        return

    print("Calculando la columna 'snr_calculated'...")
    # La incertidumbre inferior (err2) suele ser negativa. La incertidumbre promedio
    # se calcula como (error_superior - error_inferior) / 2.
    avg_error = (df['pl_trandeperr1'] - df['pl_trandeperr2']) / 2
    
    # Se calcula el SNR. .fillna(0) maneja casos donde los datos de error no existen.
    df['snr_calculated'] = (df['pl_trandep'] / avg_error).fillna(0)
    
    # Se reemplazan valores infinitos (si el error era 0) con 0.
    df['snr_calculated'].replace([np.inf, -np.inf], 0, inplace=True)
    
    print("Cálculo de SNR finalizado.")
    
    # Guardar el DataFrame completo con la nueva columna
    df.to_csv(output_filepath, index=False)
    print(f"Proceso completado. Archivo guardado en: '{output_filepath}'")


# --- CONFIGURACIÓN ---
# Aquí puedes cambiar los nombres de tus archivos de entrada y salida
INPUT_FILEPATH = "./data/raw/toi.csv"
OUTPUT_FILEPATH = "./data/raw/toi_with_snr.csv"


# --- EJECUCIÓN ---
# Llama a la función principal con los nombres de archivo definidos arriba
calculate_snr_from_toi_catalog(INPUT_FILEPATH, OUTPUT_FILEPATH)