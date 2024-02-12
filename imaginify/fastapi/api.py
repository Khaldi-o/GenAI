

# ------------------- IMPORT LIBRAIRIES -------------- #
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from util.auth import jwtBearer
import uvicorn
# ----------------------------------------------------- #


# ------------------- IMPORT ROUTES ------------------ #
from routes.test import router_test
from routes.gen import router_gen
from routes.post import router_post
from routes.auth import router_auth
import logging
import os

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Configure logging
logging.basicConfig(level=logging.INFO)
# ----
app = FastAPI()
# ----
origins = ["http://localhost:3000"]
if FRONTEND_URL != "http://localhost:3000":
    origins = [FRONTEND_URL, "http://localhost:3000"]

# Set up CORS middleware options
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.mount("/data", StaticFiles(directory="data"), name="data")


@app.get("/")
async def root():
    return {"message": "alive"}



app.include_router(router_auth, 
                   tags=["auth"]
)

app.include_router(router_test,
                   tags=["test"],
                   dependencies=[Depends(jwtBearer())]
)

app.include_router(router_gen,
                   tags=["gen"],
                   dependencies=[Depends(jwtBearer())]
)

app.include_router(router_post,
                   tags=["post"],
                   dependencies=[Depends(jwtBearer())]
)

# ----------------------------------------------------- #


# Run this only if this script is executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")



