import os

LOG_FILE = "log.txt"


def saveLog(log: str):
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("")
    else:
        with open(LOG_FILE, "a") as f:
            f.write("\n" + log)

    return True
