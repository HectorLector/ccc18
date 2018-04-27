import os
import sys


def parse_input():
    with open("bla.txt", "r") as f:
        num = f.readline()
        content = f.readlines()

        print(content)
    return num


if __name__ == "__main__":
    num = parse_input()
    print(num)
