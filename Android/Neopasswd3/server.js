const WebSocket = require('ws');
const sqlite3 = require('sqlite3').verbose();
const { v4: uuidv4 } = require('uuid');

const db = new sqlite3.Database('./app.db');

const pendingWebClients = new Map();

db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS device (
    id TEXT PRIMARY KEY,
    identifier TEXT
  )`);

  db.run(`CREATE TABLE IF NOT EXISTS event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT,
    reason TEXT
  )`);

  db.get(`SELECT id FROM device WHERE id = ?`, ['11111111-1111-1111-1111-111111111111'], (err, row) => {
    if (!row) {
      db.run(`INSERT INTO device (id, identifier) VALUES (?, ?)`, ['11111111-1111-1111-1111-111111111111', 'not the same on remote :)']);
      console.log('Default device inserted');
    }
  });
});

const wss = new WebSocket.Server({ port: 8000, host: '0.0.0.0' });
console.log('WebSocket server running on ws://0.0.0.0:8000');

wss.on('connection', (ws) => {
  ws.on('message', async (message) => {
    try {
      const data = JSON.parse(message);

      if (data.type === 'authorization') {
        const { id, reason } = data;
        db.get(`SELECT id FROM device WHERE id = ?`, [id], (err, row) => {
          if (row) {
            db.run(`INSERT INTO event (device_id, reason) VALUES (?, ?)`, [id, reason]);
            pendingWebClients.set(id, ws);
            ws.send(JSON.stringify({ status: 'waiting_for_device' }));
          } else {
            ws.send(JSON.stringify({ status: 'invalid_id' }));
          }
        });
      }

      else if (data.type === 'device' && data.method === 'login') {
        const { identifier, id } = data;

        const handleDevice = (deviceId) => {
          ws.send(JSON.stringify({ status: 'connected', id: deviceId }));
          startEventLoop(ws, deviceId);
        };

        if (id) {
          db.get(`SELECT id, identifier FROM device WHERE id = ?`, [id], (err, row) => {
            if (row) {
              if (
                id === '11111111-1111-1111-1111-111111111111' &&
                identifier !== row.identifier
              ) {
                ws.send(JSON.stringify({ status: 'invalid_identifier' }));
                return;
              }
              handleDevice(row.id);
            } else {
              ws.send(JSON.stringify({ status: 'invalid_id' }));
            }
          });
        } else {
          const newId = uuidv4();
          db.run(`INSERT INTO device (id, identifier) VALUES (?, ?)`, [newId, identifier], function(err) {
            if (err) return console.error(err);
            handleDevice(newId);
          });
        }
      }

      else if (data.type === 'authorization_response') {
        const { id, decision } = data;
        const webClient = pendingWebClients.get(id);
        if (webClient) {
          webClient.send(JSON.stringify({ type: 'auth_result', result: decision }));
          pendingWebClients.delete(id);
        }
      }

    } catch (e) {
      console.error('Invalid JSON:', e);
      ws.send(JSON.stringify({ status: 'error', error: 'Invalid JSON' }));
    }
  });
});

function startEventLoop(ws, deviceId) {
  const interval = setInterval(() => {
    db.get(`SELECT * FROM event WHERE device_id = ? ORDER BY id LIMIT 1`, [deviceId], (err, row) => {
      if (row) {
        ws.send(JSON.stringify({
          type: "authorization",
          reason: row.reason,
          id: row.device_id
        }));
        db.run(`DELETE FROM event WHERE id = ?`, [row.id]);
      }
    });
  }, 1000);

  ws.on('close', () => {
    clearInterval(interval);
    console.log(`Device ${deviceId} disconnected`);
  });
}
