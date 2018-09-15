import numpy as np
import json
import pdb
import csv
import random
from tqdm import tqdm, trange
import pandas as pd
import os
import subprocess

PATH_TO_DATA_DIR = "/Users/Vinit/Documents/BasketballAnalysis/nba-movement-data-master/data/"
NUM_PREVIOUS_EVENTS = 0
FRACTION_MOMENTS = .025

temp = PATH_TO_DATA_DIR + "/12.31.2015.PHX.at.OKC.7z"
shot_csv = PATH_TO_DATA_DIR + "/shots/actual_shots_with_games.csv"
corresponding_events_csv = PATH_TO_DATA_DIR + "corresponding_events_1percent.csv"
# command = "7z e " + temp
# subprocess.call(["7z", "e", temp])

with open(shot_csv, 'r') as s:
    with open(corresponding_events_csv, 'w') as corresponding_events_file:
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
        # print(home_index, vis_index)
        no_game_list = []
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
                # print(df.ix[i, 'events']['eventId'])
                if int(df.ix[j, 'events']['eventId']) == int(event_num):
                    df_event_index = j
                    # print(df.ix[j, 'events']['eventId'])
                    break
            else:
                print("event doesnt exist")
                continue
            # print(df.ix[df_event_index, 'events']['eventId'])
            # print(df.ix[df_event_index, 'events']['moments'])
            for k in range(df_event_index-NUM_PREVIOUS_EVENTS, df_event_index+1, 1):
                # print(len(df.ix[k, 'events']['moments']))
                try:
                    moments = df.ix[k, 'events']['moments']
                    # print(m[0])
                    # exit(0)
                except KeyError:
                    continue
                for moment_index in range(len(moments)):
                    if random.random() <= FRACTION_MOMENTS:
                        corr_writer.writerow([i, df.ix[k, 'events']['eventId'],
                                              moment_index, str(df.ix[k, 'events']['moments'][moment_index])])
            # exit(0)
        # pdb.set_trace()
exit(0)

for f in os.listdir(os.fsencode(PATH_TO_DATA_DIR)):
    f_name = PATH_TO_DATA_DIR + "/" + os.fsdecode(f)
    if f_name.endswith(".json"):
        print(str(f_name))
        with open(str(f_name)) as jf:
            df = pd.read_json(str(f_name))
            for c in df.columns:
                print(c)
            # print(df.ix[1])
            # print(df.ix[1, 'events'])

subprocess.call("rm *.json", shell=True)
exit(0)
# delete any last jsons
for f in os.listdir(os.fsencode(PATH_TO_DATA_DIR)):
    f_name = PATH_TO_DATA_DIR + "/" + os.fsdecode(f)
    if f_name.endswith(".json"):
        os.remove(f_name)

# with open(temp, 'rb') as f:
#     buffer_ = f.read()
#     with libarchive.public.memory_reader(buffer_) as e:
#         for entry in e:
#             with open('/tmp/' + str(entry), 'wb') as ft:
#                 for block in entry.get_blocks():
#                     ft.write(block)
#
# exit(0)
# for f in os.listdir(os.fsencode(PATH_TO_DATA_DIR)):
#     # print(os.fsdecode(f))
#     print(PATH_TO_DATA_DIR + "/" + os.fsdecode(f))
#     with zf.ZipFile(PATH_TO_DATA_DIR + "/" + os.fsdecode(f), 'r') as zip_ref:
#         zip_ref.extractall(PATH_TO_DATA_DIR)
