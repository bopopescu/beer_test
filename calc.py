import mysql.connector
import math


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
    print(x)
    result = 2 * radius * math.asin(math.sqrt(x))
    print(result)
    return result



if __name__ == "__main__":
    get_distance((56.0, 20.0), (58.0, 30.0))
    # sql = mysql.connector.connect(host="localhost", user="root", passwd="", database="beer_test")
    # cur = sql.cursor()
    # cur.execute("SELECT * FROM categories")
    # data = cur.fetchall()
    # cur.close()
    # print(data)

