import sys

if __name__ == "__main__":
    file_name = sys.argv[1]
    with open(file_name, "r") as f:
        s = f.readlines()[0]
        print(s, " (in judger.py)")