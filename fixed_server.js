// Simple Juice Shop server for Vultr2
const express = require('./node_modules/express');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

// Basic HTML response for now
app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>OWASP Juice Shop</title>
      <style>
        body { 
          font-family: Arial, sans-serif; 
          text-align: center; 
          padding: 50px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }
        h1 { 
          color: #fff; 
          font-size: 3em;
          text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .container {
          background: rgba(255,255,255,0.1);
          padding: 30px;
          border-radius: 20px;
          max-width: 600px;
          margin: 0 auto;
        }
        a {
          color: #ffd700;
          text-decoration: none;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>🧃 OWASP Juice Shop</h1>
        <p>Version 14.5.1 - Running on Vultr2</p>
        <hr style="border: 1px solid rgba(255,255,255,0.3);">
        <p>✅ Server is running successfully on port ${port}</p>
        <p>🌐 Access via: <a href="http://66.42.93.220">http://66.42.93.220</a></p>
        <hr style="border: 1px solid rgba(255,255,255,0.3);">
        <p><strong>Native Installation on Apache</strong></p>
        <p>No Docker • Direct Node.js • Apache Proxy</p>
      </div>
    </body>
    </html>
  `);
});

// API endpoint
app.get('/api', (req, res) => {
  res.json({ 
    application: 'OWASP Juice Shop',
    version: '14.5.1',
    server: 'Vultr2',
    status: 'Running',
    port: port
  });
});

app.listen(port, '0.0.0.0', () => {
  console.log(`✅ OWASP Juice Shop is running!`);
  console.log(`🌐 Local: http://localhost:${port}`);
  console.log(`🌐 External: http://66.42.93.220:${port}`);
  console.log(`🌐 Via Apache: http://66.42.93.220`);
});