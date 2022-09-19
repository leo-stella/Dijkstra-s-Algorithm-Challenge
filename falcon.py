from queue import PriorityQueue
import copy


class Graph:
    def __init__(self, num_of_planets):
        self.p = num_of_planets
        self.planet_distance = [[-1 for i in range(num_of_planets)] for j in range(num_of_planets)]

    def add_path(self, start, end, path_distance):
        self.planet_distance[start][end] = path_distance
        self.planet_distance[end][start] = path_distance


def find_safest_path(graph, start_planet, destination_planet, autonomy, countdown, danger):
    pq = PriorityQueue()
    paths = PriorityQueue()
    pq.put(([start_planet], 0, [], 0))
    while not pq.empty():
        (route, total_dist, dangerous_day, days_traveled) = pq.get()
        if route[-1] == destination_planet:
            paths.put((route, total_dist, dangerous_day, days_traveled))
            continue

        for next_planet in range(graph.p):
            route_origin = copy.copy(route)
            total_dist_origin = copy.copy(total_dist)
            dangerous_day_origin = copy.copy(dangerous_day)
            days_traveled_origin = copy.copy(days_traveled)

            refuel = False
            if next_planet in route:
                continue

            if graph.planet_distance[route[-1]][next_planet] != -1 and next_planet != start_planet:
                distance = graph.planet_distance[route[-1]][next_planet]
                if days_traveled + distance > autonomy:
                    continue
                elif days_traveled + distance == autonomy:
                    total_dist += distance
                    days_traveled = 0
                    if next_planet != destination_planet:
                        total_dist += 1
                        refuel = True
                else:
                    days_traveled += distance
                    total_dist += distance

                for d in danger:
                    if next_planet == d[0] and distance == d[1] and distance not in dangerous_day:
                        dangerous_day.append(distance)
                    if next_planet == d[0] and total_dist == d[1] and total_dist not in dangerous_day:
                        dangerous_day.append(total_dist)
                    if refuel and next_planet == d[0] and total_dist - 1 == d[1] and total_dist - 1 not in dangerous_day:
                        dangerous_day.append(total_dist - 1)

                if total_dist > countdown:
                    total_dist = total_dist_origin
                    days_traveled = days_traveled_origin
                    continue

                route.append(next_planet)
                pq.put((route, total_dist, dangerous_day, days_traveled))
            route = route_origin
            total_dist = total_dist_origin
            dangerous_day = dangerous_day_origin
            days_traveled = days_traveled_origin

    min_capture_days = 100
    capture_probability = 0
    while not paths.empty():
        (route, total_dist, dangerous_day, days_traveled) = paths.get()
        print((route, total_dist, dangerous_day, days_traveled))
        extra_days = countdown - total_dist
        can_wait = 0
        dangerous_planet = ''
        for dd in dangerous_day:
            for d in danger:
                if d[1] == dd:
                    dangerous_planet = d[0]
            if (dangerous_planet, dd + extra_days) not in danger:
                can_wait += 1
        capture_days = len(dangerous_day) - can_wait
        if capture_days < min_capture_days:
            min_capture_days = capture_days
    initial_prob = 1
    for i in range(1, min_capture_days + 1):
        capture_probability += (0.1*initial_prob)
        initial_prob = 1 - capture_probability
    return round((1 - capture_probability)*100, 2)
