import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd 
import numpy as np
from scipy import signal 


mus_loc = r"Analysis\data\arduino_square\microsecond\A0002CH1.CSV"
# mus_zoom_loc = "microsecondzoom\A0003CH1.CSV"
ms_loc = r"Analysis\data\arduino_square\onemillisecond\A0000CH1.CSV"
ten_mus_loc = r"Analysis\data\arduino_square\tenms\A0000CH1.CSV"
# ten_zoom_loc = "tenmszoom\A0001CH1.CSV"

# fpga_5 = "5musecondFPGA\A0000CH1.CSV"
# fpga_alt = "alternating\A0000CH1.CSV"
# 
# fpga_3_pulse = "mz_3_pulse\A0001CH1.CSV"
# fpga_3_pulse_zoom = "mz_3_pulse_zoomed\A0002CH1.CSV"

# ard_3_pulse = "ALL0004\A0004CH1.CSV"

def square_wave(sp, period, duration):
    '''Generates data points for a given sample period, period and duration.'''
    t = np.linspace(0, duration, 1000, endpoint = True)
    y = signal.square(2 * np.pi * (1/period) * t)
    return t, y


def calculate_x(y_values, x_scale, sp):
    '''Calculates x_values and x_ticks '''
    # print(len(y_values))
    x_values = np.arange(0, len(y_values)) * sp
    time = len(x_values) * sp
    
    x_ticks = np.arange(0, time, x_scale)
    # print(x_ticks)
    return x_values, x_ticks


def get_data(df):
    '''Gets data from csv and converts to x and y values.'''
    y_scale = float(df.iloc[4, 1])
    x_scale = float(df.iloc[7,1])
    # print(x_scale)
    y_units = df.iloc[3,1]
    sampling_period = float(df.iloc[10, 1])

    y_vals = df.iloc[ 16:, 0].values
    y_values = np.array(list(map(int,y_vals)))
    # print(y_values)
    x_values, ticks = calculate_x(y_values, x_scale, sampling_period)
    return x_values, y_values, ticks, sampling_period


def get_widths(x_data, y_data, ll, ul, del_lim):
    '''gets the width of the pulses given the data and the upper and lower
    limits over which the y_data should be analysed
    
    args:
     - x_data: x values for the dataset to be analysed.
     - y_data: y_values for the dataset to be analysed.
     - ll: the lower limit of the y_values to be analysed.
     - ul: the upper limit of the y_values to be analysed. '''
    

    index = np.where((ll <= y_data) & (y_data <= ul))
    widths = np.diff(x_data[index])
    del_index = np.where( widths <= del_lim)
    corrected_widths = np.delete(widths, del_index)[:-1]
    # print(f"1 mus pulse_widths = {corrected_widths}")
    his = [] 
    los = []
    for i in range(len(corrected_widths)):
        if i % 2 == 0:
            his.append(corrected_widths[i])

        elif i % 2 == 1:
            los.append(corrected_widths[i])
    
    avg_lo_t = np.mean(los)
    avg_hi_t = np.mean(his)

    return corrected_widths, avg_lo_t, avg_hi_t



data = pd.read_csv(mus_loc)
x, y, ticks, sp = get_data(data)
time = len(x) * sp
fig, axs = plt.subplots(nrows = 3, sharey=True, figsize=(7, 4))
axs[0].plot(x * 1e+6 , y, label="1 $\mu$s",color="blue")

# axs[0].hlines(np.mean(y), xmin = 0, xmax=7.5e-5)
avg = np.mean(y)
ll,ul = avg - 10, avg + 20


widths, avg_lo_t, avg_hi_t = get_widths(x, y, ll, ul ,del_lim=5e-7)
print(widths)
print(f"1 mus standard deviation {np.std(widths)}")
# print(widths)
print(f"avg_lo_t {avg_lo_t}")
print(f"avg_hi_t{avg_hi_t}")

avg_pulse = np.mean([avg_lo_t, avg_hi_t])
print(f"average pulse length 1mus = {avg_pulse}")
print(f"percentage error {((avg_pulse - 1e-6)/1e-6) * 100} %")
# axs[0].plot(x[index], y[index])
# print(f"index{index}")

# getting the average pulse height 
top_index = np.where(y > 78)
avg_hi = np.mean(y[top_index])
multi = 3.3/82.5
hi_y_std_err = np.std(y[top_index] * multi)/np.sqrt(len(y[top_index]))
print(f"average high height = {avg_hi * multi} \n")  # need to figure out the conversion for this because current units are useless. 
print(f"high error = {hi_y_std_err}")
# plotting expected square wave in red
verticals = np.linspace(0, 7.5e-5, 76) * 1e+6
tops = []
bottoms = []

for i in range(len(verticals)):
    if i % 2 == 0:
        tops.append(verticals[i])
    elif i % 2 == 1:
        bottoms.append(verticals[i])

sq_color = "red"
sq_alpha = 0.8
# def square_plot(ax)

axs[0].vlines(verticals, ymin = 0, ymax = 83, color=sq_color, alpha = sq_alpha)
for x_pos in tops:
    axs[0].hlines(83, x_pos, x_pos + 1, color=sq_color, alpha = sq_alpha)
    # axs[0].hlines(0, x_pos + 1e-6, x_pos + 2e-6, color=sq_color, alpha = sq_alpha)
for x_pos in bottoms:
    axs[0].hlines(0, x_pos, x_pos + 1, color=sq_color, alpha = sq_alpha)

axs[0].vlines(0,1,2, color="red", label="expected")


x_10, y_10, mus_ticks, sp= get_data(pd.read_csv(ten_mus_loc))
axs[1].plot(1e+6 * x_10, y_10, label="10$\mu$s", color="blue")

avg = np.mean(y)
ll,ul = avg - 20, avg + 20

widths, avg_lo_t, avg_hi_t = get_widths(x_10, y_10, ll, ul, del_lim = 5e-7)
print(widths)
print(f"10 mus standard deviation {np.std(widths)}")
print(f"avg_lo_t {avg_lo_t}")
print(f"avg_hi_t{avg_hi_t}")

avg_pulse = np.mean([avg_lo_t, avg_hi_t])
print(f"average pulse length 10mus = {avg_pulse}")
print(f"percentage error {((avg_pulse - 5e-6)/5e-6) * 100} %")
# axs[0].plot(x[index], y[index])
# print(f"index{index}")

# plotting expected square wave in red
verticals = (np.linspace(0, 8e-5, 9) + 1.5e-6) * 1e+6
# print(verticals)
tops = []
bottoms = []

for i in range(len(verticals)):
    if i % 2 == 0:
        tops.append(verticals[i])
    elif i % 2 == 1:
        bottoms.append(verticals[i])

sq_color = "red"
sq_alpha = 0.8
# def square_plot(ax)

axs[1].vlines(verticals, ymin = 0, ymax = 83, color=sq_color, alpha = sq_alpha)
for x_pos in tops:
    axs[1].hlines(83, x_pos, x_pos + 10, color=sq_color, alpha = sq_alpha)
    # axs[0].hlines(0, x_pos + 1e-6, x_pos + 2e-6, color=sq_color, alpha = sq_alpha)
for x_pos in bottoms:
    axs[1].hlines(0, x_pos, x_pos + 10, color=sq_color, alpha = sq_alpha)

axs[1].vlines(0,1,2, color="red", label="expected")


# x_10, y_10, mus_ticks, sp= get_data(pd.read_csv(ten_mus_loc))
# axs[1].plot(x_10, y_10, label="10$\mu$s", color="blue")



x_1, y_1, ms_ticks, sp = get_data(pd.read_csv(ms_loc))
axs[2].plot(x_1 * 1e+3, y_1, label="1ms", color="blue", alpha = 0.8)

# plotting expected square wave in red
verticals = np.linspace(0, 8e-3, 9) * 1e+3
tops = []
bottoms = []

for i in range(len(verticals)):
    if i % 2 == 0:
        tops.append(verticals[i])
    elif i % 2 == 1:
        bottoms.append(verticals[i])

sq_color = "red"
sq_alpha = 0.8
# def square_plot(ax)

axs[2].vlines(verticals, ymin = 0, ymax = 83, color=sq_color, alpha = sq_alpha)
for x_pos in tops:
    axs[2].hlines(83, x_pos, x_pos + 1, color=sq_color, alpha = sq_alpha)
    # axs[0].hlines(0, x_pos + 1e-6, x_pos + 2e-6, color=sq_color, alpha = sq_alpha)
for x_pos in bottoms:
    axs[2].hlines(0, x_pos, x_pos + 1, color=sq_color, alpha = sq_alpha)

axs[2].vlines(0,1,2, color="red", label="expected")


ll,ul = 84 - 6, 84 + 6
widths , avg_lo_t, avg_hi_t = get_widths(x_1, y_1, ll, ul, del_lim=5e-4)
print(f"1 ms standard deviation {np.std(widths)}")

print(f"avg_lo_t {avg_lo_t}")
print(f"avg_hi_t{avg_hi_t}")
print(avg_hi_t - avg_lo_t)
avg_pulse = np.mean([avg_lo_t, avg_hi_t])
print(f"average pulse length 1ms = {avg_pulse}")
print(f"percentage error {((avg_pulse - 1e-3)/1e-3) * 100} %")

# adjusting axes scales to remove scientific notation 
axs[0].set_xticks(ticks * 1e+6)
axs[0].grid()
axs[0].legend(loc = "upper right")
axs[0].set_xlabel("time ($\mu s$)")
axs[0].set_xlim((0,75))

axs[1].set_xticks(ticks * 1e+6)
axs[1].grid()
axs[1].legend(loc = "upper right")
axs[1].set_xlabel("time ($\mu s$)")
axs[1].set_xlim((0,75))

axs[2].set_xticks(ms_ticks * 1e+3)
axs[2].set_xlabel("time (ms)")
axs[2].grid()
axs[2].legend(loc="upper right")
axs[2].vlines([0, 1e-3, 2e-3], ymin = 0, ymax=80, color="red")
axs[2].set_xlim((0,7.5))

for ax in axs.flatten():
    ax.set_ylabel("Time (S)")


axs[0].get_yaxis().set_ticks([0])
axs[1].get_yaxis().set_ticks([0])
axs[2].get_yaxis().set_ticks([0])

fig.tight_layout()

# x_alt, y_alt, alt_ticks, sp=get_data(pd.read_csv(fpga_alt))
# x_pulse, y_pulse, pulse_ticks, sp = get_data(pd.read_csv(ard_3_pulse))

plt.show()