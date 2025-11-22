# AnotherMe - Birthday Social Network Platform

A social networking platform that connects people who share the exact same birthday (year, month, and day).

## Project Structure

```
anotherme/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API route handlers
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── core/        # Config, security, database
│   │   └── services/    # Business logic
│   ├── database/        # Database files
│   ├── main.py          # FastAPI entry point
│   └── requirements.txt
│
├── frontend/            # Multi-page HTML frontend
│   ├── pages/          # HTML pages
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   └── assets/         # Images, icons
│
└── docs/               # Documentation
```

## Tech Stack

**Backend:**
- Python 3.9+
- FastAPI
- SQLAlchemy (ORM)
- SQLite (development) / PostgreSQL (production)
- JWT authentication

**Frontend:**
- HTML5, CSS3
- Tailwind CSS (CDN)
- Vue.js 3 (CDN)
- Vanilla JavaScript

## Getting Started

### Backend Setup

1. Create virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env and update SECRET_KEY
   ```

4. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

   Server will run at: http://localhost:8000

### Frontend Setup

1. Simply open the HTML files in a browser, or use a simple HTTP server:
   ```bash
   cd frontend
   python -m http.server 8080
   ```

   Frontend will be available at: http://localhost:8080

## Development Progress

See the todo list in the Claude Code session for current progress.

## Features

- ✅ User registration and authentication
- ✅ Birthday matching (find your birthday twins)
- ✅ User profiles
- ✅ Friends system (one-way friendships)
- ✅ Posts and comments
- ✅ Direct messaging
- ✅ Birthday-based groups
- ✅ Search and filters

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

Private project - All rights reserved

## Contact

For questions or issues, please create an issue in the repository.
