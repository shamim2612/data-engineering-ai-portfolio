SELECT
  peak_hour,
  COUNT(*) AS trip_count,
  ROUND(AVG(trip_duration_min), 2) AS avg_trip_duration_min,
  ROUND(AVG(trip_distance), 2) AS avg_distance_miles
FROM d610_taxi.yellow_taxi_weekday_curated
GROUP BY peak_hour
ORDER BY peak_hour;
