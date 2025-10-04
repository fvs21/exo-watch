from fastapi import APIRouter, HTTPException
from .schemas import CreateModelRequest, PredictRequest
from . import service
from fastapi import UploadFile
from .model.predict import predict_candidate

router = APIRouter(prefix="/api", tags=["api"])

@router.post("/predict")
def predict(req: PredictRequest):
    model_path = service.get_model(req.model)

    verdict, confidence = predict_candidate(model_path, req.features.model_dump())

    if verdict is None or confidence is None:
        raise HTTPException(status_code=500, detail="La predicción falló.")

    return {"status": "success", "prediction": {"verdict": verdict, "confidence": confidence}}

@router.post("/model")
def create_model(req: CreateModelRequest):
    model_id = service.create_model(req)
    return {"status": "success", "model_id": model_id}

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
