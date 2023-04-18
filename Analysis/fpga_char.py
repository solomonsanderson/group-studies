'''python script to plot and characterise the Intel Cylcone 10 FPGA using sqyuare waves'''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.ticker as ticker


def get_data(path):
    df = pd.read_csv(path)
    col1= df.iloc[19:, 0].values
    times = np.array(list(map(float, col1)))

    col2= df.iloc[19:, 1].values
    ch1 = np.array(list(map(float, col2)))

    return times, ch1


fig, axs = plt.subplots(2, sharex=True, figsize=(6,3))

axs[0].plot(*get_data(r"Analysis\data\fpga_square\tek0018CH1.csv"), color="blue", label="$0.5 \mu s$") # think this is 5mus
axs[1].plot(*get_data(r"Analysis\data\fpga_square\tek0017CH1.csv"), color="blue", label="$1 \mu s$") # think this is 1mus
# axs[2].plot(*get_data("tek0015C`H1.csv"), color="blue")


    
axs[0].set_xlim(-0.000005, 0.000005)

axs[1].set_xlim(-0.000005, 0.000005)


# plotting expected square wave in red
verticals = (np.linspace(-0.000005, 0.000005, 21) + 0.5e-6)
tops = []
bottoms = []

print(verticals)

for i in range(len(verticals)):
    if i % 2 == 0:
        tops.append(verticals[i])
    elif i % 2 == 1:
        bottoms.append(verticals[i])

sq_color = "red"
sq_alpha = 0.8
# def square_plot(ax)

axs[0].vlines(verticals, ymin = 0, ymax = 3.3, color=sq_color, alpha = sq_alpha)
for x_pos in tops:
    axs[0].hlines(3.3, x_pos + 0.5e-6 - 1.0e-6, x_pos + 1e-6 - 1.0e-6, color=sq_color, alpha = sq_alpha)
    # axs[0].hlines(0, x_pos + 1e-6, x_pos + 2e-6, color=sq_color, alpha = sq_alpha)
for x_pos in bottoms:
    axs[0].hlines(0, x_pos - 0.5e-6, x_pos,color=sq_color, alpha = sq_alpha)

axs[0].vlines(0.5e-6,1,2, color="red", label="expected")
axs[1].vlines(0,1,2, color="red", label="expected")


# plotting expected square wave in red
verticals = np.linspace(-0.000010, 0.000010, 21)
tops = []
bottoms = []

print(verticals)

for i in range(len(verticals)):
    if i % 2 == 0:
        tops.append(verticals[i])
    elif i % 2 == 1:
        bottoms.append(verticals[i])

sq_color = "red"
sq_alpha = 0.8
# def square_plot(ax)

axs[1].vlines(verticals, ymin = 0, ymax = 3.3, color=sq_color, alpha = sq_alpha)
for x_pos in tops:
    axs[1].hlines(3.3, x_pos, x_pos + 1e-6, color=sq_color, alpha = sq_alpha)
    # axs[0].hlines(0, x_pos + 1e-6, x_pos + 2e-6, color=sq_color, alpha = sq_alpha)
for x_pos in bottoms:
    axs[1].hlines(0, x_pos, x_pos + 1e-6, color=sq_color, alpha = sq_alpha)


for ax in axs.flatten():
    ax.set_ylabel("Voltage (V)")
    ax.legend(loc="upper right")

axs[1].set_xlabel("time ($\mu s$)")

scale_x = 1e-6


ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))
axs[1].xaxis.set_major_formatter(ticks_x)

hi_ll = 3.3-0.05
hi_ul = 3.3+0.05

x_1, y_1 = get_data(r"Analysis\data\fpga_square\tek0018CH1.csv")

hi_index = np.where((hi_ll <= y_1) & (y_1 <= hi_ul))
# print(f"\n 1ms index{hi_index}")
# axs[0].plot(x_1[hi_index], y_1[hi_index])
widths = np.diff(x_1[hi_index])
del_hi_index = np.where( widths <= 0.5e-6)
hi_corrected_widths = np.delete(widths, del_hi_index)[:-1]
# print(f"0.5 microseconds hi_pulse_widths = {hi_corrected_widths}")
print(f"average hi pulsewidths = {np.mean(hi_corrected_widths)}")

hi_y_avg = np.mean(y_1[hi_index])
hi_y_std_err = np.std(y_1[hi_index])/np.sqrt(len(y_1[hi_index]))

print(f"0.5 mus height = {hi_y_avg} +/- {hi_y_std_err} V")

lo_ll = 0 - 0.1
lo_ul = 0 + 0.1

lo_index = np.where((lo_ll <= y_1) & (y_1 <= lo_ul))
# print(f"\n lo 0.5mus index{lo_index}")
# axs[0].plot(x_1[lo_index], y_1[lo_index], color="orange", marker="o")
widths = np.diff(x_1[lo_index])
del_lo_index = np.where( widths <= 0.5e-6)
lo_corrected_widths = np.delete(widths, del_lo_index)[:-1]
# print(f"0.5 microseconds lo_pulse_widths = {lo_corrected_widths}")
print(f"average 0.5 mus lo pulsewidths = {np.mean(lo_corrected_widths)}")
print(f"hi lo diff = {np.mean(hi_corrected_widths) - np.mean(lo_corrected_widths)}")
avg_pulse_half_mus = np.mean([np.mean(lo_corrected_widths), np.mean(hi_corrected_widths)])
print(f"mean pulse widths 0.5 mus = {avg_pulse_half_mus}")
print(f"lo percentage error {((np.mean(lo_corrected_widths) - 0.5e-6)/0.e-6) * 100} % \n")
print(f"percentage error {((avg_pulse_half_mus - 0.5e-6)/0.5e-6) * 100} % \n")

lo_y_avg = np.mean(y_1[lo_index])
lo_y_std_err = np.std(y_1[lo_index])/np.sqrt(len(y_1[lo_index]))

print(f"0.5 mus height = {lo_y_avg} +/- {lo_y_std_err} V")

hi_y_avg = np.mean(y_1[hi_index])
hi_y_std_err = np.std(y_1[hi_index])/np.sqrt(len(y_1[hi_index]))

print(f"0.5 mus height = {hi_y_avg} +/- {hi_y_std_err} V")

# 1 microsecodn

x_2, y_2 = get_data(r"Analysis\data\fpga_square\tek0017CH1.csv")

hi_index = np.where((hi_ll <= y_2) & (y_2 <= hi_ul))
# print(f"\n 1ms index{hi_index}")
# axs[1].plot(x_2[hi_index], y_2[hi_index], marker="o")
widths = np.diff(x_2[hi_index])
del_hi_index = np.where( widths <= 0.5e-6)
hi_corrected_widths = np.delete(widths, del_hi_index)[:-1]
# print(f"0.5 microseconds hi_pulse_widths = {hi_corrected_widths}")



lo_ll = 0 - 0.1
lo_ul = 0 + 0.1

lo_index = np.where((lo_ll <= y_2) & (y_2 <= lo_ul))
# print(f"\n lo 1mus index{lo_index}")
# axs[1].plot(x_2[lo_index], y_2[lo_index], color="orange", marker="o")
widths = np.diff(x_2[lo_index])
del_lo_index = np.where( widths <= 0.5e-6)
lo_corrected_widths = np.delete(widths, del_lo_index)[:-1]
# print(f"0.5 microseconds lo_pulse_widths = {lo_corrected_widths}")
print(f"average lo pulsewidths = {np.mean(lo_corrected_widths)}")
print(f"average hi 1 mus pulsewidths = {np.mean(hi_corrected_widths)}")
print(f"hi lo diff = {np.mean(hi_corrected_widths) - np.mean(lo_corrected_widths)}")
avg_pulse_1mus = np.mean([np.mean(lo_corrected_widths), np.mean(hi_corrected_widths)])
print(f"mean pulse widths 1 mus = {avg_pulse_1mus}")
print(f"percentage error {((avg_pulse_1mus - 1e-6)/1e-6) * 100} %")

lo_y_avg = np.mean(y_2[lo_index])
lo_y_std_err = np.std(y_2[lo_index])/np.sqrt(len(y_2[lo_index]))

hi_y_avg = np.mean(y_2[hi_index])
hi_y_std_err = np.std(y_2[hi_index])/np.sqrt(len(y_2[hi_index]))

print(f"1 mus height = {lo_y_avg} +/- {lo_y_std_err} V")
print(f"1 mus height = {hi_y_avg} +/- {hi_y_std_err} V")

fig.tight_layout()

plt.show()  
