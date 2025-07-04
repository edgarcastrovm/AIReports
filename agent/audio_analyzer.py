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

API_URL = "http://localhost:3000/api/ventas"


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


def generar_resumen_ia(df, tipo, datos):
    prompt = (
        f"Analiza los datos de ventas y genera un breve resumen en español sobre la petición del usuario:'{tipo}'. Datos json: {datos}. Responde solo con el análisis, sin explicaciones adicionales."
        f"No agregues formato markdown."
    )

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Eres un analista de datos."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def generar_grafica_ia(df, tipo, datos):
    prompt = (
        f"Genera directamente solo el objeto JSON (sin envolverlo en una variable ni usar 'const') "
        f"de configuración para Chart.js. El gráfico será de tipo acorde a la petición: '{tipo}'. "
        f"Datos en formato JSON: {datos}. Responde solamente con el objeto JSON de configuración para Chart.js. "
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
        
        data = data_json = df.to_dict(orient="records")
        #print(f"Datos del gráfico: {data}")
        
        chart=generar_grafica_ia(df, texto, data)
        
        
        print(f"Gráfico: {chart}")
        
        analisis = generar_resumen_ia(df, texto, data)

        return {
            "chartData": chart,
            "analisis": analisis
        }

    except Exception as e:
        return {
            "chartData": None,
            "analisis": f"❌ Error durante el análisis: {str(e)}"
        }
