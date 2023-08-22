# TP1 SIA - Métodos de Búsqueda

Este repositorio contiene un programa que permite resolver el juego _Sokoban_ con diversos metodos de busqueda y heuristicas. 
Tanto el nivel seleccionado como los metodos de busqueda son configurables mediante el archivo `config.json`. 

## Configuracion

El archivo `config.json` sigue el siguiente formato:
```json
{
  "searching_algorithm": "human" | "bfs" | "dfs" | "greedy" | "a_star",
  "heuristic": "walkable_distance" | "admissible_manhattan_distance" | "inadmissible_manhattan_distance",
  "level": 4,
  "levels_file": "levels.txt"
}
```

Donde cada opcion representa lo siguiente:
- **searching_algorithm**: el algoritmo de busqueda de la solucion que se dividen en 3 categorias
    - _no_informados_: bfs y dfs
    - _informados_: greedy (global) y A*
    - _human_: permite al usuario jugar al _Sokoban_
- **heuristic**: la heuristica utilizada por el algoritmo _informado_
    - _admissible_manhattan_distance_: Calcula la distancia _manhattan_ del jugador a la caja mas cercana y le agrega la suma total de la distancia _manhattan_ de cada caja al _goal_ mas cercano
    - _inadmissible_manhattan_distance_: Calcula suma total de las distancias _manhattan_ del jugador a cada caja y le agrega la suma total de la distancia _manhattan_ de cada caja al _goal_ mas cercano
    - _walkable_distance_: Calcula la longitud del camino mas corto a la caja mas cercana que no esta en un _goal_ y le agrega la suma total de la longitud del camino mas corto de cada caja al _goal_ mas cercano
- **level**: El nivel a seleccionar del archivo de niveles
- **levels_file**: El _path_ del archivo donde se encuentran los niveles

## Ejecucion
Para ejecutar el programa basta con correr `python main.py` desde la raiz del proyecto

