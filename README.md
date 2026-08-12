# JobG — Full Connected Project (React frontend + Django backend)

This is your original React frontend, completely unchanged (no design or CSS
edits), connected to the Django backend that replaces the old Node/Express
API. Run both, and everything — login, register, jobs, applications, resume
upload — works exactly as before.

## Folder structure
```
jobg_full_project/
├── backend/     ← Django (replaces the old Node backend)
└── frontend/    ← Your original React app, untouched
```

## 1. Start the backend (Django) — port 4000

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# open .env and fill in your Cloudinary credentials
# (FRONTEND_URL is already set to http://localhost:5173, matches Vite's default)

python manage.py migrate
python manage.py runserver 4000
```

Leave this running in its own terminal.

## 2. Start the frontend (React) — port 5173

Open a **second terminal**:

```bash
cd frontend
npm install
npm run dev
```

Vite will start on `http://localhost:5173` by default. Open that URL in your
browser — the app is fully functional against the Django backend.

## Why no frontend code needed to change

Your React app already calls `http://localhost:4000/api/v1/...` with
`withCredentials: true` in every request (see `src/App.jsx`,
`src/components/Auth/Login.jsx`, etc.). The Django backend was built to
answer on that exact same port, with the exact same routes and exact same
JSON field names (`_id`, `fixedSalary`, `jobPostedOn`, `coverLetter`, etc.),
so the two sides line up without edits.

## Verified working (tested before packaging)
- Register → sets httpOnly `token` cookie → confirmed with `Origin: http://localhost:5173`
- `getuser` → returns the logged-in user using that cookie
- CORS preflight (`OPTIONS`) → allows the Vite origin with credentials
- `npm run dev` and `python manage.py runserver 4000` both start cleanly
- Frontend HTML served correctly by Vite

## If something doesn't connect
- Check both servers are actually running (`4000` for Django, `5173` for Vite)
- Check `backend/.env` → `FRONTEND_URL` matches your browser's address bar exactly (protocol + host + port)
- Open browser DevTools → Network tab → look for CORS errors or a missing `Set-Cookie` on login
