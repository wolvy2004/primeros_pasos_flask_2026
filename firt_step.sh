#!/bin/bash
docker compose exec backend flask db upgrade
docker compose exec backend python seeder.py
