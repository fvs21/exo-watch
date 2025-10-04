'''aqui se supone que debe de ir el bakend'''
from fastapi import FastAPI
from app.data import routes


app = FastAPI()

app.include_router(routes.router)

@app.get("/")
def root():
    return {"Status":"Allokay"}
