#!/usr/bin/python3

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse
import uvicorn
import requests
import htmx

from fastapi.staticfiles import StaticFiles

app = FastAPI() 

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


if __name__ == "__main__":
    uvicorn.run(app="main:app",host="0.0.0.0", reload=True)

# @app.post("/submit")
# async def submit_form(request: Request):
#     form_data = await request.form()
#     # Process form_data as needed
#     return htmx.json_response({"message": "Form submitted successfully!"})
