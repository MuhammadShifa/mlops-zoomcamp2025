import psycopg

with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example") as conn:
    with conn.cursor() as curr:
        curr.execute("SELECT MAX(metric_value) FROM quantile_metrics;")
        max_median = curr.fetchone()[0]
        print(f"Max daily median fare from DB: {max_median}")
