# Background Narrative Generation Workers

The narrative generation worker asynchronously processes LLM predictions for marriage and career using a Redis job queue.

## Operational Setup

### 1. Environment Variables

- `REDIS_URL`: Redis server connection URL (Default: `redis://localhost:6379/0`)
- `WORKER_CONCURRENCY`: Number of concurrent worker threads/tasks (Default: `4`)
- `JOB_TTL_SECONDS`: Lifetime of completed/failed job records in Redis (Default: `86400` / 24 hours)
- `MAX_RETRIES`: Maximum transient retry attempts (Default: `3`)

### 2. Starting Worker Process

Run the worker event loop process:
```bash
python workers/narrative_worker.py
```

Alternatively, use the shell runner script:
```bash
./workers/start.sh
```

### 3. Worker Healthcheck

Verify worker status by querying Redis queue state:
```bash
python -c "from shared.queue.redis_queue import default_queue; print(default_queue.queue_name)"
```
