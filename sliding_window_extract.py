import os
import pandas as pd

source_dir = './preprocessing'
dest_dir = './statics'

# List of people and courses
name_list = ['jojeongdeok', 'leeyunguel', 'huhongjune', 'leegahyeon', 'leejaeho', 'leekanghyuk', 'leeseunglee', 'simboseok', 'jeongyubin', 'choimingi', 'leegihun']
course_list = ['A', 'B', 'C']

# 설정한 슬라이딩 윈도우 크기
window_size = 60

def calculate_window_statistics(data, window_size):
    """
    각 시점에 대해 슬라이딩 윈도우를 적용하여 통계적 특성을 계산하는 함수

    Parameters:
    data (pd.DataFrame): 계산할 데이터 프레임
    window_size (int): 슬라이딩 윈도우의 크기 (초 단위)

    Returns:
    pd.DataFrame: 통계적 특성이 추가된 데이터 프레임


    """

    # 결측치 앞 값으로 대체
    data = data.fillna(method='ffill')
    # 모든 숫자 열에 대해 반복
    for column in data.select_dtypes(include='number').columns:
        # 통계적 특성 계산
        mean_col = data[column].rolling(window=window_size, min_periods=window_size).mean()
        std_col = data[column].rolling(window=window_size, min_periods=window_size).std()
        median_col = data[column].rolling(window=window_size, min_periods=window_size).median()

        # 새 컬럼 이름 지정
        data[f"{column}_mean"] = mean_col
        data[f"{column}_std"] = std_col
        data[f"{column}_median"] = median_col

    data = data.iloc[window_size-1:]


    return data

# 각 사용자 및 코스에 대한 데이터를 로드하고 처리
for name in name_list:
    for course in course_list:
        source_path = os.path.join(source_dir, name, course)
        dest_path = os.path.join(dest_dir, name, course)

        # If the destination path does not exist, create it
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)

        # 모든 CSV 파일에 대해 반복
        for file_name in os.listdir(source_path):
            if file_name.endswith(".csv"):
                file_path = os.path.join(source_path, file_name)
                df = pd.read_csv(file_path)

                # 슬라이딩 윈도우를 사용하여 통계적 특성 계산
                df = calculate_window_statistics(df, window_size)

                # 결과 저장
                dest_file_name = f"statistics_{file_name}"
                dest_file_path = os.path.join(dest_path, dest_file_name)
                df.to_csv(dest_file_path)

                print(f"Processed and saved statistics: {dest_file_path}")
