import os
import tempfile
import requests
import pandas as pd
import speech_recognition as sr
from pydub import AudioSegment
from dotenv import load_dotenv
from openai import OpenAI
import re
import json

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

API_URL = os.getenv("API_URL")


def obtener_datos():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.RequestException:
        return pd.DataFrame()


def interpretar_audio(audio_file):
    """Convierte audio en texto usando SpeechRecognition y pydub."""
    recognizer = sr.Recognizer()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        try:
            audio_file.seek(0)
            audio = AudioSegment.from_file(audio_file)
            audio.export(temp_wav.name, format="wav")

            with sr.AudioFile(temp_wav.name) as source:
                audio_data = recognizer.record(source)

            text = recognizer.recognize_google(audio_data, language="es-ES")
            return text.lower()
        except (sr.UnknownValueError, sr.RequestError):
            return ""
        except Exception:
            return ""

def generar_grafica_ia(df, tipo, datos):
    prompt = (
        f"Genera directamente solo el objeto JSON con el objeto de configuración para Chart.js  y  un analisis breve de los datos ten en cuenta la moneda es USD. "
        f"El gráfico será de tipo acorde a la petición: '{tipo}'. "
        f"Datos en formato JSON: {datos}. Responde solamente con el objeto JSON "
        f"un objeto 'chartData' con de configuración para Chart.js. y un atributo 'analysis' con el analisis breve de los datos."
        f"No agregues texto adicional, explicaciones ni formato markdown."
    )


    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Eres un analista de datos que genera graficas con Chart.js"},
            {"role": "user", "content": prompt}
        ]
    )
    
    raw_output = response.choices[0].message.content.strip()
    try:
        # Detectar el bloque JSON usando expresión regular
        json_match = re.search(r"\{.*\}", raw_output, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            return json.loads(json_str)
        else:
            raise ValueError("No se encontró un objeto JSON en la respuesta.")
    except Exception as e:
        return {"error": f"❌ Error al procesar configuración JSON: {str(e)}"}


def procesar_audio_y_generar_respuesta(audio_bytes):
    """Proceso completo: interpreta audio, genera Chart.js y resumen."""
    try:
        texto = interpretar_audio(audio_bytes)
        print(f"Texto interpretado: {texto}")

        df = obtener_datos()
        if df.empty:
            return {
                "chartData": None,
                "analisis": "⚠️ No se encontraron datos en el API."
            }
        
        data = df.to_dict(orient="records")
        
        chart=generar_grafica_ia(df, texto, data)
        
        print(f"Gráfico: {chart['chartData']}","\n")
        print(f"Analisis: {chart['analysis']}","\n")

        return {
            "chartData": chart['chartData']if "chartData" in chart else None,
            "analisis":  chart['analysis'] if "analysis" in chart else "⚠️ No se pudo generar el análisis."
        }

    except Exception as e:
        print(f"Error durante el procesamiento: {str(e)}")
        # Manejo de errores, devolviendo un mensaje genérico
        return {
            "chartData": None,
            "analisis": f"❌ Error durante el análisis: {str(e)}"
        }
