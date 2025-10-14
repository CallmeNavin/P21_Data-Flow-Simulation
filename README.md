# P21_Data-Flow-Simulation

**VERSION 1 - DATA INTEGRITY SYSTEM DESIGN & DATA CONSISTENCY, ROOT CAUSE SIMULATION**

**A. Project Overview**

- Design a weekly data validation & consolidation system to ensure data consistency and reliability across all operational domains (Operational, MES, Accounting and Logistics) before loading into analysis or Power BI dashboards.

**B. Dataset Information**

_**Source**_

- Realistics Simulated

**C. Methodology**

- Pseudo Coding

**D. System Logic Overview & Actionable Plans**

**System Logic Overview**

**1. File Detection & Initialization:**
- Monitor folder /Weekly_Uploaded/ for new weekly .csv files.
(Naming pattern: <FileType>_YYYYW##.csv, e.g., MES_Data_2025W41.csv)
- Identify all 4 expected file types: Operational_Data, MES_Data, Accounting_Data, Logistics_Data. 

→ If fewer than 4 detected → flag “Incomplete Week Upload” in Validation_Log.csv and stop process.
- Check for Validation_Log.csv and all Master_*.csv files. 

→ If missing: auto-create with headers: Validation_Log.csv = [ File_Name, File_Type, Upload_Date, Upload_By, Status, Error_Message ]

**2. File Validation (for each new file):**
- Detect file type: (Operational / MES / Accounting / Logistics).

→ If not .csv: convert to .csv. Log errors & warnings to Validation_Log.csv.
- Validate file name format: Must follow template <Type>_YYYYW##.csv.

→ If mismatch: auto-rename + log errors & warnings to Validation_Log.csv.
- Validate schema: Compare actual columns vs expected template.

→ If mismatch: log to Validation_Log.csv and skip file.
- File Type	Expected Columns

| File Type   | Expected Columns                                |
| ----------- | ----------------------------------------------- |
| Operational | batch_id, date, shift, egg_weight_g, larvae_age_day, larvae_weight_kg, feed_intake_kg, mortality_rate, drying_temp_avg, drying_duration_min, moisture_after_dry, output_kg, defect_kg, operator         |
| MES         | batch_id, sensor_id, avg_temp, humidity, drying_time_min, chamber_id, vibration_alert |
| Accounting  | batch_id, feed_cost, electricity_cost, maintenance_cost, labor_cost, packaging_cost, total_cost, cost_date                        |
| Logistics   | batch_id, truck_id, shipment_date, destination, delivery_status, weight_kg, delay_hour, driver_name       |

**3. Data Cleaning (for each validated file):**
- Standardize column formats (string / float / datetime).
- Remove blank rows.
- Detect and highlight outliers or abnormal patterns.
- Save as [FileName]_cleaned.csv → folder /Clean_Data/.

**4. Append Clean Data**
- Append each cleaned file to its corresponding master file under folder /Master_Data/:

| Cleaned File                 | Target Master File     |
| ---------------------------- | ---------------------- |
| Operational_Data_cleaned.csv | Master_Operational.csv |
| MES_Data_cleaned.csv         | Master_MES.csv         |
| Accounting_Data_cleaned.csv  | Master_Accounting.csv  |
| Logistics_Data_cleaned.csv   | Master_Logistics.csv   |

→ Log append results into Validation_Log.csv (including timestamp and status).

**5. Merge Master Files**
- After all four master files are updated: Merge them by Batch_ID and update it to Master_Data_All.csv file.

**6. Weekly Summary & Escalation**
- Export Validation_Log.csv ( Passed / Failed / Skipped files ).

**Expected Outputs**

| File Name             | Description                               |
| --------------------- | ----------------------------------------- |
| Validation_Log.csv    | Record of all validation and error events |
| *_cleaned.csv         | Cleaned, validated weekly files           |
| Master_*.csv          | Master datasets by domain                 |
| Master_Data_All.csv   | Merged dataset for analytics              |

**Actionable Plans**
- Use Master_Data_All.csv to detect missing batches, yield deviation, and cost variance across departments.
- Prepare summary table for cross-team review.

**E. Appendix**

**Standard Structures:**

![Structure](https://github.com/CallmeNavin/P21_Data-Flow-Simulation/blob/main/Version%201/Visualization/Structures.jpg)


**E. Further Version**

- Version 2:

**About Me**

Hi, I'm Navin (Bao Vy) – an aspiring Data Analyst passionate about turning raw data into actionable business insights. I’m eager to contribute to data-driven decision making and help organizations translate analytics into business impact. For more details, please reach out at:

🌐 LinkedIn: https://www.linkedin.com/in/navin826/

📂 Portfolio: https://github.com/CallmeNavin/
