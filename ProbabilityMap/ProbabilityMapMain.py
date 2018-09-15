from shot_data import shot_data

from probability_map import Processor

p = Processor(shot_data)

mesh = p.probability_mesh();
