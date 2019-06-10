"""
Get the timestamps of all claims and plot the cumulative number vs. time!
"""

import matplotlib.pyplot as plt
import numpy as np
import sqlite3

# Open the DB
db_file = "/home/brewer/local/lbry/lbryum-data/claims.db"
conn = sqlite3.connect(db_file)
c = conn.cursor()

# List for results
times = []

# Iterate over query results
i = 0
for t in c.execute("SELECT creation_timestamp FROM claim"):
    times.append(t)
    i = i + 1
    print(i)

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

# Sort the times and convert to a numpy array
times = np.sort(np.array(times))

# Remove pending ones
times = times[times >= 1E9]

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 14
plt.rc("text", usetex=True)

plt.figure(figsize=(15, 10))

plt.subplot(2, 1, 1)
times_in_days = (times - times.min())/86400.0
plt.plot(times_in_days,
            np.arange(len(times)), "k-", linewidth=1.5)
plt.ylabel("Cumulative number of claims")
plt.title("Total number of claims = {n}.".format(n=len(times)))
plt.xlim([0.0, times_in_days.max()])
plt.ylim(bottom=-100)
plt.gca().grid(True)
plt.gca().tick_params(labelright=True)



plt.subplot(2, 1, 2)
# Integers
days = times_in_days.astype("int64")
bin_width = 1.0
bins = np.arange(0, np.max(days)+1) - 0.5*bin_width # Bin edges including right edge of last bin
counts = plt.hist(days, bins, alpha=0.5, color="g", label="Raw",
                    width=bin_width, align="mid")[0]

# Compute 10-day moving average
moving_average = np.zeros(len(bins)-1)
for i in range(len(moving_average)):
    subset = counts[0:(i+1)]
    if len(subset) >= 10:
        subset = subset[-10:]
    moving_average[i] = np.mean(subset)
plt.plot(bins[0:-1] + 0.5*bin_width, moving_average, "k-",
            label="10-day moving average", linewidth=1.5)
#        plt.gca().set_yscale("log")
plt.xlim([0.0, times_in_days.max()])
plt.xlabel("Time (days since LBRY began)")
plt.ylabel("New claims added each day")
subset = counts[-30:]
plt.title("Recent average rate (last 30 days) = {n} claims per day.".\
            format(n=int(subset.mean())))
plt.gca().grid(True)
plt.gca().tick_params(labelright=True)
#        plt.gca().set_yticks([1.0, 10.0, 100.0, 1000.0, 10000.0])
#        plt.gca().set_yticklabels(["1", "10", "100", "1000", "10000"])
plt.legend()

#plt.savefig("claims.svg", bbox_inches="tight")
#print("Figure saved to claims.svg.")
plt.show()
