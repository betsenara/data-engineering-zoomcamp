# Homework 1: Docker, SQL, and Terraform  
Data Engineering Zoomcamp 2026

---

## Question 1: pip version in `python:3.13` image
```
docker run -it --rm --entrypoint=bash python:3.13.11-slim
pip --version

pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```
Answer: 25.3

---

## Question 2: pgAdmin connection hostname and port

Answer: db:5432

---

## Question 3: Trips in November 2025 with `trip_distance <= 1`
```
docker compose -f docker/docker-compose.yml up -d
```
```
uv run python pipelines/ingest_data.py `
--pg-user root `
--pg-pass root `
--pg-host localhost `
--pg-port 5432 `
--pg-db ny_taxi `
--target-table green_tripdata_2025_11 `
--source "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
```
```
uv run python pipelines/ingest_data.py `
--pg-user root `
--pg-pass root `
--pg-host localhost `
--pg-port 5432 `
--pg-db ny_taxi `
--target-table taxi_zone_lookup `
--source "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
```

```sql
SELECT COUNT(*)
FROM green_tripdata_2025_11 g
WHERE g.lpep_pickup_datetime >= '2025-11-01'
AND g.lpep_pickup_datetime < '2025-12-01'
AND g.trip_distance <= 1
```
Answer: 8007

---

## Question 4: Pickup day with the longest trip distance (trip_distance < 100)
```
SELECT g.trip_distance, g.lpep_pickup_datetime
FROM green_tripdata_2025_11 g
WHERE g.trip_distance < 100
ORDER BY g.trip_distance DESC
LIMIT 5
```
Answer: 2025-11-14

---

## Question 5: Pickup zone with the largest total_amount on November 18, 2025
```
SELECT t."Zone", SUM(d.total_amount) AS sum_total_amount
FROM green_tripdata_2025_11 d
JOIN taxi_zone_lookup t
ON d."PULocationID" = t."LocationID"
WHERE d.lpep_pickup_datetime >= '2025-11-18'
AND d.lpep_pickup_datetime < '2025-11-19'
GROUP BY t."Zone"
ORDER BY sum_total_amount DESC
LIMIT 5
```
Answer: East Harlem North

---

## Question 6: Drop-off zone with the largest tip (pickup zone: East Harlem North)
```
SELECT t."Zone", MAX(g.tip_amount) AS max_tip
FROM green_tripdata_2025_11 g
JOIN taxi_zone_lookup t
ON g."DOLocationID" = t."LocationID"
WHERE g.lpep_pickup_datetime >= '2025-11-01'
AND g.lpep_pickup_datetime < '2025-12-01'
AND g."PULocationID" = (
  SELECT "LocationID"
  FROM taxi_zone_lookup
  WHERE "Zone" = 'East Harlem North'
)
GROUP BY t."Zone"
ORDER BY max_tip DESC
LIMIT 5
```
Answer: Yorkville West

---

## Question 7: Terraform workflow sequence
```
terraform init
terraform apply -auto-approve
terraform destroy
```
Answer: terraform init, terraform apply -auto-approve, terraform destroy
