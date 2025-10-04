from fastapi import APIRouter, HTTPException, Status
from . import services
from app.model.predict import predict_candidate
from pydantic import BaseModel
from .serializers import CandidateFeatures
import pandas as pd

router = APIRouter(prefix="/api", tags=["api"])

#---Predict endpoint---
@router.get("/predict")
def predict(features: CandidateFeatures):
    MODEL_PATH=services.CURRENT_MODEL_PATH #define la ruta del modelo

    features_dict=features.model_dump()
    
    prediction = predict_candidate(MODEL_PATH, features_dict)
    if prediction is None:
        raise HTTPException(status_code=500, detail="La predicción falló.")

    return {"status": "success", "input":features_dict, "prediction": prediction} #retorna {"status": "success", "input":features_dict, "prediction": prediction}

@router.get("/predict_csv")
def predict_csv(file_path: str):
    MODEL_PATH="RUTA DEL MODELO" #define la ruta del modelo

    try:
        df = pd.read_csv(file_path)
        features_list = df.to_dict(orient='records')
        
        predictions = []
        for features in features_list:
            prediction = predict_candidate(MODEL_PATH, features)
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



@router.post("/change")
