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
                    img.matrix[r, c] = int(column[c]) # int(int(column[c]) != 0)
            img.matrix = img.matrix[~(img.matrix == 0).all(1)]
            img.matrix = np.transpose(img.matrix)
            img.matrix = img.matrix[~(img.matrix == 0).all(1)]
            img.matrix = img.matrix.clip(max = 1)
            if img.matrix.size > 0:
                images.append(img)
    return start, end, images

def is_same_shape(obj1, obj2):
    if np.array_equal(obj1.matrix, obj2.matrix):
        return True
    else:
        return False


if __name__ == "__main__":

    path = "lvl2/"
    filname = "lvl2-4."

    start, end, images = parse_input(path+filname+"inp")
    print(start, end, images)

    # filter(lambda x: np.max(x.matrix) != 0, images);
    images = sorted(images, key = lambda x: x.timestamp)
    images = [x for x in images if np.max(x.matrix) > 0 and int(start) <= x.timestamp <= int(end)]

    with open(path+filname+"outp", "w") as of:

        img_result = []
        for img in images:
            occurs = [img]
            for other in images:
                if img is not other and other not in occurs and is_same_shape(img, other):
                    occurs.append(other)
            occurs = sorted(occurs, key=lambda x: x.timestamp)
            result = str(occurs[0].timestamp) + ' ' + str(occurs[-1].timestamp) + ' ' + str(len(occurs))

            if result not in img_result:
                img_result.append(result)
                of.write(result + '\n')
                print(result)

    pass
