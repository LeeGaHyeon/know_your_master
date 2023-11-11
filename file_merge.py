import os
import pandas as pd

source_dir = './last'
dest_dir = './last'

# List of people and courses
name_list = ['jojeongdeok', 'leeyunguel', 'huhongjune', 'leegahyeon', 'leejaeho', 'leekanghyuk', 'leeseunglee', 'simboseok', 'jeongyubin', 'choimingi', 'leegihun']
course_list = ['A', 'B', 'C']

# Initialize an empty DataFrame to store the concatenated data
concatenated_df = pd.DataFrame()

# Loop through each person and course
for name in name_list:
    for course in course_list:
        source_path = os.path.join(source_dir, name, course)

        # If the destination path does not exist, create it
        dest_path = os.path.join(dest_dir, name, course)
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)

        # 모든 CSV 파일에 대해 반복
        for file_name in os.listdir(source_path):
            if file_name.endswith(".csv"):
                file_path = os.path.join(source_path, file_name)
                df = pd.read_csv(file_path)

                # # Add new columns
                # df['course'] = course
                # df['round'] = file_name.split('_')[2].split('.')[0]  # Extract round from file name
                # df['label'] = name_list.index(name)  # Use the index of name_list as label

                # Concatenate the current DataFrame to the existing one
                concatenated_df = pd.concat([concatenated_df, df], ignore_index=True)

# Save the concatenated DataFrame to a new CSV file
dest_file_name = "./merge_data.csv"
dest_file_path = os.path.join(dest_dir, dest_file_name)
concatenated_df.to_csv(dest_file_path, index=False)

print(f"All files concatenated and saved to: {dest_file_path}")
