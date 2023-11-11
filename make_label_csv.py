import os
import pandas as pd

source_dir = './statics'
dest_dir = './last'

# List of people and courses
name_list = ['jojeongdeok', 'leeyunguel', 'huhongjune', 'leegahyeon', 'leejaeho', 'leekanghyuk', 'leeseunglee', 'simboseok', 'jeongyubin', 'choimingi', 'leegihun']
course_list = ['A', 'B', 'C']

# Create a dictionary to map course values to numeric representations
course_mapping = {'A': 0, 'B': 1, 'C': 2}

# Loop through each person and course
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

                # Check if 'course' column exists
                if 'course' not in df.columns:
                    df['course'] = course

                # Add new columns with mapped values
                df['course'] = df['course'].map(course_mapping)
                df['round'] = file_name.split('_')[2].split('.')[0]  # Extract round from file name
                df['label'] = name_list.index(name)  # Use the index of name_list as label

                # Save processed data to destination path
                dest_file_name = f"data_{file_name}"
                dest_file_path = os.path.join(dest_path, dest_file_name)
                df.to_csv(dest_file_path, index=False)

                print(f"Processed and saved: {dest_file_path}")
