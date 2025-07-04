from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
from audio_analyzer import procesar_audio_y_generar_respuesta  # Lo que refactorizamos

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/procesar-audio")
async def analizar_audio(file: UploadFile = File(...)):
    print("Recibiendo archivo de audio...")
    if not file.filename.endswith(('.wav', '.mp3', '.ogg')):
        return JSONResponse(status_code=400, content={"error": "Formato de archivo no soportado. Use .wav, .mp3 o .ogg."})
    resultado = procesar_audio_y_generar_respuesta(file.file)
    return JSONResponse(content=resultado)
