import subprocess
from FixEventData import fix_event_data
from ExtractPlayers import extract_players

PATH_TO_DATA_DIR = ""  # used if data lives elsewhere
SHOTS = "shots/shots.csv"
CORRESPONDING_MOMENTS = PATH_TO_DATA_DIR + "corresponding_moments.csv"

try:
    extract_players(PATH_TO_DATA_DIR, SHOTS, CORRESPONDING_MOMENTS)
except ValueError:
    subprocess.call("rm *.json", shell=True)
    # NOTE: this value error will only occur if there are missing sportVU data
    # in this directory, which WILL happen unless all data is moved here from
    # the mirror: https://github.com/sealneaward/nba-movement-data/tree/master/data
    pass
fix_event_data(CORRESPONDING_MOMENTS, PATH_TO_DATA_DIR + "corresponding_moments_cleaned.csv")
