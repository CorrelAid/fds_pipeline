# Pipeline to extract data from FDS API


## Jobs
This Dagster project consists of three jobs: proc_insert, proc_insert_jurisdictions and proc_insert_campaigns.

### proc_insert
Given an id, will 
1. get the corresponding foi request from API, extract the needed fields from the foi request itself and its public body and messages.
2. generate a sql string to insert/update the foi request, public_body and messages
3. execute these sql strings

proc_insert_jurisdictions and proc_insert_campaigns does the same but for multiple objects (campaigns and jurisdictions respectively
)
## Schedules
proc_insert_jurisdictions and proc_insert_campaigns are executed once every hour

## Sensors
proc_insert is executed based on the evaluation of a sensor. If the database contains less entries than the api, the sensor retreives the highest id in the database or the id in the cursor(jobs can result in not inserting a foi request when an id doesnt exist in api) and makes a run request for a number of proc_insert jobs with ids that are not already in db.

## Dev Setup
1. Clone Repo

2. Install requirements

```
poetry install
```
3. Set up pre commit hook

```
poetry run pre-commit install 
```
4. Create an .env file with following contents:

```
AWS_ACCESS_KEY_ID=minio
AWS_SECRET_ACCESS_KEY=minio123
MINIO_ENDPOINT_URL=http://localhost:9000
MINIO_BUCKET=main
POSTGRES_USER=dagster
POSTGRES_PASSWORD=dagster
POSTGRES_DB=main
POSTGRES_PORT=5436
POSTGRES_HOST=localhost
```

5. Create necessary infrastructure

```
docker compose -f local_dev.yml down --volumes
docker compose build --no-cache
docker compose -f local_dev.yml up --force-recreate --verbose
```

This will spin up a postgres database and minio s3 storage.

6. Run the dagster daemon and GUI or only GUI

Daemon and GUI:
```
poetry run dagster dev
```
GUI:
```
poetry run dagit
```