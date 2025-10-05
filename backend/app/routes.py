from fastapi import APIRouter, HTTPException, Form
from .schemas import CreateModelRequest, PredictRequest
from . import service
from fastapi import UploadFile
from .model.predict import predict_candidate, KOI_FEATURES
import pandas as pd
import io

router = APIRouter(prefix="/api", tags=["api"])

@router.post("/predict")
def predict(req: PredictRequest):
    model_path = service.get_model(req.model)

    verdict, confidence = predict_candidate(model_path, req.features.model_dump())

    if verdict is None or confidence is None:
        raise HTTPException(status_code=500, detail="La predicción falló.")
    
    return {"status": "success", "prediction": {"verdict": verdict, "confidence": float(confidence)}}

@router.post("/model")
def create_model(req: CreateModelRequest):
    model_id = service.create_model(req)
    return {"status": "success", "model_id": model_id}

@router.post("/predict_csv")
async def predict_csv(file: UploadFile, model: int = Form(None)):

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV válido.")

    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al leer el CSV: {str(e)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="El archivo CSV está vacío.")

    #Normalizar nombres de columnas
    df.columns = df.columns.str.strip().str.lower()

    #Crear diccionario para renombrar columnas automáticamente
    COLUMN_MAP = {tce: koi for koi, tce in KOI_FEATURES}

    #Renombrar las columnas que coincidan con las alternativas
    df.rename(columns=COLUMN_MAP, inplace=True)

    koi_cols = [koi for koi, _ in KOI_FEATURES]
    cols_present = [c for c in koi_cols if c in df.columns]
    missing_cols = [c for c in koi_cols if c not in df.columns]

    if len(cols_present) == 0:
        raise HTTPException(status_code=400, detail="El CSV no contiene columnas reconocibles para KOI_FEATURES.")

    #Si faltan columnas, completarlas con 0
    if missing_cols:
        for col in missing_cols:
            df[col] = 0

    # Mantener solo las columnas relevantes
    df = df[koi_cols]
    df = df.apply(pd.to_numeric, errors='coerce').fillna(0)

    model_path = service.get_model(model)

# Realizar predicciones fila por fila
    predictions = []
    for _, row in df.iterrows():
        features = row.to_dict()
        verdict, confidence = predict_candidate(model_path, features)
        predictions.append({
            "prediction": {
                "verdict": verdict,
                "confidence": float(confidence)
            }
        })

    return {"status": "success", "count": len(predictions), "predictions": predictions}


@router.get("/models")
def list_models():
    models = service.list_models()
    return {"status": "success", "models": models}
