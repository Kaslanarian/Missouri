import os, time

pwd1 = "."
pwd2 = "."
pwd3 = "."

while True:
    if "json" in [name[-4:] for name in os.listdir(pwd1)]:
        break
    print("waiting")

while True:
    time_file = dict([[
        os.path.getmtime(pwd1 + "/" + name),
        name,
    ] for name in os.listdir(pwd1)])
    target = time_file[sorted(time_file)[-1]]
    os.system("python {}/proc.py {}".format(pwd2, target))
    os.system("python {}/judger.py {}".format(pwd3, target))
    time.sleep(1)
