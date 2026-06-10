#!/usr/bin/env bash
cd "$(dirname "$0")/.."
docker compose -f docker/docker-compose.yml down 2>/dev/null || \
  docker-compose -f docker/docker-compose.yml down
echo "Infra stopped."
