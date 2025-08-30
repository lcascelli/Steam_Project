from fastapi import FastAPI
from routes import predict

app = FastAPI(title="Steam Insights ML API")

app.include_router(predict.router)
