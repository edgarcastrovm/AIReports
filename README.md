
# AIReports

**AIReports** es una solución basada en inteligencia artificial para la generación automatizada de reportes y análisis gráficos a partir de datos de ventas simulados y comandos de voz del usuario.

---

## 🚀 Descripción del Proyecto

Este proyecto consta de dos aplicaciones principales:

### 1. API de Datos (api/)
Una API simulada que proporciona datos de ventas en formato JSON. Los datos se generan de forma mock y se almacenan en la carpeta `data/ventas.json`.

### 2. Agente Inteligente (agent/)
Una aplicación que:

- Permite capturar audio desde el navegador.
- Transcribe el audio a texto usando reconocimiento de voz.
- Consulta la API de ventas simuladas.
- Utiliza un modelo de OpenAI para interpretar los datos y generar:
  - Un análisis textual.
  - Un gráfico con Chart.js.
- Renderiza el resultado en la interfaz web (`index.html`), mostrando el gráfico y el análisis de manera clara al usuario.

---

## 📦 Estructura del Proyecto

```
./
├── agent/
│   ├── audio_analyzer.py             # Analiza audio, transcribe y consulta OpenAI
│   ├── env.txt                       # Ejemplo configuración archivo '.env'
│   ├── gen_mock_data.py              # Generador de datos simulados
│   ├── main.py                       # Punto de entrada del servidor FastAPI
│   ├── requirements.txt              # Dependencias del agente
│   ├── static/
│   │   ├── css/
│   │   │   └── site.css              # Estilos frontend
│   │   └── js/
│   │       └── site.js               # Scripts frontend
│   └── templates/
│       └── index.html                # Interfaz para grabar audio y ver resultados
├── api/
│   ├── data/
│   │   └── ventas.json               # Archivo de datos mock
│   ├── index.js                      # Lógica de la API (Express.js)
│   ├── package.json                  # Configuración del proyecto API (Node.js)
│   └── package-lock.json
└── README.md                         # Descripción del proyecto
```

---

## 🔧 Instalación

### 1. Clona el repositorio

```bash
git clone https://github.com/edgarcastrovm/AIReports.git
cd AIReports
```

### 2. Instala dependencias del Agente (Python)

```bash
cd agent
pip install -r requirements.txt
```

O directamente:

```bash
pip install pydub fastapi uvicorn jinja2 requests pandas openai speechrecognition
```

### 3. Configurar apiKey de OpenApi

Crear un archivo `.env` con el siguiente contenido.

**OPENAI_API_KEY** apykey obtenida de la consola administradore de OpenIA

**API_URL** url en la que se ejecuta nuestra api proveedora de datos

```properties
OPENAI_API_KEY=KEY_VALUE
API_URL=http://localhost:3000/api/ventas
```

### 4. Instala dependencias del API (Node.js)

```bash
cd ../api
npm install
```

---

## ▶️ Ejecución

### Ejecutar API de Datos

```bash
cd api
node index.js
```

### Ejecutar Agente IA (Servidor FastAPI)

```bash
cd agent
uvicorn main:app --reload
```

Luego abre tu navegador en: [http://localhost:8000](http://localhost:8000)

---

## 🎤 ¿Cómo funciona?

1. El usuario graba un audio diciendo algo como:  
   _"Muéstrame las ventas de huevos durante junio por vendedor."_
2. El audio es transcrito a texto.
3. Se consulta la API para obtener los datos relevantes.
4. OpenAI analiza los datos, genera un análisis y un gráfico en formato JSON para Chart.js.
5. El gráfico se muestra en la misma página (`index.html`) junto al análisis generado.

---

## 📁 Datos Simulados

El archivo `api/data/ventas.json` contiene datos de ejemplo generados con `gen_mock_data.py`, incluyendo información como:

- Producto
- Cantidad vendida
- Precio unitario
- Vendedor
- Fecha de la venta

---

## 📜 Licencia

MIT License — libre para modificar, usar y distribuir con fines educativos o comerciales.

---

## 🤖 Créditos

Proyecto impulsado con FastAPI, Chart.js, OpenAI y tecnologías web modernas.
