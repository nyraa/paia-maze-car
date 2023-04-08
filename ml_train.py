import os
import pickle
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

threhold = {
    5: 350,
    7: 500,
}

import os

FOLDER_NAME = "record"
MODEL_FOLDER = 'model'
MAX_TAKE = 500

threshold = {
    5: 350,
    7: 500,
}

dataset_path = []
for folder_name in os.listdir(FOLDER_NAME):
    if not os.path.isdir(os.path.join(FOLDER_NAME, folder_name)):
        continue  # skip files that aren't directories

    folder_threshold = threshold.get(int(folder_name), None)  # default to 0 if folder not in threshold dict

    folder_dataset_path = []

    for filename in os.listdir(os.path.join(FOLDER_NAME, folder_name)):
        if not filename.endswith(".pickle"):
            continue  # skip non-pickle files

        file_parts = filename.split("_")
        if len(file_parts) != 2:
            continue  # skip files that don't match the expected format

        record_framecount = int(file_parts[1].split(".")[0])
        if folder_threshold != None and record_framecount >= folder_threshold:
            continue  # skip files that don't meet the threshold

        # do something with the selected file
        folder_dataset_path.append((record_framecount, os.path.join(FOLDER_NAME, folder_name, filename)))
    folder_dataset_path.sort(key=lambda x: x[0])
    print(f'map {folder_name} has {len(folder_dataset_path)} vaild record(s)')
    dataset_path += [x[1] for x in folder_dataset_path[:MAX_TAKE]]


data_x = []
data_y = []
# input frame:
# [stuck_frame_count, sensors]
# output frame:
# [left_PWM, right_PWM]
for path in dataset_path:
    last_x = 0
    last_y = 0
    stuck_frame_count = 0
    with open(path, 'rb') as f:
        record = pickle.load(f)
        for i, scene_info in enumerate(record['scene_infos']):
            x = scene_info['x']
            y = scene_info['y']
            if ((x - last_x) ** 2 + (y - last_y) ** 2) ** 0.5 < 1:
                stuck_frame_count += 1
            else:
                stuck_frame_count = 0
            data_x.append([stuck_frame_count, scene_info['L_sensor'], scene_info['L_T_sensor'], scene_info['F_sensor'], scene_info['R_T_sensor'], scene_info['R_sensor']])
            data_y.append([record['control_lists'][i]['left_PWM'], record['control_lists'][i]['right_PWM']])

X_train, X_test, y_train, y_test = train_test_split(
    data_x,  # Features
    data_y,  # Target variable
    test_size=0.2,  # Percentage of data for testing
    random_state=87  # Set random seed for reproducibility
)

# Create a DecisionTreeRegressor object
regressor = DecisionTreeRegressor(random_state=87)

# Train the model
regressor.fit(X_train, y_train)

# Make predictions on the testing set
y_predict = regressor.predict(X_test)

# Evaluate the model's performance
mse = mean_squared_error(y_test, y_predict)
print(f"Mean Squared Error: {mse:.2f}")
os.makedirs(MODEL_FOLDER, exist_ok=True)
with open(os.path.join(MODEL_FOLDER, 'model.pickle'), 'wb') as f:
    pickle.dump(regressor, f)