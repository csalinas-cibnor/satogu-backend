from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/cuadrantes_frios")
def cuadrantes_frios(umbral: float = Query(18.0)) -> List[dict]:
    try:
        df = pd.read_csv("datos_cuadrantes_frios.csv")
        filtrado = df[df["tsm_media"] < umbral]
        return filtrado[["lat", "lon"]].to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}