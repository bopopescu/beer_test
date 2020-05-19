from sys import exit
from calc import get_distance


def test_route(head, distance):
    dist = 0.0
    current = head
    while True:
        dist += get_distance(current.data[2], current.next.data[2])
        current = current.next
        if current == head:
            break
    if round(distance, 6) != round(dist, 6):  # millimeter accuracy
        print("distances does not macth")
        exit(255)
