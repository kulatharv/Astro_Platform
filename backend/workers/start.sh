#!/bin/bash
# Start worker loop for narrative background jobs

echo "Starting Astro-Platform Narrative Background Worker..."
export WORKER_CONCURRENCY=${WORKER_CONCURRENCY:-4}
python workers/narrative_worker.py
