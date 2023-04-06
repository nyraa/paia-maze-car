import math
import pickle
import time
import os
class MLPlay:
    def __init__(self, ai_name, game_params,*args,**kwargs):
        self.player_no = ai_name
        self.game_params = game_params
        
        self.round_status = None
        # paste start
        self.prev_pos = []
        self.control_list = {}
        self.record = {'scene_infos': [], 'control_lists': []}

    def update(self, scene_info: dict, *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            self.round_status = scene_info['status']
            return "RESET"
        # paste start
        r_sensor, rf_sensor, l_sensor, lf_sensor, f_sensor = scene_info["R_sensor"], scene_info['R_T_sensor'], scene_info["L_sensor"], scene_info['L_T_sensor'], scene_info["F_sensor"]
        MAX_D = 20
        left = 0
        right = 0
        if f_sensor > MAX_D:
            left = 255
            right = 255
        else:
            if lf_sensor > rf_sensor:
                left = -160
                right = 255
            elif rf_sensor > lf_sensor:
                left = 255
                right = -160
            else:
                left = 255
                right = 255
            if l_sensor < MAX_D:
                left = (l_sensor / MAX_D) * left
            if r_sensor < MAX_D:
                right = (r_sensor / MAX_D) * right

        if left > 255:
            left = 255
        elif left < -255:
            left = -255
        if right > 255:
            right = 255
        elif left < -255:
            left = -255
        
        self.control_list = {'left_PWM': left, 'right_PWM': right}
        self.record['scene_infos'].append(scene_info)
        self.record['control_lists'].append(self.control_list)
        return self.control_list

    def reset(self):
        """
        Reset the status
        """
        if self.round_status == 'GAME_PASS':
            # Get current timestamp
            timestamp = int(time.time())

            # Define filename
            dir_path = os.path.join('record', str(self.game_params['map']))
            os.makedirs(dir_path, exist_ok=True)
            filepath = os.path.join(dir_path, f'{timestamp}.pickle')

            # Open file in binary write mode
            with open(filepath, "wb") as f:
                # Dump self.record to file using pickle
                pickle.dump(self.record, f)
                print(f'record save to {filepath}')

        # reset
        self.round_status = None
        self.record = {'scene_infos': [], 'control_lists': []}
        pass