def get_center_of_bbox(bbox: list) -> tuple:
    x1, y1, x2, y2 = bbox
    return int((x1 + x2) / 2), int((y1 + y2) / 2)

def get_bbox_width(bbox: list) -> int:
    x1, y1, x2, y2 = bbox
    return int(x2 - x1)

def measure_distance(p1: tuple, p2: tuple) -> float:
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def measure_xy_distance(p1: tuple, p2: tuple) -> tuple:
    return (p1[0] - p2[0], p1[1] - p2[1])

def get_foot_position(bbox: list) -> tuple:
    x1, y1, x2, y2 = bbox
    return int((x1 + x2) / 2), int(y2)
