
// Variables globales
let mediaRecorder;
let audioChunks = [];
let chartInstance = null;

// Elementos del DOM
const micButton = document.getElementById('micButton');
const statusElement = document.getElementById('status');
const errorElement = document.getElementById('error');
const analysisContainer = document.getElementById('analysis');
const analysisText = document.getElementById('analysisText');
const chartCanvas = document.getElementById('salesChart');

// Manejar el clic en el botón del micrófono
micButton.addEventListener('click', async () => {
    try {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            stopRecording();
            return;
        }

        // Solicitar permiso para usar el micrófono
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        // Configurar el grabador de audio
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        // Evento cuando hay datos disponibles
        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        // Evento cuando se detiene la grabación
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            await sendAudioToBackend(audioBlob);
            stream.getTracks().forEach(track => track.stop());
        };

        // Iniciar grabación
        mediaRecorder.start();
        micButton.classList.add('recording');
        statusElement.textContent = "Grabando... Habla ahora. Haz clic de nuevo para detener.";

        // Detener automáticamente después de 10 segundos
        setTimeout(() => {
            if (mediaRecorder && mediaRecorder.state === 'recording') {
                stopRecording();
            }
        }, 8000);

    } catch (error) {
        showError("Error al acceder al micrófono: " + error.message);
        console.error("Error al acceder al micrófono:", error);
    }
});

// Función para detener la grabación
function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        micButton.classList.remove('recording');
        statusElement.textContent = "Procesando tu audio...";
    }
}

// Función para enviar el audio al backend
async function sendAudioToBackend(audioBlob) {
    try {
        const formData = new FormData();
        console.log("Enviando audio al backend...", audioBlob);
        formData.append('file', audioBlob, 'audio.wav');

        const response = await fetch('/procesar-audio', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const result = await response.json();

        if (result.error) {
            throw new Error(result.error);
        }

        // Mostrar resultados
        displayResults(result);

    } catch (error) {
        showError("Error al procesar el audio: " + error.message);
        console.error("Error al enviar audio:", error);
        statusElement.textContent = "";
    }
}

// Función para mostrar los resultados
function displayResults(result) {
    // Limpiar estado anterior
    errorElement.style.display = 'none';
    statusElement.textContent = "";

    // Mostrar análisis
    if (result.analisis) {
        analysisText.textContent = result.analisis;
        analysisContainer.style.display = 'block';
    }

    // Mostrar gráfico si hay configuración
    if (result.chartData) {
        // Destruir gráfico anterior si existe
        if (chartInstance) {
            chartInstance.destroy();
        }

        // Crear nuevo gráfico
        chartInstance = new Chart(
            chartCanvas.getContext('2d'),
            result.chartData
        );
    } else {
        showError("No se pudo generar el gráfico. Intenta con otra consulta.");
    }
}

// Función para mostrar errores
function showError(message) {
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}