#!/usr/bin/python3

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse
import uvicorn
import requests

from fastapi.staticfiles import StaticFiles

app = FastAPI() 

# Mount the "static" directory as a route to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)  
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})

@app.get("/characters", response_class=HTMLResponse)  
async def read_root(request: Request):

    response = requests.get("https://rickandmortyapi.com/api/character")
    data = response.json()
    print(data["results"])

    return templates.TemplateResponse("index.html", context={"request": request, "results": data["results"]})


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)