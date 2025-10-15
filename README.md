# P21_Data-Flow-Simulation

**VERSION 1 - DATA INTEGRITY SYSTEM DESIGN & SYSTEM SIMULATION**

**A. Project Overview**

- A data integrity and validation pipeline designed to ensure weekly operational consistency across all domains (Operational, MES, Accounting and Logistics) before data is consolidated for analytics and Power BI dashboards.
- This version focuses on data validation, cleaning, schema alignment, and master data merging.

**B. Dataset Information**

_**Source**_

| Field      | Description                                                          |
| ---------- | -------------------------------------------------------------------- |
| Source     | Realistic simulated data generated for operational process testing   |
| Frequency  | Weekly uploads                                                       |
| File Types | Operational, MES, Accounting, Logistics                              |
| Format     | CSV (`<FileType>_YYYYW##.csv`, e.g., `Operational_Data_2025W41.csv`) |


**C. Methodology**

- Framework used: Python
- Approach: Modular pseudo-coding, replicating a real-world ETL pipeline structure.

**D. System Logic Overview & Actionable Plans**

**System Logic Overview**

_**1. File Detection & Initialization**_

- Monitor folder /Weekly_Uploaded/ for new .csv files.
- Validate presence of all 4 required domains (Operational_Data, MES_Data, Accounting_Data, Logistics_Data).
- Auto-create log file Validation_Log.csv if missing.
- Naming pattern enforced: <FileType>_YYYYW##.csv → e.g. MES_Data_2025W41.csv.
- If fewer than 4 files detected → stop pipeline & log “Incomplete Upload” status.

_**2. File Validation**_

- Each file passes through schema and format validation:
  + Check file type: ensure .csv format, rename automatically if needed.
  + Check schema: compare columns against expected templates.
  + Log errors to Validation_Log.csv if missing columns or mismatched schema.

| File Type   | Expected Columns                                                                                                                                                                                |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Operational | batch_id, date, shift, egg_weight_g, larvae_age_day, larvae_weight_kg, feed_intake_kg, mortality_rate, drying_temp_avg, drying_duration_min, moisture_after_dry, output_kg, defect_kg, operator |
| MES         | batch_id, sensor_id, avg_temp, humidity, drying_time_min, chamber_id, vibration_alert                                                                                                           |
| Accounting  | batch_id, feed_cost, electricity_cost, maintenance_cost, labor_cost, packaging_cost, total_cost, cost_date                                                                                      |
| Logistics   | batch_id, truck_id, shipment_date, destination, delivery_status, weight_kg, delay_hour, driver_name                                                                                             |

_**3. Data Cleaning**_

- Normalize column names → lowercase & trim spaces.
- Remove blank rows.
- Standardize data types (date, numeric, string).
- Detect outliers using IQR method (Interquartile Range).
- Export cleaned files → /Clean_Data/.
- Output: [FileType]_cleaned.csv

_**4. Master Data Appending**_

- Each cleaned dataset is appended to its corresponding master dataset:

| Cleaned File                 | Master Target          |
| ---------------------------- | ---------------------- |
| Operational_Data_cleaned.csv | Master_Operational.csv |
| MES_Data_cleaned.csv         | Master_MES.csv         |
| Accounting_Data_cleaned.csv  | Master_Accounting.csv  |
| Logistics_Data_cleaned.csv   | Master_Logistics.csv   |

- Remove duplicates by batch_id (keep latest).
- Log results: “Appended to Master”.

_**5. Master Merging**_

- Merge all 4 master files on batch_id (LEFT JOIN) to create one consolidated dataset: Operational + MES + Accounting + Logistics → Master_Data_All.csv
- Output: Master_Data_All.csv — base for analytical dashboards.

_**6. Weekly Validation Log & Escalation**_

- All operations (validation, cleaning, merging) are logged into Validation_Log.csv with timestamp and status.
- This ensures traceability for future audits or automation.

**VERSION 2 - ROOT CAUSE SIMULATION**

**A. Project Overview**

- This project builds an automated Root Cause Simulation System that detects operational anomalies from weekly production data

**B. Dataset Information**

- Master_Data_All.csv – consolidated dataset from Version 1.

**C. Direction**

- Define acceptable range.
- Apply rule-based conditions.
- Generate reports:
  + Root_Cause_Report.csv → detailed batch-level anomalies.
  + Root_Cause_Summary.csv → summary of root-cause counts.
- Log activity to Validation_Log.csv.

**About Me**

Hi, I'm Navin (Bao Vy) – an aspiring Data Analyst passionate about turning raw data into actionable business insights. I’m eager to contribute to data-driven decision making and help organizations translate analytics into business impact. For more details, please reach out at:

🌐 LinkedIn: https://www.linkedin.com/in/navin826/

📂 Portfolio: https://github.com/CallmeNavin/
