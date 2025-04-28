#!/bin/sh

docker compose run --rm api pytest -v && docker compose down
