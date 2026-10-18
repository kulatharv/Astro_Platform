# 📖 AstroLogic AI — Complete Workspace File Reference Manual

**Workspace Root:** `c:\Desktop\astro_may_res (2)`  
**Total Files Cataloged:** 422 files across all subdirectories  
**Generated On:** October 2026  
**Target Audience:** Developers, Technical Auditors, Astrological System Engineers  

---

## 📌 Executive Architectural Summary

This document provides an exhaustive, granular inventory and architectural analysis of **every single file** contained within the workspace.


The project represents a production-oriented Vedic Astrology & AI Prediction platform (**AstroLogic AI**). It has transitioned from a traditional monolithic prototype (`astro-platform/app/`) into a highly decoupled, resilient **Modular Monolith architecture** (`astro-platform/backend/`):

1. **`backend/gateway/`**: Edge router handling request filtering, language negotiation, session cookies, default-deny route security, and dynamic HTML page rendering.

2. **`backend/modules/`**: 8 strictly bounded domain modules (`auth`, `kundali`, `prediction`, `panchang`, `horoscope`, `narrative`, `blog`, `feedback`).

3. **`backend/shared/`**: Common foundations including Swiss Ephemeris wrappers (`pyswisseph`), classical Vedic algorithms (`shared/veda`), two-tier Redis/LRU caching, i18n translation loaders, and database session lifecycles.

4. **`backend/workers/`**: Asynchronous Redis-backed workers for high-latency tasks (AI narrative text generation and PDF rendering).

5. **`backend/tests/`**: Comprehensive test suite (174 passing tests) covering unit math, integration, contract boundaries, byte-identical regression, and event timing accuracy.

6. **`frontend/`**: Standalone HTML5/ES6 static web distribution with multi-language UI, North Indian chart visualizers, and interactive dashboards ready for static hosting.

7. **`astro-platform/app/`**: Legacy monolithic source preserved for backward compatibility and serving embedded assets.


---


## 1. Workspace Root Files (`c:\Desktop\astro_may_res (2)\`)


### 📁 Directory: Workspace Root (`.`) (7 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [COMPLETE_WORKSPACE_FILE_REFERENCE.md](file:///c:/Desktop/astro_may_res%20%282%29/COMPLETE_WORKSPACE_FILE_REFERENCE.md) | `.md` | 871 | 108606 | Project asset or configuration file. |
| [CURRENT_PROJECT_PHASE.md](file:///c:/Desktop/astro_may_res%20%282%29/CURRENT_PROJECT_PHASE.md) | `.md` | 134 | 11049 | Official project status document defining the completion of Phase 5 (Timing Fusion Engine) and roadmap for Phase 6 (Empirical Validation). |
| [Untitled-1.txt](file:///c:/Desktop/astro_may_res%20%282%29/Untitled-1.txt) | `.txt` | 3 | 68 | Saved HTTP health check test response: `{"status":"ok","app":"AstroLogicAI","environment":"development"}`. |
| [Untitled-2.txt](file:///c:/Desktop/astro_may_res%20%282%29/Untitled-2.txt) | `.txt` | 3 | 68 | Duplicate benchmark response artifact for health endpoint verification. |
| [astrologic.db](file:///c:/Desktop/astro_may_res%20%282%29/astrologic.db) | `.db` | 159 | 86016 | Production/development SQLite database containing user accounts, blog posts, feedback, and telemetry data. |
| [audit](file:///c:/Desktop/astro_may_res%20%282%29/audit) | `plain` | 261 | 21068 | Exhaustive 12-dimension technical and astrological accuracy audit report evaluating code quality, ephemeris math, and empirical backtesting needs. |
| [project_architecture_and_file_details.md](file:///c:/Desktop/astro_may_res%20%282%29/project_architecture_and_file_details.md) | `.md` | 234 | 12485 | Architecture and data flow design specification document detailing system interactions and calculation flow. |

## 2. Backend API Gateway Layer (`backend/gateway/`)


### 📁 Directory: `astro-platform\backend\gateway` (4 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [deps.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/gateway/deps.py) | `.py` | 38 | 1298 | **Doc**: Gateway dependencies for user authentication and session database access. <br> **Functions**: `get_current_user, require_authenticated_user, require_admin` |
| [main.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/gateway/main.py) | `.py` | 211 | 7000 | **Doc**: FastAPI Gateway Application Entry Point & Edge Router. <br> **Classes**: `DefaultDenyAuthMiddleware` <br> **Functions**: `lifespan, health_check, get_metrics, get_admin_cache_stats, flush_admin_cache`... |
| [pages.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/gateway/pages.py) | `.py` | 80 | 2939 | **Doc**: HTML Page Routes for Gateway App. <br> **Functions**: `_render_page, home_page, prediction_html_page, chat_html_page, panchang_html_page`... |
| [settings.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/gateway/settings.py) | `.py` | 5 | 122 | **Doc**: Gateway settings re-export from shared config. |

### 📁 Directory: `astro-platform\backend\gateway\middleware` (1 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [language.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/gateway/middleware/language.py) | `.py` | 53 | 1872 | **Doc**: Language Detection Middleware for gateway. <br> **Classes**: `LanguageDetectionMiddleware` <br> **Functions**: `resolve_request_language` |

## 3. Backend Bounded Domain Modules (`backend/modules/`)


### 📁 Directory: `astro-platform\backend\modules\auth` (7 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/auth/__init__.py) | `.py` | 4 | 124 | **Doc**: Auth Bounded Context Module. |
| [api.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/auth/api.py) | `.py` | 235 | 7803 | **Doc**: Auth module API routers & AuthService public interface. <br> **Classes**: `AuthService` <br> **Functions**: `_render_auth_page, change_language, signup_page, signup, login_page`... |
| [engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/auth/engine.py) | `.py` | 74 | 2568 | **Doc**: Authentication and user management engine. <br> **Classes**: `AuthEngine` |
| [models.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/auth/models.py) | `.py` | 87 | 2761 | **Classes**: `User, UserProfile, AdminUser, UserActivity` |
| [repository.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/auth/repository.py) | `.py` | 66 | 2198 | **Classes**: `AuthRepository` |
| [schemas.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/auth/schemas.py) | `.py` | 65 | 1393 | **Classes**: `UserRegister, UserLogin, AdminLogin, TokenResponse`... |
| [security.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/auth/security.py) | `.py` | 33 | 869 | **Functions**: `hash_password, verify_password` |

### 📁 Directory: `astro-platform\backend\modules\blog` (6 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/blog/__init__.py) | `.py` | 4 | 109 | **Doc**: Blog Bounded Context Module. |
| [api.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/blog/api.py) | `.py` | 71 | 2522 | **Doc**: Blog Router and Public Service Interface. <br> **Classes**: `BlogService` <br> **Functions**: `list_blogs, get_blog, create_blog` |
| [engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/blog/engine.py) | `.py` | 25 | 924 | **Doc**: Blog Business Engine. <br> **Classes**: `BlogEngine` |
| [models.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/blog/models.py) | `.py` | 23 | 715 | **Doc**: Blog Post ORM Model. <br> **Classes**: `BlogPost` |
| [repository.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/blog/repository.py) | `.py` | 39 | 1131 | **Doc**: Blog database repository. <br> **Classes**: `BlogRepository` |
| [schemas.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/blog/schemas.py) | `.py` | 35 | 759 | **Doc**: Blog validation schemas. <br> **Classes**: `BlogPostCreate, BlogPostResponse` |

### 📁 Directory: `astro-platform\backend\modules\feedback` (6 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/feedback/__init__.py) | `.py` | 4 | 121 | **Doc**: Feedback Bounded Context Module. |
| [api.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/feedback/api.py) | `.py` | 32 | 1154 | **Doc**: Feedback Router and Public Service Interface. <br> **Classes**: `FeedbackService` <br> **Functions**: `create_feedback, get_feedback_list` |
| [engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/feedback/engine.py) | `.py` | 18 | 676 | **Doc**: Feedback Business Engine. <br> **Classes**: `FeedbackEngine` |
| [models.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/feedback/models.py) | `.py` | 31 | 1083 | **Doc**: Feedback and Activity ORM Models. <br> **Classes**: `Feedback, ActivityLog` |
| [repository.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/feedback/repository.py) | `.py` | 37 | 1146 | **Doc**: Feedback database repository. <br> **Classes**: `FeedbackRepository` |
| [schemas.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/feedback/schemas.py) | `.py` | 23 | 627 | **Doc**: Feedback Pydantic validation schemas. <br> **Classes**: `FeedbackCreate, FeedbackResponse` |

### 📁 Directory: `astro-platform\backend\modules\horoscope` (4 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/horoscope/__init__.py) | `.py` | 4 | 124 | **Doc**: Horoscope Bounded Context Module. |
| [api.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/horoscope/api.py) | `.py` | 62 | 1858 | **Doc**: Daily Horoscope API routes. <br> **Classes**: `HoroscopeService` <br> **Functions**: `get_daily_horoscope, horoscope_by_sign_index` |
| [engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/horoscope/engine.py) | `.py` | 106 | 4753 | **Doc**: Dynamic transit-driven daily horoscope engine. <br> **Functions**: `generate_horoscope, generate_all_horoscopes` |
| [schemas.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/horoscope/schemas.py) | `.py` | 21 | 581 | **Doc**: Horoscope response and request schemas. <br> **Classes**: `HoroscopeRequest, HoroscopeResponse` |

### 📁 Directory: `astro-platform\backend\modules\horoscope\rules` (3 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/horoscope/rules/__init__.py) | `.py` | 5 | 298 | **Doc**: Horoscope rule definitions package. |
| [daily.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/horoscope/rules/daily.py) | `.py` | 174 | 6327 | **Doc**: Deterministic Rule Evaluator for Daily Panchang Actions & Auspicious Windows. <br> **Functions**: `evaluate_daily_rules` |
| [definitions.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/horoscope/rules/definitions.py) | `.py` | 227 | 11878 | **Doc**: Config-driven Deterministic Vedic Rules for Daily Actions and Muhurtas. |

### 📁 Directory: `astro-platform\backend\modules\kundali` (10 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/kundali/__init__.py) | `.py` | 4 | 118 | **Doc**: Kundali Bounded Context Module. |
| [api.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/kundali/api.py) | `.py` | 125 | 4401 | **Doc**: Kundali generation, Chart calculation, PDF download, and Kundali chat API routes. <br> **Classes**: `KundaliService` <br> **Functions**: `get_cities, generate_chart_api, get_kundali, download_kundali, kundali_chat` |
| [cache.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/kundali/cache.py) | `.py` | 15 | 459 | **Doc**: Kundali cache wrapper keyed by input_hash / chart parameters. <br> **Classes**: `KundaliCache` |
| [cities.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/kundali/cities.py) | `.py` | 186 | 10972 | **Functions**: `get_city, get_city_elevation, get_city_names` |
| [dasha.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/kundali/dasha.py) | `.py` | 169 | 5266 | **Doc**: Vimshottari Dasha calculation engine. <br> **Functions**: `calculate_mahadasha, generate_dasha_timeline, generate_antardasha, compute_pratyantardasha, generate_dasha_chain` |
| [engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/kundali/engine.py) | `.py` | 243 | 9412 | **Doc**: Master Kundali Engine assembling Rasi, Navamsa D9, Dasha, Yogas, Doshas, and Scores. <br> **Functions**: `calculate_chart_scores, calculate_kundali` |
| [houses.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/kundali/houses.py) | `.py` | 74 | 1984 | **Doc**: Lagna (Ascendant) and house calculation engine. <br> **Functions**: `calculate_lagna, assign_house, assign_bhava_house` |
| [planets.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/kundali/planets.py) | `.py` | 89 | 2225 | **Doc**: Swiss Ephemeris precision planetary calculations. <br> **Functions**: `calculate_all_planets, calculate_planets_with_speed` |
| [schemas.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/kundali/schemas.py) | `.py` | 66 | 1549 | **Classes**: `BirthData, KundaliRequest, KundaliChatRequest, PlanetDetail`... |
| [varga.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/kundali/varga.py) | `.py` | 229 | 8190 | **Doc**: Divisional Charts (Varga) Engine: Navamsa (D9), Dashamsha (D10), etc. <br> **Functions**: `calculate_navamsa, calculate_navamsa_sign, calculate_house_lords, classify_functional_nature, calculate_dispositors`... |

### 📁 Directory: `astro-platform\backend\modules\narrative` (8 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/narrative/__init__.py) | `.py` | 4 | 119 | **Doc**: Narrative Module (AI Engine & Smart Chat) |
| [api.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/narrative/api.py) | `.py` | 105 | 3584 | **Classes**: `NarrativeService` <br> **Functions**: `generate_narrative, get_narrative_job_status, stream_narrative_job, chat_narrative` |
| [chat.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/narrative/chat.py) | `.py` | 210 | 10805 | **Doc**: Vedic Astrology Smart Chat Service answering user queries from Natal Chart data with i18n support. <br> **Classes**: `ChatService` |
| [engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/narrative/engine.py) | `.py` | 39 | 1413 | **Doc**: AI Prediction Orchestrator for Marriage, Career, and Life Domains. <br> **Classes**: `NarrativeEngine` |
| [jobs.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/narrative/jobs.py) | `.py` | 110 | 4019 | **Doc**: Job store for async narrative generation tasks. <br> **Functions**: `compute_job_id, create_job, get_job, mark_running, mark_completed`... |
| [llm_client.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/narrative/llm_client.py) | `.py` | 108 | 4606 | **Doc**: Unified LLM client supporting Ollama and OpenAI with graceful rule-based fallback. <br> **Classes**: `LLMClient` <br> **Functions**: `ask_llm` |
| [prompt_builder.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/narrative/prompt_builder.py) | `.py` | 62 | 2669 | **Doc**: Token-optimized astrological prompt formatting utilities with multi-language (i18n) support. <br> **Functions**: `build_prediction_prompt, build_chat_prompt` |
| [schemas.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/narrative/schemas.py) | `.py` | 64 | 1577 | **Doc**: Pydantic Schemas for Narrative Module. <br> **Classes**: `NarrativeRequest, NarrativeResponse, ChatRequest, ChatResponse`... |

### 📁 Directory: `astro-platform\backend\modules\panchang` (8 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/panchang/__init__.py) | `.py` | 4 | 121 | **Doc**: Panchang Bounded Context Module. |
| [api.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/panchang/api.py) | `.py` | 216 | 8311 | **Doc**: Panchang, Personalization, Decision Assistant, and Festival API routes. <br> **Classes**: `PanchangService` <br> **Functions**: `panchang_share_image, panchang_city, resolve_profile, decision_assistant, panchang_calendar_ics`... |
| [engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/panchang/engine.py) | `.py` | 709 | 27002 | **Doc**: Enterprise-Grade Panchang Engine with Swiss Ephemeris Precision. <br> **Functions**: `_fmt_time_ampm, _minutes_between, calculate_choghadiya_list, calculate_horas_list, get_full_panchang`... |
| [festival.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/panchang/festival.py) | `.py` | 300 | 28563 | **Doc**: Live Hindu Festival Engine computed from Swiss Ephemeris lunar & solar data with astronomical precision. <br> **Functions**: `_get_lunar_day_details, get_day_festivals, get_today_festivals, get_upcoming_festivals` |
| [ics.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/panchang/ics.py) | `.py` | 96 | 3407 | **Doc**: RFC 5545 Compliant iCalendar (.ics) Generator for Vedic Panchang Events. <br> **Functions**: `generate_panchang_ics` |
| [image.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/panchang/image.py) | `.py` | 435 | 21635 | **Doc**: Share Today's Panchang Image Generator (Pillow-based). <br> **Functions**: `_get_fonts, _draw_diamond, _draw_sparkle, _draw_sun_icon, _draw_rounded_card`... |
| [personalization.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/panchang/personalization.py) | `.py` | 914 | 38707 | **Doc**: Vedic Personalization & Decision Engine. <br> **Functions**: `calculate_tara_bala, calculate_chandra_bala, calculate_category_scores, evaluate_decision, derive_natal_moon`... |
| [schemas.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/panchang/schemas.py) | `.py` | 98 | 3206 | **Classes**: `PanchangRequest, ProfileResolveRequest, DecisionRequest, PanchangResponse` |

### 📁 Directory: `astro-platform\backend\modules\prediction` (13 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/__init__.py) | `.py` | 4 | 123 | **Doc**: Prediction & Life Domain Analysis Module. |
| [api.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/api.py) | `.py` | 137 | 5029 | **Classes**: `PredictionService` <br> **Functions**: `generate_prediction, astro_chat, get_life_domains, get_domain_timing` |
| [engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/engine.py) | `.py` | 62 | 2616 | **Doc**: Prediction Engine Orchestrator. <br> **Functions**: `analyse_all_domains` |
| [remedies.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/remedies.py) | `.py` | 102 | 4794 | **Doc**: Remedies and Timing Windows for Life Domain Analysis. <br> **Functions**: `_build_remedies, _timing_windows, _house_lord_str` |
| [schemas.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/schemas.py) | `.py` | 59 | 1441 | **Doc**: Pydantic Schemas for Prediction & Life Domain Module. <br> **Classes**: `PredictionRequest, ChatRequest, DomainRequest, TimingWindow`... |
| [scoring.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/scoring.py) | `.py` | 273 | 10748 | **Doc**: Scoring and Chart Context Utilities for Life Domain Analysis. <br> **Functions**: `parse_degree, _planet_strength, _house_from, _ordinal, _sign_lord`... |
| [timing.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/timing.py) | `.py` | 162 | 6675 | **Doc**: Event timing and Dasha-Gochara fusion timing engine. <br> **Functions**: `evaluate_event_trigger, compute_timing, build_timing_block` |
| [timing_config.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/timing_config.py) | `.py` | 196 | 6279 | **Doc**: Classical Parashari & Gochara configuration for all 10 life domains. <br> **Functions**: `get_domain_timing_config` |
| [timing_dasha.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/timing_dasha.py) | `.py` | 222 | 8355 | **Doc**: Dasha activation scoring engine for domain timing (Step 5.4). <br> **Classes**: `ScoredPeriod` <br> **Functions**: `is_functional_benefic, is_functional_malefic, evaluate_lord_subscore, score_dasha_periods` |
| [timing_fusion.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/timing_fusion.py) | `.py` | 225 | 8381 | **Doc**: Window fusion engine combining Dasha (60%) + Gochara (40%) into ranked, smoothed timing windows. <br> **Classes**: `TimingWindow, TimingFusionResult` <br> **Functions**: `get_confidence_tier, fuse_windows` |
| [timing_transit.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/timing_transit.py) | `.py` | 270 | 10921 | **Doc**: Gochara Transit activation scoring engine for domain timing (Step 5.5). <br> **Classes**: `ScoredMonth` <br> **Functions**: `_get_planet_sign_house_at_date, score_transit_months` |
| [transit_forecast.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/transit_forecast.py) | `.py` | 151 | 5349 | **Doc**: Future planetary transit forecast engine. <br> **Functions**: `compute_transit_aspects, is_sade_sati_active, compute_ingress_windows, compute_transit_forecast` |
| [transits.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/transits.py) | `.py` | 48 | 1535 | **Doc**: Real-time planetary transits engine. <br> **Functions**: `calculate_transits` |

### 📁 Directory: `astro-platform\backend\modules\prediction\domains` (11 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/domains/__init__.py) | `.py` | 1 | 55 | **Doc**: Domain Evaluators Package for Prediction Module. |
| [career.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/domains/career.py) | `.py` | 106 | 5190 | **Doc**: Career & Profession Domain Evaluator. <br> **Functions**: `analyse_career, _career_narrative` |
| [challenges.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/domains/challenges.py) | `.py` | 76 | 3894 | **Doc**: Challenges & Dosha Domain Evaluator. <br> **Functions**: `analyse_challenges, _challenges_narrative` |
| [children.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/domains/children.py) | `.py` | 55 | 2784 | **Doc**: Children & Next Generation Domain Evaluator. <br> **Functions**: `analyse_children` |
| [education.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/domains/education.py) | `.py` | 64 | 3266 | **Doc**: Education & Skills Domain Evaluator. <br> **Functions**: `analyse_education` |
| [health.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/domains/health.py) | `.py` | 88 | 4301 | **Doc**: Health & Longevity Domain Evaluator. <br> **Functions**: `analyse_health, _health_narrative` |
| [marriage.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/domains/marriage.py) | `.py` | 130 | 6770 | **Doc**: Marriage & Relationships Domain Evaluator. <br> **Functions**: `analyse_marriage, _marriage_narrative` |
| [property.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/domains/property.py) | `.py` | 61 | 3041 | **Doc**: Property & Home Domain Evaluator. <br> **Functions**: `analyse_property` |
| [spirituality.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/domains/spirituality.py) | `.py` | 67 | 4034 | **Doc**: Spirituality & Karma Domain Evaluator. <br> **Functions**: `analyse_spirituality` |
| [travel.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/domains/travel.py) | `.py` | 52 | 2453 | **Doc**: Travel & Foreign Domain Evaluator. <br> **Functions**: `analyse_travel` |
| [wealth.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/modules/prediction/domains/wealth.py) | `.py` | 87 | 4178 | **Doc**: Wealth & Finance Domain Evaluator. <br> **Functions**: `analyse_wealth, _wealth_narrative` |

## 4. Backend Shared Libraries & Core Calculations (`backend/shared/`)


### 📁 Directory: `astro-platform\backend\shared` (1 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/__init__.py) | `.py` | 1 | 63 | **Doc**: Shared core library for Astro-Platform modular monolith. |

### 📁 Directory: `astro-platform\backend\shared\cache` (6 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/cache/__init__.py) | `.py` | 5 | 248 | **Doc**: Shared caching package. |
| [decorators.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/cache/decorators.py) | `.py` | 77 | 2958 | **Doc**: Decorator for chart computation caching with fail-open semantics. <br> **Functions**: `cached_chart` |
| [envelope.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/cache/envelope.py) | `.py` | 47 | 1299 | **Doc**: Envelope serialization for cached chart responses. <br> **Classes**: `CacheEnvelope` <br> **Functions**: `serialize_chart, deserialize_chart` |
| [keys.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/cache/keys.py) | `.py` | 46 | 1816 | **Doc**: Cache key computation utilities for chart computations. <br> **Functions**: `compute_input_hash, chart_cache_key` |
| [metrics.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/cache/metrics.py) | `.py` | 44 | 1368 | **Doc**: Cache metrics counter registry for observability. <br> **Classes**: `CacheMetrics` |
| [redis_client.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/cache/redis_client.py) | `.py` | 156 | 5092 | **Doc**: Thread-safe In-Memory TTL & Redis Cache Implementation. <br> **Classes**: `InMemoryTTLCache, RedisCacheWrapper, CacheService` |

### 📁 Directory: `astro-platform\backend\shared\config` (3 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/config/__init__.py) | `.py` | 6 | 343 | **Doc**: Shared settings and configuration package. |
| [constants.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/config/constants.py) | `.py` | 19 | 367 | **Doc**: System-wide infrastructure constants. |
| [settings.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/config/settings.py) | `.py` | 88 | 2988 | **Doc**: Global Application Settings & Environment Configuration. <br> **Classes**: `Settings` <br> **Functions**: `validate_settings` |

### 📁 Directory: `astro-platform\backend\shared\db` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/db/__init__.py) | `.py` | 4 | 171 | **Doc**: Shared database session package. |
| [session.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/db/session.py) | `.py` | 35 | 752 | **Doc**: SQLAlchemy Database Engine & Session Management. <br> **Classes**: `Base` <br> **Functions**: `get_db, init_db` |

### 📁 Directory: `astro-platform\backend\shared\ephemeris` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/ephemeris/__init__.py) | `.py` | 4 | 170 | **Doc**: Shared Swiss Ephemeris wrapper package. |
| [wrapper.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/ephemeris/wrapper.py) | `.py` | 27 | 952 | **Doc**: Thin wrapper over pyswisseph (Swiss Ephemeris) for planetary math. <br> **Functions**: `calc_ut, get_ayanamsa_ut, julday, houses` |

### 📁 Directory: `astro-platform\backend\shared\errors` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/errors/__init__.py) | `.py` | 10 | 322 | **Doc**: Shared error types package. |
| [types.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/errors/types.py) | `.py` | 32 | 1313 | **Doc**: Typed domain and infrastructure exceptions for Astro-Platform. <br> **Classes**: `AstroError, ChartComputationError, PredictionError, NarrativeError`... |

### 📁 Directory: `astro-platform\backend\shared\i18n` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/i18n/__init__.py) | `.py` | 17 | 328 | Python package initialization file. |
| [translation.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/i18n/translation.py) | `.py` | 114 | 4269 | **Doc**: Translation and Localization Utility Engine. <br> **Functions**: `load_translations, translate, translate_astrology_term` |

### 📁 Directory: `astro-platform\backend\shared\logging` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/logging/__init__.py) | `.py` | 4 | 135 | **Doc**: Shared logging package. |
| [logger.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/logging/logger.py) | `.py` | 26 | 685 | **Doc**: Centralized Application Logging Infrastructure. <br> **Functions**: `setup_logger` |

### 📁 Directory: `astro-platform\backend\shared\queue` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/queue/__init__.py) | `.py` | 5 | 160 | **Doc**: Queue package exports. |
| [redis_queue.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/queue/redis_queue.py) | `.py` | 76 | 2390 | **Doc**: Async Task Queue Interface & Redis Queue Wrapper. <br> **Classes**: `JobStatus, RedisQueue` |

### 📁 Directory: `astro-platform\backend\shared\timezone` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/timezone/__init__.py) | `.py` | 10 | 312 | **Doc**: Shared timezone package. |
| [tz.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/timezone/tz.py) | `.py` | 63 | 1639 | **Doc**: Timezone utilities for IST (UTC+5:30) and local conversions. <br> **Functions**: `now_ist, to_ist, resolve_timezone, validate_iana_timezone, get_local_now`... |

### 📁 Directory: `astro-platform\backend\shared\veda` (11 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/veda/__init__.py) | `.py` | 27 | 1650 | **Doc**: Shared Pure Vedic Astrology Calculation Library (shared.veda). |
| [aspects.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/veda/aspects.py) | `.py` | 42 | 1460 | **Doc**: Vedic Planetary Aspects (Drishti) Engine (Pure Shared Library). <br> **Functions**: `calculate_vedic_aspects` |
| [combustion.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/veda/combustion.py) | `.py` | 38 | 1137 | **Doc**: Sun Combustion (Asta) Detection Engine (Pure Shared Library). <br> **Functions**: `is_combust` |
| [constants.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/veda/constants.py) | `.py` | 40 | 1083 | **Doc**: Application and Astrological Constants (Pure Shared Library). |
| [dignity.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/veda/dignity.py) | `.py` | 93 | 2875 | **Doc**: 9-Tier Dignity and Naisargika Maitri Planetary Friendship Engine (Pure Shared Library). <br> **Functions**: `get_naisargika_dignity, get_positional_strength` |
| [doshas.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/veda/doshas.py) | `.py` | 256 | 9089 | **Doc**: Vedic Doshas detection engine with remedies (Pure Shared Library). <br> **Functions**: `_get_planet_map, _house_of, _sign_of, evaluate_mangal_dosha, evaluate_pitru_dosha`... |
| [nakshatra.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/veda/nakshatra.py) | `.py` | 45 | 1630 | **Doc**: Nakshatra and Pada calculation utilities (Pure Shared Library). <br> **Functions**: `calculate_nakshatra, get_nakshatra_pada, get_nakshatra_lord` |
| [neech_bhanga.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/veda/neech_bhanga.py) | `.py` | 54 | 1892 | **Doc**: Neech Bhanga (Debilitation Cancellation) Engine (Pure Shared Library). <br> **Functions**: `is_neech_bhanga` |
| [strength.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/veda/strength.py) | `.py` | 107 | 3571 | **Doc**: Planetary Dignity, Exaltation, Debilitation, and Strength Scoring (Pure Shared Library). <br> **Functions**: `planet_strength_label, final_strength, calculate_weighted_strength` |
| [yogas.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/veda/yogas.py) | `.py` | 164 | 6537 | **Doc**: Classical Vedic Astrology Yogas Detection Engine (Pure Shared Library). <br> **Functions**: `_get_planet_map, _house_of, _sign_of, calculate_yogas, detect_advanced_yogas` |
| [zodiac.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/shared/veda/zodiac.py) | `.py` | 52 | 1537 | **Doc**: Zodiac signs and degree conversion utilities (Pure Shared Library). <br> **Functions**: `degree_to_sign, to_dms` |

## 5. Backend Background Workers & Task Queues (`backend/workers/`)


### 📁 Directory: `astro-platform\backend\workers` (6 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [README.md](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/workers/README.md) | `.md` | 31 | 925 | Master platform documentation, architectural diagram, and execution guide. |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/workers/__init__.py) | `.py` | 1 | 34 | **Doc**: Background workers package. |
| [narrative_worker.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/workers/narrative_worker.py) | `.py` | 83 | 3232 | **Doc**: Background narrative generation worker process. <br> **Functions**: `process_job, run_worker` |
| [pdf_worker.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/workers/pdf_worker.py) | `.py` | 124 | 4803 | **Doc**: PDF Report generation service for Kundali and Horoscope charts using in-memory buffers. <br> **Functions**: `generate_kundali_pdf_buffer` |
| [queue_config.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/workers/queue_config.py) | `.py` | 15 | 357 | **Doc**: Background task queue configuration. |
| [start.sh](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/workers/start.sh) | `.sh` | 6 | 211 | Shell script to launch worker processes. |

## 6. Backend Automated Test Suites (`backend/tests/`)


### 📁 Directory: `astro-platform\backend\tests` (13 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/__init__.py) | `.py` | 1 | 20 | **Doc**: Test package. |
| [conftest.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/conftest.py) | `.py` | 16 | 390 | **Doc**: Pytest fixtures and database initialization. <br> **Functions**: `setup_test_database` |
| [test_api_routes.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/test_api_routes.py) | `.py` | 176 | 4722 | **Doc**: Integration tests for FastAPI endpoints. <br> **Functions**: `get_auth_client, test_get_cities, test_generate_chart_endpoint, test_kundali_endpoint, test_panchang_endpoint`... |
| [test_astrology_engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/test_astrology_engine.py) | `.py` | 198 | 5980 | **Doc**: Unit tests for Pure Astrology Calculation Engine. <br> **Functions**: `test_zodiac_and_dms, test_nakshatra_calculation, test_navamsa_calculation, test_planet_calculation, test_lagna_calculation`... |
| [test_auth_and_db.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/test_auth_and_db.py) | `.py` | 83 | 2458 | **Doc**: Database and Authentication tests. <br> **Functions**: `db, test_password_hashing, test_user_registration_and_auth, test_blog_crud` |
| [test_benchmark_regression.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/test_benchmark_regression.py) | `.py` | 69 | 3190 | **Doc**: Phase 1 Regression Test Suite — 20 Benchmark Charts. <br> **Functions**: `test_benchmark_chart_regression, test_reproducibility_across_runs` |
| [test_drikpanchang_reference.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/test_drikpanchang_reference.py) | `.py` | 117 | 4949 | **Doc**: Permanent regression unit tests validating AstroLogic Panchang Engine against <br> **Functions**: `_parse_ampm_minutes, _assert_time_within_tolerance_mins, test_drikpanchang_chennai_december_solstice_2026, test_drikpanchang_leh_high_altitude_solstice_2026, test_drikpanchang_chennai_sunrise_proximate_tithi_transition_2026` |
| [test_i18n.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/test_i18n.py) | `.py` | 186 | 6994 | **Doc**: Comprehensive Automated Verification Test Suite for Multi-Language (i18n) Support. <br> **Functions**: `test_01_language_detection_priority, test_02_all_8_supported_locales_exist, test_03_locales_api_endpoint, test_04_astrology_terminology_translation, test_05_ai_prompt_language_directives`... |
| [test_panchang_enterprise.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/test_panchang_enterprise.py) | `.py` | 255 | 9380 | **Doc**: Enterprise Test Suite for Panchang Decision Engine. <br> **Functions**: `client, test_timezone_resolution, test_deterministic_rule_engine, test_rahu_kaal_rule_override, test_cache_service`... |
| [test_panchang_personalization.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/test_panchang_personalization.py) | `.py` | 291 | 10799 | **Doc**: Test Suite for Personalized Vedic Decision Engine. <br> **Functions**: `client, test_tara_bala_sampat, test_tara_bala_vipat, test_tara_bala_janma, test_tara_bala_wraps_around_27`... |
| [test_panchang_share_image.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/test_panchang_share_image.py) | `.py` | 146 | 5311 | **Doc**: Unit tests for 'Share Today's Panchang' Image Generator & API Endpoint. <br> **Functions**: `client, test_share_image_portrait_png, test_share_image_square_jpeg, test_data_parity_with_get_full_panchang, test_no_personalized_fields_in_general_share`... |
| [test_reference_charts.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/test_reference_charts.py) | `.py` | 142 | 5537 | **Doc**: Reference Birth Chart Validation Test Suite. <br> **Functions**: `arcmin_diff, test_reference_chart_nehru, test_reference_chart_gandhi, test_reference_chart_vivekananda` |
| [test_security_phase0.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/test_security_phase0.py) | `.py` | 138 | 5664 | **Doc**: Phase 0 Security Verification Test Suite. <br> **Functions**: `test_01_fail_fast_config_validation, test_02_no_hardcoded_secrets_or_astro123, test_03_admin_user_db_pbkdf2_auth, test_04_admin_login_flow, test_05_blog_api_security`... |

### 📁 Directory: `astro-platform\backend\tests\backtest` (1 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [test_timing_accuracy.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/backtest/test_timing_accuracy.py) | `.py` | 58 | 1870 | **Doc**: Timing accuracy backtest suite against known reference birth charts and historical events. <br> **Functions**: `test_backtest_timing_accuracy` |

### 📁 Directory: `astro-platform\backend\tests\contract` (1 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [test_module_boundaries.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/contract/test_module_boundaries.py) | `.py` | 19 | 720 | **Doc**: Contract tests enforcing module boundary rules via import-linter. <br> **Functions**: `test_import_linter_contracts` |

### 📁 Directory: `astro-platform\backend\tests\integration` (4 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [test_async_narrative.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/integration/test_async_narrative.py) | `.py` | 71 | 2034 | **Doc**: Integration test for async narrative queue and predictions API. <br> **Functions**: `get_auth_client, test_async_prediction_endpoint_latency_and_job_id, test_narrative_job_status_polling, test_legacy_sync_prediction_flag` |
| [test_cache_end_to_end.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/integration/test_cache_end_to_end.py) | `.py` | 98 | 2765 | **Doc**: Integration tests verifying end-to-end caching behavior and fail-open guarantees. <br> **Functions**: `get_auth_client, test_cache_hit_and_miss_via_api, test_metrics_endpoint, test_admin_cache_flush` |
| [test_module_integration.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/integration/test_module_integration.py) | `.py` | 40 | 1188 | **Doc**: Integration tests for module cross-communication and gateway router mounting. <br> **Functions**: `test_gateway_mounts_all_routers, test_prediction_calls_kundali_via_public_api` |
| [test_timing_end_to_end.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/integration/test_timing_end_to_end.py) | `.py` | 63 | 1712 | **Doc**: Integration tests for Phase 5 concrete timing windows and Dasha-Gochara fusion. <br> **Functions**: `test_timing_windows_generation, get_auth_client, test_standalone_timing_endpoint` |

### 📁 Directory: `astro-platform\backend\tests\unit` (10 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [test_cache_decorators.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/unit/test_cache_decorators.py) | `.py` | 42 | 1304 | **Doc**: Unit tests for @cached_chart decorator. <br> **Classes**: `DummyService` <br> **Functions**: `test_cached_chart_hit_and_miss, test_cached_chart_fail_open_on_cache_error` |
| [test_cache_envelope.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/unit/test_cache_envelope.py) | `.py` | 29 | 871 | **Doc**: Unit tests for cache envelope serialization and deserialization. <br> **Functions**: `test_envelope_roundtrip_byte_identical, test_deserialize_fallback` |
| [test_cache_keys.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/unit/test_cache_keys.py) | `.py` | 35 | 1215 | **Doc**: Unit tests for cache key generation and input hash determinism. <br> **Functions**: `test_deterministic_input_hash, test_different_inputs_produce_different_hashes, test_cache_key_formatting` |
| [test_domain_timing_integration.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/unit/test_domain_timing_integration.py) | `.py` | 112 | 3368 | **Doc**: Unit test suite for Step 5.8 Domain Integration & Timing Block wiring. <br> **Functions**: `test_each_domain_returns_timing_block, test_timing_windows_have_required_fields, test_legacy_timing_preserved, test_fail_open_on_timing_error, test_timing_deterministic`... |
| [test_narrative_jobs.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/unit/test_narrative_jobs.py) | `.py` | 49 | 1526 | **Doc**: Unit tests for narrative job state management. <br> **Functions**: `test_narrative_job_lifecycle` |
| [test_queue.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/unit/test_queue.py) | `.py` | 24 | 757 | **Doc**: Unit tests for shared queue infrastructure. <br> **Functions**: `test_queue_enqueue_and_get` |
| [test_timing_dasha.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/unit/test_timing_dasha.py) | `.py` | 135 | 4340 | **Doc**: Unit tests for modules/prediction/timing_dasha.py. <br> **Functions**: `test_score_returns_periods, test_karaka_md_scores_high, test_combust_md_scores_low, test_functional_benefic_boost, test_reasons_are_readable`... |
| [test_timing_fusion.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/unit/test_timing_fusion.py) | `.py` | 257 | 8107 | **Doc**: Unit test suite for Step 5.6 Window Fusion Engine (modules/prediction/timing_fusion.py). <br> **Functions**: `test_fuse_returns_windows, test_jupiter_7h_marriage_scores_high, test_saturn_7h_marriage_blocks, test_smoothing_reduces_spikes, test_consecutive_months_merge`... |
| [test_timing_transit.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/unit/test_timing_transit.py) | `.py` | 150 | 4712 | **Doc**: Unit tests for Step 5.5 Gochara transit activation scorer (modules/prediction/timing_transit.py). <br> **Functions**: `test_returns_monthly_snapshots, test_jupiter_transit_scores_high, test_saturn_7h_blocks_marriage, test_sade_sati_modifier, test_negative_transit_inversion`... |
| [test_transit_forecast.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/tests/unit/test_transit_forecast.py) | `.py` | 79 | 2460 | **Doc**: Unit tests for future transit forecasting and Dasha chain expansion. <br> **Functions**: `test_dasha_chain_pratyantardasha, test_compute_transit_aspects, test_sade_sati_detection, test_compute_transit_forecast_and_caching` |

## 7. Backend Database Migrations (`backend/alembic/`)


### 📁 Directory: `astro-platform\backend\alembic` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [env.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/alembic/env.py) | `.py` | 61 | 1548 | **Functions**: `run_migrations_offline, run_migrations_online` |
| [script.py.mako](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/alembic/script.py.mako) | `.mako` | 23 | 469 | Alembic database migration template. |

### 📁 Directory: `astro-platform\backend\alembic\versions` (3 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [20260526_0001_initial_postgresql_schema.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/alembic/versions/20260526_0001_initial_postgresql_schema.py) | `.py` | 110 | 5120 | **Doc**: initial postgresql schema <br> **Functions**: `upgrade, downgrade` |
| [20260825_0002_add_admin_users_table.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/alembic/versions/20260825_0002_add_admin_users_table.py) | `.py` | 34 | 1155 | **Doc**: add admin users table <br> **Functions**: `upgrade, downgrade` |
| [20260825_0003_add_language_to_blogs.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/alembic/versions/20260825_0003_add_language_to_blogs.py) | `.py` | 23 | 599 | **Doc**: add language to blogs <br> **Functions**: `upgrade, downgrade` |

## 8. Backend Maintenance & Data Scripts (`backend/scripts/`)


### 📁 Directory: `astro-platform\backend\scripts` (1 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [build_cities_db.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/scripts/build_cities_db.py) | `.py` | 112 | 3421 | **Doc**: Build script to download GeoNames data and compile SQLite database for city lookups. <br> **Functions**: `build_db` |

## 9. Backend Configuration & Meta Files (`backend/` root)


### 📁 Directory: `astro-platform\backend` (10 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [.env](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/.env) | `plain` | 20 | 666 | Active environment variables file (database URLs, JWT secrets, CORS settings). |
| [.env.example](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/.env.example) | `.example` | 26 | 606 | Template configuration file for required environment variables. |
| [.importlinter](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/.importlinter) | `plain` | 54 | 1270 | Import linter rules configuration to enforce architectural boundaries and prevent circular dependencies. |
| [README.md](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/README.md) | `.md` | 248 | 14292 | Master platform documentation, architectural diagram, and execution guide. |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/__init__.py) | `.py` | 1 | 62 | **Doc**: Backend package for the gradual AstroLogicAI migration. |
| [alembic.ini](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/alembic.ini) | `.ini` | 41 | 668 | Database migration configuration file for SQLAlchemy and Alembic. |
| [astrologic.db](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/astrologic.db) | `.db` | 2775 | 405504 | Production/development SQLite database containing user accounts, blog posts, feedback, and telemetry data. |
| [requirements.txt](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/requirements.txt) | `.txt` | 15 | 278 | Python dependencies specification (FastAPI, Uvicorn, pyswisseph, SQLAlchemy, Pydantic, etc.). |
| [sample_pune_portrait.png](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/sample_pune_portrait.png) | `.png` | 1126 | 149035 | Sample image asset / test fixture. |
| [sample_pune_square.jpeg](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/sample_pune_square.jpeg) | `.jpeg` | 1144 | 204313 | Sample image asset / test fixture. |

## 10. Backend Embedded UI Templates, Static Assets & Legacy Engine (`backend/app/`)


### 📁 Directory: `astro-platform\backend\app` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/__init__.py) | `.py` | 1 | 64 | **Doc**: Application package for the modular AstroLogicAI backend. |
| [main.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/main.py) | `.py` | 5 | 182 | **Doc**: Legacy re-export stub for gateway.main. |

### 📁 Directory: `astro-platform\backend\app\ai` (4 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/ai/__init__.py) | `.py` | 0 | 0 | Python package initialization file. |
| [llm_service.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/ai/llm_service.py) | `.py` | 0 | 0 | Project asset or configuration file. |
| [prompt_builder.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/ai/prompt_builder.py) | `.py` | 0 | 0 | Project asset or configuration file. |
| [rag_service.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/ai/rag_service.py) | `.py` | 0 | 0 | Project asset or configuration file. |

### 📁 Directory: `astro-platform\backend\app\api` (3 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/api/__init__.py) | `.py` | 1 | 49 | **Doc**: HTTP API packages and router aggregators. |
| [api.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/api/api.py) | `.py` | 769 | 31074 | **Classes**: `PanchangRequest, KundaliRequest, PredictionRequest, ChatRequest`... <br> **Functions**: `panchang_city, generate_chart_api, get_cities, get_kundali, download_kundali`... |
| [blogs.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/api/blogs.py) | `.py` | 90 | 2414 | **Functions**: `get_db, require_admin, get_all_blogs, create_blog, delete_blog`... |

### 📁 Directory: `astro-platform\backend\app\api\schemas` (1 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [chart_schemas.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/api/schemas/chart_schemas.py) | `.py` | 11 | 228 | **Classes**: `BirthData` |

### 📁 Directory: `astro-platform\backend\app\astro_engine\strengths` (1 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [functional_nature.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astro_engine/strengths/functional_nature.py) | `.py` | 30 | 800 | **Functions**: `classify_functional_nature` |

### 📁 Directory: `astro-platform\backend\app\astrology` (38 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/__init__.py) | `.py` | 8 | 219 | Python package initialization file. |
| [aspects.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/aspects.py) | `.py` | 32 | 998 | **Functions**: `calculate_aspects` |
| [chart_engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/chart_engine.py) | `.py` | 156 | 5264 | **Functions**: `generate_full_chart` |
| [chat_mode.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/chat_mode.py) | `.py` | 48 | 1220 | **Functions**: `build_chat_prompt, chat_with_chart` |
| [cities.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/cities.py) | `.py` | 299 | 12506 | **Doc**: cities.py — Complete Indian city database with coordinates and timezone <br> **Functions**: `get_city, get_city_names` |
| [dasha.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/dasha.py) | `.py` | 138 | 3110 | **Functions**: `get_nakshatra_lord, calculate_mahadasha, generate_dasha_timeline, generate_antardasha, generate_dasha_calendar`... |
| [dasha_activation.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/dasha_activation.py) | `.py` | 23 | 676 | **Functions**: `activated_houses` |
| [data](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/data) | `plain` | 376 | 22242 | Project asset or configuration file. |
| [dataset](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/dataset) | `plain` | 907 | 67310 | Project asset or configuration file. |
| [dispositor.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/dispositor.py) | `.py` | 22 | 594 | **Functions**: `calculate_dispositors` |
| [domain_engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/domain_engine.py) | `.py` | 2633 | 131768 | **Doc**: domain_engine.py — Complete Life Domain Analysis Engine <br> **Functions**: `_functional_nature, _ordinal, _positional_strength, _house_strength, _retrograde_modifier`... |
| [event_engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/event_engine.py) | `.py` | 134 | 4141 | **Functions**: `evaluate_event` |
| [explanation_builder.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/explanation_builder.py) | `.py` | 86 | 3338 | **Functions**: `build_event_explanation` |
| [festival_engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/festival_engine.py) | `.py` | 1503 | 72775 | **Doc**: festival_engine.py — Tithi-based Hindu Festival Engine + Dynamic Horoscope Engine <br> **Functions**: `get_ist_now, _jd_now, _panchang_at, _jd_to_date, _match_rule`... |
| [functional_nature.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/functional_nature.py) | `.py` | 30 | 800 | **Functions**: `classify_functional_nature` |
| [horoscope_engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/horoscope_engine.py) | `.py` | 672 | 31998 | **Doc**: horoscope_engine.py — AstroLogic Dynamic Horoscope Engine <br> **Functions**: `_planet_strength, _house_from_sign, _aspect_strength, get_current_positions, generate_horoscope`... |
| [house_lords.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/house_lords.py) | `.py` | 36 | 751 | **Functions**: `calculate_house_lords` |
| [houses.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/houses.py) | `.py` | 74 | 1490 | **Functions**: `calculate_lagna, assign_house, assign_bhava_house` |
| [julian.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/julian.py) | `.py` | 0 | 0 | Project asset or configuration file. |
| [kundali_engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/kundali_engine.py) | `.py` | 1035 | 37303 | **Doc**: import swisseph as swe <br> **Functions**: `to_dms, get_nakshatra_pada, ist_to_jd, planet_strength_label, get_planet_map`... |
| [llm_engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/llm_engine.py) | `.py` | 72 | 1643 | **Doc**: import requests <br> **Functions**: `ask_llm` |
| [llm_layer.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/llm_layer.py) | `.py` | 32 | 746 | **Functions**: `build_llm_prompt` |
| [nakshatra.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/nakshatra.py) | `.py` | 25 | 734 | **Functions**: `calculate_nakshatra` |
| [navamsa.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/navamsa.py) | `.py` | 29 | 793 | **Functions**: `calculate_navamsa` |
| [panchang_engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/panchang_engine.py) | `.py` | 751 | 20994 | **Doc**: import swisseph as swe <br> **Functions**: `get_ist_now, jd_to_ist, get_sun_times, get_full_panchang` |
| [planets.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/planets.py) | `.py` | 33 | 714 | **Functions**: `calculate_all_planets` |
| [prediction.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/prediction.py) | `.py` | 21 | 596 | **Functions**: `basic_prediction` |
| [prediction_builder.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/prediction_builder.py) | `.py` | 83 | 2160 | **Doc**: def build_prediction_prompt(chart, event_type): <br> **Functions**: `build_prediction_prompt` |
| [scoring.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/scoring.py) | `.py` | 57 | 1770 | **Functions**: `calculate_chart_scores` |
| [strength.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/strength.py) | `.py` | 58 | 1507 | **Functions**: `evaluate_strength, final_strength` |
| [sunrise_engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/sunrise_engine.py) | `.py` | 19 | 351 | **Functions**: `calculate_sun_times` |
| [timing_engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/timing_engine.py) | `.py` | 55 | 1721 | **Functions**: `evaluate_event_trigger` |
| [transits.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/transits.py) | `.py` | 37 | 919 | **Functions**: `calculate_transits` |
| [vedic_aspects.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/vedic_aspects.py) | `.py` | 38 | 1202 | **Functions**: `calculate_vedic_aspects` |
| [weighted_strength.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/weighted_strength.py) | `.py` | 63 | 1531 | **Functions**: `calculate_weighted_strength` |
| [yogas.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/yogas.py) | `.py` | 26 | 859 | **Functions**: `detect_yogas` |
| [yogas_engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/yogas_engine.py) | `.py` | 63 | 1866 | **Functions**: `detect_advanced_yogas` |
| [zodiac.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/astrology/zodiac.py) | `.py` | 10 | 304 | **Functions**: `degree_to_sign` |

### 📁 Directory: `astro-platform\backend\app\core` (5 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/core/__init__.py) | `.py` | 1 | 61 | **Doc**: Core configuration, logging, security, and constants. |
| [config.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/core/config.py) | `.py` | 57 | 2129 | **Classes**: `Settings` <br> **Functions**: `_csv_env, get_settings` |
| [constants.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/core/constants.py) | `.py` | 15 | 288 | Project asset or configuration file. |
| [logger.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/core/logger.py) | `.py` | 16 | 383 | **Functions**: `configure_logging, get_logger` |
| [security.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/core/security.py) | `.py` | 29 | 671 | **Functions**: `hash_password, verify_password` |

### 📁 Directory: `astro-platform\backend\app\database` (4 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/database/__init__.py) | `.py` | 4 | 165 | Python package initialization file. |
| [base.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/database/base.py) | `.py` | 9 | 250 | **Functions**: `import_models` |
| [init_db.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/database/init_db.py) | `.py` | 12 | 363 | **Functions**: `init_db` |
| [session.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/database/session.py) | `.py` | 110 | 2537 | **Functions**: `get_db` |

### 📁 Directory: `astro-platform\backend\app\models` (6 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/models/__init__.py) | `.py` | 4 | 190 | Python package initialization file. |
| [activity_model.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/models/activity_model.py) | `.py` | 3 | 78 | Project asset or configuration file. |
| [blog_model.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/models/blog_model.py) | `.py` | 12 | 389 | **Classes**: `Blog` |
| [feedback_model.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/models/feedback_model.py) | `.py` | 3 | 70 | Project asset or configuration file. |
| [kundali_model.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/models/kundali_model.py) | `.py` | 1 | 62 | **Doc**: Placeholder for saved kundali/chart SQLAlchemy models. |
| [user_model.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/models/user_model.py) | `.py` | 85 | 2899 | **Classes**: `User, UserProfile, UserActivity, Feedback` |

### 📁 Directory: `astro-platform\backend\app\schemas` (5 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/schemas/__init__.py) | `.py` | 0 | 0 | Python package initialization file. |
| [auth_schema.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/schemas/auth_schema.py) | `.py` | 0 | 0 | Project asset or configuration file. |
| [chart_schema.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/schemas/chart_schema.py) | `.py` | 81 | 1746 | **Classes**: `BirthData, PlanetDetails, DashaTimeline, DashaDetails`... |
| [feedback_schema.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/schemas/feedback_schema.py) | `.py` | 0 | 0 | Project asset or configuration file. |
| [user_schema.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/schemas/user_schema.py) | `.py` | 0 | 0 | Project asset or configuration file. |

### 📁 Directory: `astro-platform\backend\app\services` (6 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/services/__init__.py) | `.py` | 1 | 33 | **Doc**: Business service package. |
| [ai_service.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/services/ai_service.py) | `.py` | 0 | 0 | Project asset or configuration file. |
| [horoscope_service.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/services/horoscope_service.py) | `.py` | 37 | 881 | **Functions**: `fetch_horoscope` |
| [prediction_service.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/services/prediction_service.py) | `.py` | 0 | 0 | Project asset or configuration file. |
| [translation_service.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/services/translation_service.py) | `.py` | 22 | 508 | **Functions**: `load_translations` |
| [user_service.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/services/user_service.py) | `.py` | 0 | 0 | Project asset or configuration file. |

### 📁 Directory: `astro-platform\backend\app\static\js` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [i18n.js](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/static/js/i18n.js) | `.js` | 66 | 2169 | Client-side JavaScript interaction logic. |
| [kundali.js](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/static/js/kundali.js) | `.js` | 1095 | 56235 | Client-side JavaScript interaction logic. |

### 📁 Directory: `astro-platform\backend\app\static\locales` (8 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [bn.json](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/static/locales/bn.json) | `.json` | 49 | 3171 | JSON data / localization translations dictionary. |
| [en.json](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/static/locales/en.json) | `.json` | 14 | 337 | JSON data / localization translations dictionary. |
| [gu.json](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/static/locales/gu.json) | `.json` | 49 | 2986 | JSON data / localization translations dictionary. |
| [hi.json](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/static/locales/hi.json) | `.json` | 14 | 491 | JSON data / localization translations dictionary. |
| [kn.json](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/static/locales/kn.json) | `.json` | 49 | 3116 | JSON data / localization translations dictionary. |
| [mr.json](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/static/locales/mr.json) | `.json` | 14 | 519 | JSON data / localization translations dictionary. |
| [ta.json](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/static/locales/ta.json) | `.json` | 49 | 3388 | JSON data / localization translations dictionary. |
| [te.json](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/static/locales/te.json) | `.json` | 49 | 3208 | JSON data / localization translations dictionary. |

### 📁 Directory: `astro-platform\backend\app\static\svg` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [navamsa.svg](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/static/svg/navamsa.svg) | `.svg` | 52 | 1541 | Scalable Vector Graphic chart diagram. |
| [north_indian_kundali.svg](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/static/svg/north_indian_kundali.svg) | `.svg` | 52 | 1541 | Scalable Vector Graphic chart diagram. |

### 📁 Directory: `astro-platform\backend\app\templates` (19 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [Untitled-1.md](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/Untitled-1.md) | `.md` | 148 | 5131 | Project asset or configuration file. |
| [about.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/about.html) | `.html` | 401 | 27602 | HTML UI template / page view. |
| [admin-activity.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/admin-activity.html) | `.html` | 63 | 5374 | HTML UI template / page view. |
| [admin-blog.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/admin-blog.html) | `.html` | 160 | 8475 | HTML UI template / page view. |
| [admin-feedback.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/admin-feedback.html) | `.html` | 57 | 4656 | HTML UI template / page view. |
| [admin-login.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/admin-login.html) | `.html` | 97 | 4165 | HTML UI template / page view. |
| [admin-users.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/admin-users.html) | `.html` | 61 | 5592 | HTML UI template / page view. |
| [auth.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/auth.html) | `.html` | 463 | 11090 | HTML UI template / page view. |
| [base.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/base.html) | `.html` | 34 | 746 | HTML UI template / page view. |
| [blog-detail.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/blog-detail.html) | `.html` | 134 | 6982 | HTML UI template / page view. |
| [blogs.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/blogs.html) | `.html` | 386 | 21581 | HTML UI template / page view. |
| [daily-horoscope.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/daily-horoscope.html) | `.html` | 498 | 27164 | HTML UI template / page view. |
| [index.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/index.html) | `.html` | 723 | 41472 | HTML UI template / page view. |
| [kundali.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/kundali.html) | `.html` | 1540 | 82809 | HTML UI template / page view. |
| [kundali.js](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/kundali.js) | `.js` | 1095 | 56235 | Client-side JavaScript interaction logic. |
| [panchang.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/panchang.html) | `.html` | 744 | 36748 | HTML UI template / page view. |
| [prediction.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/prediction.html) | `.html` | 725 | 47221 | HTML UI template / page view. |
| [profile.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/profile.html) | `.html` | 653 | 13893 | HTML UI template / page view. |
| [vercel.json](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/templates/vercel.json) | `.json` | 14 | 598 | Routing configuration for deploying the frontend static distribution on Vercel. |

### 📁 Directory: `astro-platform\backend\app\utils` (4 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/utils/__init__.py) | `.py` | 0 | 0 | Python package initialization file. |
| [date_utils.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/utils/date_utils.py) | `.py` | 0 | 0 | Project asset or configuration file. |
| [helpers.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/utils/helpers.py) | `.py` | 0 | 0 | Project asset or configuration file. |
| [validators.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/backend/app/utils/validators.py) | `.py` | 0 | 0 | Project asset or configuration file. |

## 11. Standalone Static Web Frontend (`frontend/`)


### 📁 Directory: `astro-platform\frontend` (19 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [Untitled-1.md](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/Untitled-1.md) | `.md` | 148 | 5131 | Project asset or configuration file. |
| [about.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/about.html) | `.html` | 401 | 27602 | HTML UI template / page view. |
| [admin-activity.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/admin-activity.html) | `.html` | 63 | 5374 | HTML UI template / page view. |
| [admin-blog.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/admin-blog.html) | `.html` | 160 | 8475 | HTML UI template / page view. |
| [admin-feedback.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/admin-feedback.html) | `.html` | 57 | 4656 | HTML UI template / page view. |
| [admin-login.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/admin-login.html) | `.html` | 97 | 4165 | HTML UI template / page view. |
| [admin-users.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/admin-users.html) | `.html` | 61 | 5592 | HTML UI template / page view. |
| [auth.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/auth.html) | `.html` | 463 | 11090 | HTML UI template / page view. |
| [base.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/base.html) | `.html` | 34 | 746 | HTML UI template / page view. |
| [blog-detail.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/blog-detail.html) | `.html` | 134 | 6982 | HTML UI template / page view. |
| [blogs.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/blogs.html) | `.html` | 386 | 21581 | HTML UI template / page view. |
| [daily-horoscope.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/daily-horoscope.html) | `.html` | 498 | 27142 | HTML UI template / page view. |
| [index.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/index.html) | `.html` | 723 | 41472 | HTML UI template / page view. |
| [kundali.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/kundali.html) | `.html` | 1540 | 82809 | HTML UI template / page view. |
| [kundali.js](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/kundali.js) | `.js` | 1095 | 56235 | Client-side JavaScript interaction logic. |
| [panchang.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/panchang.html) | `.html` | 744 | 36727 | HTML UI template / page view. |
| [prediction.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/prediction.html) | `.html` | 725 | 47105 | HTML UI template / page view. |
| [profile.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/profile.html) | `.html` | 653 | 13893 | HTML UI template / page view. |
| [vercel.json](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/vercel.json) | `.json` | 14 | 598 | Routing configuration for deploying the frontend static distribution on Vercel. |

### 📁 Directory: `astro-platform\frontend\js` (1 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [kundali.js](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/js/kundali.js) | `.js` | 1095 | 56235 | Client-side JavaScript interaction logic. |

### 📁 Directory: `astro-platform\frontend\locales` (3 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [en.json](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/locales/en.json) | `.json` | 14 | 337 | JSON data / localization translations dictionary. |
| [hi.json](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/locales/hi.json) | `.json` | 14 | 491 | JSON data / localization translations dictionary. |
| [mr.json](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/locales/mr.json) | `.json` | 14 | 519 | JSON data / localization translations dictionary. |

### 📁 Directory: `astro-platform\frontend\svg` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [navamsa.svg](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/svg/navamsa.svg) | `.svg` | 52 | 1541 | Scalable Vector Graphic chart diagram. |
| [north_indian_kundali.svg](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/frontend/svg/north_indian_kundali.svg) | `.svg` | 52 | 1541 | Scalable Vector Graphic chart diagram. |

## 12. Legacy Monolithic Source Code (`astro-platform/app/`)


### 📁 Directory: `astro-platform\app` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/__init__.py) | `.py` | 1 | 64 | **Doc**: Application package for the modular AstroLogicAI backend. |
| [main.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/main.py) | `.py` | 173 | 5428 | **Doc**: FastAPI Application Entry Point & Server Bootstrap. <br> **Classes**: `DefaultDenyAuthMiddleware` <br> **Functions**: `lifespan, health_check, get_locale_translations, global_exception_handler` |

### 📁 Directory: `astro-platform\app\api` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/api/__init__.py) | `.py` | 28 | 600 | Python package initialization file. |
| [dependencies.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/api/dependencies.py) | `.py` | 38 | 1297 | **Doc**: API dependencies for database sessions, user authentication, and admin authorization. <br> **Functions**: `get_current_user, require_authenticated_user, require_admin` |

### 📁 Directory: `astro-platform\app\api\middleware` (1 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [language.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/api/middleware/language.py) | `.py` | 53 | 1906 | **Doc**: Language Detection Middleware for i18n support across the platform. <br> **Classes**: `LanguageDetectionMiddleware` <br> **Functions**: `resolve_request_language` |

### 📁 Directory: `astro-platform\app\api\routes` (10 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/api/routes/__init__.py) | `.py` | 21 | 621 | Python package initialization file. |
| [admin.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/api/routes/admin.py) | `.py` | 204 | 6898 | **Doc**: Admin portal dashboard, blog management, user telemetry, and activity routes. <br> **Functions**: `_render_admin, admin_home, admin_login_page, admin_login, admin_logout`... |
| [auth.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/api/routes/auth.py) | `.py` | 200 | 6259 | **Doc**: Authentication and user session routes. <br> **Functions**: `_render_auth_page, change_language, signup_page, signup, login_page`... |
| [blogs.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/api/routes/blogs.py) | `.py` | 24 | 884 | **Doc**: Public Blog API routes. <br> **Functions**: `get_blogs, get_blog` |
| [feedback.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/api/routes/feedback.py) | `.py` | 68 | 2750 | **Doc**: User activity telemetry and testing feedback API routes. <br> **Functions**: `record_user_activity, submit_testing_feedback` |
| [horoscope.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/api/routes/horoscope.py) | `.py` | 51 | 1523 | **Doc**: Daily Horoscope API routes. <br> **Functions**: `get_daily_horoscope, horoscope_by_sign_index` |
| [kundali.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/api/routes/kundali.py) | `.py` | 95 | 3501 | **Doc**: Kundali generation, Chart calculation, PDF download, and Kundali chat API routes. <br> **Functions**: `get_cities, generate_chart_api, get_kundali, download_kundali, kundali_chat` |
| [pages.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/api/routes/pages.py) | `.py` | 86 | 3431 | **Doc**: Frontend HTML template rendering routes with multi-language (i18n) support. <br> **Functions**: `_render_page, home_page, prediction_page, chat_page, panchang_page`... |
| [panchang.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/api/routes/panchang.py) | `.py` | 32 | 1139 | **Doc**: Panchang and Festival API routes. <br> **Functions**: `panchang_city, festivals_today, festivals_upcoming` |
| [prediction.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/api/routes/prediction.py) | `.py` | 61 | 2247 | **Doc**: AI Prediction, 10 Life Domains Analysis, and Contextual Chat API routes. <br> **Functions**: `generate_prediction, astro_chat, get_life_domains` |

### 📁 Directory: `astro-platform\app\core` (5 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/core/__init__.py) | `.py` | 14 | 344 | Python package initialization file. |
| [config.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/core/config.py) | `.py` | 75 | 2838 | **Classes**: `Settings` <br> **Functions**: `_csv_env, validate_settings, get_settings` |
| [constants.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/core/constants.py) | `.py` | 40 | 1061 | **Doc**: Application and Astrological Constants. |
| [logger.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/core/logger.py) | `.py` | 21 | 595 | **Functions**: `configure_logging, get_logger` |
| [security.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/core/security.py) | `.py` | 33 | 869 | **Functions**: `hash_password, verify_password` |

### 📁 Directory: `astro-platform\app\db` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/db/__init__.py) | `.py` | 9 | 156 | Python package initialization file. |
| [database.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/db/database.py) | `.py` | 75 | 2169 | **Functions**: `get_db, init_db` |

### 📁 Directory: `astro-platform\app\models` (6 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/models/__init__.py) | `.py` | 16 | 310 | Python package initialization file. |
| [activity.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/models/activity.py) | `.py` | 24 | 761 | **Classes**: `UserActivity` |
| [admin.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/models/admin.py) | `.py` | 15 | 529 | **Classes**: `AdminUser` |
| [blog.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/models/blog.py) | `.py` | 14 | 441 | **Classes**: `Blog` |
| [feedback.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/models/feedback.py) | `.py` | 29 | 1017 | **Classes**: `Feedback` |
| [user.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/models/user.py) | `.py` | 57 | 1769 | **Classes**: `User, UserProfile` |

### 📁 Directory: `astro-platform\app\schemas` (9 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/schemas/__init__.py) | `.py` | 43 | 1172 | Python package initialization file. |
| [auth.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/schemas/auth.py) | `.py` | 26 | 544 | **Classes**: `UserRegister, UserLogin, AdminLogin, TokenResponse` |
| [blog.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/schemas/blog.py) | `.py` | 22 | 444 | **Classes**: `BlogCreate, BlogUpdate, BlogResponse` |
| [feedback.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/schemas/feedback.py) | `.py` | 42 | 1105 | **Classes**: `FeedbackCreate, ActivityCreate, FeedbackResponse` |
| [horoscope.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/schemas/horoscope.py) | `.py` | 26 | 620 | **Classes**: `HoroscopeResponse, FestivalItem, FestivalListResponse` |
| [kundali.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/schemas/kundali.py) | `.py` | 66 | 1549 | **Classes**: `BirthData, KundaliRequest, KundaliChatRequest, PlanetDetail`... |
| [panchang.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/schemas/panchang.py) | `.py` | 22 | 605 | **Classes**: `PanchangRequest, PanchangResponse` |
| [prediction.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/schemas/prediction.py) | `.py` | 22 | 631 | **Classes**: `PredictionRequest, ChatRequest, DomainRequest` |
| [user.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/schemas/user.py) | `.py` | 40 | 880 | **Classes**: `UserProfileUpdate, UserProfileResponse, UserResponse` |

### 📁 Directory: `astro-platform\app\services` (7 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/__init__.py) | `.py` | 19 | 549 | Python package initialization file. |
| [auth_service.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/auth_service.py) | `.py` | 60 | 1849 | **Doc**: Authentication, registration, and session management service. <br> **Classes**: `AuthService` |
| [blog_service.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/blog_service.py) | `.py` | 69 | 2296 | **Doc**: Blog CRUD and administrative management service with multi-language support. <br> **Classes**: `BlogService` |
| [feedback_service.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/feedback_service.py) | `.py` | 52 | 1843 | **Doc**: User Feedback collection and Activity audit logging service. <br> **Classes**: `FeedbackService` |
| [pdf_service.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/pdf_service.py) | `.py` | 124 | 4803 | **Doc**: PDF Report generation service for Kundali and Horoscope charts using in-memory buffers. <br> **Functions**: `generate_kundali_pdf_buffer` |
| [translation_service.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/translation_service.py) | `.py` | 104 | 6978 | **Doc**: Localization and astrology terminology translation service. <br> **Functions**: `load_translations, get_translation, translate_astrology_term` |
| [user_service.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/user_service.py) | `.py` | 40 | 1342 | **Doc**: User Profile and Account management service. <br> **Classes**: `UserService` |

### 📁 Directory: `astro-platform\app\services\ai_engine` (5 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/ai_engine/__init__.py) | `.py` | 16 | 459 | Python package initialization file. |
| [chat_service.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/ai_engine/chat_service.py) | `.py` | 212 | 10889 | **Doc**: Vedic Astrology Smart Chat Service answering user queries from Natal Chart data with i18n support. <br> **Classes**: `ChatService` |
| [llm_client.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/ai_engine/llm_client.py) | `.py` | 108 | 4520 | **Doc**: Unified LLM client supporting Ollama and OpenAI with graceful rule-based fallback. <br> **Classes**: `LLMClient` <br> **Functions**: `ask_llm` |
| [prediction_service.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/ai_engine/prediction_service.py) | `.py` | 41 | 1508 | **Doc**: AI Prediction Orchestrator for Marriage, Career, and Life Domains. <br> **Classes**: `PredictionService` |
| [prompt_builder.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/ai_engine/prompt_builder.py) | `.py` | 62 | 2566 | **Doc**: Token-optimized astrological prompt formatting utilities with multi-language (i18n) support. <br> **Functions**: `build_prediction_prompt, build_chat_prompt` |

### 📁 Directory: `astro-platform\app\services\astrology_engine` (20 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/__init__.py) | `.py` | 63 | 2249 | Python package initialization file. |
| [aspects.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/aspects.py) | `.py` | 42 | 1438 | **Doc**: Vedic Planetary Aspects (Drishti) Engine. <br> **Functions**: `calculate_vedic_aspects` |
| [charts.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/charts.py) | `.py` | 189 | 7054 | **Doc**: Full Chart Calculation and Orchestration Engine. <br> **Functions**: `calculate_house_lords, classify_functional_nature, calculate_dispositors, evaluate_event, build_event_explanation`... |
| [cities.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/cities.py) | `.py` | 168 | 8263 | **Doc**: Comprehensive city database and coordinates resolver for Indian and international cities. <br> **Functions**: `get_city, get_city_names` |
| [dasha.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/dasha.py) | `.py` | 105 | 3042 | **Doc**: Vimshottari Dasha calculation engine. <br> **Functions**: `calculate_mahadasha, generate_dasha_timeline, generate_antardasha, generate_dasha_calendar` |
| [domain_analysis.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/domain_analysis.py) | `.py` | 2633 | 131768 | **Doc**: domain_engine.py — Complete Life Domain Analysis Engine <br> **Functions**: `_functional_nature, _ordinal, _positional_strength, _house_strength, _retrograde_modifier`... |
| [doshas.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/doshas.py) | `.py` | 156 | 5393 | **Doc**: Vedic Doshas detection engine with remedies. <br> **Functions**: `_get_planet_map, _house_of, _sign_of, calculate_doshas` |
| [festival.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/festival.py) | `.py` | 326 | 29138 | **Doc**: Live Hindu Festival Engine computed from Swiss Ephemeris lunar & solar data with astronomical precision. <br> **Functions**: `_get_lunar_day_details, get_day_festivals, get_today_festivals, get_upcoming_festivals` |
| [horoscope.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/horoscope.py) | `.py` | 106 | 4742 | **Doc**: Dynamic transit-driven daily horoscope engine. <br> **Functions**: `generate_horoscope, generate_all_horoscopes` |
| [houses.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/houses.py) | `.py` | 74 | 1973 | **Doc**: Lagna (Ascendant) and house calculation engine. <br> **Functions**: `calculate_lagna, assign_house, assign_bhava_house` |
| [kundali.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/kundali.py) | `.py` | 240 | 8830 | **Doc**: Master Kundali Engine assembling Rasi, Navamsa D9, Dasha, Yogas, Doshas, and Scores. <br> **Functions**: `calculate_chart_scores, calculate_kundali` |
| [nakshatra.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/nakshatra.py) | `.py` | 45 | 1608 | **Doc**: Nakshatra and Pada calculation utilities. <br> **Functions**: `calculate_nakshatra, get_nakshatra_pada, get_nakshatra_lord` |
| [navamsa.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/navamsa.py) | `.py` | 37 | 1076 | **Doc**: Navamsa (D9) Divisional Chart calculations. <br> **Functions**: `calculate_navamsa, calculate_navamsa_sign` |
| [panchang.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/panchang.py) | `.py` | 118 | 4433 | **Doc**: Vedic Panchang Calculation Engine. <br> **Functions**: `calculate_panchang_for_datetime, get_full_panchang` |
| [planets.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/planets.py) | `.py` | 89 | 2225 | **Doc**: Swiss Ephemeris precision planetary calculations. <br> **Functions**: `calculate_all_planets, calculate_planets_with_speed` |
| [strength.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/strength.py) | `.py` | 108 | 3624 | **Doc**: Planetary Dignity, Exaltation, Debilitation, and Strength Scoring. <br> **Functions**: `planet_strength_label, final_strength, calculate_weighted_strength` |
| [timing.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/timing.py) | `.py` | 48 | 1654 | **Doc**: Event timing and Dasha activation engine. <br> **Functions**: `evaluate_event_trigger` |
| [transits.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/transits.py) | `.py` | 48 | 1509 | **Doc**: Real-time planetary transits engine. <br> **Functions**: `calculate_transits` |
| [yogas.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/yogas.py) | `.py` | 164 | 6709 | **Doc**: Classical Vedic Astrology Yogas Detection Engine. <br> **Functions**: `_get_planet_map, _house_of, _sign_of, calculate_yogas, detect_advanced_yogas` |
| [zodiac.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/services/astrology_engine/zodiac.py) | `.py` | 51 | 1538 | **Doc**: Zodiac signs and degree conversion utilities. <br> **Functions**: `degree_to_sign, to_dms` |

### 📁 Directory: `astro-platform\app\static\js` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [i18n.js](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/static/js/i18n.js) | `.js` | 66 | 2169 | Client-side JavaScript interaction logic. |
| [kundali.js](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/static/js/kundali.js) | `.js` | 1095 | 56235 | Client-side JavaScript interaction logic. |

### 📁 Directory: `astro-platform\app\static\locales` (3 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [en.json](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/static/locales/en.json) | `.json` | 14 | 337 | JSON data / localization translations dictionary. |
| [hi.json](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/static/locales/hi.json) | `.json` | 14 | 491 | JSON data / localization translations dictionary. |
| [mr.json](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/static/locales/mr.json) | `.json` | 60 | 3964 | JSON data / localization translations dictionary. |

### 📁 Directory: `astro-platform\app\static\svg` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [navamsa.svg](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/static/svg/navamsa.svg) | `.svg` | 52 | 1541 | Scalable Vector Graphic chart diagram. |
| [north_indian_kundali.svg](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/static/svg/north_indian_kundali.svg) | `.svg` | 52 | 1541 | Scalable Vector Graphic chart diagram. |

### 📁 Directory: `astro-platform\app\templates` (19 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [Untitled-1.md](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/Untitled-1.md) | `.md` | 148 | 5131 | Project asset or configuration file. |
| [about.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/about.html) | `.html` | 401 | 27602 | HTML UI template / page view. |
| [admin-activity.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/admin-activity.html) | `.html` | 63 | 5374 | HTML UI template / page view. |
| [admin-blog.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/admin-blog.html) | `.html` | 160 | 8475 | HTML UI template / page view. |
| [admin-feedback.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/admin-feedback.html) | `.html` | 57 | 4656 | HTML UI template / page view. |
| [admin-login.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/admin-login.html) | `.html` | 97 | 4165 | HTML UI template / page view. |
| [admin-users.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/admin-users.html) | `.html` | 61 | 5592 | HTML UI template / page view. |
| [auth.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/auth.html) | `.html` | 463 | 11090 | HTML UI template / page view. |
| [base.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/base.html) | `.html` | 15 | 942 | HTML UI template / page view. |
| [blog-detail.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/blog-detail.html) | `.html` | 134 | 6982 | HTML UI template / page view. |
| [blogs.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/blogs.html) | `.html` | 386 | 21581 | HTML UI template / page view. |
| [daily-horoscope.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/daily-horoscope.html) | `.html` | 498 | 27142 | HTML UI template / page view. |
| [index.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/index.html) | `.html` | 723 | 41472 | HTML UI template / page view. |
| [kundali.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/kundali.html) | `.html` | 1540 | 82809 | HTML UI template / page view. |
| [kundali.js](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/kundali.js) | `.js` | 1095 | 56235 | Client-side JavaScript interaction logic. |
| [panchang.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/panchang.html) | `.html` | 1057 | 56932 | HTML UI template / page view. |
| [prediction.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/prediction.html) | `.html` | 725 | 47105 | HTML UI template / page view. |
| [profile.html](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/profile.html) | `.html` | 653 | 13893 | HTML UI template / page view. |
| [vercel.json](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/app/templates/vercel.json) | `.json` | 14 | 598 | Routing configuration for deploying the frontend static distribution on Vercel. |

## 13. Root Test Suite (`astro-platform/tests/`)


### 📁 Directory: `astro-platform\tests` (5 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/tests/__init__.py) | `.py` | 1 | 20 | **Doc**: Test package. |
| [conftest.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/tests/conftest.py) | `.py` | 11 | 282 | **Doc**: Pytest fixtures and database initialization. <br> **Functions**: `setup_test_database` |
| [test_api_routes.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/tests/test_api_routes.py) | `.py` | 160 | 4263 | **Doc**: Integration tests for FastAPI endpoints. <br> **Functions**: `test_get_cities, test_generate_chart_endpoint, test_kundali_endpoint, test_panchang_endpoint, test_daily_horoscope_endpoint`... |
| [test_astrology_engine.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/tests/test_astrology_engine.py) | `.py` | 153 | 4076 | **Doc**: Unit tests for Pure Astrology Calculation Engine. <br> **Functions**: `test_zodiac_and_dms, test_nakshatra_calculation, test_navamsa_calculation, test_planet_calculation, test_lagna_calculation`... |
| [test_auth_and_db.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/tests/test_auth_and_db.py) | `.py` | 80 | 2467 | **Doc**: Database and Authentication tests. <br> **Functions**: `db, test_password_hashing, test_user_registration_and_auth, test_blog_crud` |

## 14. Documentation Directory (`astro-platform/docs/`)


### 📁 Directory: `astro-platform\docs` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [COMPLETE_WORKSPACE_FILE_REFERENCE.md](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/docs/COMPLETE_WORKSPACE_FILE_REFERENCE.md) | `.md` | 871 | 108606 | Project asset or configuration file. |
| [CURRENT_PROJECT_PHASE.md](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/docs/CURRENT_PROJECT_PHASE.md) | `.md` | 134 | 11049 | Official project status document defining the completion of Phase 5 (Timing Fusion Engine) and roadmap for Phase 6 (Empirical Validation). |

## 15. Astro-Platform Platform Root (`astro-platform/`)


### 📁 Directory: `astro-platform` (10 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [.env](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/.env) | `plain` | 20 | 666 | Active environment variables file (database URLs, JWT secrets, CORS settings). |
| [.env.example](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/.env.example) | `.example` | 20 | 451 | Template configuration file for required environment variables. |
| [.gitignore](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/.gitignore) | `plain` | 215 | 4965 | Project asset or configuration file. |
| [LICENSE](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/LICENSE) | `plain` | 21 | 1097 | MIT Open Source License file. |
| [README.md](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/README.md) | `.md` | 138 | 8226 | Master platform documentation, architectural diagram, and execution guide. |
| [__init__.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/__init__.py) | `.py` | 1 | 62 | **Doc**: Backend package for the gradual AstroLogicAI migration. |
| [alembic.ini](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/alembic.ini) | `.ini` | 41 | 668 | Database migration configuration file for SQLAlchemy and Alembic. |
| [astrologic.db](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/astrologic.db) | `.db` | 116 | 73728 | Production/development SQLite database containing user accounts, blog posts, feedback, and telemetry data. |
| [requirements.txt](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/requirements.txt) | `.txt` | 15 | 278 | Python dependencies specification (FastAPI, Uvicorn, pyswisseph, SQLAlchemy, Pydantic, etc.). |
| [runtime.txt](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/runtime.txt) | `.txt` | 1 | 15 | Specifies runtime Python version (e.g., `python-3.11.4`) for cloud deployment environments. |

## 16. Miscellaneous Workspace Files


### 📁 Directory: `astro-platform\alembic` (2 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [env.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/alembic/env.py) | `.py` | 61 | 1548 | **Functions**: `run_migrations_offline, run_migrations_online` |
| [script.py.mako](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/alembic/script.py.mako) | `.mako` | 23 | 469 | Alembic database migration template. |

### 📁 Directory: `astro-platform\alembic\versions` (1 files)

| File Name | Type | Lines | Size (Bytes) | Role & Key Components |
| :--- | :---: | :---: | :---: | :--- |
| [20260526_0001_initial_postgresql_schema.py](file:///c:/Desktop/astro_may_res%20%282%29/astro-platform/alembic/versions/20260526_0001_initial_postgresql_schema.py) | `.py` | 110 | 5120 | **Doc**: initial postgresql schema <br> **Functions**: `upgrade, downgrade` |