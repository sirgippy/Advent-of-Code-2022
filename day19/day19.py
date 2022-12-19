import re
from json import dumps, loads
from math import prod


def main(input_file_name, minutes, part1=True):
    with open(input_file_name) as input_file:
        lines = [line.strip() for line in input_file.readlines() if line != '\n']

    blueprints = {}
    for line in lines:
        [
            b_id, ore_cost, clay_cost, obs_ore_cost, obs_clay_cost, geo_ore_cost, geo_obs_cost
        ] = [int(n) for n in re.findall(r'\d+', line)]
        blueprints[b_id] = {
            'ore_cost': ore_cost,
            'clay_cost': clay_cost,
            'obs_ore_cost': obs_ore_cost,
            'obs_clay_cost': obs_clay_cost,
            'geo_ore_cost': geo_ore_cost,
            'geo_obs_cost': geo_obs_cost
        }

    if part1:
        return sum([get_max_geodes(blueprint, minutes) * b_id for b_id, blueprint in blueprints.items()])
    else:
        return prod([get_max_geodes(blueprint, minutes) for b_id, blueprint in blueprints.items() if b_id <= 3])


def get_max_geodes(blueprint, minutes):
    max_ore = max(blueprint['ore_cost'], blueprint['clay_cost'], blueprint['obs_ore_cost'], blueprint['geo_ore_cost'])

    best_states = {}

    state = {
        'time': 0,
        'ore_robots': 1, 'ore': 0,
        'clay_robots': 0, 'clay': 0,
        'obs_robots': 0, 'obs': 0,
        'geo_robots': 0, 'geo': 0
    }
    max_geodes = 0
    states = [state]
    while states:
        state = states.pop()
        if max_geodes > state['geo'] + max_possible_geos(state['geo_robots'], minutes - state['time']):
            continue
        robots = (state['ore_robots'], state['clay_robots'], state['obs_robots'], state['geo_robots'])
        if robots in best_states.keys() and best_states[robots] < state['time']:
            continue
        else:
            best_states[robots] = state['time']
        if state['ore_robots'] <= max_ore:
            new_state = loads(dumps(state))
            dt = next(
                t for t in range(0, max_ore + 1)
                if state['ore'] + state['ore_robots'] * t >= blueprint['ore_cost']
            )
            advance_time(new_state, dt + 1, minutes)
            if new_state['time'] == minutes:
                max_geodes = max(max_geodes, new_state['geo'])
            else:
                new_state['ore'] -= blueprint['ore_cost']
                new_state['ore_robots'] += 1
                states.append(new_state)
        if state['clay_robots'] <= blueprint['obs_clay_cost']:
            new_state = loads(dumps(state))
            dt = next(
                t for t in range(0, blueprint['clay_cost'] + 1)
                if state['ore'] + state['ore_robots'] * t >= blueprint['clay_cost']
            )
            advance_time(new_state, dt + 1, minutes)
            if new_state['time'] == minutes:
                max_geodes = max(max_geodes, new_state['geo'])
            else:
                new_state['ore'] -= blueprint['clay_cost']
                new_state['clay_robots'] += 1
                states.append(new_state)
        if state['obs_robots'] <= blueprint['geo_obs_cost'] and state['clay_robots'] > 0:
            new_state = loads(dumps(state))
            dt = next(
                t for t in range(0, blueprint['obs_clay_cost'] + 1)
                if state['ore'] + state['ore_robots'] * t >= blueprint['obs_ore_cost']
                and state['clay'] + state['clay_robots'] * t >= blueprint['obs_clay_cost']
            )
            advance_time(new_state, dt + 1, minutes)
            if new_state['time'] == minutes:
                max_geodes = max(max_geodes, new_state['geo'])
            else:
                new_state['ore'] -= blueprint['obs_ore_cost']
                new_state['clay'] -= blueprint['obs_clay_cost']
                new_state['obs_robots'] += 1
                states.append(new_state)
        if state['obs_robots'] > 0:
            new_state = loads(dumps(state))
            dt = next(
                t for t in range(0, blueprint['geo_obs_cost'] + 1)
                if state['ore'] + state['ore_robots'] * t >= blueprint['geo_ore_cost']
                and state['obs'] + state['obs_robots'] * t >= blueprint['geo_obs_cost']
            )
            advance_time(new_state, dt + 1, minutes)
            if new_state['time'] == minutes:
                max_geodes = max(max_geodes, new_state['geo'])
            else:
                new_state['ore'] -= blueprint['geo_ore_cost']
                new_state['obs'] -= blueprint['geo_obs_cost']
                new_state['geo_robots'] += 1
                states.append(new_state)
    return max_geodes


def advance_time(state, dt, max_time):
    if max_time - state['time'] < dt:
        dt = max_time - state['time']
    state['time'] += dt
    state['ore'] += state['ore_robots'] * dt
    state['clay'] += state['clay_robots'] * dt
    state['obs'] += state['obs_robots'] * dt
    state['geo'] += state['geo_robots'] * dt


def max_possible_geos(current_robots, time_remaining):
    return current_robots * time_remaining + sum([t - 1 for t in range(time_remaining, 1, -1)])


if __name__ == '__main__':
    print(main('test.txt', 24))  # 33
    print(main('input.txt', 24))
    print(main('test.txt', 32, False))  # 56 * 62 = 3472
    print(main('input.txt', 32, False))
