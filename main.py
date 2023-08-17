import json

from src.sokoban import Sokoban

from src.searching_algorithms.bfs import bfs
from src.searching_algorithms.dfs import dfs
from src.searching_algorithms.greedy import greedy


def main():
    config_file = 'config.json'

    with open(config_file, 'r') as f:
        config = json.load(f)

        levels_file = config['levels_file']
        level = config['level']
        
        sokoban = Sokoban(level, levels_file)

        # TODO: Inject euristic function to searching algorithm
        match config['searching_algorithm']:
            case 'bfs':
                path_to_solution, elapsed_time = bfs(sokoban)
            case 'dfs':
                path_to_solution, elapsed_time = dfs(sokoban)
            case 'greedy':
                path_to_solution, elapsed_time = greedy(sokoban)
            case _:
                raise Exception('Invalid searching algorithm')

        # Print solution
        print(f"Elapsed time: {elapsed_time} seconds")
        for node in path_to_solution:
            print(str(node))


if __name__ == '__main__':
    main()
