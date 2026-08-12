# JobG Backend — Django Rewrite

A drop-in replacement for the original Node/Express/MongoDB backend, built with
Django + Django REST Framework. It exposes the **exact same routes, JSON field
names, and httpOnly-cookie JWT auth flow**, so the existing React frontend
needs no code changes — you only need to run this server on the same port
(4000) the frontend already calls.

## 1. Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Environment variables

```bash
cp .env.example .env
```

Edit `.env`:

| Variable | Meaning |
|---|---|
| `SECRET_KEY` | Django's internal secret (any random string) |
| `DEBUG` | `True` for local dev |
| `FRONTEND_URL` | Your Vite dev URL, e.g. `http://localhost:5173` — must match exactly for CORS + cookies to work |
| `JWT_SECRET_KEY` | Secret used to sign JWTs (equivalent to Node's `JWT_SECRET_KEY`) |
| `JWT_EXPIRES_DAYS` | Token lifetime in days |
| `COOKIE_EXPIRE_DAYS` | Cookie lifetime in days |
| `CLOUDINARY_CLIENT_NAME` / `_API` / `_SECRET` | Same Cloudinary credentials you used in the Node app |

## 3. Database

SQLite is used by default — zero setup required.

```bash
python manage.py migrate
```

(Optional) create an admin user to browse data at `/admin/`:

```bash
python manage.py createsuperuser
```

## 4. Run the server on port 4000

The React app has `http://localhost:4000` hardcoded in every `axios` call,
so run Django on that same port to avoid touching frontend code:

```bash
python manage.py runserver 4000
```

## 5. Connect the frontend

No code changes needed. Just:

1. Start this Django server on port 4000.
2. Start the React app as usual (`npm run dev`, typically port 5173).
3. Make sure `FRONTEND_URL` in `.env` matches the Vite URL exactly (protocol + host + port).

That's it — login, register, job posting, applications, and resume uploads
all work against this backend unchanged.

## API map (identical to the Node app)

| Method | Path | Notes |
|---|---|---|
| POST | `/api/v1/user/register` | |
| POST | `/api/v1/user/login` | |
| GET | `/api/v1/user/logout` | requires auth |
| GET | `/api/v1/user/getuser` | requires auth |
| GET | `/api/v1/job/getall` | public |
| POST | `/api/v1/job/post` | Employer only |
| GET | `/api/v1/job/getmyjobs` | Employer only |
| PUT | `/api/v1/job/update/<id>` | Employer only |
| DELETE | `/api/v1/job/delete/<id>` | Employer only |
| GET | `/api/v1/job/<id>` | requires auth |
| POST | `/api/v1/application/post` | Job Seeker only, multipart w/ `resume` file |
| GET | `/api/v1/application/employer/getall` | Employer only |
| GET | `/api/v1/application/jobseeker/getall` | Job Seeker only |
| DELETE | `/api/v1/application/delete/<id>` | Job Seeker only |

## Notes on design choices

- **IDs**: Mongo's `_id` (ObjectId string) is replaced by Django's integer
  auto-increment `id`, but every response still exposes it as `_id` so the
  frontend's `element._id` usage keeps working unchanged.
- **Auth**: instead of `djangorestframework-simplejwt` (which uses
  Authorization headers), a custom `CookieJWTAuthentication` class in
  `users/authentication.py` reads the same `token` httpOnly cookie the Node
  app used, so `withCredentials: true` on the frontend keeps working as-is.
- **Errors**: a custom DRF exception handler (`config/exceptions.py`) always
  returns `{ success: false, message: "..." }`, matching `middlewares/error.js`.
- **File uploads**: handled by DRF's `MultiPartParser` and uploaded straight
  to Cloudinary via the `cloudinary` Python SDK — no temp-file step needed
  (Django holds small uploads in memory automatically).
