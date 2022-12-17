from re import match
from itertools import combinations
from json import dumps, loads

valve_pattern = r'Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)'


def main(input_file_name, people, execution_time):
    with open(input_file_name) as input_file:
        valves = parse_valves([line.strip() for line in input_file.readlines()])
    minimum_distances = get_minimum_distances(valves)
    pressurized_valves = find_quickest_paths(valves, minimum_distances)
    pressure = get_optimal_pressure_released(minimum_distances, pressurized_valves, execution_time, people)
    return pressure


def parse_valves(lines):
    valves = {}
    for valve in lines:
        [valve, flow_rate, tunnels] = match(valve_pattern, valve).groups()
        flow_rate = int(flow_rate)
        valves[valve] = {'flow_rate': flow_rate, 'tunnels': tunnels.split(', ')}
    return valves


def find_quickest_paths(valves, minimum_distances):
    pressurized_valve_ids = [key for key in valves.keys() if valves[key]['flow_rate'] > 0]
    pressurized_valves = {}
    for valve_id in pressurized_valve_ids:
        pressurized_valves[valve_id] = {
            'flow_rate': valves[valve_id]['flow_rate'],
            'tunnels': {
                other_valve_id: minimum_distances[valve_id][other_valve_id]
                for other_valve_id in pressurized_valve_ids
                if other_valve_id != valve_id
                and other_valve_id in minimum_distances[valve_id].keys()
            }
        }
    return pressurized_valves


def get_minimum_distances(valves):
    distances = {}
    for valve in valves.keys():
        for other_valve in valves.keys():
            get_distance(valve, other_valve, valves, [], distances)
    return distances


def get_distance(from_valve, to_valve, valves, path, distances):
    if from_valve not in distances.keys():
        distances[from_valve] = {}
    if to_valve in distances[from_valve].keys():
        return distances[from_valve][to_valve]
    if to_valve in valves[from_valve]['tunnels']:
        distances[from_valve][to_valve] = 1
        return 1
    min_distance = 1000
    for valve in valves[from_valve]['tunnels']:
        if valve not in path:
            distance = get_distance(valve, to_valve, valves, path + [from_valve], distances)
            if distance:
                min_distance = min(min_distance, distance + 1)
    if min_distance < 1000:
        distances[from_valve][to_valve] = min_distance
        return min_distance
    return None


def get_optimal_pressure_released(minimum_distances, valves, remaining_time, people):
    best_pressure = 0
    for tunnels in combinations([
        (tunnel, remaining_time - distance)
        for tunnel, distance in minimum_distances['AA'].items()
        if tunnel in valves.keys()
    ], people):
        tunnels = [[tunnel] for tunnel in tunnels]
        [pressure, _] = find_optimal_path(tunnels, valves)
        best_pressure = max(pressure, best_pressure)
    return best_pressure


def find_optimal_path(paths, valves):
    best_path = [0, None]
    remaining_times = [path[-1][1] for path in paths]
    next_to_act, remaining_time = next(
        (idx, ttg) for idx, ttg in enumerate(remaining_times) if ttg == max(remaining_times)
    )
    opened_valves = [valve[0] for path in paths for valve in path]
    remaining_tunnels = [valve for valve in valves.keys() if valve not in opened_valves]
    for tunnel, distance in valves[paths[next_to_act][-1][0]]['tunnels'].items():
        if tunnel in remaining_tunnels and remaining_time - distance - 1 > 1:
            new_paths = loads(dumps(paths))
            new_paths[next_to_act].append((tunnel, remaining_time - distance - 1))
            [pressure, optimal_paths] = find_optimal_path(new_paths, valves)
            if pressure > best_path[0]:
                best_path = [pressure, optimal_paths]
    if best_path[0] == 0:
        return [evaluate_paths(paths, valves), paths]
    return best_path


def evaluate_paths(paths, valves):
    return sum([valves[valve]['flow_rate'] * (open_time - 1) for path in paths for (valve, open_time) in path])


if __name__ == '__main__':
    print(main('test.txt', 1, 30))
    print(main('input.txt', 1, 30))
    print(main('test.txt', 2, 26))
    print(main('input.txt', 2, 26))
