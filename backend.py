import json
import sqlite3
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'fitlife.db'
PORT = 4000
ADMIN_USER = 'admin'
ADMIN_PASSWORD = 'fitlife123'
ADMIN_TOKEN = 'fitlife-admin-token'

PROGRAMS = [
    {
        'id': 1,
        'name': 'Starter Routine',
        'description': 'Easy-to-follow sessions for steady progress and strong habits.',
        'features': ['3 workouts / week', 'Technique-first coaching', 'Recovery guidance']
    },
    {
        'id': 2,
        'name': 'Strength Builder',
        'description': 'Build muscle and confidence with a focused strength pathway.',
        'features': ['4 workouts / week', 'Progressive training plan', 'Nutrition support']
    },
    {
        'id': 3,
        'name': 'Endurance & Mobility',
        'description': 'Increase cardio fitness and flexibility without burnout.',
        'features': ['3 cardio + 2 mobility sessions', 'Low-impact options', 'Stress relief focus']
    }
]

CREATE_CONTACTS_TABLE = '''
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    goal TEXT,
    created_at TEXT NOT NULL
);
'''


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(CREATE_CONTACTS_TABLE)
        conn.commit()


class BackendHandler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        return super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith('/api/'):
            self.handle_api_get(parsed.path)
            return

        if parsed.path == '/' or parsed.path == '':
            self.path = '/index.html'
        return super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == '/api/contact':
            self.handle_contact_post()
            return

        if parsed.path == '/api/admin/login':
            self.handle_admin_login()
            return

        self.send_error(404, 'Not Found')

    def handle_api_get(self, path: str) -> None:
        if path == '/api/programs':
            self.send_json(PROGRAMS)
            return

        if path == '/api/admin/contacts':
            if not self.authorize():
                return

            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.execute(
                    'SELECT id, name, email, goal, created_at AS createdAt FROM contacts ORDER BY id DESC'
                )
                rows = [dict(row) for row in map(lambda r: {**dict(zip([c[0] for c in cursor.description], r))}, cursor.fetchall())]
            self.send_json(rows)
            return

        self.send_error(404, 'Not Found')

    def handle_contact_post(self) -> None:
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            raw_body = self.rfile.read(content_length)
            payload = json.loads(raw_body.decode('utf-8') if raw_body else '{}')
        except json.JSONDecodeError:
            self.send_json({'error': 'Invalid JSON payload.'}, status=400)
            return

        name = payload.get('name', '').strip()
        email = payload.get('email', '').strip()
        goal = payload.get('goal', '').strip()

        if not name or not email:
            self.send_json({'error': 'Name and email are required.'}, status=400)
            return

        created_at = datetime.utcnow().isoformat() + 'Z'
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute(
                'INSERT INTO contacts (name, email, goal, created_at) VALUES (?, ?, ?, ?)',
                (name, email, goal, created_at)
            )
            conn.commit()
            contact_id = cursor.lastrowid

        self.send_json(
            {
                'id': contact_id,
                'name': name,
                'email': email,
                'goal': goal,
                'createdAt': created_at,
            }
        )

    def handle_admin_login(self) -> None:
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            raw_body = self.rfile.read(content_length)
            payload = json.loads(raw_body.decode('utf-8') if raw_body else '{}')
        except json.JSONDecodeError:
            self.send_json({'error': 'Invalid JSON payload.'}, status=400)
            return

        username = payload.get('username', '')
        password = payload.get('password', '')
        if username == ADMIN_USER and password == ADMIN_PASSWORD:
            self.send_json({'token': ADMIN_TOKEN})
        else:
            self.send_json({'error': 'Invalid admin credentials.'}, status=401)

    def authorize(self) -> bool:
        auth_header = self.headers.get('Authorization', '')
        if auth_header and auth_header.strip() == f'Bearer {ADMIN_TOKEN}':
            return True
        self.send_json({'error': 'Unauthorized.'}, status=401)
        return False

    def send_json(self, payload, status=200) -> None:
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        print('%s - - [%s] %s' % (self.client_address[0], self.log_date_time_string(), format % args))


def run_server() -> None:
    init_db()
    server_address = ('', PORT)
    print(f'Starting FitLife backend on http://localhost:{PORT}')
    with ThreadingHTTPServer(server_address, BackendHandler) as httpd:
        httpd.serve_forever()


if __name__ == '__main__':
    run_server()
