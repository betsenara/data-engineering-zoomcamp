# Homework 3: Data Warehousing & BigQuery
Data Engineering Zoomcamp 2026

---

## Question 1: Counting records

We created external table and table with the following:
```sql
CREATE OR REPLACE EXTERNAL TABLE
  `advance-subject-485403-c4.ny_taxi.external_yellow_tripdata_2024`
OPTIONS (
  format = 'PARQUET',
  uris = [
    'gs://dezoomcamp-hw3-yellow-2024-betul-001/yellow_tripdata_2024-*.parquet'
  ]
);
```
and 
```sql
CREATE OR REPLACE TABLE `advance-subject-485403-c4.ny_taxi.yellow_tripdata_2024` AS
SELECT * FROM `advance-subject-485403-c4.ny_taxi.external_yellow_tripdata_2024`;
```
Next we used the following query:

```sql
SELECT COUNT(*)
FROM `advance-subject-485403-c4.ny_taxi.external_yellow_tripdata_2024`
```
Answer: 20,332,093

---

## Question 2: Data read estimation
```sql
SELECT COUNT(*)
FROM `advance-subject-485403-c4.ny_taxi.external_yellow_tripdata_2024`
```
and 
```sql
SELECT COUNT(DISTINCT PULocationID)
FROM `advance-subject-485403-c4.ny_taxi.yellow_tripdata_2024`;
```
Answer: 0 MB for the External Table and 155.12 MB for the Materialized Table

---

## Question 3: Understanding columnar storage
We have the following queries:
```sql
SELECT PULocationID
FROM `advance-subject-485403-c4.ny_taxi.yellow_tripdata_2024`;
```
and
```sql
SELECT PULocationID, DOLocationID
FROM `advance-subject-485403-c4.ny_taxi.yellow_tripdata_2024`;
```
Answer: BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

---

## Question 4: Counting zero fare trips
```sql
SELECT COUNT(*)
FROM `advance-subject-485403-c4.ny_taxi.external_yellow_tripdata_2024`
WHERE fare_amount=0;
```

Answer: 8,333

---

## Question 5: Partitioning and clustering
Partitioning and clustering is done with:
```sql
CREATE OR REPLACE TABLE `advance-subject-485403-c4.ny_taxi.yellow_tripdata_2024_optimized`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT *
FROM `advance-subject-485403-c4.ny_taxi.yellow_tripdata_2024`;
```

Answer: Partition by tpep_dropoff_datetime and Cluster on VendorID

---

## Question 6: Partition benefits
```sql
SELECT DISTINCT VendorID
FROM `advance-subject-485403-c4.ny_taxi.yellow_tripdata_2024_optimized`
WHERE tpep_dropoff_datetime >= '2024-03-01'
  AND tpep_dropoff_datetime <  '2024-03-16';
```
and

```sql
SELECT DISTINCT VendorID
FROM `advance-subject-485403-c4.ny_taxi.yellow_tripdata_2024`
WHERE tpep_dropoff_datetime >= '2024-03-01'
  AND tpep_dropoff_datetime <  '2024-03-16';
```
Answer: 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table

---

## Question 7: External table storage
An external table in BigQuery does not store the data inside BigQuery storage. It only stores metadata (schema + pointers). The actual data remains in Google Cloud Storage (GCS)

Answer: GCP Bucket
---

## Question 8: Clustering best practices
Clustering is **not always** a best practice in BigQuery.

Clustering is helpful only when:
- We frequently filter, group by, or sort on specific columns
- The table is large enough for clustering to matter
- Query patterns are stable and predictable

It’s not recommended when:
- Tables are small (benefit is negligible)
- Query patterns change often
- We don’t consistently filter or group by the same columns
- We already get good performance from partitioning alone

Answe:False
---

## Question 9: Understanding table scans
The COUNT(*) query reads 0 bytes because BigQuery can return the total row count using table metadata without scanning any column data.
Answer: 0b
