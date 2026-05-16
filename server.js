const express = require('express');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const port = process.env.PORT || 4000;
const dbPath = path.join(__dirname, 'fitlife.db');

const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Unable to open database', err);
    process.exit(1);
  }
});

const createContactsTable = `
  CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    goal TEXT,
    created_at TEXT NOT NULL
  )
`;

db.run(createContactsTable, (err) => {
  if (err) {
    console.error('Could not create contacts table', err);
  }
});

app.use(express.json());
app.use(require('cors')());
app.use(express.static(path.join(__dirname)));

app.get('/api/programs', (req, res) => {
  res.json([
    {
      id: 1,
      name: 'Starter Routine',
      description: 'Easy-to-follow sessions for steady progress and strong habits.',
      features: ['3 workouts / week', 'Technique-first coaching', 'Recovery guidance']
    },
    {
      id: 2,
      name: 'Strength Builder',
      description: 'Build muscle and confidence with a focused strength pathway.',
      features: ['4 workouts / week', 'Progressive training plan', 'Nutrition support']
    },
    {
      id: 3,
      name: 'Endurance & Mobility',
      description: 'Increase cardio fitness and flexibility without burnout.',
      features: ['3 cardio + 2 mobility sessions', 'Low-impact options', 'Stress relief focus']
    }
  ]);
});

app.post('/api/contact', (req, res) => {
  const { name, email, goal } = req.body;
  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email are required.' });
  }

  const createdAt = new Date().toISOString();

  const stmt = db.prepare('INSERT INTO contacts (name, email, goal, created_at) VALUES (?, ?, ?, ?)');
  stmt.run(name, email, goal || '', createdAt, function (err) {
    if (err) {
      console.error('Database insert error', err);
      return res.status(500).json({ error: 'Unable to save contact request.' });
    }

    res.json({ id: this.lastID, name, email, goal, createdAt });
  });
  stmt.finalize();
});

app.get('/api/contacts', (req, res) => {
  db.all('SELECT id, name, email, goal, created_at as createdAt FROM contacts ORDER BY id DESC', (err, rows) => {
    if (err) {
      return res.status(500).json({ error: 'Unable to retrieve contacts.' });
    }
    res.json(rows);
  });
});

app.listen(port, () => {
  console.log(`FitLife backend running at http://localhost:${port}`);
});
