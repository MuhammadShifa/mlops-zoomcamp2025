# MLOps Zoomcamp — Monitoring Module

#### Quick Recap
We have learnt how to run and track ML experiments, and deploy the chosen models into production. The prediction services are now up and running, and generating predictions for given data.
So are we done now?

No, not yet. With time the business concept changes and so is the data. We need to be cognizant about the model performance from time to time so as to take timely appropriate action.

### Monitoring ML Models
Monitoring ML models in production is a critical part of MLOps. It ensures that models continue to deliver value while remaining reliable, fair, and aligned with business goals. Below is a detailed summary of what I covered in the Monitoring module of the MLOps Zoomcamp, with additional insights and best practices.

---

### ✅ **How to monitor models in production?**

Monitoring can be divided into several key areas:

---

#### 1️⃣ **Service Health**
- The first priority is to ensure that the service is available and functional.
- Monitor system-level metrics like:
  - **Latency**
  - **Throughput**
  - **Error rates**
  - **Uptime**
- Tools: Prometheus for metric collection, Grafana for visualization and alerting.

---

#### 2️⃣ **Model Performance**
- Track how well the model is performing with respect to its intended task.
- Metrics depend on the problem type:
  - **Classification:** Log loss, precision, recall, F1 score, ROC AUC
  - **Regression:** Mean Absolute Error (MAE), Root Mean Squared Error (RMSE)
  - **Ranking/Recommender:** NDCG, MAP, hit rate
- Performance monitoring can be challenging in the absence of immediate ground truth — delayed feedback should be handled carefully.

---

#### 3️⃣ **Data Quality and Integrity**
- Ensure that input data is valid and matches the expected format:
  - Check for **missing values**
  - Check for **data types**
  - Monitor **value ranges**
  - Validate against **business rules**
- Can also compare production data characteristics to those seen during training (e.g. counts, distributions).

---

#### 4️⃣ **Data Drift and Concept Drift**
- Even if data quality is acceptable, the environment might change:
  - **Data drift:** Input data distribution changes over time.
  - **Concept drift:** The relationship between features and target changes.
- Monitor distributions of inputs and outputs; use statistical tests or divergence measures (e.g. KL divergence, PSI).

---

#### ➕ **Other important monitoring dimensions**
- **Performance by segment:** Does performance vary across user groups or regions?
- **Bias and fairness:** Are predictions equitable across sensitive attributes?
- **Outliers:** Identify anomalous inputs or predictions.
- **Explainability:** Ensure model decisions can be interpreted; monitor changes in feature importance over time.

---

### 🏛️ **Monitoring Architectures**

#### Batch (Offline) Monitoring
- Suitable for batch scoring systems.
- Metrics are computed at intervals (e.g. daily or weekly).
- Good for drift detection, performance reports, fairness audits.

#### Online (Real-time) Monitoring
- Suitable for online/streaming systems.
- Metrics are computed in near real-time.
- Useful for service health, latency monitoring, and fast anomaly detection.

---

### ⚙️ **Tooling**
- **Evidently:** Provides ready-to-use monitors for data drift, concept drift, data quality, target drift, and model performance. It generates interactive reports and dashboards that can be reviewed manually or incorporated into automated monitoring pipelines.
- **Custom monitoring code:** Use Python or other languages to compute ML-specific metrics, generate reports, or create custom checks for your model.
- **Grafana (optional):** Can be used for dashboarding and alerting if integrated with a metrics store (e.g. via custom exporters or database connections).
- **Alerting:** You can implement custom alerting (e.g. via scripts, Slack notifications, or email) based on Evidently outputs or custom monitoring logic.

👉 Combine model-level monitoring (e.g. data drift, performance metrics) with any infrastructure monitoring tools you use to achieve end-to-end visibility of production health.

---

### 💡 **Key Takeaways**
- Monitoring is not one-size-fits-all — it depends on the business case, model type, and risk tolerance.
- A comprehensive monitoring strategy covers:
  - **System health**
  - **Model quality**
  - **Data integrity**
  - **Drift**
  - **Fairness & explainability**
- **Grafana dashboards** provide a clear, visual way to keep an eye on both system and model metrics.
----
  ### 🛠️ **Practical Work**
----
- **Environment Setup:**  
  Set up the environment using `pipenv` and installed all necessary packages via `requirements.txt`.
    
  Used `docker-compose` to manage supporting services:
  - **PostgreSQL** for storing data and metadata.
  - **Adminer** for database management, accessible at [http://localhost:8080/](http://localhost:8080/)
  - **Grafana** for monitoring visualization, accessible at [http://localhost:3000/login](http://localhost:3000/login)

- **Data + Model Pipeline:**  
  All practical work is contained in `baseline_model_nyc_taxi_data.ipynb`:
  - Downloaded the NYC taxi dataset.
  - Preprocessed the data for training.
  - Trained a **Linear Regression** model.
  - Saved the trained model for reuse.
  - Saved validation results as **Parquet** files to use as reference data for monitoring.

- **Monitoring:**  
  - Generated **Evidently reports** to assess data quality, drift, and model performance.
  - Created an **Evidently dashboard** for detailed visual analysis.

✅ Everything — from data download and model training to saving artifacts and producing monitoring outputs — is included in the notebook:  
`baseline_model_nyc_taxi_data.ipynb`

 **Dummy Metrics Calculation**

- **File:** `dummy_metrics_calculation.py`
- Initializes a `test` database and creates a `dummy_metrics` table in PostgreSQL.
- Generates and inserts synthetic metrics:
  - `timestamp`: Current time in the Europe/London timezone.
  - `value1`: Random integer between 0 and 1000.
  - `value2`: Random UUID string.
  - `value3`: Random float between 0 and 1.
- Sends new records every **10 seconds**, producing 100 records in total.
- Uses `psycopg` for database connections and inserts, with `logging` for status updates.
- Designed to simulate a metric stream for testing and validating monitoring setups (e.g., Grafana dashboards).

**Evidently Metrics Calculation**

- **File:** `evidently_metrics_calculation.py`
- Sets up the `test` PostgreSQL database and creates the `dummy_metrics` table for storing monitoring metrics.
- Loads:
  - Reference dataset (`reference.parquet`)
  - Trained linear regression model (`lin_reg.bin`)
  - Raw NYC taxi trip data (`green_tripdata_2022-02.parquet`)
- Computes key metrics using **Evidently**:
  - `prediction_drift`: Drift score of model predictions
  - `num_drifted_columns`: Number of drifted columns
  - `share_missing_values`: Proportion of missing values in current batch
- Processes data in **27 hourly segments**, inserting results every 10 seconds.
- Uses **Prefect** to orchestrate batch monitoring backfill and simulate real-world monitoring.
- Suitable for validating data and model monitoring dashboards (e.g., Grafana) and alerting systems.

📊 **Grafana Visualization**

- Connected **Grafana** to the PostgreSQL `test` database to display and monitor metrics stored in `dummy_metrics`.
- Created dashboard panels to visualize:
  - **prediction_drift**: Track drift in model predictions over time.
  - **num_drifted_columns**: Monitor the number of features showing drift at each timestamp.
  - **share_missing_values**: Observe trends in data completeness and quality.
- Configured time-series graphs and set thresholds to highlight drift or quality issues visually.
- Added alert rules to notify when metrics exceed defined limits, enabling proactive issue detection.
- Access the Grafana dashboard at [http://localhost:3000/](http://localhost:3000/) (default user: `admin`, password: `admin`).

### 🐞 **Debugging NYC Taxi Data**

- **File:** `debugging_nyc_taxi_data.ipynb`
- Performed data drift debugging using **Evidently Test Suites** and **Reports**.
- Steps:
  - Loaded reference data, problematic data, and the trained model.
  - Generated predictions for the problematic data (after filling missing values with `0`).
  - Defined a **ColumnMapping** specifying:
    - `prediction`: Prediction column name
    - `numerical_features`: List of numerical features
    - `categorical_features`: List of categorical features
    - `target`: Set to `None` (no true target provided)
  - Created and ran an **Evidently Test Suite** with `DataDriftTestPreset` to automatically test for drift between reference and problematic data.
  - Generated an **Evidently Report** with `DataDriftPreset` for a detailed visual analysis of drift metrics.
  - Displayed both the test suite results and report inline in the notebook.
- Enabled detection and visualization of data drift issues to support debugging and improve data quality.

---

### ✅ **Summary**

This project implements end-to-end **model monitoring** for a batch ML pipeline. We set up the environment using Docker
(PostgreSQL, Adminer, Grafana), trained and saved a linear regression model, and generated reference data. 
Using **Evidently**, we calculated drift and data quality metrics, stored them in PostgreSQL, and 
visualized them in **Grafana** dashboards. Prefect flows handled orchestration, and **Evidently Test Suites**
helped debug and validate data drift issues.

-----
