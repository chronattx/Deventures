import csv
import datetime as dt


def save_progress(progress: dict[str, str]):
    title = ["timestamp", "room", "x", "y"]

    try:
        with open("progress.csv", "r") as file:
            first = file.readline().strip()

            if first == "":
                raise FileNotFoundError
    except FileNotFoundError:
        with open("progress.csv", "w", newline="") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(title)
    finally:
        with open("progress.csv", "a", newline="") as file:
            writer = csv.DictWriter(file, delimiter=",", fieldnames=title)
            progress["timestamp"] = str(dt.datetime.now())
            writer.writerow(progress)


def get_progress() -> dict[str, str]:
    try:
        with open("progress.csv", "r") as file:
            items = list(csv.DictReader(file, delimiter=","))

            if not items:
                raise FileNotFoundError
            else:
                return items[-1]
    except FileNotFoundError:
        return {}
