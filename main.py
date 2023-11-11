import pandas as pd
import numpy as np
import os

signal = ['RearHeatPower266', 'DI_accelPedalPos', 'BattVoltage132', 'VCFRONT_chillerExvFlowm3', 'BMS_maxDischargePower', 'DI_regenLight', 'DI_vehicleSpeed', 'DI_regenLight', 'DIR_torqueActual', 'RearTorque1D8', 'SystemHeatPowerMax268', 'VCFRONT_pumpBatteryRPMActualm0', 'SmoothBattCurrent132', 'DIR_torqueCommand', 'VCFRONT_chillerExvFlowm3', 'DI_regenLight', 'SteeringSpeed129', 'DI_vehicleSpeed']

import os
import pandas as pd

source_dir = './data'
dest_dir = './preprocessing'

# List of people and courses
name_list = ['jojeongdeok' , 'leeyunguel' , 'huhongjune' , 'leegahyeon' , 'leejaeho' , 'leekanghyuk' , 'leeseunglee' , 'simboseok' , 'jeongyubin' , 'choimingi' , 'leegihun' ]
course_list = ['A', 'B', 'C']

def normalize_features(data):
    """
    모든 feature에 대해 Min-Max 스케일링을 수행하는 함수

    Parameters:
    data (pd.DataFrame): 정규화할 데이터 프레임

    Returns:
    pd.DataFrame: 정규화된 데이터 프레임
    """

    normalized_data = data.copy()

    # 각 열(feature)에 대해 정규화 수행
    for column in data.columns:
        # 현재 열의 최소값과 최대값 계산
        min_value = data[column].min()
        max_value = data[column].max()

        # 정규화 수행: (xi - min(xi)) / (max(xi) - min(xi))
        normalized_data[column] = (data[column] - min_value) / (max_value - min_value)

    return normalized_data

# Loop through each person and course
for name in name_list:
    for course in course_list:
        source_path = os.path.join(source_dir, name, course)
        dest_path = os.path.join(dest_dir, f"{name}", course)

        if not os.path.exists(dest_path):
            os.makedirs(dest_path)

        n = 0

        # Loop through each CSV file in the source path
        for file_name in os.listdir(source_path):
            if file_name.endswith(".csv"):
                n += 1
                # CSV 파일 로드
                df = pd.read_csv(os.path.join(source_path, file_name))

                sample = pd.DataFrame()

                # Process each signal
                for i in signal:
                    new_df = pd.DataFrame()
                    filtered_df = df[df['Signal'] == i]
                    filtered_df = filtered_df.reset_index()

                    filtered_df['Timestamp'] = pd.to_datetime(filtered_df['Timestamp'], format='%Y.%m.%d.%H:%M:%S.%f')
                    filtered_df['timestamp_rounded'] = filtered_df['Timestamp'].dt.round('1S')
                    filtered_df = filtered_df.drop_duplicates(subset='timestamp_rounded', keep='first')

                    filtered_df.set_index('timestamp_rounded', inplace=True)
                    filtered_df.drop(columns='Timestamp', inplace=True)

                    new_df[i] = filtered_df['Physical_value']
                    sample = pd.concat([sample, new_df], axis=1)

                # Normalize the features
                sample_normalized = normalize_features(sample)

                # Save processed and normalized data to destination path
                dest_file_name = f"data_{n}_normalized.csv"
                dest_file_path = os.path.join(dest_path, dest_file_name)
                sample_normalized.to_csv(dest_file_path)

                print(f"Processed, normalized, and saved: {dest_file_path}")

