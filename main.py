#!/usr/bin/python3

from typing import Optional
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse
import uvicorn
import requests
import htmx

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
app = FastAPI() 


app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with the list of allowed origins (or use "*" for any origin)
    allow_methods=["*"],  # Replace with the list of allowed HTTP methods (e.g., ["GET", "POST"])
    allow_headers=["*"],  # Replace with the list of allowed headers
)

# Mount the "static" directory as a route to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/home", response_class=HTMLResponse)  
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})

@app.get("/", response_class=HTMLResponse)  
async def read_root(request: Request):

    response = requests.get("https://rickandmortyapi.com/api/character")
    data = response.json()

    return templates.TemplateResponse("character_card.html", context={"request": request, "characters": data["results"]})

@app.get("/data", response_class=HTMLResponse)  
async def read_data(request: Request, search: Optional[str]=Query(None)):
    if search:
        response = requests.get(f"https://rickandmortyapi.com/api/character/?name={search}")
        data = response.json()
    else:
        response = requests.get(f"https://rickandmortyapi.com/api/character")
        data = response.json()
        
    return templates.TemplateResponse("character_card.html", context={"request": request, "characters": data["results"]})


if __name__ == "__main__":
    uvicorn.run(app="main:app",host="0.0.0.0", reload=True)

# @app.post("/submit")
# async def submit_form(request: Request):
#     form_data = await request.form()
#     # Process form_data as needed
#     return htmx.json_response({"message": "Form submitted successfully!"})
