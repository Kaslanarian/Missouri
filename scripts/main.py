import threading, os


if __name__ == "__main__":
    thread1 = threading.Thread(target=lambda: os.system("python generate.py"))
    thread2 = threading.Thread(target=lambda: os.system("python script.py"))

    thread2.start()
    thread1.start()