MAP = 1
GAME_TYPE=MAZE
USER_NUM=1
TIME_TO_PLAY=450
USER_SCRIPT=ml_play.py
RUN_COMMAND=python3.9 -m mlgame
ARGS=./Maze_Car --map $(MAP) --game_type $(GAME_TYPE) --time_to_play $(TIME_TO_PLAY) --sensor_num 5 --sound off


play:
	$(RUN_COMMAND) -i ml_play.py $(ARGS)

collect:
	$(RUN_COMMAND) -i bot_collect.py $(ARGS)

train:
	python3.9 ml_train.py