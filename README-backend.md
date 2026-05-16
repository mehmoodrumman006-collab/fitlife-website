# FitLife Backend

This backend uses Python's standard library and SQLite.

## Run locally

1. Open a terminal in `c:\Users\Lenovo\OneDrive\Documents\.vscode`
2. Run:

```powershell
C:/Users/Lenovo/AppData/Local/Microsoft/WindowsApps/python3.12.exe backend.py
```

3. Open `http://localhost:4000`

## API endpoints

- `GET /api/programs`
- `POST /api/contact`
- `POST /api/admin/login`
- `GET /api/admin/contacts` (requires `Authorization: Bearer fitlife-admin-token`)

The contact form in `index.html` submits to `/api/contact` and stores requests in `fitlife.db`.

## Admin access

Use the credentials below to log in and retrieve saved contact submissions:

- username: `admin`
- password: `fitlife123`
- token: `fitlife-admin-token`

## Deploying to make the site public (recommended)

Option A — Single deploy (frontend + backend together): Render (or any PaaS)

- Push the project to a public GitHub repository.
- Create a new Web Service on Render and connect the GitHub repo.
- Set the build command to: `python -m py_compile backend.py` (optional)
- Set the start command to: `python backend.py`
- Render will provide a public URL (e.g. `https://your-app.onrender.com`). Use that URL as the canonical site URL.

Option B — Static frontend only (fast, free): GitHub Pages + separate backend

- Push only the static files (`index.html`, `styles.css`, `script.js`, `favicon.svg`, `sitemap.xml`, `robots.txt`, `site.webmanifest`) to a GitHub repo and enable GitHub Pages.
- Host the Python backend on Render / Railway / Fly / an inexpensive VPS and set the `fetch` URLs in `script.js` to the backend's public URL.

Submitting to search engines:

- Once your site is publicly available, submit the `sitemap.xml` URL to Google Search Console and Bing Webmaster Tools to index the site faster.
- Ensure `robots.txt` allows crawling (this project includes `robots.txt` that allows all crawlers).

If you want, I can create the GitHub repo and a simple `deploy` workflow next.
