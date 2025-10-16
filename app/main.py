from fastapi import FastAPI
from app.routers import nn_routes

app = FastAPI(
    title="NeuralNetLive Drawing",
    description="A project that hosts live model prediction based on user-drawn images",
    version="1.0.0"
)

# Register your routes
app.include_router(nn_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to NeuralNetLive Drawing!"}
