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
        raise Exception("distances does not macth")
