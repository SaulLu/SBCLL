import csv
import os
import re
import time
import pandas as pd

from speed_test import loadMap
from strategies.target_strategy_v2 import TargetStrategy2
from strategies.heuristics import distance_target_difference_heuristic
import models.engine as engine


def test_stat():
    path_metrics = os.path.join('test_maps',"metrics.csv")
    with open(path_metrics, "w+") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                'row',
                'mons',
                'hums',
                'map_path',
                'turn_time',
                # 'depth_reached',
                # 'depth_max',
                # 'Timed_out',
                # 'visited',
                # 'cut',
                # 'unvisited',
                # 'generated_boards',
                # 'random_move',
            ]
        )

    our_creature = "Werewolves"
    their_creature = "Vampires"

    for file in os.listdir('test_maps'):
        if file.endswith(".xml"):
            map_path = os.path.join('test_maps', file)

            try:
                row, mons, hums, _ = file.split('_')
                row = re.sub('map', '', row)
            except:
                row, mons, hums = None, None, None


            with open(path_metrics, "a") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        row,
                        mons,
                        hums,
                        file,
                        None,
                        # None,
                        # None,
                        # None,
                        # None,
                        # None,
                        # None,
                        # None,
                        # None,
                    ]
                )

            max_x, max_y, board = loadMap(map_path, our_creature)
            strategy = TargetStrategy2(max_x, max_y, distance_target_difference_heuristic)
            strategy.current_board = board

            t0 = time.time()
            _ = strategy.next_moves(2)
            tf = time.time() - t0
            add_infos(turn_time=tf)

def show_stat():
    path = os.path.join('test_maps','metrics.csv')
    df = pd.read_csv(path)
    print(df.describe())

def add_infos(turn_time=None, 
                depth_reached=None,
                depth_max=None,
                Timed_out=None,
                visited=None,
                cut=None,
                unvisited=None, 
                generated_boards=None,
                random_move=None):
    
    path_metrics = os.path.join('test_maps',"metrics.csv")
    with open(path_metrics, "r") as f:
        reader = csv.reader(f)
        mylist = list(reader)
        f.close()

    mylist[-1][4] = turn_time
    # mylist[-1][5] = depth_reached
    # mylist[-1][6] = depth_max
    # mylist[-1][7] = Timed_out
    # mylist[-1][8] = visited
    # mylist[-1][9] = cut
    # mylist[-1][10] = unvisited
    # mylist[-1][11] = generated_boards

    with open(path_metrics, 'w', newline = '') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(mylist)
    
if __name__ == "__main__":
    test_stat()
    show_stat()
