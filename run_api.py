import uvicorn

from api import app

if __name__ == '__main__':
    uvicorn.run("run_api:app", host="localhost", port=8080, reload=True, workers=3)
