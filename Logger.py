import os

LOG_FILE = "log.txt"


def saveLog(log: str, file=LOG_FILE):
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write(log)
    else:
        with open(file, "a") as f:
            f.write("\n" + log)

    return True
