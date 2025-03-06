from fastapi import FastAPI
import uvicorn
from app.routers.router import define_routes

app = FastAPI(docs_url="/")
define_routes(app)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000, log_level="info", reload=True, debug=True)