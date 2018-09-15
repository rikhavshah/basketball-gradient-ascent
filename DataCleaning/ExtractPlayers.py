import numpy as np
import json
import pdb
import csv
import random
from tqdm import tqdm, trange
import pandas as pd
import os
import subprocess


def extract_players(path_to_data_dir, shots, corresponding_moments):
    PATH_TO_DATA_DIR = path_to_data_dir
    NUM_PREVIOUS_EVENTS = 0  # because the moments encompass enough time, don't need multiple events per shot
    # but the option exists if we want to do multi event analysis
    FRACTION_MOMENTS = .025  # sampling fraction of moments

    shot_csv = shots
    corresponding_moments_csv = corresponding_moments

    with open(shot_csv, 'r') as s:
        with open(corresponding_moments_csv, 'w') as corresponding_events_file:
            shots = list(s)
            corr_headers = ["CORRESPONDING SHOT", "EVENT_ID", "MOMENT_NUMBER", "MOMENT_DATA"]
            corr_writer = csv.writer(corresponding_events_file, delimiter=',')
            corr_writer.writerow(corr_headers)
            headers = shots[0].split(",")
            # print(headers)
            date_index = headers.index("GAME_DATE")
            home_index = headers.index("HTM")
            vis_index = headers.index("VTM\n")
            game_id_index = headers.index("GAME_ID")
            event_id_index = headers.index("GAME_EVENT_ID")
            if not os.path.exists(PATH_TO_DATA_DIR + "0021500001.json"):
                subprocess.call(["7z", "e", PATH_TO_DATA_DIR + "10.27.2015.DET.at.ATL.7z"], stdout=subprocess.DEVNULL)
            df = pd.read_json(PATH_TO_DATA_DIR + "0021500001.json")
            for i in trange(1, len(shots), 1):  # middle should be len(shots), start at 1 to ignore headers
                shot = shots[i]
                shot_split = shot.split(",")
                shot_split[-1] = shot_split[-1].rstrip()
                temp_date = shot_split[date_index]

                game_file = PATH_TO_DATA_DIR + temp_date[4:6] + "." + temp_date[6:] + "." + temp_date[:4] + "." \
                    + shot_split[vis_index].rstrip() + ".at." + shot_split[home_index] + ".7z"

                game_json = PATH_TO_DATA_DIR + "00" + shot_split[game_id_index] + ".json"

                # note all games exist b/c preprocessing

                if not os.path.exists(game_json):
                    subprocess.call("rm *.json", shell=True)
                    subprocess.call(["7z", "e", game_file], stdout=subprocess.DEVNULL)
                    # print(game_file)
                    df = pd.read_json(game_json)

                event_num = shot_split[event_id_index]
                for j in range(len(df)):
                    if int(df.ix[j, 'events']['eventId']) == int(event_num):
                        df_event_index = j
                        break
                else:
                    print("event doesnt exist")
                    continue
                for k in range(df_event_index-NUM_PREVIOUS_EVENTS, df_event_index+1, 1):
                    try:
                        moments = df.ix[k, 'events']['moments']

                    except KeyError:
                        continue
                    for moment_index in range(len(moments)):
                        if random.random() <= FRACTION_MOMENTS:
                            corr_writer.writerow([i, df.ix[k, 'events']['eventId'],
                                                  moment_index, str(df.ix[k, 'events']['moments'][moment_index])])
