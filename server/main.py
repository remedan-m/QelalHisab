from fastapi import FastAPI
from .database import engine, Base
from .routers import income, expense, summary
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for specific origin (e.g., your frontend running on localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow only React app origin > https://qelal-hisab.vercel.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

Base.metadata.create_all(bind=engine)

app.include_router(income.router)
app.include_router(expense.router)
app.include_router(summary.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to QelalHisab!"}
    