# 1. Validate filename
# Define base
import os
import re
import pandas as pd
os.chdir(r'D:\Bi\Mini Project\Project 21_Start Date 09.10.25_Data Flow Simulation\Review Version 1, 2, 3_20251019')

# Create Validation Log for tracking fault
from datetime import datetime 
import pytz
vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')

if not os.path.exists('Validation_log.csv'):
    log_df = pd.DataFrame(columns= ['File_Name', 'File_Type', 'Upload_Date', 'Upload_By', 'Status', 'Error_Message'])
    log_df.to_csv('Validation_log.csv', index= False)
    print(f'Created Validation Log')
else:
    print('Validation log file already exist')

upload_by = input('Enter Your Name - Team (e.g. James - Operational Team): ').strip().upper()
def write_log(file_name, file_type, upload_by, status, error_message):
    log_entry = pd.DataFrame([{'File_Name': file_name, 'File_Type': file_type, 'Upload_Date': datetime.now(vn_tz).strftime('%Y - %m - %d %H: %M: %S'), 'Upload_By': upload_by, 'Status': status, 'Error_Message': error_message}])
    log_entry.to_csv('Validation_log.csv', index= False, mode= 'a', header= False)

# User pick week to process
week_to_run = input('Enter week (e.g. 2025W41): ').strip().upper()
print(f'Checking data for Week: {week_to_run}')

# Check files in folder
files = os.listdir('Weekly_Uploaded')
required_raw_files = ['Operational_Data', 'MES_Data', 'Accounting_Data', 'Logistics_Data']
right_pattern_filename = re.compile(r'^(Operational_Data|MES_Data|Accounting_Data|Logistics_Data)_\d{4}W\d{2}\.csv$')
valid_raw_files = []
invalid_raw_files = []

for f in files:
    if right_pattern_filename.match(f):
        valid_raw_files.append(f)
    else:
        invalid_raw_files.append(f)

# Print raw files & auto-rename invalid files name
print(f'Valid raw files: {valid_raw_files}')
print(f'Invalid raw files: {invalid_raw_files}')

for f in invalid_raw_files:
    match_type = None
    for t in required_raw_files:
        if t.split('_')[0].lower() in f.lower():
            match_type = t
            new_filename = f'{t} _{week_to_run}.csv'
            os.rename(os.path.join('Weekly_Uploaded', f), os.path.join('Weekly_Uploaded', new_filename))
            print(f'Renamed {f} - {new_filename}')
            write_log(file_name = new_filename, file_type = t, upload_by = upload_by, status = 'Warning', error_message = f'Renamed from invalid filename: {f}')
            break


# Auto-pick the right week to process
target_files = [f for f in os.listdir('Weekly_Uploaded') if f.endswith(f'{week_to_run}.csv')]
if not target_files:
    print(f'No file found for {week_to_run}')
else:
    print(f'Files for {week_to_run}: ')
    for f in target_files:
        print(f)

# 2. Validate columns in each files
# Expected columns for each files
expected_schema = {'Operational_Data': ['batch_id', 'date', 'shift', 'egg_weight_g', 'larvae_age_day', 'larvae_weight_kg', 'feed_intake_kg', 'mortality_rate', 'drying_temp_avg', 'drying_duration_min', 'moisture_after_dry', 'output_kg', 'defect_kg', 'operator'], 'MES_Data': ['batch_id', 'sensor_id', 'avg_temp', 'humidity', 'drying_time_min', 'chamber_id', 'vibration_alert'], 'Accounting_Data': ['batch_id', 'feed_cost', 'electricity_cost', 'maintenance_cost', 'labor_cost', 'packaging_cost', 'total_cost', 'cost_date'], 'Logistics_Data': ['batch_id', 'truck_id', 'shipment_date', 'destination', 'delivery_status', 'weight_kg', 'delay_hour', 'driver_name']}
for f in target_files:
    file_path = os.path.join('Weekly_Uploaded', f)
    file_type = '_'.join(f.split('_')[:2])
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f'Error in reading file {f} : {e}')
        write_log(file_name = f, file_type = file_type, upload_by = upload_by, status = 'Failed', error_message = f'Cannot read file: {e}')
        continue

# Actual & Expected cols
expected_cols = [c.lower() for c in expected_schema.get(file_type, [])]
actual_cols = df.columns.str.strip().str.lower().tolist()

# Find missing/extra cols
missing_cols = [c for c in expected_cols if c not in actual_cols]
extra_cols = [c for c in actual_cols if c not in expected_cols]

# Log note to Validation Log files
if missing_cols:
    write_log(file_name = f, file_type = file_type, upload_by = upload_by, status = 'Failed', error_message = f'Missing columns: {missing_cols}')
elif extra_cols:
    write_log(file_name = f, file_type = file_type, upload_by = upload_by, status = 'Failed', error_message = f'Extra columns: {extra_cols}')
else:
    print('All columns valid')
    write_log(file_name = f, file_type = file_type, upload_by = upload_by, status = 'Success', error_message = 'Columns OK')

# 3. Data Cleaning
# Create Folder Cleaned Data
import numpy as np
os.makedirs('Cleaned_Data', exist_ok = True)

# Drop N/A, outliers, Log note to Validation Log files
def cleaned_files(file_path, file_type):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip().str.lower()
    df.dropna(how= 'all', inplace= True)
    for col in df.columns:
        if 'date' in col:
            df[col] = pd.to_datetime(df[col], errors= 'coerce')
        elif df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip()
    numeric_cols = df.select_dtypes(include = np.number).columns
    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        outliers = (df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)
        df.loc[outliers, f'{col}_outliers_flag'] = 'Outliers'
    cleaned_path = os.path.join('Cleaned_Data', os.path.basename(file_path).replace('.csv', '_cleaned.csv'))
    df.to_csv(cleaned_path, index = False)
    has_outlier = any(df.filter(like = '_flag').count())
    write_log(file_name = os.path.basename(cleaned_path), file_type = file_type, upload_by = upload_by, status = 'Cleaned', error_message = 'Outliers Flag' if has_outlier else 'OK')
    print(f'Cleaned {file_type} - {cleaned_path}')
    return cleaned_path

# 4. Append to Master Data
# Create Master Data Folder
os.makedirs('Master_Data', exist_ok= True)

def append_to_master(cleaned_path, file_type):
    master_file = os.path.join('Master_Data', f'Master_{file_type.split('_')[0]}.csv')
    cleaned_df = pd.read_csv(cleaned_path)
    if os.path.exists(master_file):
        master_df = pd.read_csv(master_file)
        combined_df = pd.concat([master_df, cleaned_df], ignore_index= True)
    else:
        combined_df = cleaned_df
    combined_df.drop_duplicates(subset= ['batch_id'], keep= 'last', inplace= True)
    combined_df.to_csv(master_file, index= False)
    write_log(file_name = os.path.basename(master_file), file_type = file_type, upload_by = upload_by, status = 'Append to Master', error_message = ' ')
    print(f'Appended {file_type} - {master_file}')
    return master_file

for f in os.listdir('Cleaned_Data'):
    file_path = os.path.join('Cleaned_Data', f)
    file_type = '_'.join(f.split('_')[:2])
    if file_type in expected_schema.keys():
        append_to_master(file_path, file_type)

for f in target_files:
    file_path = os.path.join('Weekly_Uploaded', f)
    file_type = '_'.join(f.split('_')[:2])
    cleaned_path = cleaned_files(file_path, file_type)
    append_to_master(cleaned_path, file_type)

# 5. Merge all master files to Master Data All
def merge_all_master():
    try:
        operational = pd.read_csv(os.path.join('Master_Data', 'Master_Operational.csv'))
        mes = pd.read_csv(os.path.join('Master_Data', 'Master_MES.csv'))
        acc = pd.read_csv(os.path.join('Master_Data', 'Master_Accounting.csv'))
        logistics = pd.read_csv(os.path.join('Master_Data', 'Master_Logistics.csv'))
        for df in [operational, mes, acc, logistics]:
            df.drop_duplicates(subset= ['batch_id'], keep= 'last', inplace= True)
        merge = (operational.merge(mes, on= 'batch_id', how= 'left', suffixes= ('', '_mes')).merge(acc, on= 'batch_id', how= 'left', suffixes= ('', '_acc')).merge(logistics, on= 'batch_id', how= 'left', suffixes= ('', '_logistics')))
        merge.to_csv('Master_Data\Master_Data_All.csv', index= False)
        write_log(file_name = 'Master_Data_All', file_type = 'Merge Master Data', upload_by = upload_by, status = 'Merged', error_message = ' ')
        print('Merge Successfully')
    except Exception as e:
        write_log(file_name = 'Master_Data_All', file_type = 'Merge Master Data', upload_by = upload_by, status = 'Merged Failed', error_message = e)
        print(f'Merge failed: {e}')

merge_all_master()

print('\nAll steps completed! Master_Data_All.csv ready for analysis')
            












