# Pipeline to extract data from FDS API

## Dev Setup
```
docker compose -f local_dev.yml down --volumes
docker compose build --no-cache
docker compose -f local_dev.yml up --force-recreate --verbose
```