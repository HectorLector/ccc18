import os
import sys
import numpy as np


class Image:
    def __init__(self, timestamp, rows, cols):
        self.timestamp = timestamp
        self.num_rows = rows
        self.num_cols = cols
        self.matrix = np.empty([rows, cols])


def parse_input(file):
    images = []
    with open(file, "r") as f:
        start, end, num_pics = f.readline().split()

        for i in range(0, int(num_pics)):
            timestamp, rows, cols = f.readline().split()
            img = Image(int(timestamp), int(rows), int(cols))
            for r in range(0, int(rows)):
                column = f.readline().split()
                for c in range(0, int(cols)):
                    img.matrix[r, c] = int(column[c])
            images.append(img)
    return start, end, images


if __name__ == "__main__":

    path = "lvl1/"
    filname = "lvl1-4."

    start, end, images = parse_input(path+filname+"inp")
    print(start, end, images)

    # filter(lambda x: np.max(x.matrix) != 0, images);
    images = sorted(images, key = lambda x: x.timestamp)

    with open(path+filname+"outp", "w") as of:

        for img in images:
            if np.max(img.matrix) > 0 and int(start) <= img.timestamp <= int(end):
                print(img.timestamp)
                of.write(str(img.timestamp) + '\n')

    pass

# 1000 9999 3
# 3505 3 3
# 622 593 231
# 0 442 0
# 0 0 0
# 3593 3 3
# 0 0 0
# 0 0 0
# 0 0 0
# 4352 3 3
# 0 0 0
# 0 298 708
# 191 557 0