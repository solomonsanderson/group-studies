'''molasses_plot.py

A simple python script for plotting the output of the Arduino Due output with
the molasses sketch is loaded. 
'''

import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd


mc_ci_df = pd.read_csv("Analysis\data\molasses\mot_ci\mot_cf_01.csv")
time_ci = mc_ci_df["Time"][1:].astype(float)
ci = mc_ci_df["Channel A"][1:].astype(float)
mc = mc_ci_df["Channel B"][1:].astype(float)
fig, ax = plt.subplots(1)

mc_repump_df = pd.read_csv("Analysis\data\molasses\mot_repump\mot_ci_01.csv")
time_repump = mc_repump_df["Time"][1:].astype(float)
repump = mc_repump_df["Channel A"][1:].astype(float)

ax.plot(time_repump, repump, label="Repump", alpha=1, color="blue"    , marker="o" )
ax.plot(time_ci, mc, label = "MOT Coils", alpha=1, color="red"        , marker="o" )
ax.plot(time_ci, ci, label="Cooling Intensity", alpha=1, color="green", marker="o" )
ax.set_xlim(-2,23)
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Output (V)")
ax.legend()

ax.vlines([0, 1.75, 5, 6.5, 14, 18.25], ymin = 0, ymax=3.3)
fig.tight_layout()
fig.set_size_inches(5,2)
plt.show()