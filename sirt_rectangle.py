import math
from typing import List, Tuple

# Type alias for coordinates
Coord = Tuple[int, int]

def cells_on_line(width: int, height: int, angle_deg: float, steps: int = 1000) -> List[Coord]:
    """Return list of grid cells that a line at angle_deg intersects."""
    cx = width / 2.0
    cy = height / 2.0
    angle_rad = math.radians(angle_deg)
    dx = math.cos(angle_rad)
    dy = math.sin(angle_rad)
    max_len = math.hypot(width, height)
    cells = []
    for step in range(-steps // 2, steps // 2 + 1):
        t = (step / (steps // 2)) * max_len
        x = cx + dx * t
        y = cy + dy * t
        xi = int(math.floor(x))
        yi = int(math.floor(y))
        if 0 <= xi < width and 0 <= yi < height:
            coord = (xi, yi)
            if not cells or cells[-1] != coord:
                cells.append(coord)
    return cells

def rotate_and_detect(width: int, height: int, anomalies: List[Coord]):
    for angle in range(0, 360, 18):
        cells = cells_on_line(width, height, angle)
        count = sum(1 for c in cells if c in anomalies)
        print(f"Angle {angle:3d} deg: {count} anomaly cell(s) detected")


def display_grid(width: int, height: int, anomalies: List[Coord]):
    print("\nGrid (X = anomaly):")
    for y in range(height):
        row = []
        for x in range(width):
            if (x, y) in anomalies:
                row.append('X')
            else:
                row.append('.')
        print(' '.join(row))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple SIRT-like anomaly detection")
    parser.add_argument("width", type=int, help="Rectangle width in pixels")
    parser.add_argument("height", type=int, help="Rectangle height in pixels")
    parser.add_argument("--anomaly", action="append", default=[], help="Anomaly cell as x,y (repeatable)")
    args = parser.parse_args()
    anomalies = []
    for item in args.anomaly:
        try:
            x_str, y_str = item.split(',')
            anomalies.append((int(x_str), int(y_str)))
        except ValueError:
            pass
    rotate_and_detect(args.width, args.height, anomalies)
    display_grid(args.width, args.height, anomalies)
