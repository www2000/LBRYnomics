from fetch_data import *
import json
import numpy
import time

# Needs an initial JSON file to bootstrap from

hour = 3600.0
day = 24*hour
week = 7*day

while True:
    f = open("subscriber_counts.json")
    t = json.load(f)["unix_time"]
    f.close()

    gap = time.time() - t
    print("It's been {d} days since the last update."\
                .format(d=np.round(gap/day, 4)))

    time.sleep(week - gap)
    subscriber_counts("") # <- Put auth token there as a string

