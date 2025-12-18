from fastapi import FastAPI
from routes import predict
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Steam Insights ML API")
app.add_middleware(
    CORSMiddleware,
    allow_origins="https://lc-da-portfolio.netlify.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Steam Insights ML API"}

