from fastapi.middleware.cors import CORSMiddleware
from router import file_router, folder_router
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Include routers for file and folder endpoints
app.include_router(file_router)
app.include_router(folder_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with the list of allowed origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Add the allowed HTTP methods
    allow_headers=["*"],  # Allow all headers for simplicity. You can restrict this based on your requirements.
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
