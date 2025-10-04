from fastapi import APIRouter, HTTPException, Status
from app.data import services
from ...model.predict import predict_candidate
from pydantic import BaseModel
from schemas import CandidateFeatures
import pandas as pd
from . import service
from fastapi import UploadFile

router = APIRouter(prefix="/api", tags=["api"])

#---Predict endpoint---
@router.post("/predict")
def predict(features: CandidateFeatures):
    features_dict = features.model_dump()

    model_path = service.get_model(features_dict.get("model"))
    
    prediction = predict_candidate(model_path, features_dict)
    
    if prediction is None:
        raise HTTPException(status_code=500, detail="La predicción falló.")

    return {"status": "success", "input":features_dict, "prediction": prediction}

@router.post("/predict_csv")
def predict_csv(file: UploadFile, model: int = None):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un archivo CSV.")

    model_path = service.get_model(model)

    try:
        df = pd.read_csv(file.file)
        features_list = df.to_dict(orient='records')
        
        predictions = []
        for features in features_list:
            prediction = predict_candidate(model_path, features)
            if prediction is None:
                raise HTTPException(status_code=500, detail="La predicción falló para una de las filas.")
            predictions.append(prediction)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo no encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    return {"status": "success", "predictions": predictions}

@router.post("/create")
def create(hyperparams: services.HyperParams):
    try:
        services.create(hyperparams)
        return {"status": "success", "message": "Datos creados exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))