from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.sintomasAPI import router as sintomas_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://healthmedufpb.netlify.app",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "null",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sintomas_router, tags=["Sintomas"])


@app.get("/")
async def raiz():
    return {"message": "Welcome to Oromaxillofacial AI Helper API"}



