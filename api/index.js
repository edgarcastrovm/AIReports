const express = require('express');
const fs = require('fs');
const cors = require('cors');

const app = express();
const PORT = 3000;

app.use(cors());

app.get('/api/ventas', (req, res) => {
  console.log('Solicitud recibida para /api/ventas');
  // Leer el archivo ventas.json

  fs.readFile('data/ventas.json', 'utf8', (err, data) => {
    if (err) {
      console.error('Error leyendo ventas.json:', err);
      return res.status(500).json({ error: 'Error interno del servidor' });
    }
    const ventas = JSON.parse(data);
    console.log('Datos de ventas leídos correctamente');
    // Enviar los datos como respuesta
    console.log(`Enviando ${ventas.length} registros de ventas`);
    res.json(ventas);
  });
});

app.listen(PORT, () => {
  console.log(`🚀 API corriendo en http://localhost:${PORT}/api/ventas`);
});
