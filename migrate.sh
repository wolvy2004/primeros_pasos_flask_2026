#!/bin/bash

docker compose exec backend flask db migrate -m $1