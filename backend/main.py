from fastapi import FastAPI
from routes import predict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Steam Insights ML API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Steam Insights ML API"}
    return {"prediction": int(prediction)}
app.include_router(predict.router)
