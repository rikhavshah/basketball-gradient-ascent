from tqdm import tqdm, trange
import csv

PATH_TO_DATA_DIR = "/Users/Vinit/Documents/BasketballAnalysis/nba-movement-data-master/data/"
EVENT_DATA = PATH_TO_DATA_DIR + "all_corresponding_events.csv"
OUT_CSV = PATH_TO_DATA_DIR + "moment_data_cleaned.csv"


def fix_row(row):
    split = row.split(",")
    for i, j in enumerate(row.split(",")):
        split[i] = j.replace("\"", '').replace("[", '').replace("]", '').replace(" ", '').rstrip()
    new_row = [0] * 39
    try:
        # print(len(split))
        # for i,j in enumerate(split):
        #     print(i, j)

        assert len(split) == 63  # is all the data there for this row?
        new_row[0] = split[0]  # shot
        new_row[1] = split[1]  # event_id
        new_row[2] = split[2]  # moment_number
        new_row[3] = split[5]  # game time left
        new_row[4] = split[6]  # shot time left
        new_row[5] = split[13]  # team1 id
        new_row[6] = split[38]  # team2 id
        new_row[7] = split[11]  # ball_x
        new_row[8] = split[12]  # ball_y
        new_row[9] = split[14]  # player 1 id
        new_row[10] = split[15]  # player 1 x
        new_row[11] = split[16]  # player 1 y
        new_row[12] = split[19]  # player 2 id
        new_row[13] = split[20]  # player 2 x
        new_row[14] = split[21]  # player 2 y
        new_row[15] = split[24]  # player 3 id
        new_row[16] = split[25]  # player 3 x
        new_row[17] = split[26]  # player 3 y
        new_row[18] = split[29]  # player 4 id
        new_row[19] = split[30]  # player 4 x
        new_row[20] = split[31]  # player 4 y
        new_row[21] = split[34]  # player 5 id
        new_row[22] = split[35]  # player 5 x
        new_row[23] = split[36]  # player 5 y
        new_row[24] = split[39]  # player 6 id
        new_row[25] = split[40]  # player 6 x
        new_row[26] = split[41]  # player 6 y
        new_row[27] = split[44]  # player 7 id
        new_row[28] = split[45]  # player 7 x
        new_row[29] = split[46]  # player 7 y
        new_row[30] = split[49]  # player 8 id
        new_row[31] = split[50]  # player 8 x
        new_row[32] = split[51]  # player 8 y
        new_row[33] = split[54]  # player 9 id
        new_row[34] = split[55]  # player 9 x
        new_row[35] = split[56]  # player 9 y
        new_row[36] = split[59]  # player 10 id
        new_row[37] = split[60]  # player 10 x
        new_row[38] = split[61]  # player 10 y
        return new_row
        # print(new_row)

    except AssertionError:
        # this is a very rare catch statement if some data are missing
        pass


def fix_event_data(event_data, out_csv):
    EVENT_DATA = event_data
    OUT_CSV = out_csv
    with open(EVENT_DATA, 'r') as f:
        events = list(f)
        new_df = []
        for row in tqdm(events[1:]):
            new = fix_row(row)
            # print(new)
            if new:
                new_df.append(new)
        headers = ["CORRESPONDING SHOT", "EVENT_ID", "MOMENT_NUMBER", "GAME_TIME_LEFT", "SHOT_TIME_LEFT",
                   "TEAM1_ID", "TEAM2_ID", "BALL_X", "BALL_Y",
                   "PLAYER1_ID", "PLAYER1_X", "PLAYER1_Y", "PLAYER2_ID", "PLAYER2_X", "PLAYER2_Y",
                   "PLAYER3_ID", "PLAYER3_X", "PLAYER3_Y", "PLAYER4_ID", "PLAYER4_X", "PLAYER4_Y",
                   "PLAYER5_ID", "PLAYER5_X", "PLAYER5_Y", "PLAYER6_ID", "PLAYER6_X", "PLAYER6_Y",
                   "PLAYER7_ID", "PLAYER7_X", "PLAYER7_Y", "PLAYER8_ID", "PLAYER8_X", "PLAYER8_Y",
                   "PLAYER9_ID", "PLAYER9_X", "PLAYER9_Y", "PLAYER10_ID", "PLAYER10_X", "PLAYER10_Y"]
        with open(OUT_CSV, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(headers)
            for row_to_write in new_df:
                writer.writerow(row_to_write)
