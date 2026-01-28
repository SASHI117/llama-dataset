from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(title="Farm Vaidya AI Backend")

# Allow Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later you can restrict to your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok"}

app.include_router(router)
