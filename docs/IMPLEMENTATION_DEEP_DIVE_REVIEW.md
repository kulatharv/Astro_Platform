# 🔬 AstroLogic AI: Comprehensive Implementation-Level Architectural Deep-Dive Review

**Auditor:** Senior Principal Software Architect  
**Project:** AstroLogic AI (Vedic Astrology & AI Prediction Platform)  
**Target Baseline:** Production Modular Monolith (FastAPI + Swiss Ephemeris + Redis + PostgreSQL/SQLite + Vanilla ES6/Jinja2)  
**Review Date:** October 2026  
**Status:** Verification Baseline for Extension Tasks (Uncertainty Propagation, Sensitivity Endpoints, Calibration, Guardrails)

---

## 📑 TABLE OF CONTENTS
1. [FULL DIRECTORY TREE](#1-full-directory-tree)
2. [ACTUAL CODE — KEY MODULES](#2-actual-code--key-modules)
3. [DATA MODELS & SCHEMAS (exact)](#3-data-models--schemas-exact)
4. [API CONTRACTS (exact)](#4-api-contracts-exact)
5. [CORE ALGORITHMS (exact implementation)](#5-core-algorithms-exact-implementation)
6. [CACHING & QUEUE (exact)](#6-caching--queue-exact)
7. [AUTH & SECURITY (exact)](#7-auth--security-exact)
8. [TEST SUITE (exact)](#8-test-suite-exact)
9. [FRONTEND](#9-frontend)
10. [DEPLOYMENT & INFRA](#10-deployment--infra)
11. [KNOWN GAPS, TODOS, AND DEBT](#11-known-gaps-todos-and-debt)
12. [PERFORMANCE BASELINE](#12-performance-baseline)
13. [ACCURACY BASELINE (critical for next steps)](#13-accuracy-baseline-critical-for-my-next-step)
14. [EXTENSION READINESS FOR MY NEXT TASK](#14-extension-readiness-for-my-next-task)

---

## 1. FULL DIRECTORY TREE

Below is the complete inventory of active source trees (`backend/`, `frontend/`, `tests/`, `workers/`, `shared/`, `modules/`, `gateway/`, and infra/config). Stubs and 0-byte placeholders from early monolithic scaffolding are explicitly marked `[STUB - 0 LOC]`.

```text
astro-platform/backend/gateway/deps.py                                 |    38 LOC | Configuration, asset or migration script
astro-platform/backend/gateway/main.py                                 |   211 LOC | Gateway app entrypoint, routing & edge middlewares
astro-platform/backend/gateway/pages.py                                |    80 LOC | Jinja2 HTML template rendering page endpoints
astro-platform/backend/gateway/settings.py                             |     5 LOC | Configuration, asset or migration script
astro-platform/backend/gateway/middleware/language.py                  |    53 LOC | Configuration, asset or migration script
astro-platform/backend/modules/auth/__init__.py                        |     4 LOC | Package export / initialization
astro-platform/backend/modules/auth/api.py                             |   235 LOC | Module edge HTTP routers & public service facades
astro-platform/backend/modules/auth/engine.py                          |    74 LOC | Module core business calculation engine
astro-platform/backend/modules/auth/models.py                          |    87 LOC | SQLAlchemy ORM database entity declarations
astro-platform/backend/modules/auth/repository.py                      |    66 LOC | Database query & persistence layer
astro-platform/backend/modules/auth/schemas.py                         |    65 LOC | Pydantic validation & serialization models
astro-platform/backend/modules/auth/security.py                        |    33 LOC | Password hashing & token verification
astro-platform/backend/modules/blog/__init__.py                        |     4 LOC | Package export / initialization
astro-platform/backend/modules/blog/api.py                             |    71 LOC | Module edge HTTP routers & public service facades
astro-platform/backend/modules/blog/engine.py                          |    25 LOC | Module core business calculation engine
astro-platform/backend/modules/blog/models.py                          |    23 LOC | SQLAlchemy ORM database entity declarations
astro-platform/backend/modules/blog/repository.py                      |    39 LOC | Database query & persistence layer
astro-platform/backend/modules/blog/schemas.py                         |    35 LOC | Pydantic validation & serialization models
astro-platform/backend/modules/feedback/__init__.py                    |     4 LOC | Package export / initialization
astro-platform/backend/modules/feedback/api.py                         |    32 LOC | Module edge HTTP routers & public service facades
astro-platform/backend/modules/feedback/engine.py                      |    18 LOC | Module core business calculation engine
astro-platform/backend/modules/feedback/models.py                      |    31 LOC | SQLAlchemy ORM database entity declarations
astro-platform/backend/modules/feedback/repository.py                  |    37 LOC | Database query & persistence layer
astro-platform/backend/modules/feedback/schemas.py                     |    23 LOC | Pydantic validation & serialization models
astro-platform/backend/modules/horoscope/__init__.py                   |     4 LOC | Package export / initialization
astro-platform/backend/modules/horoscope/api.py                        |    62 LOC | Module edge HTTP routers & public service facades
astro-platform/backend/modules/horoscope/engine.py                     |   106 LOC | Module core business calculation engine
astro-platform/backend/modules/horoscope/schemas.py                    |    21 LOC | Pydantic validation & serialization models
astro-platform/backend/modules/horoscope/rules/__init__.py             |     5 LOC | Package export / initialization
astro-platform/backend/modules/horoscope/rules/daily.py                |   174 LOC | Configuration, asset or migration script
astro-platform/backend/modules/horoscope/rules/definitions.py          |   227 LOC | Configuration, asset or migration script
astro-platform/backend/modules/kundali/__init__.py                     |     4 LOC | Package export / initialization
astro-platform/backend/modules/kundali/api.py                          |   125 LOC | Module edge HTTP routers & public service facades
astro-platform/backend/modules/kundali/cache.py                        |    15 LOC | Configuration, asset or migration script
astro-platform/backend/modules/kundali/cities.py                       |   186 LOC | Configuration, asset or migration script
astro-platform/backend/modules/kundali/dasha.py                        |   169 LOC | Configuration, asset or migration script
astro-platform/backend/modules/kundali/engine.py                       |   243 LOC | Module core business calculation engine
astro-platform/backend/modules/kundali/houses.py                       |    74 LOC | Configuration, asset or migration script
astro-platform/backend/modules/kundali/planets.py                      |    89 LOC | Configuration, asset or migration script
astro-platform/backend/modules/kundali/schemas.py                      |    66 LOC | Pydantic validation & serialization models
astro-platform/backend/modules/kundali/varga.py                        |   229 LOC | Configuration, asset or migration script
astro-platform/backend/modules/narrative/__init__.py                   |     4 LOC | Package export / initialization
astro-platform/backend/modules/narrative/api.py                        |   105 LOC | Module edge HTTP routers & public service facades
astro-platform/backend/modules/narrative/chat.py                       |   210 LOC | Configuration, asset or migration script
astro-platform/backend/modules/narrative/engine.py                     |    39 LOC | Module core business calculation engine
astro-platform/backend/modules/narrative/jobs.py                       |   110 LOC | Configuration, asset or migration script
astro-platform/backend/modules/narrative/llm_client.py                 |   108 LOC | Configuration, asset or migration script
astro-platform/backend/modules/narrative/prompt_builder.py             |    62 LOC | Configuration, asset or migration script
astro-platform/backend/modules/narrative/schemas.py                    |    64 LOC | Pydantic validation & serialization models
astro-platform/backend/modules/panchang/__init__.py                    |     4 LOC | Package export / initialization
astro-platform/backend/modules/panchang/api.py                         |   216 LOC | Module edge HTTP routers & public service facades
astro-platform/backend/modules/panchang/engine.py                      |   709 LOC | Module core business calculation engine
astro-platform/backend/modules/panchang/festival.py                    |   300 LOC | Configuration, asset or migration script
astro-platform/backend/modules/panchang/ics.py                         |    96 LOC | Configuration, asset or migration script
astro-platform/backend/modules/panchang/image.py                       |   435 LOC | Configuration, asset or migration script
astro-platform/backend/modules/panchang/personalization.py             |   914 LOC | Configuration, asset or migration script
astro-platform/backend/modules/panchang/schemas.py                     |    98 LOC | Pydantic validation & serialization models
astro-platform/backend/modules/prediction/__init__.py                  |     4 LOC | Package export / initialization
astro-platform/backend/modules/prediction/api.py                       |   137 LOC | Module edge HTTP routers & public service facades
astro-platform/backend/modules/prediction/engine.py                    |    62 LOC | Module core business calculation engine
astro-platform/backend/modules/prediction/remedies.py                  |   102 LOC | Configuration, asset or migration script
astro-platform/backend/modules/prediction/schemas.py                   |    59 LOC | Pydantic validation & serialization models
astro-platform/backend/modules/prediction/scoring.py                   |   273 LOC | Configuration, asset or migration script
astro-platform/backend/modules/prediction/timing.py                    |   162 LOC | Configuration, asset or migration script
astro-platform/backend/modules/prediction/timing_config.py             |   196 LOC | Configuration, asset or migration script
astro-platform/backend/modules/prediction/timing_dasha.py              |   222 LOC | Vimshottari Dasha 15-year progression evaluator
astro-platform/backend/modules/prediction/timing_fusion.py             |   225 LOC | Phase 5 Dasha (60%) + Gochara (40%) event window fusion
astro-platform/backend/modules/prediction/timing_transit.py            |   270 LOC | Gochara Jupiter/Saturn transit monthly scorer
astro-platform/backend/modules/prediction/transit_forecast.py          |   151 LOC | Configuration, asset or migration script
astro-platform/backend/modules/prediction/transits.py                  |    48 LOC | Configuration, asset or migration script
astro-platform/backend/modules/prediction/domains/__init__.py          |     1 LOC | Package export / initialization
astro-platform/backend/modules/prediction/domains/career.py            |   106 LOC | Configuration, asset or migration script
astro-platform/backend/modules/prediction/domains/challenges.py        |    76 LOC | Configuration, asset or migration script
astro-platform/backend/modules/prediction/domains/children.py          |    55 LOC | Configuration, asset or migration script
astro-platform/backend/modules/prediction/domains/education.py         |    64 LOC | Configuration, asset or migration script
astro-platform/backend/modules/prediction/domains/health.py            |    88 LOC | Configuration, asset or migration script
astro-platform/backend/modules/prediction/domains/marriage.py          |   130 LOC | Configuration, asset or migration script
astro-platform/backend/modules/prediction/domains/property.py          |    61 LOC | Configuration, asset or migration script
astro-platform/backend/modules/prediction/domains/spirituality.py      |    67 LOC | Configuration, asset or migration script
astro-platform/backend/modules/prediction/domains/travel.py            |    52 LOC | Configuration, asset or migration script
astro-platform/backend/modules/prediction/domains/wealth.py            |    87 LOC | Configuration, asset or migration script
astro-platform/backend/shared/__init__.py                              |     1 LOC | Package export / initialization
astro-platform/backend/shared/cache/__init__.py                        |     5 LOC | Package export / initialization
astro-platform/backend/shared/cache/decorators.py                      |    77 LOC | @cached_chart fail-open caching decorator
astro-platform/backend/shared/cache/envelope.py                        |    47 LOC | Configuration, asset or migration script
astro-platform/backend/shared/cache/keys.py                            |    46 LOC | Configuration, asset or migration script
astro-platform/backend/shared/cache/metrics.py                         |    44 LOC | Configuration, asset or migration script
astro-platform/backend/shared/cache/redis_client.py                    |   156 LOC | Two-tier in-memory LRU + Redis cache wrapper
astro-platform/backend/shared/config/__init__.py                       |     6 LOC | Package export / initialization
astro-platform/backend/shared/config/constants.py                      |    19 LOC | Configuration, asset or migration script
astro-platform/backend/shared/config/settings.py                       |    88 LOC | Configuration, asset or migration script
astro-platform/backend/shared/db/__init__.py                           |     4 LOC | Package export / initialization
astro-platform/backend/shared/db/session.py                            |    35 LOC | Configuration, asset or migration script
astro-platform/backend/shared/ephemeris/__init__.py                    |     4 LOC | Package export / initialization
astro-platform/backend/shared/ephemeris/wrapper.py                     |    27 LOC | Configuration, asset or migration script
astro-platform/backend/shared/errors/__init__.py                       |    10 LOC | Package export / initialization
astro-platform/backend/shared/errors/types.py                          |    32 LOC | Configuration, asset or migration script
astro-platform/backend/shared/i18n/__init__.py                         |    17 LOC | Package export / initialization
astro-platform/backend/shared/i18n/translation.py                      |   114 LOC | Configuration, asset or migration script
astro-platform/backend/shared/logging/__init__.py                      |     4 LOC | Package export / initialization
astro-platform/backend/shared/logging/logger.py                        |    26 LOC | Configuration, asset or migration script
astro-platform/backend/shared/queue/__init__.py                        |     5 LOC | Package export / initialization
astro-platform/backend/shared/queue/redis_queue.py                     |    76 LOC | Redis/memory async task queue abstraction
astro-platform/backend/shared/timezone/__init__.py                     |    10 LOC | Package export / initialization
astro-platform/backend/shared/timezone/tz.py                           |    63 LOC | Configuration, asset or migration script
astro-platform/backend/shared/veda/__init__.py                         |    27 LOC | Package export / initialization
astro-platform/backend/shared/veda/aspects.py                          |    42 LOC | Configuration, asset or migration script
astro-platform/backend/shared/veda/combustion.py                       |    38 LOC | Configuration, asset or migration script
astro-platform/backend/shared/veda/constants.py                        |    40 LOC | Configuration, asset or migration script
astro-platform/backend/shared/veda/dignity.py                          |    93 LOC | Configuration, asset or migration script
astro-platform/backend/shared/veda/doshas.py                           |   256 LOC | Configuration, asset or migration script
astro-platform/backend/shared/veda/nakshatra.py                        |    45 LOC | Configuration, asset or migration script
astro-platform/backend/shared/veda/neech_bhanga.py                     |    54 LOC | Configuration, asset or migration script
astro-platform/backend/shared/veda/strength.py                         |   107 LOC | Configuration, asset or migration script
astro-platform/backend/shared/veda/yogas.py                            |   164 LOC | Configuration, asset or migration script
astro-platform/backend/shared/veda/zodiac.py                           |    52 LOC | Configuration, asset or migration script
astro-platform/backend/workers/README.md                               |    31 LOC | Configuration, asset or migration script
astro-platform/backend/workers/__init__.py                             |     1 LOC | Package export / initialization
astro-platform/backend/workers/narrative_worker.py                     |    83 LOC | Background worker consuming narrative LLM jobs
astro-platform/backend/workers/pdf_worker.py                           |   124 LOC | Configuration, asset or migration script
astro-platform/backend/workers/queue_config.py                         |    15 LOC | Configuration, asset or migration script
astro-platform/backend/workers/start.sh                                |     6 LOC | Configuration, asset or migration script
astro-platform/backend/alembic/env.py                                  |    61 LOC | Configuration, asset or migration script
astro-platform/backend/alembic/script.py.mako                          |    23 LOC | Configuration, asset or migration script
astro-platform/backend/alembic/versions/20260526_0001_initial_postgresql_schema.py |   110 LOC | Configuration, asset or migration script
astro-platform/backend/alembic/versions/20260825_0002_add_admin_users_table.py |    34 LOC | Configuration, asset or migration script
astro-platform/backend/alembic/versions/20260825_0003_add_language_to_blogs.py |    23 LOC | Configuration, asset or migration script
astro-platform/backend/scripts/build_cities_db.py                      |   112 LOC | Configuration, asset or migration script
astro-platform/backend/tests/__init__.py                               |     1 LOC | Package export / initialization
astro-platform/backend/tests/conftest.py                               |    16 LOC | Configuration, asset or migration script
astro-platform/backend/tests/test_api_routes.py                        |   176 LOC | Automated test suite module
astro-platform/backend/tests/test_astrology_engine.py                  |   198 LOC | Automated test suite module
astro-platform/backend/tests/test_auth_and_db.py                       |    83 LOC | Automated test suite module
astro-platform/backend/tests/test_benchmark_regression.py              |    69 LOC | Automated test suite module
astro-platform/backend/tests/test_drikpanchang_reference.py            |   117 LOC | Automated test suite module
astro-platform/backend/tests/test_i18n.py                              |   186 LOC | Automated test suite module
astro-platform/backend/tests/test_panchang_enterprise.py               |   255 LOC | Automated test suite module
astro-platform/backend/tests/test_panchang_personalization.py          |   291 LOC | Automated test suite module
astro-platform/backend/tests/test_panchang_share_image.py              |   146 LOC | Automated test suite module
astro-platform/backend/tests/test_reference_charts.py                  |   142 LOC | Automated test suite module
astro-platform/backend/tests/test_security_phase0.py                   |   138 LOC | Automated test suite module
astro-platform/backend/tests/backtest/test_timing_accuracy.py          |    58 LOC | Automated test suite module
astro-platform/backend/tests/contract/test_module_boundaries.py        |    19 LOC | Automated test suite module
astro-platform/backend/tests/integration/test_async_narrative.py       |    71 LOC | Automated test suite module
astro-platform/backend/tests/integration/test_cache_end_to_end.py      |    98 LOC | Automated test suite module
astro-platform/backend/tests/integration/test_module_integration.py    |    40 LOC | Automated test suite module
astro-platform/backend/tests/integration/test_timing_end_to_end.py     |    63 LOC | Automated test suite module
astro-platform/backend/tests/unit/test_cache_decorators.py             |    42 LOC | Automated test suite module
astro-platform/backend/tests/unit/test_cache_envelope.py               |    29 LOC | Automated test suite module
astro-platform/backend/tests/unit/test_cache_keys.py                   |    35 LOC | Automated test suite module
astro-platform/backend/tests/unit/test_domain_timing_integration.py    |   112 LOC | Automated test suite module
astro-platform/backend/tests/unit/test_narrative_jobs.py               |    49 LOC | Automated test suite module
astro-platform/backend/tests/unit/test_queue.py                        |    24 LOC | Automated test suite module
astro-platform/backend/tests/unit/test_timing_dasha.py                 |   135 LOC | Automated test suite module
astro-platform/backend/tests/unit/test_timing_fusion.py                |   257 LOC | Automated test suite module
astro-platform/backend/tests/unit/test_timing_transit.py               |   150 LOC | Automated test suite module
astro-platform/backend/tests/unit/test_transit_forecast.py             |    79 LOC | Automated test suite module
astro-platform/backend/app/__init__.py                                 |     1 LOC | Package export / initialization
astro-platform/backend/app/main.py                                     |     5 LOC | Gateway app entrypoint, routing & edge middlewares
astro-platform/backend/app/ai/__init__.py                              |     0 LOC | [STUB / UNUSED - 0 LOC]
astro-platform/backend/app/ai/llm_service.py                           |     0 LOC | [STUB / UNUSED - 0 LOC]
astro-platform/backend/app/ai/prompt_builder.py                        |     0 LOC | [STUB / UNUSED - 0 LOC]
astro-platform/backend/app/ai/rag_service.py                           |     0 LOC | [STUB / UNUSED - 0 LOC]
astro-platform/backend/app/api/__init__.py                             |     1 LOC | Package export / initialization
astro-platform/backend/app/api/api.py                                  |   769 LOC | Module edge HTTP routers & public service facades
astro-platform/backend/app/api/blogs.py                                |    90 LOC | Configuration, asset or migration script
astro-platform/backend/app/api/schemas/chart_schemas.py                |    11 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/__init__.py                       |     8 LOC | Package export / initialization
astro-platform/backend/app/astrology/aspects.py                        |    32 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/chart_engine.py                   |   156 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/chat_mode.py                      |    48 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/cities.py                         |   299 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/dasha.py                          |   138 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/dasha_activation.py               |    23 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/data                              |   376 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/dataset                           |   907 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/dispositor.py                     |    22 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/domain_engine.py                  |  2633 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/event_engine.py                   |   134 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/explanation_builder.py            |    86 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/festival_engine.py                |  1503 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/functional_nature.py              |    30 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/horoscope_engine.py               |   672 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/house_lords.py                    |    36 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/houses.py                         |    74 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/julian.py                         |     0 LOC | [STUB / UNUSED - 0 LOC]
astro-platform/backend/app/astrology/kundali_engine.py                 |  1035 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/llm_engine.py                     |    72 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/llm_layer.py                      |    32 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/nakshatra.py                      |    25 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/navamsa.py                        |    29 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/panchang_engine.py                |   751 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/planets.py                        |    33 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/prediction.py                     |    21 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/prediction_builder.py             |    83 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/scoring.py                        |    57 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/strength.py                       |    58 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/sunrise_engine.py                 |    19 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/timing_engine.py                  |    55 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/transits.py                       |    37 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/vedic_aspects.py                  |    38 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/weighted_strength.py              |    63 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/yogas.py                          |    26 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/yogas_engine.py                   |    63 LOC | Configuration, asset or migration script
astro-platform/backend/app/astrology/zodiac.py                         |    10 LOC | Configuration, asset or migration script
astro-platform/backend/app/astro_engine/strengths/functional_nature.py |    30 LOC | Configuration, asset or migration script
astro-platform/backend/app/core/__init__.py                            |     1 LOC | Package export / initialization
astro-platform/backend/app/core/config.py                              |    57 LOC | Configuration, asset or migration script
astro-platform/backend/app/core/constants.py                           |    15 LOC | Configuration, asset or migration script
astro-platform/backend/app/core/logger.py                              |    16 LOC | Configuration, asset or migration script
astro-platform/backend/app/core/security.py                            |    29 LOC | Password hashing & token verification
astro-platform/backend/app/database/__init__.py                        |     4 LOC | Package export / initialization
astro-platform/backend/app/database/base.py                            |     9 LOC | Configuration, asset or migration script
astro-platform/backend/app/database/init_db.py                         |    12 LOC | Configuration, asset or migration script
astro-platform/backend/app/database/session.py                         |   110 LOC | Configuration, asset or migration script
astro-platform/backend/app/models/__init__.py                          |     4 LOC | Package export / initialization
astro-platform/backend/app/models/activity_model.py                    |     3 LOC | Configuration, asset or migration script
astro-platform/backend/app/models/blog_model.py                        |    12 LOC | Configuration, asset or migration script
astro-platform/backend/app/models/feedback_model.py                    |     3 LOC | Configuration, asset or migration script
astro-platform/backend/app/models/kundali_model.py                     |     1 LOC | Configuration, asset or migration script
astro-platform/backend/app/models/user_model.py                        |    85 LOC | Configuration, asset or migration script
astro-platform/backend/app/schemas/__init__.py                         |     0 LOC | [STUB / UNUSED - 0 LOC]
astro-platform/backend/app/schemas/auth_schema.py                      |     0 LOC | [STUB / UNUSED - 0 LOC]
astro-platform/backend/app/schemas/chart_schema.py                     |    81 LOC | Configuration, asset or migration script
astro-platform/backend/app/schemas/feedback_schema.py                  |     0 LOC | [STUB / UNUSED - 0 LOC]
astro-platform/backend/app/schemas/user_schema.py                      |     0 LOC | [STUB / UNUSED - 0 LOC]
astro-platform/backend/app/services/__init__.py                        |     1 LOC | Package export / initialization
astro-platform/backend/app/services/ai_service.py                      |     0 LOC | [STUB / UNUSED - 0 LOC]
astro-platform/backend/app/services/horoscope_service.py               |    37 LOC | Configuration, asset or migration script
astro-platform/backend/app/services/prediction_service.py              |     0 LOC | [STUB / UNUSED - 0 LOC]
astro-platform/backend/app/services/translation_service.py             |    22 LOC | Configuration, asset or migration script
astro-platform/backend/app/services/user_service.py                    |     0 LOC | [STUB / UNUSED - 0 LOC]
astro-platform/backend/app/static/js/i18n.js                           |    66 LOC | Client-side JavaScript interaction logic
astro-platform/backend/app/static/js/kundali.js                        |  1095 LOC | Client-side JavaScript interaction logic
astro-platform/backend/app/static/locales/bn.json                      |    49 LOC | Localization dictionary / configuration
astro-platform/backend/app/static/locales/en.json                      |    14 LOC | Localization dictionary / configuration
astro-platform/backend/app/static/locales/gu.json                      |    49 LOC | Localization dictionary / configuration
astro-platform/backend/app/static/locales/hi.json                      |    14 LOC | Localization dictionary / configuration
astro-platform/backend/app/static/locales/kn.json                      |    49 LOC | Localization dictionary / configuration
astro-platform/backend/app/static/locales/mr.json                      |    14 LOC | Localization dictionary / configuration
astro-platform/backend/app/static/locales/ta.json                      |    49 LOC | Localization dictionary / configuration
astro-platform/backend/app/static/locales/te.json                      |    49 LOC | Localization dictionary / configuration
astro-platform/backend/app/static/svg/navamsa.svg                      |    52 LOC | Configuration, asset or migration script
astro-platform/backend/app/static/svg/north_indian_kundali.svg         |    52 LOC | Configuration, asset or migration script
astro-platform/backend/app/templates/Untitled-1.md                     |   148 LOC | Configuration, asset or migration script
astro-platform/backend/app/templates/about.html                        |   401 LOC | HTML web template / UI view
astro-platform/backend/app/templates/admin-activity.html               |    63 LOC | HTML web template / UI view
astro-platform/backend/app/templates/admin-blog.html                   |   160 LOC | HTML web template / UI view
astro-platform/backend/app/templates/admin-feedback.html               |    57 LOC | HTML web template / UI view
astro-platform/backend/app/templates/admin-login.html                  |    97 LOC | HTML web template / UI view
astro-platform/backend/app/templates/admin-users.html                  |    61 LOC | HTML web template / UI view
astro-platform/backend/app/templates/auth.html                         |   463 LOC | HTML web template / UI view
astro-platform/backend/app/templates/base.html                         |    34 LOC | HTML web template / UI view
astro-platform/backend/app/templates/blog-detail.html                  |   134 LOC | HTML web template / UI view
astro-platform/backend/app/templates/blogs.html                        |   386 LOC | HTML web template / UI view
astro-platform/backend/app/templates/daily-horoscope.html              |   498 LOC | HTML web template / UI view
astro-platform/backend/app/templates/index.html                        |   723 LOC | HTML web template / UI view
astro-platform/backend/app/templates/kundali.html                      |  1540 LOC | HTML web template / UI view
astro-platform/backend/app/templates/kundali.js                        |  1095 LOC | Client-side JavaScript interaction logic
astro-platform/backend/app/templates/panchang.html                     |   744 LOC | HTML web template / UI view
astro-platform/backend/app/templates/prediction.html                   |   725 LOC | HTML web template / UI view
astro-platform/backend/app/templates/profile.html                      |   653 LOC | HTML web template / UI view
astro-platform/backend/app/templates/vercel.json                       |    14 LOC | Localization dictionary / configuration
astro-platform/backend/app/utils/__init__.py                           |     0 LOC | [STUB / UNUSED - 0 LOC]
astro-platform/backend/app/utils/date_utils.py                         |     0 LOC | [STUB / UNUSED - 0 LOC]
astro-platform/backend/app/utils/helpers.py                            |     0 LOC | [STUB / UNUSED - 0 LOC]
astro-platform/backend/app/utils/validators.py                         |     0 LOC | [STUB / UNUSED - 0 LOC]
astro-platform/frontend/Untitled-1.md                                  |   148 LOC | Configuration, asset or migration script
astro-platform/frontend/about.html                                     |   401 LOC | HTML web template / UI view
astro-platform/frontend/admin-activity.html                            |    63 LOC | HTML web template / UI view
astro-platform/frontend/admin-blog.html                                |   160 LOC | HTML web template / UI view
astro-platform/frontend/admin-feedback.html                            |    57 LOC | HTML web template / UI view
astro-platform/frontend/admin-login.html                               |    97 LOC | HTML web template / UI view
astro-platform/frontend/admin-users.html                               |    61 LOC | HTML web template / UI view
astro-platform/frontend/auth.html                                      |   463 LOC | HTML web template / UI view
astro-platform/frontend/base.html                                      |    34 LOC | HTML web template / UI view
astro-platform/frontend/blog-detail.html                               |   134 LOC | HTML web template / UI view
astro-platform/frontend/blogs.html                                     |   386 LOC | HTML web template / UI view
astro-platform/frontend/daily-horoscope.html                           |   498 LOC | HTML web template / UI view
astro-platform/frontend/index.html                                     |   723 LOC | HTML web template / UI view
astro-platform/frontend/kundali.html                                   |  1540 LOC | HTML web template / UI view
astro-platform/frontend/kundali.js                                     |  1095 LOC | Client-side JavaScript interaction logic
astro-platform/frontend/panchang.html                                  |   744 LOC | HTML web template / UI view
astro-platform/frontend/prediction.html                                |   725 LOC | HTML web template / UI view
astro-platform/frontend/profile.html                                   |   653 LOC | HTML web template / UI view
astro-platform/frontend/vercel.json                                    |    14 LOC | Localization dictionary / configuration
astro-platform/frontend/js/kundali.js                                  |  1095 LOC | Client-side JavaScript interaction logic
astro-platform/frontend/locales/en.json                                |    14 LOC | Localization dictionary / configuration
astro-platform/frontend/locales/hi.json                                |    14 LOC | Localization dictionary / configuration
astro-platform/frontend/locales/mr.json                                |    14 LOC | Localization dictionary / configuration
astro-platform/frontend/svg/navamsa.svg                                |    52 LOC | Configuration, asset or migration script
astro-platform/frontend/svg/north_indian_kundali.svg                   |    52 LOC | Configuration, asset or migration script
astro-platform/tests/__init__.py                                       |     1 LOC | Package export / initialization
astro-platform/tests/conftest.py                                       |    11 LOC | Configuration, asset or migration script
astro-platform/tests/test_api_routes.py                                |   160 LOC | Automated test suite module
astro-platform/tests/test_astrology_engine.py                          |   153 LOC | Automated test suite module
astro-platform/tests/test_auth_and_db.py                               |    80 LOC | Automated test suite module
astro-platform/docs/COMPLETE_WORKSPACE_FILE_REFERENCE.md               |   875 LOC | Configuration, asset or migration script
astro-platform/docs/CURRENT_PROJECT_PHASE.md                           |   134 LOC | Configuration, asset or migration script
astro-platform/docs/LOW_LEVEL_DESIGN.md                                |   545 LOC | Configuration, asset or migration script
```

---

## 2. ACTUAL CODE — KEY MODULES

### a) gateway/main.py
**Path:** `astro-platform/backend/gateway/main.py`  
```python
"""FastAPI Gateway Application Entry Point & Edge Router."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware

from gateway.middleware.language import LanguageDetectionMiddleware
from shared.config.settings import settings
from shared.logging.logger import get_logger
from shared.db.session import init_db
from shared.i18n.translation import SUPPORTED_LANGUAGES, load_translations

from shared.cache.metrics import cache_metrics
from shared.cache.redis_client import CacheService

# Import 8 extracted service module routers
from modules.auth.api import router as auth_router, admin_router
from modules.kundali.api import router as kundali_router
from modules.panchang.api import router as panchang_router
from modules.prediction.api import router as prediction_router
from modules.narrative.api import router as narrative_router
from modules.horoscope.api import router as horoscope_router
from modules.blog.api import router as blog_router
from modules.feedback.api import router as feedback_router
from gateway.pages import router as pages_router


logger = get_logger("gateway.main")
BASE_DIR = Path(__file__).resolve().parent.parent / "app"


class DefaultDenyAuthMiddleware(BaseHTTPMiddleware):
    """Enforces strict default-deny security for all /api/* routes except explicit public allowlist."""

    PUBLIC_API_PREFIXES = (
        "/health",
        "/metrics",
        "/api/locales",
        "/api/panchang",
        "/api/festivals",
        "/api/horoscope",
        "/api/daily-horoscope",
        "/api/cities",
        "/api/auth/login",
        "/api/auth/signup",
        "/api/auth/logout",
    )

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Non-API routes (HTML pages, static files, docs) are allowed
        if not path.startswith("/api/"):
            return await call_next(request)

        # Public API routes allowed without authentication
        if any(path.startswith(prefix) for prefix in self.PUBLIC_API_PREFIXES):
            return await call_next(request)

        # Public GET endpoints for blogs
        if path.startswith("/api/blogs") and request.method == "GET":
            return await call_next(request)

        # Default-deny authorization check for all other API endpoints
        user_id = request.session.get("user_id")
        is_admin = request.session.get("admin") == "true"

        if not user_id and not is_admin:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authentication required. Default-deny policy enforced."},
            )

        return await call_next(request)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for application startup and shutdown."""
    logger.info(f"Starting {settings.app_name} in {settings.environment} mode via Gateway...")
    try:
        init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
    yield
    logger.info("Application shutdown complete.")


# Initialize FastAPI Gateway App
app = FastAPI(
    title=settings.app_name,
    description="Enterprise Vedic Astrology & AI Prediction Platform (Gateway)",
    version="2.0.0",
    lifespan=lifespan,
    debug=settings.debug,
)


@app.get("/health")
def health_check():
    """Application Health Check Endpoint."""
    return {"status": "ok", "app": settings.app_name, "environment": settings.environment}


@app.get("/metrics")
def get_metrics():
    """Expose application and cache counters for observability/Prometheus."""
    return {
        "status": "ok",
        "cache": cache_metrics.get_stats(),
    }


@app.get("/api/admin/cache/stats")
def get_admin_cache_stats(request: Request):
    """Return cache statistics (Admin only)."""
    is_admin = request.session.get("admin") == "true"
    if not is_admin:
        return JSONResponse(status_code=403, content={"detail": "Admin authorization required."})
    return {
        "status": "ok",
        "cache": cache_metrics.get_stats(),
    }


@app.post("/api/admin/cache/flush")
def flush_admin_cache(request: Request):
    """Flush in-memory and Redis cache entries (Admin only)."""
    is_admin = request.session.get("admin") == "true"
    if not is_admin:
        return JSONResponse(status_code=403, content={"detail": "Admin authorization required."})
    CacheService.clear()
    cache_metrics.reset()
    return {"status": "ok", "message": "Chart cache flushed successfully."}


@app.get("/api/locales/{lang}")
def get_locale_translations(lang: str):
    """Return JSON translation dictionary for client-side i18n dynamic switching."""
    translations = load_translations(lang)
    return {
        "lang": lang,
        "supported_languages": SUPPORTED_LANGUAGES,
        "translations": translations,
    }


# Set up Template Engine and Static Directory
static_dir = BASE_DIR / "static"
templates_dir = BASE_DIR / "templates"

if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates = Jinja2Templates(directory=str(templates_dir))
app.state.templates = templates

# Security & Session & Language Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LanguageDetectionMiddleware)
app.add_middleware(DefaultDenyAuthMiddleware)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret_key,
    same_site="lax",
    https_only=settings.is_production,
)

# Register All Sub-Routers
app.include_router(auth_router)
app.include_router(kundali_router)
app.include_router(prediction_router)
app.include_router(panchang_router)
app.include_router(horoscope_router)
app.include_router(blog_router)
app.include_router(admin_router)
app.include_router(feedback_router)
app.include_router(narrative_router)
app.include_router(pages_router)


# Global Exception Handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=500,
            content={"detail": "An internal error occurred. Please verify inputs or try again."},
        )
    # Return friendly error on web pages if needed
    return JSONResponse(
        status_code=500,
        content={"detail": "Something went wrong. Please check your request."},
    )
```

---

### b) gateway/middleware/language.py
**Path:** `astro-platform/backend/gateway/middleware/language.py`  
```python
"""Language Detection Middleware for gateway."""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from shared.i18n.translation import SUPPORTED_LANGUAGES


def resolve_request_language(request: Request) -> str:
    """Extract requested language using 5-level detection priority."""
    path = request.url.path.strip("/")
    parts = path.split("/")

    # Level 1: URL path prefix (e.g., /hi/kundali -> 'hi')
    if parts and parts[0] in SUPPORTED_LANGUAGES:
        return parts[0]

    # Level 2: Query parameter (?lang=hi)
    query_lang = request.query_params.get("lang", "").lower().strip()
    if query_lang in SUPPORTED_LANGUAGES:
        return query_lang

    # Level 3: Cookie (lang=hi)
    cookie_lang = request.cookies.get("lang", "").lower().strip()
    if cookie_lang in SUPPORTED_LANGUAGES:
        return cookie_lang

    # Level 4: Accept-Language header
    accept_lang = request.headers.get("accept-language", "")
    if accept_lang:
        for item in accept_lang.split(","):
            raw_lang = item.split(";")[0].strip().lower()
            code = raw_lang.split("-")[0]
            if code in SUPPORTED_LANGUAGES:
                return code

    # Level 5: Default fallback
    return "en"


class LanguageDetectionMiddleware(BaseHTTPMiddleware):
    """Middleware extracting language preference and setting request.state.lang."""

    async def dispatch(self, request: Request, call_next):
        lang = resolve_request_language(request)
        request.state.lang = lang
        response = await call_next(request)

        # Set lang cookie if not explicitly set or mismatched
        if request.cookies.get("lang") != lang:
            response.set_cookie(key="lang", value=lang, max_age=31536000, httponly=False)

        response.headers["Content-Language"] = lang
        return response
```

---

### c) gateway/pages.py
**Path:** `astro-platform/backend/gateway/pages.py`  
```python
"""HTML Page Routes for Gateway App."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from shared.i18n.translation import load_translations

router = APIRouter(tags=["Pages"])


def _render_page(request: Request, template_name: str, context: dict | None = None) -> HTMLResponse:
    templates = request.app.state.templates
    lang = request.cookies.get("lang", "en")
    page_context = {"request": request, "lang": lang, "t": load_translations(lang)}
    if context:
        page_context.update(context)
    return templates.TemplateResponse(template_name, page_context)


@router.get("/", response_class=HTMLResponse)
@router.get("/{lang}/", response_class=HTMLResponse)
def home_page(request: Request, lang: str = "en"):
    return _render_page(request, "index.html")


@router.get("/prediction", response_class=HTMLResponse)
@router.get("/{lang}/prediction", response_class=HTMLResponse)
def prediction_html_page(request: Request, lang: str = "en"):
    return _render_page(request, "prediction.html")


@router.get("/chat", response_class=HTMLResponse)
@router.get("/{lang}/chat", response_class=HTMLResponse)
def chat_html_page(request: Request, lang: str = "en"):
    return _render_page(request, "chat.html")


@router.get("/panchang.html", response_class=HTMLResponse)
@router.get("/panchang", response_class=HTMLResponse)
@router.get("/{lang}/panchang", response_class=HTMLResponse)
def panchang_html_page(request: Request, lang: str = "en"):
    return _render_page(request, "panchang.html")


@router.get("/blogs", response_class=HTMLResponse)
@router.get("/{lang}/blogs", response_class=HTMLResponse)
def blogs_html_page(request: Request, lang: str = "en"):
    return _render_page(request, "blogs.html")


@router.get("/about", response_class=HTMLResponse)
@router.get("/{lang}/about", response_class=HTMLResponse)
def about_html_page(request: Request, lang: str = "en"):
    return _render_page(request, "about.html")


@router.get("/horoscope", response_class=HTMLResponse)
@router.get("/{lang}/horoscope", response_class=HTMLResponse)
def horoscope_html_page(request: Request, lang: str = "en"):
    return _render_page(request, "daily-horoscope.html")


@router.get("/kundali", response_class=HTMLResponse)
@router.get("/{lang}/kundali", response_class=HTMLResponse)
def kundali_html_page(request: Request, lang: str = "en"):
    return _render_page(request, "kundali.html")


@router.get("/blog/{blog_id}", response_class=HTMLResponse)
def blog_detail_html_page(request: Request, blog_id: int):
    return _render_page(request, "blog-detail.html", {"blog_id": blog_id})


@router.get("/admin/login", response_class=HTMLResponse)
def admin_login_html_page(request: Request):
    return _render_page(request, "admin-login.html")


@router.get("/admin/blogs", response_class=HTMLResponse)
def admin_blogs_html_page(request: Request):
    return _render_page(request, "admin-blog.html")
```

---

### d) modules/kundali/engine.py
**Path:** `astro-platform/backend/modules/kundali/engine.py`  
```python
"""Master Kundali Engine assembling Rasi, Navamsa D9, Dasha, Yogas, Doshas, and Scores."""

from datetime import datetime, timedelta
import swisseph as swe

from shared.veda.zodiac import SIGNS_SK, SIGN_LORDS, to_dms
from shared.veda.nakshatra import calculate_nakshatra
from modules.kundali.varga import calculate_navamsa
from shared.veda.strength import planet_strength_label
from modules.kundali.dasha import calculate_mahadasha, generate_antardasha
from shared.veda.yogas import calculate_yogas
from shared.veda.doshas import calculate_doshas

PLANET_LIST = [
    ("Sun", swe.SUN),
    ("Moon", swe.MOON),
    ("Mars", swe.MARS),
    ("Mercury", swe.MERCURY),
    ("Jupiter", swe.JUPITER),
    ("Venus", swe.VENUS),
    ("Saturn", swe.SATURN),
    ("Rahu", swe.TRUE_NODE),
]

TITHI_NAMES = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya",
]

YOGA_NAMES = [
    "Vishkambha", "Preeti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shoola", "Ganda", "Vriddhi",
    "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata",
    "Variyana", "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha",
    "Shukla", "Brahma", "Indra", "Vaidhriti",
]

KARANA_NAMES = ["Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti"]


def calculate_chart_scores(planets: list[dict], lagna_sign: str, houses: dict) -> dict[str, int]:
    """Calculate normalized scores (0-100) across all life areas."""
    pmap = {p.get("name"): p for p in planets}
    KENDRA = {1, 4, 7, 10}
    TRIKONA = {1, 5, 9}
    DUSTHANA = {6, 8, 12}
    lagna_idx = SIGNS_SK.index(lagna_sign) if lagna_sign in SIGNS_SK else 0

    def ps(name: str) -> float:
        p = pmap.get(name)
        if not p:
            return 5.0
        label = p.get("strength", "Neutral")
        b = 10.0 if "Exalted" in label else 8.0 if "Own" in label else 2.0 if "Debilitated" in label else 5.0
        h = p.get("house", 1)
        if isinstance(h, int):
            if h in KENDRA or h in TRIKONA:
                b += 1.0
            elif h in DUSTHANA:
                b -= 1.5
        if p.get("retrograde"):
            b -= 0.5
        return max(1.0, min(10.0, b))

    def lord_of(house_num: int) -> str:
        return SIGN_LORDS.get(SIGNS_SK[(lagna_idx + house_num - 1) % 12], "Mars")

    overall = sum(ps(p) for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"])
    career = ps("Sun") * 1.5 + ps("Saturn") * 1.5 + ps("Mars") + ps(lord_of(10)) * 2.0
    finance = ps("Jupiter") * 2.0 + ps("Venus") * 1.5 + ps(lord_of(2)) * 1.5 + ps(lord_of(11))
    marriage = ps("Venus") * 2.0 + ps("Jupiter") * 1.5 + ps(lord_of(7)) * 2.0 + ps("Moon") * 0.5
    health = ps("Sun") * 1.5 + ps("Mars") * 1.5 + ps(lord_of(1)) * 2.0 + ps(lord_of(6))
    mental = ps("Moon") * 2.5 + ps("Mercury") * 2.0 + ps(lord_of(4)) * 1.5
    ketu_h = pmap.get("Ketu", {}).get("house", 1)
    spirit = ps("Jupiter") * 2.0 + ps(lord_of(9)) * 2.0 + (7.0 if ketu_h in {1, 5, 9, 12} else 5.0)

    def norm(val: float, denom: float) -> int:
        return round(min((val / denom) * 100.0, 100.0))

    return {
        "overall_strength": norm(overall, 70.0),
        "career_score": norm(career, 60.0),
        "finance_score": norm(finance, 60.0),
        "marriage_score": norm(marriage, 60.0),
        "health_score": norm(health, 60.0),
        "mental_score": norm(mental, 60.0),
        "spirituality_score": norm(spirit, 40.0),
    }


def calculate_kundali(year: int, month: int, day: int, hour: int, minute: int, lat: float, lon: float) -> dict:
    """
    Master Kundali engine returning complete Rasi, Navamsa D9, Panchang, Dasha, Yogas, Doshas, and Scores.
    """
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    ist_offset = 5.5
    utc_hours = (hour + minute / 60.0) - ist_offset
    calc_day = day
    if utc_hours < 0:
        utc_hours += 24.0
        calc_day -= 1

    jd = swe.julday(year, month, calc_day, utc_hours)

    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'W', flags)
    lagna_lon = ascmc[0] % 360.0
    lagna_idx = int(lagna_lon / 30.0)
    lagna_sign = SIGNS_SK[lagna_idx]
    lagna_nak, lagna_pada = calculate_nakshatra(lagna_lon)

    houses = {i: [] for i in range(1, 13)}
    houses[1].append("Lagna")
    planet_data = []

    rahu_raw = 0.0

    for name, planet_id in PLANET_LIST:
        data = swe.calc_ut(jd, planet_id, flags)
        raw_lon = data[0][0] % 360.0
        speed = data[0][3]

        if name == "Rahu":
            rahu_raw = raw_lon

        sign_idx = int(raw_lon / 30.0)
        sign_name = SIGNS_SK[sign_idx]
        house_num = ((sign_idx - lagna_idx) % 12) + 1
        nak_name, pada = calculate_nakshatra(raw_lon)
        nav_sign = calculate_navamsa(raw_lon)
        strength = planet_strength_label(name, sign_name)

        houses[house_num].append(name)
        planet_data.append({
            "name": name,
            "sign": sign_name,
            "degree": to_dms(raw_lon % 30.0),
            "degree_decimal": round(raw_lon % 30.0, 4),
            "house": house_num,
            "nakshatra": nak_name,
            "pada": pada,
            "navamsa": nav_sign,
            "strength": strength,
            "retrograde": speed < 0 or name in ("Rahu", "Ketu"),
            "_raw_lon": raw_lon,
        })

    ketu_lon = (rahu_raw + 180.0) % 360.0
    ketu_sign_idx = int(ketu_lon / 30.0)
    ketu_sign = SIGNS_SK[ketu_sign_idx]
    ketu_house = ((ketu_sign_idx - lagna_idx) % 12) + 1
    ketu_nak, ketu_pada = calculate_nakshatra(ketu_lon)

    houses[ketu_house].append("Ketu")
    planet_data.append({
        "name": "Ketu",
        "sign": ketu_sign,
        "degree": to_dms(ketu_lon % 30.0),
        "degree_decimal": round(ketu_lon % 30.0, 4),
        "house": ketu_house,
        "nakshatra": ketu_nak,
        "pada": ketu_pada,
        "navamsa": calculate_navamsa(ketu_lon),
        "strength": planet_strength_label("Ketu", ketu_sign),
        "retrograde": True,
        "_raw_lon": ketu_lon,
    })

    sun_lon = next(p["_raw_lon"] for p in planet_data if p["name"] == "Sun")
    moon_lon = next(p["_raw_lon"] for p in planet_data if p["name"] == "Moon")
    diff = (moon_lon - sun_lon) % 360.0

    tithi_num = int(diff / 12.0) + 1
    tithi_name = TITHI_NAMES[(tithi_num - 1) % 30]
    paksha = "Shukla" if tithi_num <= 15 else "Krishna"
    moon_nak, moon_pada = calculate_nakshatra(moon_lon)
    yoga_name = YOGA_NAMES[int(((sun_lon + moon_lon) % 360.0) / (360.0 / 27.0)) % 27]
    karana_name = KARANA_NAMES[int(diff / 6.0) % 7]
    ayanamsa = swe.get_ayanamsa(jd)

    maha_lord, balance_years = calculate_mahadasha(moon_lon, moon_nak)
    antardasha = generate_antardasha(maha_lord)

    d9_houses = {i: [] for i in range(1, 13)}
    d9_lagna_nav = calculate_navamsa(lagna_lon)
    d9_lagna_idx = SIGNS_SK.index(d9_lagna_nav)
    d9_houses[1].append("Lagna")

    for p in planet_data:
        nav = p.get("navamsa", "")
        if nav in SIGNS_SK:
            nav_idx = SIGNS_SK.index(nav)
            d9_h = ((nav_idx - d9_lagna_idx) % 12) + 1
            d9_houses[d9_h].append(p["name"])

    planets_out = [{k: v for k, v in p.items() if k != "_raw_lon"} for p in planet_data]
    scores = calculate_chart_scores(planet_data, lagna_sign, houses)
    yogas = calculate_yogas(planet_data, lagna_sign, houses)
    doshas = calculate_doshas(planet_data, lagna_sign, houses)

    lagna_deg_in_sign = lagna_lon % 30.0
    is_near_boundary = lagna_deg_in_sign < 2.0 or lagna_deg_in_sign > 28.0
    boundary_warning = (
        f"Lagna (Ascendant) is situated at {round(lagna_deg_in_sign, 2)}° near a sign boundary (0°-2° or 28°-30°). "
        "Chart sensitivity is elevated; verify birth time precision within ±10 minutes for optimal stability."
        if is_near_boundary else "Lagna is comfortably positioned within sign boundaries."
    )

    return {
        "lagna": lagna_sign,
        "lagna_degree": to_dms(lagna_deg_in_sign),
        "lagna_degree_decimal": round(lagna_deg_in_sign, 4),
        "lagna_nakshatra": lagna_nak,
        "lagna_pada": lagna_pada,
        "is_near_boundary": is_near_boundary,
        "boundary_warning": boundary_warning,
        "time_sensitivity_note": "Ascendant degrees shift approximately 1° every 4 minutes. If exact birth time is uncertain, domain score boundaries may vary.",
        "houses": houses,
        "d9_houses": d9_houses,
        "d9_lagna": d9_lagna_nav,
        "planets": planets_out,
        "tithi_number": tithi_num,
        "tithi_name": tithi_name,
        "paksha": paksha,
        "nakshatra": moon_nak,
        "nakshatra_pada": moon_pada,
        "yoga_name": yoga_name,
        "karana_name": karana_name,
        "ayanamsa": round(ayanamsa, 4),
        "jd": round(jd, 6),
        "mahadasha": maha_lord,
        "dasha_balance": f"{balance_years:.1f} years",
        "antardasha": antardasha[0]["lord"] if antardasha else "",
        "antardasha_list": antardasha,
        "scores": scores,
        "yogas": yogas,
        "doshas": doshas,
    }
```

---

### e) modules/kundali/service.py
**Path:** `astro-platform/backend/modules/kundali/api.py`  
> [!IMPORTANT]
> NOTE: In the actual codebase, KundaliService is declared in `modules/kundali/api.py` (lines 29-60). There is no standalone `service.py` in `modules/kundali/`.

```python
"""Kundali generation, Chart calculation, PDF download, and Kundali chat API routes."""

from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
import swisseph as swe

from modules.kundali.schemas import BirthData, KundaliChatRequest, KundaliRequest
from modules.kundali.cities import CITIES, get_city
from modules.kundali.houses import calculate_lagna
from modules.kundali.engine import calculate_kundali
from modules.kundali.planets import calculate_all_planets
try:
    from modules.narrative.chat import chat_service
except ImportError:
    from app.services.ai_engine.chat_service import chat_service

try:
    from workers.pdf_worker import generate_kundali_pdf_buffer
except ImportError:
    from app.services.pdf_service import generate_kundali_pdf_buffer

router = APIRouter(prefix="/api", tags=["Kundali & Charts"])


from shared.cache.decorators import cached_chart


class KundaliService:
    @cached_chart(ttl=2592000)
    def compute_chart(self, req: KundaliRequest) -> dict:
        coords = get_city(req.city)
        if coords is None:
            raise HTTPException(
                status_code=400,
                detail=f"City '{req.city}' not found in database. Please try a nearby major city.",
            )
        lat, lon, tz = coords

        ist_offset = 5.5
        if tz != ist_offset:
            dt_local = datetime(req.year, req.month, req.day, req.hour, req.minute)
            dt_ist = dt_local + timedelta(hours=(ist_offset - tz))
            year, month, day = dt_ist.year, dt_ist.month, dt_ist.day
            hour, minute = dt_ist.hour, dt_ist.minute
        else:
            year, month, day, hour, minute = req.year, req.month, req.day, req.hour, req.minute

        return calculate_kundali(year, month, day, hour, minute, lat, lon)


    def get_chart(self, chart_hash: str) -> dict:
        from modules.kundali.cache import kundali_cache
        return kundali_cache.get(chart_hash) or {}

    def compute_varga(self, chart_hash: str, varga: str) -> dict:
        from modules.kundali.varga import calculate_navamsa
        return {"varga": varga, "chart_hash": chart_hash}


@router.get("/cities")
def get_cities():
    """Return sorted list of all supported city names."""
    return sorted(CITIES.keys())


@router.post("/generate-chart")
def generate_chart_api(data: BirthData):
    """Generate basic planetary degrees and Lagna for chart rendering."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    jd = swe.julday(data.year, data.month, data.day, data.hour)
    planets = calculate_all_planets(jd)

    lagna_degree, lagna_sign = calculate_lagna(jd)

    return {
        "basic_details": {
            "date": f"{data.day:02d}-{data.month:02d}-{data.year}",
            "time": data.hour,
            "lagna": lagna_sign,
            "lagna_degree": round(lagna_degree % 30.0, 2),
        },
        "planets": planets,
    }


kundali_service = KundaliService()


@router.post("/kundali")
def get_kundali(request: Request, data: KundaliRequest):
    """Calculate comprehensive Vedic Kundali with D9, Yogas, Doshas, and Dasha."""
    result = kundali_service.compute_chart(data)
    result["disclaimer"] = (
        "Vedic astrology interpretations represent traditional symbolic frameworks for self-reflection and personal growth. "
        "Outputs are non-binding and do not constitute professional medical, legal, or financial advice."
    )

    request.session["kundali_chart"] = result
    return result



@router.get("/download-kundali")
def download_kundali(request: Request):
    """Generate and return an in-memory PDF report for the session's Kundali."""
    chart = request.session.get("kundali_chart")
    if not chart:
        raise HTTPException(
            status_code=400,
            detail="No Kundali chart found in current session. Please calculate a chart first.",
        )

    pdf_buffer = generate_kundali_pdf_buffer(chart)
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=AstroLogic_Kundali_Report.pdf"},
    )


@router.post("/kundali-chat")
def kundali_chat(data: KundaliChatRequest):
    """Contextual life questions assistant using natal chart positions."""
    return chat_service.answer_kundali_chat(data.message, data.chart)
```

---

### f) modules/kundali/planet_engine.py
**Path:** `astro-platform/backend/modules/kundali/planets.py`  
> [!IMPORTANT]
> NOTE: In the actual codebase, this component is named `modules/kundali/planets.py`.

```python
"""Swiss Ephemeris precision planetary calculations."""

import swisseph as swe

PLANETS_MAP = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.TRUE_NODE,
    "Ketu": swe.TRUE_NODE,
}


def calculate_all_planets(jd: float) -> dict[str, float]:
    """
    Calculate Sidereal (Lahiri) longitudes for all 9 Vedic planets.
    Returns: dict mapping planet name -> longitude degree (0-360).
    """
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    positions = {}
    rahu_lon = 0.0

    for name, code in PLANETS_MAP.items():
        if name == "Ketu":
            continue
        result = swe.calc_ut(jd, code, flags)
        lon = result[0][0] % 360.0
        positions[name] = lon
        if name == "Rahu":
            rahu_lon = lon

    # Ketu is exactly 180 degrees from Rahu
    positions["Ketu"] = (rahu_lon + 180.0) % 360.0

    return positions


def calculate_planets_with_speed(jd: float) -> list[dict]:
    """
    Calculate detailed planetary positions including speed, sign, degree, and retrograde status.
    """
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    planet_list = [
        ("Sun", swe.SUN),
        ("Moon", swe.MOON),
        ("Mars", swe.MARS),
        ("Mercury", swe.MERCURY),
        ("Jupiter", swe.JUPITER),
        ("Venus", swe.VENUS),
        ("Saturn", swe.SATURN),
        ("Rahu", swe.TRUE_NODE),
    ]

    results = []
    rahu_raw = 0.0

    for name, code in planet_list:
        data = swe.calc_ut(jd, code, flags)
        lon = data[0][0] % 360.0
        speed = data[0][3]

        if name == "Rahu":
            rahu_raw = lon

        results.append({
            "name": name,
            "longitude": lon,
            "speed": speed,
            "retrograde": speed < 0 or name in ("Rahu", "Ketu"),
        })

    # Add Ketu
    ketu_lon = (rahu_raw + 180.0) % 360.0
    results.append({
        "name": "Ketu",
        "longitude": ketu_lon,
        "speed": -0.05,
        "retrograde": True,
    })

    return results
```

---

### g) modules/kundali/house_engine.py
**Path:** `astro-platform/backend/modules/kundali/houses.py`  
> [!IMPORTANT]
> NOTE: In the actual codebase, this component is named `modules/kundali/houses.py`.

```python
"""Lagna (Ascendant) and house calculation engine."""

import swisseph as swe
from shared.veda.zodiac import SIGNS_SK, degree_to_sign


def calculate_lagna(jd: float, latitude: float = 18.5204, longitude: float = 73.8567) -> tuple[float, str]:
    """
    Calculate Lagna (Ascendant) longitude and sign name.
    Returns: (lagna_degree_360, lagna_sign_name).
    """
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    cusps, ascmc = swe.houses_ex(
        jd,
        latitude,
        longitude,
        b'W',  # Whole sign
        flags,
    )

    asc_degree = ascmc[0] % 360.0
    sign, _ = degree_to_sign(asc_degree)

    return asc_degree, sign


def assign_house(planet_sign: str, lagna_sign: str) -> int:
    """
    Determine the house number (1-12) of a planet using the Vedic Whole Sign system.
    """
    lagna_index = SIGNS_SK.index(lagna_sign) if lagna_sign in SIGNS_SK else 0
    planet_index = SIGNS_SK.index(planet_sign) if planet_sign in SIGNS_SK else 0

    return ((planet_index - lagna_index) % 12) + 1


def assign_bhava_house(jd: float, latitude: float, longitude: float, planet_longitude: float) -> int:
    """
    Calculate Placidus / Sripati Bhava Chalit house (1-12) for a given planet longitude.
    """
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    cusps, ascmc = swe.houses_ex(
        jd,
        latitude,
        longitude,
        b'P',  # Placidus / Bhava
        flags,
    )

    cusp_list = list(cusps)
    if len(cusp_list) == 13:
        cusp_list = cusp_list[1:]

    if len(cusp_list) != 12:
        return 1

    pl = planet_longitude % 360.0

    for i in range(12):
        start = cusp_list[i] % 360.0
        end = cusp_list[(i + 1) % 12] % 360.0

        if start < end:
            if start <= pl < end:
                return i + 1
        else:  # Wraps around 360/0
            if pl >= start or pl < end:
                return i + 1

    return 1
```

---

### h) modules/kundali/varga_engine.py
**Path:** `astro-platform/backend/modules/kundali/varga.py`  
> [!IMPORTANT]
> NOTE: In the actual codebase, this component is named `modules/kundali/varga.py`.

```python
"""
Divisional Charts (Varga) Engine: Navamsa (D9), Dashamsha (D10), etc.
"""

from collections import defaultdict
from datetime import datetime
import swisseph as swe

from shared.veda.zodiac import SIGNS_SK, SIGN_LORDS, degree_to_sign
from modules.kundali.planets import calculate_all_planets
from modules.kundali.houses import calculate_lagna, assign_house, assign_bhava_house
from shared.veda.nakshatra import calculate_nakshatra
from shared.veda.strength import final_strength, calculate_weighted_strength
from modules.kundali.dasha import calculate_mahadasha, generate_dasha_timeline
from shared.veda.aspects import calculate_vedic_aspects

# 9 Navamsa parts per sign (3°20' each)
NAVAMSA_START = {
    # Fire signs (Mesha, Simha, Dhanu) start from Mesha (0)
    0: 0, 4: 0, 8: 0,
    # Earth signs (Vrishabha, Kanya, Makara) start from Makara (9)
    1: 9, 5: 9, 9: 9,
    # Air signs (Mithuna, Tula, Kumbha) start from Tula (6)
    2: 6, 6: 6, 10: 6,
    # Water signs (Karka, Vrischika, Meena) start from Karka (3)
    3: 3, 7: 3, 11: 3,
}

PADA_DEG = 30.0 / 9.0  # 3.3333333333333335 degrees


def calculate_navamsa(longitude: float) -> str:
    """
    Calculate the D9 Navamsa sign name for a given absolute longitude degree (0-360).
    """
    norm_deg = longitude % 360.0
    sign_idx = int(norm_deg / 30.0)
    deg_in_sign = norm_deg % 30.0

    pada = int(deg_in_sign / PADA_DEG)
    start_sign = NAVAMSA_START[sign_idx]
    nav_idx = (start_sign + pada) % 12

    return SIGNS_SK[nav_idx]


def calculate_navamsa_sign(longitude: float) -> str:
    """Alias for calculate_navamsa."""
    return calculate_navamsa(longitude)


def calculate_house_lords(lagna_sign: str) -> dict[int, str]:
    """Calculate the planetary ruler for each of the 12 houses from Lagna."""
    lagna_idx = SIGNS_SK.index(lagna_sign) if lagna_sign in SIGNS_SK else 0
    lords = {}
    for h in range(1, 13):
        sign = SIGNS_SK[(lagna_idx + h - 1) % 12]
        lords[h] = SIGN_LORDS.get(sign, "Mars")
    return lords


def classify_functional_nature(lagna_sign: str, house_lords: dict[int, str]) -> dict:
    """Classify functional benefics, malefics, and yogakarakas for a given Lagna."""
    benefics = []
    malefics = []
    neutral = []

    for h, lord in house_lords.items():
        if h in (1, 5, 9) and lord not in benefics:
            benefics.append(lord)
        elif h in (6, 8, 12) and lord not in malefics and lord not in benefics:
            malefics.append(lord)
        elif lord not in neutral and lord not in benefics and lord not in malefics:
            neutral.append(lord)

    return {
        "functional_benefics": benefics,
        "functional_malefics": malefics,
        "neutral": neutral,
    }


def calculate_dispositors(chart: dict) -> dict[str, str]:
    """Calculate the sign dispositor (ruler of sign occupied) for each planet."""
    dispositors = {}
    planets_by_house = chart.get("planets_by_house", {})
    for h, p_list in planets_by_house.items():
        for p in p_list:
            name = p.get("planet")
            sign = p.get("sign")
            disp = SIGN_LORDS.get(sign, "Mars")
            dispositors[name] = disp
    return dispositors


def evaluate_event(chart: dict, event_type: str) -> dict:
    """Evaluate overall score, confidence, and level for an event (marriage / career)."""
    weights = chart.get("planet_strength_scores", {})
    if event_type == "marriage":
        v_score = weights.get("Venus", 6.0)
        j_score = weights.get("Jupiter", 6.0)
        raw_score = (v_score * 0.6 + j_score * 0.4) * 10.0
    else:  # career
        s_score = weights.get("Sun", 6.0)
        sat_score = weights.get("Saturn", 6.0)
        m_score = weights.get("Mars", 6.0)
        raw_score = (s_score * 0.4 + sat_score * 0.4 + m_score * 0.2) * 10.0

    score = round(max(30.0, min(95.0, raw_score)), 1)
    if score >= 75:
        level = "Strong"
    elif score >= 55:
        level = "Moderate"
    else:
        level = "Challenging"

    reasons = [
        f"Key karaka planetary strength evaluated at {score}% vitality.",
        f"Active Mahadasha period shaping current karmic cycle.",
    ]

    return {
        "event": event_type,
        "score": score,
        "alignment_strength": 88.0,
        "level": level,
        "reasons": reasons,
    }


def build_event_explanation(chart: dict, event_type: str) -> str:
    """Build a concise, classical interpretation for an event."""
    pred = evaluate_event(chart, event_type)
    lagna = chart.get("basic_details", {}).get("lagna", "Mesha")
    md = chart.get("dasha", {}).get("current_mahadasha", "Jupiter")
    return (
        f"With {lagna} Lagna and {md} Mahadasha currently operating, {event_type} potential is {pred['level']} "
        f"(vitality score: {pred['score']}/100). Focus on favorable astrological windows for optimal success."
    )


def generate_full_chart(year: int, month: int, day: int, hour: float, latitude: float, longitude: float) -> dict:
    """
    Generate comprehensive birth chart for prediction and AI reasoning.
    """
    timezone_offset = 5.5
    utc_hour = hour - timezone_offset
    calc_day = day

    if utc_hour < 0:
        utc_hour += 24.0
        calc_day -= 1

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    jd = swe.julday(year, month, calc_day, utc_hour)

    planet_positions = calculate_all_planets(jd)
    asc_degree, lagna_sign = calculate_lagna(jd, latitude, longitude)
    house_lords = calculate_house_lords(lagna_sign)
    functional_nature = classify_functional_nature(lagna_sign, house_lords)

    house_data = defaultdict(list)
    for planet, degree in planet_positions.items():
        sign, sign_degree = degree_to_sign(degree)
        navamsa_sign = calculate_navamsa(degree)
        strength = final_strength(planet, sign, navamsa_sign)
        rasi_house = assign_house(sign, lagna_sign)
        bhava_house = assign_bhava_house(jd, latitude, longitude, degree)
        nak, pada = calculate_nakshatra(degree)

        house_data[rasi_house].append({
            "planet": planet,
            "degree": round(sign_degree, 2),
            "sign": sign,
            "navamsa": navamsa_sign,
            "nakshatra": nak,
            "pada": pada,
            "bhava_house": bhava_house,
            "strength": strength,
        })

    planets_by_house = dict(house_data)

    moon_longitude = planet_positions.get("Moon", 0.0)
    moon_nak, _ = calculate_nakshatra(moon_longitude)
    dasha_lord, balance = calculate_mahadasha(moon_longitude, moon_nak)
    timeline = generate_dasha_timeline(dasha_lord, balance)

    chart = {
        "basic_details": {
            "date": f"{day:02d}-{month:02d}-{year}",
            "time": hour,
            "lagna": lagna_sign,
        },
        "planets_by_house": planets_by_house,
        "house_lords": house_lords,
        "dasha": {
            "current_mahadasha": dasha_lord,
            "balance_years": round(balance, 2),
            "timeline": timeline,
        },
        "activated_houses": [1, 5, 9, 10],
        "functional_nature": functional_nature,
    }

    chart["dispositors"] = calculate_dispositors(chart)
    chart["vedic_aspects"] = calculate_vedic_aspects(chart)

    try:
        from modules.prediction.transits import calculate_transits
        from shared.veda.yogas import detect_advanced_yogas
        from modules.prediction.timing import evaluate_event_trigger


        today = datetime.today()
        chart["current_transits"] = calculate_transits(chart, today.year, today.month, today.day)
        chart["marriage_timing"] = evaluate_event_trigger(chart, "marriage")
        chart["career_timing"] = evaluate_event_trigger(chart, "career")
        chart["advanced_yogas"] = detect_advanced_yogas(chart)
    except Exception:
        pass

    chart["planet_strength_scores"] = calculate_weighted_strength(chart)
    chart["marriage_prediction"] = evaluate_event(chart, "marriage")
    chart["career_prediction"] = evaluate_event(chart, "career")
    chart["marriage_explanation"] = build_event_explanation(chart, "marriage")
    chart["career_explanation"] = build_event_explanation(chart, "career")

    return chart
```

---

### i) modules/kundali/dasha_engine.py
**Path:** `astro-platform/backend/modules/kundali/dasha.py`  
> [!IMPORTANT]
> NOTE: In the actual codebase, this component is named `modules/kundali/dasha.py`.

```python
"""Vimshottari Dasha calculation engine."""

from datetime import datetime, timedelta
from shared.veda.nakshatra import NAKSHATRAS, NAKSHATRA_SIZE

DASHA_SEQUENCE = [
    "Ketu", "Venus", "Sun", "Moon",
    "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
]

DASHA_YEARS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17
}


def calculate_mahadasha(moon_longitude: float, nak_name: str) -> tuple[str, float]:
    """
    Calculate the starting Mahadasha lord and remaining balance years at birth.
    Returns: (lord_name, balance_years).
    """
    if nak_name in NAKSHATRAS:
        nak_index = NAKSHATRAS.index(nak_name)
    else:
        nak_index = int((moon_longitude % 360.0) / NAKSHATRA_SIZE) % 27

    lord = DASHA_SEQUENCE[nak_index % 9]
    full_years = DASHA_YEARS[lord]

    remainder = (moon_longitude % 360.0) % NAKSHATRA_SIZE
    balance_fraction = (NAKSHATRA_SIZE - remainder) / NAKSHATRA_SIZE
    balance_years = balance_fraction * full_years

    return lord, round(balance_years, 2)


def generate_dasha_timeline(start_lord: str, balance_years: float) -> list[dict]:
    """Generate the full 120-year Vimshottari Mahadasha progression timeline."""
    timeline = []
    current_index = DASHA_SEQUENCE.index(start_lord) if start_lord in DASHA_SEQUENCE else 0

    timeline.append({
        "lord": start_lord,
        "years": round(balance_years, 2)
    })

    total_years = balance_years
    next_index = (current_index + 1) % 9

    while total_years < 120:
        lord = DASHA_SEQUENCE[next_index]
        years = DASHA_YEARS[lord]

        timeline.append({
            "lord": lord,
            "years": years
        })

        total_years += years
        next_index = (next_index + 1) % 9

    return timeline


def generate_antardasha(mahadasha_lord: str) -> list[dict]:
    """Calculate the 9 Antardasha periods for a given Mahadasha lord."""
    antardashas = []
    start_idx = DASHA_SEQUENCE.index(mahadasha_lord) if mahadasha_lord in DASHA_SEQUENCE else 0
    md_years = DASHA_YEARS.get(mahadasha_lord, 10)

    for i in range(9):
        lord = DASHA_SEQUENCE[(start_idx + i) % 9]
        ad_years = (md_years * DASHA_YEARS[lord]) / 120.0
        antardashas.append({
            "lord": lord,
            "years": round(ad_years, 2)
        })

    return antardashas


DASHA_DEPTH = "PD"


def compute_pratyantardasha(md_lord: str, ad_lord: str, ad_start: datetime, ad_end: datetime) -> list[dict]:
    """Calculate the 9 Pratyantardasha (PD) sub-periods within an Antardasha."""
    pds = []
    ad_duration_days = (ad_end - ad_start).total_seconds() / 86400.0
    start_idx = DASHA_SEQUENCE.index(ad_lord) if ad_lord in DASHA_SEQUENCE else 0

    curr_start = ad_start
    for i in range(9):
        pd_lord = DASHA_SEQUENCE[(start_idx + i) % 9]
        pd_duration_days = ad_duration_days * (DASHA_YEARS[pd_lord] / 120.0)
        curr_end = curr_start + timedelta(days=pd_duration_days)

        pds.append({
            "md_lord": md_lord,
            "ad_lord": ad_lord,
            "pd_lord": pd_lord,
            "start": curr_start.strftime("%Y-%m-%d"),
            "end": curr_end.strftime("%Y-%m-%d"),
            "days": round(pd_duration_days, 1),
        })
        curr_start = curr_end

    return pds


def generate_dasha_chain(birth_datetime: datetime, timeline: list[dict], filter_start: str | None = None, filter_end: str | None = None) -> list[dict]:
    """
    Generate nested MD/AD/PD periods for chart forecast within optional filter date range.
    """
    chain = []
    curr_md_start = birth_datetime

    f_start = datetime.strptime(filter_start, "%Y-%m-%d") if filter_start else None
    f_end = datetime.strptime(filter_end, "%Y-%m-%d") if filter_end else None

    for md in timeline:
        md_lord = md["lord"]
        md_duration_days = md["years"] * 365.25
        curr_md_end = curr_md_start + timedelta(days=md_duration_days)

        # Quick boundary prune
        if f_end and curr_md_start > f_end:
            break
        if f_start and curr_md_end < f_start:
            curr_md_start = curr_md_end
            continue

        # Antardashas
        ads = generate_antardasha(md_lord)
        curr_ad_start = curr_md_start
        for ad in ads:
            ad_lord = ad["lord"]
            ad_duration_days = (md_duration_days * DASHA_YEARS[ad_lord]) / 120.0
            curr_ad_end = curr_ad_start + timedelta(days=ad_duration_days)

            if f_end and curr_ad_start > f_end:
                break
            if f_start and curr_ad_end < f_start:
                curr_ad_start = curr_ad_end
                continue

            # Pratyantardashas
            pds = compute_pratyantardasha(md_lord, ad_lord, curr_ad_start, curr_ad_end)
            for pd in pds:
                pd_s = datetime.strptime(pd["start"], "%Y-%m-%d")
                pd_e = datetime.strptime(pd["end"], "%Y-%m-%d")
                if f_start and pd_e < f_start:
                    continue
                if f_end and pd_s > f_end:
                    continue

                chain.append(pd)

            curr_ad_start = curr_ad_end

        curr_md_start = curr_md_end

    return chain
```

---

### j) modules/panchang/engine.py
**Path:** `astro-platform/backend/modules/panchang/engine.py`  
```python
"""
Enterprise-Grade Panchang Engine with Swiss Ephemeris Precision.
Computes:
1. Five Sacred Limbs (Tithi, Nakshatra, Yoga, Karana, Vaar) with exact progress & end times.
2. Astronomical Local Sunrise, Sunset, Sandhya & Moon Times.
3. 16-Period Choghadiya (8 Day + 8 Night) with live status & countdown.
4. 24-Hour Planetary Horas.
5. Inauspicious Periods (Rahu Kaal, Yamaganda, Gulika).
6. Auspicious Windows (Abhijit Muhurta, Brahma Muhurta, Amrit/Shubh Choghadiyas).
7. Disha Shool & Ancient Vedic Remedies.
8. Deterministic Actionable Advice (Do's & Don'ts) & 0-10 Auspiciousness Scoring.
9. Optional Personalization (Tara Bala & Chandra Bala).
"""

from datetime import datetime, date, timedelta, timezone
import math
from typing import Dict, Any, List, Optional
import swisseph as swe

from shared.timezone.tz import resolve_timezone, get_local_now, to_local_iso
from shared.cache.redis_client import CacheService
from modules.kundali.cities import CITIES, get_city, get_city_elevation

from shared.veda.nakshatra import NAKSHATRAS
from shared.veda.zodiac import SIGNS, SIGNS_EN, to_dms
from modules.horoscope.rules.daily import evaluate_daily_rules

TITHI_NAMES = [
    "Shukla Pratipada", "Shukla Dwitiya", "Shukla Tritiya", "Shukla Chaturthi",
    "Shukla Panchami", "Shukla Shashthi", "Shukla Saptami", "Shukla Ashtami",
    "Shukla Navami", "Shukla Dashami", "Shukla Ekadashi", "Shukla Dwadashi",
    "Shukla Trayodashi", "Shukla Chaturdashi", "Purnima",
    "Krishna Pratipada", "Krishna Dwitiya", "Krishna Tritiya", "Krishna Chaturthi",
    "Krishna Panchami", "Krishna Shashthi", "Krishna Saptami", "Krishna Ashtami",
    "Krishna Navami", "Krishna Dashami", "Krishna Ekadashi", "Krishna Dwadashi",
    "Krishna Trayodashi", "Krishna Chaturdashi", "Amavasya"
]

YOGA_NAMES = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shula", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
    "Asiddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
    "Indra", "Vaidhriti"
]

KARANA_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitila", "Gara",
    "Vanija", "Vishti (Bhadra)", "Shakuni", "Chatushpada",
    "Naga", "Kimstughna"
]

CHOGHADIYA_ORDER = ["Udveg", "Char", "Labh", "Amrit", "Kaal", "Shubh", "Rog"]
DAY_CHOGHADIYA_START = {
    0: 0, 1: 3, 2: 6, 3: 2, 4: 5, 5: 1, 6: 4
}
NIGHT_CHOGHADIYA_START = {
    0: 5, 1: 1, 2: 4, 3: 0, 4: 3, 5: 6, 6: 2
}

CHOGHADIYA_INFO = {
    "Amrit": {"is_good": True, "planet": "Moon", "label": "Auspicious (Nectar)"},
    "Shubh": {"is_good": True, "planet": "Jupiter", "label": "Auspicious (Good)"},
    "Labh": {"is_good": True, "planet": "Mercury", "label": "Auspicious (Gain)"},
    "Char": {"is_good": True, "planet": "Venus", "label": "Neutral / Mobile"},
    "Rog": {"is_good": False, "planet": "Mars", "label": "Inauspicious (Disease)"},
    "Kaal": {"is_good": False, "planet": "Saturn", "label": "Inauspicious (Loss)"},
    "Udveg": {"is_good": False, "planet": "Sun", "label": "Inauspicious (Anxiety)"}
}

CHALDEAN_HORAS = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
WEEKDAY_HORA_START = {
    0: "Sun", 1: "Moon", 2: "Mars", 3: "Mercury", 4: "Jupiter", 5: "Venus", 6: "Saturn"
}


def _fmt_time_ampm(dt: datetime) -> str:
    return dt.strftime("%I:%M %p")


def _minutes_between(start_dt: datetime, end_dt: datetime) -> float:
    return (end_dt - start_dt).total_seconds() / 60.0


def calculate_choghadiya_list(
    start_dt: datetime,
    end_dt: datetime,
    start_idx: int
) -> List[Dict[str, Any]]:
    total_seconds = (end_dt - start_dt).total_seconds()
    segment_duration = total_seconds / 8.0
    segments = []

    for i in range(8):
        name = CHOGHADIYA_ORDER[(start_idx + i) % 7]
        seg_start = start_dt + timedelta(seconds=i * segment_duration)
        seg_end = start_dt + timedelta(seconds=(i + 1) * segment_duration)
        info = CHOGHADIYA_INFO.get(name, {"is_good": False, "planet": "Sun", "label": name})

        segments.append({
            "name": name,
            "label": info["label"],
            "is_auspicious": info["is_good"],
            "ruling_planet": info["planet"],
            "start": _fmt_time_ampm(seg_start),
            "end": _fmt_time_ampm(seg_end),
            "start_iso": seg_start.isoformat(),
            "end_iso": seg_end.isoformat(),
            "start_dt": seg_start,
            "end_dt": seg_end
        })
    return segments


def calculate_horas_list(
    sunrise_dt: datetime,
    weekday_idx: int
) -> List[Dict[str, Any]]:
    start_planet = WEEKDAY_HORA_START[weekday_idx % 7]
    ch_idx = CHALDEAN_HORAS.index(start_planet)
    horas = []

    for i in range(24):
        h_start = sunrise_dt + timedelta(hours=i)
        h_end = sunrise_dt + timedelta(hours=i + 1)
        planet = CHALDEAN_HORAS[(ch_idx + i) % 7]

        horas.append({
            "hour_number": i + 1,
            "planet": planet,
            "start": _fmt_time_ampm(h_start),
            "end": _fmt_time_ampm(h_end),
            "start_iso": h_start.isoformat(),
            "end_iso": h_end.isoformat(),
            "start_dt": h_start,
            "end_dt": h_end
        })
    return horas


def get_full_panchang(
    city_name: str = "Pune",
    target_date: Optional[date] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    elevation: Optional[float] = None,
    tz_str: Optional[str] = None,
    user_rashi: Optional[str] = None,
    user_nakshatra: Optional[str] = None
) -> Dict[str, Any]:
    city_info = get_city(city_name)
    if city_info:
        default_lat, default_lon, _ = city_info
    else:
        default_lat, default_lon = 18.5204, 73.8567

    resolved_lat = lat if lat is not None else default_lat
    resolved_lon = lon if lon is not None else default_lon
    resolved_elevation = elevation if elevation is not None else get_city_elevation(name=city_name, lat=resolved_lat, lon=resolved_lon)
    tz_obj, resolved_tz_name = resolve_timezone(lat=resolved_lat, lon=resolved_lon, tz_str=tz_str)

    now_local = get_local_now(tz_obj)
    d = target_date if target_date else now_local.date()
    date_str = d.strftime("%Y-%m-%d")

    cache_key = CacheService.get_panchang_key(f"{date_str}_{resolved_elevation}", resolved_lat, resolved_lon)
    base_data = CacheService.get(cache_key)

    if not base_data or "sunrise_iso" not in base_data:
        base_data = _compute_astronomical_base(d, resolved_lat, resolved_lon, resolved_elevation, tz_obj, city_name)
        CacheService.set(cache_key, base_data, ttl=86400)

    res = _build_dynamic_panchang_response(
        base_data=base_data,
        now_local=now_local,
        resolved_tz_name=resolved_tz_name,
        tz_obj=tz_obj,
        user_rashi=user_rashi,
        user_nakshatra=user_nakshatra
    )
    return res


def _compute_astronomical_base(
    d: date,
    lat: float,
    lon: float,
    elevation: float,
    tz_obj: Any,
    city_display_name: str
) -> Dict[str, Any]:
    jd_noon = swe.julday(d.year, d.month, d.day, 12.0)

    def _jd_to_dt(jd_val: float) -> datetime:
        y, m, d_int, ut_h_float = swe.revjul(jd_val)
        h = int(ut_h_float)
        m_f = (ut_h_float - h) * 60.0
        minute = int(m_f)
        sec_f = (m_f - minute) * 60.0
        sec = min(int(sec_f), 59)
        dt_utc = datetime(y, m, d_int, h, minute, sec, tzinfo=timezone.utc)
        return dt_utc.astimezone(tz_obj)

    try:
        jd_midnight = swe.julday(d.year, d.month, d.day, 0.0)
        res_rise = swe.rise_trans(jd_midnight, swe.SUN, swe.CALC_RISE, (lon, lat, elevation), 0.0, 0.0)
        res_set = swe.rise_trans(jd_midnight, swe.SUN, swe.CALC_SET, (lon, lat, elevation), 0.0, 0.0)
        jd_rise = res_rise[1][0]
        jd_set = res_set[1][0]

        res_next_rise = swe.rise_trans(jd_midnight + 1.0, swe.SUN, swe.CALC_RISE, (lon, lat, elevation), 0.0, 0.0)
        jd_next_rise = res_next_rise[1][0]

        sunrise_dt = _jd_to_dt(jd_rise)
        sunset_dt = _jd_to_dt(jd_set)
        next_sunrise_dt = _jd_to_dt(jd_next_rise)
    except Exception:
        sunrise_dt = datetime(d.year, d.month, d.day, 6, 0, 0, tzinfo=tz_obj)
        sunset_dt = datetime(d.year, d.month, d.day, 18, 30, 0, tzinfo=tz_obj)
        next_sunrise_dt = sunrise_dt + timedelta(days=1)
        jd_rise = swe.julday(d.year, d.month, d.day, 6.0 - (lon / 15.0))

    sunrise_str = _fmt_time_ampm(sunrise_dt)
    sunset_str = _fmt_time_ampm(sunset_dt)

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    anchor_jd = jd_rise
    sun_res, _ = swe.calc_ut(anchor_jd, swe.SUN, swe.FLG_SWIEPH | swe.FLG_SPEED)
    moon_res, _ = swe.calc_ut(anchor_jd, swe.MOON, swe.FLG_SWIEPH | swe.FLG_SPEED)
    ayanamsa = swe.get_ayanamsa_ut(anchor_jd)

    sun_sid = (sun_res[0] - ayanamsa) % 360.0
    moon_sid = (moon_res[0] - ayanamsa) % 360.0
    sun_speed = sun_res[3]
    moon_speed = moon_res[3]
    rel_speed = moon_speed - sun_speed if (moon_speed - sun_speed) > 0 else 12.19

    tithi_diff = (moon_sid - sun_sid) % 360.0
    tithi_num = int(tithi_diff / 12.0) + 1
    tithi_name = TITHI_NAMES[(tithi_num - 1) % 30]
    paksha = "Shukla" if tithi_num <= 15 else "Krishna"
    tithi_deg_in = tithi_diff % 12.0
    tithi_progress = round((tithi_deg_in / 12.0) * 100.0, 1)

    target_tithi_diff = (tithi_num * 12.0) % 360.0
    tithi_approx_days = (12.0 - tithi_deg_in) / rel_speed
    low_jd = anchor_jd + tithi_approx_days - 0.25
    high_jd = anchor_jd + tithi_approx_days + 0.25
    for _ in range(22):
        mid_jd = (low_jd + high_jd) / 2.0
        s_res, _ = swe.calc_ut(mid_jd, swe.SUN, swe.FLG_SWIEPH)
        m_res, _ = swe.calc_ut(mid_jd, swe.MOON, swe.FLG_SWIEPH)
        ay = swe.get_ayanamsa_ut(mid_jd)
        diff = ((m_res[0] - ay) - (s_res[0] - ay)) % 360.0
        err = diff - target_tithi_diff
        if err > 180.0:
            err -= 360.0
        elif err < -180.0:
            err += 360.0
        if err < 0:
            low_jd = mid_jd
        else:
            high_jd = mid_jd
    tithi_end_dt = _jd_to_dt((low_jd + high_jd) / 2.0)
    tithi_end_str = _fmt_time_ampm(tithi_end_dt)

    nak_deg = 360.0 / 27.0
    nak_num = int(moon_sid / nak_deg) + 1
    nak_idx = (nak_num - 1) % 27
    nak_name = NAKSHATRAS[nak_idx]
    nak_deg_in = moon_sid % nak_deg
    nak_pada = int(nak_deg_in / (nak_deg / 4.0)) + 1

    target_nak_deg = (nak_num * nak_deg) % 360.0
    nak_approx_days = (nak_deg - nak_deg_in) / (moon_speed if moon_speed > 0 else 13.176)
    low_jd = anchor_jd + nak_approx_days - 0.25
    high_jd = anchor_jd + nak_approx_days + 0.25
    for _ in range(22):
        mid_jd = (low_jd + high_jd) / 2.0
        m_res, _ = swe.calc_ut(mid_jd, swe.MOON, swe.FLG_SWIEPH)
        ay = swe.get_ayanamsa_ut(mid_jd)
        moon_pos = (m_res[0] - ay) % 360.0
        err = moon_pos - target_nak_deg
        if err > 180.0:
            err -= 360.0
        elif err < -180.0:
            err += 360.0
        if err < 0:
            low_jd = mid_jd
        else:
            high_jd = mid_jd
    nak_end_dt = _jd_to_dt((low_jd + high_jd) / 2.0)
    nak_end_str = _fmt_time_ampm(nak_end_dt)

    yoga_sum = (sun_sid + moon_sid) % 360.0
    yoga_deg = 360.0 / 27.0
    yoga_num = int(yoga_sum / yoga_deg) + 1
    yoga_idx = (yoga_num - 1) % 27
    yoga_name = YOGA_NAMES[yoga_idx]
    comb_speed = moon_speed + sun_speed

    target_yoga_deg = (yoga_num * yoga_deg) % 360.0
    yoga_deg_in = yoga_sum % yoga_deg
    yoga_approx_days = (yoga_deg - yoga_deg_in) / (comb_speed if comb_speed > 0 else 14.17)
    low_jd = anchor_jd + yoga_approx_days - 0.25
    high_jd = anchor_jd + yoga_approx_days + 0.25
    for _ in range(22):
        mid_jd = (low_jd + high_jd) / 2.0
        s_res, _ = swe.calc_ut(mid_jd, swe.SUN, swe.FLG_SWIEPH)
        m_res, _ = swe.calc_ut(mid_jd, swe.MOON, swe.FLG_SWIEPH)
        ay = swe.get_ayanamsa_ut(mid_jd)
        curr_sum = ((s_res[0] - ay) + (m_res[0] - ay)) % 360.0
        err = curr_sum - target_yoga_deg
        if err > 180.0:
            err -= 360.0
        elif err < -180.0:
            err += 360.0
        if err < 0:
            low_jd = mid_jd
        else:
            high_jd = mid_jd
    yoga_end_dt = _jd_to_dt((low_jd + high_jd) / 2.0)
    yoga_end_str = _fmt_time_ampm(yoga_end_dt)

    half_tithi = int(tithi_diff / 6.0)
    if half_tithi == 0:
        karana_name = "Kimstughna"
    elif half_tithi >= 57:
        karana_name = ["Shakuni", "Chatushpada", "Naga"][half_tithi - 57]
    else:
        karana_name = KARANA_NAMES[(half_tithi - 1) % 7]

    target_karana_deg = ((half_tithi + 1) * 6.0) % 360.0
    karana_approx_days = (6.0 - (tithi_diff % 6.0)) / rel_speed
    low_jd = anchor_jd + karana_approx_days - 0.25
    high_jd = anchor_jd + karana_approx_days + 0.25
    for _ in range(22):
        mid_jd = (low_jd + high_jd) / 2.0
        s_res, _ = swe.calc_ut(mid_jd, swe.SUN, swe.FLG_SWIEPH)
        m_res, _ = swe.calc_ut(mid_jd, swe.MOON, swe.FLG_SWIEPH)
        ay = swe.get_ayanamsa_ut(mid_jd)
        diff = ((m_res[0] - ay) - (s_res[0] - ay)) % 360.0
        err = diff - target_karana_deg
        if err > 180.0:
            err -= 360.0
        elif err < -180.0:
            err += 360.0
        if err < 0:
            low_jd = mid_jd
        else:
            high_jd = mid_jd
    karana_end_dt = _jd_to_dt((low_jd + high_jd) / 2.0)
    karana_end_str = _fmt_time_ampm(karana_end_dt)

    day_len_mins = _minutes_between(sunrise_dt, sunset_dt)
    part_mins = day_len_mins / 8.0

    v_wd = (d.weekday() + 1) % 7
    rahu_parts = {0: 7, 1: 1, 2: 6, 3: 4, 4: 5, 5: 3, 6: 2}
    yama_parts = {0: 4, 1: 3, 2: 2, 3: 1, 4: 0, 5: 6, 6: 5}
    guli_parts = {0: 6, 1: 5, 2: 4, 3: 3, 4: 2, 5: 1, 6: 0}

    def _calc_window(part_idx: int) -> Dict[str, Any]:
        s = sunrise_dt + timedelta(minutes=part_idx * part_mins)
        e = s + timedelta(minutes=part_mins)
        return {
            "start": _fmt_time_ampm(s),
            "end": _fmt_time_ampm(e),
            "start_iso": s.isoformat(),
            "end_iso": e.isoformat(),
            "start_dt_str": s.strftime("%Y-%m-%d %H:%M:%S"),
            "end_dt_str": e.strftime("%Y-%m-%d %H:%M:%S")
        }

    rahu_win = _calc_window(rahu_parts[v_wd])
    yama_win = _calc_window(yama_parts[v_wd])
    guli_win = _calc_window(guli_parts[v_wd])

    muhurta_len = day_len_mins / 15.0
    abhijit_start = sunrise_dt + timedelta(minutes=7 * muhurta_len)
    abhijit_end = sunrise_dt + timedelta(minutes=8 * muhurta_len)
    brahma_start = sunrise_dt - timedelta(minutes=96)
    brahma_end = sunrise_dt - timedelta(minutes=48)

    abhijit_win = {
        "start": _fmt_time_ampm(abhijit_start),
        "end": _fmt_time_ampm(abhijit_end),
        "start_iso": abhijit_start.isoformat(),
        "end_iso": abhijit_end.isoformat(),
        "start_dt_str": abhijit_start.strftime("%Y-%m-%d %H:%M:%S"),
        "end_dt_str": abhijit_end.strftime("%Y-%m-%d %H:%M:%S")
    }
    brahma_win = {
        "start": _fmt_time_ampm(brahma_start),
        "end": _fmt_time_ampm(brahma_end),
        "start_iso": brahma_start.isoformat(),
        "end_iso": brahma_end.isoformat()
    }

    planet_constants = [
        ("Sun", "Surya", swe.SUN),
        ("Moon", "Chandra", swe.MOON),
        ("Mars", "Mangal", swe.MARS),
        ("Mercury", "Budha", swe.MERCURY),
        ("Jupiter", "Guru", swe.JUPITER),
        ("Venus", "Shukra", swe.VENUS),
        ("Saturn", "Shani", swe.SATURN),
        ("Rahu", "Rahu", swe.TRUE_NODE),
    ]

    planets_out = []
    for en_name, sk_name, pid in planet_constants:
        pres, _ = swe.calc_ut(jd_noon, pid, swe.FLG_SWIEPH | swe.FLG_SPEED)
        p_sid = (pres[0] - ayanamsa) % 360.0
        p_sign_idx = int(p_sid / 30.0) % 12
        p_deg_in_sign = p_sid % 30.0
        p_nak_idx = int(p_sid / (360.0 / 27.0)) % 27
        p_retro = pres[3] < 0 if pid != swe.TRUE_NODE else True

        planets_out.append({
            "name": f"{sk_name} ({en_name})",
            "en_name": en_name,
            "sign": f"{SIGNS[p_sign_idx]} ({SIGNS_EN[p_sign_idx]})",
            "degree": to_dms(p_deg_in_sign),
            "nakshatra": NAKSHATRAS[p_nak_idx],
            "retrograde": bool(p_retro)
        })

    rahu_obj = planets_out[-1]
    r_res, _ = swe.calc_ut(jd_noon, swe.TRUE_NODE, swe.FLG_SWIEPH)
    k_sid = ((r_res[0] - ayanamsa) + 180.0) % 360.0
    k_sign_idx = int(k_sid / 30.0) % 12
    k_nak_idx = int(k_sid / (360.0 / 27.0)) % 27

    planets_out.append({
        "name": "Ketu (Ketu)",
        "en_name": "Ketu",
        "sign": f"{SIGNS[k_sign_idx]} ({SIGNS_EN[k_sign_idx]})",
        "degree": to_dms(k_sid % 30.0),
        "nakshatra": NAKSHATRAS[k_nak_idx],
        "retrograde": True
    })

    return {
        "date_str": d.strftime("%Y-%m-%d"),
        "city": city_display_name,
        "lat": lat,
        "lon": lon,
        "weekday_idx": v_wd,
        "tithi": tithi_name,
        "tithi_name": tithi_name,
        "paksha": paksha,
        "tithi_progress": tithi_progress,
        "tithi_end": tithi_end_str,
        "nakshatra": nak_name,
        "nakshatra_pada": nak_pada,
        "nakshatra_end": nak_end_str,
        "yoga": yoga_name,
        "yoga_name": yoga_name,
        "yoga_end": yoga_end_str,
        "karana": karana_name,
        "karana_name": karana_name,
        "karana_end": karana_end_str,
        "sunrise": sunrise_str,
        "sunset": sunset_str,
        "sunrise_iso": sunrise_dt.isoformat(),
        "sunset_iso": sunset_dt.isoformat(),
        "next_sunrise_iso": next_sunrise_dt.isoformat(),
        "rahu": f"{rahu_win['start']} - {rahu_win['end']}",
        "rahu_kaal": f"{rahu_win['start']} - {rahu_win['end']}",
        "rahu_window": rahu_win,
        "yamaganda": f"{yama_win['start']} - {yama_win['end']}",
        "yamaganda_window": yama_win,
        "gulika": f"{guli_win['start']} - {guli_win['end']}",
        "gulika_kaal": f"{guli_win['start']} - {guli_win['end']}",
        "gulika_window": guli_win,
        "abhijit": f"{abhijit_win['start']} - {abhijit_win['end']}",
        "abhijit_muhurta": f"{abhijit_win['start']} - {abhijit_win['end']}",
        "abhijit_window": abhijit_win,
        "brahma": f"{brahma_win['start']} - {brahma_win['end']}",
        "brahma_window": brahma_win,
        "vara": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"][v_wd],
        "date": d.strftime("%Y-%m-%d"),
        "planets": planets_out,
        "samvat": {
            "vikram_samvat": d.year + 57,
            "shaka_samvat": d.year - 78,
            "month_amanta": "Chaitra"
        }
    }


def _build_dynamic_panchang_response(
    base_data: Dict[str, Any],
    now_local: datetime,
    resolved_tz_name: str,
    tz_obj: Any,
    user_rashi: Optional[str] = None,
    user_nakshatra: Optional[str] = None
) -> Dict[str, Any]:
    sunrise_dt = datetime.fromisoformat(base_data["sunrise_iso"]).astimezone(tz_obj)
    sunset_dt = datetime.fromisoformat(base_data["sunset_iso"]).astimezone(tz_obj)
    next_sunrise_dt = datetime.fromisoformat(base_data["next_sunrise_iso"]).astimezone(tz_obj)
    v_wd = base_data["weekday_idx"]

    chog_day = calculate_choghadiya_list(sunrise_dt, sunset_dt, DAY_CHOGHADIYA_START[v_wd])
    chog_night = calculate_choghadiya_list(sunset_dt, next_sunrise_dt, NIGHT_CHOGHADIYA_START[v_wd])

    all_chogs = chog_day + chog_night
    current_chog = None
    for c in all_chogs:
        if c["start_dt"] <= now_local < c["end_dt"]:
            current_chog = c
            break
    if not current_chog:
        current_chog = all_chogs[0]

    rem_secs = max(0, int((current_chog["end_dt"] - now_local).total_seconds()))
    rem_mins = rem_secs // 60
    current_chog_clean = {
        "name": current_chog["name"],
        "label": current_chog["label"],
        "is_auspicious": current_chog["is_auspicious"],
        "ruling_planet": current_chog["ruling_planet"],
        "start": current_chog["start"],
        "end": current_chog["end"],
        "time_remaining_mins": rem_mins,
        "time_remaining_str": f"{rem_mins}m {rem_secs % 60}s"
    }

    horas = calculate_horas_list(sunrise_dt, v_wd)
    current_hora = None
    for h in horas:
        if h["start_dt"] <= now_local < h["end_dt"]:
            current_hora = h
            break
    if not current_hora:
        current_hora = horas[0]

    current_hora_clean = {
        "hour_number": current_hora["hour_number"],
        "planet": current_hora["planet"],
        "start": current_hora["start"],
        "end": current_hora["end"]
    }

    def _is_active(win_dict: Dict[str, Any]) -> bool:
        try:
            s = datetime.fromisoformat(win_dict["start_iso"]).astimezone(tz_obj)
            e = datetime.fromisoformat(win_dict["end_iso"]).astimezone(tz_obj)
            return s <= now_local < e
        except Exception:
            return False

    is_rahu = _is_active(base_data["rahu_window"])
    is_yama = _is_active(base_data["yamaganda_window"])
    is_guli = _is_active(base_data["gulika_window"])

    rule_output = evaluate_daily_rules(
        tithi_name=base_data["tithi"],
        nakshatra_name=base_data["nakshatra"],
        yoga_name=base_data["yoga"],
        karana_name=base_data["karana"],
        weekday_idx=v_wd,
        current_choghadiya=current_chog_clean,
        current_hora=current_hora_clean,
        is_in_rahu_kaal=is_rahu,
        is_in_yamaganda=is_yama,
        is_in_gulika=is_guli,
        has_abhijit=True
    )

    next_auspicious = None
    for c in all_chogs:
        if c["start_dt"] > now_local and c["is_auspicious"]:
            mins_until = int((c["start_dt"] - now_local).total_seconds() / 60.0)
            next_auspicious = {
                "name": f"{c['name']} Choghadiya",
                "start": c["start"],
                "end": c["end"],
                "time_until_start": f"{mins_until} mins",
                "category": "Auspicious Choghadiya"
            }
            break

    if not next_auspicious:
        next_auspicious = {
            "name": "Abhijit Muhurat",
            "start": base_data["abhijit_window"]["start"],
            "end": base_data["abhijit_window"]["end"],
            "time_until_start": "Midday",
            "category": "Daily Divine Window"
        }

    def _clean_chog_list(lst: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [{
            "name": x["name"],
            "label": x["label"],
            "is_auspicious": x["is_auspicious"],
            "ruling_planet": x["ruling_planet"],
            "start": x["start"],
            "end": x["end"]
        } for x in lst]

    def _clean_hora_list(lst: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [{
            "hour_number": x["hour_number"],
            "planet": x["planet"],
            "start": x["start"],
            "end": x["end"]
        } for x in lst]

    full_resp = dict(base_data)
    full_resp.update({
        "resolved_timezone": resolved_tz_name,
        "local_datetime": to_local_iso(now_local, tz_obj),
        "mode": "general",
        "today_score": rule_output["today_score"],
        "rule_alignment_score": rule_output.get("rule_alignment_score", 0.96),
        "confidence_score": rule_output.get("rule_alignment_score", rule_output.get("confidence_score", 0.96)),
        "current_period_summary": rule_output["current_period_summary"],
        "next_auspicious_window": next_auspicious,
        "disha_shool": rule_output["disha_shool"],
        "dos_and_donts": {
            "recommended": rule_output["recommended"],
            "avoid": rule_output["avoid"]
        },
        "choghadiya_day": _clean_chog_list(chog_day),
        "choghadiya_night": _clean_chog_list(chog_night),
        "current_choghadiya": current_chog_clean,
        "horas": _clean_hora_list(horas),
        "current_hora": current_hora_clean
    })

    if user_rashi or user_nakshatra:
        from modules.panchang.personalization import (
            calculate_tara_bala,
            calculate_chandra_bala,
            calculate_category_scores
        )

        transit_nak = base_data.get("nakshatra", "Pushya")
        transit_rashi = "Mesha"
        for p in base_data.get("planets", []):
            if "Moon" in p.get("name", "") or "Chandra" in p.get("name", ""):
                transit_rashi = p.get("sign", "Mesha").split("(")[0].strip()
                break

        tara = calculate_tara_bala(user_nakshatra or "Ashwini", transit_nak) if user_nakshatra else None
        chandra = calculate_chandra_bala(user_rashi or "Mesha", transit_rashi) if user_rashi else None

        category_scores = calculate_category_scores(
            tara_bala=tara or {"score_mod": 0, "tara_name": "Sadhana"},
            chandra_bala=chandra or {"score_mod": 0, "house_distance": 1},
            today_base_score=rule_output["today_score"],
            active_hora_planet=current_hora_clean.get("planet", "Sun"),
            active_chog_auspicious=current_chog_clean.get("is_auspicious", True)
        )

        personal_score_mod = (
            (tara["score_mod"] if tara else 0) * 0.4 +
            (chandra["score_mod"] if chandra else 0) * 0.4
        )
        personalized_score = round(max(1.0, min(10.0, rule_output["today_score"] + personal_score_mod)), 1)

        personal_advice = []
        if tara and tara["is_auspicious"]:
            personal_advice.append({
                "type": "positive",
                "text": tara["advice"],
                "source": f"Tara Bala: {tara['tara_name']} ({tara['category']})"
            })
        elif tara:
            personal_advice.append({
                "type": "caution",
                "text": tara["advice"],
                "source": f"Tara Bala: {tara['tara_name']} ({tara['category']})"
            })

        if chandra and chandra["is_auspicious"]:
            personal_advice.append({
                "type": "positive",
                "text": f"Moon transit in your {chandra['house_distance']}th house: {chandra['status']}.",
                "source": "Chandra Bala"
            })
        elif chandra:
            personal_advice.append({
                "type": "caution",
                "text": f"Moon transit in your {chandra['house_distance']}th house: {chandra['status']}. {chandra['desc'].split('—')[-1].strip() if '—' in chandra['desc'] else ''}",
                "source": "Chandra Bala"
            })

        full_resp["mode"] = "personalized"
        full_resp["personalization"] = {
            "tara_bala": tara,
            "chandra_bala": chandra,
            "category_scores": category_scores,
            "personalized_score": personalized_score,
            "personalized_advice": personal_advice
        }
        full_resp["today_score"] = personalized_score
        full_resp["rule_alignment_score"] = 0.94
        full_resp["confidence_score"] = 0.94

    return full_resp


calculate_panchang_for_datetime = get_full_panchang
```

---

### k) modules/panchang/festival.py
**Path:** `astro-platform/backend/modules/panchang/festival.py`  
```python
"""Live Hindu Festival Engine computed from Swiss Ephemeris lunar & solar data with astronomical precision."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import swisseph as swe

MONTH_NAMES = [
    "", "Chaitra", "Vaisakha", "Jyeshtha", "Ashadha", "Shravana",
    "Bhadrapada", "Ashwina", "Kartika", "Margashirsha", "Pausha", "Magha", "Phalguna"
]

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
    "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

TITHI_NAMES = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi",
    "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi",
    "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi",
    "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi",
    "Trayodashi", "Chaturdashi", "Amavasya"
]

ANNUAL_FESTIVALS: List[Dict[str, Any]] = [
    {"month_lunar": 1, "paksha": "Shukla", "tithi_in_paksha": 1, "name": "Gudi Padwa / Ugadi / Chaitra Navratri Begins", "tag": "major", "icon": "🚩", "desc": "Vedic New Year and invocation of Divine Mother Durga.", "remedies": "Erect Gudi / Neem-Jaggery prasad, invoke blessings of Maa Durga."},
    {"month_lunar": 1, "paksha": "Shukla", "tithi_in_paksha": 9, "name": "Rama Navami", "tag": "major", "icon": "🏹", "desc": "Divine birth celebration of Maryada Purushottam Lord Rama.", "remedies": "Chant Shri Rama Raksha Stotra, perform Rama Archana at midday."},
    {"month_lunar": 1, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Kamada Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Sacred Ekadashi for fulfillment of righteous desires.", "remedies": "Observe Ekadashi fast, offer Tulsi leaves to Lord Vishnu."},
    {"month_lunar": 1, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Hanuman Jayanti (Chaitra Purnima)", "tag": "major", "icon": "🐒", "desc": "Birth of Lord Hanuman, embodiment of courage, strength, and devotion.", "remedies": "Recite Hanuman Chalisa 7 times and offer sindoor with jasmine oil."},
    {"month_lunar": 1, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Varuthini Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Virtuous Ekadashi removing past negative karmas.", "remedies": "Fast dedicated to Lord Vamana avatar."},
    {"month_lunar": 2, "paksha": "Shukla", "tithi_in_paksha": 3, "name": "Akshaya Tritiya (Parashurama Jayanti)", "tag": "major", "icon": "✨", "desc": "Day of eternal auspiciousness, unending prosperity, and noble charity.", "remedies": "Gold/silver purchase, donation of water and food grains."},
    {"month_lunar": 2, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Mohini Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi commemorating Lord Vishnu enchantress Mohini form.", "remedies": "Fast for purification of consciousness."},
    {"month_lunar": 2, "paksha": "Shukla", "tithi_in_paksha": 14, "name": "Narasimha Jayanti", "tag": "vrat", "icon": "🦁", "desc": "Sunset advent of Lord Narasimha protecting devotee Prahlada.", "remedies": "Sunset meditation and prayer for fearlessness."},
    {"month_lunar": 2, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Buddha Purnima (Vaisakha Purnima)", "tag": "purnima", "icon": "🌕", "desc": "Celebration of Lord Buddha enlightenment and compassion.", "remedies": "Satyanarayan puja and distribution of food to the needy."},
    {"month_lunar": 2, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Apara Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi granting boundless spiritual merit.", "remedies": "Vishnu worship with sacred yellow flowers."},
    {"month_lunar": 3, "paksha": "Shukla", "tithi_in_paksha": 10, "name": "Ganga Dussehra", "tag": "vrat", "icon": "🌊", "desc": "Descent of holy river Ganga upon Earth.", "remedies": "Holy dip in holy rivers or offer Ganga jal at home."},
    {"month_lunar": 3, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Nirjala Ekadashi", "tag": "major", "icon": "💧", "desc": "Most sacred Ekadashi observed with waterless fast.", "remedies": "Donate water pitchers, hand fans, and summer fruits."},
    {"month_lunar": 3, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Vat Purnima (Jyeshtha Purnima)", "tag": "vrat", "icon": "🌳", "desc": "Worship of sacred Banyan tree for spouse longevity and family harmony.", "remedies": "Tie sacred white/yellow thread around Banyan tree."},
    {"month_lunar": 3, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Yogini Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Fast for physical well-being and purification.", "remedies": "Fast dedicated to Lord Narayana."},
    {"month_lunar": 3, "paksha": "Krishna", "tithi_in_paksha": 15, "name": "Vat Savitri Vrat (Amavasya) / Shani Jayanti", "tag": "amavasya", "icon": "🌑", "desc": "Devotion of Devi Savitri and birth of Lord Shani Dev.", "remedies": "Offer mustard oil and black sesame to Shani Dev."},
    {"month_lunar": 4, "paksha": "Shukla", "tithi_in_paksha": 2, "name": "Jagannath Ratha Yatra", "tag": "major", "icon": "🛕", "desc": "Grand Chariot procession of Lord Jagannath, Balabhadra, and Subhadra.", "remedies": "Sing Jagannath Ashtakam and Mahamantra."},
    {"month_lunar": 4, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Devshayani Ekadashi (Ashadhi Ekadashi)", "tag": "major", "icon": "🌿", "desc": "Beginning of the 4-month sacred Chaturmas period.", "remedies": "Begin sacred sankalpa, observe fast, recite Vishnu Sahasranama."},
    {"month_lunar": 4, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Guru Purnima (Vyasa Puja)", "tag": "major", "icon": "🧘", "desc": "Veneration of spiritual teachers, mentors, and Sage Veda Vyasa.", "remedies": "Express gratitude to Guru and parents; chant Guru Paduka Stotram."},
    {"month_lunar": 4, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Kamika Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi for spiritual purification during early Chaturmas.", "remedies": "Offer Tulsi leaves to Lord Krishna."},
    {"month_lunar": 5, "paksha": "Shukla", "tithi_in_paksha": 3, "name": "Hariyali Teej", "tag": "vrat", "icon": "🌸", "desc": "Celebration of the divine reunion of Shiva and Parvati.", "remedies": "Shiva-Parvati worship for happy married life."},
    {"month_lunar": 5, "paksha": "Shukla", "tithi_in_paksha": 5, "name": "Nag Panchami", "tag": "vrat", "icon": "🐍", "desc": "Sacred worship of Serpent deities for nature harmony and Rahu remedies.", "remedies": "Offer milk and kheer to snake deities for Rahu-Ketu dosha shanti."},
    {"month_lunar": 5, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Shravana Putrada Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi fast for progeny protection and spiritual prosperity.", "remedies": "Fast dedicated to Lord Vishnu."},
    {"month_lunar": 5, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Raksha Bandhan (Shravani Purnima / Upakarma)", "tag": "major", "icon": "🧵", "desc": "Sacred thread ritual of brother-sister bond and Vedic Upakarma.", "remedies": "Tie Rakhi, exchange auspicious blessings and sweets."},
    {"month_lunar": 5, "paksha": "Krishna", "tithi_in_paksha": 8, "name": "Krishna Janmashtami (Gokulashtami)", "tag": "major", "icon": "🦚", "desc": "Divine birth celebration of Lord Krishna in midnight Rohini Nakshatra.", "remedies": "Midnight Puja, offer Makhan-Mishri bhog and cradle infant Krishna."},
    {"month_lunar": 5, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Aja Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi for cleansing past negativities and gaining clarity.", "remedies": "Worship Lord Hrishikesha with heartfelt prayer."},
    {"month_lunar": 6, "paksha": "Shukla", "tithi_in_paksha": 3, "name": "Hartalika Teej", "tag": "vrat", "icon": "🌺", "desc": "Vow of Devi Parvati for obtaining Lord Shiva as consort.", "remedies": "Observe Nirjala fast and worship handmade Shiva-Parvati idols."},
    {"month_lunar": 6, "paksha": "Shukla", "tithi_in_paksha": 4, "name": "Ganesh Chaturthi (Vinayaka Chavithi)", "tag": "major", "icon": "🐘", "desc": "Grand 10-day celebration of Lord Ganesha, remover of all obstacles.", "remedies": "Install Ganesha idol; offer 21 Durva blades, red flowers, and Modaks."},
    {"month_lunar": 6, "paksha": "Shukla", "tithi_in_paksha": 5, "name": "Rishi Panchami", "tag": "vrat", "icon": "📜", "desc": "Sacred veneration of Sapta Rishis for purification from mistakes.", "remedies": "Pray to ancient Rishis for spiritual clarity."},
    {"month_lunar": 6, "paksha": "Shukla", "tithi_in_paksha": 8, "name": "Radha Ashtami", "tag": "vrat", "icon": "🌸", "desc": "Divine advent of Shri Radharani at noon.", "remedies": "Midday worship of Radha-Krishna with fragrant flowers."},
    {"month_lunar": 6, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Parsva Ekadashi (Parivartini Ekadashi)", "tag": "ekadashi", "icon": "🌿", "desc": "Lord Vishnu shifts posture during cosmic sleep; powerful fast.", "remedies": "Fast and light ghee lamps for Vishnu."},
    {"month_lunar": 6, "paksha": "Shukla", "tithi_in_paksha": 14, "name": "Anant Chaturdashi (Ganesh Visarjan)", "tag": "major", "icon": "🔱", "desc": "Culmination of Ganeshotsav and sacred 14-knot Ananta ritual.", "remedies": "Tie sacred Anant thread and perform Ganesha visarjan with chanting."},
    {"month_lunar": 6, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Bhadrapada Purnima / Pitru Paksha Shraddha Begins", "tag": "purnima", "icon": "🌕", "desc": "Commencement of the solemn fortnight dedicated to ancestors (Pitrus).", "remedies": "Perform Tarpan and feed cows, crows, and seekers."},
    {"month_lunar": 6, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Indira Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi dedicated to ancestral liberation and family lineage peace.", "remedies": "Offer Ekadashi fast merit for the peace of ancestors."},
    {"month_lunar": 6, "paksha": "Krishna", "tithi_in_paksha": 15, "name": "Sarva Pitru Amavasya (Mahalaya Amavasya)", "tag": "major", "icon": "🌑", "desc": "Grand culmination of Pitru Paksha; all ancestors are venerated.", "remedies": "Perform Shraddha with black sesame, kheer, and water for all departed souls."},
    {"month_lunar": 7, "paksha": "Shukla", "tithi_in_paksha": 1, "name": "Sharad Navratri Begins (Ghatasthapana)", "tag": "major", "icon": "🪔", "desc": "Nine sacred nights invoking Divine Mother Durga.", "remedies": "Perform Kalash Sthapana; light Akhand Jyoti; recite Argala Stotram."},
    {"month_lunar": 7, "paksha": "Shukla", "tithi_in_paksha": 8, "name": "Maha Ashtami (Durga Ashtami)", "tag": "major", "icon": "⚔️", "desc": "Worship of Maa Mahagauri and grand Sandhi Puja celebration.", "remedies": "Perform Kanya Pujan (worship of 9 girls) and offer Puri-Chana-Halwa."},
    {"month_lunar": 7, "paksha": "Shukla", "tithi_in_paksha": 9, "name": "Maha Navami / Ayudha Puja", "tag": "major", "icon": "🌸", "desc": "Worship of Maa Siddhidatri, tools of craft, books, and vehicles.", "remedies": "Blessing of work tools, vehicles, and books with turmeric & flowers."},
    {"month_lunar": 7, "paksha": "Shukla", "tithi_in_paksha": 10, "name": "Dussehra (Vijayadashami)", "tag": "major", "icon": "🏹", "desc": "Triumph of Lord Rama over Ravana and Maa Durga over Mahishasura.", "remedies": "Exchange auspicious Shami leaves and initiate new studies or ventures."},
    {"month_lunar": 7, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Papankusha Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi fast freeing the mind from attachment and remorse.", "remedies": "Fast with meditation and prayer to Lord Padmanabha."},
    {"month_lunar": 7, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Sharad Purnima (Kojagiri Lakshmi Puja)", "tag": "major", "icon": "🌕", "desc": "Night of divine nectar showers and arrival of Goddess Lakshmi.", "remedies": "Place sweet rice kheer under moonlight; worship Lakshmi at midnight."},
    {"month_lunar": 7, "paksha": "Krishna", "tithi_in_paksha": 4, "name": "Karwa Chauth (Sankashti Vrat)", "tag": "major", "icon": "🌙", "desc": "Sacred fast by married women for partner longevity and health.", "remedies": "Observe Nirjala fast until moonrise; offer Arghya to Chandra Dev."},
    {"month_lunar": 7, "paksha": "Krishna", "tithi_in_paksha": 8, "name": "Ahoi Ashtami", "tag": "vrat", "icon": "⭐", "desc": "Maternal fast for children happiness, health, and longevity.", "remedies": "Worship Ahoi Mata in evening after sighting evening stars."},
    {"month_lunar": 7, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Rama Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Pre-Diwali Ekadashi fast dedicated to Lord Vishnu and Devi Lakshmi.", "remedies": "Recite Vishnu Sahasranama and light evening lamps."},
    {"month_lunar": 7, "paksha": "Krishna", "tithi_in_paksha": 13, "name": "Dhanteras (Dhanvantari Jayanti)", "tag": "major", "icon": "🪙", "desc": "Advent of Lord Dhanvantari (God of Ayurveda) & wealth invocation.", "remedies": "Buy copper/silver/brass items; light 13 Yamadeepam diyas outside home."},
    {"month_lunar": 7, "paksha": "Krishna", "tithi_in_paksha": 14, "name": "Naraka Chaturdashi (Kali Chaudas / Choti Diwali)", "tag": "major", "icon": "🪔", "desc": "Elimination of Narakasura and cleansing of bodily impurities.", "remedies": "Pre-dawn Abhyanga Snan (oil bath) with sesame paste; light 14 lamps."},
    {"month_lunar": 7, "paksha": "Krishna", "tithi_in_paksha": 15, "name": "Diwali (Maha Lakshmi Puja)", "tag": "major", "icon": "✨", "desc": "Grand Festival of Lights! Invocation of Goddess Lakshmi, Ganesha & Kuber.", "remedies": "Perform Lakshmi Puja in Pradosh/Sthir Lagna; illuminate entire home with clay lamps."},
    {"month_lunar": 8, "paksha": "Shukla", "tithi_in_paksha": 1, "name": "Govardhan Puja / Annakut / Gujarati New Year", "tag": "major", "icon": "🌄", "desc": "Lifting of Govardhan Hill by Lord Krishna & culinary gratitude feast.", "remedies": "Prepare Annakut (56 delicacies); perform Gau Puja (cow worship)."},
    {"month_lunar": 8, "paksha": "Shukla", "tithi_in_paksha": 2, "name": "Bhai Dooj (Yama Dwitiya)", "tag": "major", "icon": "👫", "desc": "Sacred sibling festival celebrating love, protection, and longevity.", "remedies": "Sisters apply vermilion tilak to brothers; mutual gifts and feast."},
    {"month_lunar": 8, "paksha": "Shukla", "tithi_in_paksha": 6, "name": "Chhath Puja (Surya Shashthi)", "tag": "major", "icon": "☀️", "desc": "Auspicious sun-worship festival in running waters for health and vitality.", "remedies": "Offer Sandhya and Usha Arghya to Surya Dev with Thekua prasad."},
    {"month_lunar": 8, "paksha": "Shukla", "tithi_in_paksha": 8, "name": "Gopashtami", "tag": "vrat", "icon": "🐄", "desc": "Veneration of cows and calves nurtured by Lord Krishna.", "remedies": "Feed green grass, jaggery, and rotis to mother cows."},
    {"month_lunar": 8, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Devutthana Ekadashi (Tulsi Vivah Begins)", "tag": "major", "icon": "🌿", "desc": "Lord Vishnu awakens from Yogic slumber; holy wedding season opens.", "remedies": "Perform wedding of sacred Tulsi plant with Shaligram/Vishnu."},
    {"month_lunar": 8, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Dev Deepawali (Kartik Purnima)", "tag": "major", "icon": "🪔", "desc": "Festival of lights celebrated by the Gods in Kashi (Varanasi).", "remedies": "Light lamps near water bodies/temples; recite Shiva Mahimna Stotra."},
    {"month_lunar": 8, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Utpanna Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Manifestation of Goddess Ekadashi for protection of righteous devotees.", "remedies": "Fast dedicated to Lord Narayana."},
    {"month_lunar": 9, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Gita Jayanti (Mokshada Ekadashi)", "tag": "major", "icon": "📖", "desc": "Deliverance of the holy Srimad Bhagavad Gita by Lord Krishna on Kurukshetra.", "remedies": "Recite Gita chapters, donate copies of Bhagavad Gita, Vishnu Puja."},
    {"month_lunar": 9, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Dattatreya Jayanti (Margashirsha Purnima)", "tag": "major", "icon": "🕉️", "desc": "Birth of Lord Dattatreya, supreme synthesis of Brahma, Vishnu & Shiva.", "remedies": "Chant Datta Bavani and meditate on the universal Guru."},
    {"month_lunar": 9, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Saphala Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi turning earnest spiritual efforts into fruitful reality.", "remedies": "Fast with prayer to Lord Achyuta."},
    {"month_lunar": 10, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Pausha Putrada Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi fast for progeny protection and prosperity.", "remedies": "Offer fragrant flowers and white sweets to Lord Vishnu."},
    {"month_lunar": 10, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Pausha Purnima (Shakambhari Purnima)", "tag": "purnima", "icon": "🌕", "desc": "Start of Magha holy snan month; devotion to Mother Nature Shakambhari.", "remedies": "Donate vegetables, grains, and warm blankets to the poor."},
    {"month_lunar": 10, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Shattila Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi utilizing sacred sesame in 6 sanctifying rituals.", "remedies": "Sesame bath, sesame donation, sesame havan, and sesame food."},
    {"month_lunar": 11, "paksha": "Shukla", "tithi_in_paksha": 5, "name": "Vasant Panchami (Saraswati Puja)", "tag": "major", "icon": "🌸", "desc": "Advent of Spring and veneration of Goddess Saraswati, patron of wisdom.", "remedies": "Wear yellow attire; worship books, musical instruments, and Saraswati with yellow flowers."},
    {"month_lunar": 11, "paksha": "Shukla", "tithi_in_paksha": 7, "name": "Ratha Saptami (Surya Jayanti)", "tag": "major", "icon": "☀️", "desc": "Birth of Sun God turning his cosmic chariot towards North-East.", "remedies": "Morning bath with 7 Ark leaves on head; offer milk boiled in clay pot to Surya."},
    {"month_lunar": 11, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Jaya Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi granting victory over inner doubts and spiritual hurdles.", "remedies": "Observe fast dedicated to Lord Madhava."},
    {"month_lunar": 11, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Magha Purnima (Maha Maghi Snan)", "tag": "purnima", "icon": "🌕", "desc": "Culmination of month-long Magha snan; divine bathing in holy rivers.", "remedies": "Holy river bath, donation of food and clothes to spiritual seekers."},
    {"month_lunar": 11, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Vijaya Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Ekadashi observed by Lord Rama prior to crossing the ocean to Lanka.", "remedies": "Fast for overcoming major undertakings and trials."},
    {"month_lunar": 11, "paksha": "Krishna", "tithi_in_paksha": 14, "name": "Maha Shivaratri", "tag": "major", "icon": "🔱", "desc": "The Great Night of Shiva! Grand wedding of Shiva-Parvati & Jyotirlinga manifestation.", "remedies": "Night-long Shiva Abhishek with Belpatra, milk, gangajal, honey; chant Om Namah Shivaya."},
    {"month_lunar": 12, "paksha": "Shukla", "tithi_in_paksha": 11, "name": "Amalaki Ekadashi", "tag": "ekadashi", "icon": "🍈", "desc": "Sacred Ekadashi worshipping the life-giving Amla tree and Lord Vishnu.", "remedies": "Offer water and incense to Amla tree; distribute Amla prasad."},
    {"month_lunar": 12, "paksha": "Shukla", "tithi_in_paksha": 14, "name": "Holika Dahan (Choti Holi)", "tag": "major", "icon": "🔥", "desc": "Victory of devotee Prahlada over Holika; burning of negativity in sacred fire.", "remedies": "Circumambulate Holika bonfire; offer green wheat earheads, coconut, and sweets."},
    {"month_lunar": 12, "paksha": "Shukla", "tithi_in_paksha": 15, "name": "Holi (Rangwali Holi / Dhulivandan)", "tag": "major", "icon": "🎨", "desc": "Grand Festival of Colors celebrating spring, divine love, and harmonious union.", "remedies": "Apply natural herbal gulal, embrace loved ones, seek forgiveness and start anew."},
    {"month_lunar": 12, "paksha": "Krishna", "tithi_in_paksha": 11, "name": "Papmochani Ekadashi", "tag": "ekadashi", "icon": "🌿", "desc": "Final Ekadashi of the Vedic year clearing all past remorse and negativity.", "remedies": "Fast dedicated to Lord Vishnu in preparation for Vedic New Year."},
]


def _get_lunar_day_details(dt: datetime) -> Dict[str, Any]:
    """Calculate comprehensive Vedic lunar state for a given date."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    jd = swe.julday(dt.year, dt.month, dt.day, 6.0)
    sun_lon = swe.calc_ut(jd, swe.SUN, flags)[0][0] % 360.0
    moon_lon = swe.calc_ut(jd, swe.MOON, flags)[0][0] % 360.0

    diff = (moon_lon - sun_lon) % 360.0
    tithi_idx = int(diff / 12.0)  # 0 to 29
    paksha = "Shukla" if tithi_idx < 15 else "Krishna"
    tithi_in_paksha = (tithi_idx % 15) + 1  # 1 to 15

    nak_idx = int(moon_lon / (360.0 / 27.0)) % 27
    nakshatra = NAKSHATRA_NAMES[nak_idx]
    tithi_name = TITHI_NAMES[tithi_idx]

    # Calculate Chandramana Amanta Lunar Month (Masa)
    days_back = diff / 12.190749
    jd_nm = jd - days_back
    for _ in range(3):
        s = swe.calc_ut(jd_nm, swe.SUN, flags)[0][0] % 360.0
        m = swe.calc_ut(jd_nm, swe.MOON, flags)[0][0] % 360.0
        d = (m - s) % 360.0
        if d > 180.0:
            d -= 360.0
        jd_nm -= d / 12.190749

    s_nm = swe.calc_ut(jd_nm, swe.SUN, flags)[0][0] % 360.0
    nm_sign = int(s_nm / 30.0) % 12
    month_lunar = ((nm_sign + 1) % 12) + 1
    month_name = MONTH_NAMES[month_lunar]

    return {
        "jd": jd,
        "sun_lon": sun_lon,
        "moon_lon": moon_lon,
        "tithi_idx": tithi_idx,
        "paksha": paksha,
        "tithi_in_paksha": tithi_in_paksha,
        "tithi_name": tithi_name,
        "nakshatra": nakshatra,
        "month_lunar": month_lunar,
        "month_name": month_name,
    }


def get_day_festivals(dt: datetime) -> List[Dict[str, Any]]:
    """Retrieve all astronomical festivals and observances for a single specific calendar date."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    details = _get_lunar_day_details(dt)
    month_lunar = details["month_lunar"]
    month_name = details["month_name"]
    paksha = details["paksha"]
    tithi_in_paksha = details["tithi_in_paksha"]
    tithi_name = details["tithi_name"]
    nakshatra = details["nakshatra"]
    sun_lon = details["sun_lon"]
    jd = details["jd"]

    results: List[Dict[str, Any]] = []

    # 1. Check Solar Ingress (Makar Sankranti)
    if 269.0 <= sun_lon <= 272.0:
        jd_prev = jd - 1.0
        s_prev = swe.calc_ut(jd_prev, swe.SUN, flags)[0][0] % 360.0
        if s_prev < 270.0 <= sun_lon:
            results.append({
                "name": "Makar Sankranti / Pongal / Uttarayana",
                "tag": "major",
                "icon": "☀️",
                "desc": "Sun enters Makara (Capricorn) marking the start of auspicious Uttarayana.",
                "remedies": "Holy bath, offer Arghya to Sun God, donate til-gul and warm clothes.",
            })

    # 2. Match Annual Festivals
    for fest in ANNUAL_FESTIVALS:
        if (
            fest["month_lunar"] == month_lunar
            and fest["paksha"] == paksha
            and fest["tithi_in_paksha"] == tithi_in_paksha
        ):
            results.append(fest)

    # 3. Monthly Recurring Vrats (Only if no major annual festival is assigned)
    if not results:
        if paksha == "Shukla" and tithi_in_paksha == 4:
            results.append({
                "name": "Vinayaka Chaturthi",
                "tag": "vrat",
                "icon": "🐘",
                "desc": "Monthly auspicious day for Lord Ganesha worship.",
                "remedies": "Offer Modak and Durva grass to Lord Ganesha.",
            })
        elif paksha == "Krishna" and tithi_in_paksha == 4:
            results.append({
                "name": "Sankashti Chaturthi",
                "tag": "vrat",
                "icon": "🌙",
                "desc": "Monthly fast for Lord Ganesha for removal of distress.",
                "remedies": "Fast until Moonrise; worship Ganesha with modak.",
            })
        elif tithi_in_paksha == 13:
            results.append({
                "name": f"{paksha} Pradosh Vrat",
                "tag": "vrat",
                "icon": "🔱",
                "desc": "Sacred twilight worship of Lord Shiva and Maa Parvati.",
                "remedies": "Perform evening Shiva Puja during Pradosh Kaal.",
            })
        elif paksha == "Shukla" and tithi_in_paksha == 15:
            results.append({
                "name": f"{month_name} Purnima / Satyanarayan Vrat",
                "tag": "purnima",
                "icon": "🌕",
                "desc": "Auspicious full moon day for Sri Satyanarayan Katha and charity.",
                "remedies": "Perform Satyanarayan Puja and donate food.",
            })
        elif paksha == "Krishna" and tithi_in_paksha == 15:
            results.append({
                "name": f"{month_name} Amavasya (Darsha Amavasya)",
                "tag": "amavasya",
                "icon": "🌑",
                "desc": "Auspicious new moon day for meditation and ancestor Tarpan.",
                "remedies": "Offer water and black sesame to ancestors; feed birds and cows.",
            })

    formatted: List[Dict[str, Any]] = []
    for r in results:
        formatted.append({
            "name": r["name"],
            "date": dt.strftime("%d %b %Y"),
            "iso_date": dt.strftime("%Y-%m-%d"),
            "desc": r["desc"],
            "description": r["desc"],
            "tithi": f"{paksha} {tithi_name}",
            "paksha": paksha,
            "nakshatra": nakshatra,
            "tag": r.get("tag", "festival"),
            "icon": r.get("icon", "🎉"),
            "remedies": r.get("remedies", ""),
            "month": month_name,
            "is_today": False,
        })

    return formatted


def get_today_festivals() -> List[Dict[str, Any]]:
    """Retrieve all festivals falling on today's date."""
    today = datetime.now()
    festivals = get_day_festivals(today)

    for f in festivals:
        f["date"] = today.strftime("%Y-%m-%d")
        f["is_today"] = True

    if not festivals:
        details = _get_lunar_day_details(today)
        festivals.append({
            "name": f"{details['paksha']} {details['tithi_name']} Nitya Puja",
            "date": today.strftime("%Y-%m-%d"),
            "desc": f"Auspicious day for personal meditation and mantra japa under {details['nakshatra']} Nakshatra.",
            "description": f"Auspicious day for personal meditation and mantra japa under {details['nakshatra']} Nakshatra.",
            "tithi": f"{details['paksha']} {details['tithi_name']}",
            "paksha": details["paksha"],
            "nakshatra": details["nakshatra"],
            "tag": "vrat",
            "icon": "🕉️",
            "remedies": "Chant Gayatri mantra or perform personal Ishta Devata worship.",
            "month": details["month_name"],
            "is_today": True,
        })

    return festivals


def get_upcoming_festivals(limit: int = 14) -> List[Dict[str, Any]]:
    """Calculate upcoming festivals for the next 60 days with clean deduplication."""
    upcoming: List[Dict[str, Any]] = []
    base_date = datetime.now()
    seen_festival_names = set()

    for day_offset in range(1, 65):
        dt = base_date + timedelta(days=day_offset)
        day_events = get_day_festivals(dt)

        for fest in day_events:
            key = (fest["name"], fest["month"])
            if key not in seen_festival_names:
                seen_festival_names.add(key)
                upcoming.append(fest)
                if len(upcoming) >= limit:
                    return upcoming

    return upcoming
```

---

### l) modules/prediction/engine.py
**Path:** `astro-platform/backend/modules/prediction/engine.py`  
```python
"""
Prediction Engine Orchestrator.
Imports all 10 domain evaluators and runs analyse_all_domains.
"""

import hashlib
from modules.prediction.scoring import _build_ctx
from modules.prediction.domains.marriage import analyse_marriage
from modules.prediction.domains.career import analyse_career
from modules.prediction.domains.wealth import analyse_wealth
from modules.prediction.domains.health import analyse_health
from modules.prediction.domains.children import analyse_children
from modules.prediction.domains.education import analyse_education
from modules.prediction.domains.property import analyse_property
from modules.prediction.domains.challenges import analyse_challenges
from modules.prediction.domains.travel import analyse_travel
from modules.prediction.domains.spirituality import analyse_spirituality


from modules.prediction.timing import compute_timing, build_timing_block


def analyse_all_domains(chart: dict) -> dict:
    chart_bytes = str(sorted((k, str(v)) for k, v in chart.items())).encode('utf-8')
    input_hash = hashlib.sha256(chart_bytes).hexdigest()[:12]
    ctx = _build_ctx(chart)

    domains = {
        "marriage":    analyse_marriage(ctx),
        "career":      analyse_career(ctx),
        "wealth":      analyse_wealth(ctx),
        "health":      analyse_health(ctx),
        "children":    analyse_children(ctx),
        "education":   analyse_education(ctx),
        "property":    analyse_property(ctx),
        "challenges":  analyse_challenges(ctx),
        "travel":      analyse_travel(ctx),
        "spirituality":analyse_spirituality(ctx),
    }

    # Attach concrete timing block per domain
    for d_name, d_val in domains.items():
        if isinstance(d_val, dict):
            legacy_t = d_val.get("timing")
            timing_block = build_timing_block(chart, d_name)
            d_val["timing"] = timing_block
            d_val["timing_legacy"] = legacy_t
            d_val["timing_windows"] = timing_block.get("timing_windows", [])
            d_val["peak_window"] = timing_block.get("peak_window")
            d_val["next_12_months_summary"] = timing_block.get("next_12_months_summary", "")
            d_val["timing_methodology"] = timing_block.get("methodology", "")
            d_val["timing_engine"] = timing_block.get("engine_version", "1.0.0")

    return {
        "engine_version": "2.0.0-modular",
        "input_hash":     input_hash,
        "lagna":          ctx["lagna"],
        "mahadasha":      ctx["mahadasha"],
        "antardasha":     ctx["antardasha"],
        "yogas_detected": ctx["yogas"],
        "domains":        domains,
    }
```

---

### m) modules/prediction/timing_fusion.py
**Path:** `astro-platform/backend/modules/prediction/timing_fusion.py`  
```python
"""Window fusion engine combining Dasha (60%) + Gochara (40%) into ranked, smoothed timing windows."""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Dict, Any, List, Optional

from modules.prediction.timing_config import get_domain_timing_config
from modules.prediction.timing_dasha import score_dasha_periods, ScoredPeriod
from modules.prediction.timing_transit import score_transit_months, ScoredMonth


@dataclass
class TimingWindow:
    start_date: date
    end_date: date
    peak_date: date
    peak_score: float
    confidence: str
    mahadasha: str
    antardasha: str
    pratyantardasha: str
    reasons: List[str]
    drivers: List[str]
    sub_scores: Dict[str, float]


@dataclass
class TimingFusionResult:
    timing_windows: List[TimingWindow]
    peak_window: Optional[TimingWindow]
    next_12_months_summary: str
    methodology: str
    threshold_used: float
    engine_version: str


def get_confidence_tier(score: float) -> str:
    """Return confidence tier based on peak fused score."""
    if score >= 0.75:
        return "High"
    elif score >= 0.55:
        return "Moderate"
    elif score >= 0.35:
        return "Possible"
    return "Unlikely"


def fuse_windows(
    chart: dict,
    domain: str,
    start_date: date,
    end_date: date,
    top_n: int = 5,
) -> TimingFusionResult:
    """
    Combine Dasha periods (60%) + Transit months (40%) into ranked, smoothed timing windows.
    """
    config = get_domain_timing_config(domain)
    dasha_w = config.get("dasha_weight", 0.60)
    transit_w = config.get("transit_weight", 0.40)
    special_rules = config.get("special_rules", [])

    # 1. Fetch raw Dasha and Transit scores
    dasha_periods = score_dasha_periods(chart, domain, start_date, end_date)
    transit_months = score_transit_months(chart, domain, start_date, end_date)

    if not transit_months:
        return TimingFusionResult(
            timing_windows=[],
            peak_window=None,
            next_12_months_summary=f"No timing windows generated for {domain}.",
            methodology="Dasha 60% + Gochara 40%, 15-year horizon",
            threshold_used=0.45,
            engine_version="1.0.0",
        )

    # 2. STEP A — Align time axes per monthly snapshot
    monthly_snapshots = []
    for m in transit_months:
        # Find matching dasha period covering month_start
        matching_dasha = None
        for dp in dasha_periods:
            if dp.start_date <= m.month_start <= dp.end_date or dp.start_date <= m.month_end <= dp.end_date or m.month_start <= dp.start_date <= m.month_end:
                matching_dasha = dp
                break

        d_score = matching_dasha.score if matching_dasha else 0.30
        t_score = m.score

        combined = (dasha_w * d_score) + (transit_w * t_score)

        monthly_snapshots.append({
            "month_start": m.month_start,
            "month_end": m.month_end,
            "dasha_score": d_score,
            "transit_score": t_score,
            "combined_score": round(combined, 3),
            "dasha_period": matching_dasha,
            "transit_month": m,
        })

    # 3. STEP B — 3-month rolling average smoothing
    num_months = len(monthly_snapshots)
    smoothed_scores = []
    for i in range(num_months):
        prev_s = monthly_snapshots[i - 1]["combined_score"] if i > 0 else monthly_snapshots[i]["combined_score"]
        curr_s = monthly_snapshots[i]["combined_score"]
        next_s = monthly_snapshots[i + 1]["combined_score"] if i < num_months - 1 else monthly_snapshots[i]["combined_score"]

        smooth_val = round((prev_s + curr_s + next_s) / 3.0, 3)
        smoothed_scores.append(smooth_val)
        monthly_snapshots[i]["smoothed_score"] = smooth_val

    # 4. STEP C & D — Threshold & Merge consecutive months (with 1-month gap tolerance)
    threshold = 0.45
    qualifying_indices = [i for i, snap in enumerate(monthly_snapshots) if snap["smoothed_score"] >= threshold]

    raw_groups = []
    if qualifying_indices:
        current_group = [qualifying_indices[0]]
        for idx in qualifying_indices[1:]:
            # Allow up to 1-month gap between qualifying months (diff <= 2)
            if idx - current_group[-1] <= 2:
                current_group.append(idx)
            else:
                raw_groups.append(current_group)
                current_group = [idx]
        if current_group:
            raw_groups.append(current_group)

    # 5. Build raw TimingWindow objects from groups
    built_windows = []
    for grp in raw_groups:
        grp_months = [monthly_snapshots[i] for i in grp]
        peak_snap = max(grp_months, key=lambda x: x["smoothed_score"])

        w_start = grp_months[0]["month_start"]
        w_end = grp_months[-1]["month_end"]
        peak_dt = peak_snap["month_start"]
        peak_score = peak_snap["smoothed_score"]

        d_period = peak_snap["dasha_period"]
        t_month = peak_snap["transit_month"]

        md_l = d_period.mahadasha_lord if d_period else "Jupiter"
        ad_l = d_period.antardasha_lord if d_period else "Venus"
        pd_l = d_period.pratyantardasha_lord if d_period else "Saturn"

        d_reasons = d_period.reasons if d_period else []
        t_reasons = t_month.reasons if t_month else []
        merged_reasons = list(dict.fromkeys(d_reasons + t_reasons))

        top_drivers = merged_reasons[:4]
        conf = get_confidence_tier(peak_score)

        # 6. STEP H — Special rule enforcement
        sat_house = t_month.active_transits.get("Saturn", {}).get("house") if t_month else None
        if "saturn_7h_block" in special_rules and sat_house == 7 and domain == "marriage":
            conf = "Possible"

        if "jupiter_return_7h" in special_rules and peak_score >= 0.60:
            jup_h = t_month.active_transits.get("Jupiter", {}).get("house") if t_month else None
            if jup_h == 7:
                conf = "High"

        built_windows.append(
            TimingWindow(
                start_date=w_start,
                end_date=w_end,
                peak_date=peak_dt,
                peak_score=peak_score,
                confidence=conf,
                mahadasha=md_l,
                antardasha=ad_l,
                pratyantardasha=pd_l,
                reasons=merged_reasons,
                drivers=top_drivers,
                sub_scores={
                    "dasha_score": peak_snap["dasha_score"],
                    "transit_score": peak_snap["transit_score"],
                },
            )
        )

    # 7. STEP G — Deduplicate overlapping windows (>50% overlap)
    deduped_windows: List[TimingWindow] = []
    for w in built_windows:
        if not deduped_windows:
            deduped_windows.append(w)
        else:
            prev_w = deduped_windows[-1]
            overlap_start = max(prev_w.start_date, w.start_date)
            overlap_end = min(prev_w.end_date, w.end_date)
            if overlap_start <= overlap_end:
                overlap_days = (overlap_end - overlap_start).days + 1
                len1 = (prev_w.end_date - prev_w.start_date).days + 1
                len2 = (w.end_date - w.start_date).days + 1
                min_len = min(len1, len2)

                if min_len > 0 and (overlap_days / min_len) >= 0.50:
                    # Merge into stronger window
                    if w.peak_score > prev_w.peak_score:
                        deduped_windows[-1] = w
                    continue
            deduped_windows.append(w)

    # 8. STEP F — Rank and limit
    deduped_windows.sort(key=lambda x: x.peak_score, reverse=True)
    top_windows = deduped_windows[:top_n]
    peak_win = top_windows[0] if top_windows else None

    # Next 12 months summary
    if peak_win:
        summary_msg = f"Peak activation window for {domain} occurs around {peak_win.peak_date.strftime('%B %Y')} with {peak_win.confidence} confidence during {peak_win.mahadasha}-{peak_win.antardasha} Dasha."
    else:
        summary_msg = f"No major timing activation window identified for {domain} in the next 12 months."

    return TimingFusionResult(
        timing_windows=top_windows,
        peak_window=peak_win,
        next_12_months_summary=summary_msg,
        methodology="Dasha 60% + Gochara 40%, 15-year horizon",
        threshold_used=threshold,
        engine_version="1.0.0",
    )
```

---

### n) modules/prediction/timing_dasha.py
**Path:** `astro-platform/backend/modules/prediction/timing_dasha.py`  
```python
"""Dasha activation scoring engine for domain timing (Step 5.4)."""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Dict, Any, List, Optional

from shared.veda.zodiac import SIGNS, SIGN_LORDS
from modules.kundali.dasha import generate_dasha_timeline, generate_dasha_chain
from modules.prediction.timing_config import get_domain_timing_config
from modules.prediction.scoring import _build_ctx


@dataclass
class ScoredPeriod:
    start_date: date
    end_date: date
    mahadasha_lord: str
    antardasha_lord: str
    pratyantardasha_lord: str
    score: float           # 0.0 to 1.0
    reasons: List[str]
    sub_scores: Dict[str, float]  # {"md": float, "ad": float, "pd": float}


def is_functional_benefic(lord: str, lagna: str) -> bool:
    """Determine classical functional benefic status based on Lagna (Parashari)."""
    BENEFICS_BY_LAGNA = {
        "Mesha": ["Mars", "Jupiter", "Sun"],
        "Vrishabha": ["Venus", "Saturn", "Mercury"],
        "Mithuna": ["Mercury", "Venus", "Saturn"],
        "Karka": ["Moon", "Mars", "Jupiter"],
        "Simha": ["Sun", "Mars", "Jupiter"],
        "Kanya": ["Mercury", "Venus"],
        "Tula": ["Venus", "Saturn", "Mercury"],
        "Vrischika": ["Mars", "Jupiter", "Moon"],
        "Dhanu": ["Jupiter", "Sun", "Mars"],
        "Makara": ["Saturn", "Venus", "Mercury"],
        "Kumbha": ["Saturn", "Venus"],
        "Meena": ["Jupiter", "Mars", "Moon"],
    }
    return lord in BENEFICS_BY_LAGNA.get(lagna, ["Jupiter", "Venus"])


def is_functional_malefic(lord: str, lagna: str) -> bool:
    """Determine classical functional malefic status based on Lagna."""
    MALEFICS_BY_LAGNA = {
        "Mesha": ["Mercury", "Saturn"],
        "Vrishabha": ["Jupiter", "Mars"],
        "Mithuna": ["Mars", "Jupiter"],
        "Karka": ["Saturn", "Mercury"],
        "Simha": ["Saturn", "Venus"],
        "Kanya": ["Mars", "Jupiter"],
        "Tula": ["Sun", "Jupiter"],
        "Vrischika": ["Mercury", "Venus"],
        "Dhanu": ["Venus", "Mercury"],
        "Makara": ["Mars", "Jupiter"],
        "Kumbha": ["Moon", "Mars"],
        "Meena": ["Sun", "Venus", "Saturn"],
    }
    return lord in MALEFICS_BY_LAGNA.get(lagna, ["Rahu", "Ketu"])


def evaluate_lord_subscore(lord: str, role_name: str, config: Dict[str, Any], ctx: dict) -> tuple[float, List[str]]:
    """
    Evaluate sub-score (0.0 to 1.0) and reasons for a single Dasha lord (MD, AD, or PD).
    """
    raw_points = 0
    reasons = []

    lagna = ctx["lagna"]
    lagna_idx = ctx["lagna_idx"]
    target_houses = config.get("significator_houses", [1, 5, 9])
    primary_k = config.get("primary_karaka")
    secondary_ks = config.get("secondary_karaka", [])
    if isinstance(secondary_ks, str):
        secondary_ks = [secondary_ks]

    # 1. Karaka evaluation
    if lord == primary_k:
        raw_points += 2
        reasons.append(f"{lord} {role_name} is primary karaka for {config['domain']}")
    elif lord in secondary_ks:
        raw_points += 1
        reasons.append(f"{lord} {role_name} is secondary karaka for {config['domain']}")

    # 2. House lordship
    ruled_houses = []
    for h in range(1, 13):
        sign = SIGNS[(lagna_idx + h - 1) % 12]
        if SIGN_LORDS.get(sign) == lord:
            ruled_houses.append(h)

    matched_ruled = [h for h in ruled_houses if h in target_houses]
    if matched_ruled:
        raw_points += 2
        reasons.append(f"{lord} {role_name} is lord of {config['domain']} house(s) {matched_ruled}")

    # 3. Placement
    planet_data = ctx["planet_map"].get(lord, {})
    placement_house = planet_data.get("house", 1)
    if placement_house in target_houses:
        raw_points += 1
        reasons.append(f"{lord} {role_name} is placed in {config['domain']} house {placement_house}")

    # 4. Aspects (simplified 7th aspect / special Parashari aspects)
    aspect_houses = [(placement_house + 6) % 12 or 12]
    if lord == "Jupiter":
        aspect_houses.extend([(placement_house + 4) % 12 or 12, (placement_house + 8) % 12 or 12])
    elif lord == "Saturn":
        aspect_houses.extend([(placement_house + 2) % 12 or 12, (placement_house + 9) % 12 or 12])

    if any(h in target_houses for h in aspect_houses):
        raw_points += 1
        reasons.append(f"{lord} {role_name} aspects {config['domain']} house(s)")

    # 5. Functional Benefic / Malefic
    if is_functional_benefic(lord, lagna):
        raw_points += 1
        reasons.append(f"{lord} {role_name} is functional benefic for {lagna} Lagna")
    elif is_functional_malefic(lord, lagna):
        raw_points -= 2
        reasons.append(f"{lord} {role_name} is functional malefic for {lagna} Lagna")

    # 6. Dignity & Net Strength
    strength_label = planet_data.get("strength", "Neutral")
    if strength_label == "Exalted":
        raw_points += 1
        reasons.append(f"{lord} {role_name} is exalted")
    elif strength_label == "Debilitated":
        raw_points -= 2
        reasons.append(f"{lord} {role_name} is debilitated (penalty)")

    if placement_house in (6, 8, 12) and config["domain"] != "challenges":
        raw_points -= 1
        reasons.append(f"{lord} {role_name} is in dusthana house {placement_house}")

    # Clamp raw_points to [0, 7] and convert to [0.0, 1.0]
    clamped_points = max(0, min(7, raw_points))
    subscore = round(clamped_points / 7.0, 2)

    return subscore, reasons


def score_dasha_periods(
    chart: dict,
    domain: str,
    start_date: date,
    end_date: date,
) -> List[ScoredPeriod]:
    """
    Score Vimshottari Dasha periods (MD/AD/PD) for a domain over a given date range.
    """
    config = get_domain_timing_config(domain)
    ctx = _build_ctx(chart)

    # Convert date to string format for dasha chain filter
    f_start = start_date.strftime("%Y-%m-%d")
    f_end = end_date.strftime("%Y-%m-%d")

    dasha_info = chart.get("dasha", {})
    md_lord = dasha_info.get("current_mahadasha", "Jupiter")
    balance_years = dasha_info.get("balance_years", 10.0)

    now_dt = datetime(start_date.year, start_date.month, start_date.day)
    timeline = generate_dasha_timeline(md_lord, balance_years)
    dasha_chain = generate_dasha_chain(
        birth_datetime=now_dt,
        timeline=timeline,
        filter_start=f_start,
        filter_end=f_end,
    )

    scored_periods = []
    # Cap total returned periods at 200 to prevent performance bottlenecks
    for p in dasha_chain[:200]:
        p_s = datetime.strptime(p["start"], "%Y-%m-%d").date()
        p_e = datetime.strptime(p["end"], "%Y-%m-%d").date()

        # Clip dates to range boundary
        effective_start = max(p_s, start_date)
        effective_end = min(p_e, end_date)

        if effective_start >= effective_end:
            continue

        md_l = p["md_lord"]
        ad_l = p["ad_lord"]
        pd_l = p.get("pd_lord", ad_l)

        md_sub, md_reasons = evaluate_lord_subscore(md_l, "MD", config, ctx)
        ad_sub, ad_reasons = evaluate_lord_subscore(ad_l, "AD", config, ctx)
        pd_sub, pd_reasons = evaluate_lord_subscore(pd_l, "PD", config, ctx) if "pd_lord" in p else (ad_sub, ["PD not available, fallback to AD"])

        combined_score = (0.30 * md_sub) + (0.45 * ad_sub) + (0.25 * pd_sub)

        # Apply domain-specific special rules overrides
        special_rules = config.get("special_rules", [])
        if "saturn_7h_block" in special_rules and (md_l == "Saturn" or ad_l == "Saturn"):
            combined_score *= 0.70
            md_reasons.append("Saturn MD/AD applies 7H block multiplier (0.7)")

        if "venus_md_activates" in special_rules and md_l == "Venus":
            combined_score *= 1.20
            md_reasons.append("Venus MD universally activates marriage (1.2 multiplier)")

        final_score = round(max(0.0, min(1.0, combined_score)), 2)
        all_reasons = list(dict.fromkeys(md_reasons + ad_reasons + pd_reasons))

        scored_periods.append(
            ScoredPeriod(
                start_date=effective_start,
                end_date=effective_end,
                mahadasha_lord=md_l,
                antardasha_lord=ad_l,
                pratyantardasha_lord=pd_l,
                score=final_score,
                reasons=all_reasons,
                sub_scores={"md": md_sub, "ad": ad_sub, "pd": pd_sub},
            )
        )

    return scored_periods
```

---

### o) modules/prediction/timing_transit.py
**Path:** `astro-platform/backend/modules/prediction/timing_transit.py`  
```python
"""Gochara Transit activation scoring engine for domain timing (Step 5.5)."""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Dict, Any, List, Optional
import functools

import swisseph as swe

from shared.veda.zodiac import degree_to_sign, SIGNS, SIGN_LORDS
from modules.kundali.houses import assign_house
from modules.prediction.timing_config import get_domain_timing_config
from modules.prediction.transit_forecast import is_sade_sati_active, compute_transit_aspects
from shared.cache.keys import compute_input_hash


@dataclass
class ScoredMonth:
    month_start: date
    month_end: date
    score: float           # 0.0 to 1.0
    reasons: List[str]
    active_transits: dict  # planet -> {sign, house, aspect_houses}
    sub_scores: dict       # {jupiter, saturn, nodes, sade_sati}


def _get_planet_sign_house_at_date(dt: date, planet: str, lagna: str) -> tuple[str, int, List[int]]:
    """Compute exact sidereal sign, house from Lagna, and aspected houses for a planet at a date."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    planet_codes = {
        "Jupiter": swe.JUPITER,
        "Saturn": swe.SATURN,
        "Rahu": swe.TRUE_NODE,
        "Ketu": swe.TRUE_NODE,
    }

    code = planet_codes.get(planet, swe.JUPITER)
    jd = swe.julday(dt.year, dt.month, dt.day, 12.0)

    raw_pos = swe.calc_ut(jd, code, flags)[0][0]
    if planet == "Ketu":
        raw_pos = (raw_pos + 180.0) % 360.0
    else:
        raw_pos = raw_pos % 360.0

    sign, _ = degree_to_sign(raw_pos)
    house = assign_house(sign, lagna)
    aspects = compute_transit_aspects(planet, house)

    return sign, house, aspects


def score_transit_months(
    chart: dict,
    domain: str,
    start_date: date,
    end_date: date,
) -> List[ScoredMonth]:
    """Score monthly Gochara transit snapshots for a domain over a date range."""
    config = get_domain_timing_config(domain)
    lagna = chart.get("basic_details", {}).get("lagna", "Mesha")
    lagna_idx = SIGNS.index(lagna) if lagna in SIGNS else 0
    natal_moon = chart.get("basic_details", {}).get("moon_sign", "Mesha")
    natal_moon_idx = SIGNS.index(natal_moon) if natal_moon in SIGNS else 0

    transit_houses = config.get("transit_houses", [1, 5, 9])
    karaka_sign_house = config.get("transit_karaka_sign_house")
    is_negative_domain = config.get("transit_aspect_negative", False)
    special_rules = config.get("special_rules", [])

    # Find natal sign of domain primary karaka / lord
    primary_k = config.get("primary_karaka")
    natal_karaka_sign = None
    if primary_k:
        planets = chart.get("planets", {})
        if primary_k in planets:
            natal_karaka_sign = planets[primary_k].get("sign")

    # Generate monthly dates (sample at 15th of each month)
    scored_months: List[ScoredMonth] = []

    curr_year = start_date.year
    curr_month = start_date.month

    max_months = 180  # cap at 15 years
    month_count = 0

    while month_count < max_months:
        m_start = date(curr_year, curr_month, 1)
        if curr_month == 12:
            next_start = date(curr_year + 1, 1, 1)
        else:
            next_start = date(curr_year, curr_month + 1, 1)

        m_end = next_start - date.resolution

        if m_start > end_date:
            break

        sample_dt = date(curr_year, curr_month, 15)
        month_count += 1

        active_transits = {}
        reasons = []

        # 1. Evaluate Jupiter
        jup_sign, jup_house, jup_aspects = _get_planet_sign_house_at_date(sample_dt, "Jupiter", lagna)
        active_transits["Jupiter"] = {"sign": jup_sign, "house": jup_house, "aspects": jup_aspects}

        jup_pts = 0
        if not is_negative_domain:
            if jup_house in transit_houses:
                jup_pts += 3
                reasons.append(f"Jupiter transits domain house {jup_house}")

            matched_jup_aspects = [h for h in jup_aspects if h in transit_houses]
            if matched_jup_aspects:
                jup_pts += 2 * len(matched_jup_aspects)
                reasons.append(f"Jupiter aspects domain house(s) {matched_jup_aspects}")

            if karaka_sign_house and jup_house == karaka_sign_house:
                jup_pts += 2
                reasons.append(f"Jupiter transits karaka house {karaka_sign_house}")

            if jup_sign in ("Karka", "Dhanu", "Meena"):
                jup_pts += 1
                reasons.append(f"Jupiter is exalted/own sign in {jup_sign}")

            # Jupiter in kendra from Moon
            jup_from_moon = (SIGNS.index(jup_sign) - natal_moon_idx) % 12 + 1
            if jup_from_moon in (1, 4, 7, 10):
                jup_pts += 1
        else:
            # Negative domain: Jupiter protection reduces severity
            if jup_house in transit_houses:
                jup_pts += 2
                reasons.append(f"Jupiter protection in domain house {jup_house}")

        # Max achievable Jupiter points = 9 for benefic domains, 4 for negative domains
        max_jup = 9.0 if not is_negative_domain else 4.0
        jup_subscore = max(0.0, min(1.0, jup_pts / max_jup))

        # 2. Evaluate Saturn
        sat_sign, sat_house, sat_aspects = _get_planet_sign_house_at_date(sample_dt, "Saturn", lagna)
        active_transits["Saturn"] = {"sign": sat_sign, "house": sat_house, "aspects": sat_aspects}

        sat_pts = 0
        saturn_penalty = 0.0

        if is_negative_domain:
            if sat_house in transit_houses:
                sat_pts += 3
                reasons.append(f"Saturn transits domain house {sat_house} (activates discipline/health)")

            matched_sat_aspects = [h for h in sat_aspects if h in transit_houses]
            if matched_sat_aspects:
                sat_pts += 2 * len(matched_sat_aspects)
                reasons.append(f"Saturn aspects domain house(s) {matched_sat_aspects}")

            if sat_sign in ("Tula", "Makara", "Kumbha"):
                sat_pts += 1
                reasons.append(f"Saturn is exalted/own sign in {sat_sign}")
            max_sat = 6.0
            sat_subscore = max(0.0, min(1.0, sat_pts / max_sat))
        else:
            # Benefic domain: Saturn direct transit or aspect applies penalty
            if sat_house in transit_houses:
                saturn_penalty = 1.0
                reasons.append(f"Saturn transits domain house {sat_house} (blocking influence)")
            elif any(h in transit_houses for h in sat_aspects):
                saturn_penalty = 0.5
                reasons.append(f"Saturn aspects domain house(s)")
            sat_subscore = 0.0

        # 3. Evaluate Rahu & Ketu
        rahu_sign, rahu_house, rahu_aspects = _get_planet_sign_house_at_date(sample_dt, "Rahu", lagna)
        ketu_sign, ketu_house, ketu_aspects = _get_planet_sign_house_at_date(sample_dt, "Ketu", lagna)

        active_transits["Rahu"] = {"sign": rahu_sign, "house": rahu_house, "aspects": rahu_aspects}
        active_transits["Ketu"] = {"sign": ketu_sign, "house": ketu_house, "aspects": ketu_aspects}

        node_pts = 0
        nodes_penalty = 0.0

        if is_negative_domain:
            if rahu_house in transit_houses:
                node_pts += 2
                reasons.append(f"Rahu transits domain house {rahu_house}")
            if ketu_house in transit_houses:
                node_pts += 2
                reasons.append(f"Ketu transits domain house {ketu_house}")
            if any(h in transit_houses for h in rahu_aspects + ketu_aspects):
                node_pts += 1
                reasons.append("Rahu/Ketu aspect domain house(s)")
            node_subscore = max(0.0, min(1.0, node_pts / 3.0))
        else:
            if rahu_house in transit_houses or ketu_house in transit_houses:
                nodes_penalty = 1.0
                reasons.append(f"Rahu/Ketu transit domain house (disruptive influence)")
            elif any(h in transit_houses for h in rahu_aspects + ketu_aspects):
                nodes_penalty = 0.5
                reasons.append("Rahu/Ketu aspect domain house(s)")
            node_subscore = 0.0

        if domain == "marriage" and (rahu_house in (1, 7) or ketu_house in (1, 7)):
            reasons.append("Rahu/Ketu on 1H/7H axis (unconventional partnerships)")

        # 4. Sade Sati Modifier
        sade_info = is_sade_sati_active(sat_sign, natal_moon)
        sade_sati_modifier = 0.0
        if sade_info["active"]:
            if domain in ("health", "marriage", "career"):
                sade_sati_modifier = -0.15
                reasons.append(f"Sade Sati active ({sade_info['phase']}) — caution for {domain}")
            elif domain in ("challenges", "spirituality", "education"):
                sade_sati_modifier = 0.15
                reasons.append(f"Sade Sati active ({sade_info['phase']}) — intensifies focus for {domain}")

        # Final Transit score formula
        if not is_negative_domain:
            raw_transit = (0.65 * jup_subscore) - (0.25 * saturn_penalty) - (0.10 * nodes_penalty) + sade_sati_modifier
        else:
            raw_transit = (0.65 * sat_subscore) + (0.20 * node_subscore) + (0.15 * jup_subscore) + sade_sati_modifier

        month_score = max(0.0, min(1.0, raw_transit))
        if month_score == 0.0 and not reasons:
            month_score = 0.20  # baseline if no specific transits active
            reasons.append("Baseline transit activity")

        # 5. Apply Special Rules
        if "jupiter_return_7h" in special_rules and jup_house == 7 and natal_karaka_sign and jup_sign == natal_karaka_sign:
            month_score += 0.20
            reasons.append("Jupiter return to 7H (marriage blessing)")

        if "saturn_7h_block" in special_rules and sat_house == 7 and domain == "marriage":
            month_score *= 0.60
            reasons.append("Saturn 7H transit block multiplier (0.6)")

        if "saturn_10h_activates" in special_rules and sat_house == 10 and domain == "career":
            month_score += 0.20
            reasons.append("Saturn 10H transit activates career responsibilities")

        final_score = round(max(0.0, min(1.0, month_score)), 2)

        scored_months.append(
            ScoredMonth(
                month_start=m_start,
                month_end=m_end,
                score=final_score,
                reasons=list(dict.fromkeys(reasons)),
                active_transits=active_transits,
                sub_scores={
                    "jupiter": round(jup_subscore, 2),
                    "saturn": round(sat_subscore, 2),
                    "nodes": round(node_subscore, 2),
                    "sade_sati_modifier": round(sade_sati_modifier, 2),
                },
            )
        )

        # Advance to next month
        if curr_month == 12:
            curr_year += 1
            curr_month = 1
        else:
            curr_month += 1

    return scored_months
```

---

### q) modules/horoscope/engine.py
**Path:** `astro-platform/backend/modules/horoscope/engine.py`  
```python
"""Dynamic transit-driven daily horoscope engine."""

from datetime import date, datetime
import swisseph as swe
from shared.veda.zodiac import SIGNS_EN, SIGNS_SK

SIGN_TO_RASHI = {
    "aries": 0, "taurus": 1, "gemini": 2, "cancer": 3,
    "leo": 4, "virgo": 5, "libra": 6, "scorpio": 7,
    "sagittarius": 8, "capricorn": 9, "aquarius": 10, "pisces": 11,
}

MANTRAS = {
    "Aries": "Om Angarakaya Namaha (108×) — channel Mars' vitality with wisdom",
    "Taurus": "Om Shukraya Namaha (108×) — cultivate Venusian harmony and grace",
    "Gemini": "Om Budhaya Namaha (108×) — sharpen intellect and clear expression",
    "Cancer": "Om Chandraya Namaha (108×) — calm and harmonize emotional waters",
    "Leo": "Om Suryaya Namaha (108×) — strengthen inner sun, confidence, and dharma",
    "Virgo": "Om Budhaya Namaha (108×) — bring analytical precision to life",
    "Libra": "Om Shukraya Namaha (108×) — balance relationships and aesthetic joy",
    "Scorpio": "Om Bhaumaya Namaha (108×) — transform deep challenges into power",
    "Sagittarius": "Om Gurave Namaha (108×) — expand philosophical vision and truth",
    "Capricorn": "Om Shanaischaraya Namaha (19×) — build patient, enduring success",
    "Aquarius": "Om Sham Shanaischaraya Namaha (19×) — innovate for higher purpose",
    "Pisces": "Om Gurave Namaha (108×) — receive spiritual grace and compassion",
}

COLORS = {
    "Aries": "Crimson Red", "Taurus": "Pastel Pink", "Gemini": "Emerald Green",
    "Cancer": "Pearl White", "Leo": "Royal Gold", "Virgo": "Forest Green",
    "Libra": "Sky Blue", "Scorpio": "Deep Maroon", "Sagittarius": "Bright Yellow",
    "Capricorn": "Charcoal Navy", "Aquarius": "Electric Cyan", "Pisces": "Sea Green",
}


def generate_horoscope(sign_input: str | int) -> dict:
    """Generate dynamic transit-based horoscope for a given sign name or 0-11 index."""
    if isinstance(sign_input, int):
        sign_idx = max(0, min(11, sign_input))
        sign_en = SIGNS_EN[sign_idx]
    else:
        sign_clean = sign_input.strip().lower()
        sign_idx = SIGN_TO_RASHI.get(sign_clean, 0)
        sign_en = SIGNS_EN[sign_idx]

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    today = date.today()
    jd = swe.julday(today.year, today.month, today.day, 6.0)

    # Planetary positions
    sun_lon = swe.calc_ut(jd, swe.SUN, flags)[0][0] % 360.0
    moon_lon = swe.calc_ut(jd, swe.MOON, flags)[0][0] % 360.0
    jup_lon = swe.calc_ut(jd, swe.JUPITER, flags)[0][0] % 360.0
    ven_lon = swe.calc_ut(jd, swe.VENUS, flags)[0][0] % 360.0
    sat_lon = swe.calc_ut(jd, swe.SATURN, flags)[0][0] % 360.0

    sun_sign_idx = int(sun_lon / 30.0)
    moon_sign_idx = int(moon_lon / 30.0)
    jup_sign_idx = int(jup_lon / 30.0)

    # Relative house placement from current sign
    moon_h = ((moon_sign_idx - sign_idx) % 12) + 1
    jup_h = ((jup_sign_idx - sign_idx) % 12) + 1

    # Dynamic scores (60-95%)
    career_score = 70 + (15 if jup_h in (1, 5, 9, 10) else 0) + (5 if moon_h in (3, 6, 10, 11) else 0)
    love_score = 72 + (12 if ven_lon % 30 < 15 else 5)
    finance_score = 68 + (14 if jup_h in (2, 11, 9) else 4)
    health_score = 75 + (10 if moon_h not in (6, 8, 12) else -10)
    luck_score = 70 + (15 if jup_h in (1, 5, 9) else 5)

    lucky_num = ((sign_idx * 3 + today.day) % 9) + 1

    prediction_text = (
        f"For {sign_en}, today's cosmic transits highlight meaningful opportunities. "
        f"The Moon transit through house {moon_h} sharpens intuition and inner focus. "
        f"Jupiter's position in house {jup_h} grants steady support in professional and personal endeavors. "
        f"Stay aligned with your highest priorities, practice deliberate patience in communication, "
        f"and channel planetary energies into proactive action."
    )

    return {
        "status": "success",
        "sign": sign_en,
        "date": today.strftime("%Y-%m-%d"),
        "horoscope": prediction_text,
        "scores": {
            "career": min(98, career_score),
            "love": min(98, love_score),
            "finance": min(98, finance_score),
            "health": min(98, health_score),
            "luck": min(98, luck_score),
        },
        "lucky_number": lucky_num,
        "lucky_color": COLORS.get(sign_en, "Gold"),
        "mantra": MANTRAS.get(sign_en, "Om Namah Shivaya"),
        "tip": f"Focus constructive energy early in the day and maintain clear boundaries.",
        "compatible_signs": [SIGNS_EN[(sign_idx + 4) % 12], SIGNS_EN[(sign_idx + 8) % 12]],
    }


def generate_all_horoscopes() -> dict[str, dict]:
    """Generate horoscopes for all 12 signs."""
    return {sign: generate_horoscope(sign) for sign in SIGN_TO_RASHI}
```

---

### s) workers/narrative_worker.py
**Path:** `astro-platform/backend/workers/narrative_worker.py`  
```python
"""Background narrative generation worker process."""

import asyncio
import logging
from shared.logging.logger import get_logger
from shared.queue.redis_queue import default_queue, JobStatus
from modules.narrative.jobs import get_job, mark_running, mark_completed, mark_failed
from modules.narrative.engine import NarrativeEngine
from modules.narrative.schemas import NarrativeJobResult

logger = get_logger("workers.narrative_worker")


async def process_job(job_id: str, max_retries: int = 3):
    """Execute narrative LLM generation for a queued job."""
    job_status = await get_job(job_id)
    if not job_status or job_status.status == JobStatus.COMPLETED:
        return

    await mark_running(job_id)
    logger.info(f"Processing narrative job {job_id}...")

    # Load original request params from state
    from shared.cache.redis_client import CacheService
    import json
    raw = CacheService.get(f"narrative:job:{job_id}")
    data = json.loads(raw) if isinstance(raw, str) else raw
    req_dict = data.get("request", {})

    attempt = 0
    while attempt < max_retries:
        attempt += 1
        try:
            res_dict = NarrativeEngine.generate_predictions(
                year=req_dict.get("year", 1990),
                month=req_dict.get("month", 1),
                day=req_dict.get("day", 1),
                hour=req_dict.get("hour", 12.0),
                city=req_dict.get("city", "Pune"),
                lang=req_dict.get("lang", "en"),
            )
            result = NarrativeJobResult(
                marriage_prediction=res_dict.get("marriage_prediction"),
                career_prediction=res_dict.get("career_prediction"),
                raw_marriage_score=res_dict.get("raw_marriage_score"),
                raw_career_score=res_dict.get("raw_career_score"),
                chart=res_dict.get("chart"),
            )
            await mark_completed(job_id, result)
            logger.info(f"Narrative job {job_id} completed successfully.")
            return
        except Exception as exc:
            logger.warning(f"Attempt {attempt}/{max_retries} failed for job {job_id}: {exc}")
            if attempt >= max_retries:
                await mark_failed(job_id, f"LLM narrative generation failed after {max_retries} attempts: {exc}")
                return
            await asyncio.sleep(2 ** attempt)


async def run_worker():
    """Worker event loop pulling jobs from Redis queue."""
    logger.info("Narrative worker started listening for jobs...")
    while True:
        try:
            from shared.cache.redis_client import CacheService
            import json
            queue_key = "queue:narrative_queue"
            raw_list = CacheService.get(queue_key)
            job_ids = json.loads(raw_list) if isinstance(raw_list, str) else (raw_list or [])

            if job_ids:
                job_id = job_ids.pop(0)
                CacheService.set(queue_key, json.dumps(job_ids))
                await process_job(job_id)
            else:
                await asyncio.sleep(0.5)
        except Exception as exc:
            logger.error(f"Worker loop error: {exc}")
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(run_worker())
```

---

### t) modules/auth/security.py
**Path:** `astro-platform/backend/modules/auth/security.py`  
```python
import hashlib
import hmac
import os


def hash_password(password: str) -> str:
    """Hash a plaintext password using PBKDF2 with SHA-256 and a random salt."""
    salt = os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120000,
    ).hex()
    return f"{salt}${digest}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a plaintext password against a stored PBKDF2 hash string."""
    if not stored_hash or "$" not in stored_hash:
        return False
    try:
        salt, digest = stored_hash.split("$", 1)
    except ValueError:
        return False

    check = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120000,
    ).hex()
    return hmac.compare_digest(check, digest)
```

---

### u) shared/ephemeris/wrapper.py
**Path:** `astro-platform/backend/shared/ephemeris/wrapper.py`  
```python
"""Thin wrapper over pyswisseph (Swiss Ephemeris) for planetary math."""

import swisseph as swe

# Set Lahiri Ayanamsa by default
swe.set_ephe_path('.')
swe.set_sid_mode(swe.SIDM_LAHIRI)


def calc_ut(julian_day: float, body: int, flags: int = swe.FLG_SIDEREAL) -> tuple:
    """Calculate sidereal longitude and speed for a celestial body."""
    return swe.calc_ut(julian_day, body, flags)


def get_ayanamsa_ut(julian_day: float) -> float:
    """Return Lahiri ayanamsa value for a given Julian Day."""
    return swe.get_ayanamsa_ut(julian_day)


def julday(year: int, month: int, day: int, hour: float) -> float:
    """Convert UT date and decimal hour to Julian Day number."""
    return swe.julday(year, month, day, hour)


def houses(julian_day: float, lat: float, lon: float, hsys: bytes = b'E') -> tuple:
    """Calculate house cusps and Ascendant/MC (Equal system b'E' or Placidus b'P')."""
    return swe.houses(julian_day, lat, lon, hsys)
```

---

### v) shared/cache/redis_client.py
**Path:** `astro-platform/backend/shared/cache/redis_client.py`  
```python
"""Thread-safe In-Memory TTL & Redis Cache Implementation."""

import os
import time
import logging
from typing import Any, Optional

logger = logging.getLogger("app.core.cache")


class InMemoryTTLCache:
    """Thread-safe in-memory cache with Time-To-Live (TTL) expiration."""

    def __init__(self, default_ttl: int = 3600):
        self._cache: dict[str, tuple[Any, float]] = {}
        self.default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None
        val, expiry = self._cache[key]
        if time.time() > expiry:
            del self._cache[key]
            return None
        return val

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        ttl = ttl if ttl is not None else self.default_ttl
        expiry = time.time() + ttl
        self._cache[key] = (value, expiry)

    def delete(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self) -> None:
        self._cache.clear()

    def cleanup_expired(self) -> int:
        now = time.time()
        expired_keys = [k for k, (_, exp) in self._cache.items() if now > exp]
        for k in expired_keys:
            del self._cache[k]
        return len(expired_keys)


class RedisCacheWrapper:
    """Unified Cache Interface supporting Redis with In-Memory fallback."""

    def __init__(self, redis_url: Optional[str] = None, default_ttl: int = 3600):
        self.default_ttl = default_ttl
        self._fallback_cache = InMemoryTTLCache(default_ttl=default_ttl)
        self._redis_client = None
        self._use_redis = False

        if redis_url:
            try:
                import redis
                self._redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
                self._redis_client.ping()
                self._use_redis = True
                logger.info("Connected to Redis cache successfully.")
            except Exception as e:
                logger.warning(f"Redis unavailable ({e}), using thread-safe In-Memory TTL Cache.")
                self._use_redis = False
        else:
            logger.info("Redis unavailable, using thread-safe In-Memory TTL Cache.")

    def get_val(self, key: str) -> Optional[Any]:
        if self._use_redis and self._redis_client:
            try:
                import json
                raw = self._redis_client.get(key)
                return json.loads(raw) if raw else None
            except Exception as e:
                logger.error(f"Redis GET failed for key {key}: {e}")
                return self._fallback_cache.get(key)
        return self._fallback_cache.get(key)

    def set_val(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        ttl = ttl if ttl is not None else self.default_ttl
        if self._use_redis and self._redis_client:
            try:
                import json
                raw = json.dumps(value)
                self._redis_client.setex(key, ttl, raw)
                return True
            except Exception as e:
                logger.error(f"Redis SET failed for key {key}: {e}")
                self._fallback_cache.set(key, value, ttl)
                return True
        else:
            self._fallback_cache.set(key, value, ttl)
            return True

    def get(self, key: str) -> Optional[Any]:
        return self.get_val(key)

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        return self.set_val(key, value, ttl)

    def delete(self, key: str) -> bool:
        if self._use_redis and self._redis_client:
            try:
                res = self._redis_client.delete(key)
                return bool(res)
            except Exception as e:
                logger.error(f"Redis DELETE failed for key {key}: {e}")
                return self._fallback_cache.delete(key)
        return self._fallback_cache.delete(key)

    def clear(self) -> None:
        if self._use_redis and self._redis_client:
            try:
                self._redis_client.flushdb()
            except Exception as e:
                logger.error(f"Redis FLUSHDB failed: {e}")
        self._fallback_cache.clear()


# Global Singleton Cache Instance
REDIS_URL = os.getenv("REDIS_URL", None)
cache = RedisCacheWrapper(redis_url=REDIS_URL, default_ttl=3600)


class CacheService:
    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        return cache.get_val(key)

    @classmethod
    def set(cls, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        return cache.set_val(key, value, ttl)


    @classmethod
    def delete(cls, key: str) -> bool:
        return cache.delete(key)

    @classmethod
    def clear(cls) -> None:
        cache.clear()

    @staticmethod
    def get_panchang_key(date_str: str, lat: float, lon: float) -> str:
        return f"panchang:{date_str}:{round(lat, 3)}:{round(lon, 2)}"

    @staticmethod
    def get_kundali_key(hash_str: str) -> str:
        return f"kundali:{hash_str}"
```

---

### w) shared/cache/decorators.py
**Path:** `astro-platform/backend/shared/cache/decorators.py`  
```python
"""Decorator for chart computation caching with fail-open semantics."""

import functools
import logging
from typing import Any, Callable
from shared.cache.keys import compute_input_hash, chart_cache_key
from shared.cache.envelope import serialize_chart, deserialize_chart
from shared.cache.redis_client import CacheService
from shared.cache.metrics import cache_metrics

logger = logging.getLogger("shared.cache.decorators")


def cached_chart(ttl: int = 2592000, engine_version: str = "2.0.0") -> Callable:
    """
    Decorator for birth chart calculation methods.
    Checks cache first by input hash; computes & stores on miss.
    Guarantees fail-open behavior (never raises cache errors to callers).
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 1. Extract request object or kwargs
            req_data = None
            if args:
                for arg in args:
                    if isinstance(arg, dict) or (hasattr(arg, "__dict__") and not hasattr(arg, "__class__") and not hasattr(arg, "__module__")):
                        req_data = arg
                        break
                    elif hasattr(arg, "__dict__") and type(arg).__name__ not in ("DummyService", "KundaliService") and "Service" not in type(arg).__name__:
                        req_data = arg
                        break
            if not req_data:
                req_data = kwargs



            # 2. Try cache lookup
            key = None
            try:
                input_hash = compute_input_hash(req_data)
                key = chart_cache_key(input_hash, engine_version=engine_version)
                cached_bytes = CacheService.get(key)
                if cached_bytes:
                    payload = deserialize_chart(cached_bytes)
                    cache_metrics.record_hit(trace_id=key)
                    logger.info(f"Chart cache HIT for key: {key}")
                    return payload
                else:
                    cache_metrics.record_miss(trace_id=key)
            except Exception as exc:
                cache_metrics.record_error(str(exc), trace_id=key)
                logger.warning(f"Chart cache lookup error (failing open): {exc}")

            # 3. Compute chart on miss or error
            logger.info(f"Chart cache MISS for key: {key or 'unknown'}")
            res = func(*args, **kwargs)

            # 4. Store in cache
            if key and res:
                try:
                    serialized = serialize_chart(res, engine_version=engine_version)
                    CacheService.set(key, serialized, ttl=ttl)
                except Exception as exc:
                    cache_metrics.record_error(str(exc), trace_id=key)
                    logger.warning(f"Chart cache store error (failing open): {exc}")

            return res


        return wrapper

    return decorator


cached_by_hash = cached_chart
```

---

### x) shared/queue/redis_queue.py
**Path:** `astro-platform/backend/shared/queue/redis_queue.py`  
```python
"""Async Task Queue Interface & Redis Queue Wrapper."""

import os
import json
import logging
from typing import Any, Dict, Optional
from shared.cache.redis_client import CacheService

logger = logging.getLogger("shared.queue.redis_queue")


class JobStatus:
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class RedisQueue:
    """Lightweight Redis/In-Memory task queue abstraction."""

    def __init__(self, queue_name: str = "narrative_queue", ttl: int = 86400):
        self.queue_name = queue_name
        self.ttl = ttl

    async def enqueue(self, job_name: str, payload: Dict[str, Any], job_id: Optional[str] = None) -> str:
        """Enqueue job metadata and payload into Redis list and state store."""
        jid = job_id or f"job:{payload.get('input_hash', 'unknown')}"
        state_key = f"narrative:job:{jid}"

        job_data = {
            "job_id": jid,
            "job_name": job_name,
            "payload": payload,
            "status": JobStatus.QUEUED,
            "result": None,
            "error": None,
            "retries": 0,
        }

        try:
            # Store initial job state
            CacheService.set(state_key, json.dumps(job_data), ttl=self.ttl)
            # Push job id into queue list
            queue_key = f"queue:{self.queue_name}"
            raw_list = CacheService.get(queue_key) or []
            if isinstance(raw_list, str):
                try:
                    raw_list = json.loads(raw_list)
                except Exception:
                    raw_list = []
            if jid not in raw_list:
                raw_list.append(jid)
            CacheService.set(queue_key, json.dumps(raw_list), ttl=self.ttl)
            logger.info(f"Enqueued job {jid} into queue {self.queue_name}")
        except Exception as exc:
            logger.error(f"Failed to enqueue job {jid}: {exc}")
            raise exc

        return jid

    async def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve job state payload."""
        state_key = f"narrative:job:{job_id}"
        val = CacheService.get(state_key)
        if not val:
            return None
        if isinstance(val, str):
            try:
                return json.loads(val)
            except Exception:
                return None
        return val


default_queue = RedisQueue()
```

---

### y) shared/db/session.py
**Path:** `astro-platform/backend/shared/db/session.py`  
```python
"""SQLAlchemy Database Engine & Session Management."""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from shared.config import settings

logger = logging.getLogger("app.db.database")

# Ensure connect_args for SQLite
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
```

---

### z) shared/config/settings.py
**Path:** `astro-platform/backend/shared/config/settings.py`  
```python
"""Global Application Settings & Environment Configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Astro-Platform"
    APP_NAME: str = "Astro-Platform"
    app_name: str = "Astro-Platform"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = "astrologic-ai-super-secret-jwt-key-2026-production-secure"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    DATABASE_URL: str = "sqlite:///./astrologic.db"
    REDIS_URL: Optional[str] = None

    # LLM Settings
    GROQ_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "mistral"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "mistral"
    openai_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    llm_provider: str = "auto"
    LLM_PROVIDER: str = "auto"  # 'groq', 'gemini', 'openai', or 'auto'

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    ALLOWED_ORIGINS: str = "*"
    SESSION_SECRET_KEY: str = "astrologic-session-secret-key-2026"
    session_secret_key: str = "astrologic-session-secret-key-2026"

    # Chart Cache Settings
    CHART_CACHE_ENABLED: bool = True
    CHART_CACHE_TTL_SECONDS: int = 2592000  # 30 days
    CHART_CACHE_LRU_SIZE: int = 1000

    @property
    def cors_origins_list(self) -> list[str]:
        if isinstance(self.ALLOWED_ORIGINS, str):
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]
        return self.ALLOWED_ORIGINS or ["*"]

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() in ("production", "prod")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def __getattr__(self, name: str):
        # Prevent recursion when checking attributes
        upper_name = name.upper()
        if upper_name in self.__class__.model_fields or upper_name in self.__dict__ or hasattr(self.__class__, upper_name):
            return getattr(self, upper_name)
        lower_name = name.lower()
        if lower_name in self.__class__.model_fields or lower_name in self.__dict__ or hasattr(self.__class__, lower_name):
            return getattr(self, lower_name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")





def validate_settings(s: Settings = None) -> bool:
    """Validate critical security settings."""
    if s is None:
        s = settings
    sec_key = getattr(s, "secret_key", None) or getattr(s, "SECRET_KEY", None)
    if not sec_key:
        raise RuntimeError("Missing required environment variable: SECRET_KEY")
    return True



settings = Settings()
```

---

### p) modules/prediction/domains/*.py (All 10 Domain Evaluators)

#### Domain Evaluator: `career.py`
**Path:** `astro-platform/backend/modules/prediction/domains/career.py`
```python
"""Career & Profession Domain Evaluator."""

from modules.prediction.scoring import (
    _score_planets_in_houses, _score_house_lord, _dasha_activates,
    _yoga_present, _pct, _ordinal
)
from modules.prediction.remedies import _timing_windows, _build_remedies


def analyse_career(ctx: dict) -> dict:
    pm  = ctx["planet_map"]
    hl  = ctx["house_lords"]

    sun    = pm.get("Sun",{})
    saturn = pm.get("Saturn",{})
    mars   = pm.get("Mars",{})
    jupiter= pm.get("Jupiter",{})
    mercury= pm.get("Mercury",{})

    lord_10 = hl[10]; lord_10_data = pm.get(lord_10,{})
    lord_6  = hl[6];  lord_6_data  = pm.get(lord_6,{})
    h10_occ = [p for p,d in pm.items() if d["house"]==10]
    h6_occ  = [p for p,d in pm.items() if d["house"]==6]

    base   = _score_planets_in_houses(ctx, [10,6,11])
    l10s   = _score_house_lord(ctx, 10)
    sun_sc = sun.get("str_score",0) + (2 if sun.get("house") in (10,1,9) else 0)
    total  = base + l10s + sun_sc

    dasha_active = _dasha_activates(ctx, [10,6,11])
    pct = _pct(50, total, 12 if dasha_active else 0)

    sun_strong  = sun.get("str_score",0) >= 1 or sun.get("house") in (10,1)
    saturn_str  = saturn.get("str_score",0)
    if sun_strong and "Sun" in h10_occ:
        sector = "Government / Authority / IAS / Politics — strong Sun in 10th"
    elif saturn.get("house") in (10,6,11):
        sector = "Corporate / Technical / Service sector — Saturn influences career"
    elif mercury.get("house") in (10,6):
        sector = "Business / Communication / Finance / IT — Mercury drives career"
    elif jupiter.get("house") in (10,9):
        sector = "Teaching / Law / Finance / Spirituality — Jupiter in career houses"
    elif mars.get("house") in (10,6):
        sector = "Military / Police / Engineering / Surgery — Mars drives ambition"
    else:
        sector = "Diverse options — multiple planets influence career path"

    sign10 = ctx["house_signs"][10]
    FIELD_MAP = {
        "Mesha":"engineering, military, sports, surgery",
        "Vrishabha":"finance, banking, agriculture, arts, luxury goods",
        "Mithuna":"journalism, IT, marketing, teaching, trading",
        "Karka":"nursing, real estate, catering, hospitality, social work",
        "Simha":"leadership, politics, entertainment, management, medicine",
        "Kanya":"accounting, medicine, analysis, research, editing",
        "Tula":"law, diplomacy, design, fashion, HR, mediation",
        "Vrischika":"research, intelligence, psychology, occult, mining",
        "Dhanu":"education, law, philosophy, export-import, travel",
        "Makara":"administration, engineering, construction, government",
        "Kumbha":"technology, science, social sector, aviation, astrology",
        "Meena":"spirituality, arts, medicine, marine, photography",
    }
    best_fields = FIELD_MAP.get(sign10,"diverse professional fields")

    raj_yogas = _yoga_present(ctx, ["Raj","Raja","Budhaditya","Dharma Karma"])

    h11_lord = hl[11]; h11_data = pm.get(h11_lord,{})
    prom_active = h11_data.get("house") in (1,10,11) or "Jupiter" in [ctx["transit_map"].get("Jupiter",{}).get("house")]

    timing   = _timing_windows(ctx, [10,6,11], "career")
    weak_p   = [p for p,d in pm.items() if d["house"]==10 and d["str_score"]<0]
    if not weak_p and lord_10_data.get("str_score",0)<0: weak_p=[lord_10]
    remedies = _build_remedies(ctx, weak_p + ["Sun"], "career")

    return {
        "domain": "Career & Profession",
        "icon": "★",
        "score": pct,
        "sector": sector,
        "best_fields": best_fields,
        "tenth_lord": f"{lord_10} in {_ordinal(lord_10_data.get('house',0))}H — {lord_10_data.get('strength','')}",
        "h10_planets": h10_occ,
        "raj_yogas": raj_yogas,
        "business_vs_job": "Business favoured" if "Mercury" in h10_occ or mercury.get("house")==10 else "Service/Job favoured" if saturn.get("house")==10 else "Both viable — assess 7th for business",
        "foreign_work": "Strong foreign career indicators" if "Rahu" in h10_occ or ctx["transit_map"].get("Rahu",{}).get("house")==10 else "Domestic career more prominent",
        "dasha_active": dasha_active,
        "timing": timing,
        "remedies": remedies,
        "analysis": _career_narrative(ctx, pct, sector, best_fields, raj_yogas, timing),
    }


def _career_narrative(ctx, pct, sector, fields, yogas, timing):
    md = ctx["mahadasha"]; ad = ctx["antardasha"]
    hl10 = ctx["house_lords"][10]
    h10d = ctx["planet_map"].get(hl10,{})
    parts = []
    parts.append(f"Your 10th house of career is ruled by {hl10}, placed in the {_ordinal(h10d.get('house',1))} house — {h10d.get('strength','Neutral')}.")
    parts.append(f"Career direction points strongly toward {sector}. Best professional fields for your chart: {fields}.")
    if yogas:
        parts.append(f"Powerful career yogas are present: {', '.join(yogas)} — indicating recognition and rise to authority.")
    parts.append(f"Current {md}/{ad} dasha {'actively fires' if timing['dasha_active'] else 'does not directly trigger'} your career houses. Optimal window: {timing['best_window']}.")
    return " ".join(parts)


_career = analyse_career
```


#### Domain Evaluator: `challenges.py`
**Path:** `astro-platform/backend/modules/prediction/domains/challenges.py`
```python
"""Challenges & Dosha Domain Evaluator."""

from shared.veda import evaluate_mangal_dosha, evaluate_pitru_dosha
from modules.prediction.scoring import RASHI, _ordinal
from modules.prediction.remedies import _build_remedies


def analyse_challenges(ctx: dict) -> dict:
    pm  = ctx["planet_map"]
    hl  = ctx["house_lords"]

    rahu = pm.get("Rahu",{}); ketu=pm.get("Ketu",{})
    saturn=pm.get("Saturn",{}); mars=pm.get("Mars",{})

    rahu_h = rahu.get("house",1); ketu_h = ketu.get("house",1)
    all_others = [p for p in pm if p not in ("Rahu","Ketu")]
    ks_range = list(range(min(rahu_h,ketu_h), max(rahu_h,ketu_h)+1))
    kaal_sarp = all(pm[p]["house"] in ks_range for p in all_others if p in pm)

    eval_m = evaluate_mangal_dosha(pm)
    mangal = eval_m["present"] and not eval_m.get("cancelled", False)

    moon_sign_idx = RASHI.index(pm.get("Moon",{}).get("sign","Mesha")) if pm.get("Moon",{}).get("sign") in RASHI else 0
    sat_sign_idx  = RASHI.index(saturn.get("sign","Mesha")) if saturn.get("sign") in RASHI else 0
    sade_sati = abs(sat_sign_idx - moon_sign_idx) in (0,1,11)

    eval_p = evaluate_pitru_dosha(pm)
    pitru = eval_p["present"]

    grahan_planets = []
    for lum in ["Sun","Moon"]:
        lum_h = pm.get(lum,{}).get("house",0)
        if lum_h in (rahu.get("house",0), ketu.get("house",0)):
            grahan_planets.append(lum)
    grahan = len(grahan_planets) > 0

    doshas_found = []
    if kaal_sarp: doshas_found.append({"name":"Kaal Sarp Dosh","severity":"High","desc":"All planets hemmed between Rahu and Ketu — intense karmic patterns, obstacles followed by sudden rises."})
    if mangal:    doshas_found.append({"name":"Mangal Dosh","severity":"Moderate","desc":f"Mars in {_ordinal(mars.get('house',1))} house — relationship friction, energy imbalance. Match with similar chart."})
    if sade_sati: doshas_found.append({"name":"Shani Sade Sati","severity":"Moderate","desc":"Saturn transiting near Moon sign — 7.5-year karmic cleansing phase."})
    if pitru:     doshas_found.append({"name":"Pitru Dosh","severity":"Moderate","desc":"Ancestral karmic debt — offer tarpan on Amavasya and Pitru Paksha."})
    if grahan:    doshas_found.append({"name":"Grahan Dosh","severity":"Moderate" if len(grahan_planets)==1 else "High","desc":f"Rahu/Ketu eclipsing {', '.join(grahan_planets)} — emotional or identity challenges."})

    h6_malefics = [p for p in ["Saturn","Mars","Rahu"] if pm.get(p,{}).get("house")==6]
    legal_risk = len(h6_malefics)>0

    total_severity = len(doshas_found)
    pct = max(10, min(90, 80 - total_severity*15))

    remedies = _build_remedies(ctx,
        (["Rahu","Ketu"] if kaal_sarp else []) +
        (["Mars"] if mangal else []) +
        (["Saturn"] if sade_sati else []) +
        (["Sun"] if pitru else []),
        "challenges")

    return {
        "domain":"Challenges & Doshas","icon":"⚡","score":pct,
        "kaal_sarp":kaal_sarp,"mangal_dosh":mangal,"sade_sati":sade_sati,
        "pitru_dosh":pitru,"grahan_dosh":grahan,
        "doshas_found":doshas_found,"dosha_count":total_severity,
        "legal_risk":legal_risk,
        "legal_txt":"6th house affliction — highlights the importance of clear agreements, documentation, and diplomacy in professional matters." if legal_risk else "No strong legal trouble indicators.",
        "remedies":remedies,
        "analysis":_challenges_narrative(doshas_found),
    }


def _challenges_narrative(doshas_found):
    if not doshas_found:
        return "No major doshas detected — chart is relatively clean and free from major planetary afflictions."
    names = ", ".join([d["name"] for d in doshas_found])
    return f"{len(doshas_found)} dosha(s) detected: {names}. Appropriate remedies can significantly mitigate these effects. Consult an experienced Vedic astrologer for personalised rituals."


_challenges = analyse_challenges
```


#### Domain Evaluator: `children.py`
**Path:** `astro-platform/backend/modules/prediction/domains/children.py`
```python
"""Children & Next Generation Domain Evaluator."""

from modules.prediction.scoring import (
    _score_planets_in_houses, _score_house_lord, _dasha_activates,
    _dosha_present, _yoga_present, _pct, _ordinal
)
from modules.prediction.remedies import _timing_windows, _build_remedies


def analyse_children(ctx: dict) -> dict:
    pm = ctx["planet_map"]
    hl = ctx["house_lords"]

    jupiter = pm.get("Jupiter",{}); sun=pm.get("Sun",{}); moon=pm.get("Moon",{})
    lord_5 = hl[5]; l5d = pm.get(lord_5,{})
    h5_occ = [p for p,d in pm.items() if d["house"]==5]
    h9_occ = [p for p,d in pm.items() if d["house"]==9]

    base   = _score_planets_in_houses(ctx, [5,9,1])
    l5s    = _score_house_lord(ctx, 5)
    j_sc   = jupiter.get("str_score",0) + (2 if jupiter.get("house") in (5,9,1) else 0)
    total  = base + l5s + j_sc

    dasha_active = _dasha_activates(ctx, [5,9])
    pct = _pct(50, total, 10 if dasha_active else 0)

    putra_dosh = _dosha_present(ctx, ["Putra","Santana"])
    santana_yoga = _yoga_present(ctx, ["Santana","Putra"])

    j_h = jupiter.get("house",5)
    count = "Multiple children possible" if j_h in (5,11) and jupiter.get("str_score",0)>=0 \
            else "1-2 children indicated" if jupiter.get("str_score",0)>=0 \
            else "Challenges in childbearing — seek remedies"

    sign5 = ctx["house_signs"][5]
    MALE_SIGNS = ["Mesha","Mithuna","Simha","Dhanu","Kumbha"]
    gender_txt = "Male child indicated" if sign5 in MALE_SIGNS else "Female child indicated"

    child_nature = f"Child likely to be {'creative and intelligent' if 'Jupiter' in h5_occ or 'Mercury' in h5_occ else 'energetic and ambitious' if 'Mars' in h5_occ else 'artistic and sensitive' if 'Venus' in h5_occ or 'Moon' in h5_occ else 'disciplined and serious' if 'Saturn' in h5_occ else 'independent and bright'}"

    timing   = _timing_windows(ctx, [5,9], "children")
    remedies = _build_remedies(ctx, ["Jupiter"] if j_sc<0 else [], "children")

    return {
        "domain":"Children & Next Generation","icon":"❋","score":pct,
        "count_indicator":count,"gender_indicator":gender_txt,
        "child_nature":child_nature,"putra_dosh":putra_dosh,"santana_yoga":santana_yoga,
        "fifth_lord":f"{lord_5} in {_ordinal(l5d.get('house',0))}H — {l5d.get('strength','')}",
        "h5_planets":h5_occ,"jupiter_position":f"Jupiter in {_ordinal(jupiter.get('house',1))}H — {jupiter.get('strength','')}",
        "dasha_active":dasha_active,"timing":timing,"remedies":remedies,
        "analysis":f"Jupiter (putra karaka) in {_ordinal(jupiter.get('house',1))} house ({jupiter.get('strength','')}). 5th lord {lord_5} in {_ordinal(l5d.get('house',1))} house. {count}. {child_nature}. Timing: {timing['best_window']}.",
    }


_children = analyse_children
```


#### Domain Evaluator: `education.py`
**Path:** `astro-platform/backend/modules/prediction/domains/education.py`
```python
"""Education & Skills Domain Evaluator."""

from modules.prediction.scoring import (
    _score_planets_in_houses, _score_house_lord, _dasha_activates,
    _yoga_present, _pct, _ordinal
)
from modules.prediction.remedies import _timing_windows, _build_remedies


def analyse_education(ctx: dict) -> dict:
    pm = ctx["planet_map"]
    hl = ctx["house_lords"]

    mercury = pm.get("Mercury",{}); jupiter = pm.get("Jupiter",{}); sun=pm.get("Sun",{})
    lord_4 = hl[4]; l4d = pm.get(lord_4,{})
    lord_5 = hl[5]; l5d = pm.get(lord_5,{})
    h4_occ = [p for p,d in pm.items() if d["house"]==4]
    h5_occ = [p for p,d in pm.items() if d["house"]==5]

    base  = _score_planets_in_houses(ctx, [4,5,9])
    l4s   = _score_house_lord(ctx, 4)
    l5s   = _score_house_lord(ctx, 5)
    m_sc  = mercury.get("str_score",0)+(1 if mercury.get("house") in (4,5,9) else 0)
    j_sc  = jupiter.get("str_score",0)+(1 if jupiter.get("house") in (4,5,9) else 0)
    total = base + l4s + l5s + m_sc + j_sc

    dasha_active = _dasha_activates(ctx, [4,5,9])
    pct = _pct(50, total, 8 if dasha_active else 0)

    sign4 = ctx["house_signs"][4]
    STUDY_FIELDS = {
        "Mesha":"engineering, sports science, defense, physical therapy",
        "Vrishabha":"commerce, arts, agriculture, banking, architecture",
        "Mithuna":"journalism, languages, IT, mass communication, mathematics",
        "Karka":"nursing, psychology, hospitality, history",
        "Simha":"medicine, management, drama, literature, leadership",
        "Kanya":"medicine, accounting, research, editing, pharmacy",
        "Tula":"law, design, diplomacy, social sciences, fine arts",
        "Vrischika":"research, forensics, psychology, occult sciences",
        "Dhanu":"philosophy, law, education, foreign languages, travel",
        "Makara":"administration, civil services, engineering, finance",
        "Kumbha":"computer science, electronics, astrology, innovation",
        "Meena":"spirituality, medicine, arts, marine, music",
    }
    study_fields = STUDY_FIELDS.get(sign4,"diverse academic fields")

    vidya_yoga = _yoga_present(ctx, ["Saraswati","Vidya","Budhaditya"])
    foreign_edu = "Rahu" in h5_occ or pm.get("Rahu",{}).get("house") in (4,5,9)

    timing = _timing_windows(ctx, [4,5,9], "education")
    remedies = _build_remedies(ctx, ["Mercury"] if m_sc<0 else [], "education")

    return {
        "domain":"Education & Skills","icon":"✦","score":pct,
        "study_fields":study_fields,"vidya_yoga":vidya_yoga,
        "foreign_education":foreign_edu,
        "competitive_success":"Good competitive exam success" if pct>65 else "Focused preparation needed for competitive exams",
        "mercury_position":f"Mercury in {_ordinal(mercury.get('house',1))}H — {mercury.get('strength','')}",
        "dasha_active":dasha_active,"timing":timing,"remedies":remedies,
        "analysis":f"4th/5th houses govern education. Mercury (intellect) in {_ordinal(mercury.get('house',1))} house — {mercury.get('strength','')}. Best study fields: {study_fields}. {('Vidya Yoga present: '+', '.join(vidya_yoga)+' — academic distinction likely.' if vidya_yoga else '')} Foreign education: {'indicated' if foreign_edu else 'less prominent'}.",
    }


_education = analyse_education
```


#### Domain Evaluator: `health.py`
**Path:** `astro-platform/backend/modules/prediction/domains/health.py`
```python
"""Health & Longevity Domain Evaluator."""

from modules.prediction.scoring import (
    _score_planets_in_houses, _score_house_lord, _dasha_activates,
    _dosha_present, _pct, _ordinal
)
from modules.prediction.remedies import _timing_windows, _build_remedies


def analyse_health(ctx: dict) -> dict:
    pm  = ctx["planet_map"]
    hl  = ctx["house_lords"]

    sun    = pm.get("Sun",{})
    moon   = pm.get("Moon",{})
    saturn = pm.get("Saturn",{})
    mars   = pm.get("Mars",{})

    lord_1 = hl[1]; l1d = pm.get(lord_1,{})
    lord_6 = hl[6]; l6d = pm.get(lord_6,{})
    lord_8 = hl[8]; l8d = pm.get(lord_8,{})

    h1_occ = [p for p,d in pm.items() if d["house"]==1]
    h6_occ = [p for p,d in pm.items() if d["house"]==6]
    h8_occ = [p for p,d in pm.items() if d["house"]==8]

    base  = _score_planets_in_houses(ctx, [1,6,8])
    l1s   = _score_house_lord(ctx, 1)
    sun_sc= sun.get("str_score",0)
    total = base + l1s + sun_sc

    dasha_active = _dasha_activates(ctx, [6,8,12])
    pct = _pct(70, -total, -8 if dasha_active else 0)

    sign6 = ctx["house_signs"][6]
    ORGAN_MAP = {
        "Mesha":"head, brain, eyes","Vrishabha":"throat, neck, thyroid",
        "Mithuna":"lungs, arms, shoulders","Karka":"chest, stomach, breast",
        "Simha":"heart, spine, upper back","Kanya":"intestines, digestion, skin",
        "Tula":"kidneys, lower back, ovaries","Vrischika":"reproductive organs, excretory",
        "Dhanu":"hips, thighs, liver","Makara":"knees, bones, joints, teeth",
        "Kumbha":"ankles, nervous system, circulation","Meena":"feet, lymphatic, immune",
    }
    lagna_sign = ctx["lagna"]
    weak_organs = ORGAN_MAP.get(sign6,"general constitution")
    lagna_organs = ORGAN_MAP.get(lagna_sign,"overall vitality")

    DOSHA_MAP = {
        "Mesha":"Pitta","Vrishabha":"Kapha","Mithuna":"Vata","Karka":"Kapha",
        "Simha":"Pitta","Kanya":"Vata","Tula":"Vata","Vrischika":"Pitta",
        "Dhanu":"Pitta","Makara":"Vata","Kumbha":"Vata","Meena":"Kapha",
    }
    ayurvedic_dosha = DOSHA_MAP.get(lagna_sign,"Tridoshic")

    arishta = _dosha_present(ctx, ["Arishta","Balarishta","Kaal Sarp"])
    mental_h = moon.get("house",1)
    mental_ok = moon.get("str_score",0) >= 0 and mental_h not in (6,8,12)

    surgery_risk = "Mars" in h8_occ or "Mars" in h6_occ or saturn.get("house")==8
    disease_periods = f"Periods to watch: {ctx['mahadasha']} dasha / {ctx['antardasha']} antardasha if Saturn or Mars transits 1st, 6th or 8th"

    timing   = _timing_windows(ctx, [6,8,1], "health")
    remedies = _build_remedies(ctx, ["Sun"] if sun.get("str_score",0)<0 else (["Mars"] if mars.get("str_score",0)<0 else ["Saturn"]), "health")

    return {
        "domain":"Health & Longevity","icon":"✚","score":pct,
        "weak_organs":weak_organs,"lagna_organs":lagna_organs,
        "ayurvedic_dosha":ayurvedic_dosha,"emotional_sensitivity":"elevated" if not mental_ok else "balanced",
        "wellness_focus":surgery_risk,
        "wellness_txt":"Classical Vedic texts highlight this placement as a reminder to prioritize preventive health care and routine medical checkups." if surgery_risk else "Planetary alignment supports steady physical vitality.",
        "arishta_doshas":arishta,"disease_periods":disease_periods,
        "first_lord":f"{lord_1} in {_ordinal(l1d.get('house',0))}H — {l1d.get('strength','')}",
        "dasha_active":dasha_active,"timing":timing,"remedies":remedies,
        "analysis":_health_narrative(ctx,pct,weak_organs,ayurvedic_dosha,mental_ok),
    }


def _health_narrative(ctx,pct,organs,dosha,mental_ok):
    lagna=ctx["lagna"]; sun=ctx["planet_map"].get("Sun",{}); moon=ctx["planet_map"].get("Moon",{})
    parts=[]
    parts.append(f"Your Lagna (Ascendant) in {lagna} gives a {dosha} constitution — focus on balancing this Ayurvedic dosha through diet, lifestyle and seasonal cleansing.")
    parts.append(f"Vulnerable areas include {organs} — preventive care for these systems is advised.")
    parts.append(f"Sun (vitality karaka) is in the {_ordinal(sun.get('house',1))} house — {sun.get('strength','Neutral')}.")
    parts.append(f"Mental health is {'stable and resilient' if mental_ok else 'sensitive — Moon afflicted; manage stress proactively'}.")
    return " ".join(parts)


_health = analyse_health
```


#### Domain Evaluator: `marriage.py`
**Path:** `astro-platform/backend/modules/prediction/domains/marriage.py`
```python
"""Marriage & Relationships Domain Evaluator."""

from modules.prediction.scoring import (
    _score_planets_in_houses, _score_house_lord, _dasha_activates,
    _transit_influence, _pct, _ordinal, RASHI, RASHI_EN
)
from modules.prediction.remedies import _timing_windows, _build_remedies


def analyse_marriage(ctx: dict) -> dict:
    pm = ctx["planet_map"]
    hl = ctx["house_lords"]

    venus = pm.get("Venus", {})
    jupiter = pm.get("Jupiter", {})
    mars = pm.get("Mars", {})
    moon = pm.get("Moon", {})

    lord_7 = hl[7]
    lord_7_data = pm.get(lord_7, {})
    lord_7_house = lord_7_data.get("house", 0)
    lord_7_sign  = lord_7_data.get("sign","")
    lord_7_str   = lord_7_data.get("strength","Neutral")

    h7_occupants = [p for p,d in pm.items() if d["house"]==7]
    h5_occupants = [p for p,d in pm.items() if d["house"]==5]
    h2_occupants = [p for p,d in pm.items() if d["house"]==2]

    base  = _score_planets_in_houses(ctx, [7,5,2])
    l7s   = _score_house_lord(ctx, 7)
    venus_score = venus.get("str_score",0) + (2 if venus.get("house") in (7,5,2,1) else 0)
    total_score = base + l7s + venus_score

    dasha_active = _dasha_activates(ctx, [7,5,2])
    transit_sc   = _transit_influence(ctx, [7,5,2], ["Jupiter","Venus"])
    pct = _pct(50, total_score, 10 if dasha_active else 0)

    mangal_dosh = mars.get("house") in (1,4,7,8,12)
    mangal_txt = f"Mars in {_ordinal(mars.get('house',0))} house — Mangal Dosh present. Seek dosha cancellation or match with similar chart." if mangal_dosh else "No Mangal Dosh detected."

    kalatra = "Kalatra Yoga" in str(ctx.get("yogas",""))

    if h5_occupants and "Venus" in h5_occupants:
        marriage_type = "Strong indicators of love marriage — Venus in 5th house of romance."
    elif "Jupiter" in h7_occupants:
        marriage_type = "Arranged marriage favoured — Jupiter blesses the 7th house with wisdom and tradition."
    elif "Rahu" in h7_occupants:
        marriage_type = "Unconventional or inter-cultural marriage possible — Rahu influences 7th."
    elif venus.get("house") == 7:
        marriage_type = "Love or love-cum-arranged marriage — Venus directly occupies partnership house."
    else:
        marriage_type = "Arranged marriage most likely — assess 5th house for romance indicators."

    sign7 = ctx["house_signs"][7]
    PARTNER_TRAITS = {
        "Mesha":"dynamic, ambitious, independent, sometimes impatient",
        "Vrishabha":"loyal, sensual, patient, materialistic, loves comfort",
        "Mithuna":"witty, communicative, versatile, may be dual-natured",
        "Karka":"caring, emotional, home-loving, intuitive, protective",
        "Simha":"confident, generous, dramatic, needs admiration",
        "Kanya":"analytical, health-conscious, critical, service-oriented",
        "Tula":"charming, diplomatic, aesthetic, partnership-oriented",
        "Vrischika":"intense, secretive, transformative, passionate",
        "Dhanu":"philosophical, adventurous, honest, sometimes blunt",
        "Makara":"disciplined, ambitious, traditional, reliable",
        "Kumbha":"independent, humanitarian, unconventional, intellectual",
        "Meena":"spiritual, compassionate, artistic, sometimes escapist",
    }
    partner_traits = PARTNER_TRAITS.get(sign7, "dignified and balanced")
    if h7_occupants:
        planet_modifiers = {"Venus":"charming and romantic","Jupiter":"wise and spiritual",
                           "Saturn":"mature and serious","Mars":"energetic and assertive",
                           "Mercury":"intelligent and communicative","Moon":"emotional and nurturing",
                           "Sun":"authoritative and proud","Rahu":"exotic or foreign connection",
                           "Ketu":"spiritual or detached"}
        mods = [planet_modifiers[p] for p in h7_occupants if p in planet_modifiers]
        if mods: partner_traits += f" — {', '.join(mods)}"

    h8_lord = hl[8]
    h8_data = pm.get(h8_lord,{})
    second_marriage = "Indicators present for second marriage or significant relationship transformation" \
                      if (h8_data.get("house") in (7,2) or "Rahu" in h7_occupants) \
                      else "No strong indicators for second marriage."

    h8_occ = [p for p,d in pm.items() if d["house"]==8]
    intimacy = "Strong physical chemistry" if "Mars" in h8_occ or "Venus" in h8_occ \
               else "Emotional and spiritual connection dominates"

    timing  = _timing_windows(ctx, [7,5,2], "marriage")
    remedies = _build_remedies(ctx,
        [p for p,d in pm.items() if d["house"] in (7,) and d["str_score"]<0] + (["Venus"] if venus.get("str_score",0)<0 else []),
        "marriage")

    return {
        "domain": "Marriage & Relationships",
        "icon":   "♥",
        "score":  pct,
        "marriage_type":   marriage_type,
        "partner_traits":  partner_traits,
        "partner_sign":    f"{sign7} ({RASHI_EN[RASHI.index(sign7)] if sign7 in RASHI else sign7})",
        "mangal_dosh":     mangal_dosh,
        "mangal_dosh_txt": mangal_txt,
        "kalatra_yoga":    kalatra,
        "second_marriage": second_marriage,
        "intimacy":        intimacy,
        "venus_position":  f"Venus in {venus.get('house',0)}H {venus.get('sign','')} — {venus.get('strength','')}",
        "seventh_lord":    f"{lord_7} in {_ordinal(lord_7_house)} house — {lord_7_str}",
        "h7_planets":      h7_occupants,
        "dasha_active":    dasha_active,
        "timing":          timing,
        "remedies":        remedies,
        "analysis":        _marriage_narrative(ctx, pct, marriage_type, partner_traits, timing),
    }


def _marriage_narrative(ctx, pct, mtype, traits, timing):
    md = ctx["mahadasha"]; ad = ctx["antardasha"]
    venus = ctx["planet_map"].get("Venus",{})
    h7 = [p for p,d in ctx["planet_map"].items() if d["house"]==7]
    parts = []
    parts.append(f"Your 7th house of marriage is ruled by {ctx['house_lords'][7]}, and {mtype.lower()}")
    if h7:
        parts.append(f"With {', '.join(h7)} occupying the 7th house, your partnerships carry their energies — {', '.join([str(p) for p in h7])} shapes the nature of your unions.")
    parts.append(f"Venus, the primary karaka for marriage, is placed in the {_ordinal(venus.get('house',1))} house in {venus.get('sign','')} — {venus.get('strength','')}, indicating {'strong' if venus.get('str_score',0)>=0 else 'a challenged'} capacity for love and harmony.")
    parts.append(f"Your partner is likely to be {traits}.")
    parts.append(f"Current {md}/{ad} dasha {'actively triggers' if timing['dasha_active'] else 'does not directly activate'} the marriage houses. Best timing window: {timing['best_window']}.")
    return " ".join(parts)


_marriage = analyse_marriage
```


#### Domain Evaluator: `property.py`
**Path:** `astro-platform/backend/modules/prediction/domains/property.py`
```python
"""Property & Home Domain Evaluator."""

from modules.prediction.scoring import (
    _score_planets_in_houses, _score_house_lord, _dasha_activates,
    _pct, _ordinal
)
from modules.prediction.remedies import _timing_windows, _build_remedies


def analyse_property(ctx: dict) -> dict:
    pm = ctx["planet_map"]
    hl = ctx["house_lords"]

    mars = pm.get("Mars",{}); moon=pm.get("Moon",{}); saturn=pm.get("Saturn",{})
    lord_4 = hl[4]; l4d = pm.get(lord_4,{})
    h4_occ = [p for p,d in pm.items() if d["house"]==4]

    base  = _score_planets_in_houses(ctx, [4,2,12])
    l4s   = _score_house_lord(ctx, 4)
    m_sc  = mars.get("str_score",0)+(2 if mars.get("house") in (4,2) else 0)
    total = base + l4s + m_sc

    dasha_active = _dasha_activates(ctx, [4,12,2])
    pct = _pct(50, total, 8 if dasha_active else 0)

    sign4 = ctx["house_signs"][4]
    PROP_TYPE = {
        "Mesha":"independent house / active environment preferred",
        "Vrishabha":"fertile land, luxurious property, garden",
        "Mithuna":"apartment in busy area, multi-story building",
        "Karka":"near water body, ancestral property",
        "Simha":"large prestigious property, prominent location",
        "Kanya":"clean, hygienic, well-organized living space",
        "Tula":"beautiful, artistically designed home",
        "Vrischika":"old or hidden property, secretive location",
        "Dhanu":"property near temples, open land, hills",
        "Makara":"durable construction, traditional or stone buildings",
        "Kumbha":"modern housing society, tech-enabled home",
        "Meena":"near sea, spiritual property, irregular shape",
    }
    prop_type = PROP_TYPE.get(sign4,"varied property types")

    multiple_props = mars.get("str_score",0)>=2 or (mars.get("house")==4 and "Mars" in h4_occ)
    domestic_happiness = "Moon" in h4_occ or moon.get("house")==4 or moon.get("str_score",0)>=1

    timing = _timing_windows(ctx, [4,2,12], "property")
    remedies = _build_remedies(ctx, ["Mars"] if m_sc<0 else [], "property")

    return {
        "domain":"Property & Home","icon":"⌂","score":pct,
        "property_type":prop_type,"multiple_properties":multiple_props,
        "domestic_happiness":domestic_happiness,
        "vastu":"4th house in earthy signs — vastu compliance highly beneficial" if sign4 in ("Vrishabha","Kanya","Makara") else "Standard vastu principles apply",
        "fourth_lord":f"{lord_4} in {_ordinal(l4d.get('house',0))}H — {l4d.get('strength','')}",
        "mars_position":f"Mars in {_ordinal(mars.get('house',1))}H — {mars.get('strength','')}",
        "dasha_active":dasha_active,"timing":timing,"remedies":remedies,
        "analysis":f"4th house (property) ruled by {lord_4} in {_ordinal(l4d.get('house',1))} house — {l4d.get('strength','')}. Property type: {prop_type}. Mars (real estate karaka) in {_ordinal(mars.get('house',1))} house. {('Multiple properties possible.' if multiple_props else '')} Best purchase window: {timing['best_window']}.",
    }


_property = analyse_property
```


#### Domain Evaluator: `spirituality.py`
**Path:** `astro-platform/backend/modules/prediction/domains/spirituality.py`
```python
"""Spirituality & Karma Domain Evaluator."""

from modules.prediction.scoring import _domain_score, _ordinal
from modules.prediction.remedies import _timing, _build_remedies, _house_lord_str


def analyse_spirituality(ctx: dict) -> dict:
    pm=ctx["planet_map"]; hl=ctx["house_lords"]; fn=ctx.get("fn",{}); ns=ctx.get("net_scores",{}); yogas=ctx.get("yogas",[])

    result=_domain_score(ctx,[9,12],karaka="Jupiter",secondary_houses=[1,5,8])
    sc=result["score"]

    ketu=pm.get("Ketu",{}); jupiter=pm.get("Jupiter",{})
    lord_9=hl[9]; lord_12=hl[12]

    ketu_h=ketu.get("house",1)
    spiritual_inc=(ketu_h in (1,5,9,12) and ns.get("Ketu",0)>=-1) or (ns.get("Jupiter",0)>=1 and jupiter.get("house") in (9,12))

    moksha=[y for y in yogas if any(k in (y if isinstance(y, str) else y.get("name","")) for k in ("Vipreet","Moksha","Kaal Sarp"))]

    moon_nak=pm.get("Moon",{}).get("nakshatra","Ashwini")
    DEITY={
        "Ashwini":"Ashwini Kumaras","Bharani":"Lord Yama","Krittika":"Lord Agni",
        "Rohini":"Lord Brahma / Krishna","Mrigashira":"Soma (Chandra)","Ardra":"Lord Shiva / Rudra",
        "Punarvasu":"Mother Aditi","Pushya":"Lord Brihaspati / Shiva","Ashlesha":"Naga Devatas",
        "Magha":"Pitrus (Ancestors)","Purva Phalguni":"Lord Bhaga","Uttara Phalguni":"Lord Aryaman",
        "Hasta":"Surya (Savitri)","Chitra":"Lord Vishwakarma","Swati":"Lord Vayu",
        "Vishakha":"Indra and Agni","Anuradha":"Lord Mitra","Jyeshtha":"Lord Indra",
        "Mula":"Nirrti (Kali)","Purva Ashadha":"Apas (Water deities)","Uttara Ashadha":"Vishwadevas",
        "Shravana":"Lord Vishnu","Dhanishta":"Ashta Vasus","Shatabhisha":"Lord Varuna",
        "Purva Bhadrapada":"Aja Ekapada","Uttara Bhadrapada":"Ahir Budhanya","Revati":"Pusha",
    }
    deity=DEITY.get(moon_nak,"Lord Vishnu")

    ketu_domain=["self-mastery","wealth and family","communication","home and comfort",
                 "creativity and past merit","service and karma","partnerships","occult and transformation",
                 "dharma and teacher","career and action","social connections","liberation and loss"][ketu_h-1]
    past_karma=f"Ketu in {_ordinal(ketu_h)} house — past-life mastery in {ketu_domain}. This life, the soul seeks to balance through the opposite {_ordinal(((ketu_h+5)%12)+1)} house themes."

    sign9=ctx["house_signs"][9]
    DHARMA={"Mesha":"courage and individual initiative","Vrishabha":"sensory service and material dharma",
            "Mithuna":"communication and mental dharma","Karka":"emotional service and family dharma",
            "Simha":"leadership and creative dharma","Kanya":"service, healing and perfection",
            "Tula":"justice, balance and relational dharma","Vrischika":"transformation and occult dharma",
            "Dhanu":"knowledge, teaching and philosophical dharma","Makara":"discipline and structural dharma",
            "Kumbha":"innovation, community and humanitarian dharma","Meena":"surrender, compassion and spiritual dharma"}
    dharma=DHARMA.get(sign9,"alignment with cosmic order")

    remedies=_build_remedies(ctx,["Jupiter","Ketu"],"spirituality")
    timing=_timing(ctx,[9,12,5],"spirituality")

    j_ns=round(ns.get("Jupiter",0),1); l9_ns=round(ns.get(lord_9,0),1)

    return {
        "domain":"Spirituality & Karma","icon":"☯","score":sc,
        "spiritual_inclination":spiritual_inc,"moksha_yoga":moksha,"deity":deity,"past_karma":past_karma,
        "dharma_path":f"9th house in {sign9} — dharma through {dharma}",
        "ninth_lord":_house_lord_str(ctx,9),
        "ketu_position":f"Ketu in {_ordinal(ketu_h)}H",
        "dasha_active":result["dasha_active"],
        "timing":timing,"remedies":remedies,
        "analysis":f"9th lord {lord_9} net {l9_ns:+.1f}. Jupiter net {j_ns:+.1f}. {'Strong spiritual inclination — Ketu in spiritual house.' if spiritual_inc else 'Spiritual growth through material experience first.'} {past_karma} Deity: {deity}. Dharma: {dharma}.",
        "_scoring":result,
    }


_spirituality = analyse_spirituality
```


#### Domain Evaluator: `travel.py`
**Path:** `astro-platform/backend/modules/prediction/domains/travel.py`
```python
"""Travel & Foreign Domain Evaluator."""

from modules.prediction.scoring import (
    _score_planets_in_houses, _score_house_lord, _dasha_activates,
    _pct, _ordinal
)
from modules.prediction.remedies import _timing_windows, _build_remedies


def analyse_travel(ctx: dict) -> dict:
    pm = ctx["planet_map"]
    hl = ctx["house_lords"]

    rahu=pm.get("Rahu",{}); ketu=pm.get("Ketu",{}); moon=pm.get("Moon",{})
    lord_12=hl[12]; l12d=pm.get(lord_12,{})
    lord_9=hl[9]; l9d=pm.get(lord_9,{})
    h12_occ=[p for p,d in pm.items() if d["house"]==12]
    h9_occ=[p for p,d in pm.items() if d["house"]==9]

    base  = _score_planets_in_houses(ctx, [12,9,3])
    l12s  = _score_house_lord(ctx, 12)
    r_sc  = 2 if rahu.get("house") in (12,9,3) else 0
    total = base + l12s + r_sc

    dasha_active = _dasha_activates(ctx, [12,9,3])
    pct = _pct(50, total, 8 if dasha_active else 0)

    foreign_strong = rahu.get("house") in (12,9,7,1) or "Rahu" in h12_occ
    visa_ok = lord_9 == "Jupiter" or l9d.get("str_score",0)>=1 or "Jupiter" in h9_occ

    sign4=ctx["house_signs"][4]
    DIR_MAP={"Mesha":"East","Vrishabha":"South","Mithuna":"North","Karka":"North-West",
             "Simha":"East","Kanya":"South","Tula":"West","Vrischika":"North",
             "Dhanu":"North-East","Makara":"South","Kumbha":"West","Meena":"North-East"}
    direction = DIR_MAP.get(sign4,"Variable direction")

    timing  = _timing_windows(ctx, [12,9,3], "travel")
    remedies= _build_remedies(ctx, ["Rahu"] if not foreign_strong else [], "travel")

    return {
        "domain":"Travel & Foreign","icon":"✈","score":pct,
        "foreign_settlement":foreign_strong,"visa_success":visa_ok,
        "direction":direction,
        "overseas_career":"Strong overseas career potential" if rahu.get("house")==10 else "Domestic career more prominent",
        "twelfth_lord":f"{lord_12} in {_ordinal(l12d.get('house',0))}H — {l12d.get('strength','')}",
        "rahu_position":f"Rahu in {_ordinal(rahu.get('house',1))}H — key foreign indicator",
        "dasha_active":dasha_active,"timing":timing,"remedies":remedies,
        "analysis":f"12th house (foreign lands) ruled by {lord_12} in {_ordinal(l12d.get('house',1))} house. Rahu in {_ordinal(rahu.get('house',1))} house. Foreign settlement: {'strongly indicated' if foreign_strong else 'less prominent'}. Best direction: {direction}. Travel window: {timing['best_window']}.",
    }


_travel = analyse_travel
```


#### Domain Evaluator: `wealth.py`
**Path:** `astro-platform/backend/modules/prediction/domains/wealth.py`
```python
"""Wealth & Finance Domain Evaluator."""

from modules.prediction.scoring import (
    _score_planets_in_houses, _score_house_lord, _dasha_activates,
    _yoga_present, _pct, _ordinal
)
from modules.prediction.remedies import _timing_windows, _build_remedies


def analyse_wealth(ctx: dict) -> dict:
    pm = ctx["planet_map"]
    hl = ctx["house_lords"]

    jupiter = pm.get("Jupiter",{})
    venus   = pm.get("Venus",{})
    moon    = pm.get("Moon",{})

    lord_2  = hl[2]; l2d = pm.get(lord_2,{})
    lord_11 = hl[11]; l11d = pm.get(lord_11,{})
    h2_occ  = [p for p,d in pm.items() if d["house"]==2]
    h11_occ = [p for p,d in pm.items() if d["house"]==11]

    base   = _score_planets_in_houses(ctx, [2,11,9,5])
    l2s    = _score_house_lord(ctx, 2)
    l11s   = _score_house_lord(ctx, 11)
    j_sc   = jupiter.get("str_score",0) + (2 if jupiter.get("house") in (2,11,5,9) else 0)
    total  = base + l2s + l11s + j_sc

    dasha_active = _dasha_activates(ctx, [2,11,5,9])
    pct = _pct(50, total, 10 if dasha_active else 0)

    dhana_yogas = _yoga_present(ctx, ["Dhana","Lakshmi","Kubera","Wealth"])

    sign11 = ctx["house_signs"][11]
    SOURCE_MAP = {
        "Mesha":"business, real estate, initiative-driven income",
        "Vrishabha":"banking, agriculture, luxury trade, accumulation",
        "Mithuna":"communication, media, commission, intellectual work",
        "Karka":"real estate, food industry, family business, water",
        "Simha":"government, leadership, speculation, creative work",
        "Kanya":"service industry, health, detailed analytical work",
        "Tula":"partnerships, trade, legal, design, negotiation",
        "Vrischika":"research, insurance, inheritance, occult",
        "Dhanu":"education, exports, foreign income, law",
        "Makara":"professional services, construction, government",
        "Kumbha":"technology, NGO, innovation, irregular but large gains",
        "Meena":"spiritual services, medicine, arts, sea trade",
    }
    income_sources = SOURCE_MAP.get(sign11,"varied income streams")

    h8_occ  = [p for p,d in pm.items() if d["house"]==8]
    sudden_gain = "Lottery/sudden gains potential" if "Rahu" in h8_occ or "Jupiter" in h8_occ \
                  else "Moderate unexpected income possible" if "Moon" in h8_occ \
                  else "Earned wealth more prominent than windfalls"

    h6_saturn = pm.get("Saturn",{}).get("house") == 6
    debt_risk  = "6th house alignment indicates prudent budget management. Maintain disciplined finances and structured investments." if h6_saturn \
                 else "No strong debt indicators in current planetary configuration."

    timing   = _timing_windows(ctx, [2,11,9], "wealth")
    remedies = _build_remedies(ctx, ["Jupiter","Venus"] if j_sc < 0 else (["Jupiter"] if j_sc==0 else []), "wealth")

    return {
        "domain":"Wealth & Finance","icon":"₹","score":pct,
        "dhana_yogas":dhana_yogas,"income_sources":income_sources,
        "sudden_gain":sudden_gain,"debt_risk":debt_risk,
        "second_lord":f"{lord_2} in {_ordinal(l2d.get('house',0))}H — {l2d.get('strength','')}",
        "eleventh_lord":f"{lord_11} in {_ordinal(l11d.get('house',0))}H — {l11d.get('strength','')}",
        "h2_planets":h2_occ,"h11_planets":h11_occ,
        "dasha_active":dasha_active,"timing":timing,"remedies":remedies,
        "analysis":_wealth_narrative(ctx,pct,dhana_yogas,income_sources,timing),
    }


def _wealth_narrative(ctx,pct,yogas,sources,timing):
    md=ctx["mahadasha"]; ad=ctx["antardasha"]
    j=ctx["planet_map"].get("Jupiter",{})
    parts=[]
    parts.append(f"Jupiter, the primary wealth karaka, is placed in the {_ordinal(j.get('house',1))} house in {j.get('sign','')} — {j.get('strength','')}.")
    parts.append(f"Primary income sources: {sources}.")
    if yogas:
        parts.append(f"Dhana Yogas present: {', '.join(yogas)} — strong wealth accumulation potential.")
    parts.append(f"{md}/{ad} dasha {'is actively triggering' if timing['dasha_active'] else 'does not directly trigger'} wealth houses. Best financial window: {timing['best_window']}.")
    return " ".join(parts)


_wealth = analyse_wealth
```


### r) modules/narrative/*.py

#### Narrative Component: `api.py`
**Path:** `astro-platform/backend/modules/narrative/api.py`
```python
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
import asyncio

from modules.narrative.schemas import (
    NarrativeRequest,
    NarrativeResponse,
    ChatRequest,
    ChatResponse,
    NarrativeJobRequest,
    NarrativeJobStatus,
)
from modules.narrative.engine import NarrativeEngine
from modules.narrative.chat import ChatService
from modules.narrative.jobs import create_job, get_job
from shared.cache.keys import compute_input_hash
from shared.logging.logger import get_logger

logger = get_logger("modules.narrative.api")
router = APIRouter(prefix="/api/narrative", tags=["narrative"])


class NarrativeService:
    def generate(self, req: NarrativeRequest) -> NarrativeResponse:
        result = NarrativeEngine.generate_predictions(
            year=req.year,
            month=req.month,
            day=req.day,
            hour=req.hour,
            city=req.city,
            lang=req.lang
        )
        return NarrativeResponse(**result)

    async def generate_async(self, req: NarrativeRequest) -> str:
        input_hash = compute_input_hash(req.dict())
        job_req = NarrativeJobRequest(
            input_hash=input_hash,
            year=req.year,
            month=req.month,
            day=req.day,
            hour=req.hour,
            city=req.city,
            lang=req.lang,
        )
        return await create_job(job_req)

    async def get_status(self, job_id: str) -> NarrativeJobStatus:
        st = await get_job(job_id)
        if not st:
            raise HTTPException(status_code=404, detail="Narrative job not found.")
        return st

    def chat(self, req: ChatRequest) -> ChatResponse:
        result = ChatService.answer_kundali_chat(
            message=req.message,
            chart=req.chart,
            lang=req.lang
        )
        return ChatResponse(**result)


@router.post("/generate", response_model=NarrativeResponse)
async def generate_narrative(req: NarrativeRequest, async_job: bool = Query(False, alias="async")):
    try:
        service = NarrativeService()
        if async_job:
            job_id = await service.generate_async(req)
            return {"job_id": job_id, "status": "queued"}
        return service.generate(req)
    except Exception as e:
        logger.error(f"Narrative generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Narrative generation failed.")


@router.get("/{job_id}", response_model=NarrativeJobStatus)
async def get_narrative_job_status(job_id: str):
    service = NarrativeService()
    return await service.get_status(job_id)


@router.get("/{job_id}/stream")
async def stream_narrative_job(job_id: str):
    """Server-Sent Events (SSE) streaming endpoint for job progress."""
    async def event_generator():
        service = NarrativeService()
        while True:
            st = await service.get_status(job_id)
            payload = st.model_dump_json() if hasattr(st, "model_dump_json") else st.json()
            yield f"data: {payload}\n\n"
            if st.status in ("completed", "failed"):
                break
            await asyncio.sleep(1)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/chat", response_model=ChatResponse)
def chat_narrative(req: ChatRequest):
    try:
        service = NarrativeService()
        return service.chat(req)
    except Exception as e:
        logger.error(f"Chat service failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Chat engine failed.")
```


#### Narrative Component: `chat.py`
**Path:** `astro-platform/backend/modules/narrative/chat.py`
```python
"""Vedic Astrology Smart Chat Service answering user queries from Natal Chart data with i18n support."""

import re
from shared.veda.zodiac import SIGNS as SIGNS_SK, SIGN_LORDS
from shared.i18n.translation import get_translation, translate_astrology_term
from modules.narrative.llm_client import ask_llm
from modules.narrative.prompt_builder import build_chat_prompt

DASHA_YRS = dict(Ketu=7, Venus=20, Sun=6, Moon=10, Mars=7, Rahu=18, Jupiter=16, Saturn=19, Mercury=17)
DASHA_SEQ = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]


class ChatService:
    @staticmethod
    def answer_general_chat(message: str, chart: dict | None, lang: str = "en") -> str:
        """Answer chat questions utilizing chart context if available in user's requested language."""
        if not chart:
            return get_translation(
                "kundali.form.title",
                lang,
                default="Please generate your birth chart or Kundali first so I can analyze your planetary positions.",
            )

        prompt = build_chat_prompt(chart, message, lang=lang)
        return ask_llm(prompt)

    @staticmethod
    def answer_kundali_chat(message: str, chart: dict, lang: str = "en") -> dict:
        """Smart rules + context aware Kundali chat engine answering life domain questions."""
        if not chart:
            return {
                "reply": get_translation(
                    "common.error",
                    lang,
                    default="Please generate your Kundali first before asking questions.",
                ),
                "topic": "error",
            }

        msg = message.strip().lower()
        topic = ChatService._detect_topic(msg)

        planets_list = chart.get("planets", []) if isinstance(chart, dict) else []
        pm = {p["name"]: p for p in planets_list if "name" in p}
        lagna = chart.get("lagna", "Aries") if isinstance(chart, dict) else "Aries"
        md = chart.get("mahadasha", "Jupiter") if isinstance(chart, dict) else "Jupiter"
        ad = chart.get("antardasha", "Jupiter") if isinstance(chart, dict) else "Jupiter"
        bal = chart.get("dasha_balance", "5.0 years") if isinstance(chart, dict) else "5.0 years"
        yogas = [y.get("name", "") for y in chart.get("yogas", []) if y.get("present")] if isinstance(chart, dict) else []
        doshas = [d.get("name", "") for d in chart.get("doshas", []) if d.get("present")] if isinstance(chart, dict) else []

        if topic == "career":
            core = ChatService._answer_career(pm, lagna, md, ad, bal)
        elif topic == "marriage":
            core = ChatService._answer_marriage(pm, lagna, md, ad, bal)
        elif topic == "wealth":
            core = ChatService._answer_wealth(pm, lagna, md, ad, bal)
        elif topic == "health":
            core = ChatService._answer_health(pm, lagna)
        elif topic == "foreign":
            core = ChatService._answer_foreign(pm, lagna, md)
        elif topic == "timing":
            core = f"**Current Dasha Period**: **{md}/{ad}** (Balance remaining: {bal}).\n\nPlanetary energies are primarily directed by {md}, activating associated house themes in your chart."
        elif topic == "dosha":
            core = f"**Active Doshas Detected**: {', '.join(doshas) if doshas else 'No severe doshas detected.'}\n\n**Key Yogas**: {', '.join(yogas[:3]) if yogas else 'Standard planetary configurations.'}"
        elif topic == "remedy":
            core = ChatService._answer_remedy(pm, md)
        else:
            ai_reply = ask_llm(build_chat_prompt(chart, message, lang=lang))
            core = ai_reply if ai_reply else (
                f"**Chart Summary**: Lagna: **{translate_astrology_term(lagna, lang)}** | Mahadasha: **{md}/{ad}**.\n"
                f"Active Yogas: {', '.join(yogas[:3]) if yogas else 'None'}. "
                f"Please ask about career, marriage, wealth, health, or remedies for specific guidance."
            )

        return {
            "reply": core,
            "topic": topic,
            "chart_context": {
                "lagna": translate_astrology_term(lagna, lang),
                "mahadasha": md,
                "antardasha": ad,
                "dasha_balance": bal,
                "active_yogas": yogas[:4],
                "active_doshas": doshas[:3],
            },
        }

    @staticmethod
    def _detect_topic(msg: str) -> str:
        if any(w in msg for w in ["job", "career", "work", "business", "promotion", "profession"]):
            return "career"
        if any(w in msg for w in ["marr", "husband", "wife", "spouse", "partner", "love", "wedding"]):
            return "marriage"
        if any(w in msg for w in ["wealth", "money", "rich", "income", "finance", "earn"]):
            return "wealth"
        if any(w in msg for w in ["health", "sick", "disease", "illness", "body", "surgery"]):
            return "health"
        if any(w in msg for w in ["foreign", "abroad", "visa", "settle", "overseas", "travel"]):
            return "foreign"
        if any(w in msg for w in ["dasha", "timing", "period", "when", "year"]):
            return "timing"
        if any(w in msg for w in ["dosha", "mangal", "sade", "kaal sarp", "pitru"]):
            return "dosha"
        if any(w in msg for w in ["remedy", "gemstone", "mantra", "puja", "fast", "ring", "stone"]):
            return "remedy"
        return "general"

    @staticmethod
    def _house_of(pm: dict, name: str) -> int:
        p = pm.get(name, {})
        h = p.get("house", 1)
        if isinstance(h, int):
            return h
        try:
            return int(str(h).split("/")[0])
        except (ValueError, TypeError):
            return 1

    @staticmethod
    def _answer_career(pm: dict, lagna: str, md: str, ad: str, bal: str) -> str:
        lagna_idx = SIGNS_SK.index(lagna) if lagna in SIGNS_SK else 0
        lord_10 = SIGN_LORDS.get(SIGNS_SK[(lagna_idx + 9) % 12], "Mars")
        sign_10 = SIGNS_SK[(lagna_idx + 9) % 12]
        l10_h = ChatService._house_of(pm, lord_10)
        l10_str = pm.get(lord_10, {}).get("strength", "Neutral")

        return (
            f"**10th House (Career & Status)** is in **{sign_10}**, ruled by **{lord_10}**.\n"
            f"• **{lord_10}** is placed in house {l10_h} with **{l10_str}** dignity.\n"
            f"• Current operating Dasha: **{md}/{ad}**.\n"
            f"• Career growth accelerates when taking initiative in strategic domains aligned with {lord_10}'s qualities."
        )

    @staticmethod
    def _answer_marriage(pm: dict, lagna: str, md: str, ad: str, bal: str) -> str:
        lagna_idx = SIGNS_SK.index(lagna) if lagna in SIGNS_SK else 0
        lord_7 = SIGN_LORDS.get(SIGNS_SK[(lagna_idx + 6) % 12], "Venus")
        sign_7 = SIGNS_SK[(lagna_idx + 6) % 12]
        l7_h = ChatService._house_of(pm, lord_7)
        l7_str = pm.get(lord_7, {}).get("strength", "Neutral")
        venus = pm.get("Venus", {})
        mars_h = ChatService._house_of(pm, "Mars")
        mangal = mars_h in (1, 2, 4, 7, 8, 12)

        return (
            f"**7th House (Marriage & Partnership)** is in **{sign_7}**, ruled by **{lord_7}**.\n"
            f"• **{lord_7}** is situated in house {l7_h} ({l7_str}).\n"
            f"• **Venus (Kalatra Karaka)** is placed in {venus.get('sign', '')} in house {ChatService._house_of(pm, 'Venus')}.\n"
            f"• {'⚠️ **Mangal Dosha** present (Mars in house ' + str(mars_h) + ') — matched compatibility advised.' if mangal else '✅ No severe Mangal Dosha afflictions to the 7th house.'}\n"
            f"• Current Dasha: **{md}/{ad}** supports constructive relational alignment."
        )

    @staticmethod
    def _answer_wealth(pm: dict, lagna: str, md: str, ad: str, bal: str) -> str:
        lagna_idx = SIGNS_SK.index(lagna) if lagna in SIGNS_SK else 0
        lord_2 = SIGN_LORDS.get(SIGNS_SK[(lagna_idx + 1) % 12], "Venus")
        lord_11 = SIGN_LORDS.get(SIGNS_SK[(lagna_idx + 10) % 12], "Jupiter")
        jup_h = ChatService._house_of(pm, "Jupiter")
        jup_str = pm.get("Jupiter", {}).get("strength", "Neutral")

        return (
            f"**Financial Indicators (2nd & 11th Houses)**:\n"
            f"• 2nd Lord (Accumulated Wealth): **{lord_2}** in house {ChatService._house_of(pm, lord_2)}.\n"
            f"• 11th Lord (Gains & Income): **{lord_11}** in house {ChatService._house_of(pm, lord_11)}.\n"
            f"• **Jupiter (Dhana Karaka)** is placed in house {jup_h} ({jup_str}).\n"
            f"• Steady accumulation through disciplined value-oriented investments is favored."
        )

    @staticmethod
    def _answer_health(pm: dict, lagna: str) -> str:
        lagna_idx = SIGNS_SK.index(lagna) if lagna in SIGNS_SK else 0
        lord_1 = SIGN_LORDS.get(SIGNS_SK[lagna_idx], "Mars")
        l1_h = ChatService._house_of(pm, lord_1)
        l1_str = pm.get(lord_1, {}).get("strength", "Neutral")
        sun_str = pm.get("Sun", {}).get("strength", "Neutral")

        return (
            f"**Vitality & Health (1st & 6th Houses)**:\n"
            f"• Lagna Lord **{lord_1}** is in house {l1_h} ({l1_str}) governing physical stamina.\n"
            f"• Sun (Vitality indicator) is in house {ChatService._house_of(pm, 'Sun')} ({sun_str}).\n"
            f"• Maintain balanced Ayurvedic lifestyle and regular physical activity to optimize planetary energies."
        )

    @staticmethod
    def _answer_foreign(pm: dict, lagna: str, md: str) -> str:
        rahu_h = ChatService._house_of(pm, "Rahu")
        foreign_strong = rahu_h in (1, 7, 9, 12)
        return (
            f"**Foreign Travel & Relocation (9th & 12th Houses)**:\n"
            f"• Rahu is placed in house {rahu_h} — {'Strong indicator for foreign opportunities and overseas travel.' if foreign_strong else 'Travel indicated for specific educational or professional assignments.'}\n"
            f"• Favorable periods activate during Rahu, 9th lord, or 12th lord sub-dashas."
        )

    @staticmethod
    def _answer_remedy(pm: dict, md: str) -> str:
        gems = {
            "Sun": "Ruby", "Moon": "Pearl", "Mars": "Red Coral", "Mercury": "Emerald",
            "Jupiter": "Yellow Sapphire", "Venus": "Diamond / White Topaz", "Saturn": "Blue Sapphire",
            "Rahu": "Hessonite", "Ketu": "Cat's Eye"
        }
        return (
            f"**Astrological Remedies & Strengthening**:\n"
            f"• Current Mahadasha Lord is **{md}**.\n"
            f"• Primary Gemstone recommendation for {md}: **{gems.get(md, 'Consult Astrologer')}** (wear after proper Energization).\n"
            f"• Daily Mantra: Recite the planetary mantra for {md} 108 times at sunrise for mental clarity and protection."
        )


chat_service = ChatService()
```


#### Narrative Component: `engine.py`
**Path:** `astro-platform/backend/modules/narrative/engine.py`
```python
"""AI Prediction Orchestrator for Marriage, Career, and Life Domains."""

from modules.kundali.varga import generate_full_chart
from modules.kundali.cities import get_city

from modules.narrative.llm_client import ask_llm
from modules.narrative.prompt_builder import build_prediction_prompt


class NarrativeEngine:
    @staticmethod
    def generate_predictions(
        year: int, month: int, day: int, hour: float, city: str = "Pune", lang: str = "en"
    ) -> dict:
        """Generate full natal chart and synthesize localized AI marriage & career predictions."""
        coords = get_city(city)
        if coords is None:
            lat, lon = 18.5204, 73.8567
        else:
            lat, lon, _ = coords

        chart = generate_full_chart(year, month, day, hour, lat, lon)

        marriage_prompt = build_prediction_prompt(chart, "marriage", lang=lang)
        career_prompt = build_prediction_prompt(chart, "career", lang=lang)

        marriage_output = ask_llm(marriage_prompt)
        career_output = ask_llm(career_prompt)

        return {
            "chart": chart,
            "marriage_prediction": marriage_output,
            "career_prediction": career_output,
            "raw_marriage_score": chart.get("marriage_prediction", {}).get("score", 75),
            "raw_career_score": chart.get("career_prediction", {}).get("score", 78),
        }


prediction_service = NarrativeEngine()
```


#### Narrative Component: `jobs.py`
**Path:** `astro-platform/backend/modules/narrative/jobs.py`
```python
"""Job store for async narrative generation tasks."""

import hashlib
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any

from shared.cache.redis_client import CacheService
from shared.queue.redis_queue import JobStatus, default_queue
from modules.narrative.schemas import NarrativeJobRequest, NarrativeJobStatus, NarrativeJobResult

logger = logging.getLogger("modules.narrative.jobs")
JOB_TTL_SECONDS = 86400  # 24 hours


def compute_job_id(input_hash: str, engine_version: str = "2.0.0", prompt_version: str = "1.0.0") -> str:
    """Deterministic 16-character job ID from input hash and engine/prompt versions."""
    raw = f"{input_hash}:{engine_version}:{prompt_version}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


async def create_job(req: NarrativeJobRequest) -> str:
    """Create or return existing narrative job state in Redis."""
    job_id = compute_job_id(req.input_hash, req.engine_version, req.prompt_version)
    state_key = f"narrative:job:{job_id}"

    # Check if job already exists
    existing = CacheService.get(state_key)
    if existing:
        if isinstance(existing, str):
            try:
                existing = json.loads(existing)
            except Exception:
                existing = None

        if existing and isinstance(existing, dict):
            logger.info(f"Narrative job {job_id} already exists with status: {existing.get('status')}")
            return job_id

    now_iso = datetime.utcnow().isoformat()
    req_dict = req.model_dump() if hasattr(req, "model_dump") else req.dict()
    job_state = {
        "job_id": job_id,
        "status": JobStatus.QUEUED,
        "input_hash": req.input_hash,
        "language": req.lang,
        "created_at": now_iso,
        "request": req_dict,
        "result": None,
        "error": None,
    }

    CacheService.set(state_key, json.dumps(job_state), ttl=JOB_TTL_SECONDS)
    await default_queue.enqueue(job_name="process_narrative", payload=job_state["request"], job_id=job_id)
    return job_id


async def get_job(job_id: str) -> Optional[NarrativeJobStatus]:
    """Get job status and result from Redis store."""
    state_key = f"narrative:job:{job_id}"
    raw = CacheService.get(state_key)
    if not raw:
        return None
    if isinstance(raw, str):
        data = json.loads(raw)
    else:
        data = raw

    res_obj = NarrativeJobResult(**data["result"]) if data.get("result") else None
    input_hash = data.get("input_hash") or (data.get("request", {}).get("input_hash") if isinstance(data.get("request"), dict) else "unknown")
    created_at = data.get("created_at") or datetime.utcnow().isoformat()
    return NarrativeJobStatus(
        job_id=data["job_id"],
        status=data["status"],
        input_hash=input_hash,
        language=data.get("language", "en"),
        created_at=created_at,
        result=res_obj,
        error=data.get("error"),
    )


async def mark_running(job_id: str) -> None:
    """Update job state to RUNNING."""
    await _update_job_status(job_id, JobStatus.RUNNING)


async def mark_completed(job_id: str, result: NarrativeJobResult) -> None:
    """Update job state to COMPLETED with payload."""
    await _update_job_status(job_id, JobStatus.COMPLETED, result=result.dict())


async def mark_failed(job_id: str, error_msg: str) -> None:
    """Update job state to FAILED with error details."""
    await _update_job_status(job_id, JobStatus.FAILED, error=error_msg)


async def _update_job_status(job_id: str, status: str, result: Optional[Dict[str, Any]] = None, error: Optional[str] = None) -> None:
    state_key = f"narrative:job:{job_id}"
    raw = CacheService.get(state_key)
    if not raw:
        return
    data = json.loads(raw) if isinstance(raw, str) else raw
    data["status"] = status
    if result is not None:
        data["result"] = result
    if error is not None:
        data["error"] = error
    CacheService.set(state_key, json.dumps(data), ttl=JOB_TTL_SECONDS)
```


#### Narrative Component: `llm_client.py`
**Path:** `astro-platform/backend/modules/narrative/llm_client.py`
```python
"""Unified LLM client supporting Ollama and OpenAI with graceful rule-based fallback."""

import json
import logging
import requests

from shared.config.settings import settings

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self):
        self.ollama_url = f"{getattr(settings, 'ollama_base_url', 'http://localhost:11434').rstrip('/')}/api/generate"
        self.model = getattr(settings, 'ollama_model', 'mistral')
        self.openai_key = getattr(settings, 'openai_api_key', None)

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """
        Send a prompt to Ollama or OpenAI with automatic fallback to structured astrological synthesis.
        """
        # 1. Try Ollama if running
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.5,
                    "num_predict": 250,
                },
            }
            if system_prompt:
                payload["system"] = system_prompt

            resp = requests.post(self.ollama_url, json=payload, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if "response" in data and data["response"].strip():
                    return data["response"].strip()
        except Exception as e:
            logger.debug(f"Ollama not available: {e}")

        # 2. Try OpenAI if API key configured
        if self.openai_key:
            try:
                headers = {
                    "Authorization": f"Bearer {self.openai_key}",
                    "Content-Type": "application/json",
                }
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})

                openai_payload = {
                    "model": "gpt-3.5-turbo",
                    "messages": messages,
                    "max_tokens": 250,
                    "temperature": 0.5,
                }
                resp = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=openai_payload,
                    timeout=8,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    return data["choices"][0]["message"]["content"].strip()
            except Exception as e:
                logger.debug(f"OpenAI call failed: {e}")

        # 3. Fallback: Intelligent structured synthesis
        return self._generate_fallback_response(prompt)

    def _generate_fallback_response(self, prompt: str) -> str:
        """Produce a coherent astrological analysis when external LLMs are unreachable."""
        prompt_lower = prompt.lower()
        if "marriage" in prompt_lower:
            return (
                "Based on the Vedic 7th house and Venus karaka evaluation, your chart indicates meaningful "
                "relational growth. Planetary alignments suggest auspicious timing during favorable Dasha sub-periods. "
                "Cultivating emotional patience and shared spiritual values will create lasting marital harmony."
            )
        elif "career" in prompt_lower or "job" in prompt_lower:
            return (
                "Your 10th house and planetary dignities highlight strong executive and strategic capability. "
                "Current planetary transits support career expansion and recognition for sustained effort. "
                "Focus on building high-value skills and strategic networking for maximum professional advancement."
            )
        elif "wealth" in prompt_lower or "finance" in prompt_lower:
            return (
                "2nd and 11th house configurations indicate steady financial accumulation. Jupiter's benevolent "
                "influence supports ethical enterprise and long-term investments over speculative risks."
            )
        return (
            "The cosmic alignments in your natal chart reveal strong foundational vitality and purposeful direction. "
            "Aligning your daily actions with the prevailing Mahadasha period will unlock favorable karmic results."
        )


llm_client = LLMClient()


def ask_llm(prompt: str, system_prompt: str | None = None) -> str:
    """Convenience functional wrapper for asking LLM."""
    return llm_client.generate(prompt, system_prompt)
```


#### Narrative Component: `prompt_builder.py`
**Path:** `astro-platform/backend/modules/narrative/prompt_builder.py`
```python
"""Token-optimized astrological prompt formatting utilities with multi-language (i18n) support."""

from shared.i18n.translation import SUPPORTED_LANGUAGES, translate_astrology_term


def build_prediction_prompt(chart: dict, prediction_type: str, lang: str = "en") -> str:
    """Build a controlled, short-format astrology prediction prompt localized per requested language."""
    prediction_data = chart.get(f"{prediction_type}_prediction", {})
    score = prediction_data.get("score", 75)
    level = prediction_data.get("level", "Moderate")
    reasons = prediction_data.get("reasons", [])

    short_reasons = reasons[:2]
    formatted_reasons = ", ".join(short_reasons) if short_reasons else "Planetary positions and Dasha activation"

    lang_name = SUPPORTED_LANGUAGES.get(lang.lower(), "English") if isinstance(SUPPORTED_LANGUAGES, dict) else "English"

    prompt = f"""
You are AstroAI, a precise and professional Vedic astrologer.

Generate a short astrology summary based on this chart calculation:
- Prediction Type: {prediction_type.capitalize()}
- Score: {score}/100
- Level: {level}
- Key Astrological Factors: {formatted_reasons}

Rules:
- Maximum 4-5 sentences.
- Mention score and level clearly.
- Highlight 1-2 key astrological factors.
- End with a constructive, actionable recommendation.
- Avoid fatalistic language.
- MANDATORY: Write your entire response strictly in {lang_name} (language code: {lang}).
"""
    return prompt.strip()


def build_chat_prompt(chart: dict, message: str, lang: str = "en") -> str:
    """Build a contextual prompt answering user life questions localized per requested language."""
    basic = chart.get("basic_details", {}) if isinstance(chart, dict) else {}
    lagna = translate_astrology_term(basic.get("lagna", "Aries"), lang)
    dasha = chart.get("dasha", {}).get("current_mahadasha", "Jupiter") if isinstance(chart, dict) else "Jupiter"
    yogas = chart.get("advanced_yogas", []) if isinstance(chart, dict) else []

    lang_name = SUPPORTED_LANGUAGES.get(lang.lower(), "English") if isinstance(SUPPORTED_LANGUAGES, dict) else "English"

    prompt = f"""
You are AstroAI, an expert Vedic astrologer.
Answer the user's question using their birth chart context:
- Lagna: {lagna}
- Current Mahadasha: {dasha}
- Active Yogas: {', '.join(yogas[:3]) if yogas else 'None'}

User Question: {message}

Instructions:
- Provide a clear, empowering, and accurate astrological interpretation.
- Reference house and planetary principles relevant to their question.
- Keep response under 120 words.
- MANDATORY: Write your entire response strictly in {lang_name} (language code: {lang}).
"""
    return prompt.strip()
```


#### Narrative Component: `schemas.py`
**Path:** `astro-platform/backend/modules/narrative/schemas.py`
```python
"""Pydantic Schemas for Narrative Module."""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class NarrativeRequest(BaseModel):
    year: int = Field(..., example=1990)
    month: int = Field(..., example=5)
    day: int = Field(..., example=15)
    hour: float = Field(..., example=14.5)
    city: str = Field("Pune", example="Pune")
    lang: str = Field("en", example="en")


class NarrativeResponse(BaseModel):
    chart: Dict[str, Any]
    marriage_prediction: str
    career_prediction: str
    raw_marriage_score: int
    raw_career_score: int


class ChatRequest(BaseModel):
    message: str
    chart: Optional[Dict[str, Any]] = None
    lang: str = "en"


class ChatResponse(BaseModel):
    reply: str
    topic: Optional[str] = "general"
    chart_context: Optional[Dict[str, Any]] = None


class NarrativeJobRequest(BaseModel):
    input_hash: str
    year: int
    month: int
    day: int
    hour: float
    city: str = "Pune"
    lang: str = "en"
    engine_version: str = "2.0.0"
    prompt_version: str = "1.0.0"


class NarrativeJobResult(BaseModel):
    marriage_prediction: Optional[str] = None
    career_prediction: Optional[str] = None
    raw_marriage_score: Optional[int] = None
    raw_career_score: Optional[int] = None
    chart: Optional[Dict[str, Any]] = None


class NarrativeJobStatus(BaseModel):
    job_id: str
    status: str  # queued, running, completed, failed
    input_hash: str
    language: str = "en"
    created_at: str
    result: Optional[NarrativeJobResult] = None
    error: Optional[str] = None
```


## 3. DATA MODELS & SCHEMAS (exact)

### 3.1 SQLAlchemy ORM Models

#### User & Auth Models (`modules/auth/models.py`)
```python
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from shared.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    preferred_language = Column(String(10), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)

    profile = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    activities = relationship(
        "UserActivity",
        back_populates="user",
        passive_deletes=True,
    )
    feedback_items = relationship(
        "Feedback",
        back_populates="user",
        passive_deletes=True,
    )


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    phone = Column(String(32), nullable=True)
    birth_date = Column(String(20), nullable=True)
    birth_time = Column(String(20), nullable=True)
    birth_city = Column(String(120), nullable=True)
    zodiac_sign = Column(String(40), nullable=True)
    notes = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(120), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserActivity(Base):
    __tablename__ = "user_activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    action = Column(String(80), nullable=False)
    details = Column(Text, nullable=True)
    ip_address = Column(String(64), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="activities")
```

#### Blog ORM Model (`modules/blog/models.py`)
```python
"""Blog Post ORM Model."""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from shared.db import Base
from shared.timezone import now_ist


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(250), nullable=False)
    slug = Column(String(250), unique=True, index=True, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    language = Column(String(10), default="en", index=True)
    tags = Column(JSON, nullable=True)
    author = Column(String(100), default="Astro AI")
    created_at = Column(DateTime(timezone=True), default=now_ist)


Blog = BlogPost
```

#### Feedback ORM Model (`modules/feedback/models.py`)
```python
"""Feedback and Activity ORM Models."""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from shared.db import Base
from shared.timezone import now_ist


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    module = Column(String(50), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=now_ist)

    user = relationship("modules.auth.models.User", back_populates="feedback_items")



class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime(timezone=True), default=now_ist)
```

### 3.2 Pydantic Validation & Serialization Schemas

#### Kundali Schemas (`modules/kundali/schemas.py`)
```python
from typing import Any
from pydantic import BaseModel, Field


class BirthData(BaseModel):
    name: str = "Seeker"
    year: int = Field(..., ge=1900, le=2100)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    hour: float = Field(..., ge=0, lt=24)
    place: str = "Unknown"


class KundaliRequest(BaseModel):
    year: int = Field(..., ge=1900, le=2100)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    hour: int = Field(..., ge=0, le=23)
    minute: int = Field(..., ge=0, le=59)
    city: str = Field(..., min_length=1)


class KundaliChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    chart: dict[str, Any]


class PlanetDetail(BaseModel):
    name: str
    sign: str
    degree: str
    degree_decimal: float
    house: int
    nakshatra: str
    pada: int
    navamsa: str
    strength: str
    retrograde: bool


class KundaliResponse(BaseModel):
    lagna: str
    lagna_degree: str
    lagna_degree_decimal: float
    lagna_nakshatra: str
    lagna_pada: int
    houses: dict[int, list[str]]
    d9_houses: dict[int, list[str]]
    d9_lagna: str
    planets: list[PlanetDetail]
    tithi_number: int
    tithi_name: str
    paksha: str
    nakshatra: str
    nakshatra_pada: int
    yoga_name: str
    karana_name: str
    ayanamsa: float
    jd: float
    mahadasha: str
    dasha_balance: str
    antardasha: str
    antardasha_list: list[dict[str, Any]]
    scores: dict[str, int]
    yogas: list[dict[str, Any]]
    doshas: list[dict[str, Any]]
```

#### Prediction & Domain Schemas (`modules/prediction/schemas.py`)
```python
"""Pydantic Schemas for Prediction & Life Domain Module."""

from datetime import date
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    year: int = Field(..., ge=1900, le=2100)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    hour: float = Field(..., ge=0, lt=24)
    city: Optional[str] = "Pune"


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)


class DomainRequest(BaseModel):
    year: int = Field(..., ge=1900, le=2100)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    hour: int = Field(..., ge=0, le=23)
    minute: int = Field(..., ge=0, le=59)
    city: str = Field(..., min_length=1)


class TimingWindow(BaseModel):
    start_date: date
    end_date: date
    peak_date: date
    peak_score: float
    confidence: str
    mahadasha: str
    antardasha: str
    pratyantardasha: str
    reasons: list[str]
    drivers: list[str]
    sub_scores: dict


class TimingBlock(BaseModel):
    timing_windows: list[TimingWindow]
    peak_window: Optional[TimingWindow]
    next_12_months_summary: str
    methodology: str
    engine_version: str


class PredictionResponse(BaseModel):
    engine_version: str
    input_hash: str
    lagna: str
    mahadasha: str
    antardasha: str
    yogas_detected: list
    domains: Dict[str, Any]
    disclaimer: Optional[str] = None
```

#### Panchang Schemas (`modules/panchang/schemas.py`)
```python
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class PanchangRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    city: Optional[str] = Field(default="Pune")
    date_str: Optional[str] = None  # Format YYYY-MM-DD
    lat: Optional[float] = None
    lon: Optional[float] = None
    timezone: Optional[str] = None
    user_rashi: Optional[str] = None
    user_nakshatra: Optional[str] = None


class ProfileResolveRequest(BaseModel):
    """Resolve natal Moon sign (Rashi) and Nakshatra from birth details."""
    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None
    birth_date: str  # YYYY-MM-DD
    birth_time: Optional[str] = None  # HH:MM (24h)
    birth_place: Optional[str] = Field(default="Pune")
    lat: Optional[float] = None
    lon: Optional[float] = None


class DecisionRequest(BaseModel):
    """Interactive Decision Assistant request."""
    model_config = ConfigDict(extra="allow")

    activity: str = Field(..., description="Activity type: travel, investment, meeting, spiritual, purchase")
    city: Optional[str] = Field(default="Pune")
    user_rashi: Optional[str] = None
    user_nakshatra: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None


class PanchangResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    date_str: Optional[str] = None
    city: str
    lat: Optional[float] = None
    lon: Optional[float] = None
    resolved_timezone: Optional[str] = "Asia/Kolkata"
    local_datetime: Optional[str] = None
    mode: Optional[str] = "general"  # "general" | "personalized"

    tithi: Optional[str] = None
    tithi_name: Optional[str] = None
    paksha: Optional[str] = None
    tithi_progress: Optional[float] = None
    tithi_end: Optional[str] = None

    nakshatra: Optional[str] = None
    nakshatra_pada: Optional[int] = None
    nakshatra_end: Optional[str] = None

    yoga: Optional[str] = None
    yoga_name: Optional[str] = None
    yoga_end: Optional[str] = None

    karana: Optional[str] = None
    karana_name: Optional[str] = None
    karana_end: Optional[str] = None

    sunrise: Optional[str] = None
    sunset: Optional[str] = None

    rahu: Optional[str] = None
    yamaganda: Optional[str] = None
    gulika: Optional[str] = None
    abhijit: Optional[str] = None
    brahma: Optional[str] = None

    today_score: Optional[float] = None
    rule_alignment_score: Optional[float] = None
    confidence_score: Optional[float] = None
    current_period_summary: Optional[str] = None
    next_auspicious_window: Optional[Dict[str, Any]] = None

    choghadiya_day: Optional[List[Dict[str, Any]]] = None
    choghadiya_night: Optional[List[Dict[str, Any]]] = None
    current_choghadiya: Optional[Dict[str, Any]] = None

    horas: Optional[List[Dict[str, Any]]] = None
    current_hora: Optional[Dict[str, Any]] = None

    disha_shool: Optional[Dict[str, Any]] = None
    dos_and_donts: Optional[Dict[str, Any]] = None
    planets: Optional[List[Dict[str, Any]]] = None
    samvat: Optional[Dict[str, Any]] = None

    # ── Personalization Layer ──
    personalization: Optional[Dict[str, Any]] = None
```

#### Auth & User Schemas (`modules/auth/schemas.py`)
```python
from datetime import datetime
from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: str = Field(..., min_length=3, max_length=255)
    phone: str = Field(default="", max_length=32)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: str
    password: str


class AdminLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    name: str
    email: str


class UserProfileUpdate(BaseModel):
    name: str
    phone: str = ""
    birth_date: str = ""
    birth_time: str = ""
    birth_city: str = ""
    zodiac_sign: str = ""
    notes: str = ""


class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    phone: str | None = None
    birth_date: str | None = None
    birth_time: str | None = None
    birth_city: str | None = None
    zodiac_sign: str | None = None
    notes: str | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    preferred_language: str = "en"
    created_at: datetime
    last_login_at: datetime | None = None
    profile: UserProfileResponse | None = None

    class Config:
        from_attributes = True
```

### 3.3 Database Migration Strategy
- **Framework**: Alembic with SQLAlchemy DeclarativeBase.
- **Config**: `backend/alembic.ini` and `backend/alembic/env.py`.
- **Migrations Present**:
  1. `20260526_0001_initial_postgresql_schema.py`: Initial schema creation for users, user_profiles, user_activities.
  2. `20260825_0002_add_admin_users_table.py`: Creation of `admin_users` table with username index.
  3. `20260825_0003_add_language_to_blogs.py`: Adds `language` column (VARCHAR(10)) to `blogs`.
- **Application Startup Hook**: In `gateway/main.py:lifespan`, `init_db()` runs `Base.metadata.create_all(bind=engine)`, ensuring local SQLite tables exist even if migrations have not been applied.

### 3.4 Actual Settings & Environment Keys Required at Boot
The application loads settings via Pydantic `BaseSettings` (`shared/config/settings.py`):
```text
PROJECT_NAME
APP_NAME
API_V1_STR
SECRET_KEY                     # Enforced by validate_settings() on boot
ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
DATABASE_URL                   # Defaults to sqlite:///./astrologic.db
REDIS_URL                      # If None, in-memory TTL cache fallback is engaged
GROQ_API_KEY                   # Optional
GEMINI_API_KEY                 # Optional
OPENAI_API_KEY                 # Optional
OLLAMA_BASE_URL                # Defaults to http://localhost:11434
OLLAMA_MODEL                   # Defaults to mistral
LLM_PROVIDER                   # auto / groq / gemini / openai
ENVIRONMENT                    # development / production
DEBUG                          # True / False
ALLOWED_ORIGINS                # CORS origin list (comma-separated or *)
SESSION_SECRET_KEY             # Starlette session encryption key
CHART_CACHE_ENABLED            # True / False
CHART_CACHE_TTL_SECONDS        # Default 2592000 (30 days)
CHART_CACHE_LRU_SIZE           # Default 1000 entries
```

---

## 4. API CONTRACTS (exact)

### Summary Route Catalog

| Method | Path | Auth Required | Cache Behavior | Rate Limit |
| :--- | :--- | :---: | :--- | :--- |
| `GET` | `/health` | No | None | None |
| `GET` | `/metrics` | No | None | None |
| `GET` | `/api/cities` | No | In-memory | None |
| `POST`| `/api/kundali` | **Yes (Session)** | `@cached_chart` (30 days) | None |
| `POST`| `/api/generate-chart` | **Yes (Session)** | None | None |
| `POST`| `/api/prediction` | **Yes (Session)** | Domain scores cached via Kundali | None |
| `POST`| `/api/prediction/timing/{domain}` | **Yes (Session)** | Chart cached via Kundali | None |
| `POST`| `/api/domains` | **Yes (Session)** | Chart cached via Kundali | None |
| `POST`| `/api/chat` | **Yes (Session)** | Contextual (Session bound) | None |
| `POST`| `/api/panchang` | No | `CacheService` key | None |
| `GET` | `/api/daily-horoscope/{sign}` | No | Daily calculation | None |
| `POST`| `/api/auth/signup` | No | None | None |
| `POST`| `/api/auth/login` | No | None | None |
| `POST`| `/api/admin/cache/flush` | **Yes (Admin)** | Flushes LRU & Redis | None |

> [!CAUTION]
> **CRITICAL SECURITY DIVERGENCE BETWEEN LLD AND CODE**:
> In the LLD routes table, `/api/kundali`, `/api/prediction`, and `/api/domains` were listed as `Auth: No`.
> In the **actual codebase** (`gateway/main.py:DefaultDenyAuthMiddleware`), these routes are **NOT** in `PUBLIC_API_PREFIXES`. Therefore, the gateway enforces default-deny: if `user_id` or `admin` is not set in `request.session`, the server returns `401 Unauthorized`.

#### 1. `POST /api/kundali`
- **Request Schema**:
  - `year`: int (1900..2100, required)
  - `month`: int (1..12, required)
  - `day`: int (1..31, required)
  - `hour`: int (0..23, required)
  - `minute`: int (0..59, required)
  - `city`: str (min_length=1, required, must exist in `cities.py`)
- **Request Example**:
```json
{
  "year": 1990,
  "month": 5,
  "day": 15,
  "hour": 14,
  "minute": 30,
  "city": "Pune"
}
```
- **Success Response (200 OK)**:
```json
{
  "lagna": "Kanya",
  "lagna_degree": "14° 17' 12\"",
  "lagna_degree_decimal": 14.2867,
  "lagna_nakshatra": "Hasta",
  "lagna_pada": 2,
  "is_near_boundary": false,
  "boundary_warning": "Lagna is comfortably positioned within sign boundaries.",
  "time_sensitivity_note": "Ascendant degrees shift approximately 1° every 4 minutes. If exact birth time is uncertain, domain score boundaries may vary.",
  "houses": {"1": ["Lagna"], "2": [], "3": [], "4": [], "5": ["Rahu"], "6": [], "7": [], "8": ["Sun", "Mercury"], "9": ["Venus"], "10": ["Jupiter"], "11": ["Ketu"], "12": ["Moon", "Mars", "Saturn"]},
  "d9_houses": {"1": ["Lagna"], "2": ["Moon"], "3": [], "4": ["Jupiter"], "5": [], "6": ["Mercury"], "7": ["Sun"], "8": ["Venus"], "9": ["Mars", "Saturn"], "10": [], "11": ["Rahu"], "12": ["Ketu"]},
  "d9_lagna": "Vrishabha",
  "planets": [
    {"name": "Sun", "sign": "Mesha", "degree": "00° 51' 14\"", "degree_decimal": 0.8539, "house": 8, "nakshatra": "Krittika", "pada": 2, "navamsa": "Makara", "strength": "Exalted", "retrograde": false},
    {"name": "Moon", "sign": "Makara", "degree": "12° 24' 18\"", "degree_decimal": 12.405, "house": 5, "nakshatra": "Shravana", "pada": 1, "navamsa": "Mesha", "strength": "Neutral", "retrograde": false}
  ],
  "tithi_number": 21,
  "tithi_name": "Krishna Shashthi",
  "paksha": "Krishna",
  "nakshatra": "Shravana",
  "nakshatra_pada": 1,
  "yoga_name": "Shukla",
  "karana_name": "Garaja",
  "ayanamsa": 23.7381,
  "jd": 2448027.875,
  "mahadasha": "Moon",
  "dasha_balance": "8.4 years",
  "antardasha": "Moon",
  "antardasha_list": [{"lord": "Moon", "years": 0.83}, {"lord": "Mars", "years": 0.58}],
  "scores": {"overall_strength": 67, "career_score": 72, "finance_score": 68, "marriage_score": 65, "health_score": 70, "mental_score": 64, "spirituality_score": 75},
  "yogas": [{"name": "Gajakesari Yoga", "description": "Jupiter in Kendra from Moon...", "present": true, "strength": "Strong"}],
  "doshas": [{"name": "Manglik Dosha", "present": false, "intensity": "None", "remedies": []}],
  "disclaimer": "Vedic astrology interpretations represent traditional symbolic frameworks..."
}
```
- **Error Response (400 Bad Request — City not found)**:
```json
{
  "detail": "City 'Atlantis' not found in database. Please try a nearby major city."
}
```
- **Error Response (401 Unauthorized — Missing session)**:
```json
{
  "detail": "Authentication required. Default-deny policy enforced."
}
```

#### 2. `POST /api/prediction`
- **Query Params**: `sync` (bool, default=False), `include_narrative` (bool, default=True)
- **Request Schema**: `year` (int), `month` (int), `day` (int), `hour` (float 0..24), `city` (str, optional, default="Pune")
- **Success Response (200 OK — Async Default)**:
```json
{
  "marriage_score": 72,
  "career_score": 78,
  "narrative_job_id": "job:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "domains": {
    "marriage": {"domain": "Marriage & Relationships", "score": 72, "timing_windows": []},
    "career": {"domain": "Career & Profession", "score": 78, "timing_windows": []}
  },
  "disclaimer": "Vedic astrology interpretations represent traditional symbolic frameworks..."
}
```

---

## 5. CORE ALGORITHMS (exact implementation)

### a) Ayanamsa Conversion + Longitude Normalization
Implemented in `modules/kundali/engine.py` and `shared/ephemeris/wrapper.py`:
```python
swe.set_ephe_path('.')
swe.set_sid_mode(swe.SIDM_LAHIRI)
flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

# Convert UTC decimal hours & JD:
jd = swe.julday(year, month, calc_day, utc_hours)
raw_lon = swe.calc_ut(jd, planet_id, flags)[0][0] % 360.0
ayanamsa = swe.get_ayanamsa(jd)
```

### b) `swe_calc_ut` Call Wrapper
Implemented in `shared/ephemeris/wrapper.py`:
```python
def calc_ut(julian_day: float, body: int, flags: int = swe.FLG_SIDEREAL) -> tuple:
    """Calculate sidereal longitude and speed for a celestial body."""
    return swe.calc_ut(julian_day, body, flags)
```

### c) `swe_houses_ex` Call + Sripati vs Whole-Sign Logic
Implemented in `modules/kundali/houses.py`:
```python
# Whole Sign system:
cusps, ascmc = swe.houses_ex(jd, latitude, longitude, b'W', flags)
asc_degree = ascmc[0] % 360.0

# Placidus / Sripati Bhava Chalit:
cusps, ascmc = swe.houses_ex(jd, latitude, longitude, b'P', flags)
```

### d) Varga (D1...D60) Implementation Reality
> [!WARNING]
> **DIVERGENCE ALERT**: The codebase only implements **D9 Navamsa** in `modules/kundali/varga.py:calculate_navamsa()`.
> Other divisional charts (D2 Hora, D3 Drekkana, D7, D10 Dasamsa, D60 Shastiamsa) claimed in the LLD are **NOT IMPLEMENTED** in Python code.
```python
# Exact D9 Navamsa implementation:
NAVAMSA_START = {
    0: 0, 4: 0, 8: 0,   # Fire signs -> start from Mesha (0)
    1: 9, 5: 9, 9: 9,   # Earth signs -> start from Makara (9)
    2: 6, 6: 6, 10: 6,  # Air signs -> start from Tula (6)
    3: 3, 7: 3, 11: 3,  # Water signs -> start from Karka (3)
}
PADA_DEG = 30.0 / 9.0  # 3° 20'

def calculate_navamsa(longitude: float) -> str:
    norm_deg = longitude % 360.0
    sign_idx = int(norm_deg / 30.0)
    deg_in_sign = norm_deg % 30.0
    pada = int(deg_in_sign / PADA_DEG)
    start_sign = NAVAMSA_START[sign_idx]
    nav_idx = (start_sign + pada) % 12
    return SIGNS_SK[nav_idx]
```

### e) Vimshottari Dasha Subdivision
Implemented in `modules/kundali/dasha.py`. Subdivides down to **PD (Pratyantardasha)**:
```python
# DASHA_DEPTH = "PD" (SD and PrD are NOT IMPLEMENTED)
def compute_pratyantardasha(md_lord: str, ad_lord: str, ad_start: datetime, ad_end: datetime) -> list[dict]:
    pds = []
    ad_duration_days = (ad_end - ad_start).total_seconds() / 86400.0
    start_idx = DASHA_SEQUENCE.index(ad_lord) if ad_lord in DASHA_SEQUENCE else 0
    curr_start = ad_start
    for i in range(9):
        pd_lord = DASHA_SEQUENCE[(start_idx + i) % 9]
        pd_duration_days = ad_duration_days * (DASHA_YEARS[pd_lord] / 120.0)
        curr_end = curr_start + timedelta(days=pd_duration_days)
        pds.append({
            "md_lord": md_lord, "ad_lord": ad_lord, "pd_lord": pd_lord,
            "start": curr_start.strftime("%Y-%m-%d"),
            "end": curr_end.strftime("%Y-%m-%d"),
            "days": round(pd_duration_days, 1),
        })
        curr_start = curr_end
    return pds
```

### f) Tithi / Yoga / Karana / Nakshatra / Vara Computation
Implemented in `modules/kundali/engine.py:174-184` and `modules/panchang/engine.py:130-170`:
```python
diff = (moon_lon - sun_lon) % 360.0
tithi_num = int(diff / 12.0) + 1
tithi_name = TITHI_NAMES[(tithi_num - 1) % 30]
paksha = "Shukla" if tithi_num <= 15 else "Krishna"

moon_nak, moon_pada = calculate_nakshatra(moon_lon)
yoga_name = YOGA_NAMES[int(((sun_lon + moon_lon) % 360.0) / (360.0 / 27.0)) % 27]
karana_name = KARANA_NAMES[int(diff / 6.0) % 7]
```

### g) Tarabala and Chandrabala Matrices
Implemented in `modules/panchang/personalization.py`:
- **Tarabala**: Distance calculation across 9 categories:
  - Favorable (2, 4, 6, 8, 9): Sampat, Kshema, Sadhana, Mitra, Parama Mitra.
  - Unfavorable (1, 3, 5, 7): Janma, Vipat, Pratyak, Naidhana.
- **Chandrabala**: House of transiting Moon relative to natal Moon sign:
  - Favorable: Houses 1, 3, 6, 7, 10, 11.
  - Unfavorable: Houses 2, 4, 5, 8, 9, 12.

### h) Dignity Scoring Function
Implemented in `shared/veda/dignity.py`:
```python
"""9-Tier Dignity and Naisargika Maitri Planetary Friendship Engine (Pure Shared Library)."""

from .strength import EXALTATION, DEBILITATION, OWN_SIGNS

# Naisargika Maitri (Classical Natural Friendships)
PLANET_FRIENDS = {
    "Sun": ["Moon", "Mars", "Jupiter"],
    "Moon": ["Sun", "Mercury"],
    "Mars": ["Sun", "Moon", "Jupiter"],
    "Mercury": ["Sun", "Venus"],
    "Jupiter": ["Sun", "Moon", "Mars"],
    "Venus": ["Mercury", "Saturn"],
    "Saturn": ["Mercury", "Venus"],
    "Rahu": ["Mercury", "Venus", "Saturn"],
    "Ketu": ["Mars", "Venus", "Saturn"],
}

PLANET_ENEMIES = {
    "Sun": ["Venus", "Saturn", "Rahu", "Ketu"],
    "Moon": [],  # Moon has no natural enemies
    "Mars": ["Mercury"],
    "Mercury": ["Moon"],
    "Jupiter": ["Mercury", "Venus"],
    "Venus": ["Sun", "Moon"],
    "Saturn": ["Sun", "Moon", "Mars"],
    "Rahu": ["Sun", "Moon", "Mars"],
    "Ketu": ["Sun", "Moon"],
}

MOOLATRIKONA = {
    "Sun": "Simha",
    "Moon": "Vrishabha",
    "Mars": "Mesha",
    "Mercury": "Kanya",
    "Jupiter": "Dhanu",
    "Venus": "Tula",
    "Saturn": "Kumbha",
}


def get_naisargika_dignity(planet: str, sign: str) -> str:
    """Return 9-tier dignity classification for a planet in a sign."""
    if EXALTATION.get(planet) == sign:
        return "Exalted"
    if MOOLATRIKONA.get(planet) == sign:
        return "Moolatrikona"
    if sign in OWN_SIGNS.get(planet, []):
        return "Own Sign"
    if DEBILITATION.get(planet) == sign:
        return "Debilitated"

    from .zodiac import SIGN_LORDS
    dispositor = SIGN_LORDS.get(sign)
    if not dispositor or dispositor == planet:
        return "Own Sign"

    friends = PLANET_FRIENDS.get(planet, [])
    enemies = PLANET_ENEMIES.get(planet, [])

    if dispositor in friends:
        return "Great Friend" if dispositor in OWN_SIGNS.get(planet, []) else "Friend"
    if dispositor in enemies:
        return "Great Enemy" if dispositor in DEBILITATION.get(planet, []) else "Enemy"
    return "Neutral"


def get_positional_strength(name: str, sign: str, navamsa: str = "", degree: float = 0.0) -> float:
    """
    Calculate numerical positional strength score (-2.0 to +2.0) using 9-tier dignity.
    """
    dignity = get_naisargika_dignity(name, sign)
    score_map = {
        "Exalted": 2.0,
        "Moolatrikona": 1.5,
        "Own Sign": 1.0,
        "Great Friend": 0.75,
        "Friend": 0.50,
        "Neutral": 0.0,
        "Enemy": -0.50,
        "Great Enemy": -0.75,
        "Debilitated": -2.0,
    }
    score = score_map.get(dignity, 0.0)

    # Navamsa dignity bonus
    if navamsa:
        nav_dignity = get_naisargika_dignity(name, navamsa)
        if nav_dignity in ("Exalted", "Moolatrikona", "Own Sign"):
            score += 0.5
        elif nav_dignity in ("Debilitated", "Great Enemy"):
            score -= 0.5

    return max(-2.0, min(2.0, round(score, 2)))
```

### i) Timing Fusion Scorer
Implemented in `modules/prediction/timing_fusion.py`:
```python
"""Window fusion engine combining Dasha (60%) + Gochara (40%) into ranked, smoothed timing windows."""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Dict, Any, List, Optional

from modules.prediction.timing_config import get_domain_timing_config
from modules.prediction.timing_dasha import score_dasha_periods, ScoredPeriod
from modules.prediction.timing_transit import score_transit_months, ScoredMonth


@dataclass
class TimingWindow:
    start_date: date
    end_date: date
    peak_date: date
    peak_score: float
    confidence: str
    mahadasha: str
    antardasha: str
    pratyantardasha: str
    reasons: List[str]
    drivers: List[str]
    sub_scores: Dict[str, float]


@dataclass
class TimingFusionResult:
    timing_windows: List[TimingWindow]
    peak_window: Optional[TimingWindow]
    next_12_months_summary: str
    methodology: str
    threshold_used: float
    engine_version: str


def get_confidence_tier(score: float) -> str:
    """Return confidence tier based on peak fused score."""
    if score >= 0.75:
        return "High"
    elif score >= 0.55:
        return "Moderate"
    elif score >= 0.35:
        return "Possible"
    return "Unlikely"


def fuse_windows(
    chart: dict,
    domain: str,
    start_date: date,
    end_date: date,
    top_n: int = 5,
) -> TimingFusionResult:
    """
    Combine Dasha periods (60%) + Transit months (40%) into ranked, smoothed timing windows.
    """
    config = get_domain_timing_config(domain)
    dasha_w = config.get("dasha_weight", 0.60)
    transit_w = config.get("transit_weight", 0.40)
    special_rules = config.get("special_rules", [])

    # 1. Fetch raw Dasha and Transit scores
    dasha_periods = score_dasha_periods(chart, domain, start_date, end_date)
    transit_months = score_transit_months(chart, domain, start_date, end_date)

    if not transit_months:
        return TimingFusionResult(
            timing_windows=[],
            peak_window=None,
            next_12_months_summary=f"No timing windows generated for {domain}.",
            methodology="Dasha 60% + Gochara 40%, 15-year horizon",
            threshold_used=0.45,
            engine_version="1.0.0",
        )

    # 2. STEP A — Align time axes per monthly snapshot
    monthly_snapshots = []
    for m in transit_months:
        # Find matching dasha period covering month_start
        matching_dasha = None
        for dp in dasha_periods:
            if dp.start_date <= m.month_start <= dp.end_date or dp.start_date <= m.month_end <= dp.end_date or m.month_start <= dp.start_date <= m.month_end:
                matching_dasha = dp
                break

        d_score = matching_dasha.score if matching_dasha else 0.30
        t_score = m.score

        combined = (dasha_w * d_score) + (transit_w * t_score)

        monthly_snapshots.append({
            "month_start": m.month_start,
            "month_end": m.month_end,
            "dasha_score": d_score,
            "transit_score": t_score,
            "combined_score": round(combined, 3),
            "dasha_period": matching_dasha,
            "transit_month": m,
        })

    # 3. STEP B — 3-month rolling average smoothing
    num_months = len(monthly_snapshots)
    smoothed_scores = []
    for i in range(num_months):
        prev_s = monthly_snapshots[i - 1]["combined_score"] if i > 0 else monthly_snapshots[i]["combined_score"]
        curr_s = monthly_snapshots[i]["combined_score"]
        next_s = monthly_snapshots[i + 1]["combined_score"] if i < num_months - 1 else monthly_snapshots[i]["combined_score"]

        smooth_val = round((prev_s + curr_s + next_s) / 3.0, 3)
        smoothed_scores.append(smooth_val)
        monthly_snapshots[i]["smoothed_score"] = smooth_val

    # 4. STEP C & D — Threshold & Merge consecutive months (with 1-month gap tolerance)
    threshold = 0.45
    qualifying_indices = [i for i, snap in enumerate(monthly_snapshots) if snap["smoothed_score"] >= threshold]

    raw_groups = []
    if qualifying_indices:
        current_group = [qualifying_indices[0]]
        for idx in qualifying_indices[1:]:
            # Allow up to 1-month gap between qualifying months (diff <= 2)
            if idx - current_group[-1] <= 2:
                current_group.append(idx)
            else:
                raw_groups.append(current_group)
                current_group = [idx]
        if current_group:
            raw_groups.append(current_group)

    # 5. Build raw TimingWindow objects from groups
    built_windows = []
    for grp in raw_groups:
        grp_months = [monthly_snapshots[i] for i in grp]
        peak_snap = max(grp_months, key=lambda x: x["smoothed_score"])

        w_start = grp_months[0]["month_start"]
        w_end = grp_months[-1]["month_end"]
        peak_dt = peak_snap["month_start"]
        peak_score = peak_snap["smoothed_score"]

        d_period = peak_snap["dasha_period"]
        t_month = peak_snap["transit_month"]

        md_l = d_period.mahadasha_lord if d_period else "Jupiter"
        ad_l = d_period.antardasha_lord if d_period else "Venus"
        pd_l = d_period.pratyantardasha_lord if d_period else "Saturn"

        d_reasons = d_period.reasons if d_period else []
        t_reasons = t_month.reasons if t_month else []
        merged_reasons = list(dict.fromkeys(d_reasons + t_reasons))

        top_drivers = merged_reasons[:4]
        conf = get_confidence_tier(peak_score)

        # 6. STEP H — Special rule enforcement
        sat_house = t_month.active_transits.get("Saturn", {}).get("house") if t_month else None
        if "saturn_7h_block" in special_rules and sat_house == 7 and domain == "marriage":
            conf = "Possible"

        if "jupiter_return_7h" in special_rules and peak_score >= 0.60:
            jup_h = t_month.active_transits.get("Jupiter", {}).get("house") if t_month else None
            if jup_h == 7:
                conf = "High"

        built_windows.append(
            TimingWindow(
                start_date=w_start,
                end_date=w_end,
                peak_date=peak_dt,
                peak_score=peak_score,
                confidence=conf,
                mahadasha=md_l,
                antardasha=ad_l,
                pratyantardasha=pd_l,
                reasons=merged_reasons,
                drivers=top_drivers,
                sub_scores={
                    "dasha_score": peak_snap["dasha_score"],
                    "transit_score": peak_snap["transit_score"],
                },
            )
        )

    # 7. STEP G — Deduplicate overlapping windows (>50% overlap)
    deduped_windows: List[TimingWindow] = []
    for w in built_windows:
        if not deduped_windows:
            deduped_windows.append(w)
        else:
            prev_w = deduped_windows[-1]
            overlap_start = max(prev_w.start_date, w.start_date)
            overlap_end = min(prev_w.end_date, w.end_date)
            if overlap_start <= overlap_end:
                overlap_days = (overlap_end - overlap_start).days + 1
                len1 = (prev_w.end_date - prev_w.start_date).days + 1
                len2 = (w.end_date - w.start_date).days + 1
                min_len = min(len1, len2)

                if min_len > 0 and (overlap_days / min_len) >= 0.50:
                    # Merge into stronger window
                    if w.peak_score > prev_w.peak_score:
                        deduped_windows[-1] = w
                    continue
            deduped_windows.append(w)

    # 8. STEP F — Rank and limit
    deduped_windows.sort(key=lambda x: x.peak_score, reverse=True)
    top_windows = deduped_windows[:top_n]
    peak_win = top_windows[0] if top_windows else None

    # Next 12 months summary
    if peak_win:
        summary_msg = f"Peak activation window for {domain} occurs around {peak_win.peak_date.strftime('%B %Y')} with {peak_win.confidence} confidence during {peak_win.mahadasha}-{peak_win.antardasha} Dasha."
    else:
        summary_msg = f"No major timing activation window identified for {domain} in the next 12 months."

    return TimingFusionResult(
        timing_windows=top_windows,
        peak_window=peak_win,
        next_12_months_summary=summary_msg,
        methodology="Dasha 60% + Gochara 40%, 15-year horizon",
        threshold_used=threshold,
        engine_version="1.0.0",
    )
```

### j) Yogas Detection
Implemented in `shared/veda/yogas.py`:
```python
"""Classical Vedic Astrology Yogas Detection Engine (Pure Shared Library)."""

from .zodiac import SIGNS_SK, SIGN_LORDS
from .strength import EXALTATION, OWN_SIGNS

KENDRA = {1, 4, 7, 10}
TRIKONA = {1, 5, 9}
DUSTHANA = {6, 8, 12}


def _get_planet_map(planets: list[dict]) -> dict[str, dict]:
    return {p.get("name") or p.get("planet"): p for p in planets if p.get("name") or p.get("planet")}


def _house_of(pmap: dict, name: str) -> int:
    p = pmap.get(name, {})
    h = p.get("house", 0)
    if isinstance(h, int):
        return h
    try:
        return int(str(h).split("/")[0])
    except (ValueError, TypeError):
        return 0


def _sign_of(pmap: dict, name: str) -> str:
    return pmap.get(name, {}).get("sign", "")


def calculate_yogas(planets: list[dict], lagna_sign: str, houses: dict) -> list[dict]:
    """Detect and score classical Vedic yogas in a natal chart."""
    pmap = _get_planet_map(planets)
    yogas = []
    lagna_idx = SIGNS_SK.index(lagna_sign) if lagna_sign in SIGNS_SK else 0

    def add(name: str, desc: str, present: bool, strength: str = "Medium"):
        yogas.append({
            "name": name,
            "description": desc,
            "present": bool(present),
            "strength": strength if present else "Absent",
        })

    sun_h = _house_of(pmap, "Sun")
    moon_h = _house_of(pmap, "Moon")
    mar_h = _house_of(pmap, "Mars")
    mer_h = _house_of(pmap, "Mercury")
    jup_h = _house_of(pmap, "Jupiter")
    ven_h = _house_of(pmap, "Venus")
    sat_h = _house_of(pmap, "Saturn")

    jup_s = _sign_of(pmap, "Jupiter")
    mar_s = _sign_of(pmap, "Mars")
    mer_s = _sign_of(pmap, "Mercury")
    ven_s = _sign_of(pmap, "Venus")
    sat_s = _sign_of(pmap, "Saturn")

    # 1. Gajakesari Yoga (Jupiter in Kendra from Moon)
    gaja = bool(moon_h and jup_h and abs(jup_h - moon_h) in {0, 3, 6, 9})
    add(
        "Gajakesari Yoga",
        "Jupiter in kendra from Moon — wisdom, fame, leadership, and prosperity.",
        gaja,
        "Strong" if gaja and jup_s in OWN_SIGNS.get("Jupiter", []) else "Medium",
    )

    # 2. Pancha Mahapurusha Yogas
    mahapurusha = [
        ("Mars", mar_h, mar_s, "Ruchaka Yoga", "Mars in own/exaltation sign in kendra — courage, leadership, and authority."),
        ("Mercury", mer_h, mer_s, "Bhadra Yoga", "Mercury in own/exaltation sign in kendra — sharp intellect, commerce, and communication."),
        ("Jupiter", jup_h, jup_s, "Hamsa Yoga", "Jupiter in own/exaltation sign in kendra — spiritual wisdom, grace, and noble status."),
        ("Venus", ven_h, ven_s, "Malavya Yoga", "Venus in own/exaltation sign in kendra — luxury, artistic mastery, beauty, and prosperity."),
        ("Saturn", sat_h, sat_s, "Sasa Yoga", "Saturn in own/exaltation sign in kendra — perseverance, discipline, authority, and mass leadership."),
    ]
    for pname, ph, ps, yname, ydesc in mahapurusha:
        present = ph in KENDRA and (ps in OWN_SIGNS.get(pname, []) or EXALTATION.get(pname) == ps)
        add(yname, ydesc, present, "Strong" if present else "Absent")

    # 3. Budhaditya Yoga
    add(
        "Budhaditya Yoga",
        "Sun and Mercury conjunct — analytical mind, government/academic success, and eloquence.",
        sun_h == mer_h and sun_h != 0,
        "Strong" if sun_h in KENDRA or sun_h in TRIKONA else "Medium",
    )

    # 4. Chandra-Mangala Yoga
    cm_present = bool((moon_h == mar_h and moon_h != 0) or (moon_h and mar_h and abs(moon_h - mar_h) == 6))
    add(
        "Chandra-Mangala Yoga",
        "Moon-Mars association — intense financial drive, commercial success, and enterprising nature.",
        cm_present,
    )

    # 5. Dharma-Karmadhipati Yoga
    lord_9 = SIGN_LORDS.get(SIGNS_SK[(lagna_idx + 8) % 12])
    lord_10 = SIGN_LORDS.get(SIGNS_SK[(lagna_idx + 9) % 12])
    h9 = _house_of(pmap, lord_9) if lord_9 else 0
    h10 = _house_of(pmap, lord_10) if lord_10 else 0
    dkd = bool(lord_9 and lord_10 and lord_9 != lord_10 and ((h9 == h10 and h9 != 0) or (h9 == 10 and h10 == 9)))
    add(
        "Dharma-Karmadhipati Yoga",
        "9th and 10th lords conjunct or exchanging signs — exceptional career, highest honor, and dharmic success.",
        dkd,
        "Strong" if dkd else "Absent",
    )

    # 6. Viparita Raja Yoga
    l6 = SIGN_LORDS.get(SIGNS_SK[(lagna_idx + 5) % 12])
    l8 = SIGN_LORDS.get(SIGNS_SK[(lagna_idx + 7) % 12])
    l12 = SIGN_LORDS.get(SIGNS_SK[(lagna_idx + 11) % 12])
    h6 = _house_of(pmap, l6) if l6 else 0
    h8 = _house_of(pmap, l8) if l8 else 0
    h12 = _house_of(pmap, l12) if l12 else 0
    vip = bool((h6 in DUSTHANA and h8 in DUSTHANA) or (h6 in DUSTHANA and h12 in DUSTHANA))
    add(
        "Viparita Raja Yoga",
        "Lords of 6th, 8th, or 12th placed in dusthanas — triumph over adversaries and resilience after hardship.",
        vip,
    )

    # 7. Neecha Bhanga Raja Yoga
    nbry = False
    for planet, deb_sign in [("Sun", "Tula"), ("Moon", "Vrischika"), ("Mars", "Karka"),
                             ("Mercury", "Meena"), ("Jupiter", "Makara"), ("Venus", "Kanya"), ("Saturn", "Mesha")]:
        p = pmap.get(planet)
        if p and p.get("sign") == deb_sign:
            disp = SIGN_LORDS.get(deb_sign)
            if disp and _house_of(pmap, disp) in KENDRA:
                nbry = True
                break
    add(
        "Neecha Bhanga Raja Yoga",
        "Debilitation cancelled by dispositor in kendra — initial disadvantage transforms into great strength.",
        nbry,
        "Strong" if nbry else "Absent",
    )

    # 8. Dhana Yoga
    lord_2 = SIGN_LORDS.get(SIGNS_SK[(lagna_idx + 1) % 12])
    lord_11 = SIGN_LORDS.get(SIGNS_SK[(lagna_idx + 10) % 12])
    dhana = bool(lord_2 and lord_11 and _house_of(pmap, lord_2) == _house_of(pmap, lord_11) and _house_of(pmap, lord_2) != 0)
    add(
        "Dhana Yoga",
        "Lords of 2nd and 11th houses conjunct — strong wealth accumulation and prosperity.",
        dhana,
    )

    return yogas


def detect_advanced_yogas(chart: dict) -> list[str]:
    """Lightweight yogas extractor returning list of active yoga names."""
    planets = []
    planets_by_house = chart.get("planets_by_house", {})
    for h, p_list in planets_by_house.items():
        for p in p_list:
            p_copy = dict(p)
            p_copy["house"] = int(h)
            planets.append(p_copy)

    lagna = chart.get("basic_details", {}).get("lagna", "Mesha")
    yogas = calculate_yogas(planets, lagna, {})
    return [y["name"] for y in yogas if y["present"]]
```

### k) Doshas Detection
Implemented in `shared/veda/doshas.py`:
```python
"""Vedic Doshas detection engine with remedies (Pure Shared Library)."""

from .zodiac import SIGNS_SK

GANDMOOL_NAKSHATRAS = {"Ashwini", "Ashlesha", "Magha", "Jyeshtha", "Mula", "Revati"}


def _get_planet_map(planets: list[dict] | dict[str, dict]) -> dict[str, dict]:
    if isinstance(planets, dict):
        return planets
    return {p.get("name") or p.get("planet"): p for p in planets if p.get("name") or p.get("planet")}


def _house_of(pmap: dict, name: str) -> int:
    p = pmap.get(name, {})
    h = p.get("house", 0)
    if isinstance(h, int):
        return h
    try:
        return int(str(h).split("/")[0])
    except (ValueError, TypeError):
        return 0


def _sign_of(pmap: dict, name: str) -> str:
    return pmap.get(name, {}).get("sign", "")


MANGLIK_HOUSES = {1, 2, 4, 7, 8, 12}


def evaluate_mangal_dosha(planet_data: dict[str, dict] | list[dict]) -> dict:
    """
    Consolidated Mangal Dosh (Manglik) evaluator used across the system.
    Checks houses {1, 2, 4, 7, 8, 12} and classical cancellation rules:
      - Mars in own sign (Mesha, Vrischika) or exaltation (Makara)
      - Jupiter conjunct Mars (same house)
      - Jupiter aspecting Mars (5th, 7th, 9th aspect)
      - Jupiter occupying 7th house
    """
    pmap = _get_planet_map(planet_data)

    mars = pmap.get("Mars", {})
    mar_h = _house_of(pmap, "Mars")
    mars_sign = _sign_of(pmap, "Mars")

    jup = pmap.get("Jupiter", {})
    jup_h = _house_of(pmap, "Jupiter")

    raw = mar_h in MANGLIK_HOUSES

    reasons = []
    if raw:
        if mars_sign in ("Mesha", "Vrischika", "Makara"):
            reasons.append(f"Mars in own/exalted sign ({mars_sign})")
        if jup_h > 0 and mar_h > 0:
            if jup_h == mar_h:
                reasons.append("Jupiter conjunct Mars")
            elif (mar_h - jup_h) % 12 in (4, 6, 8):
                aspect_num = {4: "5th", 6: "7th", 8: "9th"}[(mar_h - jup_h) % 12]
                reasons.append(f"Jupiter {aspect_num} aspect on Mars")
        if jup_h == 7 and jup_h != mar_h:
            reasons.append("Jupiter in 7th house")

    cancelled = raw and bool(reasons)
    present = raw and not cancelled
    cancellation_reason = ", ".join(reasons) if cancelled else ""

    return {
        "raw": raw,
        "present": present,
        "cancelled": cancelled,
        "house": mar_h,
        "sign": mars_sign,
        "cancellation_reason": cancellation_reason,
    }


def evaluate_pitru_dosha(planet_data: dict[str, dict] | list[dict]) -> dict:
    """
    Consolidated Pitru Dosh evaluator used across the system.
    Checks:
      - Rahu or Ketu in 9th house
      - Sun in 9th house afflicted by Rahu, Ketu, or Saturn
      - Sun conjunct Rahu or Ketu in any house
    """
    pmap = _get_planet_map(planet_data)

    rahu_h = _house_of(pmap, "Rahu")
    ketu_h = _house_of(pmap, "Ketu")
    sun_h = _house_of(pmap, "Sun")
    sat_h = _house_of(pmap, "Saturn")

    h9_planets = [p for p, d in pmap.items() if (d.get("house") if isinstance(d, dict) else 0) == 9]

    in_9th = (rahu_h == 9 or ketu_h == 9)
    sun_in_9_afflicted = (sun_h == 9 and (rahu_h == 9 or ketu_h == 9 or sat_h == 9 or any(p in {"Rahu", "Ketu", "Saturn"} for p in h9_planets)))
    sun_conj_nodes = (sun_h > 0 and (sun_h == rahu_h or sun_h == ketu_h))

    present = bool(in_9th or sun_in_9_afflicted or sun_conj_nodes)
    reasons = []
    if in_9th:
        reasons.append("Rahu/Ketu in 9th house")
    if sun_in_9_afflicted:
        reasons.append("Sun in 9th house afflicted by malefic")
    if sun_conj_nodes and not in_9th:
        reasons.append("Sun conjunct Rahu/Ketu")

    return {
        "present": present,
        "reason": ", ".join(reasons) if present else "",
    }


def calculate_doshas(planets: list[dict], lagna_sign: str, houses: dict) -> list[dict]:
    """Detect and score major astrological doshas with authentic Vedic remedies."""
    pmap = _get_planet_map(planets)
    doshas = []

    def add(name: str, present: bool, severity: str, desc: str, remedies: list[str]):
        doshas.append({
            "name": name,
            "present": bool(present),
            "severity": severity if present else "None",
            "description": desc,
            "remedies": remedies if present else [],
        })

    rahu_h = _house_of(pmap, "Rahu")
    ketu_h = _house_of(pmap, "Ketu")
    sun_h = _house_of(pmap, "Sun")
    moon_h = _house_of(pmap, "Moon")
    moon_s = _sign_of(pmap, "Moon")
    sat_s = _sign_of(pmap, "Saturn")

    # 1. Mangal Dosha (Manglik)
    eval_m = evaluate_mangal_dosha(pmap)
    manglik_raw = eval_m["raw"]
    mars_canceled = eval_m["cancelled"]
    mar_h = eval_m["house"]

    severity = "Low (Canceled)" if (manglik_raw and mars_canceled) else ("High" if mar_h in {1, 7, 8} else ("Medium" if manglik_raw else "None"))

    manglik_desc = (
        f"Mars placed in house {mar_h}. "
        + (f"Mangal Dosh is present but cancelled due to: {eval_m['cancellation_reason']}." if mars_canceled else
           "Traditionally evaluated in Vedic horoscope matching for relationship intensity and partnership harmony.")
    )

    add(
        "Mangal Dosha (Manglik)",
        manglik_raw,
        severity,
        manglik_desc,
        [
            "Recite Hanuman Chalisa or Mangal Gayatri daily",
            "Donate red lentils or sweet jaggery on Tuesdays",
            "Practice mindful communication and patience in partnerships",
            "Consult a qualified astrologer for comprehensive Koota Milan matching",
        ],
    )

    # 2. Shani Sade Sati
    moon_idx = SIGNS_SK.index(moon_s) if moon_s in SIGNS_SK else -1
    sat_idx = SIGNS_SK.index(sat_s) if sat_s in SIGNS_SK else -1
    sade = moon_idx >= 0 and sat_idx >= 0 and (sat_idx - moon_idx) % 12 in {0, 1, 11}
    add(
        "Shani Sade Sati",
        sade,
        "Moderate" if sade else "None",
        "Saturn transiting within ±1 sign of natal Moon — a traditional 7.5-year phase associated with discipline, "
        "patience, and personal restructuring. Classical Vedic texts view this as a period for inner maturity.",
        [
            "Chant 'Om Sham Shanaischaraya Namaha' 108 times on Saturdays",
            "Engage in selfless service and support community welfare",
            "Feed birds or domestic animals regularly",
            "Practice patience, daily meditation, and long-term planning",
        ],
    )

    # 3. Kaal Sarp Dosha
    if rahu_h and ketu_h:
        all_h = [_house_of(pmap, p) for p in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")]
        all_h = [h for h in all_h if h > 0]

        def is_between(h):
            if rahu_h < ketu_h:
                return rahu_h < h < ketu_h
            return h > rahu_h or h < ketu_h

        ks = bool(all_h) and (all(is_between(h) for h in all_h) or all(not is_between(h) for h in all_h))
    else:
        ks = False

    add(
        "Kaal Sarp Dosha",
        ks,
        "Moderate" if ks else "None",
        "Planetary positions bounded within the Rahu-Ketu axis. Traditionally associated with focused drive; "
        "many prominent classical and modern figures carry this chart pattern successfully.",
        [
            "Practice daily meditation or Pranayama",
            "Engage in regular spiritual or charitable pursuits",
            "Worship Lord Shiva or recite Maha Mrityunjaya Mantra",
        ],
    )

    # 4. Pitru Dosha
    eval_p = evaluate_pitru_dosha(pmap)
    pitru = eval_p["present"]
    add(
        "Pitru Dosha",
        pitru,
        "Medium",
        f"Karmic ancestral debt or affliction in the 9th house of Dharma/Father. ({eval_p['reason']})" if pitru else "Karmic ancestral debt or affliction in the 9th house of Dharma/Father.",
        [
            "Perform Pitru Tarpan or Shraddha on Amavasya",
            "Feed cows and stray dogs regularly",
            "Recite Gayatri Mantra 108 times every morning",
            "Plant a sacred Peepal (Banyan) tree",
        ],
    )

    # 5. Grahan Dosha
    grahan = bool(
        (sun_h == rahu_h and sun_h != 0) or (sun_h == ketu_h and sun_h != 0) or
        (moon_h == rahu_h and moon_h != 0) or (moon_h == ketu_h and moon_h != 0)
    )
    add(
        "Grahan Dosha",
        grahan,
        "High",
        "Sun or Moon conjunct Rahu/Ketu — indicates emotional or identity sensitivity.",
        [
            "Worship Lord Surya at sunrise offering water with copper vessel",
            "Chant Chandra Gayatri mantra during full moon",
            "Donate white food (rice, milk) on Mondays and wheat on Sundays",
        ],
    )

    # 6. Gandmool Dosha
    moon_nak = pmap.get("Moon", {}).get("nakshatra", "")
    gand = moon_nak in GANDMOOL_NAKSHATRAS
    add(
        "Gandmool Dosha",
        gand,
        "Medium",
        f"Moon situated in {moon_nak} Gandmool nakshatra at birth.",
        [
            "Perform Gandmool Shanti ritual",
            "Worship Lord Ganesha daily",
            "Donate green moong dal or white items on Nakshatra transit days",
        ],
    )

    return doshas
```

### l) Cache Key Canonicalization & SHA-256
Implemented in `shared/cache/keys.py`:
```python
"""Cache key computation utilities for chart computations."""

import hashlib
import json
from typing import Any
from pydantic import BaseModel


def compute_input_hash(req_data: dict[str, Any] | BaseModel) -> str:
    """
    Compute a deterministic SHA256 input hash for birth chart data.
    Ensures keys are sorted, values are normalized (canonical JSON).
    """
    if isinstance(req_data, BaseModel):
        data = req_data.model_dump()
    else:
        data = dict(req_data)

    # Standardize & normalize fields
    normalized = {
        "year": int(data.get("year", 2000)),
        "month": int(data.get("month", 1)),
        "day": int(data.get("day", 1)),
        "hour": float(data.get("hour", 12)),
        "minute": int(data.get("minute", 0)),
        "second": int(data.get("second", 0)),
        "city": str(data.get("city", data.get("place", "Pune"))).strip().lower(),
        "latitude": round(float(data.get("latitude", data.get("lat", 0.0))), 4) if "latitude" in data or "lat" in data else None,
        "longitude": round(float(data.get("longitude", data.get("lon", 0.0))), 4) if "longitude" in data or "lon" in data else None,
        "timezone": str(data.get("timezone", "Asia/Kolkata")).strip(),
        "ayanamsa": str(data.get("ayanamsa", "Lahiri")).strip().lower(),
    }

    # Filter out None values to keep payload tight
    clean_payload = {k: v for k, v in normalized.items() if v is not None}

    canonical_json = json.dumps(clean_payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def chart_cache_key(input_hash: str, engine_version: str = "2.0.0") -> str:
    """
    Format standard chart cache key.
    Format: chart:{engine_version}:{input_hash}
    """
    return f"chart:{engine_version}:{input_hash}"
```

---

## 6. CACHING & QUEUE (exact)

### 6.1 `@cached_chart` Decorator & In-Memory LRU
- **Decorator Source**: Defined in `shared/cache/decorators.py` (lines 14-78).
- **In-Memory Cache**: `InMemoryTTLCache` in `shared/cache/redis_client.py` (lines 11-48).
  - Uses a standard Python dictionary `self._cache: dict[str, tuple[Any, float]]`.
  - Expiration checked lazily on `get()`.
  - **Thread-Safety Limitation**: `InMemoryTTLCache` does NOT use a `threading.Lock()` or `threading.RLock()`. In high-concurrency environments under multi-threaded servers, concurrent writes could lead to race conditions.

### 6.2 Redis Client & Fail-Open Resilience
- **Initialization**: `RedisCacheWrapper` initializes `redis.Redis.from_url(redis_url, decode_responses=True)`.
- **Fail-Open Policy**: If `redis.ping()` fails or `redis.get()` raises an exception, the exception is caught, logged with `logger.warning()`, and the request falls through seamlessly to `self._fallback_cache` or executes fresh ephemeris calculation.

### 6.3 Task Queue Subsystem
- **Queue Implementation**: `shared/queue/redis_queue.py:RedisQueue`.
- **Job States**: `QUEUED`, `RUNNING`, `COMPLETED`, `FAILED`.
- **Worker Process**: `workers/narrative_worker.py:run_worker()`.
  - Runs continuous polling loop: `asyncio.sleep(0.5)`.
  - Pulls job ID from Redis JSON list key `queue:narrative_queue`.
  - Exponential backoff retry loop: `max_retries = 3`, `asyncio.sleep(2 ** attempt)`.
  - Result stored at `narrative:job:{job_id}` with TTL of 86400 seconds (24 hours).

---

## 7. AUTH & SECURITY (exact)

### 7.1 Password Hashing & Verification
Implemented in `modules/auth/security.py`:
- Algorithm: PBKDF2 with SHA-256.
- Iterations: **120,000 rounds**.
- Salt: 16 random bytes encoded as hex (`os.urandom(16).hex()`).
- Format: `{salt}${digest}`.
- Timing-safe comparison: `hmac.compare_digest(check, digest)`.

### 7.2 Session Management & Cookies
- Starlette `SessionMiddleware` mounted in `gateway/main.py:179`:
  - Secret: `settings.session_secret_key` ("astrologic-session-secret-key-2026").
  - `same_site="lax"`.
  - `https_only=settings.is_production`.
- The cookie contains a cryptographically signed JSON payload containing `user_id` and `admin` flag.

### 7.3 Default-Deny Authorization Middleware
- Implemented in `gateway/main.py:DefaultDenyAuthMiddleware`.
- Intercepts all paths starting with `/api/`.
- If path is not in `PUBLIC_API_PREFIXES` (and not a public GET `/api/blogs`), verifies `request.session.get("user_id")` or `request.session.get("admin") == "true"`.
- Otherwise halts execution and returns `JSONResponse(status_code=401, content={"detail": "Authentication required. Default-deny policy enforced."})`.

### 7.4 RBAC & Admin Permissions
- Checked in `gateway/deps.py:require_admin` and `gateway/main.py:get_admin_cache_stats`:
  ```python
  is_admin = request.session.get("admin") == "true"
  if not is_admin:
      return JSONResponse(status_code=403, content={"detail": "Admin authorization required."})
  ```

---

## 8. TEST SUITE (exact)

### 8.1 Test Files Catalog (174 Passed, 1 Skipped)
1. `tests/backtest/test_timing_accuracy.py` (5 synthetic test cases, checks $\ge 40\%$ baseline hit rate).
2. `tests/contract/test_module_boundaries.py` (Skipped when importlinter is unconfigured).
3. `tests/integration/test_async_narrative.py` (Tests queue push, worker poll, and status transition).
4. `tests/integration/test_cache_end_to_end.py` (Tests LRU hit, Redis hit, and fail-open).
5. `tests/integration/test_module_integration.py` (Tests inter-module contract boundaries).
6. `tests/integration/test_timing_end_to_end.py` (End-to-end integration for marriage/career windows).
7. `tests/test_api_routes.py` (Validates `/api/cities`, `/api/generate-chart`, etc.).
8. `tests/test_astrology_engine.py` (Validates planetary degrees, signs, and Lagna math).
9. `tests/test_auth_and_db.py` (Tests user registration, PBKDF2 hashing, and SQLite session).
10. `tests/test_benchmark_regression.py` (20 synthetic benchmark charts, verifies byte-identical hash reproducibility).
11. `tests/test_drikpanchang_reference.py` (Validates Tithi, Nakshatra, Sunrise against DrikPanchang within 2-min tolerance).
12. `tests/test_i18n.py` (Validates translation loading across all 8 supported Indian languages).
13. `tests/test_panchang_enterprise.py` (Validates Choghadiya, Rahu Kaal, Horas, and Muhurtas).
14. `tests/test_panchang_personalization.py` (Validates Tarabala & Chandrabala matrices).
15. `tests/test_panchang_share_image.py` (Validates Pillow image card rendering).
16. `tests/test_reference_charts.py` (Validates known historical charts: Tagore, Einstein, Raman).
17. `tests/test_security_phase0.py` (Verifies fail-fast env validation, default-deny, and no hardcoded fallback passwords).
18. `tests/unit/test_cache_decorators.py`, `test_cache_envelope.py`, `test_cache_keys.py`.
19. `tests/unit/test_domain_timing_integration.py`, `test_timing_dasha.py`, `test_timing_fusion.py`, `test_timing_transit.py`, `test_transit_forecast.py`.
20. `tests/unit/test_narrative_jobs.py`, `test_queue.py`.

### 8.2 Tolerances & Oracles
- **DrikPanchang Reference**: दिल्ली (Delhi) test cases asserted to within $\pm 2$ minutes.
- **Planetary Positions**: Swiss Ephemeris Lahiri Sidereal asserted to within $0.01^\circ$ (36 arcseconds).
- **Regression Oracle**: Byte-identical SHA-256 hash across identical chart input dictionaries.

---

## 9. FRONTEND

### 9.1 Framework Architecture
- **Framework**: **Vanilla JavaScript (ES6) + HTML5 + CSS** with Jinja2 server-side rendering for template views.
- **Rendering Model**:
  - The FastAPI gateway mounts `backend/app/static` at `/static`.
  - The gateway mounts `backend/app/templates` at `/` via `Jinja2Templates`.
  - Static distribution in `frontend/` contains raw HTML files configured for edge CDN hosting via `frontend/vercel.json`.

### 9.2 Page Inventory
- `index.html`: Home page & quick chart calculation form.
- `kundali.html`: Comprehensive birth chart interactive visualizer (Rasi, Navamsa, Dashas, Yogas, Doshas).
- `prediction.html`: 10 Life Domains deep analysis and timing window cards.
- `panchang.html`: Daily Vedic calendar, Choghadiya tables, Muhurtas, Rahu Kaal countdown.
- `daily-horoscope.html`: Dynamic transit-based horoscope for 12 zodiac signs.
- `auth.html`: User login, registration, and session initialization.
- `profile.html`: User saved birth profiles.
- `blogs.html`, `blog-detail.html`: Editorial content.
- `admin-login.html`, `admin-users.html`, `admin-blog.html`, `admin-activity.html`, `admin-feedback.html`: Platform administrative portal.

### 9.3 Client Interaction & Async Narrative Polling
In `frontend/prediction.html`:
1. User submits birth details form.
2. Client sends `POST /api/prediction` with `include_narrative=true`.
3. Client immediately receives domain scores and `narrative_job_id`.
4. Client starts interval polling `GET /api/prediction/jobs/{job_id}` every 2 seconds until status becomes `completed`.
5. Client injects synthesized narrative into the DOM.

---

## 10. DEPLOYMENT & INFRA

- **Containerization**: **NOT PRESENT**. No `Dockerfile` or `docker-compose.yml` exists in the repository.
- **Swiss Ephemeris Files**: **NOT BUNDLED**. The repository contains no `.se1` data files. The system runs on Swiss Ephemeris's built-in Moshier analytical ephemeris (`swe.set_ephe_path('.')`).
- **Database Provisioning**:
  - Development / Default: Local SQLite (`sqlite:///./astrologic.db`).
  - Production (configured via `DATABASE_URL`): Supabase / PostgreSQL.
- **Background Processes**:
  - Web Server: `python -m uvicorn gateway.main:app --host 0.0.0.0 --port 8000`
  - Narrative Worker: `python workers/narrative_worker.py`
  - PDF Worker: `python workers/pdf_worker.py`
  - Startup script: `workers/start.sh`
- **Observability**:
  - Health check: `GET /health` (`{"status": "ok", "app": "...", "environment": "..."}`)
  - Metrics: `GET /metrics` (`{"cache": {"hits": ..., "misses": ..., "errors": ...}}`)

---

## 11. KNOWN GAPS, TODOS, AND DEBT

### 11.1 Zero-Byte Stub Files Leftover from Scaffolding
The following 12 files in `backend/app/` are empty (0 bytes) stubs that should be deleted:
- `backend/app/ai/__init__.py`, `llm_service.py`, `prompt_builder.py`, `rag_service.py`
- `backend/app/schemas/__init__.py`, `auth_schema.py`, `feedback_schema.py`, `user_schema.py`
- `backend/app/services/__init__.py`, `ai_service.py`, `prediction_service.py`, `user_service.py`
- `backend/app/utils/__init__.py`, `date_utils.py`, `helpers.py`, `validators.py`
- `backend/app/astrology/julian.py`

### 11.2 Divergences Between LLD and Codebase
1. **Shodashvarga (D1..D60)**: LLD claims 16 divisional charts. Code only implements D9 Navamsa (`modules/kundali/varga.py`).
2. **Dasha Recursion Depth**: LLD claims recursion to SD and PrD. Code only subdivides to PD (`DASHA_DEPTH = "PD"`).
3. **Missing Module Files**:
   - LLD references `modules/kundali/planet_engine.py`, `house_engine.py`, `varga_engine.py`, `dasha_engine.py`. In code, these are named `planets.py`, `houses.py`, `varga.py`, `dasha.py`.
   - LLD references `modules/kundali/service.py`. In code, `KundaliService` is embedded inside `modules/kundali/api.py`.
4. **Endpoint Mismatch**: LLD claims `POST /api/timing`. Code implements `POST /api/prediction/timing/{domain}`.
5. **Auth Enforcement**: LLD claims `/api/kundali` and `/api/prediction` require no auth. Code enforces strict default-deny (`DefaultDenyAuthMiddleware`), returning 401 without an active session.

### 11.3 Technical Debt & God Classes
- `modules/panchang/personalization.py`: **914 lines** (God class).
- `modules/panchang/engine.py`: **710 lines** (God class).
- `modules/kundali/cities.py`: Only contains **~40 static cities**. Lookups fail for all other global coordinates.
- Deprecated Pydantic V2 call: `result.dict()` in `modules/narrative/jobs.py:91`.

---

## 12. PERFORMANCE BASELINE

- **Cached Chart Calculation**: **0.15 ms – 0.35 ms** (LRU memory hit).
- **Uncached Chart Calculation**: **12 ms – 15 ms** (Swiss Ephemeris Julian Day + planets + houses).
- **10 Domains Full Analysis**: **25 ms – 35 ms** (rule-based evaluation).
- **15-Year Timing Fusion Engine (10 domains)**: **40 ms – 50 ms**.
- **LLM Synthesis (Worker Thread)**:
  - Ollama local inference: 1,800 ms – 3,500 ms.
  - OpenAI API inference: 800 ms – 1,500 ms.
  - Rule-based fallback synthesis: **< 1 ms**.
- **Observability Counters**: Real-time hit/miss/error telemetry exposed at `GET /metrics`.

---

## 13. ACCURACY BASELINE (critical for my next step)

- **Ephemeris Version**: `pyswisseph==2.10.3.2`.
- **Ephemeris Data Files**: **None bundled**. Operates in Moshier analytical mode.
- **JPL Horizons Validation**: **None performed**.
- **DrikPanchang Reference Validation**: Performed and verified within **$\pm 2$ minutes** for sunrise, sunset, tithi, and nakshatra transitions in `tests/test_drikpanchang_reference.py`.
- **Timezone Resolution Reality**:
  - `modules/kundali/engine.py:102` **hardcodes `ist_offset = 5.5`**. All charts computed directly through `calculate_kundali` assume Indian Standard Time!
  - `shared/timezone/tz.py:get_local_now()` ignores requested timezone and returns `now_ist()`.
- **Ambiguous DST Handling**: **Not implemented**. Pre-1970 historical international DST transitions fall back to static offsets.
- **Birth-Time Precision**:
  - Binary boundary warning exists in `modules/kundali/engine.py:207`: `is_near_boundary = lagna_deg_in_sign < 2.0 or lagna_deg_in_sign > 28.0`.
  - **No `birth_time_accuracy` field exists on any request schema**.
  - **No sensitivity analysis or uncertainty propagation exists anywhere in the codebase today**.

---

## 14. EXTENSION READINESS FOR MY NEXT TASK

Below is the concrete implementation blueprint for your planned extensions:

### (i) `birth_time_accuracy` Field End-to-End
- **Files to Modify**:
  - `modules/kundali/schemas.py`: Add `birth_time_accuracy: Optional[int] = Field(0, description="Uncertainty in minutes (e.g. ±5, ±15)")` to `KundaliRequest`.
  - `modules/prediction/schemas.py`: Add to `PredictionRequest` and `DomainRequest`.
  - `shared/cache/keys.py:compute_input_hash()`: Include `birth_time_accuracy` in canonical JSON. Otherwise, requests with different uncertainty windows would return the same cached exact-time chart.
  - `modules/auth/models.py:UserProfile`: Add `birth_time_accuracy = Column(Integer, default=0)`.
  - `modules/kundali/engine.py:calculate_kundali()`: Accept `uncertainty_minutes: int = 0`.
- **New Tests**: `tests/unit/test_birth_time_accuracy.py` verifying cache key differentiation and model validation.
- **Effort**: **Small (S)**.

### (ii) `POST /api/kundali/sensitivity` Endpoint (±N Minutes Stability)
- **Files to Modify**:
  - `modules/kundali/api.py`: Add route `@router.post("/kundali/sensitivity")`.
  - `modules/kundali/engine.py`: Implement `calculate_chart_sensitivity(year, month, day, hour, min, lat, lon, delta_minutes=15)`.
    - Computes chart at $T - \Delta t$, $T$, and $T + \Delta t$.
    - Checks if Lagna sign changes, Navamsa sign changes, Nakshatra changes, or Mahadasha changes.
- **New Schema**: `SensitivityResponse(is_lagna_stable: bool, lagna_shift_minutes: int, navamsa_stable: bool, dasha_stable: bool)`.
- **New Tests**: `tests/integration/test_sensitivity.py`.
- **Effort**: **Medium (M)**.

### (iii) Lagna/Nakshatra/Varga Stability Flags in Every Response
- **Files to Modify**:
  - `modules/kundali/schemas.py:KundaliResponse`: Add `stability: Dict[str, Any]`.
  - `modules/kundali/engine.py:calculate_kundali`:
    - Calculate angular distance to nearest Lagna boundary: $\min(	ext{deg}, 30 - 	ext{deg})$.
    - Calculate angular distance to nearest Navamsa boundary: $\min(	ext{deg} \pmod{3.333}, 3.333 - (	ext{deg} \pmod{3.333}))$.
    - Set `lagna_stable = min_lagna_dist > (delta_minutes / 4.0)` (since Lagna moves $1^\circ$ every 4 mins).
- **New Tests**: `tests/unit/test_stability_flags.py`.
- **Effort**: **Small (S)**.

### (iv) Automatic Confidence Downgrade When Unstable
- **Files to Modify**:
  - `modules/prediction/timing_fusion.py:get_confidence_tier(score: float, is_stable: bool = True) -> str`:
    ```python
    if not is_stable:
        # Cap confidence at "Moderate" if Lagna or Dasha is boundary-unstable
        if score >= 0.75:
            return "Moderate (Uncertainty Adjusted)"
        elif score >= 0.55:
            return "Possible (Uncertainty Adjusted)"
        return "Unlikely"
    ```
  - Pass `is_stable` flag from `chart` into `fuse_windows()`.
- **New Tests**: `tests/unit/test_confidence_downgrade.py`.
- **Effort**: **Small (S)**.

### (v) Ephemeris Version Pinning in Cache Keys
- **Files to Modify**:
  - `shared/cache/keys.py`:
    ```python
    import swisseph as swe
    SWE_VERSION = getattr(swe, "__version__", "2.10.3")

    def chart_cache_key(input_hash: str, engine_version: str = "2.0.0") -> str:
        return f"chart:{engine_version}:swe{SWE_VERSION}:{input_hash}"
    ```
- **Migration Steps**: Bump cache version to `2.1.0`. All old cached entries will expire naturally or can be flushed via `POST /api/admin/cache/flush`.
- **Effort**: **Small (S)**.

### (vi) LLM Prompt PII Redaction + Output Safety Filter
- **Files to Modify**:
  - `modules/narrative/prompt_builder.py`: Explicitly sanitize input context. Strip names, emails, IPs, city strings, and exact birth timestamps. Only pass astrological identifiers (`Lagna: Virgo, 10th Lord: Mercury in Gemini, Jupiter Dasha`).
  - `modules/narrative/llm_client.py`:
    - Add `OutputSafetyFilter.sanitize(text: str) -> str`:
      Regex-intercept fatalistic keywords (e.g. death predictions, fatal accidents, incurable diseases, curses) and replace with constructive ethical Vedic advisory language.
- **New Tests**: `tests/unit/test_llm_safety.py`.
- **Effort**: **Medium (M)**.

### (vii) Rate Limiting on `/api/prediction`
- **Files to Modify**:
  - `astro-platform/backend/requirements.txt`: Add `slowapi`.
  - `gateway/main.py`:
    ```python
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded

    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    ```
  - `modules/prediction/api.py`: Decorate `@limiter.limit("10/minute")`.
- **Effort**: **Small (S)**.

### (viii) Argon2id Migration for Passwords
- **Files to Modify**:
  - `requirements.txt`: Add `argon2-cffi`.
  - `modules/auth/security.py`:
    ```python
    from argon2 import PasswordHasher
    from argon2.exceptions import VerifyMismatchError

    ph = PasswordHasher(time_cost=2, memory_cost=102400, parallelism=8)

    def hash_password(password: str) -> str:
        return ph.hash(password)

    def verify_password(password: str, stored_hash: str) -> bool:
        if stored_hash.startswith("$argon2"):
            try:
                return ph.verify(stored_hash, password)
            except VerifyMismatchError:
                return False
        # Transparent backward-compatibility fallback to PBKDF2:
        return _verify_legacy_pbkdf2(password, stored_hash)
    ```
  - `modules/auth/api.py`: On login, if password verified via legacy PBKDF2, transparently update database with `user.password_hash = hash_password(password)`.
- **Effort**: **Small (S)**.

---
*End of Implementation Deep-Dive Review Document.*
