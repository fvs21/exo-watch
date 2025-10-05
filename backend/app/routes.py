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
    
    print(model_path)

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
    
@router.get("/models")
def list_models():
    models = service.list_models()
    return {"status": "success", "models": models}
