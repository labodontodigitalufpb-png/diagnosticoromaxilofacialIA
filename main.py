from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.sintomasAPI import router as sintomas_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://healthmedufpb.netlify.app",
        "https://labodontodigitalufpb-png.github.io",
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


@app.middleware("http")
async def add_static_cache_headers(request, call_next):
    response = await call_next(request)
    if request.url.path in {"/", "/index.html", "/logo.png"}:
        response.headers["Cache-Control"] = "no-store, max-age=0"
        response.headers["Pragma"] = "no-cache"
    return response


@app.get("/health")
async def raiz():
    return {"message": "Welcome to Oromaxillofacial AI Helper API"}


app.mount("/", StaticFiles(directory="www", html=True), name="static")



