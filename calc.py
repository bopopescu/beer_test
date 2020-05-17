import mysql.connector
import math
import numpy as np


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
    full_distance = left = 2000
    nearest_dict = {}  # dict {distance_matrix_index: brewery}
    distance_matrix = filter_nearest()

    get_distance(home, (58.0, 30.0))
    # cur = sql.cursor()
    # cur.execute("SELECT * FROM categories")
    # data = cur.fetchall()
    # cur.close()
    # print(data)
