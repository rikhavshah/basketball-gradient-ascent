import numpy as np
import json
import pdb
from tqdm import tqdm, trange
import pandas as pd
import os
import csv
import subprocess

PATH_TO_DATA_DIR = "/Users/Vinit/Documents/BasketballAnalysis/nba-movement-data-master/data/"

shot_csv = PATH_TO_DATA_DIR + "/shots/shots.csv"
shots_with_games = PATH_TO_DATA_DIR + '/shots/shots_with_games.csv'
# command = "7z e " + temp
# subprocess.call(["7z", "e", temp])

with open(shot_csv) as s:
    shots = list(s)
    headers = shots[0].split(",")
    print(headers)
    date_index = headers.index("GAME_DATE")
    home_index = headers.index("HTM")
    vis_index = headers.index("VTM\n")
    game_id_index = headers.index("GAME_ID")
    rows_to_write =[]
    with open(shots_with_games, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([i.rstrip() for i in headers])
    # print(home_index, vis_index)
        no_game_list = []
        df = pd.DataFrame(columns=headers)
        for i in trange(len(shots)):
            shot = shots[i]
            shot_split = shot.split(",")
            shot_split[-1] = shot_split[-1].rstrip()
            temp_date = shot_split[date_index]

            game_file = PATH_TO_DATA_DIR + temp_date[4:6] + "." + temp_date[6:] + "." + temp_date[:4] + "." + shot_split[vis_index].rstrip() \
                + ".at." + shot_split[home_index] + ".7z"

            # print(game_file)
            if not os.path.exists(game_file):
                no_game_list.append(i)
            else:
                rows_to_write.append(shot_split)
        rows_to_write.sort(key=lambda _row: _row[1])
        for row in rows_to_write:
            writer.writerow(row)
        # else:
        #     with open(shots_with_games, ) as csvfile:
        #         writer = csv.writer(csvfile)

    # pdb.set_trace()
exit(0)



