from building import *
from copy import deepcopy
import sys

# speed test - use "python optimizer.py" to run
if __name__ == "__main__":
    import timeit

    test_size = 20  # set to 100 to check time for speed race
    t1 = timeit.repeat(stmt="optimizer.max_food(b)",
                       setup="import gc, building, optimizer; b = building.random_building({0}, True); gc.collect()".format(
                           test_size), repeat=3, number=1)
    t2 = timeit.repeat(stmt="optimizer.max_supplies(b)",
                       setup="import gc, building, optimizer; b = building.random_building({0}, False); gc.collect()".format(
                           test_size), repeat=3, number=1)
    # some calculation that takes ~1 sec on my machine
    tref = timeit.repeat(stmt="for i in range(1000000): a=i^2", setup="import gc; gc.collect()", repeat=3, number=19)
    print(
        "max_food(n={0}) = {1} ({3} normalized), max_supplies(n={0}) = {2} ({4} normalized)".format(test_size, min(t1),
                                                                                                    min(t2),
                                                                                                    min(t1) / min(tref),
                                                                                                    min(t2) / min(
                                                                                                        tref)))


def is_direction_valid(building: Building, delta):
    (dr, dc) = delta
    newr = building.player_row + dr
    newc = building.player_col + dc
    return (not building.is_collapsed(newr, newc)) and building.is_valid(newr, newc)


directions_lst = [(0, -1), (0, 1), (-1, 0), (1, 0)]

playerPosition_maxFood_dict = {}
max_path_foods = []


def calc_max_food(building: Building) -> int:
    sys.stdout.write('.')
    sys.stdout.flush()
    global directions_lst
    global playerPosition_maxFood_dict
    current_position_food = building.rooms[building.player_row][building.player_col].food
    player_position = (building.player_row, building.player_col)
    if player_position in playerPosition_maxFood_dict:
        return playerPosition_maxFood_dict[player_position]
    else:
        if building.can_move():
            valid_directions = [d for d in directions_lst if is_direction_valid(building, d)]
            # print(f'valid_directions={valid_directions}')
            all_sub_foods = []
            for (dr, dc) in valid_directions:
                # print((dr, dc))
                cloned_building = deepcopy(building)
                # print(f'player at {cloned_building.player_row} {cloned_building.player_col}')
                cloned_building.move_player(dr, dc)
                all_sub_foods.append(calc_max_food(cloned_building))
            sub_max = max(all_sub_foods) + current_position_food
            max_path_foods.append(current_position_food)
            playerPosition_maxFood_dict[player_position] = sub_max
            return sub_max
        else:
            playerPosition_maxFood_dict[player_position] = current_position_food
            return current_position_food


def max_food(building: Building) -> int:
    print(building)
    global playerPosition_maxFood_dict
    global max_path_foods
    playerPosition_maxFood_dict = {}
    max_path_foods = []
    max_food = calc_max_food(building)
    print(max_path_foods)
    # print(len(playerPosition_maxFood_dict))
    return max_food
    """returns the maximum number of food that can be collected from given building"""
    # return building.size * 10  # dummy implementation - replace


def max_supplies(building: Building) -> int:
    """returns the maximum of min(food,water) that can be collected from given building"""
    return building.size * 5  # dummy implementation - replace
