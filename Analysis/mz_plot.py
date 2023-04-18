'''
mz_plot.py

A python script to plot the output of the Arduino MKR Vidor Mach Zehnder pulses.
'''



import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from scipy import signal 
from itertools import groupby
from operator import itemgetter
import matplotlib.ticker as ticker

fig, ax = plt.subplots(2,2, sharey=True, figsize=(7,3.5))
print(ax)
path3 =  r"Analysis\data\mach_zehnder\tek0003ALL.csv" # bad sample rate. 3 pulses
path4 =  r"Analysis\data\mach_zehnder\tek0004CH1.csv" # bad sample rate. 3 pulses
path5 =  r"Analysis\data\mach_zehnder\tek0005CH1.csv" # bad sample rate. 3 pulses
path10 = r"Analysis\data\mach_zehnder\tek0010CH1.csv" # wrong order, sample rate good
path11 = r"Analysis\data\mach_zehnder\tek0011CH1.csv" # good sample rate, 3 pulses
path12 = r"Analysis\data\mach_zehnder\tek0012CH1.csv" # wrong order, sample rate good
path13 = r"Analysis\data\mach_zehnder\tek0013CH1.csv" # has repeated waves, use for getting interval data
path15 = r"Analysis\data\mach_zehnder\tek0015CH1.csv" # has repeated waves, use for getting interval data
path3 = path11


def get_data(path):
    '''
    Args:
        path, string - the path of the data file to be loaded
    Returns:
        times, numpy array - array of times of data points
        ch1, numpy array - array of y values
    '''


    df = pd.read_csv(path)
    col1= df.iloc[19:, 0].values
    times = np.array(list(map(float, col1)))

    col2= df.iloc[19:, 1].values
    ch1 = np.array(list(map(float, col2)))

    return times, ch1


def get_range(arr1, arr2, ll, ul):
    '''
    Gets the x or y values in between 2 limits

    Args:
        arr1, array - array of values to search within
        arr2, array - array to get values of
        ll, float - lower limit of search
        ul, float - upper limit of search
    '''

    
    time_index = np.where((ll < arr1) & (arr1 < ul))
    ch_index = np.where((ll < arr1) & (arr1 < ul))

    time_data = arr1[time_index]
    ch_data = arr2[ch_index]
    return time_data, ch_data


# data = get_data(pulse_path)
# print(data)
data3 = get_data(path3)
data4 = get_data(path4)
data5 = get_data(path5)


lo = -1
hi = 1
full_range = get_range(data3[0], data3[1], lo, hi)
pi_2_1 = get_range(data3[0], data3[1], -0.001027 - 0.0001, -0.00102735 + 0.0001) # 0.00011
pi = get_range(data3[0], data3[1], -5.49986e-6 - 0.0001,-5.49986e-6 + 0.0001 )
pi_2_2 = get_range(data3[0], data3[1], 0.00101619 - 0.0001, 0.00101619 + 0.0001)

### for data "tek0011CH1.csv"
ax[0,0].plot(*full_range, label="full sequence", color="blue")
ax[0,1].plot(*pi_2_1, label="$\\frac{\pi}{2}$", color="blue")
ax[1,0].plot(*pi, label="$\\pi$", color="blue")
ax[1,1].plot(*pi_2_2, label="$\\frac{\pi}{2}$", color="blue")

ax[0,1].vlines([-1.06075e-5 - 1e-3,-1.06075e-5 - 1e-3 - 5e-6], ymin= 0, ymax=3.3, color="red")
ax[0,1].hlines(0, xmin = -0.00112702, xmax = -1.06075e-5 - 1e-3 - 5e-6, color="red")
ax[0,1].hlines(3.3, xmin = -1.06075e-5 - 1e-3 - 5e-6,  xmax= -1.06075e-5 - 1e-3, color="red", label="expected")
ax[0,1].hlines(0, xmin = -1.06075e-5 - 1e-3 - 5e-6,  xmax= -0.000925682, color="red")
# ax[0,1].hlines(0, xmin = -0.00112702, xmax = -1.06075e-5 - 1e-3)


ax[1,0].vlines([-1.06075e-5, -1.06075e-5 + 10e-6],ymin= 0, ymax=3.3, color="red")
ax[1,0].hlines(3.3, xmin=-1.06075e-5, xmax=-1.06075e-5 + 10e-6, color="red", label="expected")
ax[1,0].hlines(0, xmax=-1.06075e-5, xmin=-1e-4, color="red")
ax[1,0].hlines(0, xmax=0.8e-4, xmin=-1.06075e-5 + 10e-6, color="red")


ax[1,1].hlines(3.3, xmin=-1.06075e-5 + 1e-3, xmax=-1.06075e-5 + 1e-3 + 5e-6, color="red", label="expected")
ax[1,1].vlines([-1.06075e-5 + 1e-3,-1.06075e-5 + 1e-3 + 5e-6], ymin= 0, ymax=3.3, color="red")
ax[1,1].hlines(0, xmin=-1.06075e-5 + 1e-3 + 5e-6, xmax=1.11e-3, color="red")
ax[1,1].hlines(0, xmin=0.91e-3, xmax=-1.06075e-5 + 1e-3, color="red")



for a in ax.flatten():
    a.legend(loc="upper right")
    a.set_xlabel("time (ms)")
    # a.set_ylabel("Output (V)")
    a.ticklabel_format(axis="x", style="scientific", scilimits=[-3,6])

ax[0,0].set_ylabel("Output (V)")
ax[1,0].set_ylabel("Output (V)")

hi_ll = 3.3 - 0.1
hi_ul = 3.3 + 0.1

hi_index = np.where((hi_ll <= data3[1]) & (data3[1] <= hi_ul))

widths = np.diff(data3[0][hi_index])
del_index = np.where( widths <= 2e-6)


indicies = [list(map(itemgetter(1), g)) for k, g in groupby(enumerate(del_index[0]), lambda x: x[0]-x[1])]

pws = []
for i in indicies:
    pw = np.sum(widths[i]) + 1e-6
    pws.append(pw)

print(f"pulse widths {pws} s")

print(widths)
lo_widths = np.delete(widths, del_index)[:-1]
print(f"interval widths = {lo_widths}")
print(f"mean widths = {np.mean([1.0144e-03,  1.0148e-03])}")


scale_x = 1e-3
ticks_x= ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))
for ax in ax.flatten():
    ax.xaxis.set_major_formatter(ticks_x)


# sort this atrocity if there is time 
path13_los = np.array([0.000989, 0.001015, 0.001001, 0.000989, 0.001015, 0.001, 0.000989])
path15_los = np.array([0.001015, 0.001, 0.000989, 0.0010151, 0.0009999, 0.000989, 0.001015])
path11_los = np.array([0.0010144, 0.0010148])
low_widths = np.concatenate((path13_los, path15_los, path11_los))
print(low_widths)
avg_low_widths = np.mean(low_widths)
std_dev = np.std(low_widths)
print(f" average interval = {avg_low_widths} s, \n standard deviation of lo widths = {std_dev * 1000} ms ")


path12_his = np.array([1.1000000000000027e-05, 5.7999999999999995e-06, 5.7999999999998996e-06])
path11_his = np.array([5.7999999999998996e-06, 1.06e-05, 5.39999999999989e-06])
path10_his = np.array([1.1000000000000027e-05, 5.4e-06, 5.39999999999989e-06])
path9_his = np.array( [5.800000000000116e-06, 5.800000000000116e-06, 1.1e-05, 5.800000000000116e-06, 5.400000000000107e-06])
his = np.concatenate([path9_his, path10_his, path11_his, path12_his])

pi_pulses = []
pi_2_pulses = []

for i in his:
    if i < 6e-6:
        pi_2_pulses.append(i)
    
    else:
        pi_pulses.append(i)

pi_2_avg = np.mean(pi_2_pulses)
pi_2_std = np.std(pi_2_pulses)

pi_avg = np.mean(pi_pulses)
pi_std = np.std(pi_pulses)

print(f"pi/2 average length = {pi_2_avg * 1e+6}, std_dev = {pi_2_std * 1e+6}")
print(f"pi average_length = {pi_avg * 1e+6}, std_dev = {pi_std * 1e+6}")

fig.tight_layout()
plt.show()

