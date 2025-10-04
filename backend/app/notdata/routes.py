from fastapi import APIRouter, HTTPException
from model.predict import predict_candidate
from app.notdata.schemas import CandidateFeatures
from app.notdata import service
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
    
'''def predict(req: dict):
    modelo=req.get("modeloSeleccionado")
    features=req.get("datos")

    if not modelo or not features:
        raise HTTPException(status_code=400, detail="Faltan datos en la solicitud.")
    
    try:
        modelo_ruta=service.get_model_path(modelo) #obtiene la ruta del modelo basado en el diccionario de los nombres bonitos
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    prediction = predict_candidate(modelo_ruta, features)
    if not prediction:
        raise HTTPException(status_code=500, detail="La predicción falló.")

    return {"status": "success", "input":features, "prediction": prediction}'''
    
    
@router.get("/predict_csv")
def predict_csv(file_path: str):
    MODEL_PATH=service.get_modelo_activo() #define la ruta del modelo

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
def create(hyperparams: service.HyperParams):
    try:
        service.create(hyperparams)
        return {"status": "success", "message": "Datos creados exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
