from time import sleep
from random import randint

t = 0

while True:
    with open("{}.json".format(t), "w") as f:
        f.write(str(randint(0, 100)))
    sleep(1)
    t += 1
