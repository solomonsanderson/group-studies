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

print(f"repump{repump}")

repump = np.array(repump)

repump_ind_1 = np.where((0 < repump) & (repump < 1))
repump_ind_2 = np.where((2 < repump) & (repump < 3))
repump_ind_3 = np.where((1.4 < repump) & (repump< 1.8))
repump_ind_4 = np.where((0.9 < repump) & (repump < 1.3))

repump_1, repump_2, repump_3, repump_4 = repump[repump_ind_1], repump[repump_ind_2], repump[repump_ind_3], repump[repump_ind_4]

time_ci = np.array(time_ci)
time_repump=np.array(time_repump)
rp_t_1 = time_repump[repump_ind_1]
rp_t_2 = time_repump[repump_ind_2]
rp_t_3 = time_repump[repump_ind_3]
rp_t_4 = time_repump[repump_ind_4]

ci_1_ind = np.where((0 < ci) & (ci < 1))[0]
ci_2_ind = np.where((2 < ci) & (ci < 3))
ci_3_ind = np.where((1.4 < ci) & (ci < 1.8))
ci_4_ind = np.where((0.9 < ci) & (ci < 1.3))

ci = np.array(ci)
ci_1 =  ci[ci_1_ind]
ci_1, ci_2, ci_3, ci_4 = ci[ci_1_ind], ci[ci_2_ind], ci[ci_3_ind], ci[ci_4_ind]

ci_t_1 = time_ci[ci_1_ind]
ci_t_2 = time_ci[ci_2_ind]
ci_t_3 = time_ci[ci_3_ind]
ci_t_4 = time_ci[ci_4_ind]


mc = np.array(mc)
mc_hi_ind = np.where((3 < mc) & (mc< 3.5))
mc_lo_ind = np.where((-0.5 < mc) & (mc < 0.5))

mc_lo = mc[mc_lo_ind]
mc_hi = mc[mc_hi_ind]

mc_lo_t = time_ci[mc_lo_ind]
mc_hi_t = time_ci[mc_hi_ind]
print(mc_hi_t)
# ax.plot(mc_hi_t, mc_hi)
print(f"mc_hi_t{mc_hi_t[-1] - mc_hi_t[0]}")

def percent_adj(range_ll, range_ul, value):
    rang = range_ul - range_ll
    adj_value = value - range_ll
    adj_percentage = adj_value / rang * 100 
    return adj_percentage


print(f"percentage {percent_adj(0.55, 2.75, np.mean(ci_1))}")
print(f"percentage {percent_adj(0.55, 2.75, np.mean(ci_2))}")
print(f"percentage {percent_adj(0.55, 2.75, np.mean(ci_3))}")
print(f"average CI voltage 0: {np.mean(ci_1)}, 100%: {np.mean(ci_2)}, 45%: {np.mean(ci_3)}, 30%: {np.mean(ci_4)}")


print(f"average Repump voltage 0%: {np.mean(repump_1)},  100%: {np.mean(repump_2)}, 45%: {np.mean(repump_3)}, 30% {np.mean(repump_4)}")
print(f"percentage {percent_adj(0.55, 2.75, np.mean(repump_1))}")
print(f"percentage {percent_adj(0.55, 2.75, np.mean(repump_2))}")
print(f"percentage {percent_adj(0.55, 2.75, np.mean(repump_3))}")

print(f"average MOT low voltage {np.mean(mc_lo)}, high voltage {np.mean(mc_hi)}")
print(f"percentage {percent_adj(0, 3.3, np.mean(mc_lo))}")
print(f"percentage {percent_adj(0, 3.3, np.mean(mc_hi))}")



rp, = ax.plot(time_repump, repump, label="Repump", alpha=0.6, color="blue"    , )
mot, = ax.plot(time_ci, mc, label = "MOT Coils", alpha=0.6, color="red"        , )
cool, =ax.plot(time_ci, ci, label="Cooling Intensity", alpha=0.6, color="green", )

#expected mot coils
exp_mot, =ax.plot([-5, 0, 0, 1.5, 1.5, 25], [0, 0, 3.3, 3.3,  0, 0], linestyle = "--", label = "Expected MOT coils", color= "darkred", alpha=0.6)
# expected repump
exp_cool, = ax.plot([-5, 0, 0, 1.5, 1.5, 5, 5, 6.5, 6.5, 18, 18, 25], [0.55, 0.55, 2.75, 2.75, 0.55 , 0.55, 1.54, 1.54, 1.21, 1.21 ,0.55, 0.55], label  = "Expected cooling intensity",linestyle ="--", color="darkgreen", alpha=0.6)
exp_rp, = ax.plot([-5, 0, 0, 1.5, 1.5, 5, 5, 6.5, 6.5, 14, 14, 25], [0.55, 0.55, 2.75, 2.75, 0.55 , 0.55, 1.54, 1.54, 1.21, 1.21 ,0.55, 0.55], label  = "Expected repump ",linestyle ="--", color="darkblue", alpha=0.6)
#expected cooling

ax.set_xlim(-2,23)
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Output (V)")
legend1 = ax.legend(handles = [exp_mot, exp_cool, exp_rp], loc = (0.25,0.75), frameon = False)
legend2 = ax.legend(handles = [rp, mot, cool], loc=(0.67,0.75), frameon = False)
plt.gca().add_artist(legend1)
plt.gca().add_artist(legend2)

# ax.vlines([0, 1.75, 5, 6.5, 14, 18.25], ymin = 0, ymax=3.3)
fig.tight_layout()
fig.set_size_inches(6.3,3.4)

plt.show()