# 🌟 AstroLogic AI — Enterprise Astrology & Prediction Platform

A scalable, production-ready Vedic Astrology & AI Prediction platform built with **FastAPI**, **Swiss Ephemeris (Lahiri Sidereal)**, **SQLAlchemy 2.0**, and **Ollama / OpenAI** integration.

---

## 🏛️ Production Architecture

```
backend/
├── app/
│   ├── main.py                          # FastAPI app bootstrap, lifespan, static mounting, routers, error handlers
│   │
│   ├── api/                             # Clean API Layer (Request/Response & Routing only)
│   │   ├── dependencies.py              # DB Session, Auth, and Admin authorization dependencies
│   │   ├── routes/
│   │   │   ├── auth.py                  # User Login, Signup, Logout, Profile, Language switcher
│   │   │   ├── kundali.py               # Kundali calculation, PDF export, Kundali Chat, Cities lookup
│   │   │   ├── prediction.py            # AI Prediction, 10 Life Domains deep analysis, Contextual Chat
│   │   │   ├── panchang.py              # 5-Limb Panchang, Muhurta, Live Hindu Festivals
│   │   │   ├── horoscope.py             # Transit-based dynamic daily horoscope by sign/index
│   │   │   ├── blogs.py                 # Public blog endpoints
│   │   │   ├── admin.py                 # Admin dashboard, blog management, user telemetry, feedback
│   │   │   ├── pages.py                 # Clean HTML page template rendering routes
│   │   │   ├── feedback.py              # Feedback submission & activity telemetry endpoints
│   │
│   ├── core/                            # Core Configuration & Security
│   │   ├── config.py                    # Environment settings loader via python-dotenv
│   │   ├── security.py                  # PBKDF2-SHA256 password hashing & verification
│   │   ├── constants.py                 # Astrological & system constants
│   │   ├── logger.py                    # Structured logging setup
│   │
│   ├── db/                              # Database Layer
│   │   ├── database.py                  # SQLAlchemy engine (SQLite & PostgreSQL), SessionLocal, get_db, init_db
│   │
│   ├── models/                          # SQLAlchemy ORM Models
│   │   ├── user.py                      # User & UserProfile models
│   │   ├── blog.py                      # Blog model
│   │   ├── feedback.py                  # Feedback model
│   │   ├── activity.py                  # UserActivity audit model
│   │
│   ├── schemas/                         # Pydantic Validation & Serialization Schemas
│   │   ├── auth.py                      # Login, Signup, Token schemas
│   │   ├── user.py                      # User profile update & response schemas
│   │   ├── kundali.py                   # Kundali, Chart, Chat schemas
│   │   ├── panchang.py                  # Panchang request & response schemas
│   │   ├── prediction.py                # Prediction, Domains, Chat schemas
│   │   ├── horoscope.py                 # Horoscope & Festival schemas
│   │   ├── blog.py                      # Blog CRUD schemas
│   │   ├── feedback.py                  # Feedback & Activity telemetry schemas
│   │
│   ├── services/                        # Business Logic & Pure Calculation Engines
│   │   ├── astrology_engine/            # Pure Astronomical / Vedic Astrology Engine (No HTTP/DB coupling)
│   │   │   ├── planets.py               # Swiss Ephemeris 9-graha longitudes & speeds
│   │   │   ├── houses.py                # Lagna (Ascendant), Whole Sign & Sripati Bhava cusps
│   │   │   ├── charts.py                # Full chart orchestrator for prediction module
│   │   │   ├── dasha.py                 # Vimshottari Mahadasha, Antardasha, Pratyantardasha timeline
│   │   │   ├── transits.py              # Real-time transits relative to natal Lagna
│   │   │   ├── kundali.py               # Master Kundali engine (Rasi, D9, Yogas, Doshas, Scores)
│   │   │   ├── panchang.py              # Tithi, Vara, Nakshatra, Yoga, Karana, Sunrise/Sunset, Rahu Kaal
│   │   │   ├── domain_analysis.py       # 10 Life Domains deep analysis engine
│   │   │   ├── festival.py              # Live Ephemeris-based Hindu festival calculator
│   │   │   ├── horoscope.py             # Dynamic transit-driven daily horoscope for all 12 signs
│   │   │   ├── yogas.py                 # Detection of Raja, Dhana, Gajakesari, Mahapurusha yogas
│   │   │   ├── doshas.py                # Manglik, Sade Sati, Kaal Sarp, Pitru, Grahan, Gandmool doshas
│   │   │   ├── aspects.py               # Vedic Drishti (Mars 4/8, Jupiter 5/9, Saturn 3/10, 7th)
│   │   │   ├── strength.py              # Exaltation, Debilitation, Dignity, Weighted strength scoring
│   │   │   ├── timing.py                # Dasha activation & event triggers
│   │   │   ├── cities.py                # City coordinates database (lat, lon, tz)
│   │   │   ├── zodiac.py                # Sign mappings, elements, modalities, degree helpers
│   │   │   ├── nakshatra.py             # 27 Nakshatras & 108 Padas formulas
│   │   │   ├── navamsa.py               # Parashari D9 Navamsa calculation
│   │   │
│   │   ├── ai_engine/                   # Decoupled AI Layer
│   │   │   ├── llm_client.py            # Unified client (Ollama / OpenAI + rule-based fallback)
│   │   │   ├── prompt_builder.py        # Token-optimized astrological prompt templates
│   │   │   ├── prediction_service.py    # Marriage & career AI prediction orchestrator
│   │   │   ├── chat_service.py          # Smart natal-chart aware chat assistant
│   │   │
│   │   ├── auth_service.py              # User authentication, registration, session management
│   │   ├── blog_service.py              # Blog CRUD business logic
│   │   ├── user_service.py              # Profile management
│   │   ├── feedback_service.py          # Activity logging & feedback collection
│   │   ├── translation_service.py       # Multi-language locale dictionary loader
│   │   ├── pdf_service.py               # Kundali PDF report builder using ReportLab
│   │
│   ├── static/                          # Static assets (CSS, JS, SVGs, Locales)
│   ├── templates/                       # Jinja2 HTML templates
│
├── tests/                               # Comprehensive Automated Test Suite (26 Tests)
│   ├── test_astrology_engine.py         # Unit tests for core astrology math
│   ├── test_api_routes.py               # Integration tests for FastAPI endpoints
│   ├── test_auth_and_db.py              # Tests for auth, models, and DB operations
│
├── .env.example
├── .env
├── requirements.txt
└── README.md
```

---

## 🚀 Quickstart & Run Instructions

### 1. Prerequisites
- **Python 3.10+** (Tested on Python 3.11)
- Git & virtual environment tool

### 2. Environment Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Default settings use local SQLite (`sqlite:///./astrologic.db`) out of the box with zero external setup needed.

### 4. Run Development Server
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Open your browser at:
- **Web Application**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Admin Portal**: [http://127.0.0.1:8000/admin/login](http://127.0.0.1:8000/admin/login) (Database seeded AdminUser)

---

## 🧪 Running Automated Tests

Run the full automated test suite with `pytest`:
```bash
python -m pytest tests/ -v
```

---

## 📡 API Endpoints Reference

### 🔮 Kundali & Chart Calculations
- `POST /api/kundali`: Comprehensive Kundali generation (Rasi, Navamsa D9, Panchang, Dasha timeline, Yogas, Doshas, Domain Scores).
- `POST /api/generate-chart`: Basic chart longitudes and Lagna calculation.
- `GET /api/cities`: List of supported Indian and international cities.
- `GET /api/download-kundali`: Download official PDF report of generated Kundali.
- `POST /api/kundali-chat`: Astrological Q&A assistant referencing birth chart context.

### 🤖 AI Prediction & Life Domains
- `POST /api/prediction`: Synthesized AI predictions for marriage and career.
- `POST /api/domains`: 10 Life Domains deep analysis (Career, Marriage, Wealth, Health, Children, Education, Property, Challenges, Travel, Spirituality).
- `POST /api/chat`: Conversational astrological assistant.

### 🌙 Panchang & Festivals
- `POST /api/panchang`: Full 5-Limb daily Panchang, Sunrise, Sunset, Rahu Kaal, Abhijit Muhurta.
- `GET /api/festivals/today`: Live Hindu festivals for today's date.
- `GET /api/festivals/upcoming`: Upcoming festivals for next 60 days.

### ♈ Daily Horoscope
- `GET /api/daily-horoscope/{sign}`: Dynamic transit-driven daily horoscope by sign name (`aries`, `taurus`, etc.).
- `GET /api/horoscope/{sign_idx}`: Horoscope by 0-11 zodiac index.

### 📝 Blogs, Admin & Feedback
- `GET /api/blogs`: All published blog posts.
- `POST /api/admin/blogs`: Admin blog creation.
- `POST /api/user-activity`: Telemetry logging.
- `POST /api/testing-feedback`: User feedback submission.

---

## ⚡ Chart Cache Architecture

```
                       ┌─────────────────────────┐
                       │  HTTP Birth Chart Req   │
                       └────────────┬────────────┘
                                    │
                                    ▼
                         @cached_chart Decorator
                         key: chart:2.0.0:{sha256}
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
             In-Process LRU                    Redis Cache
               (Hit ~0.1ms)                    (Hit ~1-2ms)
                    │                               │
                    └───────────────┬───────────────┘
                                    │ Miss / Error
                                    ▼
                        Swiss Ephemeris Calculation
                              (Uncached ~15ms)
```

### Key Cache Features:
1. **Deterministic Hashing**: Inputs (`date`, `time`, `place`, `latitude`, `longitude`, `timezone`, `ayanamsa`) are normalized into sorted canonical JSON and hashed with SHA-256.
2. **Two-Tier Storage**: Fast per-worker in-memory LRU cache with fallthrough to Redis shared across application workers.
3. **Fail-Open Policy**: Network or deserialization errors log warnings and gracefully fall back to fresh ephemeris calculation without crashing requests.
4. **Byte-Identical Guarantees**: Envelopes format responses cleanly without modifying payload structure.
5. **Observability**: `GET /metrics` exposes real-time hit, miss, and error metrics.

---

## 🔄 Async Narrative Generation Sequence

```
 Client             Gateway                Redis Queue          Narrative Worker           LLM Engine
   │                   │                        │                      │                       │
   │─ POST /prediction ─▶                       │                      │                       │
   │  (< 500ms)        │─ Compute Scores        │                      │                       │
   │                   │─ Enqueue Job ─────────▶│                      │                       │
   │◀─ {job_id, scores}│                        │                      │                       │
   │                   │                        │─ Pull Job ──────────▶│                       │
   │                   │                        │                      │─ Generate Prompt ────▶│
   │                   │                        │                      │◀─ LLM Text Response ──│
   │                   │                        │◀─ Mark Completed ────│                       │
   │                   │                        │   (Result Store)     │                       │
   │                   │                        │                      │                       │
---

## ⏳ Phase 5 Event Timing Engine (Dasha + Gochara Fusion)

The timing engine replaces coarse text labels with concrete, ranked date windows generated by fusing 15-year Dasha progression timelines with planetary Gochara transits:

### Weighted Fusion Formula
$$\text{Window Score} = 0.60 \times \text{Dasha Score} + 0.40 \times \text{Gochara Transit Score}$$

### Classical Rules Applied:
1. **Dasha Chain Scoring (60%)**: Evaluates Mahadasha (MD 30%), Antardasha (AD 45%), and Pratyantardasha (PD 25%) lord placements, house lordships, and karaka status.
2. **Gochara Transit Scoring (40%)**: Evaluates 15-year Jupiter ingress/aspects over domain houses, Saturn transit afflictions/stability, and Sade Sati activation phases.
3. **Confidence Tiers**:
   - `High`: Score $\ge 0.75$
   - `Moderate`: $0.55 \le \text{Score} < 0.75$
   - `Possible`: $0.35 \le \text{Score} < 0.55$
   - `Unlikely`: Score $< 0.35$



