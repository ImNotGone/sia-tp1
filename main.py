import json
import time

from src.sokoban import Sokoban
from src.play_sokoban import play

from src.searching_algorithms.bfs import bfs
from src.searching_algorithms.dfs import dfs
from src.searching_algorithms.greedy import greedy


def main():
    config_file = "config.json"

    with open(config_file, "r") as f:
        config = json.load(f)

        levels_file = config["levels_file"]
        level = config["level"]

        sokoban = Sokoban(level, levels_file)

        if config["user_play"]:
            play(sokoban)
            exit(0)

        search_algorithm = config["searching_algorithm"]

        print(f"Calculating solution using {search_algorithm} algorithm")
        sokoban.print_level_state()
        print(f"Level: {level}")

        # TODO: Inject euristic function to searching algorithm
        match search_algorithm:
            case "bfs":
                path_to_solution, elapsed_time = bfs(sokoban)
            case "dfs":
                path_to_solution, elapsed_time = dfs(sokoban)
            case "greedy":
                path_to_solution, elapsed_time = greedy(sokoban)
            case _:
                raise Exception("Invalid searching algorithm")

        # Print solution
        for node in path_to_solution:
            # Clear screen
            print("\033c", end="")

            print(str(node))

            time.sleep(0.1)

        print(f"Elapsed time: {elapsed_time}")


if __name__ == "__main__":
    main()
