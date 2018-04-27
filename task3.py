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
            img.matrix = img.matrix[~(img.matrix == 0).all(1)]
            img.matrix = np.transpose(img.matrix)
            img.matrix = img.matrix[~(img.matrix == 0).all(1)]
            img.matrix = img.matrix.clip(max=1)
            if img.matrix.size > 0:
                images.append(img)
    return start, end, images


def is_same_shape(obj1, obj2):
    if np.array_equal(obj1.matrix, obj2.matrix):
        return True
    else:
        return False


def find_increments(timestamps):
    incs = []
    for i in range(0, len(timestamps)):
        for j in range(i, len(timestamps)):
            new_inc = timestamps[j] - timestamps[i]
            if new_inc not in incs and new_inc > 0:
                incs.append(new_inc)
    return incs


def is_periodic(timestamps, increments, t_max):

    results = []
    t_max = max(timestamps)

    for period in increments:
        for i in range(0, len(timestamps)):
            count = 1
            t_val = timestamps[i]
            last = t_val
            while t_val <= t_max:
                t_val = t_val + period
                if t_val in timestamps:
                    count += 1
                    last = t_val
                else:
                    if t_val < t_max:
                        count = 0
                    break
            if count >= 4:
                results.append((period, timestamps[i], last, count))

    final_results = []
    for res in results:
        start = res[1]
        all_with_same_start = [x for x in results if x[1] == start]
        with_max_count = max(all_with_same_start, key=lambda x: x[3])

        if with_max_count not in final_results:
            final_results.append(with_max_count)

    final_results_final = []
    for res in final_results:
        end = res[2]
        all_with_same_end = [x for x in final_results if x[2] == end]
        with_max_count = max(all_with_same_end, key=lambda x: x[3])

        if with_max_count not in final_results_final:
            final_results_final.append(with_max_count)

    # final_results_final = sorted(final_results_final, lambda x: x[1])

    for res in final_results_final:
        end = res[2]
        where_end_is_start = [x for x in final_results_final if x[1] == end]
        if where_end_is_start:
            with_max_count = max(where_end_is_start, key=lambda x: x[3])
            for x in where_end_is_start:
                if x is not with_max_count:
                    final_results_final.remove(x)

    return final_results_final


if __name__ == "__main__":

    path = "lvl3/"
    filname = "lvl3-5."

    start, end, images = parse_input(path+filname+"inp")
    print(start, end, images)

    # filter(lambda x: np.max(x.matrix) != 0, images);
    images = sorted(images, key = lambda x: x.timestamp)
    #np.max(x.matrix) > 0 and
    images = [x for x in images if int(start) <= x.timestamp <= int(end)]

    with open(path+filname+"outp", "w") as of:

        shapes = []

        for img in images:
            occurs = [img]
            for other in images:
                if img is not other and other not in occurs and is_same_shape(img, other):
                    occurs.append(other)
            occurs = sorted(occurs, key=lambda x: x.timestamp)
            if occurs not in shapes and len(occurs) >= 4:
                shapes.append(occurs)

        periodics = []

        max_timestamps = []
        for shape in shapes:
            max_timestamps.append(max([x.timestamp for x in shape]))
        max_timestamp = max(max_timestamps)

        print(max_timestamp)

        for shape in shapes:
            timestamps = [x.timestamp for x in shape]
            increments = find_increments(timestamps)
            periodics += is_periodic(timestamps, increments, max_timestamp)

        periodics = sorted(periodics, key=lambda x: x[1])
        # print(periodics)

        for p in periodics:
            result = str(p[1]) + " " + str(p[2]) + " " + str(p[3]) + '\n'
            of.write(result)
            print(result)

        print(len(periodics))

    pass
