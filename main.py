import json
import time
from src.heuristics.inadmissible import inadmissible_manhattan_distance
from src.heuristics.admisible import (
    admissible_manhattan_distance,
    walkable_distance,
)

from src.sokoban import Sokoban
from src.play_sokoban import play

from src.searching_algorithms.informed import a_star, greedy
from src.searching_algorithms.uninformed import bfs, dfs

informed_searching_algorithms = {
    "greedy": greedy,
    "a_star": a_star,
}
uninformed_searching_algorithms = {
    "bfs": bfs,
    "dfs": dfs,
}
heuristics = {
    "admissible_manhattan_distance": admissible_manhattan_distance,
    "inadmissible_manhattan_distance": inadmissible_manhattan_distance,
    "walkable_distance": walkable_distance,
}


def main():
    config_file = "config.json"

    with open(config_file, "r") as f:
        config = json.load(f)

        levels_file = config["levels_file"]
        level = config["level"]

        sokoban = Sokoban(level, levels_file)

        search_algorithm = config["searching_algorithm"]

        if search_algorithm in informed_searching_algorithms:
            heuristic = config["heuristic"]
            if heuristic not in heuristics:
                raise Exception("Invalid heuristic")

            print(f"Calculating solution using {search_algorithm} algorithm")
            print(f"Using {heuristic} heuristic")
            print(sokoban)
            print(f"Level: {level}")

            heuristic_function = heuristics[heuristic]

            search_algorithm = informed_searching_algorithms[search_algorithm]

            (
                path_to_solution,
                elapsed_time,
                nodes_expanded,
                frontier_nodes,
            ) = search_algorithm(sokoban, heuristic_function)

        elif search_algorithm in uninformed_searching_algorithms:
            print(f"Calculating solution using {search_algorithm} algorithm")
            print(sokoban)
            print(f"Level: {level}")

            search_algorithm = uninformed_searching_algorithms[search_algorithm]

            (
                path_to_solution,
                elapsed_time,
                nodes_expanded,
                frontier_nodes,
            ) = search_algorithm(sokoban)
        elif search_algorithm == "human":
            play(sokoban)
            exit(0)
        else:
            raise Exception("Invalid searching algorithm")

        print(f"Elapsed time: {elapsed_time}")
        print(f"Number of steps: {len(path_to_solution)}")
        print(f"Nodes expanded: {nodes_expanded}")
        print(f"Frontier nodes: {frontier_nodes}")

        user_input = input("Press enter to see solution or q to exit")

        if user_input == "q":
            exit(0)

        # Print solution
        for node in path_to_solution:
            # Clear screen
            print("\033c", end="")

            sokoban.set_state(node.get_player(), node.get_boxes())
            print(sokoban)

            time.sleep(0.1)


if __name__ == "__main__":
    main()
