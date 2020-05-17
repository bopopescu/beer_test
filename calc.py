import mysql.connector
import math
import numpy as np
import tests


class Node:
    def __init__(self, data, index, next, dist, head=False):
        self.data = data
        self.index = index
        self.dist = dist
        self.next = next
        self.best_index = -1  # for optimization purpose
        self.dist_increase_to_best = -1  # for optimization purpose
        self.head = head

    def find_best(self):
        """"finds best_index node to insert after current node"""
        min_dist = float("inf")
        min_index = -1
        for i in range(distance_matrix.shape[0]):
            if i != self.index and included_dict.get(i) is None:
                dist1 = distance_matrix[i][self.index]
                dist2 = distance_matrix[i][self.next.index]
                if dist1 + dist2 < min_dist:
                    min_dist = dist1 + dist2
                    min_index = i
        self.best_index = min_index
        # self.best_index = nearest_dict.get(min_index)
        self.dist_increase_to_best = min_dist - self.dist


def make_route(distance):
    """"makes linked list of selected breweries for route
    :returns traveled distance"""
    while len(included_dict) < len(nearest_dict):
        current_node = head
        min_dist = float("inf")
        min_index = -1
        min_node = None
        while True:
            if current_node.best_index == -1 or included_dict.get(current_node.index) is not None:
                current_node.find_best()  # optimization - called at least once per outer iteration instead of foreach node
            if current_node.dist_increase_to_best < min_dist:
                min_dist = current_node.dist_increase_to_best
                min_index = current_node.best_index
                min_node = current_node
            current_node = current_node.next
            if current_node == head:  # emulates do while loop
                break
        if distance - min_node.dist_increase_to_best < 0:
            break
        else:
            distance -= min_node.dist_increase_to_best
        new_node = Node(nearest_dict.get(min_index), min_index, min_node.next,
                        distance_matrix[min_index][min_node.next.index])
        min_node.next = new_node
        min_node.best_index = -1
        min_node.dist_increase_to_best = -1
        min_node.dist = distance_matrix[min_node.index][new_node.index]
        included_dict.update({new_node.index: new_node})
    return distance


def get_distance(start, finish):
    """":start tuple or list of 2 (latitude, longitude)
    :finish tuple or list of 2 (latitude, longitude)
    :returns geographical distance between"""
    radius = 6371.0
    lat1 = math.radians(start[0])
    lng1 = math.radians(start[1])
    lat2 = math.radians(finish[0])
    lng2 = math.radians(finish[1])
    d_lat = lat2 - lat1
    d_lng = lng2 - lng1
    x = math.pow(math.sin(d_lat / 2), 2) + math.cos(lat2) * math.cos(lat1) * math.pow(math.sin(d_lng / 2), 2)
    result = 2 * radius * math.asin(math.sqrt(x))
    return result


def filter_nearest():
    """"function: gets minimal info about breweries from database -> filters out unreachable breweries >
    makes distance matrix from leftovers and creates global dict {distance_matrix_index: brewery}"""
    global nearest_dict
    try:
        # get required data of breweries
        cur = sql.cursor()
        cur.execute("SELECT br.id, br.name, g.latitude, g.longitude "
                    "FROM breweries AS br "
                    "INNER JOIN geocodes AS g "
                    "ON br.id=g.brewery_id")
        data = cur.fetchall()
        cur.close()
        # filters out unreachable breweries
        nearest_dict = {0: (-1, "HOME", home)}
        count = 1
        for i in range(len(data)):
            if get_distance(home, (float(data[i][2]), float(data[i][3]))) <= full_distance / 2:
                brewery = (data[i][0], data[i][1], (float(data[i][2]), float(data[i][3])))
                nearest_dict.update({count: brewery})
                count += 1
        # makes distance matrix
        dist_mat = np.ndarray((count, count), float)
        for j in range(count):
            for i in range(count):
                if i > j:
                    dist_mat[j][i] = dist_mat[i][j] = get_distance(nearest_dict.get(i)[2], nearest_dict.get(j)[2])
        return dist_mat
    except Exception as ex:
        print(ex) # do something


if __name__ == "__main__":
    sql = mysql.connector.connect(host="localhost", user="root", passwd="", database="beer_test")
    home = (51.355468, 11.100790)
    full_distance = 2000
    head = Node((-1, "HOME", home), 0, None, 0.0, True)
    head.next = head
    nearest_dict = {}  # dict {distance_matrix_index: brewery}
    included_dict = {head.index: head}  # dict for Nodes included in route
    distance_matrix = filter_nearest()
    traveled = full_distance - make_route(full_distance)
    tests.test_route(head, traveled)
    print("traveled: " + str(traveled) + "km")

