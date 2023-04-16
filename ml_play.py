import os
import pickle

MODEL_FOLDER = 'model'
MODEL_FILE = 'model.pickle'
if os.path.isfile(os.path.join(MODEL_FOLDER, MODEL_FILE)):
    MODEL_PATH = os.path.join(MODEL_FOLDER, MODEL_FILE)
else:
    MODEL_PATH = MODEL_FILE

class MLPlay:
    def __init__(self, *args, **kwargs):
        self.last_x = 0
        self.last_y = 0
        self.stuck_frames = 0

        with open(MODEL_PATH, 'rb') as f:
            self.model = pickle.load(f)

        pass

    def update(self, scene_info, *args, **kwargs):
        if scene_info["status"] != "GAME_ALIVE":
            self.prev_x = 0
            self.prev_y = 0
            return "RESET"
        
        x = scene_info['x']
        y = scene_info['y']
        if ((x - self.last_x) ** 2 + (y - self.last_y) ** 2) ** 0.5 < 1:
            self.stuck_frames += 1
        else:
            self.stuck_frames = 0
        
        self.last_x = x
        self.last_y = y
        
        control_list = self.model.predict([[self.stuck_frames, scene_info['L_sensor'], scene_info['L_T_sensor'], scene_info['F_sensor'], scene_info['R_T_sensor'], scene_info['R_sensor']]])[0]
        
        # print(control_list)
        return {'left_PWM': control_list[0], 'right_PWM': control_list[1]}

    def reset(self):
        self.last_x = 0
        self.last_y = 0