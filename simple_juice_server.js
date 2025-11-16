const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

// Serve static files
app.use(express.static(path.join(__dirname, 'frontend/dist/frontend')));
app.use('/assets', express.static(path.join(__dirname, 'frontend/src/assets')));
app.use('/ftp', express.static(path.join(__dirname, 'ftp')));

// Basic API endpoint
app.get('/api', (req, res) => {
  res.json({ 
    application: 'OWASP Juice Shop',
    version: '14.5.1',
    message: 'Running on Vultr2'
  });
});

// Serve index.html for all other routes (Angular routing)
app.get('*', (req, res) => {
  const indexPath = path.join(__dirname, 'frontend/dist/frontend/index.html');
  const fallbackPath = path.join(__dirname, 'index.html');
  
  // Try to send the Angular app, or a simple HTML page
  try {
    res.sendFile(indexPath);
  } catch (err) {
    res.send(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>OWASP Juice Shop</title>
        <style>
          body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
          h1 { color: #ff6b35; }
        </style>
      </head>
      <body>
        <h1>🧃 OWASP Juice Shop</h1>
        <p>Version 14.5.1 - Running on Vultr2</p>
        <p>Server is running on port ${port}</p>
        <hr>
        <p>Frontend compilation in progress. Please check back later.</p>
      </body>
      </html>
    `);
  }
});

app.listen(port, '0.0.0.0', () => {
  console.log(`✅ OWASP Juice Shop is running!`);
  console.log(`🌐 Local: http://localhost:${port}`);
  console.log(`🌐 External: http://66.42.93.220:${port}`);
  console.log(`🌐 Via Apache: http://66.42.93.220`);
});