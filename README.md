# Will You Marry Me as a Service (Marriage as a Service)
A minimal Django REST API for creating and responding to marriage proposals.

## Local development (Windows PowerShell)
### 1) Create/activate venv
```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

### 2) Run migrations
```powershell
.\.venv\Scripts\python manage.py migrate
```

### 3) Start the API
```powershell
.\.venv\Scripts\python manage.py runserver
```

API base URL: `http://127.0.0.1:8000/api/`

## API
### Health
- `GET /api/health/`

### Create a proposal
- `POST /api/proposals/`

Example:
```powershell
curl -X POST http://127.0.0.1:8000/api/proposals/ `
  -H "Content-Type: application/json" `
  -d '{"proposer_name":"Alex","proposee_name":"Sam","message":"Will you marry me?"}'
```

### Fetch a proposal
- `GET /api/proposals/<uuid>/`

### Respond to a proposal
- `POST /api/proposals/<uuid>/respond/`

Example:
```powershell
curl -X POST http://127.0.0.1:8000/api/proposals/<uuid>/respond/ `
  -H "Content-Type: application/json" `
  -d '{"response":"accepted"}'
```

Valid `response` values:
- `accepted`
- `rejected`

## Admin
```powershell
.\.venv\Scripts\python manage.py createsuperuser
```
Then visit `http://127.0.0.1:8000/admin/`.




## Project type
- Minimal Django + Django REST Framework (DRF) API.
- Local persistence uses SQLite (`db.sqlite3`) configured in `config/settings.py`.

## Common commands (Windows PowerShell)
Note: this repo’s README uses the venv-local Python at `.\.venv\Scripts\python`.

### Tests
This repo uses Django’s built-in test runner (no separate pytest/tox config is present).

Run all tests:
```powershell
.\.venv\Scripts\python manage.py test
```

Run tests for a single app:
```powershell
.\.venv\Scripts\python manage.py test proposals
```

Run a single test class or method (Django dotted path):
```powershell
.\.venv\Scripts\python manage.py test proposals.tests.MyTestCase
.\.venv\Scripts\python manage.py test proposals.tests.MyTestCase.test_something
```

### Admin user
```powershell
.\.venv\Scripts\python manage.py createsuperuser
```
Then visit `http://127.0.0.1:8000/admin/`.

## High-level architecture
### Entry points / wiring
- `manage.py` bootstraps Django with `DJANGO_SETTINGS_MODULE=config.settings`.
- Top-level routing is in `config/urls.py`:
  - `/admin/` → Django admin
  - `/api/` → includes `proposals/urls.py`

### Main domain: proposals
The core API is implemented in the `proposals` Django app:
- `proposals/models.py`
  - `Proposal` model (UUID primary key) stores proposer/proposee names, message, status, timestamps.
  - Business logic lives in `Proposal.respond(response)`:
    - Only allows `accepted` or `rejected`.
    - Only allows responding once (must be `pending`).
    - Persists changes via `save(update_fields=[...])`.
- `proposals/serializers.py`
  - `ProposalSerializer` exposes the API representation (status/timestamps are read-only).
  - `ProposalRespondSerializer` validates the `response` field for the respond endpoint.
- `proposals/views.py`
  - `health` (`GET /api/health/`) returns a simple JSON status.
  - `ProposalViewSet` (DRF `ModelViewSet`) provides CRUD for proposals and a custom action:
    - `POST /api/proposals/<uuid>/respond/` calls `Proposal.respond()`.
    - `ValueError` from model logic is translated into HTTP 400 with a `detail` message.
- `proposals/urls.py`
  - Uses DRF’s `DefaultRouter` to register `ProposalViewSet` under `/api/proposals/`.

### Data flow for “respond to proposal”
1. Route: `/api/proposals/<uuid>/respond/` (`proposals/urls.py` → `ProposalViewSet.respond`).
2. Validate input: `ProposalRespondSerializer`.
3. Apply business rules + persistence: `Proposal.respond()`.
4. Return updated resource: `ProposalSerializer(proposal).data`.
