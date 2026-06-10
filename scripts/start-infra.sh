#!/usr/bin/env bash
cd "$(dirname "$0")/.."
docker compose -f docker/docker-compose.yml up -d 2>/dev/null || \
  docker-compose -f docker/docker-compose.yml up -d
echo "Infra started: SearXNG on :4004, FlareSolverr on :8191"
